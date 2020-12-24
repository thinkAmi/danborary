from django.urls import path

from datatables.views import BookDataTableView

urlpatterns = [
    path('books/', BookDataTableView.as_view(), name='datatables-books'),
]
