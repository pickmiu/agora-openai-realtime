import json

from dataclasses import dataclass, asdict, field, is_dataclass
from typing import Any, Dict, Literal, Optional, List, Set, Union, get_origin, get_args
from enum import Enum
import uuid

PCM_SAMPLE_RATE = 24000
PCM_CHANNELS = 1


def generate_event_id() -> str:
    return str(uuid.uuid4())


# Enums
class Voices(str, Enum):
    # Legacy voices
    Amuch = "amuch"
    Dan = "dan"
    Elan = "elan"
    Marilyn = "marilyn"
    Meadow = "meadow"
    Breeze = "breeze"
    Cove = "cove"
    Ember = "ember"
    Jupiter = "jupiter"
    # Current supported voices (as per API documentation)
    Alloy = "alloy"
    Ash = "ash"
    Ballad = "ballad"
    Coral = "coral"
    Echo = "echo"
    Sage = "sage"
    Shimmer = "shimmer"
    Verse = "verse"
    Marin = "marin"  # Recommended for best quality
    Cedar = "cedar"  # Recommended for best quality


class AudioFormats(str, Enum):
    PCM16 = "pcm16"
    G711_ULAW = "g711_ulaw"
    G711_ALAW = "g711_alaw"


class ItemType(str, Enum):
    Message = "message"
    FunctionCall = "function_call"
    FunctionCallOutput = "function_call_output"


class MessageRole(str, Enum):
    System = "system"
    User = "user"
    Assistant = "assistant"


class ContentType(str, Enum):
    InputText = "input_text"
    InputAudio = "input_audio"
    Text = "text"
    Audio = "audio"


@dataclass
class FunctionToolChoice:
    name: str  # Name of the function
    type: str = "function"  # Fixed value for type


# ToolChoice can be either a literal string or FunctionToolChoice
ToolChoice = Union[str, FunctionToolChoice]  # "none", "auto", "required", or FunctionToolChoice


@dataclass
class RealtimeError:
    type: str  # The type of the error
    message: str  # The error message
    code: Optional[str] = None  # Optional error code
    param: Optional[str] = None  # Optional parameter related to the error
    event_id: Optional[str] = None  # Optional event ID for tracing


@dataclass
class InputAudioTranscription:
    model: str = "whisper-1"  # Default transcription model is "whisper-1"
    language: Optional[str] = None  # The language of the input audio in ISO-639-1(e.g. en) format will improve accuracy and latency.
    prompt: Optional[str] = None  # Optional text to guide the model's style


@dataclass
class ServerVADUpdateParams:
    threshold: Optional[float] = None  # Threshold for voice activity detection (0.0 to 1.0), defaults to 0.5
    prefix_padding_ms: Optional[int] = None  # Amount of padding before the voice starts (in milliseconds), defaults to 300ms
    silence_duration_ms: Optional[int] = None  # Duration of silence before considering speech stopped (in milliseconds), defaults to 500ms
    create_response: Optional[bool] = None  # Whether to automatically generate a response when VAD stop event occurs
    idle_timeout_ms: Optional[int] = None  # Optional timeout after which a model response will be triggered automatically
    interrupt_response: Optional[bool] = None  # Whether to automatically interrupt any ongoing response when VAD start event occurs
    type: str = "server_vad"  # Fixed value for VAD type


@dataclass
class SemanticVADUpdateParams:
    eagerness: Optional[Literal["low", "medium", "high", "auto"]] = None  # The eagerness of the model to respond
    create_response: Optional[bool] = None  # Whether to automatically generate a response when VAD stop event occurs
    interrupt_response: Optional[bool] = None  # Whether to automatically interrupt any ongoing response when VAD start event occurs
    type: str = "semantic_vad"  # Fixed value for Semantic VAD type


@dataclass
class TokenLimits:
    post_instructions: Optional[int] = None  # Maximum tokens allowed in the conversation after instructions


@dataclass
class RetentionRatioTruncation:
    retention_ratio: float  # Fraction of post-instruction conversation tokens to retain (0.0 - 1.0)
    type: str = "retention_ratio"  # Use retention ratio truncation
    token_limits: Optional[TokenLimits] = None  # Optional custom token limits for this truncation strategy


# Truncation can be either a string ("auto", "disabled") or RetentionRatioTruncation object
Truncation = Union[str, RetentionRatioTruncation]


# Audio format related classes
@dataclass
class PCMAudioFormat:
    """PCM audio format with 24kHz sample rate"""
    rate: int = 24000  # The sample rate of the audio. Always 24000
    type: str = "audio/pcm"  # The audio format. Always audio/pcm


@dataclass
class PCMUAudioFormat:
    """G.711 μ-law audio format"""
    type: str = "audio/pcmu"  # The audio format. Always audio/pcmu


