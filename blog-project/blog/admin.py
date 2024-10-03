from django.contrib import admin

from blog.models import Tag, Post, Comment

# Register your models here.
admin.site.register(Tag)

class PostAdmin(admin.ModelAdmin):
    # We add the slug field automatically (depends on the title)
    prepopulated_fields = {"slug": ("title",)}
    # We use list_display to cahnge the information presented in the Post List, in this case we'll show the slug and the date it published
    list_display = ("slug", "published_at")

# Add the class PostAdmin, with this we add the properties in that class.
admin.site.register(Post, PostAdmin)

# Add the Comment model
admin.site.register(Comment)