# Queued edits

Each `*.edit` file here is one small change to existing upstream files. The
`myclient-apply-edits` workflow applies the files in name order, commits each
one as its own commit (the edit file is removed in the same commit), pushes,
and then runs the debug build.

Why: this fork is edited through the GitHub API, which replaces whole files.
Some upstream files are too large to rewrite safely that way. Anchored edits
keep the diff small and exact.

## Format

    <commit message: subject line, blank line, body>
    >>> <op> <path> [count=N]
    >>> find
    <anchor text>
    >>> text
    <whole lines to insert, or the replacement lines>

| Op | Effect |
|---|---|
| `insert_before_line` | Inserts `text` before the line where the anchor starts. |
| `insert_after_line` | Inserts `text` after the line where the anchor ends. |
| `replace_line` | Replaces the whole line(s) that the anchor spans with `text`. |
| `replace` | Replaces only the matched span with the `replace` section. |
| `create` | Creates a new file from `text` (no `find` section). Fails if the file exists. |
| `overwrite` | Replaces the whole content of an existing file with `text`. |

Anchor rules:

- Whitespace between tokens does not matter. Every other character must match (case-sensitive).
- A token that starts or ends with a letter, digit, `_` or `$` does not match inside a longer identifier.
- An anchor must match exactly once, or exactly `count` times.
- Section text is used verbatim, so `text` must carry its own indentation.
- If any edit in a file fails, that file changes nothing and the workflow fails.
