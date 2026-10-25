# Remotion 路线：把本方法论跑在 Remotion 里

> 本仓库默认路线是 **Canvas + `window.render(t)`**；本文档面向想改用 **Remotion**（React 时间线视频框架）的人。方法论——讲解设计、字幕稿、结构、质量门——**与渲染技术无关，全部照用**；要换的只是第 5–6 步的工程实现。本文用原创表述整理 Remotion 路线的做法（技术事实参考其公开文档）。

## 1. 什么时候选 Remotion 路线

| 需求 | 选 |
|---|---|
| 纯代码动画直出、零依赖、渲染管线最轻 | Canvas 默认路线 |
| 要剪辑真实视频/音频素材、逐字对轴 | **Remotion** |
| 要复杂文字排版、自动测量/适配文本 | **Remotion**（自带文本测量与适配工具） |
| 要参数化模板（改几个字段就出一期新片） | **Remotion**（schema 参数化 + Studio 内改） |
| 要浏览器里实时预览、边看边改 | 两者都可以（Canvas 用 `--serve`，Remotion 用 Studio） |

## 2. 心智模型对照表

两个路线的本质是同一条铁律：**画面 = 时间 t 的纯函数**。差异只在表达方式：

| 本仓库 Canvas 契约 | Remotion 对应物 |
|---|---|
| `window.render(t)`，t 是秒 | `useCurrentFrame()` 拿帧号；`useVideoConfig().fps` 换算秒——**永远用 fps 换算，不许写死 30** |
| `seg/ss(t,a,b)` + 缓动 | `interpolate(frame,[a*fps,b*fps],[0,1],{extrapolateLeft/Right:"clamp",easing})`——**两端必须 clamp**，等价于我们的 seg 夹取 |
| 自带缓动库 E.out3/spring | `Easing.bezier(...)` / `Easing.spring({damping})`；缩放动画加 `output:"perceptual-scale"`（否则大尺寸时感知速度不均） |
| `fade(t,a,b,fin,fout)` 包络 | `Sequence` 的 `from` + 淡入淡出插值；相邻场景衔接用 `TransitionSeries`（转场时长会**缩短**总时长，编排时要计入） |
| 一站一个函数 | 一个场景一个组件；多场景视频给每个"站"独立组件，父层把每站的 props 和时刻**内联写清** |
| 固定种子 `rng(seed)` | 同样禁止 `Math.random()`；用带种子的发生器（如 mulberry32）放在模块顶层 |
| 禁计时器/禁帧间状态 | **CSS `transition` / `animation` / Tailwind 动画类一律禁用**——它们不随帧渲染，输出会错；一切动效都由帧号驱动 |
| 字幕永远最后画 | 字幕做成顶层组件压在最上；全片常驻层（水印/角标）同理 |
| `document.fonts.ready` 坑 | 用官方字体包加载（类型安全且**阻塞到字体就绪**才出帧），从根上消掉我们踩过的"前几帧回退字体"坑 |

## 3. Remotion 路线的跑片流程（对应七步）

1–4 步（选题、剧本、分镜、确认）与本仓库完全一致；密度体检 `check_density.py` 照用。

**第 5 步·代码实现**：
- 脚手架：`npx create-video@latest --yes --blank` 建空模板，装依赖。
- **预览先行**：项目能跑的第一时间启动 Studio（`npx remotion studio`，Agent 环境加 `--no-open` 然后打开它打印的本地网址），**边写边让用户看着改**——这条和 Canvas 路线的 `--serve` 预览是同一个纪律，但 Remotion 的热更新预览更好用。
- 结构：每个"站"一个组件；相邻站用 `TransitionSeries.Sequence` + 转场（fade/slide/wipe，或自写 presentation）；时间上各自独立的元素用 `Track` / `from`。
- 时长动态化：拍数由 script 数据驱动时，用 `calculateMetadata` 从 props 算总时长，不手写死。
- 文本：标题/字幕的最长行用文本测量工具量宽、必要时自动缩字号适配容器——把我们"定稿前量最长字幕"的手工规则变成代码保证。
- 装包用 `npx remotion add 包名`，版本自动匹配。

**第 6 步·渲染合成**：
- 抽查帧：`npx remotion render <合成ID> out/ --frames=0,30,90 --image-format=png`——等价于我们渲染器的 `--stills`。
- 全片：`npx remotion render <合成ID> out/片.mp4`。
- 音频：BGM 与音效作为 `<Audio>` 层写进合成（`from` 定起点、`volume` 做包络），响度归一仍在最后一条 ffmpeg 命令做，或交给平台曲库。

**第 7 步·自检**：`qa_check.py` 照用（它只看成片文件）；看图改图用 Studio 预览 + 抽帧。

## 4. 参数化：一次搭台，期期复用

Remotion 路线最大的长线收益是**模板化**：把分镜表做成 Zod schema（每拍的字幕、染色词、年代戳、画面类型），合成注册 defaultProps。以后做新一期，改一份 JSON 就能在 Studio 里预览成片——这正是"同一套版式换内容"的工程化形态。建议按本仓库的教学样例思路搭一个 `template` 合成，之后每期只改数据。

## 5. 与质量门的对接

- 三问、六种呈现动作、1/5 不画、颜色词汇、密度红线：**原样执行**，与渲染器无关。
- 看图改图的毛病表：Remotion 路线同样适用（主体大小、字幕带侵入、转场清晰度），工具换成 Studio 预览 + 抽帧。
- 数字纪律：模拟依然放纯函数模块、固定种子、载入算完查表——在 React 里就是"模块顶层算好，组件里只查表"，**不许**在组件体内跑模拟。

## 6. 版权与致谢

本文档为原创撰写；Remotion 相关 API 名称与行为属公开技术事实，学习时以其官方开源文档为准。使用 Remotion 注意其官方授权条款（公司规模超过一定范围渲染需商业授权，具体以其官网说明为准）。
