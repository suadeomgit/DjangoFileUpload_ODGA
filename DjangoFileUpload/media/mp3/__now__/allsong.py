import os

fourth = '7'

a = os.listdir('../')
print(a)
for i in a[1:]:
    c = os.listdir(f'../{i}')
    # b = f'\nhttp://192.168.0.{fourth}:8000/media/mp3/{i}/'.join(c)
    b = f'\nhttp://121.127.79.53:8000/media/mp3/{i}/'.join(c)
    print(b)
    # c = f'\nhttp://192.168.0.{fourth}:8000/media/mp3/{i}/'+b
    c = f'\nhttp://121.127.79.53:8000/media/mp3/{i}/'+b
    c = c[1:]
    with open(f'{i}.txt', 'w', encoding='utf8') as f:
        f.write(c)