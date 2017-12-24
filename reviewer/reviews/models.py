from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.TextField()


class Instructor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()


class Comment(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    term = models.CharField(max_length=5)
    section = models.CharField(max_length=15)
    text = models.TextField()


class Review(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
