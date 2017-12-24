from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from .models import Comment, Review, Tag
from django.db.models import Count


def get_next_comment(user):
    return Comment.objects.annotate(num_reviews=Count("review")).filter(num_reviews__lt=2).exclude(review__reviewer=user).first()


def review(request):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=request.POST.get("comment"))
        approve = request.POST.get("approve").lower() == "true"
        review = Review.objects.create(
            comment=comment,
            reviewer=request.user,
            approve=approve
        )
        tags = [x.strip().lower() for x in request.POST.get("tags", "").split(",")]
        for tag in tags:
            if tag:
                tagobj, _ = Tag.objects.get_or_create(name=tag)
                review.tags.add(tagobj)
        messages.success(request, "Review {}!".format("approved" if approve else "rejected"))
        return redirect("review")

    comment = get_next_comment(request.user)
    if not comment:
        messages.success(request, "All comments have been reviewed!")
        return redirect("index")

    context = {
        "comment": comment
    }

    return render(request, "review.html", context)


def tags(request):
    if "query" in request.GET:
        tags = Tag.objects.filter(name__icontains=request.GET.get("query"))
    else:
        tags = Tag.objects.all()
    tags = list(tags.values_list("name", flat=True))
    return JsonResponse({"tags": tags})
