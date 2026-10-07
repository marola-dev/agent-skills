# Graphify

[Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) turns a codebase, with its docs,
schemas and configs, into a knowledge graph an agent can query instead of reading trees. It ships as
a `/graphify` skill for Claude Code, Codex, Cursor and Gemini CLI. Code is parsed locally with
tree-sitter; docs, YAML, PDFs and images go to an LLM pass. 124.7k stars and 12.0k forks on
2026-10-07; Apache-2.0, with a `LICENSE-MIT` for code from before the relicensing.

For marola it is already designed: [MIP-0076](https://docs.marola.dev/6-MIPs/MIP-0076-agent-routing-tooling/)
was accepted on 2026-10-03. Adopting it means delivering that MIP's open tasks, not installing the
skill.

## Why marola uses it, and for what

MIP-0017 §9 rejected graphify while marola was one repo, because `Grep` already gave an agent its
context in seconds. The polyrepo split (MIP-0070) changed that, so MIP-0076 ran two offline spikes on
the real workspace:

- It graphs the whole umbrella in one run: 4,921 nodes and 8,447 edges in 3.7 s, 0 tokens.
- It answers **symbol** questions ("where is X?"): 3 hits, 3 partials and 2 misses out of 8.
- It does not see the **wiring** between repos (workflows, dispatches, pin files). A generated table
  answers those instead: 5 of the 8 questions in 2.5 KB read once.

So graphify is half of MIP-0076. The other half is a `wiring` extractor whose table lives in the
umbrella's `REPOS.md`, and a routing skill picks between the two and `git grep`.

## The marola way

| Do | Don't (MIP-0076 §4, §5.2, §9) |
|---|---|
| Run it through the devkit's `just graph` (`build`, `query`, `path`, `explain`) | Run bare `graphify`, which can start the LLM pass |
| Take nixpkgs' `graphify` (0.9.66) through the devkit's flake lock | `pip`/`uv` install it, a second pinning mechanism |
| `extract . --code-only --no-label`, under `env -i` with `GRAPHIFY_NO_AUTO_REFRESH=1` and no API keys | Its LLM pass over YAML and docs: ~0.6–0.7M tokens a pass |
| Write output to `${XDG_CACHE_HOME:-$HOME/.cache}/marola-graph/<repo>` via `GRAPHIFY_OUT` | Commit `graphify-out/` (5.9 MB that churns) or leave it in the checkout |
| `query` with `--budget 400` (~1.8 KB an answer) | Read `GRAPH_REPORT.md` (~21k tokens) or `graph.json` whole |
| A committed `.graphifyignore` for noise (`**/vendor/**`) | `graphify install`, its hooks or `--strict`: they collide with the devkit's `core.hooksPath` and plugin |
| The CLI | Its MCP server: the same answers plus ~6.6 KB of tool schemas |

The routing rule the skill will carry (§5.3): wiring questions read the `REPOS.md` block; "where is
X" with an unknown keyword uses `just graph query` and reads only the files it names; a known
keyword uses `git grep --recurse-submodules`.

## Where the work stands

MIP-0074, which MIP-0076 was blocked by, is implemented. Every MIP-0076 task is open, and none
carries `agent-ready` yet, so an agent cannot start them until a person labels them.

| Task | Issue | What |
|---|---|---|
| 1–4 | [devkit#25](https://github.com/marola-dev/marola-devkit/issues/25), [#26](https://github.com/marola-dev/marola-devkit/issues/26), [#27](https://github.com/marola-dev/marola-devkit/issues/27), [#28](https://github.com/marola-dev/marola-devkit/issues/28) | The `wiring` extractor, its `--check`, `notify-umbrella` on every push, the devkit release |
| 5–11 | [marola#661](https://github.com/marola-dev/marola/issues/661), the five `*-notify` rows, [marola#662](https://github.com/marola-dev/marola/issues/662) | The generated wiring block and each repo's devkit bump |
| 12 | [devkit#29](https://github.com/marola-dev/marola-devkit/issues/29) | `graph`: the devkit tool around nixpkgs' graphify |
| 13 | [devkit#30](https://github.com/marola-dev/marola-devkit/issues/30) | The `routing` plugin skill |
| 14 | [devkit#31](https://github.com/marola-dev/marola-devkit/issues/31) | Devkit release with `graph` |
| 15 | [marola#663](https://github.com/marola-dev/marola/issues/663) | `wiring --check` in the umbrella's gates |
| 16 | [marola#664](https://github.com/marola-dev/marola/issues/664) | Umbrella on the new devkit, `.graphifyignore`, the `AGENTS.md` paragraph |
| 17 | [marola#665](https://github.com/marola-dev/marola/issues/665) | A CI job that builds the graph as a 7-day artifact |
| 18 | [marola#666](https://github.com/marola-dev/marola/issues/666) | MIP-0076 flipped to Implemented |

The full order and each task's tests are in
[MIP-0076.tasks.md](https://github.com/marola-dev/marola/blob/main/docs/MIPs/MIP-0076.tasks.md).
Done means at least 7 of the 8 spike questions answered right first on a fresh clone, with 0 tokens
in graphify's report footer (§7).

## Outside marola

In a personal repo with no devkit, the same rules keep it cheap: `uv tool install graphifyy`, then
`graphify extract . --code-only --no-label` with `GRAPHIFY_OUT` pointing outside the checkout, and
`graphify query --budget 400`. Skip `graphify install` if the repo already manages its own skills
and hooks.
