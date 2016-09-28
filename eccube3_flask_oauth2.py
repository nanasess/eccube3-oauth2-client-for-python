from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

app = Flask(__name__)

### see also https://gist.github.com/ib-lundgren/6507798

# This information is obtained upon registration of a new Eccube
client_id = "<client id>"
client_secret = "<client secret>"
authorization_base_url = 'https://<eccube-host>/admin/OAuth2/v0/authorize'
token_url = 'https://<eccube-host>/OAuth2/v0/token'
api_url = 'https://<eccube-host>/api/v0/product/1'

scope = [
    "product_read",
    "product_write"
]
redirect_uri = 'http://127.0.0.1:5000/callback';

## for http
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Eccube)
    using an URL with a few key OAuth parameters.
    """
    eccube = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = eccube.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    eccube = OAuth2Session(client_id, state=session['oauth_state'],
                           redirect_uri=redirect_uri)
    token = eccube.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /product.
    session['oauth_token'] = token

    return redirect(url_for('.product'))


@app.route("/product", methods=["GET"])
def product():
    """Fetching a protected resource using an OAuth 2 token.
    """
    eccube = OAuth2Session(client_id, token=session['oauth_token'],
                           redirect_uri=redirect_uri)
    return jsonify(eccube.get(api_url).json())


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True)
