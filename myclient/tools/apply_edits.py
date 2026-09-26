#!/usr/bin/env python3
# Unofficial client (myclient) tooling. Not part of upstream Telegram for Android.
"""Apply queued anchored edits and commit each edit file as its own commit.

This fork is edited remotely through the GitHub API, which can only replace
whole files. Several upstream files are too large for that (ProfileActivity.java
has more than 17,000 lines). Each file in myclient/edits/ describes one small
change. CI applies it with exact text anchors and commits the result, so the
git history shows a normal, reviewable diff. The format is described in
myclient/edits/README.md.

Outputs for GitHub Actions: applied=true|false, failed=true|false.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

EDITS_DIR = Path("myclient/edits")
MARKER = ">>> "
OPS = ("insert_before_line", "insert_after_line", "replace_line", "replace", "create")
SECTIONS = ("find", "text", "replace")
WORD_CHAR = "[A-Za-z0-9_$]"


class EditError(Exception):
    pass


def read_text(path):
    with open(path, encoding="utf-8", newline="") as handle:
        return handle.read()


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(content)


def git(*args):
    subprocess.run(["git"] + list(args), check=True)


def parse_edit_file(path):
    """Return (commit message, list of edits) for one .edit file."""
    lines = read_text(path).replace("\r\n", "\n").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    message_lines = []
    edits = []
    state = {"edit": None, "section": None, "buffer": []}

    def close_section():
        if state["edit"] is not None and state["section"] is not None:
            buffer = state["buffer"]
            state["edit"][state["section"]] = "\n".join(buffer) + ("\n" if buffer else "")
        state["section"] = None
        state["buffer"] = []

    for line in lines:
        if line.startswith(MARKER):
            words = line[len(MARKER):].split()
            if len(words) == 1 and words[0] in SECTIONS:
                if state["edit"] is None:
                    raise EditError("section '%s' comes before any edit header" % words[0])
                close_section()
                state["section"] = words[0]
                continue
            if len(words) < 2 or words[0] not in OPS:
                raise EditError("bad marker line: %r" % line)
            close_section()
            edit = {"op": words[0], "file": words[1]}
            for option in words[2:]:
                if option.startswith("count="):
                    edit["count"] = int(option[len("count="):])
                else:
                    raise EditError("unknown option %r in %r" % (option, line))
            edits.append(edit)
            state["edit"] = edit
        elif state["edit"] is None:
            message_lines.append(line)
        elif state["section"] is None:
            if line.strip():
                raise EditError("text outside a section: %r" % line)
        else:
            state["buffer"].append(line)
    close_section()
    return "\n".join(message_lines).strip(), edits


def build_pattern(find):
    """Whitespace-insensitive, identifier-safe pattern for an anchor."""
    tokens = find.split()
    if not tokens:
        raise EditError("empty anchor")
    parts = []
    for token in tokens:
        part = re.escape(token)
        if re.match(WORD_CHAR, token[0]):
            part = "(?<!" + WORD_CHAR + ")" + part
        if re.match(WORD_CHAR, token[-1]):
            part += "(?!" + WORD_CHAR + ")"
        parts.append(part)
    return re.compile(r"\s+".join(parts))


def as_block(text, newline):
    if not text.endswith("\n"):
        text += "\n"
    return text.replace("\n", newline)


def apply_edit(content, edit, newline):
    op = edit["op"]
    if "find" not in edit:
        raise EditError("missing 'find' section")
    matches = list(build_pattern(edit["find"]).finditer(content))
    expected = edit.get("count", 1)
    if len(matches) != expected:
        raise EditError("anchor matched %d time(s), expected %d: %r"
                        % (len(matches), expected, edit["find"].strip()[:200]))
    for match in reversed(matches):
        start = content.rfind("\n", 0, match.start()) + 1
        newline_at = content.find("\n", match.end())
        end = len(content) if newline_at == -1 else newline_at + 1
        if op == "replace":
            if "replace" not in edit:
                raise EditError("missing 'replace' section")
            replacement = edit["replace"].strip().replace("\n", newline)
            content = content[:match.start()] + replacement + content[match.end():]
            continue
        if "text" not in edit:
            raise EditError("missing 'text' section")
        block = as_block(edit["text"], newline)
        if op == "insert_before_line":
            content = content[:start] + block + content[start:]
        elif op == "insert_after_line":
            if end == len(content) and not content.endswith("\n"):
                block = newline + block
            content = content[:end] + block + content[end:]
        elif op == "replace_line":
            content = content[:start] + block + content[end:]
        else:
            raise EditError("unknown op %r" % op)
    return content


def process(edit_file):
    message, edits = parse_edit_file(edit_file)
    if not message:
        raise EditError("missing commit message")
    if not edits:
        raise EditError("no edits")
    contents = {}
    newlines = {}
    for number, edit in enumerate(edits, 1):
        path = edit["file"]
        try:
            if edit["op"] == "create":
                if path in contents or Path(path).exists():
                    raise EditError("file already exists")
                if "text" not in edit:
                    raise EditError("missing 'text' section")
                contents[path] = edit["text"]
                newlines[path] = "\n"
                continue
            if path not in contents:
                if not Path(path).is_file():
                    raise EditError("file not found")
                contents[path] = read_text(path)
                newlines[path] = "\r\n" if "\r\n" in contents[path] else "\n"
            contents[path] = apply_edit(contents[path], edit, newlines[path])
        except EditError as error:
            raise EditError("edit %d (%s %s): %s" % (number, edit["op"], path, error))
    for path, content in contents.items():
        write_text(Path(path), content)
        git("add", "--", path)
    git("rm", "-q", "--", str(edit_file))
    git("commit", "-q", "-m", message)
    print("Applied %s: %d edit(s) in %d file(s)." % (edit_file.name, len(edits), len(contents)))


def set_output(name, value):
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write("%s=%s\n" % (name, value))


def main():
    edit_files = sorted(EDITS_DIR.glob("*.edit"))
    if not edit_files:
        print("No queued edits.")
    applied = 0
    failed = False
    for edit_file in edit_files:
        try:
            process(edit_file)
            applied += 1
        except (EditError, OSError, ValueError, subprocess.CalledProcessError) as error:
            print("::error::%s: %s" % (edit_file.name, error))
            failed = True
            break
    set_output("applied", "true" if applied else "false")
    set_output("failed", "true" if failed else "false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
