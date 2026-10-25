# Vibe 知识大赏 · AI 知识视频制作 Skill

<p align="center">
  <b>把数学、概率、哲学等硬知识，拍成电影感的抖音知识大片</b><br>
  纯代码生成 · 无配音 · 双语字幕 · 历史文献再现 · 动画模拟推演
</p>

<p align="center">
  <img src="https://img.shields.io/badge/style-Vibe%E7%9F%A5%E8%AF%86%E5%A4%A7%E8%B5%8F-0A0A1E" alt="style">
  <img src="https://img.shields.io/badge/render-Canvas%202B%20%2B%20render(t)-C9A96A" alt="render">
  <img src="https://img.shields.io/badge/audio-numpy%20synth%20BGM-76BPM" alt="audio">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
</p>

---

> **这是什么**：一套完整的 Claude / AI Agent 技能（Skill），逆向工程自抖音「Vibe知识大赏」系列爆款知识视频（由 @Iwanau / @Juno / 叁号暗房 用 Claude Opus 5.5 代码生成）。装上它，对 AI 说一句话，就能从选题走到成片 MP4 + 抖音发布文案。
>
> **What is this**: A complete AI-agent skill that reproduces the "Vibe Knowledge Awards" style of viral Douyin explainer videos — 100% code-generated (HTML Canvas + synthesized music), no voiceover, bilingual subtitles, cinematic history-document recreations. Say one sentence, get a finished MP4.

## 🆕 v2.0 / v2.1 更新：从"长得像"到"讲得懂"

> 详细说明见 **[docs/CHANGELOG-v2.md](docs/CHANGELOG-v2.md)**。全部为增量新增，v1 用法完全不变。

v1 解决"怎么做出这种风格"，v2 解决"怎么让观众看懂"，v2.1 补齐了工程细节与发布运营，形成完整闭环：

| 新增 | 内容 |
|---|---|
| `references/visualization-design.md` | **讲解设计**：配图 vs 讲解的分界、概念→形象的六级提问、六种呈现动作、约 1/5 句子"不画"、一个比喻用到底、分镜表七列格式 |
| `references/copywriting-rules.md` | **字幕稿文体**：句量句长、句式工具箱、禁用清单、强调的克制规则、事实与出处 |
| `references/structure-bible.md` | **结构圣经**：选题四项打分、三种骨架、标准时间轴、十条叙事定律、悬念/反转/常驻读数 |
| `references/visual-grammar.md` | **画面语法速查**：21 类句型→演法对照表、分区纪律、十种转场手法（含时长）、动效手感六条 |
| `references/quality-gate.md` | **质量门**：看图改图毛病对照表、两轮修复流程、终检三遍、数字纪律（先算后写、固定种子、屏上计数） |
| `references/render-craft.md` | **渲染工程手册**：纯函数与固定种子、模拟查表回放、辉光管线、对数推拉、八种常见装置写法 |
| `references/rework-scripts.md` | **返工话术与分步推进**：八轮提示词（每轮有过关标准）+ 20 条"看到毛病怎么一句话说清" |
| `references/alternate-worlds.md` | **扩展视觉世界**：题材→世界匹配、新世界七项设计清单、节奏经验值表、"厂牌"概念 |
| `docs/common-mistakes.md` | **常见错误对照表**：渲染/剧本/画面/声音/事实五类症状速查 |
| `docs/publish-guide.md` | **发布指南**：发布前检查清单、48 小时数据复盘、数据差先查叙事 |
| `docs/topic-seeds.md` | **选题种子库**：五个出题方向、种子题示例、四关检验 |
| `references/beat-scaffold.md` | **逐拍写法骨架**（v2.2）：130 秒标准片拆成 ~44 个功能位置，每拍的写作任务与写法公式 |
| `references/image-prompts.md` | **出图提示词规范**（v2.2）：风格后缀六件事、六条规则、一期典型出图清单 |
| `docs/strict-mode.md` | **严格模式**（v2.2）：两档工作模式（自由/严格）、逐关完成标志、弱模型降级方案 |
| `references/remotion-track.md` | **Remotion 路线**（v2.4）：把本方法论跑在 Remotion 里的完整对照——心智模型、跑片流程、参数化模板、与质量门的对接 |
| `render_frames.py --sheet / --stills / --motion` | 三种**看图改图**模式：总览拼图 / 原尺寸静帧 / 转场逐帧拼图，几秒出图 |

