import asyncio
import base64
import logging
import os
from builtins import anext
from typing import Any
import httpx

from agora.rtc.rtc_connection import RTCConnection, RTCConnInfo
from aiohttp import WSServerHandshakeError
from attr import dataclass

from agora_realtime_ai_api.rtc import Channel, ChatMessage, RtcEngine, RtcOptions

from .logger import setup_logger
from .realtime.struct import ErrorMessage, FunctionCallOutputItemParam, InputAudioBufferCommitted, \
    InputAudioBufferSpeechStarted, InputAudioBufferSpeechStopped, InputAudioTranscription, ItemCreate, ItemCreated, \
    ItemAdded, ItemDone, ItemInputAudioTranscriptionCompleted, RateLimitsUpdated, ResponseAudioDelta, ResponseAudioDone, \
    ResponseAudioTranscriptDelta, ResponseAudioTranscriptDone, ResponseContentPartAdded, ResponseContentPartDone, \
    ResponseCreate, ResponseCreated, ResponseDone, ResponseFunctionCallArgumentsDelta, \
    ResponseFunctionCallArgumentsDone, ResponseOutputItemAdded, ResponseOutputItemDone, SemanticVADUpdateParams, ServerVADUpdateParams, \
    SessionUpdate, SessionUpdateParams, SessionUpdated, SystemMessageItemParam, Voices, to_json, Usage, InputTokenDetails, OutputTokenDetails, \
    CachedTokensDetails, UserMessageItemParam, ResponseOutputAudioDelta, ResponseOutputAudioTranscriptDelta, ResponseOutputAudioTranscriptDone, \
    ResponseOutputAudioDone, AudioConfig, InputAudioConfig, OutputAudioConfig, PCMAudioFormat
from .realtime.connection import RealtimeApiConnection
from .tools import ClientToolCallResponse, ToolContext
from .utils import PCMWriter
from dataclasses import asdict

# Set up the logger with color and timestamp support
logger = setup_logger(name=__name__, log_level=logging.INFO)


def _monitor_queue_size(queue: asyncio.Queue, queue_name: str, threshold: int = 5) -> None:
    queue_size = queue.qsize()
    if queue_size > threshold:
        logger.warning(f"Queue {queue_name} size exceeded {threshold}: current size {queue_size}")


async def wait_for_remote_user(channel: Channel) -> int:
    remote_users = list(channel.remote_users.keys())
    if len(remote_users) > 0:
        return remote_users[0]

    future = asyncio.Future[int]()

    channel.once("user_joined", lambda conn, user_id: future.set_result(user_id))

    try:
        # Wait for the remote user with a timeout of 30 seconds
        remote_user = await asyncio.wait_for(future, timeout=15.0)
        return remote_user
    except KeyboardInterrupt:
        future.cancel()
        
    except Exception as e:
        logger.error(f"Error waiting for remote user: {e}", extra={'channelName': channel.channelId})
        raise


def get_callback_base_url(channel_name: str) -> str:
    if "online" in channel_name:
        return os.environ.get("WEB_END_CALLBACK_URL")
    else:
        return os.environ.get("TEST_WEB_END_CALLBACK_URL")


@dataclass(frozen=True, kw_only=True)
class InferenceConfig:
    system_message: str | None = None
    turn_detection: ServerVADUpdateParams | SemanticVADUpdateParams | None = None  # MARK: CHECK!
    voice: Voices | None = None
    azure_base_url: str
    azure_api_key: str
    azure_deployment: str
    azure_api_version: str


