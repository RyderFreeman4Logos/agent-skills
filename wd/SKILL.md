---
name: wd
license: MIT
description: "Use for every non-CSA long task. Dynamic TTL check-ins."
metadata:
  version: 1.0.0
  author: obj
  short-description: "Supervise long tasks with dynamic, evidence-bearing check-ins"
  hermes:
    tags: [watchdog, long-task, kv-cache, supervision]
    trigger: "native subagent or non-CSA command expected to exceed 90 seconds"
    exception: "csa session wait"
    invariants:
      - "exactly one shared external relay per parent session"
      - "resolve active-provider TTL at every arm"
      - "each check-in proves health and forward progress"
      - "never poll between check-ins"
---

# WD

## When to Use

Use before launching or resuming any native subagent or non-CSA command expected to exceed 90 seconds, and whenever a user requests a long-task status audit.

## Required path

Use this skill for every native subagent and non-CSA long command. `csa session wait` is the only exception. Hermes' built-in WD is deprecated.

1. Identify the active parent runtime provider from current session metadata; never use the configured default. Export it as `ACTIVE_PROVIDER` and resolve `CHECKIN` immediately before every relay arm:

   ```bash
   ACTIVE_PROVIDER=<active-provider> <wd-skill-dir>/scripts/resolve-checkin.sh
   ```

   Use the linked `scripts/resolve-checkin.sh` path from `skill_view` when it is not repo-local. Abort if resolution does not return one positive integer. Do not hardcode or cache a TTL.
2. Start the primary as a managed background task with completion notification and start **one** external one-shot relay in the same control-plane response. Concurrent children share that relay.
3. On relay expiry, do one exact-handle/PID census. Confirm it is live and non-zombie; inspect a durable side effect. If the primary is live, resolve the TTL again and immediately arm one successor relay. If it is terminal, consume the authoritative completion receipt and stop the associated relay.
4. Never use `process.wait`/polling as a substitute when completion notifications are available. A user-requested immediate audit permits one bounded census. If a subagent-owned terminal explicitly reports `notify_on_complete=false` despite `notify=true`, consume that exact managed primary with a bounded `process_manage wait` no longer than the freshly resolved check-in interval; keep the one shared relay armed. This is a notification-unavailable exception, not permission for status polling. On timeout, perform the normal evidence-bearing check-in and rearm; on terminal completion, stop the relay.

## Mandatory health and proportionality check

Every check-in must assess **liveness, forward progress, and whether elapsed time is reasonable for the assigned scope**. A running delegate, unchanged receipt, or rearmed timer alone is not a healthy-work verdict.

- Take one bounded census of the exact delegate and its owned command handles/PIDs (including zombie/exit state). Compare durable checkpoints, build/test log milestones, artifact timestamps, or commits with the previous check-in; do not inspect native-child transcripts. CPU/I/O can support a diagnosis but low utilization alone does not prove a stall.
- Separate preparation, active execution, external waiting, retries, and result collection. Compare the current phase with task complexity and prior measured runs; do not invent an ETA or treat a small pin/edit task's long preparation as compilation time.
- Classify `progressing`, `waiting_external`, `suspected_stall`, or `unknown`, naming the evidence and last verified progress. Missing/stale evidence requires a bounded diagnostic or progress request, not another unsupported “still working normally.” An exited command whose result was not consumed is a collection failure: reconcile that exact result before rerunning.
- If time is disproportionate or successive checkpoints do not advance, question the strategy and narrow the next action. When permitted, steer the existing writer toward the concrete blocker or request a bounded handoff; never duplicate writers, blindly repeat full gates, kill work merely for elapsed time, or relax verification.
- Respect restart/pause boundaries: if the user forbids steering or new work, perform read-only checks and report the concern, but let existing tasks finish naturally. Do not launch replacement agents, commits/hooks, or new long work. State restart readiness only after owned non-durable work has ended; distinguish verified nohup/CSA survivors from parent-bound work.

## Check-in receipt

Emit a compact YAML receipt. For countable jobs, all progress fields are required; do not invent an ETA if no checkpoint/counter exists.

```yaml
wd:
  primary: <managed-handle-or-pid>
  state: live | zombie | exited
  ttl:
    provider: <active-provider>
    seconds: <live-resolved-int>
  progress:
    completed: <n | unavailable>
    total: <n | unavailable>
    rate_per_s: <number | unavailable>
    eta_s: <number | unavailable>
  health: <progressing | waiting_external | suspected_stall | unknown; supporting signal>
  proportionality: <phase, elapsed versus task scope, and reasoned assessment>
  evidence: <change since prior check-in and last verified progress>
  next: rearm | reconcile-completion | escalate
```

For a benchmark, the harness must expose a durable per-wave checkpoint (completed/total plus elapsed time). A live PID or open socket alone is not progress evidence.

## Resolver

`scripts/resolve-checkin.sh` maps the active provider to a CSA key and prints exactly one validated TTL. Re-run it at every arm; the parent runtime may change mid-session. Hermes `localrouter` is a first-class key (`kv_cache.provider_ttls.localrouter`, currently 1500) with grok as lookup fallback.

## Workload budgets

Before launching a long task, size retry count, request/unit timeout, and any output-token budget for the real worst-case workload—not for a quick-looking green result. Retry only classified transient failures with bounded exponential backoff; persist attempts and terminal errors. A configured output budget must be large enough for the task's meaningful completion and is part of the recorded configuration. For benchmark-specific checkpointing, hot reload, and these policies, load `resumable-benchmark-jobs`.

## Benchmark route

For a benchmark, batch evaluation, load test, or any job that needs durable progress/ETA and resume, load `resumable-benchmark-jobs` before designing or launching it.

## Boundaries

- A relay schedules a **parent** check-in; the timer itself proves neither a provider request nor cache warmth. Do not claim measured cache savings without usage telemetry.
- Process a newly delivered primary completion immediately, including an out-of-band completion attached to a relay tool result; never wait for the next heartbeat or report the superseded running snapshot.
- Unknown progress stays unavailable: directory size and a missing manifest do not prove downloading, verification, or completion phases.
- A Hermes worktree is about 1.5G. Push the commit to the fork, read back the SHA, then `git worktree remove` that directory before the next dispatch. Do not accumulate finished worktrees under `~/.hermes/worktrees/`. Before spawning a writer, delete worktrees that are no longer needed. Never delete the live checkout or a worktree a live process is using.
- Do not inspect native-child transcripts. Use immutable artifacts, process state, and durable side effects.
