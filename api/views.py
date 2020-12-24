import time

from pyndlsearch.client import SRUClient
from pyndlsearch.cql import CQL
from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.models import Ndl
from api.serializers import PackingSerializer


class NdlApiView(APIView):
    def get(self, request):
        key = request.GET.get('key')
        if not key:
            return Response(
                data={
                    'isbn': '',
                    'title': '',
                    'creator': '',
                    'publisher': '',
                    'volume': '',
                },
                status=status.HTTP_200_OK)

        # すでに取得済のISBNデータであれば、DBのデータを使う
        ndl = Ndl.objects.filter(isbn=key)

        if ndl.exists():
            return Response(
                data={
                    'isbn': ndl.get().isbn,
                    'title': ndl.get().title,
                    'creator': ndl.get().creator,
                    'publisher': ndl.get().publisher,
                    'volume': ndl.get().volume,
                },
                status=status.HTTP_200_OK)

        # 多重アクセスを回避するため、1秒くらい待つ
        time.sleep(1)

        # NDLのAPIから取得
        cql = CQL()
        cql.isbn = key
        # デフォルトだとマンガは取得できないので、明示的に「国立国会図書館オンライン」を指定
        # ただし、マンガの場合、巻数が取れない
        cql.dpid = 'iss-ndl-opac'
        client = SRUClient(cql)
        client.set_maximum_records(1)

        response = client.get_srresponse()
        if response.numberOfRecords == 0:
            return Response(
                data={
                    'isbn': '',
                    'title': '',
                    'creator': '',
                    'publisher': '',
                    'volume': '',
                },
                status=status.HTTP_404_NOT_FOUND)

        # 1件しか取れない前提
        record = response.records[0].recordData
        ndl = Ndl(isbn=key, title=record.title, creator=record.creator, publisher=record.publisher)
        ndl.save()

        return Response(
            data={
                'isbn': ndl.isbn,
                'title': ndl.title,
                'creator': ndl.creator,
                'publisher': ndl.publisher,
                # 巻数はこの時点では取得できない想定
                'volume': '',
            },
            status=status.HTTP_200_OK)


class PackingApiView(mixins.CreateModelMixin, GenericViewSet):
    queryset = Ndl.objects.all()
    serializer_class = PackingSerializer
