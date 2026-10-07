#!/usr/bin/env python3
"""Refresh data/index.json and docs/4-reference_index.md from GitHub, with no model calls.

Cost per run is GitHub API calls only: one listing per owner (a 304 when nothing changed), one tree
per repo pushed since the last run, one blob per new or changed SKILL.md. A git blob sha is a hash
of the content, so "same as upstream" and "changed since review" are sha comparisons.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from base64 import b64decode, b64encode
from datetime import date, timedelta
from fnmatch import fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com"
SKILL_GLOBS = ("SKILL.md", "*/SKILL.md")
AGENT_GLOBS = (".claude/agents/*.md", "plugins/*/agents/*.md")
SKIP_DIRS = ("node_modules/", ".devkit/", "vendor/", "test/", "tests/", "fixtures/")


def kind_of(path):
    if any(f"/{d}" in f"/{path}" for d in SKIP_DIRS):
        return None
    if any(fnmatch(path, g) for g in SKILL_GLOBS):
        return "skill"
    if any(fnmatch(path, g) for g in AGENT_GLOBS):
        return "agent"
    return None


def front_matter(text, path):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    name = re.search(r"^name:\s*['\"]?([^'\"\n]+)", fm, re.M)
    # A folded or quoted description spans lines until the next top-level key.
    desc = re.search(r"^description:\s*[>|]?-?\s*(.*?)(?=^\S+:|\Z)", fm, re.M | re.S)
    fallback = path.rsplit("/", 2)[-2] if path.endswith("SKILL.md") else Path(path).stem
    text = " ".join(desc.group(1).split()).strip("'\"") if desc else ""
    return (name.group(1).strip() if name else fallback), text[:200]


class GitHub:
    def __init__(self, token, etags):
        self.token, self.etags, self.calls = token, etags, 0

    def get(self, url, etag_key=None):
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        if etag_key and etag_key in self.etags:
            req.add_header("If-None-Match", self.etags[etag_key])
        self.calls += 1
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                if etag_key and r.headers.get("ETag"):
                    self.etags[etag_key] = r.headers["ETag"]
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 304:
                return None
            if e.code in (404, 409):  # gone, or an empty repo
                return {}
            raise


def list_repos(gh, owner, listings):
    """Public, non-fork, non-archived repos of a user or an org; a 304 page reuses its last copy."""
    repos, page = [], 1
    while True:
        key = f"{owner}:{page}"
        batch = gh.get(f"{API}/users/{owner}/repos?per_page=100&page={page}", f"list:{key}")
        if batch is None:
            batch = listings.get(key, {"raw": 0, "repos": []})
        else:
            batch = {
                "raw": len(batch),
                "repos": [
                    {
                        "repo": r["full_name"],
                        "branch": r["default_branch"],
                        "pushed_at": r["pushed_at"],
                    }
                    for r in batch
                    if not r["fork"] and not r["archived"]
                ],
            }
        listings[key] = batch
        repos += batch["repos"]
        if batch["raw"] < 100:
            return repos
        page += 1


def one_repo(gh, full):
    r = gh.get(f"{API}/repos/{full}", f"repo:{full}")
    if r is None or not r:
        return r
    return {"repo": r["full_name"], "branch": r["default_branch"], "pushed_at": r["pushed_at"]}


def scan_repo(gh, repo, old_skills):
    tree = gh.get(f"{API}/repos/{repo['repo']}/git/trees/{repo['branch']}?recursive=1") or {}
    if tree.get("truncated"):
        print(
            f"warning: {repo['repo']} tree truncated, some skills may be missing", file=sys.stderr
        )
    found = {}
    for node in tree.get("tree", []):
        kind = node["type"] == "blob" and kind_of(node["path"])
        if not kind:
            continue
        key = f"{repo['repo']}:{node['path']}"
        prev = old_skills.get(key)
        if prev and prev["blob"] == node["sha"]:
            found[key] = prev
            continue
        blob = gh.get(f"{API}/repos/{repo['repo']}/git/blobs/{node['sha']}") or {}
        text = b64decode(blob.get("content", "")).decode("utf-8", "replace")
        name, desc = front_matter(text, node["path"])
        found[key] = {
            "repo": repo["repo"],
            "path": node["path"],
            "kind": kind,
            "name": name,
            "description": desc,
            "blob": node["sha"],
            "first_seen": prev["first_seen"] if prev else str(date.today()),
            "changed": str(date.today()),
        }
    return found


def refresh(gh, sources, state):
    old_repos, old_skills = state.get("repos", {}), state.get("skills", {})
    listings, repos = dict(state.get("listings", {})), {}
    for group in ("own", "watch"):
        for entry in sources[group]:
            if "/" in entry:
                r = one_repo(gh, entry)
                r = old_repos.get(entry) if r is None else r
                listed = [r] if r else []
            else:
                listed = list_repos(gh, entry, listings)
            for r in listed:
                repos[r["repo"]] = {**r, "group": group, "owner": entry.split("/")[0]}
    skills = {}
    for full, repo in sorted(repos.items()):
        mine = {k: v for k, v in old_skills.items() if v["repo"] == full}
        prev = old_repos.get(full)
        if prev and prev["pushed_at"] == repo["pushed_at"] and prev["branch"] == repo["branch"]:
            skills.update(mine)  # not pushed since last run: no tree call
        else:
            skills.update(scan_repo(gh, repo, mine))
    for s in skills.values():
        s["group"] = repos[s["repo"]]["group"]
    return {"repos": repos, "skills": skills, "etags": gh.etags, "listings": listings}


def annotate(index, tags, reviewed):
    by_name = {}
    for s in index["skills"].values():
        if s["group"] == "watch":
            by_name.setdefault(s["name"], []).append(s)
    for key, s in index["skills"].items():
        s["tag"] = tags.get(s["name"], "untagged")
        ups = [u for u in by_name.get(s["name"], []) if u["repo"] != s["repo"]]
        same = [u for u in ups if u["blob"] == s["blob"]]
        match = (same or ups or [None])[0]
        s["upstream"] = ("identical to" if same else "differs from") if match else ""
        s["upstream_of"] = f"{match['repo']}:{match['path']}" if match else ""
        if s["group"] == "own":
            s["review"] = (
                "reviewed"
                if reviewed.get(key) == s["blob"]
                else "changed since review"
                if key in reviewed
                else "new"
            )
    return index


def render(index):
    own = [s for s in index["skills"].values() if s["group"] == "own"]
    watch = [s for s in index["skills"].values() if s["group"] == "watch"]
    queue = [s for s in own if s["review"] != "reviewed"]

    def link(key):
        repo, path = key.split(":", 1)
        return f"[{repo}](https://github.com/{repo}/blob/HEAD/{path})"

    def row(s):
        up = f"{s['upstream']} {link(s['upstream_of'])}" if s["upstream"] else ""
        where = link(f"{s['repo']}:{s['path']}")
        return (
            f"| `{s['name']}` | {s['kind']} | {s['tag']} | {where} | {up} | {s.get('review', '')} |"
        )

    head = "| Name | Kind | Tag | Where | Upstream | Review |\n|---|---|---|---|---|---|"
    out = [
        "# Index",
        "",
        "Generated by `scripts/refresh.py`; do not edit by hand. The hand-written audit is the",
        "[catalogue](4-reference.md); tags live in `data/tags.json`, the reviewed baseline in",
        "`data/reviewed.json`.",
        "",
        f"{len(own)} own, {len(watch)} watched, {len(queue)} waiting for review.",
        "",
        "## Waiting for review",
        "",
        "New or changed since its last review. An agent reviewing these reads only these files.",
        "",
    ]
    out += (
        [head, *map(row, sorted(queue, key=lambda s: (s["repo"], s["path"])))]
        if queue
        else ["None."]
    )
    for title, group in (("Own", own), ("Watched", watch)):
        out += ["", f"## {title}", "", head]
        out += map(row, sorted(group, key=lambda s: (s["tag"], s["name"], s["repo"])))
    return "\n".join(out) + "\n"


def stars(gh, curated, history, today):
    """Append today's [stars, forks] of each curated repo to history, keyed repo then date."""
    for entry in curated:
        full = entry["repo"]
        r = gh.get(f"{API}/repos/{full}", f"repo:{full}")
        past = history.setdefault(full, {})
        if r:
            past[today] = [r["stargazers_count"], r["forks_count"]]
        elif r is None and past:  # 304: unchanged since the last reading
            past[today] = past[max(past)]
    return history


