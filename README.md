# danborary

ダンボールに入れた本を管理するDjangoアプリです。

　  

## 環境

- mac / Windows
- Python 3.8
- Django 3.1.4
- Django REST framework 3.12.2
- django-datatables-view 1.19.1
- reportlab 3.5.56
- pyndlsearch 1.0
- jQuery 3.5.1
- Bootstrap 4.5.2

　  

## 機能

- ダンボールに管理用バーコードを貼り付けるため、印刷用バーコードラベルをpdf形式で作成する
- 書籍のISBNを元に、国立国会図書館サーチの検索APIを使い、タイトルなどを取得する
- ダンボールの管理用バーコードと書籍のISBNを紐付けて、SQLiteへ保存する
- ダンボールに詰めた本は、jQuery Datatablesによりグリッドで表示する
- できる限り、バーコードの読み取りだけで保存までできるUIにする

　  
## 関係するBlog

[ダンボールに入れた本を管理するDjangoアプリ「danborary」を作った - メモ的な思考的な](https://thinkami.hatenablog.com/entry/2020/12/28/120432)