# Verified scope and limitations

This skill is based on sanitized structural findings from HiAgent v2.1-era documentation, exported workflow JSON, successful imports, and selected runtime probes. It is not a complete specification of every HiAgent node or every platform deployment.

## Explored node types

The following node types have usable, evidence-backed structural knowledge:

- `Start`: fixed-name start node, user input declaration, and downstream field references.
- `End`: fixed-name end node and variable input connection. See the reply-mode limitation below.
- `Knowledge`: knowledge-base retrieval output connection, including `outputList`-style downstream use. Dataset binding remains environment-specific.
- `Code`: input-variable declarations, JavaScript handler body, output schema, downstream references, and syntax validation.
- `LLM`: system prompt, user prompt, input variables, text/JSON output formats, output schema, temperature/token/history settings observed in exports.
- `Condition`: if/else branches, condition expressions, branch port dependencies, and downstream routing.
- `VariableMerge`: multiple populated groups, declared group outputs, and downstream selection. Empty-group behavior has been observed as problematic in the tested editor.
- `Tool`: the general saved-node shape has been observed, but runtime verification is limited to a configured Bing Search plugin instance and its returned fields.

The verified multi-node pattern is: Start → Knowledge → Code/LLM evidence decision → Condition → knowledge-only or Bing-search branch → VariableMerge → answer LLM → review LLM → cleanup Code → End.

## Partially verified behavior

- `End` reply modes: variable return is structurally known. The exact serialized fields for every UI reply-mode choice have not all been captured; do not guess them.
- Knowledge citations: document names, pages, and retrieval metadata can appear in node output, but workflow-internal retrieval has not been proven to trigger HiAgent's native right-side citation/file-preview UI.
- Tool nodes: plugin identifiers, credentials, quotas, input/output fields, and failure payloads vary by plugin and environment.
- LLM configuration: model identifiers, reasoning switches, permissions, and supported fields may differ by deployment.
- Knowledge retrieval thresholds and metadata schemas may vary with knowledge-base configuration and platform version.

## Not established by this skill

- The complete catalog or JSON schema of all HiAgent node types.
- Arbitrary plugins or tool nodes other than the tested Bing Search configuration.
- Knowledge-base write/update nodes, automatic knowledge approval, or file-submission workflows.
- Workflow-native long-term memory. In the tested product, long-term memory appears to be configured at the assistant/application level rather than inside this workflow.
- Native citation cards, file icons, exact-page highlighting, or PDF page jumping from ordinary Markdown links.
- Every file parser's behavior for Word, PDF, Excel, PowerPoint, images, or OCR.
- Browser-driver/probe compatibility on every UOS or browser version.
- Cross-version portability beyond the structures verified from the target HiAgent environment.

## Validation boundary

`scripts/validate_workflow.py` performs static checks only. It can detect malformed JSON, duplicate identities, missing dependencies, undeclared Code inputs, and JavaScript syntax errors. It cannot prove that a workflow will import into every HiAgent version or that datasets, models, plugins, permissions, quotas, memory, citations, and UI rendering will work at runtime.

For any node or field outside the explored list, request a sanitized export or a probe containing only that node's save operation. Mark it supported only after the structure is captured and an import or runtime test succeeds.
