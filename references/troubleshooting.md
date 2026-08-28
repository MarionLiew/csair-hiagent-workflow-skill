# Troubleshooting

## Import says Start node name should be Start

Set the serialized name exactly to `Start`.

## A downstream variable selector is empty

Check producer order, declared output schema, source node code, `Path`, output JSONPath, populated aggregation groups, and conditional branch port.

## “Undefined” in a prompt

Inspect the upstream output schema and saved input-variable reference. A prompt placeholder alone does not create a variable.

## Code node SyntaxError near join or a quote

Extract final JavaScript from the JSON and run a syntax check. Fix newline/backslash escaping in the generator, regenerate, and check again.

## Final response is JSON or contains slashes

Determine whether wrapping comes from LLM structured output, cleanup code, End variable mode, or chat UI serialization. Do not remove useful Markdown as a generic fix.

## The workflow is overcautious

Separate “no evidence” from “evidence supports the main answer but not every exception.” Give supported conclusions and ask only for details that change the result.

## Citations are not clickable

Verify whether the chat product supports native retrieval citations or Markdown links. Workflow-internal retrieval may not propagate metadata required by a native citation panel. Fall back to numbered citations with real document name and page.

## Runtime-only failures

Bindings, credentials, quotas, model permissions, memory, UI rendering, and browser-driver compatibility require runtime evidence. Request a sanitized probe containing only the failing operation when necessary.
