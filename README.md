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
has each one's origin, test status and review notes. Jump to: [FE](#fe) · [backend](#backend) · [DE](#de) · [research](#research) · [workflow](#workflow).

### FE

17 for the marola.dev map and pages: design, motion, testing, Mapbox.

| Skill | Where | What it does |
|---|---|---|
| [`site-frontend`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/site-frontend/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/site-frontend/SKILL.md) | Use first for any change a visitor sees on marola.dev … |
| [`citizen-science-site`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/citizen-science-site/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/citizen-science-site/SKILL.md) | Use when adding or reviewing a page, section or panel on marola.dev, to keep it an open-source citizen-science site people can trust and … |
| [`ptbr-humanizer`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/ptbr-humanizer/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/ptbr-humanizer/SKILL.md) | Use when writing or reviewing any Portuguese (pt-BR) a visitor reads on marola.dev … |
| [`frontend-design`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/frontend-design/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/frontend-design/SKILL.md) | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. |
| [`webapp-testing`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/webapp-testing/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/webapp-testing/SKILL.md) | Toolkit for interacting with and testing local web applications using Playwright. |
| [`design-taste-frontend`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/design-taste-frontend/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/design-taste-frontend/SKILL.md) | Anti-slop frontend skill for landing pages, portfolios, and redesigns. |
| [`emil-design-eng`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/emil-design-eng/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/emil-design-eng/SKILL.md) | This skill encodes Emil Kowalski's philosophy on UI polish, component design, animation decisions, and the invisible details that make so… |
| [`review-animations`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/review-animations/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/review-animations/SKILL.md) | Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy. |
| [`break-ui`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/break-ui/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/break-ui/SKILL.md) | Try to break a piece of UI by feeding it worst-case data — long names, unbreakable emails, one-letter names, missing fields, huge counts,… |
| [`mapbox-cartography`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-cartography/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-cartography/SKILL.md) | Expert guidance on map design principles, color theory, visual hierarchy, typography, and cartographic best practices for creating effect… |
| [`mapbox-data-visualization-patterns`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-data-visualization-patterns/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-data-visualization-patterns/SKILL.md) | Patterns for visualizing data on maps including choropleth maps, heat maps, 3D visualizations, data-driven styling, and animated data. |
| [`mapbox-maplibre-migration`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-maplibre-migration/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-maplibre-migration/SKILL.md) | Guide for migrating from MapLibre GL JS to Mapbox GL JS, covering API compatibility, token setup, style configuration, and the benefits o… |
| [`mapbox-style-patterns`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-style-patterns/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-style-patterns/SKILL.md) | Common style patterns, layer configurations, and recipes for typical mapping scenarios including restaurant finders, real estate, data vi… |
| [`mapbox-style-quality`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-style-quality/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-style-quality/SKILL.md) | Expert guidance on validating, optimizing, and ensuring quality of Mapbox styles through validation, accessibility checks, and optimization. |
| [`mapbox-token-security`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-token-security/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-token-security/SKILL.md) | Security best practices for Mapbox access tokens, including scope management, URL restrictions, rotation strategies, and protecting sensi… |
| [`mapbox-web-integration-patterns`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-web-integration-patterns/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-web-integration-patterns/SKILL.md) | Official integration patterns for Mapbox GL JS across popular web frameworks (React, Vue, Svelte, Angular). |
| [`mapbox-web-performance-patterns`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-web-performance-patterns/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-web-performance-patterns/SKILL.md) | Performance optimization patterns for Mapbox GL JS web applications. |

### backend

5 for code quality and simplicity, and the Scala app.

