#!/usr/bin/env python3
import urllib.request
import json
from datetime import datetime, timezone, timedelta

TOKEN_UUID = "3f8290d9-241e-432a-a9cb-44be4b6a42d2"
URL = f"https://webhook.site/token/{TOKEN_UUID}/requests?sorting=newest"

def main():
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching visitor logs: {e}")
        return

    items = data.get('data', [])
    print(f"\n==========================================================================================")
    print(f"  LIVE VISITOR LOGS (9:00 AM - 12:00 PM IST) - dbmscmd.surge.sh")
    print(f"  Dashboard: https://webhook.site/#!/3f8290d9-241e-432a-a9cb-44be4b6a42d2")
    print(f"==========================================================================================\n")

    if not items:
        print("No visitors recorded yet today.")
        return

    # IST timezone (+05:30)
    ist = timezone(timedelta(hours=5, minutes=30))

    valid_visits = []
    for it in items:
        created_str = it.get('created_at') # '2026-11-12 04:26:33'
        try:
            dt_utc = datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            dt_ist = dt_utc.astimezone(ist)
        except Exception:
            dt_ist = None

        ip = it.get('ip', 'Unknown')
        city = it.get('city') or 'Unknown'
        region = it.get('region') or ''
        country = it.get('country') or ''
        isp = it.get('as_name') or 'Unknown ISP'
        user_agent = it.get('user_agent') or ''
        
        # Parse payload body if available
        body_raw = it.get('content') or ''
        screen = '-'
        platform = '-'
        referrer = '-'
        if body_raw.startswith('{'):
            try:
                b = json.loads(body_raw)
                screen = b.get('screen', '-')
                platform = b.get('platform', '-')
                referrer = b.get('referrer', '-')
            except Exception:
                pass

        valid_visits.append({
            'time_ist': dt_ist.strftime("%I:%M:%S %p") if dt_ist else created_str,
            'ip': ip,
            'loc': f"{city}, {region}".strip(', '),
            'isp': isp,
            'screen': screen,
            'platform': platform,
            'ua': user_agent
        })

    print(f"{'#':<3} | {'Time (IST)':<11} | {'IP Address':<22} | {'Location':<22} | {'Network / ISP':<26} | {'Screen'}")
    print("-" * 110)
    for idx, v in enumerate(valid_visits, 1):
        print(f"{idx:<3} | {v['time_ist']:<11} | {v['ip'][:22]:<22} | {v['loc'][:22]:<22} | {v['isp'][:26]:<26} | {v['screen']}")
    print("-" * 110)
    print(f"Total Visitors Logged: {len(valid_visits)}")
    print(f"\nOpen the live visual dashboard anytime: https://webhook.site/#!/3f8290d9-241e-432a-a9cb-44be4b6a42d2\n")

if __name__ == '__main__':
    main()
