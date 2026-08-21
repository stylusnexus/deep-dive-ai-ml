#!/usr/bin/env bash
# Confirms the host and container sides are both usable before a block starts.
set -uo pipefail
ok(){ printf "  ✅ %s\n" "$1"; }; bad(){ printf "  ❌ %s\n" "$1"; }
warn(){ printf "  ⚠️  %s\n" "$1"; }

echo "── Host (training runs here — MPS, 128GB unified memory)"
python3 - <<'PY' 2>/dev/null || echo "  ❌ python3 not usable"
import sys, importlib
print(f"  ✅ python {sys.version.split()[0]}")
try:
    import torch
    dev = "MPS" if torch.backends.mps.is_available() else "CPU only"
    print(f"  ✅ torch {torch.__version__} ({dev})")
except ImportError:
    print("  ❌ torch missing on host")
PY

echo "── Docker"
if docker info >/dev/null 2>&1; then
  mem=$(docker info --format '{{.MemTotal}}')
  gb=$(( mem / 1073741824 ))
  ok "docker running ($(docker --version | cut -d, -f1))"
  if [ "$gb" -lt 32 ]; then
    warn "Docker VM memory ${gb}GB — raise to 48-64GB before Blocks 7-8 (Settings → Resources)"
  else
    ok "Docker VM memory ${gb}GB"
  fi
else
  bad "docker not running"
fi

echo "── Hugging Face"
if command -v hf >/dev/null 2>&1; then
  who=$(hf auth whoami 2>/dev/null | head -1)
  [ -n "$who" ] && ok "hf authenticated as ${who}" || bad "hf not authenticated — run: hf auth login"
else
  bad "hf CLI missing — pip install huggingface_hub[cli]"
fi

echo "── API keys"
for k in ANTHROPIC_API_KEY OPENAI_API_KEY; do
  [ -n "${!k:-}" ] && ok "$k set" || warn "$k not set (needed from Block 3)"
done
