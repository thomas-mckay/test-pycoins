from django.urls import path, include

from pycoins.api.endpoints import alert


urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),

    path(
        'users/<int:user_pk>/alerts/',
        alert.AlertList.as_view(),
        name='alert-list',
    ),
    path(
        'users/<int:user_pk>/alerts/<int:pk>/',
        alert.AlertDetail.as_view(),
        name='alert-detail',
    ),
]
