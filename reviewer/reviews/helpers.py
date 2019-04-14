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


def get_next_comment(user):
    return Comment.objects.annotate(num_reviews=Count("review")) \
        .filter(num_reviews__lt=settings.REVIEWER_THRESHOLD) \
        .exclude(review__reviewer=user).first()


def get_next_section(user):
    Reservation.objects.filter(expiration__lt=timezone.now()).delete()
    section = Section.objects.annotate(num_reviews=Count("review"), num_reservations=Count("reservation")) \
        .filter(num_reviews__lt=settings.REVIEWER_THRESHOLD) \
        .exclude(review__reviewer=user).order_by("num_reservations").first()
    if section is not None:
        Reservation.objects.create(section=section, expiration=timezone.now() + timedelta(minutes=1))
    return section


def select_random_comment(section):
    comments = list(Comment.objects.filter(review__section=section))
    com_all = Comment.objects.annotate(text_len=Length("text")).filter(section=section)
    com_short = com_all.filter(text_len__lte=settings.SHORT_COMMENT_THRESHOLD)
    com = com_all.filter(text_len__gt=settings.SHORT_COMMENT_THRESHOLD)
    com_len = com.count()
    items = list(range(com_len))
    random.shuffle(items)
    seen = set([x.text for x in comments])
    for x in items:
        if com[x].text not in seen:
            return com[x]
    for x in com_short:
        if x.text not in seen:
            return x
    return None