#!/bin/bash
cd "/Users/gpichkhadze/New app/Dashboard"
export DEBANK_WALLET="0xe16be042f9433779909a972669be3a2003956348"
export SOL_WALLET="36RwE5mMFqZhkMrC445AYXSQpj8xDtRLC3QfnNx18e1F"
export OFFCHAIN_USD=0
python3 outputs/refresh_positions.py >> /tmp/defi_refresh.log 2>&1
cp docs/index.html index.html
cp docs/history.html history.html
git add docs/index.html docs/history.html index.html history.html outputs/snapshots/ outputs/debank_positions_log.xlsx
git diff --staged --quiet || git commit -m "refresh: $(date -u '+%Y-%m-%d %H:%M UTC')"

# Push with divergence handling: GitHub Actions also commits to main every 6h.
# Snapshots never conflict (unique filenames); generated HTML/xlsx conflicts
# are resolved in favor of local (freshest data) via merge -X ours.
for attempt in 1 2; do
  git push origin main >> /tmp/defi_refresh.log 2>&1 && break
  git fetch origin main >> /tmp/defi_refresh.log 2>&1
  git merge -X ours --no-edit origin/main >> /tmp/defi_refresh.log 2>&1 || git merge --abort
done