@dataclass
class PCMAAudioFormat:
    """G.711 A-law audio format"""
    type: str = "audio/pcma"  # The audio format. Always audio/pcma


# Union type for audio formats
AudioFormatType = Union[PCMAudioFormat, PCMUAudioFormat, PCMAAudioFormat]


@dataclass
class NoiseReduction:
    """Configuration for input audio noise reduction"""
    type: Literal["near_field", "far_field"]  # Type of noise reduction: near_field for headphones, far_field for laptop/conference mics


@dataclass
class InputAudioConfig:
    """Configuration for input audio"""
    format: Optional[AudioFormatType] = None  # The format of the input audio
    noise_reduction: Optional[NoiseReduction] = None  # Noise reduction configuration, can be null to turn off
    transcription: Optional[InputAudioTranscription] = None  # Transcription configuration, can be null to turn off
    turn_detection: Optional[Union[ServerVADUpdateParams, SemanticVADUpdateParams]] = None  # Turn detection configuration, can be null to turn off


@dataclass
class OutputAudioConfig:
    """Configuration for output audio"""
    format: Optional[AudioFormatType] = None  # The format of the output audio
    speed: Optional[float] = None  # The speed of the model's spoken response (0.25 to 1.5), 1.0 is default
    voice: Optional[str] = None  # The voice the model uses to respond


@dataclass
class AudioConfig:
    """GA API audio configuration"""
    input: Optional[InputAudioConfig] = None  # Input audio configuration
    output: Optional[OutputAudioConfig] = None  # Output audio configuration


@dataclass
class Session:
    id: str  # The unique identifier for the session
    model: str  # The model associated with the session (e.g., "gpt-4o-realtime-preview")
    expires_at: int  # Expiration time of the session in seconds since the epoch (UNIX timestamp)
    object: str = "realtime.session"  # Fixed value indicating the object type
    type: Optional[str] = None  # Session type: "realtime" for speech-to-speech, "transcription" for transcription
    audio: Optional[AudioConfig] = None  # GA API audio configuration
    instructions: Optional[str] = None  # Instructions or guidance for the session
    max_output_tokens: Optional[Union[int, str]] = None  # Max response tokens, "inf" for infinite
    output_modalities: Optional[Set[str]] = None  # Set of allowed modalities (e.g., "text", "audio")
    tool_choice: Optional[ToolChoice] = None  # ToolChoice, either string or `FunctionToolChoice`
    tools: Optional[List[Dict[str, Union[str, Any]]]] = None  # List of tools available during the session
    truncation: Optional[Truncation] = None  # Truncation strategy: "auto", "disabled", or RetentionRatioTruncation object
    include: Optional[List[str]] = None  # Additional fields to include in server outputs


@dataclass
class SessionUpdateParams:
    type: Optional[str] = None  # Session type: "realtime" for speech-to-speech, "transcription" for transcription
    audio: Optional[AudioConfig] = None  # GA API audio configuration
    instructions: Optional[str] = None  # Optional instructions string
    max_output_tokens: Optional[Union[int, str]] = None  # Max response tokens, "inf" for infinite
    model: Optional[str] = None  # Optional string to specify the model
    output_modalities: Optional[Set[str]] = None  # Set of allowed modalities (e.g., "text", "audio")
    tool_choice: Optional[ToolChoice] = None  # ToolChoice, either string or `FunctionToolChoice`
    tools: Optional[List[Dict[str, Union[str, any]]]] = None  # List of tools (e.g., dictionaries)
    truncation: Optional[Truncation] = None  # Truncation strategy: "auto", "disabled", or RetentionRatioTruncation object
    

# Define individual message item param types
@dataclass
class SystemMessageItemParam:
    content: List[dict]  # This can be more specific based on content structure
    id: Optional[str] = None
    status: Optional[str] = None
    type: str = "message"
    role: str = "system"


@dataclass
class UserMessageItemParam:
    content: List[dict]  # Similarly, content can be more specific
    id: Optional[str] = None
    status: Optional[str] = None
    type: str = "message"
    role: str = "user"


@dataclass
class AssistantMessageItemParam:
    content: List[dict]  # Content structure here depends on your schema
    id: Optional[str] = None
    status: Optional[str] = None
    type: str = "message"
    role: str = "assistant"


@dataclass
class FunctionCallItemParam:
    name: str
    call_id: str
    arguments: str
    type: str = "function_call"
    id: Optional[str] = None
    status: Optional[str] = None


@dataclass
class FunctionCallOutputItemParam:
    call_id: str
    output: str
    id: Optional[str] = None
    status: Optional[str] = None  # GA API: accepts no-op status field
    type: str = "function_call_output"


@dataclass
class ResponseItemInputTextContentPart:
    text: str
    type: str = "input_text"


@dataclass
class ResponseItemInputAudioContentPart:
    transcript: Optional[str]
    type: str = "input_audio"


