from django.shortcuts import render

# Create your views here.
from django_datatables_view.base_datatable_view import BaseDatatableView

from api.models import Book


class BookDataTableView(BaseDatatableView):
    model = Book
    columns = [
        'id',
        'ndl__isbn',
        'title',
        'ndl__volume',
        'creator',
        'publisher',
    ]
    order_columns = columns
    max_display_length = 100

    def render_column(self, row, col):
        if col == 'ndl__isbn':
            return row.ndl.isbn
        if col == 'ndl__volume':
            return row.ndl.volume
        return super().render_column(row, col)

    def filter_queryset(self, qs):
        # boxで常に絞る
        box = self._querydict.get('box')
        if box:
            qs = qs.filter(box__id=box)

        return super().filter_queryset(qs)
