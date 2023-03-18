
## このリポジトリについて
Docker + Python + endoflife.dateのAPIを利用して、サポート期限前にSlackに通知を行うものです。  

## 準備
### envの設定
```
cp .env.example .env
```

`.env` に下記を設定する。
- `WEB_HOOK_URL` : Slackの通知URL
- `NOTIFICATION_PRODUCTS` : 製品を指定する
- `NOTIFICATION_PRODUCTS_VERSION` : 製品とバージョンを指定する
- `NOTIFICATION_BEFORE_DEADLINE_DAYS` : サポート期限 ○日前に通知を行う日を設定する

例:
```
# SlackのwebhookURL
WEB_HOOK_URL=https://XXXXXXX

# 各製品のすべての情報を通知
NOTIFICATION_PRODUCTS='php mysql Apache AlmaLinux'

# PHP 8.0, MySQL8.0, Apache2.4, AlmaLinux8 の製品とバージョンの組み合わせについてEOLを通知
NOTIFICATION_PRODUCTS_VERSION='php=8.0 mysql=8.0 Apache=2.4 AlmaLinux=8'

# 10日前、20日前、30日前、40日前、50日前に通知
NOTIFICATION_BEFORE_DEADLINE_DAYS='10 20 30 40 50'
```

### crontab.txt
デフォルトでは下記のようになっています。
引数に `notify_version` を入れることで、製品とバージョンの組み合わせの通知を行うことができます。
```
0 7 * * * echo "Current date is `date`" > /var/src/app/check.log 2>&1
0 7 * * * cd /var/src/app && /usr/local/bin/python app.py notify_version >> /var/src/app/cron.log 2>&1
```

## 使い方
1. このリポジトリをcloneします。
```
git clone https://github.com/katsuobushiFPGA/eol-notify-python.git
```
2. イメージをビルドし、立ち上げます。
```
docker compose up -d
```
## トラブルシューティング
※ `crontab.txt` は `LF` コードにすること。
`CRLF` で 作成した場合は、下記のようなエラーが出てcronのjobが実行されない。 (実行される前に exitされる)
```
INFO reaped unknown pid 11 (exit status 0)
```