@dataclass
class ResponseItemTextContentPart:
    text: str
    type: str = "text"


@dataclass
class ResponseItemAudioContentPart:
    transcript: Optional[str]
    type: str = "audio"


# GA API: new output content part types
@dataclass
class ResponseItemOutputTextContentPart:
    text: str
    type: str = "output_text"  # GA API: renamed from "text"


@dataclass
class ResponseItemOutputAudioContentPart:
    transcript: Optional[str]
    type: str = "output_audio"  # GA API: renamed from "audio"


# Union of all possible item types
ItemParam = Union[
    SystemMessageItemParam,
    UserMessageItemParam,
    AssistantMessageItemParam,
    FunctionCallItemParam,
    FunctionCallOutputItemParam,
    # Beta API content parts
    ResponseItemInputTextContentPart,
    ResponseItemInputAudioContentPart,
    ResponseItemTextContentPart,
    ResponseItemAudioContentPart,
    # GA API content parts
    ResponseItemOutputTextContentPart,
    ResponseItemOutputAudioContentPart,
]


# Assuming the EventType and other enums are already defined
# For reference:
class EventType(str, Enum):
    SESSION_UPDATE = "session.update"
    INPUT_AUDIO_BUFFER_APPEND = "input_audio_buffer.append"
    INPUT_AUDIO_BUFFER_COMMIT = "input_audio_buffer.commit"
    INPUT_AUDIO_BUFFER_CLEAR = "input_audio_buffer.clear"
    UPDATE_CONVERSATION_CONFIG = "update_conversation_config"
    ITEM_CREATE = "conversation.item.create"
    ITEM_TRUNCATE = "conversation.item.truncate"
    ITEM_DELETE = "conversation.item.delete"
    RESPONSE_CREATE = "response.create"
    RESPONSE_CANCEL = "response.cancel"

    ERROR = "error"
    SESSION_CREATED = "session.created"
    SESSION_UPDATED = "session.updated"

    INPUT_AUDIO_BUFFER_COMMITTED = "input_audio_buffer.committed"
    INPUT_AUDIO_BUFFER_CLEARED = "input_audio_buffer.cleared"
    INPUT_AUDIO_BUFFER_SPEECH_STARTED = "input_audio_buffer.speech_started"
    INPUT_AUDIO_BUFFER_SPEECH_STOPPED = "input_audio_buffer.speech_stopped"

    ITEM_CREATED = "conversation.item.created"
    ITEM_ADDED = "conversation.item.added"  # GA API: replaces conversation.item.created
    ITEM_DONE = "conversation.item.done"  # GA API: new event for item completion
    ITEM_DELETED = "conversation.item.deleted"
    ITEM_TRUNCATED = "conversation.item.truncated"
    ITEM_INPUT_AUDIO_TRANSCRIPTION_COMPLETED = "conversation.item.input_audio_transcription.completed"
    ITEM_INPUT_AUDIO_TRANSCRIPTION_FAILED = "conversation.item.input_audio_transcription.failed"

    RESPONSE_CREATED = "response.created"
    RESPONSE_CANCELLED = "response.cancelled"
    RESPONSE_DONE = "response.done"
    RESPONSE_OUTPUT_ITEM_ADDED = "response.output_item.added"
    RESPONSE_OUTPUT_ITEM_DONE = "response.output_item.done"
    RESPONSE_CONTENT_PART_ADDED = "response.content_part.added"
    RESPONSE_CONTENT_PART_DONE = "response.content_part.done"
    RESPONSE_TEXT_DELTA = "response.text.delta"
    RESPONSE_TEXT_DONE = "response.text.done"
    RESPONSE_AUDIO_TRANSCRIPT_DELTA = "response.audio_transcript.delta"
    RESPONSE_AUDIO_TRANSCRIPT_DONE = "response.audio_transcript.done"
    RESPONSE_AUDIO_DELTA = "response.audio.delta"
    RESPONSE_AUDIO_DONE = "response.audio.done"
    # GA API event names
    RESPONSE_OUTPUT_TEXT_DELTA = "response.output_text.delta"
    RESPONSE_OUTPUT_TEXT_DONE = "response.output_text.done"
    RESPONSE_OUTPUT_AUDIO_TRANSCRIPT_DELTA = "response.output_audio_transcript.delta"
    RESPONSE_OUTPUT_AUDIO_TRANSCRIPT_DONE = "response.output_audio_transcript.done"
    RESPONSE_OUTPUT_AUDIO_DELTA = "response.output_audio.delta"
    RESPONSE_OUTPUT_AUDIO_DONE = "response.output_audio.done"
    RESPONSE_FUNCTION_CALL_ARGUMENTS_DELTA = "response.function_call_arguments.delta"
    RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE = "response.function_call_arguments.done"
    RATE_LIMITS_UPDATED = "rate_limits.updated"


