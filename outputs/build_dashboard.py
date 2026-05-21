import json, pathlib

snap_path = pathlib.Path('/sessions/vibrant-friendly-johnson/mnt/outputs/snapshots/latest.compact.json')
snap = snap_path.read_text()
# Sanitize for inline JSON-in-script: escape </ to prevent script tag escape
snap_safe = snap.replace('</', '<\\/')

template = pathlib.Path('/sessions/vibrant-friendly-johnson/mnt/outputs/dashboard_template.html')
out = pathlib.Path('/sessions/vibrant-friendly-johnson/mnt/outputs/dashboard_built.html')

html = template.read_text().replace('__SNAPSHOT_JSON__', snap_safe)
out.write_text(html)
print(f'Wrote {len(html)} bytes to {out}')
