# agent-skills

Public copies of two agent skills.

| Directory | License | What it is |
|---|---|---|
| [`wd/`](wd/) | Apache-2.0 | Supervise long tasks with dynamic, evidence-bearing check-ins. |
| [`dumbpipe/`](dumbpipe/) | See notice below | Install, configure, and troubleshoot [dumbpipe](https://github.com/n0-computer/dumbpipe) encrypted forwarding. |

The repository, including `wd/`, is Apache License 2.0. Copyright (c) 2026 obj. See [NOTICE](NOTICE).

## Install

Copy one directory into your agent skill path:

```bash
cp -a wd "$HOME/.hermes/skills/software-development/wd"
cp -a dumbpipe "$HOME/.hermes/skills/devops/dumbpipe"
```

The installed skill name is `dumbpipe`, not `dumupipe`. Load `wd` or `dumbpipe` from the agent that consumes these files. Do not commit tickets, `IROH_SECRET` values, or host-specific unit files into this repository.
