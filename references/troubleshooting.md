# Troubleshooting

## Import says Start node name should be Start

Set the Start node's serialized `Name` exactly to `Start`. HiAgent field names are case-sensitive. Do not use lowercase `name`. If a generated Start node contains a separate `Title`, remove it unless a verified export requires it; a localized `Title` has caused this import error in a tested environment.

## LLM OutputSchema cannot unmarshal into `[]*node.Parameters`

HiAgent expects its parameter-array representation, not a JSON Schema object such as `{ "type": "object", "properties": ... }`. Copy the array shape from a current export, or omit `OutputSchema` when the node works without it. Never substitute a generic JSON Schema object.

## `Error 1406 (22001): Data too long for column 'code'`

The tested deployment rejected an oversized Code-node program. The database limit is deployment-specific and has not been established.

1. Run `scripts/validate_workflow.py workflow.json --report-lengths` and inspect UTF-8 byte sizes.
2. Confirm whether the longest field is `Configs.Code.Code`; do not assume SystemPrompt or Prompt caused an error that explicitly names `code`.
3. Remove comments, duplicated logic, embedded reference data, and large prompt text from Code nodes.
4. Prefer moving reasoning and prose into LLM prompt fields, or split one large Code node into smaller focused nodes.
5. Converting code to one line helps only if it actually reduces byte count; removing line breaks alone is not a reliable fix.
6. When the environment's limit is known, enforce it with `--max-code-bytes N` before import.

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
