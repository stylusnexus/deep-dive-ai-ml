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
  # MemTotal is what the VM has RIGHT NOW, which can sit below the configured
  # ceiling after a restart. Report the configured value too before warning.
  cfg=$(python3 -c "
import json,pathlib
for n in ('settings-store.json','settings.json'):
    p=pathlib.Path.home()/'Library/Group Containers/group.com.docker'/n
    if p.exists():
        print(int(json.loads(p.read_text()).get('MemoryMiB',0))//1024); break
else: print(0)" 2>/dev/null || echo 0)
  if [ "${cfg:-0}" -gt 0 ]; then
    ok "Docker memory ${gb}GB live / ${cfg}GB configured"
    [ "$cfg" -lt 16 ] && warn "configured ceiling ${cfg}GB is low — raise in Settings → Resources"
  else
    ok "Docker VM memory ${gb}GB live"
  fi
  # Model serving happens on the host via Ollama/MPS, not in a container —
  # Docker on macOS is CPU-only, so container RAM is not the constraint people assume.
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
