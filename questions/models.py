from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="category")
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("questions:category", kwargs={"slug": self.slug})

    class Meta:
        ordering = ['-id']


class Question(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    question = models.CharField(max_length=256, verbose_name="question")
    details = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.question

    def get_absolute_url(self):
        return reverse("questions:question_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ['-created_at']

    def _get_unique_slug(self):
        slug = slugify(self.question)
        unique_slug = slug
        num = 1
        while Question.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Question, self).save()
