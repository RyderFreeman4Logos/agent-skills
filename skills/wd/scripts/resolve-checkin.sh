#!/bin/sh
set -eu

provider=${ACTIVE_PROVIDER:?ACTIVE_PROVIDER is required}
if ! command -v skillcfg >/dev/null 2>&1; then
  printf 'skillcfg executable not found on PATH\n' >&2
  exit 127
fi

case "$provider" in
  openai-codex) set -- "$provider" codex openai ;;
  openai*) set -- "$provider" openai ;;
  gpt*) set -- "$provider" openai ;;
  deepseek*) set -- "$provider" deepseek ;;
  grok*|xai*) set -- "$provider" grok ;;
  localrouter) set -- "$provider" grok ;;
  pm) set -- "$provider" openai gpt ;;
  *) printf 'unsupported active provider: %s\n' "$provider" >&2; exit 2 ;;
esac

if ! config_version=$(skillcfg get schema_version 2>/dev/null) || [ "$config_version" != 1 ]; then
  printf 'skillcfg could not load its selected schema_version=1 configuration\n' >&2
  exit 2
fi

for key do
  if ttl=$(skillcfg get "kv_cache.provider_ttls.$key" 2>/dev/null); then
    case "$ttl" in
      '') continue ;;
      *[!0-9]*) printf 'invalid TTL for provider key %s: expected decimal digits\n' "$key" >&2; exit 2 ;;
    esac
    positive=$ttl
    while [ "${positive#0}" != "$positive" ]; do
      positive=${positive#0}
    done
    [ -n "$positive" ] || { printf 'non-positive TTL for provider key %s\n' "$key" >&2; exit 2; }
    printf '%s\n' "$ttl"
    exit 0
  fi
done

printf 'no configured KV-cache TTL for active provider %s (tried: %s)\n' "$provider" "$*" >&2
exit 2