class RealtimeKitAgent:
    engine: RtcEngine
    channel: Channel
    connection: RealtimeApiConnection
    audio_queue: asyncio.Queue[bytes] = asyncio.Queue()

    message_queue: asyncio.Queue[ResponseAudioTranscriptDelta] = (
        asyncio.Queue()
    )
    message_done_queue: asyncio.Queue[ResponseAudioTranscriptDone] = (
        asyncio.Queue()
    )
    tools: ToolContext | None = None

    _client_tool_futures: dict[str, asyncio.Future[ClientToolCallResponse]]

    @classmethod
    async def setup_and_run_agent(
        cls,
        *,
        engine: RtcEngine,
        options: RtcOptions,
        inference_config: InferenceConfig,
        tools: ToolContext | None,
    ) -> None:
        channel = engine.create_channel(options)
        logger.info(f"Conversation used account baseUrl: {inference_config.azure_base_url} "
                    f"api_key:{inference_config.azure_api_key} "
                    f"deployment:{inference_config.azure_deployment} "
                    f"api_version:{inference_config.azure_api_version}", extra={'channelName': channel.channelId})
        await channel.connect()
        try:
            async with RealtimeApiConnection(
                base_uri=inference_config.azure_base_url,
                api_key=inference_config.azure_api_key,
                is_azure=True,
                api_verison=inference_config.azure_api_version,
                deployment=inference_config.azure_deployment,
                # 貌似是开启增强日志
                verbose=False,
            ) as connection:
                await connection.send_request(
                    SessionUpdate(
                        session=SessionUpdateParams(
                            type="realtime",  # GA API: specify session type for speech-to-speech
                            tools=tools.model_description() if tools else [],
                            tool_choice="auto",
                            # GA API: audio configuration moved to audio object
                            audio=AudioConfig(
                                input=InputAudioConfig(
                                    format=PCMAudioFormat(),
                                    turn_detection=inference_config.turn_detection,
                                    transcription=InputAudioTranscription(model="whisper-1", language="en"),
                                    # todo noise_reduction 需要前端传递用户使用的是耳机还是设备麦克风来判断降噪类型
                                ),
                                output=OutputAudioConfig(
                                    format=PCMAudioFormat(),
                                    voice=inference_config.voice if inference_config.voice else "alloy"
                                )
                            ),
                            instructions=inference_config.system_message,
                            model=os.environ.get("OPENAI_MODEL", "gpt-realtime-mini"),
                            output_modalities=["audio"],
                            max_output_tokens="inf"
                        )
                    )
                )
                start_session_message = await anext(connection.listen())
                # assert isinstance(start_session_message, messages.StartSession)
                if isinstance(start_session_message, SessionUpdated):
                    logger.info(f"Session started: {start_session_message.session.id} "
                                f"model: {start_session_message.session.model}",
                                extra={'channelName': channel.channelId})
                elif isinstance(start_session_message, ErrorMessage):
                    logger.info(f"Error: {start_session_message.error}", extra={'channelName': channel.channelId})

                agent = cls(
                    connection=connection,
                    tools=tools,
                    channel=channel,
                    inference_config=inference_config
                )
                await agent.run()
        except WSServerHandshakeError as error:
            logger.error(error)
            if error.status == 401:
                # 401 feedback web-end resource is not unavailable
                await asyncio.create_task(cls.connection_fail_feedback(channel.channelId,
                                                                       inference_config.azure_base_url,
                                                                       inference_config.azure_deployment))
        finally:
            await channel.disconnect()
            await connection.close()

    def __init__(
        self,
        *,
        connection: RealtimeApiConnection,
        tools: ToolContext | None,
        channel: Channel,
        inference_config: InferenceConfig
    ) -> None:
        self.connection = connection
        self.tools = tools
        self._client_tool_futures = {}
        self.channel = channel
        self.subscribe_user = None
        self.write_pcm = os.environ.get("WRITE_AGENT_PCM", "false") == "true"
        self.token_usage = None
        self.inference_config = inference_config
        logger.info(f"Write PCM: {self.write_pcm}", extra={'channelName': channel.channelId})

    async def run(self) -> None:
        try:

            def log_exception(t: asyncio.Task[Any]) -> None:
                if not t.cancelled() and t.exception():
                    logger.error("unhandled exception", exc_info=t.exception(),
                                 extra={'channelName': self.channel.channelId})

            def on_stream_message(agora_local_user, user_id, stream_id, data, length) -> None:
                logger.info(f"Received stream message with length: {length}",
                            extra={'channelName': self.channel.channelId})

            self.channel.on("stream_message", on_stream_message)

            logger.info("Waiting for remote user to join", extra={'channelName': self.channel.channelId})
            self.subscribe_user = await wait_for_remote_user(self.channel)
            logger.info(f"Subscribing to user {self.subscribe_user}", extra={'channelName': self.channel.channelId})
            await self.channel.subscribe_audio(self.subscribe_user)

            async def on_user_left(
                agora_rtc_conn: RTCConnection, user_id: int, reason: int
            ):
                logger.info(f"User left: {user_id}", extra={'channelName': self.channel.channelId})
                if self.subscribe_user == user_id:
                    self.subscribe_user = None
                    logger.info("Subscribed user left, disconnecting", extra={'channelName': self.channel.channelId})
                    await self.channel.disconnect()

            self.channel.on("user_left", on_user_left)

            disconnected_future = asyncio.Future[None]()

            def callback(agora_rtc_conn: RTCConnection, conn_info: RTCConnInfo, reason):
                logger.info(f"Connection state changed: {conn_info.state}", extra={'channelName': self.channel.channelId})
                if conn_info.state == 1:
                    if not disconnected_future.done():
                        disconnected_future.set_result(None)

            self.channel.on("connection_state_changed", callback)

            asyncio.create_task(self.rtc_to_model()).add_done_callback(log_exception)
            asyncio.create_task(self.model_to_rtc()).add_done_callback(log_exception)

            asyncio.create_task(self._process_model_messages()).add_done_callback(log_exception)
            asyncio.create_task(self.init_greet()).add_done_callback(log_exception)
            await disconnected_future
            # send feedback to web-end if token not none
            logger.info(f"Total token usage: {self.token_usage}", extra={'channelName': self.channel.channelId})
            await asyncio.create_task(self.conversation_end_feedback())
            logger.info("Agent finished running", extra={'channelName': self.channel.channelId})
        except asyncio.CancelledError:
            logger.info("Agent cancelled", extra={'channelName': self.channel.channelId})
        except Exception as e:
            logger.error(f"Error running agent: {e}", extra={'channelName': self.channel.channelId})
            raise

    async def rtc_to_model(self) -> None:
        while self.subscribe_user is None or self.channel.get_audio_frames(self.subscribe_user) is None:
            await asyncio.sleep(0.1)

        audio_frames = self.channel.get_audio_frames(self.subscribe_user)

        # Initialize PCMWriter for receiving audio
        pcm_writer = PCMWriter(prefix="rtc_to_model", write_pcm=self.write_pcm)

        try:
            async for audio_frame in audio_frames:
                # Process received audio (send to model)
                _monitor_queue_size(self.audio_queue, "audio_queue")
                await self.connection.send_audio_data(audio_frame.data)

                # Write PCM data if enabled
                await pcm_writer.write(audio_frame.data)

                await asyncio.sleep(0)  # Yield control to allow other tasks to run

        except asyncio.CancelledError:
            # Write any remaining PCM data before exiting
            await pcm_writer.flush()
            raise  # Re-raise the exception to propagate cancellation

    async def model_to_rtc(self) -> None:
        # Initialize PCMWriter for sending audio
        pcm_writer = PCMWriter(prefix="model_to_rtc", write_pcm=self.write_pcm)

        try:
            while True:
                # Get audio frame from the model output
                frame = await self.audio_queue.get()

                # Process sending audio (to RTC)
                await self.channel.push_audio_frame(frame)

                # Write PCM data if enabled
                await pcm_writer.write(frame)

        except asyncio.CancelledError:
            # Write any remaining PCM data before exiting
            await pcm_writer.flush()
            raise  # Re-raise the cancelled exception to properly exit the task

    async def handle_function_call(self, message: ResponseFunctionCallArgumentsDone) -> None:
        function_call_response = await self.tools.execute_tool(message.name, message.arguments)
        logger.info(f"Function call response: {function_call_response}", extra={'channelName': self.channel.channelId})
        await self.connection.send_request(
            ItemCreate(
                item = FunctionCallOutputItemParam(
                    call_id=message.call_id,
                    output=function_call_response.json_encoded_output
                )
            )
        )
        await self.connection.send_request(
            ResponseCreate()
        )

    def accumulate_token(self, usage: Usage):
        if self.token_usage is None:
            cached_tokens_details = CachedTokensDetails(
                text_tokens=0,
                audio_tokens=0
            )
            input_details = InputTokenDetails(
                cached_tokens=0,
                text_tokens=0,
                audio_tokens=0,
                cached_tokens_details=cached_tokens_details
            )
            output_details = OutputTokenDetails(
                text_tokens=0,
                audio_tokens=0
            )
            self.token_usage = Usage(
                total_tokens=0,
                input_tokens=0,
                output_tokens=0,
                input_token_details=input_details,
                output_token_details=output_details
            )
        self.token_usage.total_tokens += usage.total_tokens
        self.token_usage.input_tokens += usage.input_tokens
        self.token_usage.output_tokens += usage.output_tokens
        self.token_usage.input_token_details.cached_tokens += usage.input_token_details.cached_tokens
        self.token_usage.input_token_details.text_tokens += usage.input_token_details.text_tokens
        self.token_usage.input_token_details.audio_tokens += usage.input_token_details.audio_tokens
        self.token_usage.input_token_details.cached_tokens_details.text_tokens += usage.input_token_details.cached_tokens_details.text_tokens
        self.token_usage.input_token_details.cached_tokens_details.audio_tokens += usage.input_token_details.cached_tokens_details.audio_tokens
        self.token_usage.output_token_details.text_tokens += usage.output_token_details.text_tokens
        self.token_usage.output_token_details.audio_tokens += usage.output_token_details.audio_tokens

    async def _process_model_messages(self) -> None:
        async for message in self.connection.listen():
            # logger.info(f"Received message {message=}")
            match message:
                # GA API events (new event names)
                case ResponseOutputAudioDelta():
                    # logger.info("Received audio message")
                    self.audio_queue.put_nowait(base64.b64decode(message.delta))
                    logger.debug(f"TMS:ResponseOutputAudioDelta: response_id:{message.response_id},item_id: {message.item_id}")
                case ResponseOutputAudioTranscriptDelta():
                    # logger.info(f"Received text message {message=}")
                    asyncio.create_task(self.channel.chat.send_message(
                        ChatMessage(
                            message=to_json(message), msg_id=message.item_id
                        )
                    ))
                case ResponseOutputAudioTranscriptDone():
                    logger.info(f"Text message done: {message=}", extra={'channelName': self.channel.channelId})
                    asyncio.create_task(self.channel.chat.send_message(
                        ChatMessage(
                            message=to_json(message), msg_id=message.item_id
                        )
                    ))
                case ResponseOutputAudioDone():
                    logger.info(f"ResponseOutputAudioDone: response_id:{message.response_id}, item_id:{message.item_id}", extra={'channelName': self.channel.channelId})
                    pass
                # Beta API events
                # case ResponseAudioDelta():
                #     # logger.info("Received audio message")
                #     self.audio_queue.put_nowait(base64.b64decode(message.delta))
                #     # loop.call_soon_threadsafe(self.audio_queue.put_nowait, base64.b64decode(message.delta))
                #     logger.debug(f"TMS:ResponseAudioDelta: response_id:{message.response_id},item_id: {message.item_id}")
                # case ResponseAudioTranscriptDelta():
                #     # logger.info(f"Received text message {message=}")
                #     asyncio.create_task(self.channel.chat.send_message(
                #         ChatMessage(
                #             message=to_json(message), msg_id=message.item_id
                #         )
                #     ))
                # case ResponseAudioTranscriptDone():
                #     logger.info(f"Text message done: {message=}", extra={'channelName': self.channel.channelId})
                #     asyncio.create_task(self.channel.chat.send_message(
                #         ChatMessage(
                #             message=to_json(message), msg_id=message.item_id
                #         )
                #     ))
                case InputAudioBufferSpeechStarted():
                    await self.channel.clear_sender_audio_buffer()
                    # clear the audio queue so audio stops playing
                    while not self.audio_queue.empty():
                        self.audio_queue.get_nowait()
                    logger.info(f"TMS:InputAudioBufferSpeechStarted: item_id: {message.item_id}", extra={'channelName': self.channel.channelId})
                case InputAudioBufferSpeechStopped():
                    logger.info(f"TMS:InputAudioBufferSpeechStopped: item_id: {message.item_id}", extra={'channelName': self.channel.channelId})
                    pass
                case ItemInputAudioTranscriptionCompleted():
                    logger.info(f"ItemInputAudioTranscriptionCompleted: {message=}", extra={'channelName': self.channel.channelId})
                    asyncio.create_task(self.channel.chat.send_message(
                        ChatMessage(
                            message=to_json(message), msg_id=message.item_id
                        )
                    ))
                #  InputAudioBufferCommitted
                case InputAudioBufferCommitted():
                    logger.info(f"InputAudioBufferCommitted: {message=}", extra={'channelName': self.channel.channelId})
                    pass
                # Beta API events
                # case ItemCreated():
                #     logger.info(f"ItemCreated: {message=}", extra={'channelName': self.channel.channelId})
                #     # The purpose of sending conversation level items is to identify the order of transcription in the front
                #     asyncio.create_task(self.channel.chat.send_message(
                #         ChatMessage(
                #             message=to_json(message), msg_id=message.item.id
                #         )
                #     ))
                # GA API: new conversation item events
                case ItemAdded():
                    logger.info(f"ItemAdded: {message=}", extra={'channelName': self.channel.channelId})
                    # The purpose of sending conversation level items is to identify the order of transcription in the front
                    asyncio.create_task(self.channel.chat.send_message(
                        ChatMessage(
                            message=to_json(message), msg_id=message.item.id
                        )
                    ))
                case ItemDone():
                    logger.info(f"ItemDone: {message=}", extra={'channelName': self.channel.channelId})
                # ResponseCreated
                case ResponseCreated():
                    logger.info(f"ResponseCreated: {message=}", extra={'channelName': self.channel.channelId})
                    pass
                # ResponseDone
                case ResponseDone():
                    # This only represents the token for this dialogue
                    # the entire conversation needs to be accumulated
                    logger.info(f"ResponseDone: {message=}", extra={'channelName': self.channel.channelId})
                    self.accumulate_token(message.response.usage)
                    pass

                # ResponseOutputItemAdded
                case ResponseOutputItemAdded():
                    logger.info(f"ResponseOutputItemAdded: {message=}", extra={'channelName': self.channel.channelId})
                    pass

                # ResponseContenPartAdded
                case ResponseContentPartAdded():
                    logger.info(f"ResponseContentPartAdded: {message=}", extra={'channelName': self.channel.channelId})
                    pass
                # ResponseAudioDone
                case ResponseAudioDone():
                    logger.info(f"ResponseAudioDone: {message=}", extra={'channelName': self.channel.channelId})
                    pass
                # ResponseContentPartDone
                case ResponseContentPartDone():
                    logger.info(f"ResponseContentPartDone: {message=}", extra={'channelName': self.channel.channelId})
                    pass
                # ResponseOutputItemDone
                case ResponseOutputItemDone():
                    logger.info(f"ResponseOutputItemDone: {message=}", extra={'channelName': self.channel.channelId})
                    pass
                case SessionUpdated():
                    logger.info(f"SessionUpdated: {message=}", extra={'channelName': self.channel.channelId})
                    pass
                case RateLimitsUpdated():
                    logger.info(f"RateLimitsUpdated: {message=}", extra={'channelName': self.channel.channelId})
                    pass
                case ResponseFunctionCallArgumentsDone():
                    logger.info(f"ResponseFunctionCallArgumentsDone: {message=}", extra={'channelName': self.channel.channelId})
                    asyncio.create_task(
                        self.handle_function_call(message)
                    )
                case ResponseFunctionCallArgumentsDelta():
                    logger.info(f"ResponseFunctionCallArgumentsDelta: {message=}", extra={'channelName': self.channel.channelId})
                    pass

                case _:
                    logger.warning(f"Unhandled message {message=}", extra={'channelName': self.channel.channelId})

    async def conversation_end_feedback(self):
        async with httpx.AsyncClient() as client:
            if self.token_usage is None:
                logger.info("Token is None", extra={'channelName': self.channel.channelId})
                return

            request_body = {
                "channelName": self.channel.channelId,
                "azureBaseUrl": self.inference_config.azure_base_url,
                "deployment": self.inference_config.azure_deployment,
                "tokenUsage": asdict(self.token_usage)
            }

            response = await client.post(get_callback_base_url(self.channel.channelId)+"/conversation-end", json=request_body)

            # 检查响应状态码
            if response.status_code == 200:
                logger.info("Feedback to web-end conversation_end success", extra={'channelName': self.channel.channelId})
            else:
                logger.warning("Feedback to web-end conversation_end fail", extra={'channelName': self.channel.channelId})

    @classmethod
    async def connection_fail_feedback(cls, channel_name: str, azure_base_url: str, deployment: str):
        async with httpx.AsyncClient() as client:
            request_body = {
                "channelName": channel_name,
                "azureBaseUrl": azure_base_url,
                "deployment": deployment
            }

            response = await client.post(get_callback_base_url(channel_name)+"/connection-fail", json=request_body)

            # 检查响应状态码
            if response.status_code == 200:
                logger.info("Feedback to web-end connection_fail success", extra={'channelName': channel_name})
            else:
                logger.warning("Feedback to web-end connection_fail fail", extra={'channelName': channel_name})

    # Let the AI talk firstly after starting the conversation
    async def init_greet(self):
        await self.connection.send_request(
            ItemCreate(
                item=SystemMessageItemParam(
                    role="system",
                    content=[{'type': 'input_text', 'text': 'start the conversation'}]
                )
            )
        )
        await self.connection.send_request(
            ResponseCreate()
        )
        logger.info("init_greet has sent", extra={'channelName': self.channel.channelId})
