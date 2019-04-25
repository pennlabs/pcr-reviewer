from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from .models import Comment, Review, Tag, Section
from .helpers import select_random_comment


@login_required
def review(request):
    if request.method == "POST":
        section = get_object_or_404(Comment, id=request.POST.get("section"))
        comment = get_object_or_404(Comment, id=request.POST.get("comment"))
        if Review.objects.filter(comment=comment, reviewer=request.user).exists():
            messages.error(request, "You have already reviewed this comment!")
            return redirect("review")

        comment = get_object_or_404(Comment, id=request.POST.get("comment"))
        tags = [x.strip() for x in request.POST.get("tags", "").split(",")]
        tags = [x.lower() for x in tags if x]
        flag = request.POST.get("flag")

        review = Review.objects.create(
            comment=comment,
            section=section,
            reviewer=request.user,
            flag=flag
        )
        for tag in tags:
            tag, _ = Tag.objects.get_or_create(
                name=tag
            )
            review.tags.add(tag)
        Reservation.objects.filter(reviewer=request.user).delete()
        return redirect("review")

    comment = select_random_comment(request.user)
    if not section:
        messages.success(request, "All comments have been reviewed!")
        return redirect("index")
    if comment is None:
        raise Http404('Unable to randomly select a comment.')

    context = {
        "section": section,
        "comment": comment,
        "total_comments": Comment.objects.filter(section=section).count(),
        "tags": ",".join(Tag.objects.filter(review__section=section).distinct().values_list("name", flat=True))
    }

    return render(request, "review.html", context)


@login_required
def tags(request):
    if "query" in request.GET:
        tags = Tag.objects.filter(name__icontains=request.GET.get("query"))
    else:
        tags = Tag.objects.all()
    tags = list(tags.values_list("name", flat=True))
    return JsonResponse({"tags": tags})


@login_required
def stats(request):
    output = []
    semesters = Section.objects.values("term").distinct().order_by("-term").values_list("term", flat=True)
    comments = {x["section__term"]: x["count"] for x in Comment.objects.values("section__term").annotate(count=Count("section__term"))}
    classes = {x["term"]: x["count"] for x in Section.objects.values("term").annotate(count=Count("term"))}
    reviews = {x["term"]: x["count"] for x in Section.objects.values("term").annotate(count=Count("comment__review", distinct=True))}
    leaderboard = User.objects.annotate(reviews=Count("review")).order_by("reviews")[:10]

    for semester in semesters:
        values = {
            "comments": comments.get(semester, 0),
            "classes": classes.get(semester, 0),
            "reviews": reviews.get(semester, 0)
        }
        output.append((semester, values))

    context = {
        "semesters": output,
        "tags": Tag.objects.annotate(usage=Count("review__section", distinct=True)).order_by("usage", "name").all(),
        "leaderboard": leaderboard
    }

    return render(request, "stats.html", context)
