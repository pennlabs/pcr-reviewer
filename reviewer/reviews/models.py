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


class Section(models.Model):
    name = models.CharField(max_length=15)
    term = models.CharField(max_length=5)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    def __str__(self):
        return "<{}, {}>".format(self.term, self.name)


class Comment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return "<{}, {}>".format(self.section, self.text[:10])


class Review(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return "<{}, {}>".format(self.reviewer.username, self.section)


class CommentRating(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return "<{}, {}>".format(self.comment.text[:10], self.review.reviewer)
