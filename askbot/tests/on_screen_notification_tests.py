"""
.. _on_screen_notification_tests:

:mod:`on_screen_notification_tests` -- Module for testing on-screen notifications
=================================================================================

.. automodule:: on_screen_notification_tests 
  .. moduleauthor:: Evgeny Fadeev <evgeny.fadeev@gmail.com>
"""
import datetime
import time
from django.test import TestCase
from askbot import models
from askbot import const
from askbot.tests.utils import create_user


def get_re_notif_after(timestamp):
    """returns query set with response notifications
    posted after the ``timestamp`` - a ``datetime.datetime`` instance
    """
    notifications = models.Activity.objects.filter(
            activity_type__in = const.RESPONSE_ACTIVITY_TYPES_FOR_DISPLAY,
            active_at__gte = timestamp
        )
    return notifications


class OnScreenUpdateNotificationTests(TestCase):
    """Test update notifications that are displayed on
    screen in the user profile responses view
    and "the red envelope"
    """

    def reset_response_counts(self):
        self.reload_users()
        models.ActivityAuditStatus.objects.all().delete()
        for user in self.users:
            user.new_response_count = 0
            user.seen_response_count = 0
            user.save()

    def reload_users(self):
        self.u11 = models.User.objects.get(id=self.u11.id)
        self.u12 = models.User.objects.get(id=self.u12.id)
        self.u13 = models.User.objects.get(id=self.u13.id)
        self.u14 = models.User.objects.get(id=self.u14.id)
        self.u21 = models.User.objects.get(id=self.u21.id)
        self.u22 = models.User.objects.get(id=self.u22.id)
        self.u23 = models.User.objects.get(id=self.u23.id)
        self.u24 = models.User.objects.get(id=self.u24.id)
        self.u31 = models.User.objects.get(id=self.u31.id)
        self.u32 = models.User.objects.get(id=self.u32.id)
        self.u33 = models.User.objects.get(id=self.u33.id)
        self.u34 = models.User.objects.get(id=self.u34.id)
        self.users = [
            self.u11,
            self.u12,
            self.u13,
            self.u14,
            self.u21,
            self.u22,
            self.u23,
            self.u24,
            self.u31,
            self.u32,
            self.u33,
            self.u34,
        ]

    def setUp(self):
        #users for the exercise
        self.u11 = create_user('user11', 'user11@example.com', status='m')
        self.u12 = create_user('user12', 'user12@example.com', status='m')
        self.u13 = create_user('user13', 'user13@example.com', status='m')
        self.u14 = create_user('user14', 'user14@example.com', status='m')

        #users for first problem
        self.u21 = create_user('user21', 'user21@example.com', status='m')#post problem
        self.u22 = create_user('user22', 'user22@example.com', status='m')#edit problem
        self.u23 = create_user('user23', 'user23@example.com', status='m')
        self.u24 = create_user('user24', 'user24@example.com', status='m')

        #users for second problem
        self.u31 = create_user('user31', 'user31@example.com', status='m')#post problem
        self.u32 = create_user('user32', 'user32@example.com', status='m')#edit problem
        self.u33 = create_user('user33', 'user33@example.com', status='m')
        self.u34 = create_user('user34', 'user34@example.com', status='m')

        #a hack to initialize .users list
        self.reload_users()

        #pre-populate askbot with some content
        #create a exercise and two problems, each post gets two comments
        #users have two digit codes. What users do in the setup code
        #is explained below (x is a variable that takes integer values of [1-3])
        #user x1 makes a post, users x2 and x3 add comments to that post
        #users 1x work on exercise, 2x and 3x on the problems
        #users x4 do not do anyting in the setup code

        self.thread = models.Thread.objects.create_new(
                            title = 'test exercise',
                            author = self.u11,
                            added_at = datetime.datetime.now(),
                            wiki = False,
                            tagnames = 'test', 
                            text = 'hey listen up',
                        )
        self.exercise = self.thread._exercise_post()
        self.comment12 = self.exercise.add_comment(
                            user = self.u12,
                            comment = 'comment12'
                        )
        self.comment13 = self.exercise.add_comment(
                            user = self.u13,
                            comment = 'comment13'
                        )
        self.problem1 = models.Post.objects.create_new_problem(
                            thread = self.thread,
                            author = self.u21,
                            added_at = datetime.datetime.now(),
                            text = 'problem1'
                        )
        self.comment22 = self.problem1.add_comment(
                            user = self.u22,
                            comment = 'comment22'
                        )
        self.comment23 = self.problem1.add_comment(
                            user = self.u23,
                            comment = 'comment23'
                        )
        self.problem2 = models.Post.objects.create_new_problem(
                            thread = self.thread,
                            author = self.u31,
                            added_at = datetime.datetime.now(),
                            text = 'problem2'
                        )
        self.comment32 = self.problem2.add_comment(
                            user = self.u32,
                            comment = 'comment32'
                        )
        self.comment33 = self.problem2.add_comment(
                            user = self.u33,
                            comment = 'comment33'
                        )

    def assertNewResponseCountsEqual(self, counts_vector):
        self.reload_users()
        self.assertEquals(
            [
                self.u11.new_response_count,
                self.u12.new_response_count,
                self.u13.new_response_count,
                self.u14.new_response_count,
                self.u21.new_response_count,
                self.u22.new_response_count,
                self.u23.new_response_count,
                self.u24.new_response_count,
                self.u31.new_response_count,
                self.u32.new_response_count,
                self.u33.new_response_count,
                self.u34.new_response_count,
            ],
            counts_vector
        )

    def assertSeenResponseCountsEqual(self, counts_vector):
        self.reload_users()
        self.assertEquals(
            [
                self.u11.seen_response_count,
                self.u12.seen_response_count,
                self.u13.seen_response_count,
                self.u14.seen_response_count,
                self.u21.seen_response_count,
                self.u22.seen_response_count,
                self.u23.seen_response_count,
                self.u24.seen_response_count,
                self.u31.seen_response_count,
                self.u32.seen_response_count,
                self.u33.seen_response_count,
                self.u34.seen_response_count,
            ],
            counts_vector
        )


    def post_then_delete_problem_comment(self):
        pass

    def post_then_delete_problem(self):
        pass

    def post_then_delete_exercise_comment(self):
        pass

    def post_mention_in_exercise_then_delete(self):
        pass

    def post_mention_in_problem_then_delete(self):
        pass

    def post_mention_in_exercise_then_edit_out(self):
        pass

    def post_mention_in_problem_then_edit_out(self):
        pass

    def test_post_mention_in_comments_then_delete(self):
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        comment = self.exercise.add_comment(
                            user = self.u11,
                            comment = '@user12 howyou doin?',
                            added_at = timestamp
                        )
        comment.delete()
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 0)
        self.assertNewResponseCountsEqual(
            [
                 0, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,
            ]
        )
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        comment = self.problem1.add_comment(
                            user = self.u21,
                            comment = 'hey @user22 blah',
                            added_at = timestamp
                        )
        comment.delete()
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 0)
        self.assertNewResponseCountsEqual(
            [
                 0, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,
            ]
        )

    def test_self_comments(self):
        """poster of the exercise or problem adds a comment
        under the corresponding exercise or problem"""
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.exercise.add_comment(
                            user = self.u11,
                            comment = 'self-comment',
                            added_at = timestamp
                        )
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set([self.u12, self.u13]),
        )
        self.assertNewResponseCountsEqual(
            [
                 0, 1, 1, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,
            ]
        )
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.problem1.add_comment(
                            user = self.u21,
                            comment = 'self-comment 2',
                            added_at = timestamp
                        )
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set([self.u22, self.u23]),
        )
        self.assertNewResponseCountsEqual(
            [
                 0, 0, 0, 0,
                 0, 1, 1, 0,
                 0, 0, 0, 0,
            ]
        )

    def test_self_mention_not_posting_in_comment_to_exercise1(self):
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.exercise.add_comment(
                            user = self.u11,
                            comment = 'self-comment @user11',
                            added_at = timestamp
                        )
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set([self.u12, self.u13]),
        )
        self.assertNewResponseCountsEqual(
            [
                 0, 1, 1, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,
            ]
        )

    def test_self_mention_not_posting_in_comment_to_exercise2(self):
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.exercise.add_comment(
                            user = self.u11,
                            comment = 'self-comment @user11 blah',
                            added_at = timestamp
                        )
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set([self.u12, self.u13]),
        )
        self.assertNewResponseCountsEqual(
            [
                 0, 1, 1, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,
            ]
        )

    def test_self_mention_not_posting_in_comment_to_problem(self):
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.problem1.add_comment(
                            user = self.u21,
                            comment = 'self-comment 1 @user21',
                            added_at = timestamp
                        )
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set([self.u22, self.u23]),
        )
        self.assertNewResponseCountsEqual(
            [
                 0, 0, 0, 0,
                 0, 1, 1, 0,
                 0, 0, 0, 0,
            ]
        )

    def test_responses_clear_after_visit(self):
        """user 14 posts comment under exercise
        user 11, 12, 21, and 22 visit the exercise
        user 13 does not
        the expected outcome is that 11 and 12 have
        0 responses and 13 still has one
        remaining users still have notifications
        """
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.exercise.add_comment(
            user = self.u14,
            comment = 'dudududududu',
            added_at = timestamp
        )
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set([self.u11, self.u12, self.u13])#all users are notified
        )
        self.assertNewResponseCountsEqual(
            [
                1, 1, 1, 0,
                0, 0, 0, 0,
                0, 0, 0, 0,
            ]
        )
        self.assertSeenResponseCountsEqual(
            [
                0, 0, 0, 0,
                0, 0, 0, 0,
                0, 0, 0, 0,
            ]
        )
        self.u11.visit_exercise(self.exercise)
        self.u12.visit_exercise(self.exercise)
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(#visitors are not notified
            set(notifications[0].recipients.all()),
            set([self.u11, self.u12, self.u13])
        )
        self.assertEqual(
            self.u11.activityauditstatus_set.all()[0].status,
            models.ActivityAuditStatus.STATUS_SEEN
        )
        self.assertEqual(
            self.u12.activityauditstatus_set.all()[0].status,
            models.ActivityAuditStatus.STATUS_SEEN
        )
        self.assertEqual(
            self.u13.activityauditstatus_set.all()[0].status,
            models.ActivityAuditStatus.STATUS_NEW
        )
        self.assertNewResponseCountsEqual(
            [
                0, 0, 1, 0,
                0, 0, 0, 0,
                0, 0, 0, 0,
            ]
        )
        self.assertSeenResponseCountsEqual(
            [
                1, 1, 0, 0,
                0, 0, 0, 0,
                0, 0, 0, 0,
            ]
        )


    def test_comments_to_post_authors(self):
        self.exercise.apply_edit(
                        edited_by = self.u14,
                        text = 'now much better',
                        comment = 'improved text'
                    )
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.exercise.add_comment(
                            user = self.u12,
                            comment = 'self-comment 1',
                            added_at = timestamp
                        )
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set([self.u11, self.u13, self.u14]),
        )
        self.assertNewResponseCountsEqual(
            [
                 1, 0, 1, 1,
                 0, 0, 0, 0,
                 0, 0, 0, 0,
            ]
        )
        self.problem1.apply_edit(
                        edited_by = self.u24,
                        text = 'now much better',
                        comment = 'improved text'
                    )
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.problem1.add_comment(
                            user = self.u22,
                            comment = 'self-comment 1',
                            added_at = timestamp
                        )
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set([self.u21, self.u23, self.u24]),
        )
        self.assertNewResponseCountsEqual(
            [
                 0, 0, 0, 0,
                 1, 0, 1, 1,
                 0, 0, 0, 0,
            ]
        )

    def test_exercise_edit(self):
        """when exercise is edited
        response receivers are exercise authors, commenters
        and problem authors, but not problem commenters
        """
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.exercise.apply_edit(
                        edited_by = self.u14,
                        text = 'waaay better exercise!',
                        comment = 'improved exercise',
                    )
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set([self.u11, self.u12, self.u13, self.u21, self.u31])
        )
        self.assertNewResponseCountsEqual(
            [
                 1, 1, 1, 0,
                 1, 0, 0, 0,
                 1, 0, 0, 0,
            ]
        )
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.exercise.apply_edit(
                        edited_by = self.u31,
                        text = 'waaay even better exercise!',
                        comment = 'improved exercise',
                    )
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set([self.u11, self.u12, self.u13, self.u14, self.u21])
        )
        self.assertNewResponseCountsEqual(
            [
                 1, 1, 1, 1,
                 1, 0, 0, 0,
                 0, 0, 0, 0,
            ]
        )

    def test_problem_edit(self):
        """
        """
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.problem1.apply_edit(
                        edited_by = self.u24,
                        text = 'waaay better problem!',
                        comment = 'improved problem1',
                    )
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set(
                [
                    self.u11, self.u12, self.u13, 
                    self.u21, self.u22, self.u23,
                    self.u31
                ]
            )
        )
        self.assertNewResponseCountsEqual(
            [
                 1, 1, 1, 0,
                 1, 1, 1, 0,
                 1, 0, 0, 0,
            ]
        )

    def test_new_problem(self):
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.problem3 = models.Post.objects.create_new_problem(
                            thread = self.thread,
                            author = self.u11,
                            added_at = timestamp,
                            text = 'problem3'
                        )
        time_end = datetime.datetime.now()
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set(
                [
                    self.u12, self.u13, 
                    self.u21, self.u31
                ]
            )
        )
        self.assertNewResponseCountsEqual(
            [
                 0, 1, 1, 0,
                 1, 0, 0, 0,
                 1, 0, 0, 0,
            ]
        )
        self.reset_response_counts()
        time.sleep(1)
        timestamp = datetime.datetime.now()
        self.problem3 = models.Post.objects.create_new_problem(
                            thread = self.thread,
                            author = self.u31,
                            added_at = timestamp,
                            text = 'problem4'
                        )
        notifications = get_re_notif_after(timestamp)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            set(notifications[0].recipients.all()),
            set(
                [
                    self.u11, self.u12, self.u13, 
                    self.u21
                ]
            )
        )
        self.assertNewResponseCountsEqual(
            [
                 1, 1, 1, 0,
                 1, 0, 0, 0,
                 0, 0, 0, 0,
            ]
        )


