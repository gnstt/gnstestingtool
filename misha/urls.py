from django.contrib import admin
from django.urls import path
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', about),
    path('', home),
    path('login/', login_user),
    path('logout/', logout_user),
    path('register/', register),
    path('createchecklist/', createchecklist),
    path('listofcases/', listofcases),
    path('checklist/<int:id>', checklist),
    path('finish_checklist/<int:checklist_id>', finish_checklist),
    path('toggle_status/<int:id>/', toggle_status),
    path('toggle_action/<int:action_id>/<int:checklist_id>/', toggle_action),
    path('home/', home),
    path('add_note/', add_note),
    path('remove_checklist/<int:checklist_id>/', remove_checklist),
]



