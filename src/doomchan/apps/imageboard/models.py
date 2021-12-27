import os
import secrets

from django.db import models
from django.utils.translation import gettext_lazy as _

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Board(models.Model):
    verbose_name = models.CharField(
        max_length=20,
        help_text=_('Board verbose name.')
    )
    slug = models.SlugField(
        unique=True,
        primary_key=True,
        db_index=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.slug} : ({", ".join([str(thread.pk) for thread in self.threads.all()])})'
    
    

class Post(models.Model):
    ip = models.GenericIPAddressField(editable=False)

    name = models.CharField(
        default=_('Anonymous'),
        max_length=14,
        help_text=_('User name. 14 chars')
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True
    )

    objects = models.Manager()
    active = ActiveManager()


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # save the token in memory
        # there is no need to waste time saving a temp token
        # in the DB
        self.password = secrets.token_bytes()
        return super().save(*args, **kwargs)
   
    class Meta:
       abstract = True

class Thread(Post):
    title = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text=_('Thread title.')
    )
    board = models.ForeignKey(
        Board,
        related_name='threads',
        on_delete=models.CASCADE
    )

    image = models.ImageField(blank=True, default="static/no_image.jpeg")

    text = models.TextField(
        max_length=4000,
        help_text='OP text. Max 4K chars.'
    )

    def __str__(self):
        unique_posters = len(self.unique_posters_ips(self.comments))
        posters_str = f'by {unique_posters} posters.'

        # notice how we also count inactive comments here
        return f'{self.title} on {self.board}, id: {self.pk}. ' \
               f'{self.comments.count()} comments so far ' \
               f'{posters_str if unique_posters else "."}'
    def __repr__(self):
        return f'{self.title} ({self.pk}, {self.board})'

    # get unique ips
    def unique_posters_ips(self, comments):
        unique_ips = set(comment.ip for comment in comments.filter(is_active=True))
        return unique_ips

class Comment(Post):
    thread = models.ForeignKey(
        Thread,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    comment = models.TextField(
        max_length=2000,
        blank=True,
        help_text=_('Comment. 2K chars.')
    )
    
    image = models.ImageField(blank=True)

    def __str__(self):
        values = [str(self.name), self.ip, self.comment[:30]]
        return ", ".join(values)
    
    def __repr__(self):
        return ", ".join([self.name, self.ip, self.comment[:30]])
