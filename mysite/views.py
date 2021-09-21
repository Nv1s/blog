from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'mysite/post/list.html'


""" Первый обработчик. Запрашиваем из базы данных
 все опубликованные статьи с помощью published """


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 статьи на страницу
    page = request.GET.get('page')  # Получаем текущую страницу
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:  # Если страница не целое число
        posts = paginator.page(1)  # Возвращаем первую страницу
    except EmptyPage:  # Если номер страницы больше общего кол-ва страниц
        posts = paginator.page(paginator.num_pages)  # Возвращаем последнюю страницу
    return render(request, 'mysite/post/list.html', {'page': page, 'posts': posts})


"""Обработчик страницы статьи"""


def post_detail(requset, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)
    return render(requset, 'mysite/post/detail.html', {'post': post})


def post_share(request, post_id):

    # Получение статьи по идентификатору
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':

        # Форма была отправлена на сохранение
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "' \
                      '{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:' \
                      '{}'.format(post.title, post_url,  cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'mysite/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})
