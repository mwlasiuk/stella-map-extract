import msgpack
import json

with open('map.map', 'rb') as map_file:
    for i, unpacker in enumerate(msgpack.Unpacker(map_file)):
        with open(f'unpacker-{i}.json', 'w') as unpacker_file:
            unpacker_file.write(json.dumps(unpacker, indent=2))