# Base class for all ServerToClientMessages
@dataclass
class ServerToClientMessage:
    event_id: str


@dataclass
class ErrorMessage(ServerToClientMessage):
    error: RealtimeError
    type: str = EventType.ERROR


@dataclass
class SessionCreated(ServerToClientMessage):
    session: Session
    type: str = EventType.SESSION_CREATED


@dataclass
class SessionUpdated(ServerToClientMessage):
    session: Session
    type: str = EventType.SESSION_UPDATED


@dataclass
class InputAudioBufferCommitted(ServerToClientMessage):
    item_id: str
    type: str = EventType.INPUT_AUDIO_BUFFER_COMMITTED
    previous_item_id: Optional[str] = None


@dataclass
class InputAudioBufferCleared(ServerToClientMessage):
    type: str = EventType.INPUT_AUDIO_BUFFER_CLEARED


@dataclass
class InputAudioBufferSpeechStarted(ServerToClientMessage):
    audio_start_ms: int
    item_id: str
    type: str = EventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED


@dataclass
class InputAudioBufferSpeechStopped(ServerToClientMessage):
    audio_end_ms: int
    type: str = EventType.INPUT_AUDIO_BUFFER_SPEECH_STOPPED
    item_id: Optional[str] = None


@dataclass
class ItemCreated(ServerToClientMessage):
    item: ItemParam
    type: str = EventType.ITEM_CREATED
    previous_item_id: Optional[str] = None


# GA API new conversation item events
@dataclass
class ItemAdded(ServerToClientMessage):
    item: ItemParam
    type: str = EventType.ITEM_ADDED
    previous_item_id: Optional[str] = None


@dataclass
class ItemDone(ServerToClientMessage):
    item: ItemParam
    type: str = EventType.ITEM_DONE
    previous_item_id: Optional[str] = None


@dataclass
class ItemTruncated(ServerToClientMessage):
    item_id: str
    content_index: int
    audio_end_ms: int
    type: str = EventType.ITEM_TRUNCATED


@dataclass
class ItemDeleted(ServerToClientMessage):
    item_id: str
    type: str = EventType.ITEM_DELETED


# Assuming the necessary enums, ItemParam, and other classes are defined above
# ResponseStatus could be a string or an enum, depending on your schema

# Enum or Literal for ResponseStatus (could be more extensive)
ResponseStatus = Union[str, Literal["in_progress", "completed", "cancelled", "incomplete", "failed"]]

# Define status detail classes
@dataclass
class ResponseCancelledDetails:
    reason: str  # e.g., "turn_detected", "client_cancelled"
    type: str = "cancelled"


@dataclass
class ResponseIncompleteDetails:
    reason: str  # e.g., "max_output_tokens", "content_filter"
    type: str = "incomplete"


@dataclass
class ResponseError:
    type: str  # The type of the error, e.g., "validation_error", "server_error"
    message: str  # The error message describing what went wrong
    code: Optional[str] = None  # Optional error code, e.g., HTTP status code, API error code


@dataclass
class ResponseFailedDetails:
    error: ResponseError  # Assuming ResponseError is already defined
    type: str = "failed"


# Union of possible status details
ResponseStatusDetails = Union[ResponseCancelledDetails, ResponseIncompleteDetails, ResponseFailedDetails]


# Define Usage class to handle token usage
@dataclass
class CachedTokensDetails:
    text_tokens: int
    audio_tokens: int


@dataclass
class InputTokenDetails:
    cached_tokens: int
    text_tokens: int
    audio_tokens: int
    cached_tokens_details: CachedTokensDetails


@dataclass
class OutputTokenDetails:
    text_tokens: int
    audio_tokens: int


@dataclass
class Usage:
    total_tokens: int
    input_tokens: int
    output_tokens: int
    input_token_details: InputTokenDetails
    output_token_details: OutputTokenDetails


# The Response dataclass definition
@dataclass
class Response:
    id: str  # Unique ID for the response
    output: List[ItemParam] = field(default_factory=list)  # List of items in the response
    object: str = "realtime.response"  # Fixed value for object type
    status: ResponseStatus = "in_progress"  # Status of the response
    status_details: Optional[ResponseStatusDetails] = None  # Additional details based on status
    usage: Optional[Usage] = None  # Token usage information
    metadata: Optional[Dict[str, Any]] = None  # Additional metadata for the response


@dataclass
class ResponseCreated(ServerToClientMessage):
    response: Response
    type: str = EventType.RESPONSE_CREATED


@dataclass
class ResponseDone(ServerToClientMessage):
    response: Response
    type: str = EventType.RESPONSE_DONE


