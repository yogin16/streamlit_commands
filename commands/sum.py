from typing import List

from command import Command, ExecutionResult, register

TITLE = "Calculator"
FIELDS = [
    {
        "name": "operation",
        "type": "selectbox",
        "options": ["sum", "subtract", "multiply"]
    },
    {
        "name": "a",
        "type": "text"
    },
    {
        "name": "b",
        "type": "text"
    }
]
DESCRIPTION = """
🔢 Calculator demonstration
"""


@register(TITLE)
class Calculator(Command):
    def title(self) -> str:
        return TITLE

    def form_fields(self) -> List[dict]:
        return FIELDS

    def description(self) -> str:
        return DESCRIPTION

    def execute(self, params: dict) -> ExecutionResult:
        operation = params["operation"]
        a = float(params["a"])
        b = float(params["b"])
        ans = 0
        if "sum" == operation:
            ans = a + b
        elif "subtract" == operation:
            ans = a - b
        elif "multiply" == operation:
            ans = a * b
        return ExecutionResult(type="text", payload="Ans is: {}".format(ans))
