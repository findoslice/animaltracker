def messy_boi(jsonfile):
    import json
    from random import randint
    with open(jsonfile, 'r') as f:
        data = json.load(f)
    for key in data:
        for elem in data[key]:
            elem['lat'] = elem['lat'] + randint(-1000,1000)/1000000
            elem['lng'] = elem['lng'] + randint(-1000,1000)/1000000
    with open(jsonfile, 'w') as outfile:
            json.dump(data, outfile)

if __name__ == "__main__":
    messy_boi('database.json')