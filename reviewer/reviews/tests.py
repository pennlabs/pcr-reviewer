from django.test import TestCase
from django.contrib.auth.models import User

from .models import Instructor, Section, Comment, Review
from .helpers import select_random_comment, get_next_section, get_best_comments


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
        self.user2 = User.objects.create_user(username="test2", password="test2")
        self.user3 = User.objects.create_user(username="test3", password="test3")
        self.approve = "A"
        self.marked = "M"

    def test_next_section(self):
        """ Get next section gets the next section that needs reviewing. """
        self.assertEqual(get_next_section(self.user), self.section)

    def test_next_section_already_reviewed(self):
        """ A user shouldn't review the same class twice. """
        comment = Comment.objects.create(
            section=self.section,
            text="Good class!"
        )
        Review.objects.create(
            comment=comment,
            flag=self.approve,
            section=self.section,
            reviewer=self.user
        )
        self.assertEqual(get_next_section(self.user), None)

    def test_select_no_comments(self):
        """ Return None if there are no comments to select. """
        comment = select_random_comment(self.section)
        self.assertEqual(comment, None)

    # TODO: Rework test to work with new model scheme
    '''
    def test_select_long_short_comments(self):
        """ Make sure long comments are selected, and then short ones. """
        for x in range(3):
            Comment.objects.create(
                section=self.section,
                text="Comment #" + str(x) + " - " + "A"*settings.SHORT_COMMENT_THRESHOLD
            )
        for x in range(settings.COMMENTS_PER_REVIEW + 3):
            Comment.objects.create(
                section=self.section,
                text=str(x) + "A"*(settings.SHORT_COMMENT_THRESHOLD-3)
            )
        for x in range(3):
            self.assertTrue(len(comments[x].text) > settings.SHORT_COMMENT_THRESHOLD)
        self.assertTrue(len(comments[-1].text) < settings.SHORT_COMMENT_THRESHOLD)
    '''

    def test_select_only_short_comments(self):
        """ If there are only short comments, return those. """
        Comment.objects.create(
            section=self.section,
            text=""
        )
        comment = select_random_comment(self.section)
        self.assertEqual(len(comment.text), 0)

    def test_best_comments_no_comments(self):
        """ If there are no reviews, don't export any comments. """
        self.assertEqual(len(get_best_comments(self.section)), 0)

    def test_best_comments(self):
        """ Make sure top rated reviews are returned. """
        comment = Comment.objects.create(
            section=self.section,
            text="Good class!"
        )
        bad_comment = Comment.objects.create(
            section=self.section,
            text="This class is terrible."
        )

        for user in [self.user, self.user2, self.user3]:
            Review.objects.create(
                comment=comment,
                flag=self.approve,
                section=self.section,
                reviewer=user
            )
            Review.objects.create(
                comment=bad_comment,
                flag=self.marked,
                section=self.section,
                reviewer=user
            )

        self.assertEqual(list(get_best_comments(self.section)), [comment.text])

    # TODO: Discuss with other developers whether this test is still needed
    '''
    def test_best_comment_controversial(self):
        """ If the reviewers disagree on a comment, don't include it. """
        comment = Comment.objects.create(
            section=self.section,
            text="Good class!"
        )

        r1 = Review.objects.create(
            section=self.section,
            reviewer=self.user
        )
        r2 = Review.objects.create(
            section=self.section,
            reviewer=self.user2
        )
        r3 = Review.objects.create(
            section=self.section,
            reviewer=self.user3
        )

        for review in [r1, r2]:
            CommentRating.objects.create(
                comment=comment,
                review=review,
                rating=1
            )

        CommentRating.objects.create(
            comment=comment,
            review=r3,
            rating=5
        )

        self.assertEqual(len(get_best_comments(self.section)), 0)
    '''

    def test_best_comments_enough_reviewers(self):
        """ Only include a comment if enough people have reviewed it. """
        comment = Comment.objects.create(
            section=self.section,
            text="This class was undoubtably a class."
        )

        Review.objects.create(
            comment=comment,
            section=self.section,
            reviewer=self.user,
            flag=self.approve
        )
        Review.objects.create(
            comment=comment,
            section=self.section,
            reviewer=self.user2,
            flag=self.approve
        )

        self.assertEqual(len(get_best_comments(self.section)), 0)
