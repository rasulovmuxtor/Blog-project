from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.contrib import admin
from .models import Post,Comment,Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude=('publish_at','created_at','last_updated','author','views')
    list_display=['title','author','publish_at','status','views']
    list_filter=['status','created_at','publish_at','category','author']
    search_fields=['title','body']
    prepopulated_fields={'slug':('title',)}
    date_hierarchy='publish_at'
    ordering=['status','publish_at']
    def save_model(self, request, instance, form, change):
        instance = form.save(commit=False)
        instance.author = request.user 
        instance.save()
        form.save_m2m()
        return instance

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','posts']
    prepopulated_fields={'slug':('name',)}

    def posts(self,obj):
        count=obj.posts.count()
        url=(
            reverse('admin:blog_post_changelist')
            +"?"
            +urlencode({"category__id": f"{obj.id}"})
        )
        return format_html(f"<a href='{url}'>{count} </a>")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('name','email','post','created_at')
    list_filter=('created_at','post')
    search_fields=('name','email','body')