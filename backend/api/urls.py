from django.urls import path
from .views import signup, verify_email, login_view, supervise

urlpatterns = [
    # path('greet/', greet_view),
    # path('signup/', signup_view),
    # path('verify-email/<int:user_id>/', verify_email),
    # path('register/', register, name='register'),
    path('signup/', signup),
    path('verify_email/<str:verification_code>/', verify_email),
    path('login/', login_view),
    path('supervise/', supervise),
]
