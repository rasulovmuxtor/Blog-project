from django.urls import path,re_path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    # re_path(r'^category/(?P<category>[a-z])',views.category_posts,name='category2'),
    path('<slug:category>',views.category_posts,name='category'),
    path('<slug:slug>/<int:year>/<int:month>/<int:day>',views.detail,name='detail'),
    path('search/',views.post_search,name='search')
]