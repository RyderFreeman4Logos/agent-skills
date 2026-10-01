#!/bin/sh
set -eu

provider=${ACTIVE_PROVIDER:?ACTIVE_PROVIDER is required}
keys=$provider
case "$provider" in
  openai-codex) keys="$keys codex openai" ;;
  openai*) keys="$keys openai" ;;
  gpt*) keys="$keys openai" ;;
  deepseek*) keys="$keys deepseek" ;;
  grok*|xai*) keys="$keys grok" ;;
  localrouter) keys="$keys localrouter grok" ;;
  pm) keys="$keys openai gpt" ;;
  *) printf 'unsupported active provider: %s\n' "$provider" >&2; exit 2 ;;
esac

for key in $keys; do
  ttl=$(csa config get --global "kv_cache.provider_ttls.${key}" 2>/dev/null || true)
  if [ -z "$ttl" ]; then
    ttl=$(csa config get "kv_cache.provider_ttls.${key}" 2>/dev/null || true)
  fi
  case "$ttl" in
    '') continue ;;
    *[!0-9]*) printf 'invalid TTL for provider key %s: %s\n' "$key" "$ttl" >&2; exit 2 ;;
  esac
  [ "$ttl" -gt 0 ] || { printf 'non-positive TTL for provider key %s\n' "$key" >&2; exit 2; }
  printf '%s\n' "$ttl"
  exit 0
done

printf 'no configured KV-cache TTL for active provider %s (tried: %s)\n' "$provider" "$keys" >&2
exit 2