| Skill | Where | What it does |
|---|---|---|
| [`ponytail`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/ponytail/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/ponytail/SKILL.md), [ww3-gpu](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/ponytail/SKILL.md) | Forces the laziest solution that actually works, simplest, shortest, most minimal. |
| [`ponytail-review`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/ponytail-review/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/ponytail-review/SKILL.md), [ww3-gpu](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/ponytail-review/SKILL.md) | Code review focused exclusively on over-engineering. |
| [`ponytail-audit`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/ponytail-audit/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/ponytail-audit/SKILL.md), [ww3-gpu](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/ponytail-audit/SKILL.md) | Whole-repo audit for over-engineering. |
| [`karpathy-guidelines`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/karpathy-guidelines/SKILL.md) | [marola-site](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/karpathy-guidelines/SKILL.md) | Behavioral guidelines to reduce common LLM coding mistakes. |
| [`jar-verifier`](https://github.com/marola-dev/marola-app/blob/main/.claude/agents/jar-verifier.md) (agent) | [marola-app](https://github.com/marola-dev/marola-app/blob/main/.claude/agents/jar-verifier.md) | Verifies a Kyo (or any other pre-1.0/undocumented-drift-risk dependency) API by decompiling the actual pinned jar with javap, instead of … |

### DE

2 for getting data in: corpus documents, voice notes.

| Skill | Where | What it does |
|---|---|---|
| [`corpus-doc`](https://github.com/marola-dev/marola-corpus/blob/main/.claude/skills/corpus-doc/SKILL.md) | [marola-corpus](https://github.com/marola-dev/marola-corpus/blob/main/.claude/skills/corpus-doc/SKILL.md) | Add a new document to marola's knowledge corpus — the ocean/sea-lore notes that --ask and the ask_ocean_question MCP too… |
| [`voice-note-ingest`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/voice-note-ingest/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/voice-note-ingest/SKILL.md) | Transcribe a local voice note (WhatsApp .ogg, or similar) with local Whisper, write the transcript next to the audio, and anonymize it be… |

### research

8 for writing, citing and releasing research work.

| Skill | Where | What it does |
|---|---|---|
| [`eli5`](https://github.com/marola-dev/marola/blob/main/.claude/skills/eli5/SKILL.md) | [marola](https://github.com/marola-dev/marola/blob/main/.claude/skills/eli5/SKILL.md), [ww3-gpu](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/eli5/SKILL.md) | Explains a topic to a newcomer: ocean and marola topics in the umbrella, wave modelling in ww3-gpu (two different skills). |
| [`humanizer`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/humanizer/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/humanizer/SKILL.md), [ww3-gpu](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/humanizer/SKILL.md) | Rewrite AI-sounding text so it reads like the writer without changing what it says. |
| [`humanizar`](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/humanizar/SKILL.md) | [ww3-gpu](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/humanizar/SKILL.md) | Reescreve textos em português brasileiro para soarem mais humanos e naturais, reduzindo padrões típicos de escrita gerada por IA sem alte… |
| [`citation-cff`](https://github.com/marola-dev/marola/blob/main/.claude/skills/citation-cff/SKILL.md) | [marola](https://github.com/marola-dev/marola/blob/main/.claude/skills/citation-cff/SKILL.md) | This skill should be used when the user asks to "create citation file", "generate CITATION.cff", "validate citation", "update citation", … |
| [`zenodo-release`](https://github.com/marola-dev/marola/blob/main/.claude/skills/zenodo-release/SKILL.md) | [marola](https://github.com/marola-dev/marola/blob/main/.claude/skills/zenodo-release/SKILL.md) | Cut a citable marola release and keep its Zenodo and citation metadata right. |
| [`release`](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/release/SKILL.md) | [ww3-gpu](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/release/SKILL.md) | Cut a citable ww3-gpu release and keep its Zenodo/citation metadata right. |
| [`corpus-doc`](https://github.com/marola-dev/marola-corpus/blob/main/.claude/skills/corpus-doc/SKILL.md) | [marola-corpus](https://github.com/marola-dev/marola-corpus/blob/main/.claude/skills/corpus-doc/SKILL.md) | Add a new document to marola's knowledge corpus — the ocean/sea-lore notes that --ask and the ask_ocean_question MCP too… |
| [`revisor-proposta`](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/agents/revisor-proposta.md) (agent) | [ww3-gpu](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/agents/revisor-proposta.md) | Revisor científico da proposta de projeto de graduação (pubs/proposal). |

### workflow

11 for the team's process: MIPs, issues, stacked PRs, porting skills.

| Skill | Where | What it does |
|---|---|---|
| [`mip`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/mip/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/mip/SKILL.md) | Write or revise a Marola Improvement Proposal (MIP) — a numbered design doc under docs/MIPs/ for any non-trivial feature, integration, or… |
| [`mip-tasks`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/mip-tasks/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/mip-tasks/SKILL.md) | Turn an accepted MIP into an ordered task list and deliver it as small stacked PRs (one task = one branch = one PR, each based on the pre… |
| [`mip-solve-perpetual`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/mip-solve-perpetual/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/mip-solve-perpetual/SKILL.md) | Overnight/unattended MIP-tasks runner. |
| [`triage`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/triage/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/triage/SKILL.md) | Turn a raw idea, a voice-note fragment or a bug report into one well-formed marola issue — pick the tier, draft the body in the matching … |
| [`sharingan`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/sharingan/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/sharingan/SKILL.md) | Port a skill, workflow or pattern from another repository into marola, given its URL — fetch the whole unit, check its licence, map every… |
| [`skill-copy`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/skill-copy/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/skill-copy/SKILL.md) | Alias for sharingan — port a skill or pattern from another repository's URL into marola. |
| [`obsidian-vault`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/obsidian-vault/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/obsidian-vault/SKILL.md) | Save and resume marola work sessions through the maintainer's Obsidian vault, and keep a linked marola digest note there. |
| [`voice-to-feature`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/voice-to-feature/SKILL.md) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/voice-to-feature/SKILL.md) | Presentation/demo pipeline — turn a recorded voice note directly into a scaffolded feature branch and a Draft PR, in one pass. |
| [`architecture-diagram`](https://github.com/marola-dev/marola/blob/main/.claude/skills/architecture-diagram/SKILL.md) | [marola](https://github.com/marola-dev/marola/blob/main/.claude/skills/architecture-diagram/SKILL.md) | Draw a polished architecture or repo-map diagram as a hand-written SVG a README can embed: dark grid card, colour per kind of component, … |
| [`mip-reviewer`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/agents/mip-reviewer.md) (agent) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/agents/mip-reviewer.md) | Reviews one PR of a marola MIP task stack against its MIP-NNNN.tasks.md row and the MIP's own Scoring/Verification-plan sections, reporti… |
| [`mip-claims-auditor`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/agents/mip-claims-auditor.md) (agent) | [marola-devkit](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/agents/mip-claims-auditor.md) | Audits one MIP's §4 (Data sources and dependencies reviewed) for unsourced external claims — a price, a count, an HTTP status, a licence … |

**workflow** is a fifth tag: these skills run the team's process (MIPs, issues, stacked PRs,
porting skills) and fit none of the other four.


## Featured: Graphify

[Graphify](https://github.com/Graphify-Labs/graphify) (124.7k stars) turns a codebase into a knowledge
graph an agent queries instead of reading trees. marola adopts it through
[MIP-0076](https://docs.marola.dev/6-MIPs/MIP-0076-agent-routing-tooling/), offline and keyless behind
the devkit's `just graph`, never by installing the skill. [How, and where the work
stands](docs/4-reference_graphify.md).

## OODS lake (MIP-0075)

Skills and agents for the open ocean data lake that
[MIP-0075](https://docs.marola.dev/6-MIPs/MIP-0075-water-quality-store-r2/) builds on Cloudflare R2:
Cloudflare's own, DuckDB's, and the data-engineering ones whose rules a marola skill ports. Each
does one or more of five jobs, INIT, MANAGE, GOV, DEBUG and CONNECT. The daily refresh counts
how many have been adopted in the repos MIP-0075 lands in:

<!-- oods:start -->
**0 of 13 adopted** in MIP-0075's repos. By job: INIT 0/2 · MANAGE 0/6 · GOV 0/5 · DEBUG 0/6 · CONNECT 0/3.
<!-- oods:end -->

[Every skill, its upstream, how it comes in and what to watch for](docs/4-reference_oods.md).

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
- [OODS lake skills](docs/4-reference_oods.md): what helps build and run MIP-0075's lake, and how
  much of it is adopted.
- [Development](docs/3-development.md): how each status was established, with the commands to
  reproduce it, and how to refresh the catalogue.

The umbrella's [Agent skills](https://docs.marola.dev/3-Ways-of-working/AGENT-SKILLS/) page says
when to reach for each skill in marola's workflow; this repo is the inventory and the audit, and
it also covers ww3-gpu.

## Contracts

| Direction | Contract |
|---|---|
| repos → this | Read-only: the skills are read from each repo's `main`; nothing here is copied back |
| this → umbrella | `submodule-updated` on every push to `main`, and `submodule-docs-updated` when `README.md` or `docs/` changed (`notify-umbrella.yml`) |
| devkit → this | `marola-devkit`, pinned to one tag in `flake.nix`, the workflows and `.claude/settings.json` |

[AGENTS.md](AGENTS.md) holds the rules for agents working here. MIT licence; each skill keeps the
licence of the repo it lives in.
