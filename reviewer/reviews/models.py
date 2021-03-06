from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.TextField(unique=True)

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
        return "<{}, {}, {}>".format(self.term, self.name, self.instructor.name)


class Comment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return "<{}, {}>".format(self.section, self.text[:10])


class Review(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    flag = models.CharField(max_length=1, choices=(('A', 'Approved'), ('M', 'Not Useful'), ('I', 'Inappropriate')), null=True, default=None)

    def __str__(self):
        return "<{}, {}, {}>".format(self.comment.text[:10], self.reviewer.username, self.section)


class Reservation(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    expiration = models.DateTimeField(db_index=True)
