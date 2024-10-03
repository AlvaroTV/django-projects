from django.db import models

from django.conf import settings
# Create your models here.

class Tag(models.Model):
    value = models.TextField(max_length=100)

    def __str__(self):
        return self.value


'''
It would be great though, if as well as being able to comment on a POST, you could also comment on an author.
But this would end up beign confusing:
* Both "post" and "author" fields can be null, which means that the database will allow us to insert a "Comment" that's not mapped to any object (they could both be null). Before, when we
    only mapped to "Posts", the post field did not allow null and so the database would enforce consistency.
* Likewise, "post" and "author" could both be populated. This would mean the "Comment" applies to both, which might not make sense.
* We'd need extra code to check and query the right field when fetching the "Comments", based on which context we are in (Post or Author).
* If we ended up adding some other model, and wanted to allow comments on it, we'd need yet another field to store this information.     

class Comment(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODELS, on_delete=models.CASCADE)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
'''

# By utilizing ContentType we can allow a model to be related to any number of models by just adding three attributes to a Model:
# 1. A Foreignkey field that points to a ContentType. Normally this is called content_type
# 2. A PositiveIntegerField that stores the primary key of the related object. Normally this is called object_id
# 3. A GenericForeignKey field, a special type of field that will look up the object from the other two new fields. 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
class Comment(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    # Storing a value in GenericForeignKey is similar to a normal ForeignKey: just assign the object to it.
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


'''
REVERSE GENERIC RELATIONSHIPS
A disadvantage of the "GenericForeignKey" is that can't be requiered agaisnt, so if you try it you'll get an error.
To solve this we can consider setting up a GenericRelation field on it.
'''
from django.contrib.contenttypes.fields import GenericRelation
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    title = models.TextField(max_length=100)
    slug = models.SlugField()
    summary = models.TextField(max_length=500)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="post")
    # The comments attributes acts like a RelatedManager allowing you to query, filter(), add(), create() and remove() Comments to a Post.
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title