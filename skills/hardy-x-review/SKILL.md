---
name: hardy-x-review
description: 复盘 Hardy 的 X 账号增长与内容表现。用于分析 X Analytics Overview/Content CSV、历史快照、涨粉转化、爆款和下一次内容实验；不能取数时如实说明。
metadata:
  short-description: Hardy X 数据复盘
---

# Hardy X Review

## 工作目标

把“账号有没有涨粉”和“哪条内容带来归因关注”分开回答，并把结果转成下一次可验证的内容实验。

## 数据输入

优先读取当次 X Analytics 导出的 Overview 和 Content CSV；当前环境无法访问后台时读取用户提供的 CSV。保留抓取时间、账号、时间窗和原始文件路径。可以参考小木 X 的分类方法和历史记录，但不能把内容表的统计口径直接当账号净涨粉。若用户提供了自己的知识库规则，先读取相关部分；本技能不预设任何个人路径。

## 固定工作区与独立安装

首次运行时读取工作区配置：macOS/Linux 为 `~/.config/hardy-skill/config.json`，Windows 为 `%APPDATA%\\HardySkill\\config.json`。若不存在，默认建立用户主目录下的 `HardySkill` 文件夹；用户在首次运行明确指定其他位置时使用该位置，并把 `workspace_root` 记入配置。配置存在后只复用其绝对路径，不因新任务创建另一工作区；路径不可访问时报告阻碍。技能安装目录不能存放用户产物。

工作区固定使用 `sources/` 保存导入的原始 CSV，`artifacts/review/` 保存复盘产物，`workflows/` 保存流程记录，`index.jsonl` 登记清单；不按日期另建文件夹。若原始 CSV 在别处，复制到 `sources/` 并保留来源和抓取时间，不移动或覆盖原件。

## 核心口径

- 账号净涨粉：`Overview.New follows - Overview.Unfollows`。
- Content 的 `New follows`：单帖归因关注，只用于比较帖子，不等于账号净涨粉。
- Overview 的日期是账号日指标；Content 的日期是帖子发布日期，内容指标通常是导出时累计值。
- 抓取当天可能未结算，单独标为暂定；不要把它和完整自然日混在一起。
- 多次导出按 `Post id` 对比增量；只有一次快照时，不声称拥有 24/72 小时增量。

## 分析步骤

1. 检查列名和账号；缺列先报告，不静默填成零。
2. 计算昨日完整日、当天暂定、近 7 日净涨粉、当前粉丝数和目标缺口。
3. 对内容按主帖、疑似回复、长文/链接和用户自定义主题分类。`@` 和链接前缀只是启发式，抽查边界样本。
4. 按类型比较帖子数、曝光中位数、每千展示单帖归因关注、主页访问、收藏和讨论质量；爆款单列，不只看均值。
5. 若有历史护照或旧快照，比较上期目标、执行量、内容配比和新出现的异常；没有历史就标为基线。
6. 交叉检查外部转发、发布时间、长文生命周期、主页改动和样本量，避免把相关性写成算法规律。
7. 只提出一个次日实验，给出改变变量、保持变量、观察窗口和继续/停止条件。

## 输出

按“数据状态 → 账号结果 → 内容结构 → 交叉解释 → 一个实验 → 限制”输出。引用帖子时给链接，事实和推断分开。只有内容 CSV 时，不能给出账号净涨粉；要明确缺少 Overview 的 `Unfollows`。

每次完成复盘，在 `artifacts/review/` 生成一份新的 JSON 产物和同名 `.manifest.json`，不覆盖旧文件。产物类型是 `x.review.v1`，至少包含 `account`、`captured_at`、`period`、`overview_net_follows`、`content_attributed_follows`、`evidence`、`experiment`、`limitations`。没有 Overview 时 `overview_net_follows` 为 `null`。清单记录 `protocol_version: 0.1`、唯一 `artifact_id`、`type`、`producer: hardy-x-review`、创建时间、状态、相对工作区路径及输入 CSV 路径；正文和清单写成功后再把清单路径追加到 `index.jsonl`。下游模块只消费状态为 `ready` 的产物，不凭文件名猜测“最新报告”。

## 边界

不发帖、点赞、回复、关注，不读取账密目录，不使用其他账号数据冒充目标账号。无法登录或导出时，说明失败步骤和仍可验证的范围。
