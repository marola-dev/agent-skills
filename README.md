# agent-skills

A catalogue of every Claude Code skill and subagent used across marola-dev and
[h0ffmann/ww3-gpu](https://github.com/h0ffmann/ww3-gpu): where each one lives, where it came from,
what has actually been tested, and which ones need a human to look at them.

**Status:** hand-audited on 2026-10-07, refreshed daily by a workflow. Nothing here is loaded by
Claude Code: skills keep living in the repo that uses them, and this repo describes them.

## Automation

`refresh.yml` runs every day at 06:17 UTC (or by hand from the Actions tab). It finds every
`SKILL.md` and subagent in all public repos of the owners in [`data/sources.json`](data/sources.json),
and in the outside repos or users it watches. It writes `data/index.json` and
`docs/4-reference_index.md` (both appear with the first run), and opens one rolling PR when
anything changed.

It spends no model tokens: discovery is GitHub API calls only, and repos not pushed since the last
run cost a 304. Only the PR's "Waiting for review" list, the skills that are new or changed since
their last review, ever needs an agent to read them. To watch someone else's skills, add
`"owner"` (all their public repos) or `"owner/repo"` to `watch` in `data/sources.json`.

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

## By tag

Every skill carries one tag (two for `corpus-doc`); the [catalogue](docs/4-reference.md#tags)
defines them.

| Tag | Skills and agents |
|---|---|
| **FE** (17) | `site-frontend`, `citizen-science-site`, `ptbr-humanizer`, `frontend-design`, `webapp-testing`, `design-taste-frontend`, `emil-design-eng`, `review-animations`, `break-ui`, the eight `mapbox-*` |
| **backend** (5 names, 8 copies) | `ponytail`, `ponytail-review`, `ponytail-audit` (devkit and ww3-gpu), `karpathy-guidelines`, agent `jar-verifier` |
| **DE** (2) | `corpus-doc`, `voice-note-ingest` |
| **research** (8 names, 10 copies) | `eli5` (umbrella and ww3-gpu, different skills), `humanizer` (devkit and ww3-gpu), `humanizar`, `citation-cff`, `zenodo-release`, `release`, `corpus-doc`, agent `revisor-proposta` |
| **workflow** (11) | `mip`, `mip-tasks`, `mip-solve-perpetual`, `triage`, `sharingan`, `skill-copy`, `obsidian-vault`, `voice-to-feature`, `architecture-diagram`, agents `mip-reviewer`, `mip-claims-auditor` |

**workflow** is a fifth tag: these skills run the team's process (MIPs, issues, stacked PRs,
porting skills) and fit none of the other four.

## Featured: Graphify

[Graphify](https://github.com/Graphify-Labs/graphify) (124.7k stars) turns a codebase into a knowledge
graph an agent queries instead of reading trees. marola adopts it through
[MIP-0076](https://docs.marola.dev/6-MIPs/MIP-0076-agent-routing-tooling/), offline and keyless behind
the devkit's `just graph`, never by installing the skill. [How, and where the work
stands](docs/4-reference_graphify.md).

## Review findings

Highest first; each one has its evidence and a proposed fix.

- [R1. `mip-solve-perpetual` implements Draft MIPs unattended](docs/4-reference_review.md#r1-mip-solve-perpetual-implements-draft-mips-unattended)
- [R2. `voice-to-feature` is allowed to file and close issues](docs/4-reference_review.md#r2-voice-to-feature-is-allowed-to-file-and-close-issues)
- [R3. Stale copies of the MIP skills on the claude.ai account](docs/4-reference_review.md#r3-stale-copies-of-the-mip-skills-on-the-claudeai-account)
- [R4. Paths to a renamed folder](docs/4-reference_review.md#r4-paths-to-a-renamed-folder)
- [R5. `humanizer` is a version behind upstream](docs/4-reference_review.md#r5-humanizer-is-a-version-behind-upstream)
- [R6. `ponytail-review` and `ponytail-audit` are behind upstream](docs/4-reference_review.md#r6-ponytail-review-and-ponytail-audit-are-behind-upstream)
- [R7. `sharingan` and `skill-copy` pin a model and the highest effort](docs/4-reference_review.md#r7-sharingan-and-skill-copy-pin-a-model-and-the-highest-effort)
- [R8. Evals that ship but have never been run here](docs/4-reference_review.md#r8-evals-that-ship-but-have-never-been-run-here)
- [R9. `design-taste-frontend` pulls against the site's rules](docs/4-reference_review.md#r9-design-taste-frontend-pulls-against-the-sites-rules)
- [R10. Two mapbox skills that do not fit marola-site](docs/4-reference_review.md#r10-two-mapbox-skills-that-do-not-fit-marola-site)
- [R11. `karpathy-guidelines` has no licence file](docs/4-reference_review.md#r11-karpathy-guidelines-has-no-licence-file)
- [R12. Two different skills named `eli5`](docs/4-reference_review.md#r12-two-different-skills-named-eli5)
- [R13. `site-frontend`'s baseline run is claimed but not recorded](docs/4-reference_review.md#r13-site-frontends-baseline-run-is-claimed-but-not-recorded)

## Docs

- [Catalogue](docs/4-reference.md): every skill and agent, with its source, upstream pin and test
  status.
- [Needs review](docs/4-reference_review.md): the flagged ones, each with the evidence and a
  proposed fix.
- [Graphify](docs/4-reference_graphify.md): how marola adopts it, the rules and the open tasks.
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