## 📚 方法论地图：每一环都有文档接住

```
想法 ──── docs/topic-seeds + structure-bible §1 ────→ 立题与事实表
     ──── references/visualization-design ────→ 概念→形象→句子
     ──── references/copywriting-rules ────→ 字幕稿
     ──── references/visual-grammar ────→ 分镜表（演法+转场+动效）
     ──── references/style-guide / alternate-worlds ────→ 视觉世界
     ──── assets/template.html + render-craft ────→ 代码实现
     ──── scripts/render_frames + synth_bgm + build_video ────→ 渲染合成
     ──── qa_check + quality-gate + common-mistakes ────→ 自检修复
     ──── references/rework-scripts ────→ 不满意时的返工推进
     ──── docs/publish-guide ────→ 发布与数据复盘 ────→ 回到选题
```

七步流程与文档的对应：**第 1 步**选题核实读 `topic-seeds` 与 `structure-bible` §1；**第 2 步**剧本读 `visualization-design` + `copywriting-rules`；**第 3 步**分镜读 `visual-grammar` + `structure-bible` 十条定律；**第 4 步**确认；**第 5 步**代码读 `template.html` + `render-craft`；**第 6 步**渲染合成用四件套脚本；**第 7 步**自检读 `quality-gate` + `common-mistakes`，需要返工用 `rework-scripts`。

## 🧭 两条使用路径

**新手（第一次做）**：按 SKILL.md 七步走，不要跳步——先读 `visualization-design.md` 再动笔；分镜表没写完不写代码；每做完两三站就 `--sheet 16` 看图；卡住查 `common-mistakes.md`。第一版画面一定有毛病，按 `quality-gate.md` 修两轮是正常流程。用的模型不算强？读 `docs/strict-mode.md`，照逐拍骨架填空。

**熟手（做过几条）**：直接从 `references/prompt-brief.md` 的简报模板开工；写分镜时开着 `visual-grammar.md` 速查；大题目用 `rework-scripts.md` 的八轮分步推进；想加底图读 `image-prompts.md`；想在运营上精进读 `publish-guide.md`。

## ❓ FAQ

**Q：我不在 CodeBuddy，能用吗？**
能。知识文档任何 AI 都能读；渲染流水线需要能跑命令的环境，见 [docs/use-with-other-ai.md](docs/use-with-other-ai.md)。

**Q：一定要会 React / Remotion 吗？**
不需要。本仓库是原生 JS + Canvas，页面暴露 `window.render(t)` 纯时间函数，Python 只负责截图和合成。

**Q：可以换自己的风格吗？**
可以。默认风格在 `references/style-guide.md`；想建第二套视觉世界按 `references/alternate-worlds.md` 的七项清单来，注意保留你的"厂牌"（片名卡/字幕习惯）。

**Q：画面上的数字能自己编吗？**
绝对不能。先算后写：数字由代码算出或查证后回填文案；模拟用固定种子；屏上计数是真的在数。这是这种片子的可信度来源。

**Q：为什么我的片子"看着像但没人看完"？**
先查叙事不查画面：和观众有关吗？有悬念吗？中段转到"你"了吗？见 `publish-guide.md` §三。

## 🎬 这种视频长什么样

成片规格（逆向自 8 条原片的实测数据）：

| 维度 | 规范 |
|---|---|
| 画幅 | 1920×1080 横屏，30fps |
| 时长 | 2:00–2:45 |
| 声音 | **无旁白配音**，纯器乐 BGM 76–78 BPM（沉静纪录片节奏，numpy 从零合成） |
| 画面 | 深蓝黑底 `#0A0A1E`，五区布局（水印/顶标签/中央动画/注释带/双语字幕带） |
| 密度 | 逐秒运动均值 3.97，静止秒 < 25% —— 画面必须一直在动 |
| 严谨 | 结尾必有学术引用 + 免责声明，历史图示必标"示意图" |

