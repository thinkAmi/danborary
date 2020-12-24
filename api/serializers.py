from rest_framework import serializers

from api.models import Ndl, Book


class PackingSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = Book
        fields = ['isbn', 'box', 'title', 'creator', 'publisher']

    def create(self, validated_data):
        isbn = validated_data.pop('isbn')
        ndl = Ndl.objects.filter(isbn=isbn)
        validated_data['ndl'] = ndl.get() if ndl.exists() else None

        return super().create(validated_data)
