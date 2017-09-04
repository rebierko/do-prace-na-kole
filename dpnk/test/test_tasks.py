# -*- coding: utf-8 -*-

# Author: Petr Dlouhý <petr.dlouhy@auto-mat.cz>
#
# Copyright (C) 2017 o.s. Auto*Mat
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
import datetime

from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings

from dpnk import tasks

from model_mommy import mommy

from .mommy_recipes import UserAttendanceRecipe, testing_campaign


@override_settings(
    FAKE_DATE=datetime.date(2017, 5, 8),
)
class TestSendUnfilledRidesNotification(TestCase):
    def setUp(self):
        super().setUp()
        mommy.make(
            "price_level.PriceLevel",
            takes_effect_on=datetime.date(year=2010, month=2, day=1),
            price=100,
            pricable=testing_campaign,
        )

    def test_notification(self):
        """ Test that email is send, if the user has't got rides in last 5 days """
        self.user_attendance = UserAttendanceRecipe.make(
            campaign=testing_campaign,
            team__campaign=testing_campaign,
            approved_for_team='approved',
            userprofile__user__email='test@test.cz',
            user_trips=[
                mommy.make(
                    'Trip',
                    date='2017-05-02',
                    commute_mode_id=1,
                    direction='trip_to',
                ),
            ],
            transactions=[
                mommy.make(
                    "Payment",
                    status=99,
                    realized=datetime.date(2017, 2, 1),
                    amount=100,
                ),
            ],
        )
        self.user_attendance.save()
        mail.outbox = []
        mail_count = tasks.send_unfilled_rides_notification(campaign_slug="testing-campaign")
        self.assertEqual(mail_count, 1)
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.recipients(), ['test@test.cz'])
        self.assertEqual(str(mail.outbox[0].subject), "Testing campaign - připomenutí nevyplněných jízd")

    def test_notification_with_rides(self):
        """ Test that no email is send, if the user has recent rides """
        self.user_attendance = UserAttendanceRecipe.make(
            campaign=testing_campaign,
            team__campaign=testing_campaign,
            approved_for_team='approved',
            user_trips=[
                mommy.make(
                    'Trip',
                    date='2017-05-03',
                    commute_mode_id=1,
                    direction='trip_to',
                ),
            ],
            transactions=[
                mommy.make(
                    "Payment",
                    status=99,
                    realized=datetime.date(2017, 2, 1),
                    amount=100,
                ),
            ],
        )
        self.user_attendance.save()
        mail_count = tasks.send_unfilled_rides_notification(campaign_slug="testing-campaign")
        self.assertEqual(mail_count, 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_notification_not_paid(self):
        """ Test that email is send, if the user didn't pay. """
        self.user_attendance = UserAttendanceRecipe.make(
            campaign=testing_campaign,
            team__campaign=testing_campaign,
            approved_for_team='approved',
            user_trips=[
                mommy.make(
                    'Trip',
                    date='2017-05-02',
                    commute_mode_id=1,
                    direction='trip_to',
                ),
            ],
        )
        self.user_attendance.save()
        mail_count = tasks.send_unfilled_rides_notification(campaign_slug="testing-campaign")
        self.assertEqual(mail_count, 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_notification_pks(self):
        """ Test that email is send, if the user has't got rides in last 5 days """
        self.user_attendance = UserAttendanceRecipe.make(
            campaign=testing_campaign,
            team__campaign=testing_campaign,
            approved_for_team='approved',
            userprofile__user__email='test@test.cz',
            user_trips=[
                mommy.make(
                    'Trip',
                    date='2017-05-02',
                    commute_mode_id=1,
                    direction='trip_to',
                ),
            ],
            transactions=[
                mommy.make(
                    "Payment",
                    status=99,
                    realized=datetime.date(2017, 2, 1),
                    amount=100,
                ),
            ],
        )
        self.user_attendance.save()
        mail_count = tasks.send_unfilled_rides_notification(
            pks=[self.user_attendance.id],
            campaign_slug="testing-campaign",
        )
        self.assertEqual(mail_count, 1)
