from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    pass


class Review(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
