import random
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import Length

from .models import Comment, Section, Reservation


def get_best_comments(section):
    return Comment.objects.filter(section=section, review__flag="A") \
                          .annotate(review_count=Count("review")) \
                          .filter(review_count__gte=settings.REVIEWER_THRESHOLD).distinct() \
                          .values_list("text", flat=True)


def get_next_section(user):
    section = Section.objects.annotate(num_reviews=Count("review"), num_reservations=Count("reservation")) \
        .filter(num_reviews__lt=settings.REVIEWER_THRESHOLD) \
        .exclude(review__reviewer=user).order_by("num_reservations").first()
    if section is not None:
        return section
    else:
        return None


def select_random_comment(user):
    Reservation.objects.filter(expiration__lt=timezone.now()).delete()
    comments = Comment.objects.annotate(num_reviewers=Count("review")+Count("reservation"), text_len=Length("text"))\
        .filter(num_reviewers__lt=settings.REVIEWER_THRESHOLD)\
        .exclude(review__reviewer=user)
    com_short = comments.filter(text_len__lte=settings.SHORT_COMMENT_THRESHOLD)
    com = comments.filter(text_len__gt=settings.SHORT_COMMENT_THRESHOLD)
    com_len = com.count()
    items = list(range(com_len))
    random.shuffle(items)
    ret = None
    for x in items:
        ret = com[x]
        break
    for x in com_short:
        ret = x
        break
    if ret is not None:
        Reservation.objects.create(comment=ret, expiration=timezone.now() + timedelta(minutes=5))
    return ret
