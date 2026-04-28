import json
import os

files = [
    'obsidian-config/graph.json',
    '/home/zacmero/Documents/mero-vault/.obsidian-mobile/graph.json'
]

groups = [
    {"query": "path:\"1_ Projects Stack\"", "color": {"a": 1, "rgb": 14701138}}, # Red
    {"query": "path:\"5_ Knowledge_Library\"", "color": {"a": 1, "rgb": 10040319}}, # Purple
    {"query": "path:\"3_ Resources Stack\"", "color": {"a": 1, "rgb": 5025616}}, # Green
    {"query": "path:\"Mero's Diaries\"", "color": {"a": 1, "rgb": 16766720}}, # Gold
    {"query": "path:\"Check Later\"", "color": {"a": 1, "rgb": 16737792}}, # Orange
    {"query": "path:\"4_ Archives\"", "color": {"a": 1, "rgb": 8421504}} # Grey
]

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        data['colorGroups'] = groups
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Updated {filepath}")

