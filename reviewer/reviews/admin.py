from django.contrib import admin
from .models import Instructor, Comment, Review, Tag

admin.site.register(Instructor)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Tag)
