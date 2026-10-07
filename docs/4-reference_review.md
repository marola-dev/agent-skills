# Needs review

Thirteen findings from the 2026-10-07 audit, highest first. Each names the evidence and a proposed
fix in the repo that owns the skill; nothing has been changed there yet. Line numbers are on that
repo's `main` on the audit date.

## High

### R1. `mip-solve-perpetual` implements Draft MIPs unattended

marola-devkit `plugins/marola-devkit/skills/mip-solve-perpetual/SKILL.md`

- With no argument it auto-picks a MIP whose status is **Draft** (line 27) and implements it
  overnight, opening a PR per task. The workflow (DEV-FLOW) needs a human to accept a MIP first,
  and the org invariant says an agent begins implementation only on an issue labelled
  `agent-ready`. The skill never mentions `agent-ready`.
- `allowed-tools` grants `Bash(git *)`, which covers `git push --force` and `git reset --hard`,
  not only the `--force-with-lease` the body asks for (line 69).
- Line 148 points at `scripts/usage-lib.js`, which exists nowhere in the org.
- Mitigation already in place: every marola repo denies `gh pr merge` and `gh pr close` in
  `.claude/settings.json`, so it cannot merge.

**Fix:** pick only from issues labelled `agent-ready` (`just issue-queue`), never from MIP status;
narrow `Bash(git *)` to the subcommands it uses; drop the `usage-lib.js` pointer.

### R2. `voice-to-feature` is allowed to file and close issues

marola-devkit `plugins/marola-devkit/skills/voice-to-feature/SKILL.md:5`

`allowed-tools` includes `Bash(gh issue *)`, which pre-approves `gh issue create`, `close` and
`delete`. Nothing in the skill's body uses it, and the umbrella's rule is that filing is a
human's act (MIP-0063 §5.6).

**Fix:** remove `Bash(gh issue *)`.

### R3. Stale copies of the MIP skills on the claude.ai account

Hoffmann's account skills `mip`, `mip-tasks` and `mip-solve-perpetual` (they load as
`anthropic-skills:mip` and so on, next to `marola-devkit:mip`) are older than the devkit's. They
write to `docs/mips/`, but the folder is `docs/MIPs/`, and `mip`'s description still mentions a
`docs/SKILLS.md` exam roadmap. Two skills with the same trigger phrases means either can fire.

**Fix:** delete the three from the account's skills on claude.ai; the devkit plugin is the one
copy.

## Medium

### R4. Paths to a renamed folder

`docs/3-Working-on-the-repo/` became `docs/3-Ways-of-working/` in the umbrella (the redirect is in
`mkdocs/mkdocs.yml`), but these still cite the old path:

| File (marola-devkit, `plugins/marola-devkit/`) | Lines |
|---|---|
| `skills/mip-tasks/SKILL.md` | 80, 81, 149 |
| `skills/triage/SKILL.md` | 9, 62 |
| `skills/sharingan/SKILL.md` | 43, 71, 79 (and `evals/evals.json:22`) |
| `agents/mip-reviewer.md` | 9, 50 |

**Fix:** one search-and-replace in the devkit, then a devkit release.

### R5. `humanizer` is a version behind upstream

Both copies (devkit and ww3-gpu) are blader/humanizer v3.0.0; upstream is v3.1.0 (225a6f3), which
adds a "wrong reader" tell, sharper closer and hyphenation rules, and fixes a section reference
(the dash rule is §8, the copy says §6).

**Fix:** re-vendor v3.1.0 in the devkit; in ww3-gpu, re-vendor and keep the audience paragraph.

### R6. `ponytail-review` and `ponytail-audit` are behind upstream

Upstream (DietrichGebert/ponytail@552acd5) now numbers findings so the user can say "fix 2 and
5", adds a `reuse:` tag for a helper that already exists in the repo, and makes `ponytail-audit`
grep the tree before it recommends a delete. Both the devkit's and ww3-gpu's copies predate that;
`ponytail` itself is current.

**Fix:** re-vendor both, in both repos (ww3-gpu keeps its audience paragraph).

### R7. `sharingan` and `skill-copy` pin a model and the highest effort

Both set `model: claude-opus-5-5` and `effort: xhigh`. Every port runs at the most expensive
setting, and the pin breaks quietly when that model id is retired. `sharingan`'s 15 evals have
never been run, so there is no measurement that the pin is needed.

**Fix:** run the evals once at the default model and effort; keep the pin only if they fail
there.

### R8. Evals that ship but have never been run here

`architecture-diagram` (2 output, 12 trigger), `sharingan` (3, 12), `obsidian-vault` (4 of its 5
output cases), `citation-cff` (7) and the eight `mapbox-*` skills (3 each). The only record for
`architecture-diagram`'s is "evals.json parses".

**Fix:** run each set once with skill-creator's runner and record the score in the commit, as
`corpus-doc` did (4d55a45). The mapbox and `citation-cff` evals test upstream's skills, so they
are the lowest priority.

## Low

### R9. `design-taste-frontend` pulls against the site's rules

1,206 lines loaded whenever it triggers, and it recommends `npm install` of design systems
(lines 991–1025) and shadcn, while marola-site is plain JavaScript with no build step.
`site-frontend` already says the repo's rules win.

**Fix:** keep it, but consider `disable-model-invocation: true` so it loads only when asked.

### R10. Two mapbox skills that do not fit marola-site

`mapbox-maplibre-migration` covers moving off MapLibre, which marola never used.
`mapbox-web-integration-patterns` (lines 23–46) installs Mapbox from npm or a CDN `<script>`, while
the site vendors Mapbox GL JS's CSP build under `script-src 'self'`.

**Fix:** drop `mapbox-maplibre-migration`; keep the other, since `site-frontend` arbitrates.

### R11. `karpathy-guidelines` has no licence file

Its front matter says `license: MIT`, but neither the vendored folder nor the upstream repo
(forrestchang/andrej-karpathy-skills@2c60614) has a `LICENSE`. Every other vendored skill carries
one.

**Fix:** ask upstream to add one, or record the README's licence statement next to the skill.

### R12. Two different skills named `eli5`

The umbrella's explains sea and marola topics to a lay reader; ww3-gpu's explains wave-modelling
and HPC vocabulary. They never load together, but in a shared view the name hides that they are
unrelated (105 and 76 lines, with 111 diff lines between them).

**Fix:** none needed in the repos; this catalogue lists them separately.

### R13. `site-frontend`'s baseline run is claimed but not recorded

The umbrella's Agent skills page says `site-frontend` was written with superpowers'
`writing-skills`, with a baseline run without it. No commit records that run, so it is listed as
Untested.

**Fix:** re-run a baseline and with-skill comparison and record it, or drop the claim.

## Also worth knowing

ww3-gpu's `.claude/settings.json` has no `permissions.deny`, unlike every marola repo (which deny
`gh pr merge`, `gh pr close` and `gh stack merge`). Its `release` skill tags and pushes; a deny
for `gh pr merge` and `gh pr close` there would match the marola setup.
