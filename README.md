# redmine-issue-registerd

## 概要

メールサーバからPOPでメールを受信し、Redmineのイシュー（チケット）へ登録します。

### 動作環境

Language: Python 2.x    
Platform: LinuxOS  
Library: python-redmine  

### 設定ファイル

* redmine_ird.conf 

```text
[global]
target=redmine1
mail_path=/root/Maildir

[redmine1]
url=http://192.168.1.34:10083
username=admin
password=admin
key=発行された値

[subject]
test=[test]
```

### テスト

DockerでのRedimneの構築から動作確認までを説明します。

* dockerのインストール  
```bash
$ yum install docker-io -y
```

* postgresqlイメージの起動  
```bash
$ docker run --name=postgresql-redmine -d \
  --env='DB_NAME=redmine_production' \
  --env='DB_USER=redmine' --env='DB_PASS=password' \
  --volume=/srv/docker/redmine/postgresql:/var/lib/postgresql \
  sameersbn/postgresql:9.4-12
```

* redmineイメージの起動  
```bash
$ docker run --name=redmine -d \
  --link=postgresql-redmine:postgresql --publish=10083:80 \
  --env='REDMINE_PORT=10083' \
  --volume=/srv/docker/redmine/redmine:/home/redmine/data \
  sameersbn/redmine:3.2.0-4
```

* コンテナ稼働確認  
```bash
$ docker ps
CONTAINER ID        IMAGE                         COMMAND                CREATED             STATUS              PORTS                            NAMES
46ccc3e89fb4        sameersbn/redmine:3.2.0-4     "/sbin/entrypoint.sh   2 minutes ago       Up 2 minutes        443/tcp, 0.0.0.0:10083->80/tcp   redmine
e0288efaf27d        sameersbn/postgresql:9.4-12   "/sbin/entrypoint.sh   2 minutes ago       Up 2 minutes        5432/tcp                         postgresql-redmine
```

* WebブラウザからRedmineへアクセス

http://IPアドレス:10081/

username: admin  
password: admin  

* redmineで以下を実施
 - プロジェクトの作成
 - サービス有効化
 RESTによるWebサービスを有効にする  
 JSONPを有効にする  
 - APIキーの作成
 
### 参考

* [sameersbn/redmine](https://hub.docker.com/r/sameersbn/redmine/#internal-mysql-server)  
