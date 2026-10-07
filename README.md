# agent-skills

A catalogue of every Claude Code skill and subagent used across marola-dev and
[h0ffmann/ww3-gpu](https://github.com/h0ffmann/ww3-gpu): where each one lives, where it came from,
what has actually been tested, and which ones need a human to look at them.

**Status:** documentation only, reviewed by hand on 2026-10-07. Nothing here is loaded by Claude
Code: skills keep living in the repo that uses them, and this repo describes them.

## At a glance

| | Count |
|---|---|
| Skills (`SKILL.md`) | 43 files, 37 distinct names |
| Subagents | 4: `mip-reviewer`, `mip-claims-auditor` (devkit), `jar-verifier` (marola-app), `revisor-proposta` (ww3-gpu) |
| Written here | 18 |
| Vendored from a third party | 25, of which 17 are byte-identical to upstream today |
| Evaluated (a recorded run with and without the skill) | 2: `corpus-doc`, `obsidian-vault` |
| Ship evals nobody here has run | 11 (`mapbox-*` ×8, `citation-cff`, `sharingan`, `architecture-diagram`), plus 4 of `obsidian-vault`'s 5 |
| Flagged for review | 13 findings, three of them high |

Where they live: marola-site (18), the marola-devkit plugin (13 + 2 agents), the umbrella (4),
marola-corpus (1), marola-app (1 agent), ww3-gpu (7 + 1 agent). marola-ml and marola-oods have
none.

## Docs

- [Catalogue](docs/4-reference.md): every skill and agent, with its source, upstream pin and test
  status.
- [Needs review](docs/4-reference_review.md): the flagged ones, each with the evidence and a
  proposed fix.
- [Development](docs/3-development.md): how each status was established, with the commands to
  reproduce it, and how to refresh the catalogue.

The umbrella's [Agent skills](https://docs.marola.dev/3-Ways-of-working/AGENT-SKILLS/) page says
when to reach for each skill in marola's workflow; this repo is the inventory and the audit, and
it also covers ww3-gpu.

## Contracts

| Direction | Contract |
|---|---|
| repos → this | Read-only: the skills are read from each repo's `main`; nothing here is copied back |
| this → umbrella | `README.md` and `docs/`, once this repo is added to the docs build |

[AGENTS.md](AGENTS.md) holds the rules for agents working here. MIT licence; each skill keeps the
licence of the repo it lives in.
