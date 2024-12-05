# Observability how-to guides

## Tracing configuration

### Basic configuration

<details>
<summary>Set your tracing project</summary>
<div markdown='1'>

---
### Log traces to specific project
**Set the destination project statically**
- If left unspecified, the project is set to `default`
- You can set the `LANGCHAIN_PROJECT` environment variable to configure a custom project name for an entire application run.  
    ```bash
    export LANGCHAIN_PROJECT=my-custom-project
    ```

**Set the destination project dynamically**
```py
import openai
from langsmith import traceable
from langsmith.run_trees import RunTree

client = openai.Client()

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]

# Use the @traceable decorator with the 'project_name' parameter to log traces to LangSmith
# Ensure that the LANGCHAIN_TRACING_V2 environment variables is set for @traceable to work
@traceable(
    run_type="llm",
    name="OpenAI Call Decorator",
    project_name="My Project"
)
def call_openai(
    messages: list[dict], model: str = "gpt-4o-mini"
) -> str:
    return client.chat.completions.create(
        model=model,
        messages=messages,
    ).choices[0].message.content

# Call the decorated function
call_openai(messages)

# You can also specify the Project via the project_name parameter
# This will override the project_name specified in the @traceable decorator
call_openai(
    messages,
    langsmith_extra={"project_name": "My Overridden Project"},
)

# The wrapped OpenAI client accepts all the same langsmith_extra parameters
# as @traceable decorated functions, and logs traces to LangSmith automatically.
# Ensure that the LANGCHAIN_TRACING_V2 environment variables is set for the wrapper to work.
from langsmith import wrappers
wrapped_clinet = wrappers.wrap_openai(client)
wrapped_client.chat.completions.create(
    model='gpt-4o-mini',
    messages=messages,
    langsmith_extra={"project_name": "My Project"},
)

# Alternatively, create a RunTree object
# You can set the project name using the project_name parameter
rt = RunTree(
    run_type="llm",
    name="OpenAI Call RunTree",
    inputs={"messages": messages},
    project_name="My Project"
)
chat_completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

# End and submit the run
rt.end(outputs=chat_completion)
rt.post()
```

**Toggle tracing on and off**  
If you've decided you no longer want to trace your runs, you can unset the `LANGCHAIN_TRACING_V2` environment variable. Traces will no longer be logged to LangSmith.  
Note that this currently does not affect the RunTree objects or API users, as these are meant to be low-level and not affected by the tracing toggle.

---
</div>
</details>


<details>
<summary>Trace any Python or JS Code</summary>
<div markdown='1'>

---
### Use `@traceable` / `traceable`
LangSmith makes it easy to log traces with minimal changes to your existing code with the `@traceable` decorator in Python and `traceable` function in TypeScript.
- `The LANGCHAIN_TRACING_V2` environment variable must be set to `'true'` in order for traces to be logged to LangSmith, even when using `@traceable` or `traceable`.
```py
from openai import Client
from langsmith import traceable

openai = Client()

@traceable
def format_prompt(subject):
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": f"What's a good name for a store that sells {subject}?"
        }
    ]

@traceable(run_type="llm")
def invoke_llm(messages):
    return openai.chat.completions.create(
        messages=messages, model="gpt-4o-mini", temperature=0
    )

@traceable
def parse_output(response):
    return response.choices[0].message.content

@traceable
def run_pipeline(subject: str):
    messages = format_prompt(subject)
    response = invoke_llm(messages)
    return parse_output(response)

run_pipeline("colorful socks")
```
```
'Here are some fun and catchy name ideas for a store that sells colorful socks:\n\n1. Sock It to Me\n2. Colorful Toes\n3. Happy Feet Boutique\n4. The Sock Spectrum\n5. Rainbow Socks Co.\n6. Funky Footwear\n7. Sock Parade\n8. Dazzle Socks\n9. Vibrant Soles\n10. The Sock Garden\n\nFeel free to mix and match or modify these suggestions to find the perfect name for your store!'
```

### Use the `trace` context manager (Python only)
In Python, you can use the `trace` context manager to log traces to LangSmith. This is useful in situations where:

1. You want to log traces for a specific block of code.
2. You want control over the inputs, outputs, and other attributes of the trace.
3. It is not feasible to use a decorator or wrapper.
4. Any or all of the above.

