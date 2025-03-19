from typing import Any

from realtime_agent.customizedtool.ielts_topic_selector import get_topics_and_questions
from realtime_agent.tools import ToolContext


# Function 雅思题库获取

class IeltsAgentTools(ToolContext):
    def __init__(self) -> None:
        super().__init__()

        # # create multiple functions here as per requirement
        # self.register_function(
        #     name="get_topics_and_questions",
        #     parameters={},
        #     description="Returns topics and questions in IELTS",
        #     fn=get_topics_and_questions,
        # )