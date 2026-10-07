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
| [`site-frontend`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/site-frontend/SKILL.md) | FE | own | Untested | Entry point that orders the other frontend skills; ships `site_check.js`, which CI runs as a site gate, not as a skill test. ⚠ [R13](4-reference_review.md#r13-site-frontends-baseline-run-is-claimed-but-not-recorded) |
| [`citizen-science-site`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/citizen-science-site/SKILL.md) | FE | own | Untested | |
| [`ptbr-humanizer`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/ptbr-humanizer/SKILL.md) | FE | own | Untested | pt-BR copy on marola.dev; not the same skill as ww3-gpu's `humanizar` |
| [`frontend-design`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/frontend-design/SKILL.md) | FE | [anthropics/skills@683bc88](https://github.com/anthropics/skills/tree/683bc88/skills/frontend-design) | Upstream | |
| [`webapp-testing`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/webapp-testing/SKILL.md) | FE | [anthropics/skills@683bc88](https://github.com/anthropics/skills/tree/683bc88/skills/webapp-testing) | Upstream | Ships 4 Python helpers |
| [`design-taste-frontend`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/design-taste-frontend/SKILL.md) | FE | [Leonxlnx/taste-skill@b482f7a](https://github.com/Leonxlnx/taste-skill/tree/b482f7a/skills/taste-skill) | Upstream ⚠ [R9](4-reference_review.md#r9-design-taste-frontend-pulls-against-the-sites-rules) | 1,206 lines |
| [`emil-design-eng`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/emil-design-eng/SKILL.md) | FE | [emilkowalski/skill@e8a175d](https://github.com/emilkowalski/skill/tree/e8a175d/skills/emil-design-eng) | Upstream | |
| [`review-animations`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/review-animations/SKILL.md) | FE | [emilkowalski/skill@e8a175d](https://github.com/emilkowalski/skill/tree/e8a175d/skills/review-animations) | Upstream | `disable-model-invocation` |
| [`break-ui`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/break-ui/SKILL.md) | FE | [emilkowalski/skill@e8a175d](https://github.com/emilkowalski/skill/tree/e8a175d/skills/break-ui) | Upstream | |
| [`karpathy-guidelines`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/karpathy-guidelines/SKILL.md) | backend | [forrestchang/andrej-karpathy-skills@2c60614](https://github.com/forrestchang/andrej-karpathy-skills/tree/2c60614/skills/karpathy-guidelines) | Upstream ⚠ [R11](4-reference_review.md#r11-karpathy-guidelines-has-no-licence-file) | |
| [`mapbox-cartography`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-cartography/SKILL.md) | FE | [mapbox/mapbox-agent-skills@f71cd72](https://github.com/mapbox/mapbox-agent-skills/tree/f71cd72/skills/mapbox-cartography) | Upstream ⚠ [R8](4-reference_review.md#r8-evals-that-ship-but-have-never-been-run-here) | 3 evals, not run here |
| [`mapbox-data-visualization-patterns`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-data-visualization-patterns/SKILL.md) | FE | [mapbox/mapbox-agent-skills@f71cd72](https://github.com/mapbox/mapbox-agent-skills/tree/f71cd72/skills/mapbox-data-visualization-patterns) | Upstream ⚠ [R8](4-reference_review.md#r8-evals-that-ship-but-have-never-been-run-here) | 3 evals, not run here |
| [`mapbox-maplibre-migration`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-maplibre-migration/SKILL.md) | FE | [mapbox/mapbox-agent-skills@f71cd72](https://github.com/mapbox/mapbox-agent-skills/tree/f71cd72/skills/mapbox-maplibre-migration) | Upstream ⚠ [R8](4-reference_review.md#r8-evals-that-ship-but-have-never-been-run-here) [R10](4-reference_review.md#r10-two-mapbox-skills-that-do-not-fit-marola-site) | 3 evals, not run here |
| [`mapbox-style-patterns`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-style-patterns/SKILL.md) | FE | [mapbox/mapbox-agent-skills@f71cd72](https://github.com/mapbox/mapbox-agent-skills/tree/f71cd72/skills/mapbox-style-patterns) | Upstream ⚠ [R8](4-reference_review.md#r8-evals-that-ship-but-have-never-been-run-here) | 3 evals, not run here |
| [`mapbox-style-quality`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-style-quality/SKILL.md) | FE | [mapbox/mapbox-agent-skills@f71cd72](https://github.com/mapbox/mapbox-agent-skills/tree/f71cd72/skills/mapbox-style-quality) | Upstream ⚠ [R8](4-reference_review.md#r8-evals-that-ship-but-have-never-been-run-here) | 3 evals, not run here |
| [`mapbox-token-security`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-token-security/SKILL.md) | FE | [mapbox/mapbox-agent-skills@f71cd72](https://github.com/mapbox/mapbox-agent-skills/tree/f71cd72/skills/mapbox-token-security) | Upstream ⚠ [R8](4-reference_review.md#r8-evals-that-ship-but-have-never-been-run-here) | 3 evals, not run here |
| [`mapbox-web-integration-patterns`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-web-integration-patterns/SKILL.md) | FE | [mapbox/mapbox-agent-skills@f71cd72](https://github.com/mapbox/mapbox-agent-skills/tree/f71cd72/skills/mapbox-web-integration-patterns) | Upstream ⚠ [R8](4-reference_review.md#r8-evals-that-ship-but-have-never-been-run-here) [R10](4-reference_review.md#r10-two-mapbox-skills-that-do-not-fit-marola-site) | 3 evals, not run here |
| [`mapbox-web-performance-patterns`](https://github.com/marola-dev/marola-site/blob/main/.claude/skills/mapbox-web-performance-patterns/SKILL.md) | FE | [mapbox/mapbox-agent-skills@f71cd72](https://github.com/mapbox/mapbox-agent-skills/tree/f71cd72/skills/mapbox-web-performance-patterns) | Upstream ⚠ [R8](4-reference_review.md#r8-evals-that-ship-but-have-never-been-run-here) | 3 evals, not run here |

## marola-devkit — the `marola-devkit` plugin, `plugins/marola-devkit/`

The plugin as a whole passes `claude plugin validate --strict` on every devkit change, which makes
every row here at least Gated for its front matter.

| Skill or agent | Tag | Origin | Status | Notes |
|---|---|---|---|---|
| [`mip`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/mip/SKILL.md) | workflow | own | Gated | |
| [`mip-tasks`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/mip-tasks/SKILL.md) | workflow | own | Gated ⚠ [R4](4-reference_review.md#r4-paths-to-a-renamed-folder) | `disable-model-invocation` |
| [`mip-solve-perpetual`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/mip-solve-perpetual/SKILL.md) | workflow | own | Gated ⚠ [R1](4-reference_review.md#r1-mip-solve-perpetual-implements-draft-mips-unattended) | Unattended overnight runner |
| [`triage`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/triage/SKILL.md) | workflow | own | Gated ⚠ [R4](4-reference_review.md#r4-paths-to-a-renamed-folder) | `disable-model-invocation` |
| [`sharingan`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/sharingan/SKILL.md) | workflow | own | Gated ⚠ [R4](4-reference_review.md#r4-paths-to-a-renamed-folder) [R7](4-reference_review.md#r7-sharingan-and-skill-copy-pin-a-model-and-the-highest-effort) | 3 output + 12 trigger evals written, never run |
| [`skill-copy`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/skill-copy/SKILL.md) | workflow | own | Gated ⚠ [R7](4-reference_review.md#r7-sharingan-and-skill-copy-pin-a-model-and-the-highest-effort) | Alias stub for `sharingan` |
| [`obsidian-vault`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/obsidian-vault/SKILL.md) | workflow | rewritten from [edvmorango/nix-home-config@e541e6e](https://github.com/edvmorango/nix-home-config/blob/e541e6e/programs/claude/skills/obsidian-vault/SKILL.md) (no licence upstream) | **Evaluated** (1 of 5) | Eval 2: 4/4 assertions with the skill, baseline without it missed `--continue` and the stale note (marola-dev/marola#410) |
| [`voice-note-ingest`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/voice-note-ingest/SKILL.md) | DE | own | Gated | `scripts/transcribe.py --self-test` runs in `tests/self-tests.sh` |
| [`voice-to-feature`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/voice-to-feature/SKILL.md) | workflow | own | Gated ⚠ [R2](4-reference_review.md#r2-voice-to-feature-is-allowed-to-file-and-close-issues) | `disable-model-invocation` |
| [`humanizer`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/humanizer/SKILL.md) | research | [blader/humanizer](https://github.com/blader/humanizer) v3.0.0 | Behind ⚠ [R5](4-reference_review.md#r5-humanizer-is-a-version-behind-upstream) | Upstream is v3.1.0 (225a6f3) |
| [`ponytail`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/ponytail/SKILL.md) | backend | [DietrichGebert/ponytail@552acd5](https://github.com/DietrichGebert/ponytail/tree/552acd5/skills/ponytail) | Upstream | |
| [`ponytail-review`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/ponytail-review/SKILL.md) | backend | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/tree/552acd5/skills/ponytail-review) | Behind ⚠ [R6](4-reference_review.md#r6-ponytail-review-and-ponytail-audit-are-behind-upstream) | |
| [`ponytail-audit`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/skills/ponytail-audit/SKILL.md) | backend | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/tree/552acd5/skills/ponytail-audit) | Behind ⚠ [R6](4-reference_review.md#r6-ponytail-review-and-ponytail-audit-are-behind-upstream) | |
| agent [`mip-reviewer`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/agents/mip-reviewer.md) | workflow | own | Gated ⚠ [R4](4-reference_review.md#r4-paths-to-a-renamed-folder) | |
| agent [`mip-claims-auditor`](https://github.com/marola-dev/marola-devkit/blob/main/plugins/marola-devkit/agents/mip-claims-auditor.md) | workflow | own | Gated | |

## marola (the umbrella) — `.claude/skills/`

| Skill | Tag | Origin | Status | Notes |
|---|---|---|---|---|
| [`eli5`](https://github.com/marola-dev/marola/blob/main/.claude/skills/eli5/SKILL.md) | research | own | Untested ⚠ [R12](4-reference_review.md#r12-two-different-skills-named-eli5) | Every path it cites was checked to exist when it moved in (#652) |
| [`architecture-diagram`](https://github.com/marola-dev/marola/blob/main/.claude/skills/architecture-diagram/SKILL.md) | workflow | adapted from [Cocoon-AI/architecture-diagram-generator@4b9087d](https://github.com/Cocoon-AI/architecture-diagram-generator/tree/4b9087d) (MIT) | Untested ⚠ [R8](4-reference_review.md#r8-evals-that-ship-but-have-never-been-run-here) | 2 output + 12 trigger evals; only checked to parse |
| [`zenodo-release`](https://github.com/marola-dev/marola/blob/main/.claude/skills/zenodo-release/SKILL.md) | research | own, adapted from ww3-gpu's [`release`](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/release/SKILL.md) | Untested | The scripts it drives (`citation.py`, `release.sh`) have self-tests; the skill itself does not |
| [`citation-cff`](https://github.com/marola-dev/marola/blob/main/.claude/skills/citation-cff/SKILL.md) | research | [zircote/github-social@4fa6579](https://github.com/zircote/github-social/tree/4fa6579/skills/citation-cff) | Upstream ⚠ [R8](4-reference_review.md#r8-evals-that-ship-but-have-never-been-run-here) | 7 evals, not run here |

## marola-corpus — `.claude/skills/`

| Skill | Tag | Origin | Status | Notes |
|---|---|---|---|---|
| [`corpus-doc`](https://github.com/marola-dev/marola-corpus/blob/main/.claude/skills/corpus-doc/SKILL.md) | DE, research | own | **Evaluated** | 14 trigger queries via skill-creator's `run_eval.py`, 1 run each: 10/14, 0 false positives (4d55a45, 2026-09-06) |

## marola-app — `.claude/agents/`

| Agent | Tag | Origin | Status | Notes |
|---|---|---|---|---|
| [`jar-verifier`](https://github.com/marola-dev/marola-app/blob/main/.claude/skills/jar-verifier/SKILL.md) | backend | own | Untested | Decompiles the pinned Kyo jar with `javap` |

## h0ffmann/ww3-gpu — `.claude/skills/` and `.claude/agents/`

`.claude/hooks/check_agent_frontmatter.py` parses every skill's and agent's front matter on each
change, so every row is at least Gated.

| Skill or agent | Tag | Origin | Status | Notes |
|---|---|---|---|---|
| [`eli5`](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/eli5/SKILL.md) | research | own | Gated ⚠ [R12](4-reference_review.md#r12-two-different-skills-named-eli5) | Wave-modelling and HPC vocabulary; a different skill from the umbrella's `eli5` |
| [`release`](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/release/SKILL.md) | research | own | Gated | `release.sh --dry-run` tested in 2b7819d; the skill's prompt is not |
| [`humanizar`](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/humanizar/SKILL.md) | research | [fabricioctelles/skills@4fcc2bf](https://github.com/fabricioctelles/skills/tree/4fcc2bf/skills/humanizar) (Apache-2.0) | Upstream, edited | Jev section dropped, sibling link changed, audience paragraph added; all noted under its front matter. Otherwise equal to upstream `main` (f1de632) |
| [`humanizer`](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/humanizer/SKILL.md) | research | [blader/humanizer](https://github.com/blader/humanizer) v3.0.0 | Behind ⚠ [R5](4-reference_review.md#r5-humanizer-is-a-version-behind-upstream) | The devkit copy plus a 5-line audience paragraph |
| [`ponytail`](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/ponytail/SKILL.md) | backend | [DietrichGebert/ponytail@552acd5](https://github.com/DietrichGebert/ponytail/tree/552acd5/skills/ponytail) | Upstream, edited | Audience paragraph added |
| [`ponytail-review`](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/ponytail-review/SKILL.md) | backend | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/tree/552acd5/skills/ponytail-review) | Behind ⚠ [R6](4-reference_review.md#r6-ponytail-review-and-ponytail-audit-are-behind-upstream) | Audience paragraph added |
| [`ponytail-audit`](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/skills/ponytail-audit/SKILL.md) | backend | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/tree/552acd5/skills/ponytail-audit) | Behind ⚠ [R6](4-reference_review.md#r6-ponytail-review-and-ponytail-audit-are-behind-upstream) | Audience paragraph added |
| agent [`revisor-proposta`](https://github.com/h0ffmann/ww3-gpu/blob/main/.claude/agents/revisor-proposta.md) | research | own | Gated | Backed by `proposal_lint.py` and `proposal_review_gate.py`, both with `--self-test` |

## Outside the repos

Hoffmann's claude.ai account also carries `mip`, `mip-tasks` and `mip-solve-perpetual` (they load as
`anthropic-skills:*`). They are older copies of the devkit's and point at `docs/mips/`, a path that
no longer exists. ⚠ [R3](4-reference_review.md#r3-stale-copies-of-the-mip-skills-on-the-claudeai-account)
