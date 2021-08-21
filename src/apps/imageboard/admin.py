from django.contrib import admin

from .models import Board, Thread, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['thread']
    fields = ['ip', 'comment', 'image', 'is_active']

class ThreadInline(admin.TabularInline):
    model = Thread
    raw_id_fields = ['board']

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    inlines = [ThreadInline]

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
