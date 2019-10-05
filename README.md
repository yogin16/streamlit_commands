# streamlit_commands
The missing admin console for giving UI to the daily python commands you run, using [streamlit](https://streamlit.io).


![Executing commands in Admin Console|635x380](https://github.com/yogin16/streamlit_commands/blob/master/st-commands.gif)

Boilerplate containing form builder and default result render support for quickly and easily adding commands screen:

All you need is:
- Command name: the title (as a string)
- The "form builder" fields: the schema of what your input form would look like (as a simple python dict)
- Description of the command (a markdown string)

It would render the form based on the schema provided and gives a hook `execute(params)` which would be called when input is provided in the UI for you to implement the logic of the command. Again `params` is a python dict containing the args - the inputs captured from UI.

That's it!

Here is an example of adding the sample `Greet` command to the admin console. 

```python
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
class Greet(Command):
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

```

**Please note:** These commands are scanned from the `commands` package on the start up of the app. You can just checkout the boiler plate and start adding any new command in the `commands` directory as per your needs.


It is must to extend your command to be stateless - as it is expecting command to be Singleton. Also, the command should extend the base `Command` class and have `@register()` decorator as shown in above example.

## Instructions:
(Assumes python3)
### Start the app
Install streamlit:
```bash
pip3 install -r requirements.txt
```
Run the server:
```bash
sh start.sh
```
or
```bash
streamlit run app.py
```
### The Command API
```python
class Command(metaclass=Singleton):
    """
    The normal API browser command. The fields are used in form_builder to render the form on canvas
    And allows hook to execute the command on input
    """

    def title(self) -> str:
        raise NotImplementedError

    def form_fields(self) -> List[dict]:
        raise NotImplementedError

    def description(self) -> str:
        return self.title()

    def execute(self, params: dict) -> ExecutionResult:
        raise NotImplementedError
```

### Supported Field Types:
- **"text"**: For normal text input
- **"text_area"**: For text area input
- **"selectbox"**: For picklist

### ExecutionResult
To show command result in UI. (return value of command's `execute` method)
It's a python namedtuple
```python
ExecutionResult = namedtuple("ExecutionResult", ["type", "payload"])
```
#### Supported Result Types:
- **"text"**: for showing text result on response, when the `payload` is a string to show
- **"json"**: for showing json result on response when `payload` is a json to show
- **"graphviz"**: for showing graph on response when `graphviz` is a graphviz Graph

### TODO:
- add support all of field types streamlit allows
- add support all of result/payload types streamlit allows
