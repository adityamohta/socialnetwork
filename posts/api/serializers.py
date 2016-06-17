from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
)

from accounts.api.serializers import UserDetailSerializer
from comments.api.serializers import CommentSerializer
from comments.models import Comment
from ..models import Post


post_detail_url = HyperlinkedIdentityField(
        view_name='posts-api:detail',
        lookup_field='slug',
)
post_delete_url = HyperlinkedIdentityField(
        view_name='posts-api:delete',
        lookup_field='slug',
)


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish',
        ]


class PostDetailSerializer(ModelSerializer):
    delete = post_delete_url
    user = UserDetailSerializer()   # SerializerMethodField()
    image = SerializerMethodField()
    html_content = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'title',
            'slug',
            'content',
            'html_content',
            'publish',
            'image',
            'comments',
            'delete',
        ]

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_html_content(self, obj):
        return obj.get_markdown()

    # use it when we use: user = SerializerMethodField()
    # def get_user(self, obj):
    #     return str(obj.user.username)

    def get_comments(self, obj):
        # content_type = obj.get_content_type
        # object_id = obj.id
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments


class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer()   # SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'title',
            'slug',
            'content',
            'publish',
        ]

    # use it when we use: user = SerializerMethodField()
    # def get_user(self, obj):
    #     return str(obj.user.username)

"""
from posts.models import Post
from posts.api.serializers import PostDetailSerializer
data = {
    "title": "yeah baby",
    "content": "new_content",
    "publish": "2016-2-12",
    "slug": "yeah-buddy",
}
obj = Posts.objects.get(id=3)
new_item = PostDetailSerializer(data=data)
if new_item.is_valid():
    new_item.save()
else:
    print(new_item.errors)
"""
