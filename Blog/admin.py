from django.contrib import admin
from Blog.models import *


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields':  ('title', 'desc', 'content', 'user', 'category', 'tag', )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('click_count', 'is_recommend',),
        }),
    )
    list_display = ('title', 'desc', 'date_publish')


# 富文本编辑器引入js，后面可以尝试其他的富文本编辑器
    class Media:
        js = (
            '/static/js/kindeditor/kindeditor-all.js',
            '/static/js/kindeditor/lang/zh_CN.js',
            '/static/js/kindeditor/config.js',
        )


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)
