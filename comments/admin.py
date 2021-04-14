from django.contrib import admin
from .models import Comment

# class CommentAdmin(admin.ModelAdmin):
# 	prepopulated_fields = {'slug': ('content', )}

# Register your models here.
admin.site.register(Comment)