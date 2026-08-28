# Csair HiAgent Workflow Skill

用于让 AI Agent 构建、修改、校验和排查 Csair HiAgent 工作流 JSON，目标是直接生成可导入、节点连接完整、能够实际运行的工作流，而不只是提供示例或分析。支持 Codex，也适用于能够读取 `SKILL.md` 或自定义系统指令的其他 Agent。

## 已探明的节点

目前具备实际结构依据的节点类型如下：

- **Start**：固定名称、输入变量声明和下游字段引用。
- **End**：固定名称、变量输入连接和已验证的回复配置；如需新增其他回复模式，可根据实际导出样本扩展。
- **Knowledge**：知识库检索及 `outputList` 等下游引用方式，具体知识库绑定仍取决于使用环境。
- **Code**：输入变量、JavaScript `handler`、输出 Schema、下游引用及语法校验。
- **LLM**：系统提示词、用户提示词、输入变量、文本/JSON 输出、输出 Schema，以及已在导出文件中出现的部分模型参数。
- **Condition**：条件表达式、if/else 分支、端口依赖和下游路由。
- **VariableMerge**：多 Group 聚合和输出引用；在已测试编辑器中，空 Group 可能不暴露输出字段。
- **Tool**：已掌握通用保存结构和 Bing Search 插件的实际配置方式，可按其他插件的导出结构扩展。

已验证过的组合流程为：

`Start → Knowledge → Code/LLM 证据判断 → Condition → 知识库或 Bing Search 分支 → VariableMerge → 回答 LLM → 复核 LLM → 清理 Code → End`

## 使用边界

- 当前已覆盖构建常用智能问答工作流所需的主要节点。遇到未列出的新节点时，需要提供该节点的脱敏导出样本后再适配。
- 模型、知识库和插件属于具体 HiAgent 环境资源；导入后如果平台未自动保留绑定，需要在界面中选择对应资源。
- Tool 节点目前验证过 Bing Search，其他插件可基于其实际导出结构继续扩展。
- 长期记忆、知识库写入和原生文件引用属于应用设置或尚未探明能力，不影响使用现有节点构建普通问答、检索、搜索、判断和复核工作流。

## 隐私说明

本仓库不包含 probe、HAR、请求响应原文、Cookie、Token、登录信息、员工信息、知识库内容、内部网址、应用 ID、数据集 ID或公司业务提示词。示例必须使用占位符，抓取文件不得进入分发包。

## 使用

将仓库交给支持 Skill 的 Agent，或把 `SKILL.md` 及 `references` 作为自定义指令加载。使用时可说：

> 使用 hiagent-workflow-builder 构建一个导入后可直接使用的 HiAgent 工作流 JSON。

静态检查示例：

```bash
python3 scripts/validate_workflow.py workflow.json
```
