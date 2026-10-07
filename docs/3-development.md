# Development

How each status in the [catalogue](4-reference.md) was established on 2026-10-07, and how to
refresh it. Run from a directory holding a checkout of each source repo side by side (the
umbrella with its submodules works, plus ww3-gpu).

## Finding the skills

```bash
find marola marola-site marola-devkit marola-corpus marola-app marola-ml marola-oods ww3-gpu \
  \( -name SKILL.md -o -path '*/.claude/agents/*.md' -o -path '*/plugins/*/agents/*.md' \) \
  -not -path '*/.git/*' -not -path '*/.devkit/*'
```

## Evaluated

A skill is Evaluated only when a commit records a real eval run and its score. Search the history:

```bash
git -C <repo> log --format='%h %s%n%b' -- <skill dir> | grep -iE 'eval|baseline|without'
```

The two that pass: marola-corpus 4d55a45 (`corpus-doc`, 10/14 trigger queries) and the
`obsidian-vault` commit of marola-dev/marola#410 (eval 2, 4/4 against a failing baseline). An
`evals/` folder that only "parses" does not count.

Running a set: skill-creator's runner, as `corpus-doc` did. It calls a model, so the run's cost
goes in the commit's `Cost:`.

```bash
python3 <skill-creator>/scripts/run_eval.py --skill-path <skill dir> --runs-per-query 3
```

## Upstream and Behind

Clone each upstream at its `main`, then compare the skill folder, ignoring the licence file that
was copied in beside it:

```bash
git clone --depth 1 https://github.com/<owner>/<repo> up/<repo>
diff -r -x LICENSE -x LICENSE.txt -x LICENSE.md up/<repo>/skills/<name> <repo>/.claude/skills/<name>
git -C up/<repo> log -1 --format='%h %as'
```

No output means Upstream. When there is a diff, read it: lines only upstream has mean Behind;
lines only the local copy has are a local edit, which the row lists. The upstream commits used on
2026-10-07:

| Upstream | Commit |
|---|---|
| anthropics/skills | 683bc88 |
| Leonxlnx/taste-skill | b482f7a |
| emilkowalski/skill | e8a175d |
| forrestchang/andrej-karpathy-skills | 2c60614 |
| mapbox/mapbox-agent-skills | f71cd72 |
| blader/humanizer | 225a6f3 (v3.1.0) |
| DietrichGebert/ponytail | 552acd5 |
| fabricioctelles/skills | f1de632 |
| zircote/github-social | 4fa6579 |

## Gated

The structural checks that run on every change in the owning repo:

| Repo | Check |
|---|---|
| marola-devkit | `claude plugin validate --strict .`; `bash tests/self-tests.sh` (includes `transcribe.py --self-test`) |
| ww3-gpu | `python3 .claude/hooks/check_agent_frontmatter.py`; `proposal_lint.py` and `proposal_review_gate.py --self-test` for `revisor-proposta` |

A gate proves the file parses and its scripts work, not that the skill does what it says.

## Review flags

The paths each skill cites were checked to exist (a renamed folder shows up here as R4):

```bash
grep -oE '`[A-Za-z0-9_./-]+\.(md|sh|py|js|json|yml)`' <SKILL.md> | tr -d '`' | sort -u
```

The rest came from reading each skill's front matter (`allowed-tools`, `model`, `effort`,
`disable-model-invocation`) against its repo's `AGENTS.md` and `.claude/settings.json`.

## The daily refresh

`scripts/refresh.py` does by API what the sections above do by hand, without spending model tokens:

| Step | API calls |
|---|---|
| List each owner's public repos (forks and archived repos skipped) | 1 per 100 repos, a 304 when unchanged |
| Each watched `owner/repo` | 1, a 304 when unchanged |
| A repo's tree, only when it was pushed since the last run | 1 |
| A `SKILL.md` or agent, only when its blob sha changed | 1 |

A git blob sha is a hash of the file, so "identical to upstream" is two equal shas between an own
skill and a watched one with the same name, and "changed since review" is a sha that differs from
`data/reviewed.json`. Measured on 2026-10-07 against the six audited repos: 66 calls on a cold run,
9 (all 304s) on the next.

```bash
python3 scripts/refresh.py --self-test   # offline, a fake API
GH_TOKEN=… python3 scripts/refresh.py    # live; any token that reads public repos
python3 scripts/refresh.py --reviewed marola-dev/marola-site:.claude/skills/break-ui/SKILL.md
```

`refresh.yml` reads with `MAROLA_CROSS_REPO_PAT` when this repo has access to that org secret, else
the workflow's own token. Only the PAT makes the rolling PR start CI. Private repos are not listed.

## Refreshing the audit

Re-run the three comparisons above, update the rows whose evidence changed, and date the README's
status line. When a flagged skill is fixed in its repo, delete its finding from
[Needs review](4-reference_review.md) and its ⚠ from the catalogue, citing the fixing commit.
