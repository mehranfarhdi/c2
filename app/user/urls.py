from django.urls import path

from user import view
app_name = 'user'

urlpatterns = [
    path('create/', view.CreateUserView.as_view(), name='create')
]