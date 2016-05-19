from __future__ import absolute_import

from . import util
from .models import UserAttendance, GpxFile, Competition
from .rest_ecc import gpx_files_post
from .results import recalculate_result_competitor_nothread
from celery import shared_task
import denorm


@shared_task(bind=True)
def recalculate_competitor_task(self, user_attendance_pk):

    user_attendance = UserAttendance.objects.get(pk=user_attendance_pk)
    util.rebuild_denorm_models([user_attendance.team])
    denorm.flush()
    recalculate_result_competitor_nothread(user_attendance)


@shared_task(bind=True)
def send_ecc_tracks(self):
    gpx_files = GpxFile.objects.filter(
        trip__commute_mode='bicycle',
        ecc_last_upload__isnull=True,
        user_attendance__team__subsidiary__city__slug='praha',
        user_attendance__payment_status='done',
        user_attendance__campaign__slug='dpnk2016'
    )

    count = gpx_files_post(gpx_files)
    return count


@shared_task(bind=True)
def recalculate_competitions_results(self, queryset=None):
    if not queryset:
        queryset = Competition.objects.filter(campaign__slug='dpnk2016')
    count = queryset.count()
    for competition in queryset:
        competition.recalculate_results()
    return count


@shared_task(bind=True)
def touch_items(self, queryset):
    return util.rebuild_denorm_models(queryset)


@shared_task(bind=True)
def touch_user_attendances(self, queryset=None):
    queryset = UserAttendance.objects.filter(campaign__slug='dpnk2016')
    return util.rebuild_denorm_models(queryset)


@shared_task(bind=True)
def touch_teams(self, queryset=None):
    queryset = UserAttendance.objects.filter(campaign__slug='dpnk2016')
    return util.rebuild_denorm_models(queryset)
