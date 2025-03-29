from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .views import *

# A ordem das urls é importante por causa do slug, quando existir.
user_patterns = [
    path('', user_list, name='user_list'),  # noqa E501
    path('create/', user_create, name='user_create'),  # noqa E501
    path('<int:pk>/', user_detail, name='user_detail'),  # noqa E501
    path('<int:pk>/update/', user_update, name='user_update'),  # noqa E501
]

urlpatterns = [
    path('', MyLoginView.as_view(), name='login'),  # noqa E501
    path('logout/', LogoutView.as_view(), name='logout'),  # noqa E501
    path('register/', signup, name='signup'),  # noqa E501
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirm.as_view(), name='password_reset_confirm'),  # noqa E501
    path('reset/done/', MyPasswordResetComplete.as_view(), name='password_reset_complete'),  # noqa E501
    path('password_reset/', MyPasswordReset.as_view(), name='password_reset'),  # noqa E501
    path('password_reset/done/', MyPasswordResetDone.as_view(), name='password_reset_done'),  # noqa E501
    path('users/', include(user_patterns)),
]
