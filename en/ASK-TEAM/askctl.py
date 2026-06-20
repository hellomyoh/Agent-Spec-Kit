#!/usr/bin/env python3
"""askctl — ASK-Team coordination tool.

Single-file, dependency-free tool (Python 3.7+). Lives inside the AGENTSPECKIT/ folder.

commands:
  index            Regenerate every directory's INDEX.md from frontmatter (generated, untracked by git).
  detect <WI-id>   Cross-check this workitem's touches against other in-flight workitems.
                   contracts overlap → STOP(exit 2), modules overlap → WARN(exit 1), none → OK(exit 0).
  whoami           Match git config user.email against team/*.md and print handle/role (unregistered → exit 3).

Conventions: CONVENTIONS.md / Schemas: SCHEMAS.md
"""
import os
import sys
import glob
import subprocess

# Stabilize output encoding — force UTF-8 so non-ASCII text/symbols don't crash on Windows consoles (cp949, etc.).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.abspath(__file__))

# Always excluded from scanning
SKIP_NAMES = {"INDEX.md"}
SKIP_DIRS = {"templates", "archive"}


# ----------------------------------------------------------------------------
# Lightweight frontmatter parser (supports only the constrained form in SCHEMAS.md)
# ----------------------------------------------------------------------------
def _strip_quotes(s):
    s = s.strip()
    if len(s) >= 2 and s[0] in "\"'" and s[-1] == s[0]:
        return s[1:-1]
    return s


def _inline_or_scalar(val):
    val = val.strip()
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [_strip_quotes(x) for x in inner.split(",")]
    return _strip_quotes(val)


def parse_frontmatter(path):
    """Parse the leading --- ... --- block of a file into a dict. {} if absent."""
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    block = parts[1]

    data = {}
    cur = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if indent == 0:
            if ":" not in line:
                continue
            key, _, val = line.partition(":")
            key, val = key.strip(), val.strip()
            cur = key
            data[key] = _inline_or_scalar(val) if val else None
        else:
            if cur is None:
                continue
            if line.startswith("- "):
                if not isinstance(data.get(cur), list):
                    data[cur] = []
                data[cur].append(_strip_quotes(line[2:]))
            elif ":" in line:
                sk, _, sv = line.partition(":")
                if not isinstance(data.get(cur), dict):
                    data[cur] = {}
                data[cur][sk.strip()] = _inline_or_scalar(sv) if sv.strip() else []
    return data


# ----------------------------------------------------------------------------
# Common helpers
# ----------------------------------------------------------------------------
def fmt(v):
    if v is None:
        return ""
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    if isinstance(v, dict):
        return "; ".join("%s=%s" % (k, fmt(x)) for k, x in v.items())
    return str(v)


def as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def scan(subdir, pattern, recursive=False):
    """Return files matching pattern under subdir as (path, frontmatter)."""
    base = os.path.join(ROOT, subdir)
    if not os.path.isdir(base):
        return []
    pat = os.path.join(base, "**", pattern) if recursive else os.path.join(base, pattern)
    out = []
    for p in sorted(glob.glob(pat, recursive=recursive)):
        name = os.path.basename(p)
        if name in SKIP_NAMES:
            continue
        rel_parts = os.path.relpath(p, base).split(os.sep)
        if any(part in SKIP_DIRS for part in rel_parts[:-1]):
            continue
        out.append((p, parse_frontmatter(p)))
    return out


