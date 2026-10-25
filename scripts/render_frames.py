#!/usr/bin/env python3
"""
render_frames.py — Vibe知识大赏 逐帧渲染器
用法:
  python3 render_frames.py index.html out_frames/ --fps 30 --duration 140 [--scale 1]
原理:
  Playwright 无头浏览器打开 index.html，对每帧调用 window.render(t) 后截图。
  要求页面暴露 window.render(seconds) —— 画面只由 t 决定（纯时间函数）。
可选:
  页面暴露 window.setup(done) 时先等待异步初始化（字体/数据）完成。

v2.0 新增三种"看图改图"模式（详见 references/quality-gate.md）:
  --stills 3.5 18 62     原尺寸截几帧 → outdir/still_3.5s.png …
  --sheet 16             全片均匀 16 帧拼一张总览图 → outdir/sheet.jpg
  --sheet 3.5 18 62      指定时刻拼一张总览图
  --motion 61.5 64       该区间均匀取 12 帧拼一张 → outdir/motion_61.5-64.jpg（看转场）
其余行为与 v1 完全一致，向下兼容。
"""
import argparse, asyncio, os, sys, time

# ---------------- 拼图工具（v2 新增） ----------------

def make_sheet(png_paths, out_path, cols=4, cell_w=480, label=True):
    """把若干 PNG 拼成一张带时刻标签的总览图。"""
    from PIL import Image, ImageDraw
    cell_h = int(cell_w * 1080 / 1920) + (18 if label else 0)
    rows = (len(png_paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (12, 12, 18))
    dr = ImageDraw.Draw(sheet)
    for i, (t, p) in enumerate(png_paths):
        im = Image.open(p).resize((cell_w, int(cell_w * 1080 / 1920)))
        x, y = (i % cols) * cell_w, (i // cols) * cell_h
        sheet.paste(im, (x, y))
        if label:
            dr.text((x + 8, y + int(cell_w * 1080 / 1920) + 3), f"t={t:.2f}s", fill=(240, 210, 140))
    sheet.save(out_path, quality=90)
    return out_path

async def capture_frames(page, outdir, times, fps, prefix="f"):
    """在给定时刻各截一帧，返回 [(t, path), …]。"""
    outs = []
    for t in times:
        await page.evaluate(f"window.render({t})")
        path = os.path.join(outdir, f"{prefix}_{t:.2f}s.png".replace(".", "_", 1))
        await page.screenshot(path=path)
        outs.append((t, path))
    return outs

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html", help="index.html 路径")
    ap.add_argument("outdir", help="帧输出目录")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--duration", type=float, required=True, help="总时长（秒）")
    ap.add_argument("--scale", type=float, default=1.0, help="deviceScaleFactor（2=超采样抗锯齿）")
    ap.add_argument("--preview", type=int, default=0, metavar="N", help="只渲染 N 张均匀分布的静帧（预览模式）")
    # v2.0 看图改图模式
    ap.add_argument("--stills", nargs="+", type=float, metavar="T", default=None,
                    help="原尺寸截指定时刻的帧（秒），如 --stills 3.5 18 62")
    ap.add_argument("--sheet", nargs="+", metavar="T_OR_N", default=None,
                    help="拼总览图：一个整数 N=均匀 N 帧；或若干秒时刻，如 --sheet 3.5 18 62")
    ap.add_argument("--motion", nargs=2, type=float, metavar=("A", "B"), default=None,
                    help="取 [A,B] 秒区间均匀 12 帧拼图，检查转场，如 --motion 61.5 64")
    args = ap.parse_args()

    from playwright.async_api import async_playwright

    os.makedirs(args.outdir, exist_ok=True)
    html_path = os.path.abspath(args.html)

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--force-color-profile=srgb", "--disable-lcd-text"])
        page = await browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=args.scale)
        page.on("pageerror", lambda e: print(f"[页面JS错误] {e}", file=sys.stderr))
        await page.goto(f"file://{html_path}")
        # 等字体
        try:
            await page.evaluate("document.fonts.ready.then(()=>true)")
        except Exception:
            pass
        # 异步初始化钩子
        has_setup = await page.evaluate("typeof window.setup === 'function'")
        if has_setup:
            await page.evaluate("new Promise(res => { window.__setupDone = res; window.setup(res); })")
        # 校验 render(t)
        has_render = await page.evaluate("typeof window.render === 'function'")
        if not has_render:
            print("[致命] 页面未暴露 window.render(t) —— 请检查 index.html", file=sys.stderr)
            sys.exit(2)
        # 接管渲染模式：停掉页面自带的预览 rAF 循环（若模板遵守约定）
        await page.evaluate("window.__RENDER_MODE__ = true")

        # -------- v2.0 看图改图模式 --------
        if args.stills or args.sheet or args.motion:
            if args.stills:
                got = await capture_frames(page, args.outdir, args.stills, args.fps, prefix="still")
                for t, path in got:
                    print(f"  静帧 t={t}s → {path}")
            if args.sheet:
                spec = args.sheet
                if len(spec) == 1 and "." not in spec[0]:
                    n = max(2, int(spec[0]))
                    times = [i * (args.duration - 0.01) / (n - 1) for i in range(n)]
                else:
                    times = [float(x) for x in spec]
                got = await capture_frames(page, args.outdir, times, args.fps, prefix="sheetf")
                out = make_sheet(got, os.path.join(args.outdir, "sheet.jpg"))
                for _, pth in got: os.remove(pth)
                print(f"完成：总览图 → {out}")
            if args.motion:
                a, b = sorted(args.motion)
                times = [a + (b - a) * i / 11 for i in range(12)]
                got = await capture_frames(page, args.outdir, times, args.fps, prefix="motionf")
                out = os.path.join(args.outdir, f"motion_{a:.2f}-{b:.2f}.jpg".replace(".", "_", 1))
                make_sheet(got, out)
                for _, pth in got: os.remove(pth)
                print(f"完成：转场拼图 → {out}")
            await browser.close()
            return

        # -------- 原有全量/预览渲染（v1 行为不变） --------
        total = int(args.duration * args.fps)
        if args.preview > 0:
            idxs = [int(i * (total - 1) / (args.preview - 1)) for i in range(args.preview)] if args.preview > 1 else [0]
        else:
            idxs = range(total)

        t0 = time.time()
        n_done = 0
        n_total = len(idxs) if not isinstance(idxs, range) else total
        for fi in idxs:
            t = fi / args.fps
            await page.evaluate(f"window.render({t})")
            await page.screenshot(path=os.path.join(args.outdir, f"f{fi:06d}.png"))
            n_done += 1
            if n_done % 150 == 0 or n_done == n_total:
                el = time.time() - t0
                print(f"  已渲染 {n_done}/{n_total} 帧  ({el:.0f}s)", flush=True)
        await browser.close()
        print(f"完成：{n_done} 帧 → {args.outdir}")

if __name__ == "__main__":
    asyncio.run(main())
