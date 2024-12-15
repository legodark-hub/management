from django.urls import path, include

from users.views import ChangeUserRoleView

urlpatterns = [
    path('auth/', include('djoser.urls')),    
    path('auth/', include('djoser.urls.jwt')),
    path('change-role/<int:user_id>/', ChangeUserRoleView.as_view(), name='change-role'),
]
