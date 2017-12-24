from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Instructor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return "<{}, {}>".format(self.id, self.name)


class Comment(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    term = models.CharField(max_length=5)
    section = models.CharField(max_length=15)
    text = models.TextField()

    def __str__(self):
        return "<{}, {}, {}>".format(self.term, self.section, self.text[:10])


class Review(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    approve = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
