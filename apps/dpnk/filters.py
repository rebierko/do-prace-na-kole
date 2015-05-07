# -*- coding: utf-8 -*-
# Author: Petr Dlouhý <petr.dlouhy@email.cz>
#
# Copyright (C) 2015 o.s. Auto*Mat
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
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from dpnk import models


class CampaignFilter(SimpleListFilter):
    title = _(u"Kampaň")
    parameter_name = u'campaign'
    field='campaign'

    def lookups(self, request, model_admin):
        if not request.subdomain:
            campaigns = [('all', _('All'))]
            campaigns = [('none', _('None'))]
            campaigns += [(c.slug, c.name) for c in models.Campaign.objects.all()]
        else:
            current_campaign = models.Campaign.objects.get(slug=request.subdomain)
            campaigns = [(None, current_campaign.name)]
            campaigns += [(c.slug, c.name) for c in models.Campaign.objects.exclude(slug=request.subdomain)]
            campaigns += [('all', _('All'))]
            campaigns += [('none', _('None'))]
        return campaigns

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        elif self.value():
            campaign = self.value()
        else:
            campaign = request.subdomain
        campaign_queryarg = {self.field + "__slug": campaign}
        none_queryarg = {self.field: None}

        if self.value() == 'none':
            return queryset.filter(**none_queryarg).distinct()
        return queryset.filter(Q(**campaign_queryarg) | Q(**none_queryarg)).distinct()


class CityCampaignFilter(CampaignFilter):
    field = "subsidiaries__teams__campaign"


class SubsidiaryCampaignFilter(CampaignFilter):
    field = 'teams__campaign'


class TripCampaignFilter(CampaignFilter):
    field = 'user_attendance__campaign'


class HasVoucherFilter(SimpleListFilter):
    title = _(u"Má nějaké vouchery")
    parameter_name = u'has_voucher'
    field = 'has_voucher'

    def lookups(self, request, model_admin):
        return [
            ('yes', _('Ano')),
            ('no', _('Ne')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(voucher__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.filter(voucher__isnull=True).distinct()
        return queryset


class HasRidesFilter(SimpleListFilter):
    title = _(u"Má nějaké jízdy")
    parameter_name = u'has_rides'
    field = 'has_rides'

    def lookups(self, request, model_admin):
        return [
            ('yes', _('Ano')),
            ('no', _('Ne')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(user_trips__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.filter(user_trips__isnull=True).distinct()
        return queryset


class IsForCompanyFilter(SimpleListFilter):
    title = _(u"Je vnitrofiremní soutěž")
    parameter_name = u'is_for_company'
    field = 'is_for_company'

    def lookups(self, request, model_admin):
        return [
            ('yes', _('Ano')),
            ('no', _('Ne')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(company__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.exclude(company__isnull=False).distinct()
        return queryset
