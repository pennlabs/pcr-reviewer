import random

from django.db.models import Count
from django.db.models.functions import Length

from .models import Comment, Section


COMMENTS_PER_REVIEW = 5
SHORT_COMMENT_THRESHOLD = 10


def get_best_comments(section):
    return Comment.objects.filter(section=section, commentrating__rating__lt=2).distinct().values_list("text", flat=True)


def get_next_comment(user):
    return Comment.objects.annotate(num_reviews=Count("review")).filter(num_reviews__lt=2).exclude(review__reviewer=user).first()


def get_next_section(user):
    return Section.objects.annotate(num_reviews=Count("review")).filter(num_reviews__lt=3).exclude(review__reviewer=user).first()


def select_random_comments(section):
    comments = list(Comment.objects.filter(commentrating__review__section=section, commentrating__rating=1))
    com_all = Comment.objects.annotate(text_len=Length("text")).filter(section=section)
    com_short = com_all.filter(text_len__lte=SHORT_COMMENT_THRESHOLD)
    com = com_all.filter(text_len__gt=SHORT_COMMENT_THRESHOLD)
    com_len = com.count()
    items = list(range(com_len))
    random.shuffle(items)
    seen = set([x.text for x in comments])
    for x in items:
        if com[x].text not in seen:
            comments.append(com[x])
            seen.add(com[x].text)
        if len(comments) >= COMMENTS_PER_REVIEW:
            break
    for x in com_short:
        if len(comments) >= COMMENTS_PER_REVIEW:
            break
        if x.text not in seen:
            comments.append(x)
            seen.add(x.text)
    comments.sort(key=lambda x: -len(x.text))
    return comments
