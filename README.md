# Hardy-skill

Hardy Chen 的模块化中文长文写作与 X 运营技能合集。每个能力是独立的 Agent Skill，可单独安装，也可安装整个合集。当前版本 **0.5.1**。

## 上传自己的照片，选一套配图画风

首次使用会提示两个选项：直接使用随包的 Hardy IP（不用照片），或上传自己的照片创建专属角色。选择个人角色时，给 Codex 一张清晰个人照片，`hardy-x-illustrations` 会生成并保存你的专属角色；以后为文章配图直接复用。默认沿用 Hardy 的柔和立体正文画风，也可以选手绘笔记、清淡水彩或深色科技。照片决定身份，文章决定知识关系，主题决定画风。

**[看四套实际预览与可复制提示词 →](examples/illustration-themes/README.md)**

| 柔和立体 | 手绘笔记 |
| --- | --- |
| ![柔和立体预览](skills/hardy-x-illustrations/assets/themes/soft-3d.png) | ![手绘笔记预览](skills/hardy-x-illustrations/assets/themes/ink-notes.png) |

| 清淡水彩 | 深色科技 |
| --- | --- |
| ![清淡水彩预览](skills/hardy-x-illustrations/assets/themes/watercolor.png) | ![深色科技预览](skills/hardy-x-illustrations/assets/themes/midnight-tech.png) |

先安装配图模块，然后上传照片并说：

```text
使用 $hardy-x-illustrations，根据这张照片建立并保存我的角色。
主题选“柔和立体”，为下面正文生成一张解释图预览。
【粘贴正文】
```

只上传照片时先交付角色；已有角色时不用再传照片。实际生成依赖当前 Codex 会话的图像工具，Skill 不内置 API。

## 已提供的模块

| 目录 | 用途 |
| --- | --- |
| `hardy-skill/` | 总入口，识别需求并路由实际安装的模块 |
| `skills/hardy-x-writing/` | Hardy Chen 的中文长文写作、提纲、续写、改写与审校，重点支持 X 长文 |
| `skills/hardy-x-review/` | X Analytics 数据复盘，区分账号净涨粉与单帖归因关注 |
| `skills/hardy-x-illustrations/` | 从个人照片建立角色，四套主题任选，按文章选择认知节点，生成正文解释图、保留真实截图并插入成稿，完整文章附文末关注图；暂不生成封面 |

写作模块融合卡兹克的叙事推进、Miles 文风说明中的具体解释，以及宝玉的标题与编辑方法。当前默认表达参考 Roland.W：从具体困惑进入，用追问、明确判断和具体后果展开，保留作者原话与取舍。方法见[自然表达与作者在场](skills/hardy-x-writing/references/natural-expression.md)。文章类型改变结构，作者身份仍为 Hardy Chen。教程写到能操作和验证，故事带读者走过真实发现；不编造经历，不为了悬念修改数字，不强制口语词频或文化升华，也不承诺通过 AI 检测。该表达更新已进入本次 0.5.1 源码与下载包。

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

默认柔和立体主题沿用 Hardy 正文图解的材质、留白与主次。首次从个人照片建立角色档案，后续复用；原作者人物可在用户明确选择 Hardy IP 后直接使用，不默认替换新用户身份；选择会保存，后续不重复询问。角色与身份说明保存在个人配置区（默认 `~/.config/hardy-skill/illustrations/`；Windows 使用 APPDATA），可用随包脚本检查并恢复引用，不写入技能安装目录。

完整文章按理解难点选择图型与数量，保留准确截图，输出图片、提示词、清单和配图版 Markdown。默认结尾附一张同主题关注图，用户可修改文案或取消；单张预览不附加。当前不生成封面。

[主题选择与独立包内预览](skills/hardy-x-illustrations/references/themes.md) · [照片初始化与复用规则](skills/hardy-x-illustrations/references/character.md)

示例、个人身份和原始照片分别管理。安装包只收录仓库明确列出的生成预览、参考图、规则和档案辅助脚本，不收录用户原始照片、个人配置与运行文件。主题可以切换，人物身份保留，成图仍需检查。

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
│   └── hardy-x-illustrations/   # 正文解释图与 Markdown 插入（含文末关注图，暂不生成封面）
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

只使用 Python 标准库。打包脚本生成各模块独立 ZIP 和全集 ZIP；只收录配图模块明确列出的生成图（原有六张参考图、四张主题预览及照片生成角色示例）、档案辅助脚本和主题规则；不收录原始照片、其他用户素材、账号数据或工作区。全集包使用 `Hardy-skill-bundle-<版本>.zip`，总入口独立包使用 `hardy-skill-<版本>.zip`，避免大小写不敏感文件系统中的重名覆盖。安装包见 [GitHub Releases](https://github.com/hardychen-19/Hardy-skill/releases)。

## 来源与许可

合集采用 MIT。写作模块的参考来源、改编范围与上游版权见 [sources.md](skills/hardy-x-writing/references/sources.md) 和模块 LICENSE；来源署名不作为生成文章的作者身份。
