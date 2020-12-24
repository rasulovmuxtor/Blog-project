from django.shortcuts import render,get_object_or_404
from .models import Comment,Post,Category
from .forms import CommentForm,SearchForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from django.db.models import Count
def index(request):
    pin=Post.published.filter(is_pin=True).first()
    latest=Post.published.exclude(id=pin.id)[:5]
    popular=Post.published.order_by('-views').exclude(id__in=latest.values_list('id',flat=True)).exclude(id=pin.id)[:5]

    categories=Category.objects.all()
    without=[pin.id]+list(latest.values_list('id',flat=True))+list(popular.values_list('id',flat=True))
    category_list=[]
    #development
    without=[]
    for i in categories:
        posts=i.posts.filter(status=True).exclude(id__in=without)[:5]
        if posts.exists():
            category_list.append((i, posts))
    context={
        'pin':pin,
        'latest':latest,
        'popular':popular,
        'category_list':category_list,
        'categories':categories,
    }
    return render(request,'blog/index.html',context)
def category_posts(request,category):
    categories=Category.objects.all()
    if category == 'latest':
        posts=Post.objects.all()
    elif category == 'popular':
        posts=Post.objects.all().order_by('-views')
    else:
        posts=Post.objects.filter(category__slug=category)
        categories=categories.exclude(slug=category)
    paginator=Paginator(posts,10)

    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    context={
        'page':page,
        'posts':posts,
        'categories':categories,
        }
    
    return render(request,'blog/category.html',context)
def detail(request, slug,year,month,day):
    categories=Category.objects.all()
    
    post=get_object_or_404(Post,slug=slug,publish_at__year=year,publish_at__month=month,publish_at__day=day)
    post.views+=1
    post.save()

    latest=Post.published.exclude(id=post.id)[:8]
    comments=post.comments.all()
    
    new_comment=None
    if request.method=='POST':
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
    comment_form=CommentForm()


    

    context={
        'post':post,
        'latest':latest,
        'categories':categories,
        'comment_form':comment_form,
        'comments':comments,
        'new_comment':new_comment,
    }
    return render(request,'blog/detail.html',context)

def post_search(request):
    categories=Category.objects.all()
    posts = []
    query=None
    if request.method=='POST':
        query=request.POST.get('search')
        search_vector = SearchVector('title', 'body')
        search_query = SearchQuery(query)
        posts = Post.published.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query)          
    context={
        'posts':posts,
        'query':query,
        'categories':categories,
            }       
    return render(request,'blog/search.html',context)