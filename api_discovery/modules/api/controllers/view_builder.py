import json


def build_discovery_items(items):
    d_items = []
    for item in items:
        d_items.append({
            'name': item['name'].split('.')[0],
            'title': item['title'],
            'description': item['description'],
            'id': str(item['_id'])
        })
    return {'schemas': d_items}


def build_discovery_item(item):
    return {'schema': {
        'name': item['name'].split('.')[0],
        'title': item['title'],
        'description': item['description'],
        'id': str(item['_id']),
        'schema': json.loads(item['schema'])
    }}
