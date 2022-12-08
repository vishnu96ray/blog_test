from django.shortcuts import render,redirect, get_object_or_404
from api.models import Blog
from django.db.models import Q
from api.forms import CreateBlogForm, UpdateBlogForm
from account.models import Account
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.

def create_blog_view(request):
    context = {}
    user = request.user
    print(user,'lllllllllllllllllllll')
    if not user.is_authenticated:
        return redirect('must authenticate')

    form = CreateBlogForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        print(user.email,454)
        
        owner = Account.objects.filter(email=user.email).first()
        obj.owner = owner
        obj.save()

        # owner = Account.objects.filter(email=user.email)
        # # owner = owner.first()
        # print(owner,77878)
        # username = owner.username
        # owner.username = user
        # obj.save()
        form = CreateBlogForm()
    context['form'] = form
    return render(request, 'blog/create_blog.html')


def detail_blog_view(request, slug):

    context = {}

    blog = get_object_or_404(Blog, slug=slug)
    context['blog'] = blog
    return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):

    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must authenticate')

    blog = get_object_or_404(Blog, slug=slug)

    if blog.owner != user:
        return HttpResponse('You are not owner of this post')

    if request.POST:
        form = UpdateBlogForm(
            request.POST or None, request.FILES or None, instance=blog)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = 'Updated'
            blog = obj
    form = UpdateBlogForm(
        initial={
            'title': blog.title,
            'description': blog.description,
            'image': blog.image

        }
    )
    context['form'] = form
    return render(request, 'blog/edit_blog.html', context)


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Blog.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)
    return list(set(queryset))


