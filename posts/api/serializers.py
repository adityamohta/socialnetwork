from rest_framework.serializers import ModelSerializer

from ..models import Post


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish',
        ]


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'title',
            'slug',
            'content',
            'publish',
        ]


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'user',
            'title',
            'slug',
            'content',
            'publish',
        ]


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
