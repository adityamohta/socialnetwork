from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from ..models import Post
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    PostCreateUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer,
)


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'   # default lookup field is pk or id.
    # lookup_url_kwarg = 'abc'  # to change the url variable to something else.


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'   # default lookup field is pk or id.
    # lookup_url_kwarg = 'abc'  # to change the url variable to something else.


class PostListAPIView(ListAPIView):
    # queryset = Post.objects.all()     # we dont need it as we are manually getting the query set.
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]    # ?search=anything&ordering=-title will order anthing by title
    search_fields = ['title', 'content', 'user__first_name', ]
    #  default pagination
    pagination_class = PostPageNumberPagination     # PostLimitOffsetPagination    # user defined pagination
    # LimitOffsetPagination  ?limit=&offset=  # PageNumberPagination (this requires minimum 100objects)

    # actually we dont need to define a custom query search, as we have used filter_backends to search.
    # but both searches can run simultaneously.
    def get_queryset(self, *args, **kwargs):
        # query_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        # can be dont in both ways, using super or .objects method.
        query_list = Post.objects.all()
        query = self.request.GET.get('q')
        if query:
            query_list = query_list.filter(
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
            ).distinct()  # to not have duplicate items in there.
        return query_list


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # send email here may be.

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
