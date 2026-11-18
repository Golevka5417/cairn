#!/usr/bin/env python3
"""脱敏扫描：查仓库里有没有不该公开的东西。

用法：
    python3 scripts/scan.py            扫描全部已跟踪 + 未跟踪的文本文件
    python3 scripts/scan.py --staged   只扫暂存区（提交前钩子用）

额外的私有敏感词清单（公司名、真实姓名、编号等）不放在本仓库。
设置环境变量 CAIRN_DENYLIST 指向它，或放在 ~/gavin-playbook/public-denylist.txt，
读得到就一起查；一行一个词，# 开头是注释。
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_FILES = {"LICENSE", "scripts/scan.py"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip"}

PATTERNS = [
    ("IP 地址", r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"),
    ("邮箱", r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    ("手机号", r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    ("身份证号", r"(?<!\d)\d{17}[\dXx](?!\d)"),
    ("9 位以上长数字（订单号 / App 编号）", r"(?<![\d.])\d{9,}(?![\d.])"),
    ("备案号", r"[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼]ICP备\d{6,}"),
    ("公安备案号", r"公网安备\s*\d{6,}"),
    ("Team ID / 密钥 ID 形状", r"(?<![A-Za-z0-9])(?=[A-Z0-9]*\d)(?=[A-Z0-9]*[A-Z])[A-Z0-9]{10}(?![A-Za-z0-9])"),
    ("私钥", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("本机路径", r"/Users/[^/\s]+|~/(?:Documents|Desktop|Projects|Obsidian)"),
]
ALLOW = {"1206×2622", "1179×2556"}


def files(staged):
    if staged:
        cmd = ["git", "diff", "--cached", "--name-only", "-z", "--diff-filter=ACM"]
    else:
        cmd = ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"]
    out = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True).stdout
    for f in filter(None, out.split("\0")):
        if f in SKIP_FILES or os.path.splitext(f)[1].lower() in SKIP_EXT:
            continue
        yield f


def denylist():
    path = os.environ.get("CAIRN_DENYLIST") or os.path.expanduser("~/gavin-playbook/public-denylist.txt")
    if not os.path.exists(path):
        return []
    words = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#"):
            words.append(line)
    return words


def main():
    staged = "--staged" in sys.argv
    words = denylist()
    hits = 0
    for f in files(staged):
        try:
            text = open(os.path.join(ROOT, f), encoding="utf-8").read()
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for name, pat in PATTERNS:
                for m in re.finditer(pat, line):
                    if m.group(0) in ALLOW:
                        continue
                    hits += 1
                    print(f"{f}:{n}  [{name}]  {m.group(0)}")
            low = line.lower()
            for w in words:
                if w.lower() in low:
                    hits += 1
                    print(f"{f}:{n}  [私有敏感词]  {w}")
    note = f"（私有敏感词 {len(words)} 个）" if words else "（没找到私有敏感词清单，只查了通用规则）"
    if hits:
        print(f"\n✗ 发现 {hits} 处疑似敏感信息 {note}")
        sys.exit(1)
    print(f"✓ 没发现敏感信息 {note}")


if __name__ == "__main__":
    main()
