from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from .models import Comment, Review, Tag
from django.db.models import Count
from django.db.models.functions import Length

import random


def get_next_comment(user):
    return Comment.objects.annotate(num_reviews=Count("review")).filter(num_reviews__lt=2).exclude(review__reviewer=user).first()


def get_next_section(user):
    comment = get_next_comment(user)
    if not comment:
        return None
    return comment.section


def select_random_comments(section):
    comments = []
    com = Comment.objects.annotate(text_len=Length("text")).filter(section=section, text_len__gt=10)
    com_len = com.count()
    if com_len < 5:
        return com
    items = list(range(com_len))
    random.shuffle(items)
    for x in items:
        if all([not com[x].text == y.text for y in comments]):
            comments.append(com[x])
        if len(comments) >= 5:
            break
    return comments


def review(request):
    if request.method == "POST":
        pass
        return redirect("review")

    section = get_next_section(request.user)
    if not section:
        messages.success(request, "All comments have been reviewed!")
        return redirect("index")

    comments = select_random_comments(section)

    context = {
        "comments": comments
    }

    return render(request, "review.html", context)


def tags(request):
    if "query" in request.GET:
        tags = Tag.objects.filter(name__icontains=request.GET.get("query"))
    else:
        tags = Tag.objects.all()
    tags = list(tags.values_list("name", flat=True))
    return JsonResponse({"tags": tags})
