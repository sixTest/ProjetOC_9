from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('inscription', views.inscription, name='inscription'),
    path('flux', views.flux, name='flux'),
    path('creation_ticket', views.creation_ticket, name='creation_ticket'),
    path('creation_review_without_ticket', views.creation_review_without_ticket,
         name='creation_review_without_ticket'),
    path('creation_review', views.creation_review, name='creation_review'),
    path('posts', views.posts, name='posts'),
    path('following', views.following, name='following'),
    path('modification_ticket', views.modification_ticket, name='modification_ticket'),
    path('modification_review', views.modification_review, name='modification_review')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
