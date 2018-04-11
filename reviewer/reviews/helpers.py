import random
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Count, Max
from django.db.models.functions import Length

from .models import Comment, Section, Reservation


def get_best_comments(section):
    return Comment.objects.annotate(rating_count=Count("commentrating__rating"), rating=Max("commentrating__rating")) \
                          .filter(section=section, rating__lte=settings.COMMENT_THRESHOLD, rating_count__gte=settings.REVIEWER_THRESHOLD) \
                          .distinct().values_list("text", flat=True)


def get_next_comment(user):
    return Comment.objects.annotate(num_reviews=Count("review")) \
        .filter(num_reviews__lt=settings.REVIEWER_THRESHOLD) \
        .exclude(review__reviewer=user).first()


def get_next_section(user):
    Reservation.objects.filter(expiration__lt=datetime.now()).delete()
    section = Section.objects.annotate(num_reviews=Count("review"), num_reservations=Count("reservation")) \
        .filter(num_reviews__lt=settings.REVIEWER_THRESHOLD) \
        .exclude(review__reviewer=user).order_by("num_reservations").first()
    Reservation.objects.create(section=section, expiration=datetime.now() + timedelta(minutes=1))
    return section


def select_random_comments(section):
    comments = list(Comment.objects.filter(commentrating__review__section=section, commentrating__rating=1))
    com_all = Comment.objects.annotate(text_len=Length("text")).filter(section=section)
    com_short = com_all.filter(text_len__lte=settings.SHORT_COMMENT_THRESHOLD)
    com = com_all.filter(text_len__gt=settings.SHORT_COMMENT_THRESHOLD)
    com_len = com.count()
    items = list(range(com_len))
    random.shuffle(items)
    seen = set([x.text for x in comments])
    for x in items:
        if com[x].text not in seen:
            comments.append(com[x])
            seen.add(com[x].text)
        if len(comments) >= settings.COMMENTS_PER_REVIEW:
            break
    for x in com_short:
        if len(comments) >= settings.COMMENTS_PER_REVIEW:
            break
        if x.text not in seen:
            comments.append(x)
            seen.add(x.text)
    comments.sort(key=lambda x: -len(x.text))
    return comments
