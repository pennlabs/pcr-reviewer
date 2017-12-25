from django.test import TestCase
from django.contrib.auth.models import User

from .models import Instructor, Section, Comment, Review
from .helpers import select_random_comments, get_next_section, COMMENTS_PER_REVIEW, SHORT_COMMENT_THRESHOLD


class ReviewTestCase(TestCase):
    def setUp(self):
        self.inst = Instructor.objects.create(
            id=0,
            name="LASTNAME,FIRSTNAME"
        )
        self.section = Section.objects.create(
            name="TEST001001",
            term="2017A",
            instructor=self.inst
        )
        self.user = User.objects.create_user(username="test", password="test")

    def test_next_section(self):
        """ Get next section gets the next section that needs reviewing. """
        self.assertEqual(get_next_section(self.user), self.section)

    def test_next_section_already_reviewed(self):
        """ A user shouldn't review the same class twice. """
        Review.objects.create(
            section=self.section,
            reviewer=self.user
        )
        self.assertEqual(get_next_section(self.user), None)

    def test_select_no_comments(self):
        """ Return an empty list if there are no comments to select. """
        comments = select_random_comments(self.section)
        self.assertEqual(len(comments), 0)

    def test_select_no_duplicates(self):
        """ Do not give the reviewer duplicate comments. """
        for x in range(100):
            Comment.objects.create(
                section=self.section,
                text="A"
            )
        comments = select_random_comments(self.section)
        self.assertEqual(len(comments), 1, comments)

    def test_select_long_short_comments(self):
        """ Make sure long comments are selected, and then short ones. """
        for x in range(3):
            Comment.objects.create(
                section=self.section,
                text="Comment #" + str(x) + " - " + "A"*SHORT_COMMENT_THRESHOLD
            )
        for x in range(COMMENTS_PER_REVIEW + 3):
            Comment.objects.create(
                section=self.section,
                text=str(x) + "A"*(SHORT_COMMENT_THRESHOLD-3)
            )
        comments = select_random_comments(self.section)
        self.assertEqual(len(comments), COMMENTS_PER_REVIEW, comments)
        for x in range(3):
            self.assertTrue(len(comments[x].text) > SHORT_COMMENT_THRESHOLD)
        self.assertTrue(len(comments[-1].text) < SHORT_COMMENT_THRESHOLD)

    def test_select_only_short_comments(self):
        """ If there are only short comments, return those. """
        for x in range(COMMENTS_PER_REVIEW+5):
            Comment.objects.create(
                section=self.section,
                text=str(x)
            )
        comments = select_random_comments(self.section)
        self.assertEqual(len(comments), COMMENTS_PER_REVIEW)
