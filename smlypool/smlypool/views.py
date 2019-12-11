from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from pprint import pprint
import time
import json
from datetime import datetime
import random 
from . import block, rpc

@csrf_exempt
def get_block_template(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  b = block.Block()

  diff = 0.001

  data = {
    "result": {
      "version" : 2,
      "previousblockhash" : "00000000001be4c884211ed7477d8e6c7abe40bbc16840d159169d38a85204a8",
      "transactions" : [
      ],
      "coinbaseaux" : {
        "flags" : "062f503253482f"
      },
      "coinbasetxn": {
        "data": "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff1603ef6805030d25090103062f42534d"+random.randint(1, 2**16).to_bytes(2, 'big').hex()+"504f4f4c2fffffffff0500743ba40b0000001976a91471cda15b815ec0411c1c74412598d9e695c6e37988ac00ac23fc060000001976a9141120acffc8b30a852913dd420fc19ca6f1b770f988ac00c817a8040000001976a9142cab003c8b268c815688b9eed6cfc477997b366f88ac001417c6680000001976a914e8dbc5ac7e84cea890b29c2dcc74a5391adc225c88ac001417c6680000001976a914db7aeaa2443fb3c91662392c6cac2f6eb8f0ef6e88ac00000000"
      },
      "coinbasevalue" : 1000000000000,
      "target" : b.difficulty_to_target_hash(diff), 
      #"target" : "000000ff91120000000000000000000000000000000000000000000000000000",
      "mintime" : 1574245037,
      "mutable" : [
        "coinbase/append"
      ],
      "noncerange" : "00000000ffffffff",
      "sigoplimit" : 20000,
      "sizelimit" : 1000000,
      "curtime" : 1346886758,
      #"curtime" : int(datetime.timestamp(datetime.now())),
      "expires": 30, 
      "bits" : "1c05f705",
      "height" : 354543,
    },
    "error": None,
    "id": 0
  }


  if "submitblock" in str(request.body):
    golden_nonce = body['params'][0][152:160]
    #print(golden_nonce)
    #print(body['params'][0])

    print("Submitted difficulty: "+str(b.get_submission_difficulty(body['params'][0])))

    return JsonResponse({"result": None})

  else:
    return JsonResponse(data)


def dashboard(request):

  wallet = rpc.RPC()
  return JsonResponse(wallet.call("getblocktemplate"))

def info(request):
    return render(request, 'info.html')
