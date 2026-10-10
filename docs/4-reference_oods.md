# OODS lake skills

The skills and agents that help build and run [MIP-0075](https://docs.marola.dev/6-MIPs/MIP-0075-water-quality-store-r2/)'s
open ocean data lake: a DuckLake whose catalog and Parquet live in the Cloudflare R2 bucket
`br-open-ocean-data-storage`, written weekly by marola-app's `oods` module from marola-oods
workflows ([marola#672](https://github.com/marola-dev/marola/issues/672)). Each one does one or more
of five jobs:

| Job | For the lake |
|---|---|
| INIT | the bucket, tokens and endpoint (a person's, §5.6), the schema as numbered migrations |
| MANAGE | `oods maintain`: expire snapshots, clean and merge files, backups, size against the free tier |
| GOV | who may write (one writer, the `oods-lake` group), the two R2 tokens, secrets never persisted, checks never weakened |
| DEBUG | a failed or `partial` run: `fetch_run`, the Actions log, time travel to the last good snapshot |
| CONNECT | attaching the catalog `READ_ONLY`, the `TYPE s3` secret on R2's endpoint, reading `exports/` |

## Adoption

A skill counts as adopted when a skill or agent in a repo MIP-0075 lands in (marola-oods,
marola-app) carries it: a vendored one by its `skills.lock` row (MIP-0080) naming the same upstream
and path, a ported one by the in-house skill it was ported into (`oods-lake`, whose `NOTICE.md`
credits each source). `scripts/refresh.py` counts it from the index on every daily run and rewrites
the table below and the README's summary; the rest of this file is hand-written.

<!-- oods:start -->
**0 of 13 adopted** in MIP-0075's repos. By job: INIT 0/2 · MANAGE 0/6 · GOV 0/5 · DEBUG 0/6 · CONNECT 0/3.

| Skill | Jobs | Upstream | Comes in | Status | Why | Caveat |
|---|---|---|---|---|---|---|
| `oods-lake` | INIT, MANAGE, GOV, DEBUG, CONNECT | in-house | write in marola-oods (marola-dev/marola-oods#23) | not yet | The lake's own skill: migrations, time travel and recovery, maintenance, `checks.sql` as a gate, the R2 tokens and bucket rules | Stacks on marola-dev/marola-oods#22; its first PR (#24) closed unmerged |
| `oods-lake-reviewer` | GOV, DEBUG | in-house | write in marola-oods (agent) | not yet | Read-only review of a MIP-0075 diff against the lake's invariants: one writer, upload before export, no persistent secret, inlining off, applied migrations never edited, no glob over `lake/` | Reports, never edits; a person decides |
| `cloudflare` | INIT, GOV | [cloudflare/skills](https://github.com/cloudflare/skills/tree/0871daceb347e3c51693fbe9c77555468df7e410/skills/cloudflare) (Apache-2.0) | vendor into marola-oods | not yet | Cloudflare's own product map, with `references/r2/` (S3 API, tokens, lifecycle, limits, pricing, gotchas) | Points at live docs, not facts; R2 setup stays a person's (MIP-0075 §5.6) |
| `s3-explore` | CONNECT, DEBUG | [duckdb/duckdb-skills](https://github.com/duckdb/duckdb-skills/tree/7feda8e01e22bc0886c86123f3884947e36d8c69/skills/s3-explore) (MIT) | vendor into marola-oods | not yet | Lists the bucket and reads Parquet metadata without downloading data (`read_blob` without `content`, `parquet_metadata`) | Its R2 row is a `TYPE R2` secret on `r2://`; the lake uses `TYPE s3` on `s3://` (§4.4). Its `FROM '<glob>'` preview returns wrong rows on `lake/` after an update: list and read metadata only, query through an attach |
| `attach-db` | CONNECT | [duckdb/duckdb-skills](https://github.com/duckdb/duckdb-skills/tree/7feda8e01e22bc0886c86123f3884947e36d8c69/skills/attach-db) (MIT) | vendor into marola-oods | not yet | Attaches a local copy of `oods.ducklake` and keeps the session for `query` | Its `state.sql` may hold secrets in plain text: attach `READ_ONLY`, keep the R2 secret out of it |
| `query` | DEBUG | [duckdb/duckdb-skills](https://github.com/duckdb/duckdb-skills/tree/7feda8e01e22bc0886c86123f3884947e36d8c69/skills/query) (MIT) | vendor into marola-oods | not yet | Runs SQL on the attached lake (`beach_point`, `fetch_run`, `AT (VERSION => n)`); sets `allow_persistent_secrets=false` | Read-only by use, not by design: the attach must be `READ_ONLY` |
| `duckdb-docs` | DEBUG, MANAGE | [duckdb/duckdb-skills](https://github.com/duckdb/duckdb-skills/tree/7feda8e01e22bc0886c86123f3884947e36d8c69/skills/duckdb-docs) (MIT) | vendor into marola-oods | not yet | Full-text search over the DuckDB and DuckLake docs, so an answer cites the version the lake pins | Downloads the search indexes and installs `httpfs` and `fts` locally; never in a job |
| `motherduck-ducklake` | MANAGE | [motherduckdb/agent-skills](https://github.com/motherduckdb/agent-skills/tree/f97855858bee6cff552031358666824cf01754c5/skills/motherduck-ducklake) (MIT) | port into oods-lake | not yet | DuckLake maintenance as explicit operations (`ducklake_flush_inlined_data`, `merge_adjacent_files`), the single-writer reality, the version matrix | Written for MotherDuck: keep the DuckLake parts, drop the product's |
| `iceberg` | MANAGE | [gordonmurray/data-engineering-skills](https://github.com/gordonmurray/data-engineering-skills/tree/3547aef2e488de606ce03118d0fac6ecf941a5f2/iceberg) (MIT) | port into oods-lake | not yet | The Inspect first, Decide, Safety, Verify shape; retention windows, orphan cleanup, rollback | Iceberg, not DuckLake: structure and rules only |
| `hops-table-maintenance` | MANAGE | [logicalclocks/hopsworks-api](https://github.com/logicalclocks/hopsworks-api/tree/37ce5742e2d29c8e9ff0b8b925f58ad371a43c22/python/hopsworks/skills/data/hops-table-maintenance) (Apache-2.0) | port into oods-lake | not yet | Evidence from a script, a reviewable plan, approval per destructive step, dry run, before and after | Spark and feature groups: the workflow only |
| `b2-cloud-storage` | GOV, MANAGE | [backblaze-labs/claude-skill-b2-cloud-storage](https://github.com/backblaze-labs/claude-skill-b2-cloud-storage/tree/422d0a435fc0cd0a1bc5e270aefca820ca40cf31/skills/b2-cloud-storage) (MIT) | port into oods-lake | not yet | Object-store safety rules (read-only by default, dry run and an explicit yes before a delete, never public) and the size and cost audit | Re-point from B2 to R2: no versioning, no spend cap |
| `troubleshooting-dbt-job-errors` | DEBUG | [dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills/tree/168a2b0b92da59be88866257140907c206ff0e44/skills/dbt/skills/troubleshooting-dbt-job-errors) (Apache-2.0) | port into oods-lake | not yet | Diagnosing a failed scheduled job from its logs, history and data, and "never modify a test to make it pass" (for `checks.sql`) | dbt Cloud: map its logs and API to the Actions run and `fetch_run` |
| `security-audit` | GOV | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit) (MIT) | vendor into marola-oods | not yet | A security review of the ETL workflows and the `oods` module, which hold the R2 write token | Run its full workflow only on an explicit audit request; findings go to a person |
<!-- oods:end -->

Upstream commits and licences were read from fresh clones on 2026-10-10. "Comes in" is a
proposal: vendoring is a PR in marola-oods pinned in its `skills.lock`, porting goes through
[marola-oods#23](https://github.com/marola-dev/marola-oods/issues/23).

## Looked at and left out

| Skill | Upstream | Why not |
|---|---|---|
| `wrangler` | [cloudflare/skills](https://github.com/cloudflare/skills) | The lake uses the AWS CLI and DuckDB's S3 API, not Wrangler; the bucket and tokens are a person's. A fit for marola-site's Worker (#12) |
| `basin` | [cloudflare/skills](https://github.com/cloudflare/skills) | R2 Iceberg tables through Basin Catalog: a different table format and a paid product path, rejected by MIP-0075 §4.4 |
| `install-duckdb` | [duckdb/duckdb-skills](https://github.com/duckdb/duckdb-skills) | Installs extensions from the network; MIP-0075 row 2 pins them by sha256 and a job never downloads code |
| `motherduck-connect, motherduck-security-governance` | [motherduckdb/agent-skills](https://github.com/motherduckdb/agent-skills) | MotherDuck's service, which the lake does not use |

## Not counted

MIP-0075 is already delivered with the team's workflow skills, which are not lake skills:
`mip-tasks` and `mip-reviewer` (the devkit) run its task stack, and `jar-verifier` (marola-app)
checks the Kyo signatures §5.4 calls indicative. They are in the [catalogue](4-reference.md).