六段叙事弧：**冷开场钩子 → 历史锚点（真实文献再现）→ 机制动画模拟 → 反直觉转折 → 现实落点 → 声明+引用收尾**

## 🚀 快速开始

### 安装到 CodeBuddy / Claude Code

```bash
# 方式一：克隆到技能目录
git clone https://github.com/<你的用户名>/vibe-knowledge-video.git
cp -r vibe-knowledge-video ~/.codebuddy/skills/

# 方式二：项目级安装
cp -r vibe-knowledge-video /path/to/your/project/.codebuddy/skills/
```

### 在豆包 / Codex / Cursor / Trae 上使用

本技能不绑定 CodeBuddy——**知识文档任何 AI 都能读，渲染流水线需要能执行命令的环境**：

| 工具 | 用法 |
|---|---|
| OpenAI Codex CLI | clone 本仓库直接开工，根目录 `AGENTS.md` 自动生效 |
| Cursor / Trae | clone 后让 AI「先读 SKILL.md 和 AGENTS.md 再动手」 |
| 豆包网页版/App | 当编剧+码农用（出剧本/分镜/index.html），渲染在你本地跑 |

详见 **[docs/use-with-other-ai.md](docs/use-with-other-ai.md)**（含豆包版完整操作流与本地渲染命令）。

### 依赖

| 工具 | 用途 | 说明 |
|---|---|---|
| Python 3.10+ | 渲染/配乐/自检脚本 | `pip install playwright pillow numpy` |
| Playwright + Chromium | 逐帧截图 | `playwright install chromium` |
| ffmpeg | 视频合成 | 需 H.264 编码器（libx264 或 libopenh264，脚本自动检测） |
| tesseract + chi_sim（可选） | QA 时 OCR 校验字幕 | `apt install tesseract-ocr tesseract-ocr-chi-sim` |

### 使用

对装好技能的 AI 说：

```
用 vibe-knowledge-video 做一条《××》的知识视频
```

它会带你走完七步流水线：

```
选题核实 → 剧本 → 分镜表 → 你确认 → 代码实现 → 渲染合成 → 自检交付
```

或者手动调用脚本三件套：

```bash
# 1. 逐帧渲染（页面需暴露 window.render(t) 纯时间函数）
python3 scripts/render_frames.py index.html out_frames/ --fps 30 --duration 130

# 2. 合成 77BPM 小调 BGM（织体分段对齐分镜章节）
python3 scripts/synth_bgm.py bgm.wav --bpm 77 --duration 130 \
  --sections "0,8,pad;8,30,piano;30,90,full;90,105,arp;105,120,piano;120,130,outro"

# 3. 帧序列 + BGM → MP4（-14 LUFS 响度，抖音标准）
bash scripts/build_video.sh out_frames/ bgm.wav final.mp4

# 4. 六维自检（不过不出门）
python3 scripts/qa_check.py final.mp4
```

从 `assets/template.html` 开始——它已内置五区布局、双语字幕系统、标题卡、晾衣绳卡片/纸艺母题库、固定种子随机数、缓动函数库。

## 📁 仓库结构

