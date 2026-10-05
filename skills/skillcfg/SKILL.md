---
name: skillcfg
license: Apache-2.0
description: "Use when reading or validating skill runtime preferences with skillcfg; explain config selection, command help, and output safely."
metadata:
  version: 1.0.0
  author: obj
  short-description: "Read shared runtime preferences with skillcfg"
  hermes:
    tags: [configuration, skills, cli, runtime-preferences]
    related_skills: [wd]
---

# skillcfg

Use `skillcfg` for shared, typed runtime preferences instead of embedding per-skill settings. This guide matches the CLI help; `skillcfg -h` and every command's `-h` / `--help` work without loading a config or HOME.

## Config selection and format

The global option must precede the command: `skillcfg --config PATH get KEY`. Selection precedence is `--config`, `SKILLCFG_CONFIG`, `$XDG_CONFIG_HOME/skillcfg/config.toml`, then `$HOME/.config/skillcfg/config.toml`. Unset variables fall through; a selected empty `SKILLCFG_CONFIG` or `XDG_CONFIG_HOME` is an error. Selected files must be regular UTF-8 TOML with integer `schema_version = 1` (symlinks to regular files are followed).

```toml
schema_version = 1

[kv_cache.provider_ttls]
openai = 900
localrouter = 1200
```

Set `SKILLCFG_CONFIG=/path/to/config.toml` for scripts that invoke `skillcfg` themselves. Do not put credentials in skill settings or print sensitive values. `get` and `explain` intentionally display the requested key; only query a value you are permitted to reveal.

A key is a literal dotted path: each non-empty segment allows ASCII letters, digits, `_`, and `-`. Dots always separate table segments; quoting, escaping dots, and Unicode segments are unsupported.

## Commands

- `skillcfg get KEY` — print one value. Strings are raw (including existing newlines); other values use TOML text. A newline is added only if the output lacks one. Requires a selected config.
- `skillcfg get-many KEY... [--format kv|json]` — resolve distinct keys before output; duplicate keys fail. Default `kv` preserves input order and prints `key=value` pairs (ambiguous strings are JSON-quoted; arrays/tables use compact JSON). `json` prints a compact object; TOML date/time values become strings. Treat `kv` as data, never `eval` it. Requires a config.
- `skillcfg show-skill NAME [--all] [--format kv|json] [--root PATH]...` — resolve discovered skill bindings, sorted by alias; defaults to visible bindings, and `--all` includes opaque bindings. Default `kv` prints `alias=value` pairs (ambiguous strings are JSON-quoted; arrays/tables use compact JSON); `json` prints a compact object with TOML date/time values as strings. Requires a config and a discovered skill.
- `skillcfg discover [--root PATH]... [--verbose]` — print discovered names, sorted by name then canonical directory, one per line. `--verbose` adds resolved paths, exposures, and metadata. Without configured `discovery.roots`, it searches `$HOME/.codex/skills`, `.hermes/skills`, `.claude/skills`, and `.agents/skills`; missing conventional roots are skipped, but missing explicit roots fail. If neither `--config` nor `SKILLCFG_CONFIG` is set, an absent conventional XDG/HOME config file does not prevent discovery; `HOME` is required when XDG is unset. Repeated `--root` values replace configured roots. Discovery diagnostics go to stderr.
- `skillcfg validate [--root PATH]... [--strict]` — validate the config, discovered skills, manifests, and scripts; success prints `ok`. Warnings are non-fatal unless `--strict`; repeated roots replace configured roots. Requires a config.
- `skillcfg validate-skill PATH [--strict]` — validate one skill directory with a readable `SKILL.md`, without traversing configured roots; success prints `ok`. Requires a config.
- `skillcfg explain KEY [--root PATH]...` — display the requested value, config source paths, and known skill references. This prints the requested value; use only for values safe to disclose. Requires a config.

For any command, `--root PATH` is repeatable where listed. `--format` accepts only `kv` or `json` and may appear once. Help is handled before config access. Usage errors exit 2; config, lookup, discovery, and validation failures exit 1. Validation/discovery diagnostics are on stderr; normal results are on stdout.

## Examples

```sh
skillcfg get kv_cache.provider_ttls.openai
skillcfg get-many kv_cache.provider_ttls.openai kv_cache.provider_ttls.localrouter --format json
skillcfg discover --root ./skills --verbose
skillcfg validate --root ./skills --strict
skillcfg validate-skill ./skills/my-skill
skillcfg explain kv_cache.provider_ttls.openai --root ./skills
```

Use the runtime config-path precedence rather than hard-coding a machine-specific file path. For an isolated test or one-off config, set `SKILLCFG_CONFIG` or put `--config PATH` before the subcommand.
