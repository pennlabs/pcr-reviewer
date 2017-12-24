from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Comment
from django.db.models import Count


def get_next_comment(user):
    return Comment.objects.annotate(num_reviews=Count("review")).filter(num_reviews__lt=2).exclude(review__reviewer=user).first()


def review(request):
    comment = get_next_comment(request.user)
    if not comment:
        messages.success(request, "All comments have been reviewed!")
        return redirect("index")

    context = {
        "comment": comment
    }

    return render(request, "review.html", context)
