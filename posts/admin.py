from django.contrib import admin
from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'updated', 'timestamp']    # specifies what to display at admin panel
    list_display_links = ['updated']    # adds link to the Model details on the specified list
    list_filter = ['updated', 'timestamp']  # add a filter app on the right side of screen
    list_editable = ['title']   # list of elements which are editable right from the db table

    search_fields = ['title', 'content']    # adds a search app on top of the list.(only searches the given fields)

    class Meta:
        model = Post

# Register your models here.
admin.site.register(Post, PostModelAdmin)
