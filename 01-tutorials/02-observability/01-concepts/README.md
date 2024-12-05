# Concepts
A `Trace` is essentially a series of steps that your application takes to go from input to output.   
Each of these individual steps is represented by a `Run`.   
A `Project` is simply a collection of traces.

### Runs
A `Run` is a span representing a single unit of work or operation within your LLM application. 

### Traces
A `Trace` is a collection of runs that are related to a single operation.

### Projects
A `Project` is a collection of traces.

### Feedback
`Feedback` allows you to score an individual run based on certain criteria.

### Tags
`Tags` are collections of strings that can be attached to runs.

### Metadata
`Metadata` is a collection of key-value pairs that can be attached to runs.