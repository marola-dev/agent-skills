# AGENTS.md

Instructions for any AI coding agent working in **agent-skills**. This is the repo layer
(MIP-0070 §5.1): the workspace rules live in the umbrella's
[AGENTS.md](https://github.com/marola-dev/marola/blob/main/AGENTS.md); this file says what this
repo is and where it differs.

<!-- invariants:start -->
## Org invariants

Non-negotiable in every marola repo; a repo may make these stricter, never looser (MIP-0070 §5.1).

- **Cost and deployment safety**: never provision or deploy a paid cloud resource without explicit human confirmation first ([AGENTS.md](AGENTS.md#cost--deployment-safety-hard-rule)).
- **No secrets in code**: never hardcode a key/connection string/secret; `.env.example` holds placeholders only ([AGENTS.md](AGENTS.md#cost--deployment-safety-hard-rule)).
- **The agent-ready gate**: an agent may only begin implementation on an issue carrying `agent-ready` ([AGENTS.md](AGENTS.md#issue-tracking-hard-rule)).
- **The three commit trailers**: commits carry three trailers and nothing else — `Tested:`, `Cost:`, and `Co-Authored-By: Claude <noreply@anthropic.com>` ([AGENTS.md](AGENTS.md#attribution-and-cost-accounting-hard-rule)).
- **Phase discipline**: work one phase at a time; never start a later phase before the current one is done ([AGENTS.md](AGENTS.md#phase-discipline-hard-rule)).
<!-- invariants:end -->

## What this repo is

Documentation of the Claude Code skills and subagents in the marola-dev repos and in
h0ffmann/ww3-gpu: `README.md` and `docs/`. It holds no copy of any skill. A skill is fixed in the
repo that has it, and the row here is updated in the same week.

## Updating a row

A status is a claim, so it carries its evidence: the commit whose `Tested:` trailer records the
run, the upstream commit a vendored copy was compared against, or the `file:line` behind a
review flag. [docs/3-development.md](docs/3-development.md) has the commands. A status nobody can
reproduce is "Untested", never "Evaluated".

## Issue tracking (hard rule)

An agent starts work only on an issue carrying `agent-ready`, in this repo (MIP-0070 §5.7).

## Attribution and cost accounting (hard rule)

Commits carry `Tested:`, `Cost:` and `Co-Authored-By: Claude <noreply@anthropic.com>`, as in the
umbrella.

## Cost & deployment safety (hard rule)

As in the umbrella. Nothing here deploys or runs anything paid. Running a skill's evals calls a
model, so it counts toward the change's `Cost:`.

## Phase discipline (hard rule)

The phase list is the umbrella's `docs/PHASES.md`.

## Docs

`README.md` is the landing; `docs/` holds numbered pages (MIP-0074 §5.2), no `docs/index.md`.
Links are relative inside the repo and `https://docs.marola.dev/…` or GitHub URLs across repos.
