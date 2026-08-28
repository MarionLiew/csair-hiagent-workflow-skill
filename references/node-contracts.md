# Verified node-contract principles

Exact field names and enum values must come from a current export for the target HiAgent version.

## Identity and topology

- Each node has a unique identity. In observed exports, `ID` and `Code` may be equal; preserve the convention used by the source export.
- `Depends` identifies upstream nodes and, for conditional branches, the corresponding output port.
- Node order should place producers before consumers because editors may resolve variable selectors sequentially.
- Fixed-name nodes such as Start and End must retain the platform-required English names even when other node names are Chinese.

## Variable references

A node-field reference normally needs a source node code, a source field path, and a machine output path such as `$.field_name`. The referenced top-level field must exist in the source node's declared output schema.

## Code nodes

- Declare every `params.name` as an input variable and every returned property needed downstream in the output schema.
- JSON escaping and JavaScript escaping are separate layers. Syntax-check the final JavaScript extracted from generated JSON.

## LLM nodes

- Put stable role, policy, evidence boundaries, and output requirements in the system prompt.
- Put the per-run question and referenced variables in the user prompt.
- Match output format and output schema. Text answers should not be forced through JSON unless downstream logic needs structured data.

## Variable aggregation

- Treat each group as a real output contract.
- Some HiAgent builds expose a group's output only after it contains variables. Populate required groups with valid upstream references.

## Knowledge, tools, and End

- Keep dataset and plugin bindings from the target environment; never invent IDs.
- Strip customer identifiers before sending a query to an external search provider.
- Use only an End reply-mode serialization observed in a current export or save request. UI labels may serialize differently between versions.
