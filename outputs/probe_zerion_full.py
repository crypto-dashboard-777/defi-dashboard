"""Dump Zerion complex positions grouped by group_id."""
import urllib.request, base64, json
from collections import defaultdict

API_KEY = "zk_a890df3625624b23bc1a703808f8d79c"
WALLET = "0xe16be042f9433779909a972669be3a2003956348"
auth = base64.b64encode(f"{API_KEY}:".encode()).decode()
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def fetch(url):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Basic {auth}",
        "accept": "application/json",
        "User-Agent": UA,
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())

url = f"https://api.zerion.io/v1/wallets/{WALLET}/positions/?currency=usd&filter[positions]=only_complex&page[size]=200"
data = fetch(url)
positions = data["data"]
print(f"Fetched {len(positions)} positions\n")

# Group by group_id
groups = defaultdict(list)
ungrouped = []
for p in positions:
    a = p["attributes"]
    gid = a.get("group_id")
    if gid:
        groups[gid].append(p)
    else:
        ungrouped.append(p)

print(f"=== {len(groups)} groups, {len(ungrouped)} ungrouped ===\n")

# Print each group nicely
for gid, members in sorted(groups.items(), key=lambda x: -sum((m["attributes"].get("value") or 0) for m in x[1])):
    proto = members[0]["attributes"].get("protocol")
    chain_rel = members[0].get("relationships", {}).get("chain", {}).get("data", {})
    chain = chain_rel.get("id") if chain_rel else "?"
    deposits = [m for m in members if m["attributes"]["position_type"] == "deposit"]
    loans = [m for m in members if m["attributes"]["position_type"] == "loan"]
    rewards = [m for m in members if m["attributes"]["position_type"] == "reward"]
    locked = [m for m in members if m["attributes"]["position_type"] == "locked"]
    sup = sum((m["attributes"].get("value") or 0) for m in deposits)
    bor = sum((m["attributes"].get("value") or 0) for m in loans)
    rew = sum((m["attributes"].get("value") or 0) for m in rewards)
    lck = sum((m["attributes"].get("value") or 0) for m in locked)
    print(f"--- {proto} on {chain} | group {gid[:12]}…")
    print(f"    {len(members)} legs (D{len(deposits)}/L{len(loans)}/R{len(rewards)}/Lk{len(locked)})  sup=${sup:,.0f}  bor=${bor:,.0f}  rew=${rew:,.0f}  lck=${lck:,.0f}")
    for m in members:
        a = m["attributes"]
        sym = (a.get("fungible_info") or {}).get("symbol", "?")
        print(f"      {a['position_type']:<8} {sym:<28} ${a['value']:>12,.2f}")

print(f"\n=== Ungrouped positions ({len(ungrouped)}) ===")
for m in ungrouped:
    a = m["attributes"]
    sym = (a.get("fungible_info") or {}).get("symbol", "?")
    chain_rel = m.get("relationships", {}).get("chain", {}).get("data", {})
    chain = chain_rel.get("id") if chain_rel else "?"
    print(f"  {a.get('protocol'):<20} {chain:<10} {a['position_type']:<8} {sym:<28} ${a['value']:>12,.2f}")
