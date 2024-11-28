import json
import sys
from urllib import request
from urllib.parse import parse_qsl

import oauth2 as oauth


consumer_key = "BJjfyJvWXIhCNFwiQikv"
consumer_secret = "TQEmFPWFdczCJetExWHdDPOHgYSXDBim"

# The following oauth end-points are defined by discogs.com staff. These static endpoints
# are called at various stages of oauth handshaking.
request_token_url = "https://api.discogs.com/oauth/request_token"
authorize_url = "https://www.discogs.com/oauth/authorize"
access_token_url = "https://api.discogs.com/oauth/access_token"

# A user-agent is required with Discogs API requests. Be sure to make your user-agent
# unique, or you may get a bad response.
user_agent = "apollo/1.0"

# create oauth Consumer and Client objects using
consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)

# pass in your consumer key and secret to the token request URL. Discogs returns
# an ouath_request_token as well as an oauth request_token secret.
resp, content = client.request(
    request_token_url, "POST", headers={"User-Agent": user_agent}
)

# we terminate if the discogs api does not return an HTTP 200 OK. Something is
# wrong.
if resp["status"] != "200":
    sys.exit("Invalid response {0}.".format(resp["status"]))

request_token = dict(parse_qsl(content.decode("utf-8")))

print(" == Request Token == ")
print(f'    * oauth_token        = {request_token["oauth_token"]}')
print(f'    * oauth_token_secret = {request_token["oauth_token_secret"]}')
print()

resp, content = client.request(
    access_token_url, "POST", headers={"User-Agent": user_agent}
)
access_token = dict(parse_qsl(content.decode("utf-8")))



token = oauth.Token(
    key=access_token["oauth_token"], secret=access_token["oauth_token_secret"]
)
client = oauth.Client(consumer, token)

resp, content = client.request(
    "https://api.discogs.com/database/search?release_title=House+For+All&artist=Blunted+Dummies", #Change This URL For Search
    headers={"User-Agent": user_agent},
)

if resp["status"] != "200":
    sys.exit("Invalid API response {0}.".format(resp["status"]))

releases = json.loads(content.decode("utf-8"))
print("\n== Search results for release_title=House For All, Artist=Blunted Dummies ==")
for release in releases["results"]:
    print(f'\n\t== discogs-id {release["id"]} ==')
    print(f'\tTitle\t: {release.get("title", "Unknown")}')
    print(f'\tYear\t: {release.get("year", "Unknown")}')
    print(f'\tLabels\t: {", ".join(release.get("label", ["Unknown"]))}')
    print(f'\tCat No\t: {release.get("catno", "Unknown")}')
    print(f'\tFormats\t: {", ".join(release.get("format", ["Unknown"]))}')