# Hardy-skill

Hardy Chen 的模块化中文长文写作与 X 运营技能合集。每个能力是独立的 Agent Skill，可单独安装，也可安装整个合集。当前版本 **0.4.1**。

## 已提供的模块

| 目录 | 用途 |
| --- | --- |
| `hardy-skill/` | 总入口，识别需求并路由实际安装的模块 |
| `skills/hardy-x-writing/` | Hardy Chen 的中文长文写作、提纲、续写、改写与审校，重点支持 X 长文 |
| `skills/hardy-x-review/` | X Analytics 数据复盘，区分账号净涨粉与单帖归因关注 |
| `skills/hardy-x-illustrations/` | 按文章选择认知节点，生成正文解释图、保留真实截图并插入成稿；封面需明确请求 |

写作模块融合卡兹克的叙事推进、Miles 文风说明中的具体解释，以及宝玉的标题与编辑方法。文章类型改变结构，作者声音保持一致。教程写到能操作和验证，故事带读者走过真实发现；不编造经历，不为了悬念修改数字，不强制口语词频或文化升华。

这是指令型技能合集，效果依赖宿主模型、工具和素材。没有内置账号登录器、自动发布器、确定性写作引擎或通用工作流执行程序。模块协议可供宿主 Agent 编排，尚未验证完整发布链。

## 使用示例

```text
用 hardy-x-writing，把这份素材写成一篇面向 AI 初学者的 X 长文。
用 hardy-x-writing，先给我文章提纲，直接在对话里展示。
用 hardy-x-writing，检查这篇草稿的逻辑、步骤和文风，保留我的真实经历。
用 hardy-skill，根据这份 X Analytics CSV 做复盘，再给下一篇长文建议。
用 hardy-x-illustrations，根据这篇 Markdown 长文自动选择正文解释图，按内容决定数量、意象与动作，保留已有截图，并把图片链接插入成稿。
```

默认作者为 Hardy Chen。其他用户可提供作者资料或可选 EXTEND.md 覆盖作者名、读者和篇幅；职业、经历和联系方式不会自动补写。用户知识库是可选上下文，安装包不依赖任何个人路径。实际生成图片依赖宿主提供图像生成能力；发布还需对应模块与用户授权。

## 正文配图

默认采用已认可的 Hardy 哑光立体 IP 与编辑图解，人物小比例辅助、知识关系为主体。按全文理解难点选择图型与数量，保留已有准确截图；只试一张时不批量配图。完整交付保留原稿，输出图片、提示词、清单与正文配图版 Markdown。

配图目录包含已确认的角色生成图、正文样稿和三张用户选定的物件演示参考，独立安装时无需再找私人角色文件。案例索引按需引导反馈回路、分类检索和条件分支；样稿只校准材质、主次和可读性，不把每篇文章固定成三栏。其他作者可以指定自己的已确认参考。原始照片、私人知识库和本地运行清单不在安装包中。

## 安装

支持 Agent Skills 的工具可直接请求安装指定目录，例如：

```text
帮我安装这个写作技能：https://github.com/hardychen-19/Hardy-skill/tree/main/skills/hardy-x-writing
帮我安装这个配图技能：https://github.com/hardychen-19/Hardy-skill/tree/main/skills/hardy-x-illustrations
```

也可将该完整目录复制到宿主 skills 目录。Codex 用户级目录通常是 `~/.codex/skills/`，项目级可使用 `.agents/skills/`。目录必须包含全部 references、agents、assets 与 LICENSE；单独复制 SKILL.md 会丢失参考规则。需要统一入口时同时安装 `hardy-skill/`。

### Claude Code 插件合集

参考 baoyu-skills 的单插件清单结构，仓库提供 `.claude-plugin/marketplace.json`，注册总入口和三个子技能：

```text
/plugin marketplace add hardychen-19/Hardy-skill
/plugin install hardy-skills@hardy-skills
```

该清单已静态验证，Claude Code 内实际安装仍需在目标环境验证。不支持插件的工具仍可按目录独立安装。

## 目录结构

```text
Hardy-skill/
├── .claude-plugin/marketplace.json
├── hardy-skill/                 # 总入口，保留原有安装路径
├── skills/
│   ├── hardy-x-writing/         # 写作模块及按需参考
│   ├── hardy-x-review/          # 数据复盘
│   └── hardy-x-illustrations/   # 正文解释图与 Markdown 插入（封面需明确请求）
├── scripts/                    # 检查与生成独立下载包
├── LICENSE
└── RELEASE.md
```

## 模块协作

需要保存或连接模块时使用[固定工作区与产物协议](hardy-skill/references/artifact-protocol.md)：固定工作区默认 `~/HardySkill`，可由用户指定。复盘输出 `x.review.v1`，写作输出 `x.draft.v1`，配图输出 `x.illustrated-draft.v1`。清单明确来源、版本、状态和未核实内容；ready 草稿不代表批准发布。只在对话展示提纲或文章时不要求建立工作区。

发布仍在规划中；短推与线程也不属于本版写作范围。配图技能需要宿主提供图像生成能力，不内置图片生成 API。

## 开发与打包

```bash
python3 scripts/validate.py
python3 scripts/package.py
```

只使用 Python 标准库。打包脚本生成各模块独立 ZIP 和全集 ZIP；只额外收录配图模块明确列出的五张生成图（定稿 IP、正文样稿及三张案例参考）；不收录原始照片、其他用户素材、账号数据或工作区。安装包见 [GitHub Releases](https://github.com/hardychen-19/Hardy-skill/releases)。

## 来源与许可

合集采用 MIT。写作模块的参考来源、改编范围与上游版权见 [sources.md](skills/hardy-x-writing/references/sources.md) 和模块 LICENSE；来源署名不作为生成文章的作者身份。
