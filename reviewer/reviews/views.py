from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Comment, Review
from django.db.models import Count


def get_next_comment(user):
    return Comment.objects.annotate(num_reviews=Count("review")).filter(num_reviews__lt=2).exclude(review__reviewer=user).first()


def review(request):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=request.POST.get("comment"))
        approve = request.POST.get("approve").lower() == "true"
        Review.objects.create(
            comment=comment,
            reviewer=request.user,
            approve=approve
        )
        messages.success(request, "Review added!")
        return redirect("review")

    comment = get_next_comment(request.user)
    if not comment:
        messages.success(request, "All comments have been reviewed!")
        return redirect("index")

    context = {
        "comment": comment
    }

    return render(request, "review.html", context)
