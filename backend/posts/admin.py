from django.contrib import admin
from .models import Post, PostFile, Comment

class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 1  # Số lượng tệp đính kèm thêm có thể tạo

class PostAdmin(admin.ModelAdmin):
    inlines = [PostFileInline]
    list_display = ('title', 'author', 'created_at', 'get_likes_count')
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    get_likes_count.short_description = 'Likes Count'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
