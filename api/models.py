from django.db import models


class Box(models.Model):
    note = models.CharField('備考', max_length=255, null=True, blank=True)


class Ndl(models.Model):
    # ISBNが重複するおそれはあるが、手元の量が少ないので、重複した時に考える
    # また、ISBNは長めに持っておく
    isbn = models.CharField('ISBN', max_length=20, unique=True)
    title = models.CharField('タイトル', max_length=255, null=True, blank=True)
    creator = models.CharField('著者', max_length=255, null=True, blank=True)
    publisher = models.CharField('出版社', max_length=255, null=True, blank=True)


class Book(models.Model):
    ndl = models.ForeignKey('api.Ndl',
                            on_delete=models.SET_NULL, null=True, blank=True)
    box = models.ForeignKey('api.Box',
                            on_delete=models.SET_NULL, null=True, blank=True)

    # ISBNがなかったり、ISBN登録されているものとは異なる値を設定したいかもしれないので、別で持つ
    title = models.CharField('タイトル', max_length=255, null=True, blank=True)
    creator = models.CharField('著者', max_length=255, null=True, blank=True)
    publisher = models.CharField('出版社', max_length=255, null=True, blank=True)

    note = models.CharField('備考', max_length=255, null=True, blank=True)
