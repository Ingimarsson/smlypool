from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
import time

@csrf_exempt
def get_block_template(request):
  pprint(request.body)

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
        "data": "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff1302955d0f00456c6967697573005047dc66085fffffffff02fff1052a010000001976a9144ebeb1cd26d6227635828d60d3e0ed7d0da248fb88ac01000000000000001976a9147c866aee1fa2f3b3d5effad576df3dbf1f07475588ac00000000"
      },
      "coinbasevalue" : 1000000000000,
      "target" : "0000007d2f640000000000000000000000000000000000000000000000000000",
      "mintime" : 1574245037,
      "mutable" : [
        "submit/coinbase",
        "coinbase/append",
      ],
      "noncerange" : "00000000ffffffff",
      "sigoplimit" : 20000,
      "sizelimit" : 1000000,
      "curtime" : 1574245354,
      "expires": 120, 
      "bits" : "1c05f705",
      "height" : 598154,
    },
    "error": None,
    "id": 0
  }

  time.sleep(2)

  if "submitblock" in str(request.body):
    return JsonResponse({"result": None})

  else:
    return JsonResponse(data)

