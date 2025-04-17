import csv, random, requests
from time import sleep

PROXIES = []

def load_proxies(path='proxies.csv'):
    global PROXIES
    with open(path) as f:
        PROXIES = list(csv.DictReader(f))

load_proxies()


def assign_proxy(account: dict) -> dict:
    # фильтруем по geo
    pool = [p for p in PROXIES if p['geo']==account['geo']]
    for p in random.sample(pool, len(pool)):
        # health check
        try:
            resp = requests.get('https://facebook.com/ping', proxies={
                'http': f"http://{p['host']}:{p['port']}",
            }, timeout=5)
            if resp.status_code==200:
                account['proxy'] = f"http://{p['host']}:{p['port']}"
                return account
        except:
            sleep(1)
    raise RuntimeError('No healthy proxy for ' + account['geo'])