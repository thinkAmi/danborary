from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from reportlab.graphics.barcode import code39
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from api.models import Box


class MenuView(TemplateView):
    template_name = 'packing/menu.html'


class PackingView(TemplateView):
    template_name = 'packing/packing.html'

    def get(self, request, *args, **kwargs):
        box_number = kwargs.get('box_number')

        # Boxが存在しない場合はエラーとせずにデータを作成する
        # (Boxのバーコード生成は容易なため、Boxの存在チェックは厳しく行わない)
        Box.objects.get_or_create(number=box_number)

        return super().get(request, *args, **kwargs)


class PrintBoxBarcodeView(View):
    # portraitで原点左上にしたので、縦横が入れ替わった
    LABEL_HEIGHT = 42.4 * mm
    LABEL_WIDTH = 70 * mm

    def get(self, request, start_id, *args, **kwargs):
        # pdf用のContent-TypeやContent-Dispositionをセット
        response = HttpResponse(status=200, content_type='application/pdf')
        response['Content-Disposition'] = f'filename="barcode_start_{start_id}.pdf"'

        self.create_pdf(response, start_id)
        return response

    def create_pdf(self, response, start_id):
        # A4縦書き、原点は左下
        size = portrait(A4)
        doc = canvas.Canvas(response, pagesize=size)
        for i in range(21):
            # ラベル位置
            x = self.LABEL_WIDTH * (i % 3)
            y = self.LABEL_HEIGHT * (i // 3)

            # ラベル印刷
            self.draw_label(doc, x, y, str(start_id + i))

        doc.save()

    def draw_label(self, doc, x, y, data):
        doc.setLineWidth(0.5)
        # 目安の枠線(デバッグ用)
        # doc.rect(x, y, self.LABEL_WIDTH, self.LABEL_HEIGHT, stroke=1, fill=0)

        # おおよそラベルの中央に来るよう、位置を調整
        doc.drawString(x + self.LABEL_HEIGHT / 2 + 10*mm, y + self.LABEL_WIDTH / 2 - 5*mm, data)

        # Code39のバーコードも、位置を調整
        barcode = code39.Standard39(f'*{data}*',
                                    barWidth=0.3*mm,
                                    barHeight=6.35*mm,
                                    checksum=False)
        barcode.drawOn(doc, x + 15*mm, y + 18*mm)
