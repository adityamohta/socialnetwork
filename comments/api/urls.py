from django.conf.urls import url

from .views import (
    CommentDetailAPIView,
    CommentListAPIView,
)

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
    # url(r'^(?P<id>\d+)/delete/$', CommentListAPIView.as_view(), name='delete'),
]
