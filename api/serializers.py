from rest_framework import serializers

from api.models import Ndl, Book, Box


class PackingSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(max_length=20, write_only=True)
    volume = serializers.IntegerField(write_only=True, allow_null=True)
    number = serializers.IntegerField(write_only=True)

    class Meta:
        model = Book
        fields = ['isbn', 'volume', 'number', 'title', 'creator', 'publisher']

    def create(self, validated_data):
        isbn = validated_data.pop('isbn')
        ndls = Ndl.objects.filter(isbn=isbn)
        if ndls.exists():
            # データは1件しかない前提
            ndl = ndls.get()
            volume = validated_data.pop('volume')
            if volume:
                ndl.volume = volume
                ndl.save()

            validated_data['ndl'] = ndl

        # 箱は必ずある前提
        validated_data['box'] = Box.objects.get(number=validated_data.pop('number'))

        return super().create(validated_data)
