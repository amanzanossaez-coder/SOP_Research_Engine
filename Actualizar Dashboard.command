#!/bin/zsh
# RE-DASH.1.10 -- manual, one-click regeneration. Double-click this
# file in Finder whenever you want to refresh outputs/dashboard.html
# from the current data/raw/ files.
#
# Replaces the RE-DASH.1.8/1.9 background-launchd approach, which
# failed twice against a real macOS restriction on background
# processes opening files inside iCloud Drive -- confirmed not fixable
# from a script (an interactive run of the exact same file worked
# every time; forcing full iCloud download did not fix the background
# case). This file runs interactively -- the same context that already
# worked -- so it does not hit that restriction.

cd "$(dirname "$0")"

echo "Actualizando el dashboard..."
echo ""

python3 generate_dashboard.py

echo ""
echo "Listo. outputs/dashboard.html actualizado."
echo ""
read "?Pulsa Enter para cerrar esta ventana..."
