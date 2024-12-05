### Log first trace
```py
import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable

# Auto-trace LLM calls in-context
client = wrap_openai(openai.Client())

@traceable # Auto-trace this function
def pipeline(user_input: str):
    result = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="gpt-4o-mini"
    )
    return result.choices[0].message.content

pipeline("Hello, world") # 'Hello! How can I assist you today?'
```
- LangSmith makes it easy to log traces with minimal changes to your existing code with the `@traceable` decorator in Python and `traceable` function in TypeScript.


### Run first evaluation
```py
from langsmith import Client, evaluate

client = Client()

# Define dataset
dataset_name = "Sample Dataset"
dataset = client.create_dataset(dataset_name, description="A sample dataset in LangSmith.")

client.create_example(
    inputs=[
        {"postfix": "to LangSmith"},
        {"postfix": "to Evaluations in LangSmith"},
    ],
    outputs=[
        {"output": "Welcome to LangSmith"},
        {"output": "Welcome to Evaluations in LangSmith"},
    ],
    dataset_id=dataset.id,
)

# Define evaluator
def exact_match(run, example):
    return {"score": run.outputs["output"] == example.outputs["output"]}

experiment_results = evaluate(
    lambda input: "Welcone " + input['postfix'], # Your AI system goes here
    data=dataset_name, # The data to predict and grade over
    evaluators=[exact_match], # The evaluators to score the results
    experiment_prefix="sample-experiment", # The name of the experiment
    metadata={
        "verson": "1.0.0",
        "revision_id": "beta"
    },
)
```