#!/usr/bin/env bash
#
# hello.sh - the first script from the "Files and Permissions" demo.
#
# This file is committed without the execute permission on purpose, so you can
# repeat the demo. The first run fails with "Permission denied":
#   ./scripts/hello.sh
# Give it the execute permission, then run it again:
#   chmod +x scripts/hello.sh
#   ./scripts/hello.sh

set -euo pipefail

echo "Hello from the Pi!"
