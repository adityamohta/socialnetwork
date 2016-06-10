from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
from .models import Comment


@login_required
def comment_delete(request, id):
    instance = Comment.objects.filter(id=id).first()
    if instance is None:
        raise Http404
    if request.user != instance.user:
        # raise Http404
        response = HttpResponse()
        response.status_code = 403
        return response

    if request.method == 'POST':
        parent_obj_url = instance.content_object.get_absolute_url()
        instance.delete()
        html_message = 'Comment Deleted.'
        html_message = settings.MESSAGE % ('success', html_message)
        messages.success(request, html_message, extra_tags='html_safe')
        return HttpResponseRedirect(parent_obj_url)

    context = {
        'comment': instance,
    }
    return render(request, 'confirm_delete.html', context)


def comment_thread(request, id):
    # instance = get_object_or_404(Comment, id=id)
    instance = Comment.objects.filter(id=id).first()
    if instance is None:
        raise Http404

    if not instance.is_parent:
        instance = instance.parent

    initial_data = {
        'content_type': instance.content_type,
        'object_id': instance.object_id,
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
        html_message = '''
            Comment Posted successfully.
        '''
        html_message = settings.MESSAGE % ('success', html_message)
        messages.success(request, html_message, extra_tags='html_safe')
        if not created:
            print("Failed!")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'comment': instance,
        'comment_form': comment_form,
    }
    return render(request, 'comment_thread.html', context)
