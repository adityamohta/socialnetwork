from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment

from .forms import PostForm
from .models import Post
from urllib.parse import quote_plus  # to make string ready for url sharing


# Create your views here.
# Use CRUD--Create, Retrieve, Update, Delete


def post_list(request):  # List Items
    posts_list = Post.objects.active()  # active is user defined Model Manager. check it out in models.py
    if request.user.is_staff or request.user.is_superuser:
        posts_list = Post.objects.all()
    post_search_var = 'q'
    search = request.GET.get(post_search_var)
    if search:
        posts_list = posts_list.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
        ).distinct()  # to not have duplicate items in there.
    else:
        search = ''
    paginator = Paginator(posts_list, 3)  # Show 25 contacts per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    # Logic of Pagination
    total_pages = posts.paginator.num_pages

    if total_pages <= 10:
        page_num_list = range(1, total_pages + 1)

    else:
        if posts.number == 1:
            page_num_list = range(min(posts.number, total_pages - 9), min(posts.number + 9, total_pages) + 1)
        else:
            page_num_list = range(min(posts.number - 1, total_pages - 9), min(posts.number + 9, total_pages + 1))

    # print(page_num_list)
    # Logic ends here
    today = timezone.now().date()
    context = {
        'posts': posts,
        'page_num_list': page_num_list,
        'page_request_var': page_request_var,
        'post_search_var': post_search_var,
        'search': search,
        'today': today,
    }
    return render(request, 'post_list.html', context)


def post_create(request):  # Create
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            slug = instance.slug
            html_message = '''
                    <strong>Create Successfully.</strong>
                    To read this message,
                    <a href="/posts/%s" class="alert-link">Click here.</a>
            ''' % slug
            html_message = settings.MESSAGE % ('success', html_message)
            messages.success(
                    request,
                    # this is link to the details of the newly created post.
                    html_message,
                    # extra tags is used to add a tag in message.tags. (can be used to assign classes).
                    extra_tags='html_safe',
            )
            return redirect('posts:list')
            # request.POST.get('title')
            # request.POST.get('content')
    else:
        form = PostForm()
        # print(request.POST)

    context = {
        'form': form,
    }
    return render(request, 'post_create.html', context)


def post_detail(request, slug):  # Retrieve
    post = get_object_or_404(Post, slug=slug)
    if post.draft or post.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(post.content)
    today = timezone.now().date()

    # content_type = ContentType.objects.get_for_model(Post)
    # obj_id = post.id
    # comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
    # comments = Comment.objects.filter_by_instance(post)   # to get all comments by Comment Object.
    # difference between property and method is that we dont have to use parentheses after the funciton.
    # in this case its comments not comments()

    comments = post.comments  # .comments is a property of Post Model.
    initial_data = {
        'content_type': post.get_content_type,
        'object_id': post.id,
    }
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid() and request.user.is_authenticated():
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=obj_id,
                content=content_data,
                parent=parent_obj,
        )
        html_message = 'Comment Posted successfully.'

        html_message = settings.MESSAGE % ('success', html_message)
        messages.success(
                request,
                # this is link to the details of the newly updated post.
                html_message,
                # extra tags is used to add a tag in message.tags. (can be used to assign classes.
                extra_tags='html_safe',
        )
        if not created:
            print("Failed!")
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {
        'post': post,
        'share_string': share_string,
        'today': today,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'post_detail.html', context)


def post_update(request, slug):  # Update Item
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            html_message = '''
                <a href="/posts/%s" class="alert-link">Item saved</a>
            ''' % slug
            html_message = settings.MESSAGE % ('info', html_message)
            messages.success(
                    request,
                    # this is link to the details of the newly updated post.
                    html_message,
                    # extra tags is used to add a tag in message.tags. (can be used to assign classes.
                    extra_tags='html_safe',
            )
            # request.POST.get('title')
            # request.POST.get('content')
            # return HttpResponseRedirect(instance.get_absolute_url())
            print(instance.get_absolute_url)
            return redirect('posts:detail', instance.slug)
    else:
        form = PostForm(instance=instance)
        # print(request.POST)
    context = {
        'form': form,
    }
    return render(request, 'post_create.html', context)


def post_delete(request, slug):  # delete Item
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    html_message = '''
        <strong>Successfully deleted</strong>
    '''
    html_message = settings.MESSAGE % ('danger', html_message)
    messages.success(request, html_message, extra_tags='html_safe')

    return redirect('posts:list')
