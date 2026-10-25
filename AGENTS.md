# AGENTS.md — vibe-knowledge-video 通用 Agent 指令

> 本文件是给 AI 编程助手（OpenAI Codex / Gemini CLI / Jules / Cursor / Trae 等）看的入口指令。
> 这些工具会自动读取仓库根目录的 `AGENTS.md` 并遵守其中约定。

## 你现在拿到了什么

这是一个**视频制作技能仓库**：把数学/概率/哲学等硬知识拍成「Vibe知识大赏」风格的电影感知识短视频（1920×1080、2:00–2:45、无配音、双语字幕、纯代码生成）。

## 收到视频制作请求时，你必须这样做

1. **先完整阅读 `SKILL.md`**——它是七步工作流的总纲（选题核实→剧本→分镜→用户确认→代码实现→渲染合成→自检交付），逐步执行，不可跳步。
2. 需要风格细节时读 `references/`：
   - `references/visualization-design.md` — **（先读）讲解设计**：配图与讲解的分界、概念→形象的提问法、六种呈现动作、约 1/5 句子不配画面
   - `references/copywriting-rules.md` — 字幕稿文体：句量句长、句式工具箱、禁用清单、强调的克制规则
   - `references/structure-bible.md` — 选题打分、三种骨架、十条叙事定律、悬念/反转/读数/回扣的设计
   - `references/visual-grammar.md` — 常见句型→演法对照表、十种转场手法、动效手感（写分镜时随手查）
   - `references/beat-scaffold.md` — 逐拍写法骨架：标准片 ~44 个功能位置与写法公式（严格模式照表填）
   - `references/image-prompts.md` — 出图提示词规范（可选环节：风格后缀、六条规则、典型清单）
   - `references/quality-gate.md` — 人工看图改图毛病表、两轮修复流程、终检门槛、数字纪律
   - `references/render-craft.md` — render(t) 工程纪律：固定种子、模拟查表、辉光管线、对数推拉、常见装置写法
   - `references/rework-scripts.md` — 分步推进的八轮提示词 + 按毛病直说的返工话术
   - `references/alternate-worlds.md` — 建立第二套视觉世界的方法与节奏经验值
   - `references/style-guide.md` — 布局坐标、配色、动效规格、视觉母题库
   - `references/narrative-templates.md` — 六段式叙事弧模板 + 8 条原片逐段拆解
   - `references/prompt-brief.md` — 创作简报（Brief）填空模板
   - `docs/common-mistakes.md` — 常见错误对照表（报错/翻车先查这里）
   - `docs/publish-guide.md` — 发布前检查清单与数据复盘
   - `docs/topic-seeds.md` — 选题方向、种子题与四关检验
   - `docs/strict-mode.md` — 中等及以下模型用：逐关完成的严格模式与降级方案
3. 写代码前**必须让用户确认剧本和分镜**（第 4 步），不要自作主张直接开做。
4. 页面模板从 `assets/template.html` 起改，不要从零造轮子。
5. **（v2.0）数字纪律**：屏上每个数字先由代码算出或查证记入 NOTES.md，禁止先写数再倒推；模拟用固定种子，同一帧渲染两遍结果必须一致；模拟/示意内容在画面上标注。
6. **（v2.0）交付前的人工质检**：用 `render_frames.py` 的 `--sheet` / `--stills` / `--motion` 看图，按 `quality-gate.md` 毛病表逐条查，至少修两轮；`qa_check.py` 通过 ≠ 可以交片。
7. **（v2.4）预览先行**：页面能跑的第一时间起预览给用户看，边写边纠偏，不要闷头做完再给。
8. **（v2.4）保留用户手工改动**：发现代码在会话之外被用户改过时，不要覆盖——视为有意修改，或先询问。
9. **（v2.4）Remotion 路线**：用户要求用 Remotion 实现时，读 `references/remotion-track.md`（方法论不变，工程对照与流程在那里）；渲染命令换成 `npx remotion render / still / --frames`。

## 环境准备（渲染合成前执行一次）

```bash
# Python 依赖
pip install playwright pillow numpy

# 无头浏览器
playwright install chromium

# ffmpeg（视频合成必需，需含 H.264 编码器）
# Ubuntu/Debian: apt install -y ffmpeg
# macOS: brew install ffmpeg
# Windows: winget install ffmpeg

# 可选：QA 字幕 OCR 校验
# apt install -y tesseract-ocr tesseract-ocr-chi-sim
ffmpeg -version  # 验证可用
```

## 不可违反的技术契约

- `index.html` 必须暴露 **`window.render(t)`**：给定秒数 t 画出该帧；画面只由 t 决定（固定随机种子、无计时器、无帧间状态）。这是逐帧渲染器 `scripts/render_frames.py` 的调用契约。
- 渲染器会设置 `window.__RENDER_MODE__ = true` 接管渲染循环——页面自己的 requestAnimationFrame 预览循环检测到该标志后必须停止，否则预览循环会用墙上时钟覆盖 render(t) 的画面状态。
- 字体加载完成再截图（`document.fonts.ready`）。
- Canvas 文字手动换行，禁止依赖浏览器自动换行。

## 渲染合成命令（第 6 步）

```bash
python3 scripts/render_frames.py index.html out_frames/ --fps 30 --duration 130
python3 scripts/synth_bgm.py bgm.wav --bpm 77 --duration 130 \
  --sections "0,8,pad;8,30,piano;30,90,full;90,105,arp;105,120,piano;120,130,outro"
bash scripts/build_video.sh out_frames/ bgm.wav final.mp4
python3 scripts/qa_check.py final.mp4   # 六维自检，任何一项 < 8 分须修复重渲
```

看图改图命令（v2.0，第 7 步人工质检用，详见 `references/quality-gate.md`）：

```bash
python3 scripts/render_frames.py index.html review/ --duration 130 --sheet 16      # 全片均匀 16 帧总览图
python3 scripts/render_frames.py index.html review/ --duration 130 --sheet 3.5 18 62  # 指定时刻总览图
python3 scripts/render_frames.py index.html review/ --duration 130 --stills 18.3 62.4 # 原尺寸静帧
python3 scripts/render_frames.py index.html review/ --duration 130 --motion 61.5 64   # 转场区间 12 帧拼图
```

## 能力边界（对用户诚实）

- 若当前环境**无法安装依赖或执行 shell**（如纯对话型网页 AI）：只完成第 1–5 步（剧本/分镜/index.html 代码），并把上面两条命令块原样交给用户，请其在本地终端执行第 6–7 步。
- 所有事实（年份/人名/论文名/数字）须联网核实，没把握的不写。

## 语言

与用户交流用中文；代码注释用中文；成片字幕为中文主句 + 英文斜体对照（风格 DNA 要求，见 `references/style-guide.md`）。