The context manager integrates seamlessly with the `traceable` decorator and `wrap_openai` wrapper, so you can use them together in the same application.
```py
import openai
import langsmith as ls
from langsmith.wrappers import wrap_openai

client = wrap_openai(openai.Client())

@ls.traceable(run_type='tool', name='Retrieve Context')
def my_tool(question: str) -> str:
    return "During this morning's meeting, we solved all world conflict."

def chat_pipeline(question: str):
    context = my_tool(question)
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Please respond to the user's request only based on the given context."},
        {"role": "user", "content": f"Question: {question}\nContext: {context}"}
    ]
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages
    )
    return chat_completion.choices[0].message.content

app_inputs = {"input": "Can you summarize this morning's meetings?"}

with ls.trace("Chat Pipeline", "chain", project_name="my_test", inputs=app_inputs) as rt:
    output = chat_pipeline("Can you summarize this morning's meetings?")
    rt.end(outputs={"output": output})
```
- There are different types of `run_type`.
    - run_type : string : Type of run, e.g., "llm", "chain", "tool".

### Wrap the OpenAI client
The `wrap_openai`/`wrapOpenAI` methods in Python/TypeScript allow you to wrap your OpenAI client in order to automatically log traces 
-- no decorator or function wrapping required! 
The wrapper works seamlessly with the `@traceable` decorator or `traceable` function and you can use both in the same application.
```py
import openai
from langsmith import traceable
from langsmith.wrappers import wrap_openai

client = wrap_openai(openai.Client())

@traceable(run_type="tool", name="Retrieve Context")
def my_tool(question: str) -> str:
    return "During this morning's meeting, we solved all world conflict."

@traceable(name="Chat Pipeline")
def chat_pipeline(question: str):
    context = my_tool(question)
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Please respond to the user's request only based on the given context."},
        {"role": "user", "content": f"Question: {question}\nContext: {context}"}
    ]
    chat_completion = client.chat.completions.create(
      model="gpt-4o-mini", messages=messages
    )
    return chat_completion.choices[0].message.content

chat_pipeline("Can you summarize this morning's meetings?")
```

### Example usage
```py
from typing import Any, Callable, Type, TypeVar

T = TypeVar('T')

def traceable_cls(cls: Type[T]) -> Type[T]:
    """Instrument all public methods in a class."""
    
    def wrap_method(name: str, method: Any) -> Any:
        if callable(method) and not name.startswith('__'):
            return traceable(name=f"{cls.__name__}.{name}")(method)
        return method

    # Handle __dict__ case
    for name in dir(cls):
        if not name.startswith("_"):
            try:
                method = getattr(cls, name)
                setattr(cls, name, wrap_method(name, method))
            except AttributeError:
                pass

    # Handle __slots__ case
    if hasattr(cls, "__slots__"):
        for slot in cls.__slots__:  # type: ignore[attr-defined]
            if not slot.startswith("__"):
                try:
                    method = getattr(cls, slot)
                    setattr(cls, slot, wrap_method(slot, method))
                except AttributeError:
                    # Skip slots that don't have a value yet
                    pass

    return cls

@traceable_cls
class MyClass:
    def __init__(self, some_val: int):
        self.some_val = some_val

    def combine(self, other_val: int):
        return self.some_val + other_val

MyClass(13).combine(29)
```

---
</div>
</details>

<details>
<summary>Trace without setting environment variables</summary>
<div markdown='1'>

---

```py
import openai
from langsmith import Client, tracing_context, traceable
from langsmith.wrappers import wrap_openai

langsmith_client = Client(
    api_key="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",
    api_url="https://api.smith.langchain.com"
)

client = wrap_openai(openai.Client())

@traceable(run_type="tool", name="Retrieve Context")
def my_tool(question: str) -> str:
    return "During this morning's meeting, we solved all world conflict."

@traceable
def chat_pipeline(question: str):
    context = my_tool(question)
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Please respond to the user's request only based on the given context."},
        {"role": "user", "content": f"Question: {question} \n Context: {context}"}
    ]
    chat_completion = client.chat.completions.create(
        model='gpt-4o-mini', messages=messages
    )
    return chat_completion.choices[0].message.content

# Can set to False to disable tracing here without changing code structure
with tracing_context(enabled=True):
    # Use langsmith_extra to pass in a custom client
    chat_pipeline("Can you summarize this morning's meetings?", langsmith_extra={"client": langsmith_client})
```
- The recommended way to do this in Python is to use the `tracing_context` context manager.   
- This works for both code annotated with `traceable` and code within the `trace` context manager.

---
</div>
</details>


### Trace natively supported libraries
<details>
<summary></summary>
<div markdown='1'>

---

---
</div>
</details>

