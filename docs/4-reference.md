# Catalogue

Every skill and subagent, as of 2026-10-07. Paths are on each repo's `main`. How each status was
established is in [Development](3-development.md); the ⚠ rows are explained in
[Needs review](4-reference_review.md).

## Status

| Status | Meaning |
|---|---|
| **Evaluated** | A recorded run of the skill's evals, with the result in a commit's `Tested:` trailer or body |
| **Upstream** | Vendored, and byte-identical to the upstream repo's `main` on 2026-10-07 (licence file aside). Its quality is upstream's; nobody here ran its evals |
| **Upstream, edited** | Vendored with local edits, listed in the row |
| **Behind** | Vendored from an older upstream version that has since changed |
| **Gated** | Only a structural check runs: `claude plugin validate`, a front-matter parse, or a script's `--self-test` |
| **Untested** | Nothing checks it beyond being used |
| ⚠ | Flagged, see [Needs review](4-reference_review.md) |

## Tags

| Tag | Meaning |
|---|---|
| **FE** | What a visitor sees: pages, design, the map, front-end testing |
| **backend** | Writing and reviewing application code (Scala, Kyo, the over-engineering checks) |
| **DE** | Data engineering: ingesting and shaping data the product reads (the corpus, transcripts) |
| **research** | Scientific and written work: explaining, writing prose, citation and releases, the proposal review |
| **workflow** | How the team works: MIPs, issues, stacked PRs, porting skills. Outside the four asked-for tags; see the README |

## marola-site — `.claude/skills/`

| Skill | Tag | Origin | Status | Notes |
|---|---|---|---|---|
| `site-frontend` | FE | own | Untested | Entry point that orders the other frontend skills; ships `site_check.js`, which CI runs as a site gate, not as a skill test. ⚠ R13 |
| `citizen-science-site` | FE | own | Untested | |
| `ptbr-humanizer` | FE | own | Untested | pt-BR copy on marola.dev; not the same skill as ww3-gpu's `humanizar` |
| `frontend-design` | FE | anthropics/skills@683bc88 | Upstream | |
| `webapp-testing` | FE | anthropics/skills@683bc88 | Upstream | Ships 4 Python helpers |
| `design-taste-frontend` | FE | Leonxlnx/taste-skill@b482f7a | Upstream ⚠ R9 | 1,206 lines |
| `emil-design-eng` | FE | emilkowalski/skill@e8a175d | Upstream | |
| `review-animations` | FE | emilkowalski/skill@e8a175d | Upstream | `disable-model-invocation` |
| `break-ui` | FE | emilkowalski/skill@e8a175d | Upstream | |
| `karpathy-guidelines` | backend | forrestchang/andrej-karpathy-skills@2c60614 | Upstream ⚠ R11 | |
| `mapbox-cartography` | FE | mapbox/mapbox-agent-skills@f71cd72 | Upstream ⚠ R8 | 3 evals, not run here |
| `mapbox-data-visualization-patterns` | FE | same | Upstream ⚠ R8 | 3 evals, not run here |
| `mapbox-maplibre-migration` | FE | same | Upstream ⚠ R8 R10 | 3 evals, not run here |
| `mapbox-style-patterns` | FE | same | Upstream ⚠ R8 | 3 evals, not run here |
| `mapbox-style-quality` | FE | same | Upstream ⚠ R8 | 3 evals, not run here |
| `mapbox-token-security` | FE | same | Upstream ⚠ R8 | 3 evals, not run here |
| `mapbox-web-integration-patterns` | FE | same | Upstream ⚠ R8 R10 | 3 evals, not run here |
| `mapbox-web-performance-patterns` | FE | same | Upstream ⚠ R8 | 3 evals, not run here |

## marola-devkit — the `marola-devkit` plugin, `plugins/marola-devkit/`

The plugin as a whole passes `claude plugin validate --strict` on every devkit change, which makes
every row here at least Gated for its front matter.

