from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings

from pprint import pprint
from datetime import datetime
import time
import json
import random 
import base64

from . import block, rpc
from .models import Shares

"""
This is the entrypoint for miners, they should send a POST
request with a JSON-RPC command, either getblocktemplate
or submitblock.
"""
@csrf_exempt
def get_block_template(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  b = block.Block()
  wallet = rpc.RPC()

  template = wallet.call("getblocktemplate")

  # Put data from the wallet into the new block template
  b.previousblockhash = template['previousblockhash']
  b.transactions = template['transactions']
  b.height = template['height']
  b.difficulty = b.target_to_difficulty(template['bits'])
  b.bits = template['bits']

  if "submitblock" in str(request.body):
    # Get credentials and submission difficulty
    difficulty = b.get_submission_difficulty(body['params'][0])
    user, password = get_auth(request.META)

    print("Miner: {} Submitted difficulty: {} Network difficulty: {}".format(user, difficulty, b.difficulty))

    # If share meets difficulty then submit to blockchain
    if difficulty >= b.difficulty:
      result = wallet.call("submitblock", [ body['params'][0] ])
      print("BLOCK FOUND! Wallet response: {}".format(result))

    # Add submitted share to database
    share = Shares.objects.create()
    share.user = user
    share.submission_diff = difficulty
    share.actual_diff = b.difficulty
    share.height = b.height
    share.save()

    return JsonResponse({"result": None})

  else:
    # Collect the shares
    # Hardcoded for the moment, should be grabbed from database
    shares = {
      'BEppJqTLw5ByePPbZwm7hByqqwcmsCtVfK': 500,
      'B61eFL4bvYznW1UEXJgHcESHD588wyAfR7': 300,
      'B8XGCWSvQUKGbXRF9ScWsFp7nMTqq6P7zM': 200,
    }

    return JsonResponse(b.create_gbt(shares, settings.SHARES_DIFF))

"""
This function reads the headers of the HTTP request and
returns the BASIC AUTH username and password from the miner
"""
def get_auth(meta):
  data = base64.b64decode(meta['HTTP_AUTHORIZATION'].split()[1]).decode().split(":")

  return data[0], data[1]

"""
This is the information page that can be opened in browsers
"""
def info(request):
  latest = Shares.objects.all().order_by('-id')[:15]
  highest = Shares.objects.all().order_by('-submission_diff')[:10]

  return render(request, 'info.html', {'latest': latest, 'highest': highest})