```
vibe-knowledge-video/
├── SKILL.md                    # 技能主文件：触发条件 + 七步工作流 + 铁律（v2.x 接入讲解设计/质检关）
├── AGENTS.md                   # 通用 AI 入口指令（Codex/Cursor/Trae 自动识别）
├── references/
│   ├── visualization-design.md # 🆕 讲解设计：配图 vs 讲解、形象提问法、六种呈现动作、何时"不画"
│   ├── copywriting-rules.md    # 🆕 字幕稿规范：句式工具箱、禁用清单、强调克制规则
│   ├── structure-bible.md      # 🆕 结构圣经：选题打分、三种骨架、十条叙事定律
│   ├── visual-grammar.md       # 🆕 画面语法：句型→演法对照表、十种转场手法、动效手感
│   ├── beat-scaffold.md        # 🆕 v2.2 逐拍写法骨架：~44 个功能位置与写法公式
│   ├── image-prompts.md        # 🆕 v2.2 出图提示词规范：风格后缀、六条规则、典型清单
│   ├── quality-gate.md         # 🆕 质量门：看图改图毛病表、两轮修复、终检门槛、数字纪律
│   ├── render-craft.md         # 🆕 v2.1 渲染工程：固定种子、模拟查表、辉光管线、装置写法
│   ├── rework-scripts.md       # 🆕 v2.1 返工话术 + 八轮分步推进提示词
│   ├── alternate-worlds.md     # 🆕 v2.1 扩展视觉世界：题材匹配、七项设计清单、节奏经验值
│   ├── remotion-track.md       # 🆕 v2.4 Remotion 路线：方法论 × React 时间线的完整对照
│   ├── style-guide.md          # 风格 DNA 完整规范（布局坐标/配色/动效/母题库）
│   ├── narrative-templates.md  # 8 条原片逐段拆解 + 六段式剧本模板 + 选题公式
│   └── prompt-brief.md         # 可直接填空的 XML 创作简报模板
├── scripts/
│   ├── render_frames.py        # 逐帧渲染器（v2 新增 --sheet/--stills/--motion 看图模式）
│   ├── synth_bgm.py            # numpy 合成配乐（pad/钢琴/kick/shaker/琶音，段落织体）
│   ├── build_video.sh          # ffmpeg 合成（编码器自动回退 + 响度归一）
│   └── qa_check.py             # 自动 QA（规格/深色占比/字幕带/节奏/削波）
├── assets/
│   └── template.html           # 标准模板：开箱即改的分镜配置区
├── docs/
│   ├── CHANGELOG-v2.md         # 🆕 v2.x 升级完整说明
│   ├── common-mistakes.md      # 🆕 v2.1 常见错误对照表（五类症状速查）
│   ├── publish-guide.md        # 🆕 v2.1 发布指南：检查清单 + 48 小时数据复盘
│   ├── topic-seeds.md          # 🆕 v2.1 选题种子库：出题方向 + 种子题 + 四关检验
│   ├── strict-mode.md          # 🆕 v2.2 严格模式：两档工作模式 + 降级方案
│   ├── use-with-other-ai.md    # 豆包/Codex/Cursor/Trae 跨平台使用指南
│   └── original-analysis/      # 8 条原片逐秒 OCR 记录（风格逆向的一手数据）
├── examples/                   # 示例项目（欢迎 PR 你的作品）
├── README.md
└── LICENSE
```

## 🔍 风格是怎么逆向出来的

对 8 条原片（共 17.5 分钟）做了程序化逐帧分析：

- **下载原片**（1920×1080），每秒抽帧，共 **1091 帧**
- **逐帧 OCR**（中文+英文），还原每条片逐秒的完整文案流（见 `docs/original-analysis/`）
- **音频转录验证**：确认全系列无旁白——旁白全部做成画面字幕
- **BGM 节奏测量**：全部 76–78 BPM
- **色彩/布局测量**：深蓝黑底、字幕带 85–91% 高度、注释带 70%
- **运动密度测量**：相邻帧差异均值 3.97，峰值 34

所有规范数字（字幕字号、留停时长、密度阈值）都来自实测，不是拍脑袋。

## 🙏 致谢与说明

- 本 Skill 的风格规范逆向自抖音「Vibe知识大赏」系列，向原作者 **@Iwanau**、**@Juno**、**叁号暗房 Logos** 致敬——他们的作品证明了"知识可以被拍成大片"。
- 原片由 Claude Opus 5.5 代码生成；制作方法论的公开资料可参考 xilo 的《零基础入门 Opus 5.5 做视频》。
- `docs/original-analysis/` 中的逐秒文字记录仅作风格研究与教学用途，版权归原作者所有；请勿用于二次发布。
- 本仓库不含任何原视频文件！

## 📄 License

[MIT](LICENSE) — 脚本、模板、文档可自由使用；请保留致谢部分。

---

<p align="center">如果这个项目帮到了你，欢迎 Star ⭐ / PR 你的作品到 examples/</p>