@dataclass
class ResponseTextDelta(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    content_index: int
    delta: str
    type: str = EventType.RESPONSE_TEXT_DELTA


@dataclass
class ResponseTextDone(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    content_index: int
    text: str
    type: str = EventType.RESPONSE_TEXT_DONE


@dataclass
class ResponseAudioTranscriptDelta(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    content_index: int
    delta: str
    type: str = EventType.RESPONSE_AUDIO_TRANSCRIPT_DELTA


@dataclass
class ResponseAudioTranscriptDone(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    content_index: int
    transcript: str
    type: str = EventType.RESPONSE_AUDIO_TRANSCRIPT_DONE


@dataclass
class ResponseAudioDelta(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    content_index: int
    delta: str
    type: str = EventType.RESPONSE_AUDIO_DELTA


@dataclass
class ResponseAudioDone(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    content_index: int
    type: str = EventType.RESPONSE_AUDIO_DONE


# GA API event classes
@dataclass
class ResponseOutputTextDelta(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    content_index: int
    delta: str
    type: str = EventType.RESPONSE_OUTPUT_TEXT_DELTA


@dataclass
class ResponseOutputTextDone(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    content_index: int
    text: str
    type: str = EventType.RESPONSE_OUTPUT_TEXT_DONE


@dataclass
class ResponseOutputAudioTranscriptDelta(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    content_index: int
    delta: str
    type: str = EventType.RESPONSE_OUTPUT_AUDIO_TRANSCRIPT_DELTA


@dataclass
class ResponseOutputAudioTranscriptDone(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    content_index: int
    transcript: str
    type: str = EventType.RESPONSE_OUTPUT_AUDIO_TRANSCRIPT_DONE


@dataclass
class ResponseOutputAudioDelta(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    content_index: int
    delta: str
    type: str = EventType.RESPONSE_OUTPUT_AUDIO_DELTA


@dataclass
class ResponseOutputAudioDone(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    content_index: int
    type: str = EventType.RESPONSE_OUTPUT_AUDIO_DONE


@dataclass
class ResponseFunctionCallArgumentsDelta(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    call_id: str
    delta: str
    type: str = EventType.RESPONSE_FUNCTION_CALL_ARGUMENTS_DELTA


@dataclass
class ResponseFunctionCallArgumentsDone(ServerToClientMessage):
    response_id: str
    item_id: str
    output_index: int
    call_id: str
    name: str
    arguments: str
    type: str = EventType.RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE


@dataclass
class RateLimitDetails:
    name: str  # Name of the rate limit, e.g., "api_requests", "message_generation"
    limit: int  # The maximum number of allowed requests in the current time window
    remaining: int  # The number of requests remaining in the current time window
    reset_seconds: float  # The number of seconds until the rate limit resets


@dataclass
class RateLimitsUpdated(ServerToClientMessage):
    rate_limits: List[RateLimitDetails]
    type: str = EventType.RATE_LIMITS_UPDATED


@dataclass
class ResponseOutputItemAdded(ServerToClientMessage):
    response_id: str  # The ID of the response
    output_index: int  # Index of the output item in the response
    item: Union[ItemParam, None]  # The added item (can be a message, function call, etc.)
    type: str = EventType.RESPONSE_OUTPUT_ITEM_ADDED  # Fixed event type


@dataclass
class ResponseContentPartAdded(ServerToClientMessage):
    response_id: str  # The ID of the response
    item_id: str  # The ID of the item to which the content part was added
    output_index: int  # Index of the output item in the response
    content_index: int  # Index of the content part in the output
    part: Union[ItemParam, None]  # The added content part
    content: Union[ItemParam, None]
    type: str = EventType.RESPONSE_CONTENT_PART_ADDED  # Fixed event type


@dataclass
class ResponseContentPartDone(ServerToClientMessage):
    response_id: str  # The ID of the response
    item_id: str  # The ID of the item to which the content part belongs
    output_index: int  # Index of the output item in the response
    content_index: int  # Index of the content part in the output
    part: Union[ItemParam, None]  # The content part that was completed
    content: Union[ItemParam, None]
    type: str = EventType.RESPONSE_CONTENT_PART_ADDED  # Fixed event type


@dataclass
class ResponseOutputItemDone(ServerToClientMessage):
    response_id: str  # The ID of the response
    output_index: int  # Index of the output item in the response
    item: Union[ItemParam, None]  # The output item that was completed
    type: str = EventType.RESPONSE_OUTPUT_ITEM_DONE  # Fixed event type


@dataclass
class ItemInputAudioTranscriptionCompleted(ServerToClientMessage):
    item_id: str  # The ID of the item for which transcription was completed
    content_index: int  # Index of the content part that was transcribed
    transcript: str  # The transcribed text
    type: str = EventType.ITEM_INPUT_AUDIO_TRANSCRIPTION_COMPLETED  # Fixed event type


@dataclass
class ItemInputAudioTranscriptionFailed(ServerToClientMessage):
    item_id: str  # The ID of the item for which transcription failed
    content_index: int  # Index of the content part that failed to transcribe
    error: ResponseError  # Error details explaining the failure
    type: str = EventType.ITEM_INPUT_AUDIO_TRANSCRIPTION_FAILED  # Fixed event type


# Union of all server-to-client message types
ServerToClientMessages = Union[
    ErrorMessage,
    SessionCreated,
    SessionUpdated,
    InputAudioBufferCommitted,
    InputAudioBufferCleared,
    InputAudioBufferSpeechStarted,
    InputAudioBufferSpeechStopped,
    ItemCreated,
    ItemAdded,  # GA API
    ItemDone,   # GA API
    ItemTruncated,
    ItemDeleted,
    ResponseCreated,
    ResponseDone,
    ResponseTextDelta,
    ResponseTextDone,
    ResponseAudioTranscriptDelta,
    ResponseAudioTranscriptDone,
    ResponseAudioDelta,
    ResponseAudioDone,
    # GA API event types
    ResponseOutputTextDelta,
    ResponseOutputTextDone,
    ResponseOutputAudioTranscriptDelta,
    ResponseOutputAudioTranscriptDone,
    ResponseOutputAudioDelta,
    ResponseOutputAudioDone,
    ResponseFunctionCallArgumentsDelta,
    ResponseFunctionCallArgumentsDone,
    RateLimitsUpdated,
    ResponseOutputItemAdded,
    ResponseContentPartAdded,
    ResponseContentPartDone,
    ResponseOutputItemDone,
    ItemInputAudioTranscriptionCompleted,
    ItemInputAudioTranscriptionFailed
]


# Base class for all ClientToServerMessages
@dataclass
class ClientToServerMessage:
    event_id: str = field(default_factory=generate_event_id)


@dataclass
class InputAudioBufferAppend(ClientToServerMessage):
    audio: Optional[str] = field(default=None)
    type: str = EventType.INPUT_AUDIO_BUFFER_APPEND  # Default argument (has a default value)


@dataclass
class InputAudioBufferCommit(ClientToServerMessage):
    type: str = EventType.INPUT_AUDIO_BUFFER_COMMIT


@dataclass
class InputAudioBufferClear(ClientToServerMessage):
    type: str = EventType.INPUT_AUDIO_BUFFER_CLEAR


@dataclass
class ItemCreate(ClientToServerMessage):
    item: Optional[ItemParam] = field(default=None)  # Assuming `ItemParam` is already defined
    type: str = EventType.ITEM_CREATE
    previous_item_id: Optional[str] = None


@dataclass
class ItemTruncate(ClientToServerMessage):
    item_id: Optional[str] = field(default=None)
    content_index: Optional[int] = field(default=None)
    audio_end_ms: Optional[int] = field(default=None)
    type: str = EventType.ITEM_TRUNCATE


@dataclass
class ItemDelete(ClientToServerMessage):
    item_id: Optional[str] = field(default=None)
    type: str = EventType.ITEM_DELETE


@dataclass
class ResponseCreateParams:
    commit: bool = True  # Whether the generated messages should be appended to the conversation
    cancel_previous: bool = True  # Whether to cancel the previous pending generation
    append_input_items: Optional[List[ItemParam]] = None  # Messages to append before response generation
    input_items: Optional[List[ItemParam]] = None  # Initial messages to use for generation
    modalities: Optional[Set[str]] = None  # Allowed modalities (e.g., "text", "audio")
    instructions: Optional[str] = None  # Instructions or guidance for the model
    voice: Optional[Voices] = None  # Voice setting for audio output
    output_audio_format: Optional[AudioFormats] = None  # Format for the audio output
    tools: Optional[List[Dict[str, Any]]] = None  # Tools available for this response
    tool_choice: Optional[ToolChoice] = None  # How to choose the tool ("auto", "required", etc.)
    temperature: Optional[float] = None  # The randomness of the model's responses
    max_response_output_tokens: Optional[Union[int, str]] = None  # Max number of tokens for the output, "inf" for infinite


@dataclass
class ResponseCreate(ClientToServerMessage):
    type: str = EventType.RESPONSE_CREATE
    response: Optional[ResponseCreateParams] = None  # Assuming `ResponseCreateParams` is defined


@dataclass
class ResponseCancel(ClientToServerMessage):
    type: str = EventType.RESPONSE_CANCEL


DEFAULT_CONVERSATION = "default"


@dataclass
class UpdateConversationConfig(ClientToServerMessage):
    type: str = EventType.UPDATE_CONVERSATION_CONFIG
    label: str = DEFAULT_CONVERSATION
    subscribe_to_user_audio: Optional[bool] = None
    voice: Optional[Voices] = None
    system_message: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    tools: Optional[List[dict]] = None
    tool_choice: Optional[ToolChoice] = None
    disable_audio: Optional[bool] = None
    output_audio_format: Optional[AudioFormats] = None


@dataclass
class SessionUpdate(ClientToServerMessage):
    session: Optional[SessionUpdateParams] = field(default=None)  # Assuming `SessionUpdateParams` is defined
    type: str = EventType.SESSION_UPDATE


# Union of all client-to-server message types
ClientToServerMessages = Union[
    InputAudioBufferAppend,
    InputAudioBufferCommit,
    InputAudioBufferClear,
    ItemCreate,
    ItemTruncate,
    ItemDelete,
    ResponseCreate,
    ResponseCancel,
    UpdateConversationConfig,
    SessionUpdate
]


def from_dict(data_class, data):
    """Recursively convert a dictionary to a dataclass instance."""
    if data is None:
        return None
    
    # Handle Optional types
    origin = get_origin(data_class)
    if origin is Union:
        args = get_args(data_class)
        # Check if it's Optional (Union with None)
        if type(None) in args:
            if data is None:
                return None
            # Get the non-None type
            non_none_types = [arg for arg in args if arg is not type(None)]
            if len(non_none_types) == 1:
                return from_dict(non_none_types[0], data)
        # For other Union types, try each type
        for arg in args:
            if arg is not type(None):
                try:
                    return from_dict(arg, data)
                except:
                    continue
        return data
    
    if is_dataclass(data_class):  # Check if the target class is a dataclass
        fieldtypes = {f.name: f.type for f in data_class.__dataclass_fields__.values()}
        # Filter out keys that are not in the dataclass fields
        valid_data = {f: data[f] for f in fieldtypes if f in data}
        return data_class(**{f: from_dict(fieldtypes[f], valid_data[f]) for f in valid_data})
    elif isinstance(data, list):  # Handle lists of nested dataclass objects
        list_args = get_args(data_class)
        if list_args:
            return [from_dict(list_args[0], item) for item in data]
        return data
    else:  # For primitive types (str, int, float, etc.), return the value as-is
        return data


def parse_client_message(unparsed_string: str) -> ClientToServerMessage:
    data = json.loads(unparsed_string)
    
    # Dynamically select the correct message class based on the `type` field, using from_dict
    if data["type"] == EventType.INPUT_AUDIO_BUFFER_APPEND:
        return from_dict(InputAudioBufferAppend, data)
    elif data["type"] == EventType.INPUT_AUDIO_BUFFER_COMMIT:
        return from_dict(InputAudioBufferCommit, data)
    elif data["type"] == EventType.INPUT_AUDIO_BUFFER_CLEAR:
        return from_dict(InputAudioBufferClear, data)
    elif data["type"] == EventType.ITEM_CREATE:
        return from_dict(ItemCreate, data)
    elif data["type"] == EventType.ITEM_TRUNCATE:
        return from_dict(ItemTruncate, data)
    elif data["type"] == EventType.ITEM_DELETE:
        return from_dict(ItemDelete, data)
    elif data["type"] == EventType.RESPONSE_CREATE:
        return from_dict(ResponseCreate, data)
    elif data["type"] == EventType.RESPONSE_CANCEL:
        return from_dict(ResponseCancel, data)
    elif data["type"] == EventType.UPDATE_CONVERSATION_CONFIG:
        return from_dict(UpdateConversationConfig, data)
    elif data["type"] == EventType.SESSION_UPDATE:
        return from_dict(SessionUpdate, data)
    
    raise ValueError(f"Unknown message type: {data['type']}")


# Assuming all necessary classes and enums (EventType, ServerToClientMessages, etc.) are imported
# Here’s how you can dynamically parse a server-to-client message based on the `type` field:

def parse_server_message(unparsed_string: str) -> ServerToClientMessage:
    data = json.loads(unparsed_string)

    # Dynamically select the correct message class based on the `type` field, using from_dict
    if data["type"] == EventType.ERROR:
        return from_dict(ErrorMessage, data)
    elif data["type"] == EventType.SESSION_CREATED:
        return from_dict(SessionCreated, data)
    elif data["type"] == EventType.SESSION_UPDATED:
        return from_dict(SessionUpdated, data)
    elif data["type"] == EventType.INPUT_AUDIO_BUFFER_COMMITTED:
        return from_dict(InputAudioBufferCommitted, data)
    elif data["type"] == EventType.INPUT_AUDIO_BUFFER_CLEARED:
        return from_dict(InputAudioBufferCleared, data)
    elif data["type"] == EventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
        return from_dict(InputAudioBufferSpeechStarted, data)
    elif data["type"] == EventType.INPUT_AUDIO_BUFFER_SPEECH_STOPPED:
        return from_dict(InputAudioBufferSpeechStopped, data)
    elif data["type"] == EventType.ITEM_CREATED:
        return from_dict(ItemCreated, data)
    # GA API new conversation item events
    elif data["type"] == EventType.ITEM_ADDED:
        return from_dict(ItemAdded, data)
    elif data["type"] == EventType.ITEM_DONE:
        return from_dict(ItemDone, data)
    elif data["type"] == EventType.ITEM_TRUNCATED:
        return from_dict(ItemTruncated, data)
    elif data["type"] == EventType.ITEM_DELETED:
        return from_dict(ItemDeleted, data)
    elif data["type"] == EventType.RESPONSE_CREATED:
        return from_dict(ResponseCreated, data)
    elif data["type"] == EventType.RESPONSE_DONE:
        return from_dict(ResponseDone, data)
    elif data["type"] == EventType.RESPONSE_TEXT_DELTA:
        return from_dict(ResponseTextDelta, data)
    elif data["type"] == EventType.RESPONSE_TEXT_DONE:
        return from_dict(ResponseTextDone, data)
    elif data["type"] == EventType.RESPONSE_AUDIO_TRANSCRIPT_DELTA:
        return from_dict(ResponseAudioTranscriptDelta, data)
    elif data["type"] == EventType.RESPONSE_AUDIO_TRANSCRIPT_DONE:
        return from_dict(ResponseAudioTranscriptDone, data)
    elif data["type"] == EventType.RESPONSE_AUDIO_DELTA:
        return from_dict(ResponseAudioDelta, data)
    elif data["type"] == EventType.RESPONSE_AUDIO_DONE:
        return from_dict(ResponseAudioDone, data)
    # GA API event types
    elif data["type"] == EventType.RESPONSE_OUTPUT_TEXT_DELTA:
        return from_dict(ResponseOutputTextDelta, data)
    elif data["type"] == EventType.RESPONSE_OUTPUT_TEXT_DONE:
        return from_dict(ResponseOutputTextDone, data)
    elif data["type"] == EventType.RESPONSE_OUTPUT_AUDIO_TRANSCRIPT_DELTA:
        return from_dict(ResponseOutputAudioTranscriptDelta, data)
    elif data["type"] == EventType.RESPONSE_OUTPUT_AUDIO_TRANSCRIPT_DONE:
        return from_dict(ResponseOutputAudioTranscriptDone, data)
    elif data["type"] == EventType.RESPONSE_OUTPUT_AUDIO_DELTA:
        return from_dict(ResponseOutputAudioDelta, data)
    elif data["type"] == EventType.RESPONSE_OUTPUT_AUDIO_DONE:
        return from_dict(ResponseOutputAudioDone, data)
    elif data["type"] == EventType.RESPONSE_FUNCTION_CALL_ARGUMENTS_DELTA:
        return from_dict(ResponseFunctionCallArgumentsDelta, data)
    elif data["type"] == EventType.RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE:
        return from_dict(ResponseFunctionCallArgumentsDone, data)
    elif data["type"] == EventType.RATE_LIMITS_UPDATED:
        return from_dict(RateLimitsUpdated, data)
    elif data["type"] == EventType.RESPONSE_OUTPUT_ITEM_ADDED:
        return from_dict(ResponseOutputItemAdded, data)
    elif data["type"] == EventType.RESPONSE_CONTENT_PART_ADDED:
        return from_dict(ResponseContentPartAdded, data)
    elif data["type"] == EventType.RESPONSE_CONTENT_PART_DONE:
        return from_dict(ResponseContentPartDone, data)
    elif data["type"] == EventType.RESPONSE_OUTPUT_ITEM_DONE:
        return from_dict(ResponseOutputItemDone, data)
    elif data["type"] == EventType.ITEM_INPUT_AUDIO_TRANSCRIPTION_COMPLETED:
        return from_dict(ItemInputAudioTranscriptionCompleted, data)
    elif data["type"] == EventType.ITEM_INPUT_AUDIO_TRANSCRIPTION_FAILED:
        return from_dict(ItemInputAudioTranscriptionFailed, data)

    raise ValueError(f"Unknown message type: {data['type']}")


def remove_none_values(d):
    """Recursively remove None values and empty dicts from dictionaries"""
    if isinstance(d, dict):
        cleaned = {}
        for k, v in d.items():
            if v is not None:
                cleaned_v = remove_none_values(v)
                # Only include non-empty values
                if cleaned_v != {} and cleaned_v != []:
                    cleaned[k] = cleaned_v
                elif not isinstance(cleaned_v, (dict, list)):
                    cleaned[k] = cleaned_v
        return cleaned
    elif isinstance(d, list):
        return [remove_none_values(item) for item in d]
    else:
        return d


def to_json(obj: Union[ClientToServerMessage, ServerToClientMessage]) -> str:
    data = asdict(obj)
    # Remove None values to avoid sending unnecessary fields
    data = remove_none_values(data)
    return json.dumps(data)
