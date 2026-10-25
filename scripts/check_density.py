#!/usr/bin/env python3
"""
check_density.py — 字幕稿知识密度检查（写完字幕稿就跑，不过不改）
用法:
  python3 check_density.py subtitles.txt [--duration 120] [--min-cps 7.5] [--max-len 20]

输入格式: 每行一句字幕（中文主句）；# 开头为注释；空行忽略。
可选在行尾用 |123 标注该句的"屏上小字"字符数（不计入正文）。

检查项（来自参考片实测 + 爆款数据规律）:
  1. 信息量: 每秒 ≥ min-cps 个字（低于 = 观众觉得"讲得太少"）
  2. 句速:   每分钟 ≥ 18 句（低于 = 节奏拖）
  3. 句长:   每句 ≤ max-len 字（超长列出来拆）
  4. 填充词: 口播腔命中即列出（出现即删）
  5. 重复度: 相邻两句重复字占比过高（车轱辘话）列出来
输出: 诊断报告 + 是否达标（exit 0/1）
"""
import argparse, re, sys

FILLERS = ["今天我们来聊", "这告诉我们", "综上", "众所周知", "值得一提", "让我们一起",
           "我们不难发现", "说白了就是", "其实呢", "那么接下来", "首先", "其次", "最后总结"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script", help="字幕稿文本（每行一句）")
    ap.add_argument("--duration", type=float, required=True, help="成片目标时长（秒）")
    ap.add_argument("--genre", choices=["film", "dense"], default="film",
                    help="film=电影感稀疏字幕(参考片实测 7-15 句/分)；dense=高密度解说(20-25 句/分)")
    ap.add_argument("--min-cps", type=float, default=None, help="每秒最少字数（默认按体裁）")
    ap.add_argument("--min-lpm", type=float, default=None, help="每分钟最少句数（默认按体裁）")
    ap.add_argument("--max-len", type=int, default=None, help="单句最长字数（默认按体裁）")
    args = ap.parse_args()
    if args.genre == "dense":
        args.min_cps = args.min_cps or 7.0; args.min_lpm = args.min_lpm or 20; args.max_len = args.max_len or 20
    else:
        args.min_cps = args.min_cps or 2.6; args.min_lpm = args.min_lpm or 11; args.max_len = args.max_len or 28

    lines = []
    for ln in open(args.script, encoding="utf-8"):
        ln = re.sub(r"[「」]", "", ln).strip()
        if not ln or ln.startswith("#"): continue
        lines.append(ln)
    if not lines:
        print("没有读到任何字幕行"); sys.exit(1)

    total = sum(len(l) for l in lines)
    cps = total / args.duration
    lpm = len(lines) / args.duration * 60
    issues = []

    print(f"句数 {len(lines)}  总字数 {total}  字/秒 {cps:.2f}  句/分 {lpm:.1f}  均句长 {total/len(lines):.1f}")
    if cps < args.min_cps:
        issues.append(f"[密度] 每秒只有 {cps:.2f} 字（目标 ≥ {args.min_cps}）——信息量不足，删掉氛围句，把过渡并进下一句，或增加事实/数字句")
    if lpm < args.min_lpm:
        issues.append(f"[节奏] 每分钟只有 {lpm:.1f} 句（目标 ≥ {args.min_lpm}）")

    longs = [(i + 1, l) for i, l in enumerate(lines) if len(l) > args.max_len]
    if longs:
        issues.append(f"[句长] {len(longs)} 句超过 {args.max_len} 字，拆成两句、各给一个屏上动作：")
        for i, l in longs[:8]: issues.append(f"   第{i}句({len(l)}字): {l}")

    hits = [(i + 1, l) for i, l in enumerate(lines) if any(f in l for f in FILLERS)]
    if hits:
        issues.append(f"[口播腔] {len(hits)} 句命中填充词，出现即删：")
        for i, l in hits[:8]: issues.append(f"   第{i}句: {l}")

    dup = []
    for i in range(len(lines) - 1):
        a, b = set(lines[i]), set(lines[i + 1])
        if len(a) and len(b) and len(a & b) / max(4, min(len(a), len(b))) > 0.8:
            dup.append((i + 1, i + 2))
    if dup:
        issues.append(f"[车轱辘话] 相邻句重复度过高: {dup[:6]}——合并或让下一句推进论点")

    print()
    if issues:
        print("=" * 52)
        for m in issues: print(m)
        sys.exit(1)
    print("密度与文体检查全部通过 ✓")

if __name__ == "__main__":
    main()
