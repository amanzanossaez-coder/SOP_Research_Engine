#!/bin/zsh
# RE-DASH.1.8 -- deterministic wrapper for reactive dashboard
# regeneration. Called by launchd (see
# com.armando.sop-dashboard-regen.plist, WatchPaths on data/raw/)
# whenever a source file changes. Contains no logic of its own beyond
# locating the repo and calling the existing, already-verified
# generate_dashboard.py -- that script stays the single source of
# truth for how the dashboard is built; this file never duplicates or
# reimplements any of it.

REPO_DIR="/Users/armando/Library/Mobile Documents/com~apple~CloudDocs/12. FINANZAS/11. SOP/SOP_Research_Engine"
LOG_DIR="$REPO_DIR/logs"
LOG_FILE="$LOG_DIR/dashboard_regen.log"

mkdir -p "$LOG_DIR"
cd "$REPO_DIR" || exit 1

{
  echo "----- $(date '+%Y-%m-%d %H:%M:%S') -----"
  python3 generate_dashboard.py
  echo "outputs/dashboard.html actualizado."
  echo ""
} >> "$LOG_FILE" 2>&1
