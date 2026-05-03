#!/bin/bash
cd "/Users/gpichkhadze/New app/Dashboard"
export DEBANK_WALLET="0xe16be042f9433779909a972669be3a2003956348"
export SOL_WALLET="6QcRFrTcHCZgKdtX83iusXVBvcz3vrwiKayREZtJBx5o"
python3 outputs/refresh_positions.py >> /tmp/defi_refresh.log 2>&1
cp docs/index.html index.html
cp docs/history.html history.html
git add docs/index.html docs/history.html index.html history.html outputs/snapshots/ outputs/debank_positions_log.xlsx
git diff --staged --quiet || git commit -m "refresh: $(date -u '+%Y-%m-%d %H:%M UTC')"
git push origin main >> /tmp/defi_refresh.log 2>&1
