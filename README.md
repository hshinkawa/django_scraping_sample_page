# django_scraping_sample_page

Python Djangoを用いたスクレイピングアプリ
 
特定の旅行サイトのツアーURLと取得したい☆の数を指定すると，該当するレビューを全てリスト化します．
 
# Features
 
該当レビューをリスト化したページの出力に加えて，ダウンロードリンクも備えております．
また，ユーザ認証機能を付けており，ユーザ登録した人のみ全てのページを閲覧することができる形式にし，安全性を高めています．
さらに，ユーザがパスワードを忘れた際のパスワードリセットメールの送信やそれに伴うデータベースの更新も自動で行います．
 
# Requirement
 
"hoge"を動かすのに必要なライブラリなどを列挙する
 
* asgiref==3.3.0
* beautifulsoup4==4.9.3
* bs4==0.0.1
* Django==3.0.2
* django-crispy-forms==1.10.0
* numpy==1.20.0
* pandas==1.2.1
* Pillow==8.1.0
* python-dateutil==2.8.1
* pytz==2020.4
* six==1.15.0
* soupsieve==2.1
* sqlparse==0.4.1

# Installation
  
```bash
pip install -r requirements.txt
```
 
# Usage
 
django_project_web/django_project_web/settings.pyにSECRET_KEYとEMAIL_HOST_USER, EMAIL_HOST_PASSWORDを追加する必要があります．
EMAIL HOSTとしては，例えば，gmailとそのアプリパスワードなどをご利用ください．
 
```bash
git clone https://github.com/hshinkawa/django_scraping_sample_page.git
cd django_project_web
pip install -r requirements.txt
python manage.py runserver
```
 
# Note

スクレイピング先のサーバに負荷がかからない範囲でご利用ください．