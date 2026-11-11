#!/usr/bin/env bash
# Kokoro-82M voice model (Apache-2.0, commercial use OK). ~350 MB, not committed.
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p models
pip install --break-system-packages -q kokoro-onnx soundfile numpy pillow playwright
base=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
curl -sSL -o models/kokoro-v1.0.onnx "$base/kokoro-v1.0.onnx"
curl -sSL -o models/voices-v1.0.bin  "$base/voices-v1.0.bin"
echo "models ready"
