from typing import List

from command import Command, ExecutionResult, register

TITLE = "Greet"
FIELDS = [
    {
        "name": "user",
        "type": "text"
    }
]
DESCRIPTION = """
👋 Greet everyone you meet.
"""


@register(TITLE)
class PipelineDAGVisualizer(Command):
    def title(self) -> str:
        return TITLE

    def form_fields(self) -> List[dict]:
        return FIELDS

    def description(self) -> str:
        return DESCRIPTION

    def execute(self, params: dict) -> ExecutionResult:
        user = params.get("user", "")
        if "" == user:
            return ExecutionResult(type="text", payload="Please provide a user")
        return ExecutionResult(type="text", payload="Hello {}".format(user))
