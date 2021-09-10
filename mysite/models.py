from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # поле заголовка статьи
    title = models.CharField(max_length=250)

    # поле будет использоваться для формирования URL,
    # unique_for_date формирует уникальные URL, используя дату публикации статей
    slug = models.SlugField(max_length=250, unique_for_date='publish')

    # Поле является внешним ключом, указываем что каждая статья имеет автора
    # on_delete определяет поведение при удалении связанного объекта
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()

    # сохраняет дату публикации статьи
    publish = models.DateTimeField(default=timezone.now())

    # поле указывает, когда была создана статья
    # auto_now_add - дата будет сохранятся автоматически при создании
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        # сортировка по убыванию, об этом говорит "-"
        ordering = ('-publish', )

    """Метод возвращает отображение объекта, понятное человеку"""
    def __str__(self) -> str:
        return self.title
