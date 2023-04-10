import redis

# Conectarse a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Revisar keys en Redis
keys = r.keys()
print(f'Keys en Redis: {keys}')

# Obtener un valor en particular
valor = r.get('mi_key')
print(f'Valor de mi_key en Redis: {valor}')

# Obtener todos los valores en Redis
all_values = [valor.decode('utf-8') for valor in r.mget(keys)]
print(f'Todos los valores en Redis: {all_values}')
