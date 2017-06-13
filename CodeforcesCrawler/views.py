from django.shortcuts import render
import redis
from redis import RedisError
from django.views.defaults import server_error
from .forms import TagForm, DifficultyForm

# Create your views here.

def change(s1):
    if s1[0] == '1':
        return '3' + s1[1]
    return s1

def tags_view(request):
    try:
        conn = redis.Redis(port=6380)
        conn.ping()
    except RedisError:
        try:
            conn = redis.Redis()
            conn.ping()
        except RedisError:
            return server_error(request)

    if request.method == 'POST':
        form = TagForm(conn, request.POST)
        if form.is_valid():
            tag = form.cleaned_data['tags']
            tasks = []
            for url in conn.smembers(tag):
                dct = conn.hgetall(url)
                task = {
                    'url': url,
                    'name': dct[b'name'].decode('utf-8'),
                    'difficulty': dct[b'difficulty'].decode('utf-8')
                }
                tasks.append(task)
            headers = ['Link to problem', 'Name', 'Difficulty']
            tasks = sorted(tasks, key=lambda x: change(x['difficulty']))
            return render(request, 'tags.html', {
                'form': form,
                'tasks': tasks,
                'headers': headers
            })
    else:
        form = TagForm(conn)
    return render(request, 'tags.html', {'form':form})


def difficulties_view(request):
    try:
        conn = redis.Redis(port=6380)
        conn.ping()
    except RedisError:
        try:
            conn = redis.Redis()
            conn.ping()
        except RedisError:
            return server_error(request)

    if request.method == 'POST':
        form = DifficultyForm(conn, request.POST)
        if form.is_valid():
            diff = form.cleaned_data['difficulty']
            tasks = []
            for url in conn.smembers(diff):
                dct = conn.hgetall(url)
                task = {
                    'url': url,
                    'name': dct[b'name'].decode('utf-8'),
                }
                tasks.append(task)
            headers = ['Link to problem', 'Name']
            return render(request, 'tags.html', {
                'form': form,
                'tasks': tasks,
                'headers': headers
            })
    else:
        form = DifficultyForm(conn)
    return render(request, 'tags.html', {'form':form})


