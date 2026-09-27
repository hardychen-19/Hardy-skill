---
name: hardy-skill
description: Hardy 的 X 创作与运营技能总入口。当前路由已发布的 X 数据复盘技能；写作、封面和发布能力会在完成后逐个加入。
metadata:
  short-description: Hardy X 创作运营总入口
---

# Hardy Skill

这是模块化总入口。当前发布的子技能是 `hardy-x-review`，用于 X 数据复盘。写作、封面和发布仍在规划中；只有相应子技能实际安装后，才按其 `SKILL.md` 执行。

## 当前路由

- 用户要看 X Analytics、涨粉、内容转化、日/周复盘：读取已安装的 `hardy-x-review/SKILL.md`。
- 若找不到该子技能，说明缺少模块，给出独立安装路径；不要声称总入口本身能完成账号数据抓取或分析。
- 其他 X 创作任务按当前环境已有的工具和用户指令处理，不宣称未发布模块已存在。

## 共享约定

- 先核对目标账号、数据来源和抓取时间。账号净涨粉用 Overview 的 `New follows - Unfollows`，Content 的 `New follows` 只作单帖归因关注。
- 用户的私有知识库是可选上下文，只有用户明确提供并且当前环境确实可访问时才读取。公开安装包不依赖任何个人绝对路径。
- 生成草稿和分析不代表用户已确认或发布；实际对外操作遵循用户在当前任务给出的授权。

组合工作流遵循 `references/artifact-protocol.md`：从用户固定工作区读取产物清单，按类型和状态连接已安装模块。首次使用时初始化一次工作区，此后复用配置，不能临时改到技能安装目录或新造日期文件夹。未来模块与发布顺序见 `references/architecture.md`。总入口和 `hardy-x-review` 可分别安装。
