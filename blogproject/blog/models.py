from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django_resized import ResizedImageField
from django.utils import timezone
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=20)
    slug=models.SlugField(max_length=30,unique=True)

    def __str__(self):
        return self.name

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status=True)

class Post(models.Model):
    objects=models.Manager()
    published=PublishedManager()

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish_at')
    image = ResizedImageField(upload_to = "uploads/headerPhotos/")
    caption = models.TextField(null=True,blank=True)
    body=RichTextUploadingField()
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(null=True,blank=True)
    publish_at=models.DateTimeField(null=True,blank=True)
    status=models.BooleanField(default=False)
    is_pin=models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete = models.SET_NULL,null=True)
    views=models.PositiveIntegerField(default=1)

    class Meta:
        ordering=['-publish_at']

    def __str__(self): 
    	return f'{self.author.username}\'s Post- {self.title}'

    def save(self, *args, **kwargs):
        if self.status:
            if self.publish_at is None:
                self.publish_at=timezone.now()
        else:
            self.publish_at=None
        if self.created_at is not None:
            self.last_updated=timezone.now()
        super(Post, self).save(*args, **kwargs)
    
    def get_absolute_url(self):        
        return reverse('blog:detail', args=[self.slug,self.publish_at.year,self.publish_at.month,self.publish_at.day])    
    
    def category_url(self):
        return reverse('blog:category',args=[self.category.slug])

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=25)
    email=models.EmailField()
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['created_at']
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"