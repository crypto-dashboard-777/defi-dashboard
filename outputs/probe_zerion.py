"""Probe Zerion API to understand position grouping for our wallet."""
import urllib.request, base64, json, sys

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

try:
    data = fetch(f"https://api.zerion.io/v1/wallets/{WALLET}/positions/?currency=usd&filter[trash]=only_non_trash&page[size]=100")
    positions = data.get("data", [])
    print(f"Got {len(positions)} positions")

    if positions:
        first = positions[0]
        print("\n--- Sample position id:", first.get("id"))
        print("--- Sample attributes ---")
        print(json.dumps(first.get("attributes", {}), indent=2)[:2500])

    # Aggregate by various grouping signals
    type_counts, proto_counts, group_ids, no_group = {}, {}, set(), 0
    for p in positions:
        a = p.get("attributes", {})
        pt = a.get("position_type")
        type_counts[pt] = type_counts.get(pt, 0) + 1
        proto = (a.get("application_metadata") or {}).get("name")
        proto_counts[proto] = proto_counts.get(proto, 0) + 1
        gid = a.get("group_id")
        if gid:
            group_ids.add(gid)
        else:
            no_group += 1

    print("\n=== position_type counts ===")
    print(type_counts)
    print("=== Protocols ===")
    print(proto_counts)
    print(f"=== group_ids: {len(group_ids)} distinct | positions without group: {no_group}")
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code, e.reason)
    print(e.read().decode()[:500])
except Exception as e:
    import traceback; traceback.print_exc()
