import networkx as nx
import matplotlib.pyplot as plt
import asyncio
from modules.db import get_pool

async def visualize(path: str = 'accounts_graph.png'):
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT login, kyc_status, campaign_id FROM accounts')
    G = nx.DiGraph()
    color_map = {'OK':'green','FAIL':'red',None:'gray'}
    for r in rows:
        G.add_node(r['login'], color=color_map.get(r['kyc_status'], 'gray'))
    plt.figure(figsize=(10,10))
    colors = [data['color'] for _, data in G.nodes(data=True)]
    nx.draw(G, node_color=colors, with_labels=True)
    plt.savefig(path)