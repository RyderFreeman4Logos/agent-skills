# agent-skills

Public copies of agent skills.

| Directory | License | What it is |
|---|---|---|
| [`wd/`](wd/) | Apache-2.0 | Existing WD copy; prefer the portable `skills/wd/` version below. |
| [`skills/wd/`](skills/wd/) | Apache-2.0 | Supervise long tasks with dynamic, evidence-bearing check-ins using `skillcfg`. |
| [`skills/skillcfg/`](skills/skillcfg/) | Apache-2.0 | Read and validate skill configuration with the `skillcfg` CLI. |
| [`dumbpipe/`](dumbpipe/) | See notice below | Install, configure, and troubleshoot [dumbpipe](https://github.com/n0-computer/dumbpipe) encrypted forwarding. |

The repository, including `wd/`, is Apache License 2.0. Copyright (c) 2026 obj. See [NOTICE](NOTICE).

## Install

Copy one directory into your agent skill path:

```bash
cp -a skills/wd "$HOME/.hermes/skills/software-development/wd"
cp -a skills/skillcfg "$HOME/.hermes/skills/software-development/skillcfg"
cp -a dumbpipe "$HOME/.hermes/skills/devops/dumbpipe"
```

The installed skill name is `dumbpipe`, not `dumupipe`. Load `wd`, `skillcfg`, or `dumbpipe` from the agent that consumes these files. Do not commit tickets, `IROH_SECRET` values, or host-specific unit files into this repository.
