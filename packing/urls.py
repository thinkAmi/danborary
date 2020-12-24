from django.urls import path

from packing.views import PackingView, PrintBoxBarcodeView, MenuView

app_name = 'packing'

urlpatterns = [
    path('', MenuView.as_view(), name='menu'),
    path('box/<int:box_number>/', PackingView.as_view(), name='box'),
    path('print/start/<int:start_id>/', PrintBoxBarcodeView.as_view(), name='print'),
]
