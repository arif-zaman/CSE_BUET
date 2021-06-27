import os
from forums import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',

    # Site Admin URL
    url(r'^admin/', include(admin.site.urls)),

    # Home URL
    url(r'^lightshare.com/', 'homes.views.home'),
    url(r'^lightshare/userhome/', 'homes.views.mhome'),
    url(r'^lightshare/notications/', 'homes.views.noti'),
    url(r'^lightshare/all_groups/', 'homes.views.all'),
    url(r'^lightshare/search_result/page/(?P<page_id>\d+)/(?P<str>\D+)/', 'homes.views.search'),
    url(r'^lightshare/recommended_groups/', 'homes.views.recommended'),
    url(r'^lightshare/ad_mod_groups/', 'homes.views.admod'),

    # Profile URL
    url(r'^lightshare/user/profile/(?P<user_id>\d+)/', 'profiles.views.profile'),
    url(r'^lightshare/profile/edit/(?P<user_id>\d+)/', 'profiles.views.edit_profile'),

    # SignUp URL
    url(r'^lightshare/signup/(?P<str>\D+)/', 'signups.views.signup'),
    url(r'^lightshare/signup_success/', 'signups.views.signup_success'),

    # Login URL
    url(r'^lightshare/login/', 'logins.views.login'),
    url(r'^lightshare/auth/', 'logins.views.auth_view'),
    url(r'^lightshare/loggedin/', 'logins.views.loggedin'),
    url(r'^lightshare/logout/', 'logins.views.logout'),
    url(r'^lightshare/invalid/', 'logins.views.invalid_login'),

    # Forum URL
    url(r'^lightshare/(?P<group_id>\d+)/home/', 'forums.views.ghome'),
    url(r'^lightshare/(?P<group_id>\d+)/dashboard/', 'forums.views.dashboard'),
    url(r'^lightshare/(?P<group_id>\d+)/makeadmin/', 'forums.views.make_adm'),
    url(r'^lightshare/(?P<group_id>\d+)/makemoderator/', 'forums.views.make_mod'),
    url(r'^lightshare/(?P<group_id>\d+)/search_result/page/(?P<page_id>\d+)/(?P<str>\D+)/', 'forums.views.search'),
    url(r'^lightshare/(?P<group_id>\d+)/(?P<str>\D+)/accept/', 'forums.views.accept'),
    url(r'^lightshare/(?P<group_id>\d+)/(?P<str>\D+)/ignore/', 'forums.views.ignore'),
    url(r'^lightshare/(?P<group_id>\d+)/page/(?P<page_id>\d+)/', 'forums.views.gpage'),
    url(r'^lightshare/(?P<group_id>\d+)/new_post/', 'forums.views.cpost'),
    url(r'^lightshare/(?P<group_id>\d+)/(?P<post_id>\d+)/edit_post/', 'forums.views.post_edit'),
    url(r'^lightshare/(?P<group_id>\d+)/(?P<post_id>\d+)/$', 'forums.views.gpost'),
    url(r'^lightshare/(?P<group_id>\d+)/(?P<post_id>\d+)/likes', 'forums.views.plike'),
    url(r'^lightshare/(?P<group_id>\d+)/(?P<post_id>\d+)/ulikes', 'forums.views.ulike'),
    url(r'^lightshare/(?P<group_id>\d+)/profile/', 'forums.views.gprofile'),
    url(r'^lightshare/(?P<group_id>\d+)/add_fav/', 'forums.views.add_fav'),
    url(r'^lightshare/(?P<group_id>\d+)/rem_fav/', 'forums.views.rem_fav'),
    url(r'^lightshare/(?P<group_id>\d+)/member/', 'forums.views.member'),
    url(r'^lightshare/(?P<group_id>\d+)/jgroup/(?P<status>\d+)/', 'forums.views.jgroup'),
    url(r'^lightshare/(?P<group_id>\d+)/lgroup/', 'forums.views.lgroup'),
    url(r'^lightshare/(?P<group_id>\d+)/egroup/', 'forums.views.edit_group'),
    url(r'^lightshare/(?P<group_id>\d+)/delete_group/', 'forums.views.delete_group'),
    url(r'^lightshare/(?P<group_id>\d+)/(?P<post_id>\d+)/dpost/', 'forums.views.post_delete'),
    url(r'^lightshare/(?P<group_id>\d+)/(?P<post_id>\d+)/ppost/', 'forums.views.post_pin'),
    url(r'^lightshare/(?P<group_id>\d+)/(?P<post_id>\d+)/uppost/', 'forums.views.post_upin'),
    url(r'^lightshare/select_category/', 'forums.views.scategory'),
    url(r'^lightshare/create_group/(?P<cat_id>\d+)/', 'forums.views.cgroup'),

    # About URL
    url(r'^lightshare/about/', 'abouts.views.about'),
    url(r'^lightshare/privacy/', 'abouts.views.privacy'),
    url(r'^lightshare/term/', 'abouts.views.term'),

    # Setting URL
    url(r'^lightshare/feedback/', 'settings.views.report'),
    url(r'^lightshare/privacy_setting/', 'settings.views.privacy'),
    url(r'^lightshare/change_password/(?P<str>\D+)/', 'settings.views.chpass'),
    url(r'^lightshare/deactivate/(?P<str>\D+)/', 'settings.views.deactive'),

    # Welcome Page URL
    url(r'^$', 'abouts.views.welcome'),
)


handler404 = 'homes.views.custom404'
handler500 = 'homes.views.custom500'


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
       document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
       document_root=settings.MEDIA_ROOT)