def write_index(subdir, title, headers, rows):
    base = os.path.join(ROOT, subdir)
    os.makedirs(base, exist_ok=True)
    lines = ["# %s" % title, "", "> Generated — `askctl.py index` overwrites this. Do not edit by hand.", ""]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        lines.append("| " + " | ".join(fmt(c).replace("|", "\\|") for c in r) + " |")
    lines.append("")
    lines.append("_%d total_" % len(rows))
    with open(os.path.join(base, "INDEX.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ----------------------------------------------------------------------------
# index
# ----------------------------------------------------------------------------
def load_workitems():
    items = []
    for path, fmd in scan("workitems", "WI-*.md"):
        t = fmd.get("touches") or {}
        if not isinstance(t, dict):
            t = {}
        fmd["_contracts"] = as_list(t.get("contracts"))
        fmd["_modules"] = as_list(t.get("modules"))
        fmd["_path"] = path
        items.append(fmd)
    return items


def cmd_index():
    made = []

    wis = load_workitems()
    write_index(
        "workitems", "Workitems Index",
        ["id", "status", "owner", "feature", "contracts", "modules", "branch"],
        [[w.get("id"), w.get("status"), w.get("owner"), w.get("feature"),
          fmt(w["_contracts"]), fmt(w["_modules"]), w.get("branch")] for w in wis],
    )
    made.append(("workitems", len(wis)))

    cfs = [f for _, f in scan("conflicts", "CF-*.md")]
    write_index(
        "conflicts", "Conflicts Index",
        ["id", "status", "kind", "between", "owner"],
        [[c.get("id"), c.get("status"), c.get("kind"), fmt(c.get("between")), c.get("owner")] for c in cfs],
    )
    made.append(("conflicts", len(cfs)))

    teams = [f for _, f in scan("team", "*.md")]
    write_index(
        "team", "Team Index",
        ["handle", "name", "role", "active", "emails"],
        [[t.get("handle"), t.get("name"), t.get("role"), t.get("active"), fmt(t.get("emails"))] for t in teams],
    )
    made.append(("team", len(teams)))

    sess = [f for _, f in scan("sessions", "*--*.md")]
    write_index(
        "sessions", "Sessions Index",
        ["handle", "workitem", "status", "started"],
        [[s.get("handle"), s.get("workitem"), s.get("status"), s.get("started")] for s in sess],
    )
    made.append(("sessions", len(sess)))

    hist = [f for _, f in scan("history", "HIST-*.md", recursive=True)]
    write_index(
        "history", "History Index",
        ["id", "date", "workitem", "title"],
        [[h.get("id"), h.get("date"), h.get("workitem"), h.get("title")] for h in hist],
    )
    made.append(("history", len(hist)))

    asm = [f for _, f in scan("assumptions", "ASM-*.md")]
    write_index(
        "assumptions", "Assumptions Index",
        ["id", "status", "scope", "owner", "related_workitems", "conflicts_with"],
        [[a.get("id"), a.get("status"), a.get("scope"), a.get("owner"),
          fmt(a.get("related_workitems")), fmt(a.get("conflicts_with"))] for a in asm],
    )
    made.append(("assumptions", len(asm)))

    notes = scan("notes", "*.md", recursive=True)
    note_rows = []
    for p, f in notes:
        topic = f.get("topic") or os.path.splitext(os.path.basename(p))[0]
        note_rows.append([topic, os.path.relpath(p, os.path.join(ROOT, "notes"))])
    write_index("notes", "Notes Index", ["topic", "path"], note_rows)
    made.append(("notes", len(note_rows)))

    # SOURCES: merge the original (kind) + meta (status) by id
    srcs = {}
    for p, f in scan("SOURCES", "SRC-*.md"):
        if p.endswith(".meta.md"):
            continue
        sid = f.get("id") or os.path.splitext(os.path.basename(p))[0]
        srcs.setdefault(sid, {})["kind"] = f.get("kind")
    for p, f in scan("SOURCES", "SRC-*.meta.md"):
        sid = f.get("id") or os.path.basename(p).replace(".meta.md", "")
        d = srcs.setdefault(sid, {})
        d["status"] = f.get("status")
        d["triage_owner"] = f.get("triage_owner")
        d["summary"] = f.get("summary")
        d["related_workitems"] = f.get("related_workitems")
    write_index(
        "SOURCES", "Sources Index",
        ["id", "kind", "status", "triage_owner", "summary", "related_workitems"],
        [[sid, d.get("kind"), d.get("status"), d.get("triage_owner"),
          d.get("summary"), fmt(d.get("related_workitems"))] for sid, d in sorted(srcs.items())],
    )
    made.append(("SOURCES", len(srcs)))

    print("index regenerated:")
    for name, n in made:
        print("  %-12s %d items  -> %s/INDEX.md" % (name, n, name))
    return 0


# ----------------------------------------------------------------------------
# detect
# ----------------------------------------------------------------------------
def cmd_detect(wi_id):
    items = load_workitems()
    target = next((w for w in items if w.get("id") == wi_id), None)
    if target is None:
        sys.stderr.write("error: workitem not found: %s\n" % wi_id)
        return 4

    tcon, tmod = set(target["_contracts"]), set(target["_modules"])
    stops, warns = [], []
    for o in items:
        if o.get("id") == wi_id:
            continue
        if o.get("status") not in ("claimed", "in_progress"):
            continue
        c = tcon & set(o["_contracts"])
        m = tmod & set(o["_modules"])
        if c:
            stops.append((o.get("id"), o.get("owner"), sorted(c)))
        elif m:
            warns.append((o.get("id"), o.get("owner"), sorted(m)))

    print("detect %s  (contracts=%s, modules=%s)" % (wi_id, fmt(target["_contracts"]), fmt(target["_modules"])))
    if stops:
        print("\n[STOP] global-contract overlap — maintainer serialization required (CONVENTIONS §6):")
        for wid, owner, keys in stops:
            print("  - %s (owner=%s)  contracts overlap: %s" % (wid, owner, ", ".join(keys)))
    if warns:
        print("\n[WARN] module overlap — register conflicts/CF-*.md + agree on order (CONVENTIONS §5):")
        for wid, owner, keys in warns:
            print("  - %s (owner=%s)  modules overlap: %s" % (wid, owner, ", ".join(keys)))
    if not stops and not warns:
        print("\n[OK] no overlapping in-flight workitem. Safe to proceed.")

    return 2 if stops else (1 if warns else 0)


# ----------------------------------------------------------------------------
# whoami
# ----------------------------------------------------------------------------
def cmd_whoami():
    try:
        email = subprocess.check_output(
            ["git", "config", "user.email"], cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
    except Exception:
        email = ""
    if not email:
        sys.stderr.write("error: git config user.email is not set. Set your git identity first.\n")
        return 3

    for _, f in scan("team", "*.md"):
        emails = [e.lower() for e in as_list(f.get("emails"))]
        if email.lower() in emails:
            print("handle: %s" % f.get("handle"))
            print("name:   %s" % f.get("name"))
            print("role:   %s" % f.get("role"))
            print("email:  %s" % email)
            print("active: %s" % f.get("active"))
            return 0

    sys.stderr.write(
        "error: unregistered git identity (%s). Register in team/<handle>.md before proceeding "
        "(templates/team-TEMPLATE.md).\n" % email
    )
    return 3


# ----------------------------------------------------------------------------
def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 0
    cmd = argv[1]
    if cmd == "index":
        return cmd_index()
    if cmd == "detect":
        if len(argv) < 3:
            sys.stderr.write("usage: askctl.py detect <WI-id>\n")
            return 4
        return cmd_detect(argv[2])
    if cmd == "whoami":
        return cmd_whoami()
    sys.stderr.write("unknown command: %s\n" % cmd)
    print(__doc__)
    return 4


if __name__ == "__main__":
    sys.exit(main(sys.argv))