| Skill or agent | Tag | Origin | Status | Notes |
|---|---|---|---|---|
| `mip` | workflow | own | Gated | |
| `mip-tasks` | workflow | own | Gated ⚠ R4 | `disable-model-invocation` |
| `mip-solve-perpetual` | workflow | own | Gated ⚠ R1 | Unattended overnight runner |
| `triage` | workflow | own | Gated ⚠ R4 | `disable-model-invocation` |
| `sharingan` | workflow | own | Gated ⚠ R4 R7 | 3 output + 12 trigger evals written, never run |
| `skill-copy` | workflow | own | Gated ⚠ R7 | Alias stub for `sharingan` |
| `obsidian-vault` | workflow | rewritten from edvmorango/nix-home-config@e541e6e (no licence upstream) | **Evaluated** (1 of 5) | Eval 2: 4/4 assertions with the skill, baseline without it missed `--continue` and the stale note (marola-dev/marola#410) |
| `voice-note-ingest` | DE | own | Gated | `scripts/transcribe.py --self-test` runs in `tests/self-tests.sh` |
| `voice-to-feature` | workflow | own | Gated ⚠ R2 | `disable-model-invocation` |
| `humanizer` | research | blader/humanizer v3.0.0 | Behind ⚠ R5 | Upstream is v3.1.0 (225a6f3) |
| `ponytail` | backend | DietrichGebert/ponytail@552acd5 | Upstream | |
| `ponytail-review` | backend | DietrichGebert/ponytail | Behind ⚠ R6 | |
| `ponytail-audit` | backend | DietrichGebert/ponytail | Behind ⚠ R6 | |
| agent `mip-reviewer` | workflow | own | Gated ⚠ R4 | |
| agent `mip-claims-auditor` | workflow | own | Gated | |

## marola (the umbrella) — `.claude/skills/`

| Skill | Tag | Origin | Status | Notes |
|---|---|---|---|---|
| `eli5` | research | own | Untested ⚠ R12 | Every path it cites was checked to exist when it moved in (#652) |
| `architecture-diagram` | workflow | adapted from Cocoon-AI/architecture-diagram-generator@4b9087d (MIT) | Untested ⚠ R8 | 2 output + 12 trigger evals; only checked to parse |
| `zenodo-release` | research | own, adapted from ww3-gpu's `release` | Untested | The scripts it drives (`citation.py`, `release.sh`) have self-tests; the skill itself does not |
| `citation-cff` | research | zircote/github-social@4fa6579 | Upstream ⚠ R8 | 7 evals, not run here |

## marola-corpus — `.claude/skills/`

| Skill | Tag | Origin | Status | Notes |
|---|---|---|---|---|
| `corpus-doc` | DE, research | own | **Evaluated** | 14 trigger queries via skill-creator's `run_eval.py`, 1 run each: 10/14, 0 false positives (4d55a45, 2026-09-06) |

## marola-app — `.claude/agents/`

| Agent | Tag | Origin | Status | Notes |
|---|---|---|---|---|
| `jar-verifier` | backend | own | Untested | Decompiles the pinned Kyo jar with `javap` |

## h0ffmann/ww3-gpu — `.claude/skills/` and `.claude/agents/`

`.claude/hooks/check_agent_frontmatter.py` parses every skill's and agent's front matter on each
change, so every row is at least Gated.

| Skill or agent | Tag | Origin | Status | Notes |
|---|---|---|---|---|
| `eli5` | research | own | Gated ⚠ R12 | Wave-modelling and HPC vocabulary; a different skill from the umbrella's `eli5` |
| `release` | research | own | Gated | `release.sh --dry-run` tested in 2b7819d; the skill's prompt is not |
| `humanizar` | research | fabricioctelles/skills@4fcc2bf (Apache-2.0) | Upstream, edited | Jev section dropped, sibling link changed, audience paragraph added; all noted under its front matter. Otherwise equal to upstream `main` (f1de632) |
| `humanizer` | research | blader/humanizer v3.0.0 | Behind ⚠ R5 | The devkit copy plus a 5-line audience paragraph |
| `ponytail` | backend | DietrichGebert/ponytail@552acd5 | Upstream, edited | Audience paragraph added |
| `ponytail-review` | backend | DietrichGebert/ponytail | Behind ⚠ R6 | Audience paragraph added |
| `ponytail-audit` | backend | DietrichGebert/ponytail | Behind ⚠ R6 | Audience paragraph added |
| agent `revisor-proposta` | research | own | Gated | Backed by `proposal_lint.py` and `proposal_review_gate.py`, both with `--self-test` |

## Outside the repos

Hoffmann's claude.ai account also carries `mip`, `mip-tasks` and `mip-solve-perpetual` (they load as
`anthropic-skills:*`). They are older copies of the devkit's and point at `docs/mips/`, a path that
no longer exists. ⚠ R3
