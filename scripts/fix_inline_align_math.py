#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

FENCE_RE = re.compile(r"(```.*?```|~~~.*?~~~)", re.DOTALL)

BEGIN_ALIGN_RE = re.compile(r"\\begin\{align\*?\}")
END_ALIGN_RE = re.compile(r"\\end\{align\*?\}")

WRAPPED_ALIGN_RE = re.compile(
    r"^\s*(?P<prefix>(?:\\[A-Za-z]+\s*)*)"
    r"\\begin\{align\*?\}"
    r"(?P<body>.*?)"
    r"\\end\{align\*?\}\s*$",
    re.DOTALL,
)

def is_escaped(text: str, idx: int) -> bool:
    backslashes = 0
    i = idx - 1
    while i >= 0 and text[i] == "\\":
        backslashes += 1
        i -= 1
    return backslashes % 2 == 1

def find_matching_single_dollar(text: str, start: int) -> int:
    i = start
    while i < len(text):
        if text.startswith("$$", i) and not is_escaped(text, i):
            return -1
        if text[i] == "$" and not is_escaped(text, i):
            if (i + 1 < len(text) and text[i + 1] == "$") or (i - 1 >= 0 and text[i - 1] == "$"):
                i += 1
                continue
            return i
        i += 1
    return -1

def normalize_single_line_expr(expr: str) -> str:
    # 把 align 里常见的对齐符号去掉，尽量变成普通 inline math
    expr = expr.replace("&=", "=")
    expr = expr.replace("&<", "<")
    expr = expr.replace("&>", ">")
    expr = expr.replace("&\\le", "\\le")
    expr = expr.replace("&\\ge", "\\ge")
    expr = expr.replace("&\\leftarrow", "\\leftarrow")
    expr = expr.replace("&\\rightarrow", "\\rightarrow")
    expr = expr.replace("&", "")
    expr = re.sub(r"\s+", " ", expr).strip()
    return expr

def rewrite_inline_align_math(content: str):
    if "\\begin{align" not in content or "\\end{align" not in content:
        return content, False

    stripped = content.strip()
    m = WRAPPED_ALIGN_RE.match(stripped)

    if m:
        prefix = m.group("prefix").strip()
        body = m.group("body")
    else:
        prefix = ""
        body = BEGIN_ALIGN_RE.sub("", content)
        body = END_ALIGN_RE.sub("", body)

    body = body.strip()

    # 真正多行 align：升级成 display math
    if "\\\\" in body:
        display = "$$\n"
        if prefix:
            display += prefix + "\n"
        display += "\\begin{align*}\n" + body + "\n\\end{align*}\n$$"
        return display, True

    # 单行 align：改成 inline math
    expr = normalize_single_line_expr(body)
    if prefix:
        expr = f"{prefix} {expr}".strip()

    return f"${expr}$", True

def process_text(text: str):
    parts = FENCE_RE.split(text)
    changed = False

    for part_idx in range(0, len(parts), 2):
        chunk = parts[part_idx]
        out = []
        i = 0

        while i < len(chunk):
            # 跳过 $$...$$
            if chunk.startswith("$$", i) and not is_escaped(chunk, i):
                j = i + 2
                while j < len(chunk):
                    if chunk.startswith("$$", j) and not is_escaped(chunk, j):
                        break
                    j += 1
                if j < len(chunk):
                    out.append(chunk[i:j+2])
                    i = j + 2
                else:
                    out.append(chunk[i:])
                    i = len(chunk)
                continue

            # 处理 $...$
            if chunk[i] == "$" and not is_escaped(chunk, i):
                if i + 1 < len(chunk) and chunk[i + 1] == "$":
                    out.append("$$")
                    i += 2
                    continue

                j = find_matching_single_dollar(chunk, i + 1)
                if j == -1:
                    out.append(chunk[i])
                    i += 1
                    continue

                original_segment = chunk[i:j+1]
                content = chunk[i + 1:j]

                new_segment, did_change = rewrite_inline_align_math(content)

                if did_change:
                    out.append(new_segment)
                    changed = True
                else:
                    out.append(original_segment)

                i = j + 1
                continue

            out.append(chunk[i])
            i += 1

        parts[part_idx] = "".join(out)

    return "".join(parts), changed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Vault root path, e.g. /Users/xxx/Documents/YEEZUS")
    parser.add_argument("--scope", default="notes", help="Folder under root to process, default: notes")
    parser.add_argument("--apply", action="store_true", help="Actually write changes")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    scope = (root / args.scope).resolve()

    if not scope.exists():
        raise SystemExit(f"Scope not found: {scope}")

    changed_files = []

    for md_file in scope.rglob("*.md"):
        old_text = md_file.read_text(encoding="utf-8")
        new_text, changed = process_text(old_text)

        if changed:
            changed_files.append(md_file)
            if args.apply:
                md_file.write_text(new_text, encoding="utf-8")

    if args.apply:
        print(f"Updated {len(changed_files)} files.")
    else:
        print("Files that would change:")
        for f in changed_files:
            print(f"  {f}")

if __name__ == "__main__":
    main()