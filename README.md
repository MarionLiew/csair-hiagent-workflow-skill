# CSair HiAgent Workflow Skill

用于辅助 Codex 构建、修改、校验和排查 HiAgent 工作流 JSON。它来自对 HiAgent v2.1 相关文档、工作流导出文件、成功导入结果和部分运行探测的脱敏总结，不是 HiAgent 全平台、全版本的完整规范。

## 已探明的节点

目前具备实际结构依据的节点类型如下：

- **Start**：固定名称、输入变量声明和下游字段引用。
- **End**：固定名称和变量输入连接；并非所有回复模式都已探明。
- **Knowledge**：知识库检索及 `outputList` 等下游引用方式，具体知识库绑定仍取决于使用环境。
- **Code**：输入变量、JavaScript `handler`、输出 Schema、下游引用及语法校验。
- **LLM**：系统提示词、用户提示词、输入变量、文本/JSON 输出、输出 Schema，以及已在导出文件中出现的部分模型参数。
- **Condition**：条件表达式、if/else 分支、端口依赖和下游路由。
- **VariableMerge**：多 Group 聚合和输出引用；在已测试编辑器中，空 Group 可能不暴露输出字段。
- **Tool**：已了解通用保存结构，但运行验证目前只覆盖一个已配置的 Bing Search 插件实例。

已验证过的组合流程为：

`Start → Knowledge → Code/LLM 证据判断 → Condition → 知识库或 Bing Search 分支 → VariableMerge → 回答 LLM → 复核 LLM → 清理 Code → End`

## 明确的局限性

- 不是所有 HiAgent 节点的完整目录或 JSON Schema；未列出的节点不能视为已经支持。
- End 节点不同“回复模式”的全部序列化字段尚未完整采集，不能根据界面文字猜测 JSON。
- Tool 节点只实际验证过 Bing Search；其他插件的 ID、鉴权、输入输出和异常格式需要单独样本。
- 尚未验证知识库写入、自动审核、文件提交等节点。
- 长期记忆在已测试产品中属于智能体/应用设置，尚未证明可以由该工作流节点实现。
- 工作流内部知识检索尚未证明能触发右侧文件卡片、精确页码高亮等原生引用界面。
- 普通 Markdown 文件链接不能保证触发原生引用或准确跳转 PDF 页码。
- Word、PDF、Excel、PPT、图片和 OCR 的解析效果取决于平台解析器，不属于本 Skill 的保证范围。
- UOS、浏览器和 driver/probe 的兼容性需要在目标环境中单独测试。
- 不保证未经验证的其他 HiAgent 版本可以直接兼容。
- 静态校验只能发现 JSON、依赖、变量和 JavaScript 语法问题，不能证明模型、知识库、插件、权限、额度、记忆、引用和界面渲染在运行时可用。

对于尚未探明的节点，必须取得脱敏后的节点导出文件，或只包含该节点保存操作的 probe；完成结构提取并通过导入或运行测试后，才能加入“已支持”范围。

## 隐私说明

本仓库不包含 probe、HAR、请求响应原文、Cookie、Token、登录信息、员工信息、知识库内容、内部网址、应用 ID、数据集 ID或公司业务提示词。示例必须使用占位符，抓取文件不得进入分发包。

## 使用

将仓库目录放入 Codex 的 skills 目录，或直接让 Codex 安装该仓库。使用时可说：

> 使用 `$hiagent-workflow-builder` 构建或检查一个可导入的 HiAgent 工作流 JSON。

静态检查示例：

```bash
python3 scripts/validate_workflow.py workflow.json
```
