from django.conf.urls import patterns, include, url

from django.conf import settings
import views
import company_admin_views
from django.contrib.auth.decorators import login_required
from decorators import must_be_company_admin, must_be_in_phase, must_be_in_group, login_required_simple, must_be_competitor, must_have_team

campaign_urlpatterns = patterns(
    '',
    url(r'^tym/$',
        views.change_team,
        {'success_url': 'profil'}),
    url(r'^tym/(?P<token>[0-9A-Za-z]+)/(?P<initial_email>[^&]+)/$$',
        views.ConfirmTeamInvitationView.as_view(),
        ),
    url(r'^registrace/$',
        must_be_in_phase("registration")(views.RegistrationView.as_view()),
        {'success_url': 'typ_platby'}),
    url(r'^header_bar/$',
        views.header_bar),
    url(r'^registrace/(?P<token>[0-9A-Za-z]+)/(?P<initial_email>[^&]+)/$$',
        must_be_in_phase("registration")(views.RegistrationView.as_view()),
        {'success_url': 'typ_platby'}),
    url(r'^pozvanky/$',
        views.invite,
        {'success_url': 'typ_platby'}),
    url(r'^zaslat_zadost_clenstvi/$',
        views.team_approval_request),
    url(r'^profil/$',
        views.profile),
    url(r'^dalsi_clenove/$',
        views.other_team_members),
    url(r'^dalsi_clenove_vysledky/$',
        views.other_team_members,
        {'template': 'registration/team_members_results.html'},
        ),
    url(r'^jizdy/$',
        views.rides),
    url(r'^profil_pristup/$',
        views.profile_access),
    url(r'^team_admin_team/$',
        views.team_admin_team,
        {'success_url': 'profil'}),
    url(r'^team_admin_members/$',
        views.team_admin_members,
        ),
    url(r'^prihlasky/$',
        views.admissions,
        {'template': 'registration/admissions.html'}),
    url(r'^competitions/$',
        views.competitions,
        ),
    url(r'^vysledky_souteze/(?P<competition_slug>[0-9A-Za-z_\-]+)/$',
        views.competition_results,
        {'template': 'registration/competition_results.html'}),
    url(r'^vysledky_souteze/(?P<competition_slug>[0-9A-Za-z_\-]+)/(?P<limit>[0-9]+)/$',
        views.competition_results,
        {'template': 'registration/competition_results.html'}),
    url(r'^otazka/(?P<questionaire_slug>[0-9A-Za-z_\-]+)/$',
        views.questionaire),
    url(r'^upravit_profil/$',
        login_required_simple(views.UpdateProfileView.as_view())),
    url(r'^zmenit_triko/$',
        views.ChangeTShirtView.as_view(),
        {'success_url': 'typ_platby'}),
    url(r'^typ_platby/$',
        views.payment_type),
    url(r'^platba/$',
        views.payment),
    url(r'^statistika/(?P<variable>[0-9A-Za-z\-]+)/$',
        views.statistics),
    url(r'^denni-graf/$',
        views.daily_chart),
    url(r'^cykloservis/$',
        login_required(must_be_in_group('cykloservis')(views.BikeRepairView.as_view()))),
    url(r'^facebook_app/$',
        views.facebook_app),
    url(r'^package/$',
        views.user_attendance_view,
        {"template": "registration/package.html"}),
    url(r'^package-confirmation/$',
        views.ConfirmDeliveryView.as_view(),
        ),
    url(r'^address/$',
        views.user_attendance_view,
        {"template": "registration/address.html"}),


    #company admin:
    url(r'^spolecnost/zadost_admina/$',
        must_be_competitor(must_have_team(login_required(company_admin_views.CompanyAdminView.as_view())))),
    url(r'^spolecnost/soutez/(?P<competition_slug>[0-9A-Za-z_\-]+)/$',
        must_be_company_admin(login_required(company_admin_views.CompanyCompetitionView.as_view()))),
    url(r'^spolecnost/soutez/$',
        must_be_company_admin(login_required(company_admin_views.CompanyCompetitionView.as_view()))),
    url(r'^struktura_spolecnosti/$',
        company_admin_views.company_structure),
    url(r'^souteze/$',
        company_admin_views.competitions),
    url(r'^faktury/$',
        company_admin_views.invoices),
    url(r'^create_invoice/$',
        company_admin_views.CreateInvoiceView.as_view()),
    url(r'^zaplatit_za_uzivatele/$',
        company_admin_views.SelectUsersPayView.as_view()),
    url(r'^spolecnost/editovat_spolecnost/$',
        must_be_company_admin(login_required(company_admin_views.CompanyEditView.as_view()))),
    url(r'^spolecnost/registrace_admina/$',
        company_admin_views.CompanyAdminApplicationView.as_view()),
)

urlpatterns = patterns(
    '',
    url(r'^platba_status$',
        views.payment_status),
    url(r'^platba_uspesna/(?P<trans_id>[0-9]+)/(?P<session_id>[0-9A-Za-z\-]+)/(?P<pay_type>[0-9A-Za-z]+)/$$',
        views.payment_result,
        {'success': True}),
    url(r'^platba_neuspesna/(?P<trans_id>[0-9]+)/(?P<session_id>[0-9A-Za-z\-]+)/(?P<pay_type>[0-9A-Za-z]+)/(?P<error>[^&]+)/$$',
        views.payment_result,
        {'success': False}),
    url(r'^zapomenute_heslo/$',
        'django.contrib.auth.views.password_reset',
        name='password_reset'),
    url(r'^zapomenute_heslo/odeslano/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_done'),
    url(r'^zapomenute_heslo/zmena/(?P<uidb64>[0-9A-Za-z_]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^zapomenute_heslo/dokonceno/$',
        'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': settings.LOGOUT_NEXT_PAGE}
        ),
    url(r'^logout_redirect/$',
        views.logout_redirect),
    url(r'^login/$',
        views.login),
    url(r'^zmena_hesla/$',
        'django.contrib.auth.views.password_change',
        name='password_change'),
    url(r'^zmena_hesla_hotovo/$',
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'),
    url(r'^(?P<campaign_slug>[0-9A-Za-z_\-]+)/', include(campaign_urlpatterns)),
)
