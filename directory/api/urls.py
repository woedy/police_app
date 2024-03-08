from django.urls import path

from directory.api.views import add_directory_view, delete_directory_view, get_all_directories_view, \
    review_directory_view

app_name = 'directory'

urlpatterns = [
    path('add-directory/', add_directory_view, name="add_directory_view"),
    path('delete-directory/', delete_directory_view, name="delete_directory_view"),
    path('get-directories/', get_all_directories_view, name="get_all_directories_view"),
    path('add-directory-review/', review_directory_view, name="review_directory_view"),


]
