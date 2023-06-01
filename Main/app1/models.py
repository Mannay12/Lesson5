from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from PIL import Image
from autoslug import AutoSlugField


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    slug = AutoSlugField(populate_from='title', max_length=255, unique=True, db_index=True, verbose_name="URL")
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, blank=True, verbose_name="Фото")
    content = models.TextField(verbose_name="Текст статьи")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор статьи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комментарии'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='users/%Y/%m/%d/')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('profile', args=[self.username])

    def __str__(self):
        return f"Profile of {self.user.username}"

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
