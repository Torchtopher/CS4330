import redis
import json
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
'''
    “panda”  - “bamboo”
    “eel” - “seaweed”
    “mako” - 12
    7 - “banana”
    10 - 4
    “animals” - [“panda”,”lemming”,”sheep”]
    “user1” - “{ name: Sea, age: 3542, birthday: 1/32/-1500 }”
'''

r.set('panda', 'bamboo')
r.set('eel', 'seaweed')
r.set('mako', 12)
r.set(7, 'banana')
r.set(10, 4)
# could clear the list first or it will keep getting appended
#r.delete('animals')
r.lpush('animals', *["panda", "lemming", "sheep"])
r.hset('user1', mapping={
    'name': 'Sea',
    "age": '3542',
    "birthday": '1/32/-1500'
})

print(r.get('panda'))
print(r.get('eel'))
print(r.get('mako'))
print(r.get(7))
print(r.get(10))
print(r.lrange('animals', 0, -1))
print(r.hgetall('user1'))