def gain(past, today, days=30):
    """Stars gained over the last `days`, or since the first reading when history is shorter."""
    if not past or today not in past:
        return None, None
    cutoff = str(date.fromisoformat(today) - timedelta(days=days))
    older = [d for d in past if d <= cutoff]
    base = max(older) if older else min(past)
    return past[today][0] - past[base][0], base


def render_curated(curated, history, today):
    rows = []
    for e in curated:
        past = history.get(e["repo"], {})
        s, base = gain(past, today)
        now = past.get(today, [None, None])
        rows.append((s if s is not None else -1, e, now, s, base))
    rows.sort(key=lambda r: (-r[0], -(r[2][0] or 0)))
    out = [
        "| # | Repository | Stars | Forks | Gained | Tag | Why it is here |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, (_, e, now, s, base) in enumerate(rows, 1):
        if s is None or base == today:
            gained = ""
        elif date.fromisoformat(today) - date.fromisoformat(base) >= timedelta(days=30):
            gained = f"+{s:,}"
        else:
            gained = f"+{s:,} since {base}"
        st = "" if now[0] is None else f"{now[0]:,}"
        fk = "" if now[1] is None else f"{now[1]:,}"
        repo = f"[{e['repo']}](https://github.com/{e['repo']})"
        out.append(f"| {i} | {repo} | {st} | {fk} | {gained} | {e['tag']} | {e['why']} |")
    return "\n".join(out)


def splice(text, block, name):
    start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    head, rest = text.split(start, 1)
    return f"{head}{start}\n{block}\n{end}{rest.split(end, 1)[1]}"


def load(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument(
        "--reviewed",
        nargs="+",
        metavar="KEY",
        help="record repo:path at its indexed blob as reviewed",
    )
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    data = ROOT / "data"
    if args.reviewed:
        skills, reviewed = load(data / "index.json", {})["skills"], load(data / "reviewed.json", {})
        reviewed.update({k: skills[k]["blob"] for k in args.reviewed})
        (data / "reviewed.json").write_text(json.dumps(reviewed, indent=1, sort_keys=True) + "\n")
        return 0
    state = load(data / "index.json", {})
    gh = GitHub(
        os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"), state.get("etags", {})
    )
    index = refresh(gh, load(data / "sources.json", {}), state)
    annotate(index, load(data / "tags.json", {}), load(data / "reviewed.json", {}))
    (data / "index.json").write_text(json.dumps(index, indent=1, sort_keys=True) + "\n")
    (ROOT / "docs/4-reference_index.md").write_text(render(index))
    queue = sum(
        1 for s in index["skills"].values() if s.get("review") in ("new", "changed since review")
    )
    curated = load(data / "curated.json", [])
    if curated:
        today = str(date.today())
        history = stars(gh, curated, load(data / "stars.json", {}), today)
        (data / "stars.json").write_text(json.dumps(history, indent=1, sort_keys=True) + "\n")
        readme = ROOT / "README.md"
        block = render_curated(curated, history, today)
        readme.write_text(splice(readme.read_text(), block, "top-repos"))
    total = len(index["skills"])
    print(f"{total} skills and agents, {queue} waiting for review, {gh.calls} API calls")
    return 0


def self_test():
    class Fake(GitHub):
        def __init__(self, responses):
            super().__init__(None, {})
            self.responses, self.seen = responses, []

        def get(self, url, etag_key=None):
            self.calls += 1
            self.seen.append(url)
            return self.responses.get(url.replace(API, ""), {})

    def blob(s):
        return {"content": b64encode(s.encode()).decode()}

    sk = "---\nname: ponytail\ndescription: >\n  Be lazy,\n  on purpose.\n---\nbody"
    responses = {
        "/users/me/repos?per_page=100&page=1": [
            {
                "full_name": "me/a",
                "default_branch": "main",
                "pushed_at": "t1",
                "fork": False,
                "archived": False,
            },
            {
                "full_name": "me/f",
                "default_branch": "main",
                "pushed_at": "t1",
                "fork": True,
                "archived": False,
            },
        ],
        "/repos/up/x": {"full_name": "up/x", "default_branch": "main", "pushed_at": "t1"},
        "/repos/me/a/git/trees/main?recursive=1": {
            "tree": [
                {"path": ".claude/skills/ponytail/SKILL.md", "type": "blob", "sha": "b1"},
                {"path": ".claude/agents/rev.md", "type": "blob", "sha": "b2"},
                {"path": "node_modules/x/SKILL.md", "type": "blob", "sha": "b3"},
                {"path": "README.md", "type": "blob", "sha": "b4"},
            ]
        },
        "/repos/up/x/git/trees/main?recursive=1": {
            "tree": [{"path": "skills/ponytail/SKILL.md", "type": "blob", "sha": "b1"}]
        },
        "/repos/me/a/git/blobs/b1": blob(sk),
        "/repos/up/x/git/blobs/b1": blob(sk),
        "/repos/me/a/git/blobs/b2": blob("---\nname: rev\ndescription: Reviews.\n---\n"),
    }
    sources = {"own": ["me"], "watch": ["up/x"]}
    gh = Fake(responses)
    idx = annotate(
        refresh(gh, sources, {}), {"ponytail": "backend"}, {"me/a:.claude/agents/rev.md": "old"}
    )
    s = idx["skills"]
    assert set(s) == {
        "me/a:.claude/skills/ponytail/SKILL.md",
        "me/a:.claude/agents/rev.md",
        "up/x:skills/ponytail/SKILL.md",
    }, s.keys()
    p = s["me/a:.claude/skills/ponytail/SKILL.md"]
    assert (p["name"], p["description"], p["tag"]) == (
        "ponytail",
        "Be lazy, on purpose.",
        "backend",
    ), p
    assert (
        p["upstream"] == "identical to" and p["upstream_of"] == "up/x:skills/ponytail/SKILL.md"
    ), p
    assert p["review"] == "new", p
    assert s["me/a:.claude/agents/rev.md"]["review"] == "changed since review"
    assert "me/f" not in idx["repos"], "forks are skipped"
    first = gh.calls

    unchanged = {**responses, "/users/me/repos?per_page=100&page=1": None, "/repos/up/x": None}
    gh2 = Fake(unchanged)  # 304s everywhere: no tree or blob calls, same index
    again = refresh(gh2, sources, idx)
    assert again["skills"].keys() == idx["skills"].keys()
    assert not [u for u in gh2.seen if "/git/" in u], gh2.seen
    assert gh2.calls < first, (gh2.calls, first)

    page = render(annotate(again, {}, {}))
    assert "## Waiting for review" in page and "`rev`" in page
    assert front_matter("no front matter", "a/b/SKILL.md") == ("b", "")
    h = {"a/b": {"2026-09-01": [100, 1], "2026-09-10": [150, 2], "2026-10-07": [400, 9]}}
    assert gain(h["a/b"], "2026-10-07") == (300, "2026-09-01"), gain(h["a/b"], "2026-10-07")
    assert gain({"2026-10-06": [5, 0], "2026-10-07": [8, 0]}, "2026-10-07") == (3, "2026-10-06")
    gh3 = Fake({"/repos/a/b": {"stargazers_count": 7, "forks_count": 1}, "/repos/c/d": None})
    hist = stars(
        gh3, [{"repo": "a/b"}, {"repo": "c/d"}], {"c/d": {"2026-10-06": [3, 0]}}, "2026-10-07"
    )
    assert hist["a/b"]["2026-10-07"] == [7, 1] and hist["c/d"]["2026-10-07"] == [3, 0], hist
    cur = [{"repo": "a/b", "tag": "FE", "why": "x"}, {"repo": "c/d", "tag": "DE", "why": "y"}]
    table = render_curated(cur, hist, "2026-10-07")
    assert table.index("a/b") < table.index("c/d") and "+0 since 2026-10-06" in table, table
    doc = splice("a\n<!-- t:start -->\nold\n<!-- t:end -->\nb", "new", "t")
    assert doc == "a\n<!-- t:start -->\nnew\n<!-- t:end -->\nb", doc
    print("refresh.py self-test: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
