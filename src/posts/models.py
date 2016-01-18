from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from django.utils.text import slugify
# Create your models here.
# MVC MODEL VIEW CONTROLLER


#Post.objects.all()
#Post.objects.create(user=user, title="Some time")

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" %(new_id, filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field", 
            height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]



def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)



pre_save.connect(pre_save_post_receiver, sender=Post)










