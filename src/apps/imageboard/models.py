from django.db import models
from django.utils.translation import gettext_lazy as _
import os

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
        a= [str(thread.pk) for thread in self.threads.all()]
        return f'{self.slug} : ({", ".join(a)})'
    
    

class Thread(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text=_('Thread title.')
    )
    image = models.ImageField(blank=True)
    board = models.ForeignKey(
        Board,
        related_name='threads',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        max_length=4000,
        help_text='OP text. Max 4K chars.'
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        unique_posters = len(self.unique_posters(self.comments))
        posters_str = f'by {unique_posters} posters.'

        # notice how we also count inactive comments here
        return f'{self.title} on {self.board}, id: {self.pk}. ' \
               f'{self.comments.count()} comments so far ' \
               f'{posters_str if unique_posters else "."}'
    def __repr__(self):
        return f'{self.title} ({self.pk}, {self.board})'

    # get unique ips
    def unique_posters_ips(self, comments):
        unique_ips = set(comment.ip for comment in comments.filter(active=True))
        return unique_ips
    
    def save(self, *args, **kwargs):
        # self.file.path is read-only, so we use self.image.name
        # to asign the file to the correct folder.
        # See https://code.djangoproject.com/ticket/15590
        image_name = self.image.name.split('/')
        image_name.insert(-1, self.board.slug)
        self.image.name = "/".join(image_name)
        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # we need to delete the file as well as the reference
        # (TODO) But it should be archived before permanent deletion
        # maybe using a task that runs at a certain time every day, 
        # perma deleting old images.
        os.remove(self.image.path)
        return super().delete(*args, **kwargs)

class Comment(models.Model):
    name = models.CharField(
        default=_('Anonymous'),
        max_length=14,
        help_text=_('User name. 14 chars')
    )
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
    ip = models.GenericIPAddressField()
    active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return ", ".join([self.name, self.ip, self.comment[:30]])

    def save(self, *args, **kwargs):
        image_name = self.image.name.split('/')
        image_name.insert(-1, self.thread.board.slug)
        image_name.insert(-1, str(self.thread.pk))
        self.image.name = "/".join(image_name)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        os.remove(self.image.path)
        return super().delete(*args, **kwargs)
