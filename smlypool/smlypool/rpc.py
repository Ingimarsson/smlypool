import requests, json
from django.conf import settings

class RPC(object):
  def __init__(self):
    self.session = requests.Session()
    self.headers = {'content-type': 'text/plain'}
    self.url = "http://{}:{}@localhost:{}".format(settings.RPC_USER, settings.RPC_PASS, settings.RPC_PORT)

  def call(self, cmd, params = []):
    payload = {"method": cmd, "jsonrpc": "1.0", "params": params}

    response = self.session.post(self.url, headers=self.headers, data=json.dumps(payload))

    responseJSON = response.json()

    return responseJSON['result']
