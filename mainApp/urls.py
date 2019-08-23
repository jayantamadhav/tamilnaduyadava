from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),														        #Main Landing page
    path('feed', views.feed, name="feed" ),													        #User feed page
    path('manage_profile', views.manage_profile, name="manage_profile"),				            #Edit profile page
    path('ajax_profile_update', views.ajax_profile_update, name='ajax_profile_update'),		       #Ajax update profile
    path('ajax_profile_pic_update', views.ajax_profile_pic_update, name='ajax_profile_pic_update'),#Ajax update profile picture
    path('deactivate_user', views.deactivate_user, name='deactivate_user'),					        #Deactivate the user
    path('about_us', views.about_us, name='about_us'), 										       #About Us page
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),					       #Privacy Policy page
    path('privacy_policy_external', views.privacy_policy_external, name='privacy_policy_external'),#Privacy Policy page for not registered customer
    path('view_profile/<int:id>', views.view_profile, name="view_profile"),					       #View other's profile
    path('sort_by/<str:key>/<str:value>', views.sort_by, name="sort_by"),					       #Sort by rasi or nakshatra
    path('change_password', views.change_password, name="change_password"),                        #Password change view
    path('update_preference', views.update_preference, name="update_preference"),                  #Update User Preference
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
