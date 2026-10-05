---
name: wd
license: Apache-2.0
description: "Use for non-CSA long tasks and user-requested long-task audits; arm one shared, evidence-based watchdog relay."
metadata:
  version: 1.1.0
  author: obj
  short-description: "Supervise long tasks with dynamic provider TTLs and progress evidence"
  hermes:
    tags: [watchdog, long-task, kv-cache, supervision]
    related_skills: [skillcfg]
    trigger: "native subagent or non-CSA command expected to exceed 90 seconds"
    exception: "csa session wait"
    invariants:
      - "exactly one shared external relay per parent session"
      - "resolve active-provider TTL before every relay arm"
      - "each check-in establishes health and forward progress"
      - "never poll between check-ins"
---

# WD

## When to use

Use before launching or resuming a native subagent or non-CSA command expected to exceed 90 seconds, and whenever a user requests a long-task status audit. `csa session wait` is the sole boundary exception. This portable skill uses `skillcfg` for provider TTLs; it never reads CSA configuration. Hermes' built-in WD is deprecated.

## Required path

1. Read the active **parent runtime provider** from current session metadata. Never substitute the configured default. Resolve a fresh TTL immediately before each relay arm:

   ```sh
   ACTIVE_PROVIDER=<active-provider> <wd-skill-dir>/scripts/resolve-checkin.sh
   ```

   If using a non-default config, export `SKILLCFG_CONFIG=<path>` first. Otherwise `skillcfg` applies its normal `SKILLCFG_CONFIG`, XDG, and HOME config-path rules. The selected TOML file must be readable and have integer `schema_version = 1`. See [skillcfg usage](../skillcfg/SKILL.md).

2. The resolver prints exactly one positive base-10 integer on success. It checks the exact active-provider key first, then these compatibility keys: `openai-codex` → `codex`, `openai`; `openai*` and `gpt*` → `openai`; `deepseek*` → `deepseek`; `grok*` and `xai*` → `grok`; `localrouter` → `grok`; `pm` → `openai`, `gpt`. A missing key advances to the next alias. A malformed or non-positive value fails immediately; it does not fall through. If no key exists, resolution fails. There is no separate CSA global/local lookup.

3. Start the primary as a managed background task with completion notification and arm **one** external one-shot relay in the same control-plane response. All concurrent child tasks share that relay.

4. At relay expiry, take one bounded census of the exact task handle/PID. Confirm it is live and non-zombie, then inspect a durable side effect. If still live, assess progress and proportionality, resolve the TTL again, and immediately arm one successor. If terminal, consume the authoritative completion receipt and stop the relay.

5. Never replace completion notifications with `process.wait`/polling. A user-requested immediate audit permits one bounded census. If a subagent-owned terminal reports `notify_on_complete=false` despite `notify=true`, use a bounded `process_manage wait` no longer than the freshly resolved interval while the shared relay remains armed. On timeout, perform the normal evidence-bearing check-in and rearm; on completion, stop the relay.

## Health and proportionality

Every check-in assesses **liveness, forward progress, and whether elapsed time is reasonable for the scope**. A running delegate, unchanged receipt, or rearmed timer alone is not a healthy-work verdict.

- Census the exact delegate and owned command handles/PIDs, including zombie/exit state. Compare durable checkpoints, test/build milestones, artifact timestamps, or commits with the previous check-in. Do not inspect native-child transcripts. CPU/I/O may support diagnosis; low utilization alone does not prove a stall.
- Separate preparation, active execution, external waiting, retries, and result collection. Compare the current phase and elapsed time to task scope; do not label long preparation as compilation or invent an ETA.
- Classify `progressing`, `waiting_external`, `suspected_stall`, or `unknown`, with evidence and last verified progress. Missing/stale evidence requires a bounded diagnostic or progress request, not another unsupported “still working normally.” An exited command whose result was not consumed is a collection failure; reconcile that exact result before rerunning.
- If time is disproportionate or successive checkpoints do not advance, narrow the next action. Do not duplicate writers, blindly repeat full gates, kill work merely for elapsed time, or relax verification.
- Respect restart/pause boundaries. If the user forbids steering or new work, perform read-only checks and report concerns; let existing tasks finish naturally. Do not launch replacement agents, commits/hooks, or long work. State restart readiness only after owned non-durable work ends; distinguish verified external survivors from parent-bound work.

## Check-in receipt

For countable jobs, include every progress field; use `unavailable` rather than inventing estimates. A benchmark harness must expose a durable per-wave checkpoint (completed/total and elapsed time); a live PID or open socket alone is not progress evidence.

The developer-only [`tests/resolve-checkin-smoke.sh`](tests/resolve-checkin-smoke.sh) exercises this resolver against a real `skillcfg` executable and isolated TOML config with `csa` absent from `PATH`; it is not a runtime dependency.

```yaml
wd:
  primary: <managed-handle-or-pid>
  state: live | zombie | exited
  ttl:
    provider: <active-provider>
    seconds: <fresh-positive-integer>
  progress:
    completed: <n | unavailable>
    total: <n | unavailable>
    rate_per_s: <number | unavailable>
    eta_s: <number | unavailable>
  health: <progressing | waiting_external | suspected_stall | unknown; evidence>
  proportionality: <phase, elapsed versus task scope, assessment>
  evidence: <change since prior check-in and last verified progress>
  next: rearm | reconcile-completion | escalate
```

## Workload budgets

Before starting long work, size retries, per-request/unit timeouts, and output budgets for the real worst case. Retry only classified transient failures with bounded exponential backoff; persist attempts and terminal errors. A configured output budget must allow meaningful completion. For benchmark checkpointing, hot reload, or workload policies, load `resumable-benchmark-jobs`.

## Boundaries

- A relay schedules a **parent** check-in; it proves neither a provider request nor cache warmth. Do not claim cache savings without usage telemetry.
- Process a newly delivered primary completion immediately, including an out-of-band completion attached to a relay result; never wait for the next heartbeat or repeat a superseded running snapshot.
- Unknown progress stays unavailable: directory size or a missing manifest does not prove download, verification, or completion.
- For Hermes worktrees, push/read back the commit only when publication is authorized; remove a finished worktree before the next dispatch. Never delete the live checkout or a worktree used by a live process.
- Do not inspect native-child transcripts. Use immutable artifacts, process state, and durable side effects.
