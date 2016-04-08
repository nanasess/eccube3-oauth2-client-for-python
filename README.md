EC-CUBE3 OAuth2.0 Client for Python
=====================================

Setup
------

```
$ virtualenv venv && source venv/bin/activate
(venv)$ pip install requests-oauthlib flask
(venv)$ python eccube3_flask_oauth2.py
```


```
### 以下の変数を設定してください
client_id = "<client id>"
client_secret = "<client secret>"
authorization_base_url = 'https://<eccube-host>/admin/OAuth2/v0/authorize'
token_url = 'https://<eccube-host>/OAuth2/v0/token'
api_url = 'https://<eccube-host>/v0/productsauthsample/1'
```

`redirect_uri` は http://127.0.0.1:5000/callback を指定してください

See Also
---------

<https://gist.github.com/ib-lundgren/6507798>
