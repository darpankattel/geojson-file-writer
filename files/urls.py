from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="list-files"),
    path("<int:file_id>/", views.detail, name="detail-file"),
    path("<int:file_id>/mark-complete/",
         views.markComplete, name="mark-complete"),
    path("<int:file_id>/chunk/", views.addChunk, name="add-chunk"),
    path("<int:file_id>/chunk/<int:chunk_id>/edit/",
         views.editChunk, name="edit-chunk"),
    path("<int:file_id>/chunk/<int:chunk_id>/delete/",
         views.deleteChunk, name="delete-chunk"),
    path("download/<int:file_id>/", views.download, name="download-file"),
    path("create/", views.create, name="create-file"),
]
