# 写作模块产物

对话展示无需创建文件。保存或协作时遵循 [共享协议](artifact-protocol.md)。本模块接受用户材料，也可消费状态为 ready 或 approved 的 `x.review.v1`，保留其数据状态和建议归属。

正文为 UTF-8 Markdown，保存到 `artifacts/writing/<UTC时间>-<唯一ID>-article.md`；同目录为同名去除 `.md` 后缀的 `.manifest.json`。创建新版本文件，不覆盖历史。

清单使用共享字段，并包含 `title`、`language`、`article_type`、`content_format: markdown`。`type` 是 `x.draft.v1`，`producer` 是 `hardy-x-writing`，`evidence_status` 使用 `verified`、`partial` 或 `unverified`，以实际检查为准，不默认 verified。`inputs` 只列固定工作区内实际存在的输入路径；原文件在外部且需要保存来源时，复制到 sources 并在 sources 清单说明来源，不移动原件。直接输入的文本在需要文件协作时保存到 sources，直接对话模式不落盘。

正文和清单完成才登记到 index.jsonl。ready 表示可审阅或交给配图模块，尚不允许公开发布；未解决的关键事实阻止完整成稿时用 draft。默认 `review_required: true`。用户对具体版本明确确认后才标 approved，并保留该确认依据；不把上一次批准自动应用到改写后的版本。

建议在清单的 `unresolved` 中简要记录待核实事实，不把内部审校文字混入正文。不得登记不存在的源文件、模块或图像。
