from django.urls import path,include
from .views import *



urlpatterns = [
    path('incident/', IncidentAPIview.as_view()),
    path('incident/<incident_id>/', IncidentAPIview.as_view()),
    path('registration/', RegistrationAPIview.as_view()),
    path('login/', LoginAPIview.as_view()),
    path('change-password/', ChangeUserPasswordAPIView.as_view()),
    path('send-password-reset-link/', SendPasswordResetLinkAPIView.as_view()),
    path('reset-password/<uid>/<token>/', CompletePasswordResetAPIView.as_view()),
]

