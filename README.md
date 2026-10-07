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

## Top 20 skill repositories

Picked for the work here (FE, backend, DE and research, as in the [catalogue](docs/4-reference.md#tags)),
ranked by stars gained in the last 30 days. Listed, not reviewed: run one through the audit before
vendoring it. GitHub publishes clone counts only to a repo's own maintainers, so stars and forks are
the signal. The table is rewritten by the daily refresh from `data/curated.json`; until it has 30 days
of history, "Gained" counts from its first reading.

<!-- top-repos:start -->
| # | Repository | Stars | Forks | Gained | Tag | Why it is here |
|---|---|---|---|---|---|---|
| 1 | [tt-a1i/archify](https://github.com/tt-a1i/archify) | 78.7k |  | +38,190 in Sep | FE | Architecture and workflow diagrams as self-contained HTML; the same job as the umbrella's `architecture-diagram` |
| 2 | [nexu-io/open-design](https://github.com/nexu-io/open-design) | 99.2k |  |  | FE | Design-system skills for agent-built UI; a candidate next to marola-site's `design-taste-frontend` |
| 3 | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | 43.1k |  |  | FE | Diagram design rules for docs and READMEs (MIP-0068's diagrams) |
| 4 | [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) | 5.8k* |  |  | FE | draw.io diagrams from text, for proposal and docs figures |
| 5 | [mattpocock/skills](https://github.com/mattpocock/skills) | 278.2k |  | +1.1k on Oct 6 | backend | An engineer's day-to-day skills; the most starred skills repo this month |
| 6 | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 102.1k |  | +538 on Oct 6 | backend | Production engineering skills: testing, performance, review |
| 7 | [affaan-m/ECC](https://github.com/affaan-m/ECC) | 274.3k |  | +26,563 in Sep | backend | A whole agent harness (skills, memory, security); compare with marola-devkit before borrowing |
| 8 | [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | 43.4k |  |  | backend | Code review skills, next to `ponytail-review` and Claude Code Review |
| 9 | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | 25.4k |  | +559 on Oct 6 | backend | Multi-phase security audit with machine-readable findings, for the app and the site |
| 10 | [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) | 18.8k |  | +3,388 in Sep | research | Scans a skill for risks before it is installed; automates part of this repo's audit |
| 11 | [mksglu/context-mode](https://github.com/mksglu/context-mode) | 24.5k |  | +4,165 in Sep | backend | Context-window savings for agents, the token budget this repo optimises for |
| 12 | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 124.7k |  |  | backend | Codebase knowledge graph; marola adopts it through MIP-0076 (docs/4-reference_graphify.md) |
| 13 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 87.3k* |  |  | backend | Memory across sessions; overlaps the devkit's `obsidian-vault` handoffs |
| 14 | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 47.9k |  |  | research | 177 science skills: scientific writing, peer review, marine carbonate chemistry, CFD, GPU, Polars and Dask |
| 15 | [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 10.7k* |  |  | research | ML research and training skills, for marola-ml's fine-tune and benchmark |
| 16 | [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py) | 17.8k* |  |  | research | NotebookLM from an agent, for literature and proposal reading |
| 17 | [yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) | 14.5k* |  |  | DE | Turns documentation sites, repos and PDFs into skills, e.g. the WAVEWATCH III manual for ww3-gpu |
| 18 | [tigerless-labs/autoharness](https://github.com/tigerless-labs/autoharness) | 9.0k |  | +1.0k on Oct 6 | DE | Distils skills from past sessions and prunes unused ones |
| 19 | [max-sixty/worktrunk](https://github.com/max-sixty/worktrunk) | 8.6k |  | +1,884 in Sep | backend | Git worktrees for parallel agents, the devkit's stacked-PR worktrees |
| 20 | [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 35.1k |  |  | research | A curated directory of 1,000+ skills, to search before writing one |

Seed values from 2026-10-07, before the first refresh: stars from GitHub's pages, "in Sep" from
[GitHub Rank's monthly trending](https://wangchujiang.com/github-rank/trending-monthly.html) (2026-10-01),
"on Oct 6" from [gittrend.io](https://gittrend.io/trending/ai-skills); * marks a count from a cached
topic page, likely low.
<!-- top-repos:end -->

## Review findings

Highest first; each one has its evidence, a proposed fix and the issue tracking it in the repo that owns the fix.

- [R1. `mip-solve-perpetual` implements Draft MIPs unattended](docs/4-reference_review.md#r1-mip-solve-perpetual-implements-draft-mips-unattended) · issue [marola-devkit#36](https://github.com/marola-dev/marola-devkit/issues/36)
- [R2. `voice-to-feature` is allowed to file and close issues](docs/4-reference_review.md#r2-voice-to-feature-is-allowed-to-file-and-close-issues) · issue [marola-devkit#37](https://github.com/marola-dev/marola-devkit/issues/37)
- [R3. Stale copies of the MIP skills on the claude.ai account](docs/4-reference_review.md#r3-stale-copies-of-the-mip-skills-on-the-claudeai-account) · your claude.ai account, no repo issue
- [R4. Paths to a renamed folder](docs/4-reference_review.md#r4-paths-to-a-renamed-folder) · issue [marola-devkit#38](https://github.com/marola-dev/marola-devkit/issues/38)
- [R5. `humanizer` is a version behind upstream](docs/4-reference_review.md#r5-humanizer-is-a-version-behind-upstream) · issue [marola-devkit#39](https://github.com/marola-dev/marola-devkit/issues/39)
- [R6. `ponytail-review` and `ponytail-audit` are behind upstream](docs/4-reference_review.md#r6-ponytail-review-and-ponytail-audit-are-behind-upstream) · issue [marola-devkit#40](https://github.com/marola-dev/marola-devkit/issues/40)
- [R7. `sharingan` and `skill-copy` pin a model and the highest effort](docs/4-reference_review.md#r7-sharingan-and-skill-copy-pin-a-model-and-the-highest-effort) · issue [marola-devkit#41](https://github.com/marola-dev/marola-devkit/issues/41)
- [R8. Evals that ship but have never been run here](docs/4-reference_review.md#r8-evals-that-ship-but-have-never-been-run-here) · issue [marola#700](https://github.com/marola-dev/marola/issues/700)
- [R9. `design-taste-frontend` pulls against the site's rules](docs/4-reference_review.md#r9-design-taste-frontend-pulls-against-the-sites-rules) · issue [marola-site#89](https://github.com/marola-dev/marola-site/issues/89)
- [R10. Two mapbox skills that do not fit marola-site](docs/4-reference_review.md#r10-two-mapbox-skills-that-do-not-fit-marola-site) · issue [marola-site#90](https://github.com/marola-dev/marola-site/issues/90)
- [R11. `karpathy-guidelines` has no licence file](docs/4-reference_review.md#r11-karpathy-guidelines-has-no-licence-file) · issue [marola-site#91](https://github.com/marola-dev/marola-site/issues/91)
- [R12. Two different skills named `eli5`](docs/4-reference_review.md#r12-two-different-skills-named-eli5) · no fix needed
- [R13. `site-frontend`'s baseline run is claimed but not recorded](docs/4-reference_review.md#r13-site-frontends-baseline-run-is-claimed-but-not-recorded) · issue [marola-site#92](https://github.com/marola-dev/marola-site/issues/92)

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
