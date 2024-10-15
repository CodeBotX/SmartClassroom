from django.contrib import admin
from .models import Category, Document

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'uploaded_at', 'category')
    search_fields = ('title', 'author__username', 'category__name')
    list_filter = ('category', 'author')
    ordering = ('-uploaded_at',)
    prepopulated_fields = {'title': ('title',)}  # Tự động điền tiêu đề nếu cần

    def author_username(self, obj):
        return obj.author.username
    author_username.short_description = 'Author'
