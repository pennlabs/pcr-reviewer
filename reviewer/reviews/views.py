from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from .models import Comment, Review, Tag, Section, CommentRating
from .helpers import get_next_section, select_random_comments


def review(request):
    if request.method == "POST":
        section = get_object_or_404(Section, id=request.POST.get("section"))

        order = [x.strip() for x in request.POST.get("order").split(",")]
        order = [get_object_or_404(Comment, id=x) for x in order if x]

        if len(order) >= 1:
            review = Review.objects.create(
                section=section,
                reviewer=request.user
            )

            tags = [x.strip() for x in request.POST.get("tags", "").split(",")]
            tags = [x.lower() for x in tags if x]
            for tag in tags:
                tag, _ = Tag.objects.get_or_create(
                    name=tag
                )
                review.tags.add(tag)

            for i in range(len(order)):
                CommentRating.objects.create(
                    review=review,
                    comment=order[i],
                    rating=i
                )

            messages.success(request, "Your review has been added!")
        else:
            messages.error(request, "You did not submit any comments for review!")
        return redirect("review")

    section = get_next_section(request.user)
    if not section:
        messages.success(request, "All comments have been reviewed!")
        return redirect("index")

    comments = select_random_comments(section)

    context = {
        "section": section,
        "comments": comments,
        "tags": ",".join(Tag.objects.filter(review__section=section).distinct().values_list("name", flat=True))
    }

    return render(request, "review.html", context)


def tags(request):
    if "query" in request.GET:
        tags = Tag.objects.filter(name__icontains=request.GET.get("query"))
    else:
        tags = Tag.objects.all()
    tags = list(tags.values_list("name", flat=True))
    return JsonResponse({"tags": tags})
