from django.urls import path
from . import views
urlpatterns = [
    path('issue-book', views.issue_book, name = "issue_book"),
    path('create-issue-book', views.create_issue_book, name = "create_issue_book"),
    path('edit-issue-book/<int:pk>', views.edit_issue_book, name = "edit_issue_book"),
    path('detail-issue-book/<int:pk>', views.detail_issue_book, name = "detail_issue_book"),
    path('delete/<int:pk>', views.delete_issue_book, name = "delete_issue_book"),
    path('update-issue-book/<int:pk>', views.update_issue_book, name = "update_issue_book"),
    path('search', views.search, name = "search"),
]