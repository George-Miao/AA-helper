a = {
   'a': 'b',
   'v': 'd'
}

def b(**kwargs):
   print(kwargs['a'])

print(b.__name__)