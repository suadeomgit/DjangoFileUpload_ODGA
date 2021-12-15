import os
# from random import Random
import random
from django.http import HttpResponse


def read_media(request):
    k = [x for x in os.listdir('media/mp3') if x[0]=='_'][0][7:]
    media_path = 'media/mp3/'+k
    l = os.listdir(media_path)
    i = len(l)
    i = random.randint(a=0, b=i-1)
    print(os.listdir(media_path)[i])
    with open(media_path+'/'+os.listdir(media_path)[i], 'rb') as f:
        file_content = f.read()

    print(i, '<<<<<<<<<<i')
    print(i, '<<<<<<<<<<i')
    print(i, '<<<<<<<<<<i')
    print(i, '<<<<<<<<<<i')
    return HttpResponse(file_content, content_type='audio/mpeg')
