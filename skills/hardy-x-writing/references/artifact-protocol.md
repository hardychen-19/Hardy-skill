# Hardy Skill 产物与工作流协议 v0.1

这份协议连接独立安装的技能。它约定固定工作区、产物类型、元数据和执行顺序；不会让尚未安装的技能自动出现。

## 1. 固定工作区

每台电脑只配置一次 `workspace_root`。首次使用时，若用户没有指定位置，默认使用用户主目录下的 `HardySkill` 文件夹（macOS/Linux：`~/HardySkill`；Windows：`%USERPROFILE%\\HardySkill`）。若用户明确指定其他位置，以用户位置为准。初始化程序或 Agent 创建固定结构后，把绝对路径写入配置：macOS/Linux 为 `~/.config/hardy-skill/config.json`，Windows 为 `%APPDATA%\\HardySkill\\config.json`。配置示例：

```json
{"protocol_version":"0.1","workspace_root":"/home/example/HardySkill"}
```

所有技能先读取这同一份配置，再使用该根目录；运行中不得因某个技能需要新文件而另造工作区。配置存在时不得静默改写 `workspace_root`。若路径暂时不可访问，报告错误并暂停依赖该路径的步骤；不要自动在别处创建替代目录。用户主动迁移工作区时，先搬迁完整产物，再修改配置并核对索引。工作区根目录是用户数据，不放进公开的 Skill 仓库；安装 Skill 的目录也不作为产物目录。

固定结构：

```text
workspace_root/
├── artifacts/
│   ├── review/          # 复盘报告与结构化结论
│   ├── writing/         # 成稿与写作简报
│   ├── cover/           # 封面和设计说明（未来）
│   └── publish/         # 发布队列与回执（未来）
├── sources/             # X 导出、用户素材等只读输入
├── workflows/           # 工作流定义和每次运行记录
└── index.jsonl          # 产物登记表，追加写入
```

这些子目录是固定类别，不按日期或任务再新建目录。首次初始化时只创建上面列出的固定目录；后续每次运行产生**新文件**，避免覆盖历史数据。未安装模块的目录可保持空置。

## 2. 每个产物有正文与清单

产物文件名包含 UTC 时间和唯一 ID，例如 `20260927T103000Z-8f3c-review.json`。同目录保存一个同名 `.manifest.json`，记录：

```json
{
  "protocol_version": "0.1",
  "artifact_id": "20260927T103000Z-8f3c-review",
  "type": "x.review.v1",
  "producer": "hardy-x-review",
  "created_at": "2026-09-27T10:30:00Z",
  "status": "ready",
  "path": "artifacts/review/20260927T103000Z-8f3c-review.json",
  "inputs": ["sources/2026-09-27-overview.csv", "sources/2026-09-27-content.csv"],
  "parent_artifact_ids": [],
  "account": "@example",
  "evidence_status": "verified",
  "review_required": false
}
```

`path` 和 `inputs` 都是相对 `workspace_root` 的路径；每个实际路径必须仍位于该根目录内。`status` 只取 `draft`、`ready`、`failed`、`approved`、`published`。下游技能默认只消费 `ready` 或 `approved` 的产物；公开发布仅消费 `approved` 的内容。产物清单里的状态属于该产物，不代表用户已经批准其他产物或对外动作。

`index.jsonl` 每行记录一个清单路径和 ID，便于按时间查询。清单本身是事实来源；索引丢失可以从各固定目录重建。写产物时先写正文和清单，再把清单路径追加到索引；未完成的正文不得登记为 `ready`。不要把敏感令牌、Cookie 或密码写进正文、清单或索引。

## 3. 用类型决定能否连接

每个子技能声明它接受和产出的类型。总入口只在类型、版本和状态兼容时连接；**任意组合不意味着任意两项都能直接相连**。不兼容时需要一个明确的转换步骤，不能靠猜字段。

第一阶段的类型：

