# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask

app = Flask(__name__)

# Define a route that handles GET requests
@app.route('http/createissue', methods=['POST'])
def createJira():

    url = "https://your-atlassian-url/rest/api/3/issue"

    API_TOKEN="your-github-api-token"

    auth = HTTPBasicAuth("your-email", API_TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps( {
        "fields": {
        "description": {
            "content": [
                {
                    "content": [
                        {
                            "text": "Order entry fails when selecting supplier.",
                            "type": "text"
                        }
                    ],
                    "type": "paragraph"
                    }
                ],
            "type": "doc",
             "version": 1
        },
        "project": {
           "key": "XYZ"
        },
        "issuetype": {
            "id": "10007"
        },
        "summary": "Your designed summary",
    },
    "update": {}
    } )


    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
