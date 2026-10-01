# agent-skills

Public copies of two agent skills.

| Directory | License | What it is |
|---|---|---|
| [`wd/`](wd/) | MIT | Supervise long tasks with dynamic, evidence-bearing check-ins. |
| [`dumbpipe/`](dumbpipe/) | See notice below | Install, configure, and troubleshoot [dumbpipe](https://github.com/n0-computer/dumbpipe) encrypted forwarding. |

The repository root is Apache License 2.0. `wd/` keeps its upstream MIT license; see [NOTICE](NOTICE).

## Install

Copy one directory into your agent skill path:

```bash
cp -a wd "$HOME/.hermes/skills/software-development/wd"
cp -a dumbpipe "$HOME/.hermes/skills/devops/dumbpipe"
```

The installed skill name is `dumbpipe`, not `dumupipe`. Load `wd` or `dumbpipe` from the agent that consumes these files. Do not commit tickets, `IROH_SECRET` values, or host-specific unit files into this repository.
