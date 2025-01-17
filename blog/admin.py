from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'created_date')
    search_fields = ('title', 'text', 'author')


# admin.site.register(PostAdmin)
