# 上传照片，选择你的正文配图风格

先安装 [hardy-x-illustrations](../../skills/hardy-x-illustrations/SKILL.md)。第一次给 Codex 一张清晰个人照片，角色会自动生成并保存在个人配置区，后续文章直接复用。单独安装配图模块即可；实际图片生成需要当前 Codex 会话提供可用的图像工具。

下面四张是本次实际生成的预览：同一个由作者照片生成的角色，同一段 [示例正文](source.md)，只改变画风。生成步骤、提示词、实际尺寸与检查结果见 [演示清单](demo-manifest.json)。它们是作者演示，不会成为新用户默认人物；样例通过检查不表示获得用户审美批准。

## 选择一种画风

| 画风 | 适合的视觉偏好 | 可复制指令 |
| --- | --- | --- |
| 柔和立体 | 喜欢暖白、柔和体积与清楚关系 | [指令与规则](../../skills/hardy-x-illustrations/references/themes/soft-3d.md) |
| 手绘笔记 | 喜欢细线、纸面、轻松表达 | [指令与规则](../../skills/hardy-x-illustrations/references/themes/ink-notes.md) |
| 清淡水彩 | 喜欢柔色、留白、自然质感 | [指令与规则](../../skills/hardy-x-illustrations/references/themes/watercolor.md) |
| 深色科技 | 喜欢深蓝、清楚轮廓与技术感 | [指令与规则](../../skills/hardy-x-illustrations/references/themes/midnight-tech.md) |

### 柔和立体 · soft-3d
![柔和立体实际预览](../../skills/hardy-x-illustrations/assets/themes/soft-3d.png)
[本次完整生成提示词](prompts/soft-3d.md)

### 手绘笔记 · ink-notes
![手绘笔记实际预览](../../skills/hardy-x-illustrations/assets/themes/ink-notes.png)
[本次完整生成提示词](prompts/ink-notes.md)

### 清淡水彩 · watercolor
![清淡水彩实际预览](../../skills/hardy-x-illustrations/assets/themes/watercolor.png)
[本次完整生成提示词](prompts/watercolor.md)

### 深色科技 · midnight-tech
![深色科技实际预览](../../skills/hardy-x-illustrations/assets/themes/midnight-tech.png)
[本次完整生成提示词](prompts/midnight-tech.md)

## 从照片到个人角色

本次先从作者照片实际生成角色，检查第一轮后修正材质与比例，再保存角色档案，四套预览复用这个身份。原照片没有纳入仓库，只保留生成示例。

![本次照片生成的作者示例角色](../../skills/hardy-x-illustrations/assets/themes/photo-character-demo.png)

[照片初始化与修正提示词](prompts/character-initialization.md) · [可见身份说明](identity.md)

## 直接这样用

上传个人照片，同时粘贴下面这句话。已有角色时只需要文章与主题，不用再传照片。

```text
使用 $hardy-x-illustrations，根据我上传的照片建立并保存自己的角色。
主题选“手绘笔记”，先给下面正文做一张预览。
保存实际图片和完整提示词，不修改原文，不附关注图。
【粘贴你的正文】
```

单张满意后：

```text
使用 $hardy-x-illustrations，复用我的角色，主题选“手绘笔记”。
为 article.md 配图，按理解难点决定张数；保留原稿，另存配图版 Markdown。
输出图片、提示词和检查清单。本次附一张文末关注图，不做封面，不发布。
```

主题可随时换，人物身份会沿用。照片决定身份，文章决定知识对象，主题决定媒介与配色；没有照片不能生成你的专属人物，没有正文只生成角色。参考图能帮助保持一致性，但照片质量、模型与修改次数仍会影响成图和额度消耗。