| 类型 | 生产者 | 可供谁消费 | 含义 |
| --- | --- | --- | --- |
| `x.analytics.overview.v1` | 数据导入步骤 | `hardy-x-review` | 账号每日数据 |
| `x.analytics.content.v1` | 数据导入步骤 | `hardy-x-review` | 单帖累计数据 |
| `x.review.v1` | `hardy-x-review` | `hardy-x-writing` 或人工查看 | 净涨粉、内容结论、一个实验 |
| `x.draft.v1` | `hardy-x-writing` | 人工审稿；未来配图与发布模块 | Markdown 正文与同名清单；ready 不等于批准发布 |

写作模块已加入 `x.draft.v1`；未来模块完成后再加入 `x.cover.v1`、`x.publish_queue.v1`、`x.published.v1`。未发布的类型只在这里表示规划，不能当成已实现能力。

复盘产物 `x.review.v1` 至少包含：`account`、`captured_at`、`period`、`overview_net_follows`、`content_attributed_follows`、`evidence`、`experiment`、`limitations`。两个关注字段必须分开。来源 CSV 若缺少 Overview，`overview_net_follows` 设为 `null`，不能用内容归因值补位。

## 4. 工作流由总入口编排

一个工作流文件放在固定的 `workflows/` 目录，写明步骤、输入类型、输出类型和暂停点。总入口先检查技能是否已安装，再逐步执行。每步完成后验证清单、类型、状态和文件存在，才把产物 ID 交给下一步。失败则记录原因并停止依赖它的步骤，不沿用旧产物伪装成功。

工作流定义的最小形状如下。`step_id` 在一份工作流内唯一；`needs` 指向先前步骤；`input_types` 和 `output_type` 必须来自已发布的类型表；`gate` 是进入下一步前的状态要求。

```json
{
  "protocol_version": "0.1",
  "workflow_id": "weekly-review",
  "steps": [
    {
      "step_id": "review",
      "skill": "hardy-x-review",
      "needs": [],
      "input_types": ["x.analytics.overview.v1", "x.analytics.content.v1"],
      "output_type": "x.review.v1",
      "gate": "ready"
    }
  ]
}
```

这只是工作流定义格式；实际运行还需要总入口或宿主 Agent 读取文件、检查输入和依赖，再调用安装的技能。上述示例只有复盘步骤。当前复盘与写作模块已提供协议约定，宿主 Agent 可以按兼容清单衔接；封面和发布尚未实现，不能宣称完整链路已跑通。

当前可编排：`X 数据导入 → 复盘 → 人工查看`，或 `ready 复盘 → 写作草稿 → 人工审稿`。直接对话展示不建立产物工作区。未来可以增加 `复盘 → 写作 → 封面 → 审稿 → 发布 → 复盘`，也可以只运行 `写作 → 封面`；跳过某一步时必须仍满足下一步的输入类型。

同一份产物可被多个技能消费，例如一份复盘同时给写作和人工看。总入口按产物 ID 追踪血缘，避免“拿到了一个文件，但不知道是哪次运行的”。

## 5. 独立安装与升级

每个子技能可以独立下载：它自身的 `SKILL.md` 至少包含配置位置、自己接受/产出的类型，以及保存产物的规则，不要求用户先安装总入口。总入口保存完整协议与编排规则。新版本只能新增兼容字段；改变字段含义或删除字段时升级类型版本，例如从 `x.review.v1` 到 `x.review.v2`，并提供显式转换。总入口的模块列表只列已发布、已安装且通过验证的技能。

## 6. 写作产物 x.draft.v1

`x.draft.v1` 正文是 Markdown，位于固定 `artifacts/writing/`，使用 UTC 时间及唯一 ID 命名，每个版本新建文件。同名 `.manifest.json` 使用前述通用字段，另含 `title`、`language`、`article_type`、`content_format: markdown`。`evidence_status` 为 `verified`、`partial` 或 `unverified`，以实际检查为准；`review_required` 默认 true。ready 表示草稿可审阅，不代表已批准发布；关键事实未解决导致成稿不完整时用 draft。用户明确批准该版本才能改为 approved，后续改写是新版本，需要重新确认。

写作可以不依赖复盘。消费 `x.review.v1` 时先验证清单类型、状态和来源，不把实验建议写成用户已经做过的经历。只有实际存在的输入才登记，用户私有资料和凭据不进入公开仓库。仅要对话中的提纲、示例或正文时不落盘；用户要求保存或模块协作时才执行上述协议。
