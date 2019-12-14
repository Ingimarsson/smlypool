import struct
import bitcoinlib
import scrypt
import codecs
import random
from datetime import datetime

DIFF_1 = 0x00000000FFFF0000000000000000000000000000000000000000000000000000

class Block:
  def __init__(self):
    # Block header
    self.previousblockhash = 0
    self.target = 0
    self.height = 0
    self.bits = ""

    # Block body
    self.transactions = []

  """
  Builds the coinbase for the block, outputs is a dictionary of addresses
  and corresponding shares, the shares will be normalized such that the
  total outputs equal 1000 SMLY.
  https://bitcoin.org/en/developer-reference#raw-transaction-format
  """
  def build_coinbase(self, outputs):
    self.coinbasetx = ""

    # Version
    self.coinbasetx += "01000000"

    # Number of inputs
    self.coinbasetx += "01"

    # Previous outpoint TXID
    self.coinbasetx += "0"*64

    # Previous outpoint index
    self.coinbasetx += "ffffffff"

    # Bytes in coinbase (varint 16 = dec 22)
    self.coinbasetx += "16"

    # height (script, first byte count then bytes, little endian)
    #byte_count = math.ceil(math.log(self.height)/math.log(256))
    #self.coinbasetx += byte_count.to_bytes(1, 'little').hex()

    self.coinbasetx += "03"
    self.coinbasetx += self.height.to_bytes(3, 'little').hex()

    # Coinbase arbitrary data / extra nounce (length 22 bytes) w/ two random bytes
    self.coinbasetx += "030d25090103062f42534d4c59504f4"
    self.coinbasetx += random.randint(1, 2**16).to_bytes(2, 'big').hex()
    self.coinbasetx += "fffffffff"

    filtered_outputs = {}

    # Check for malformed outputs and add charities
    for address, amount in outputs.items():
      if len(address) == 34:
        filtered_outputs[address] = amount

    filtered_outputs['BRgKfFuPEVFHNKWUfSnobX2byUVmUMVhux'] = 4500
    filtered_outputs['BQTar7kTE2hu4f4LrRmomjkbsqSW9rbMvy'] = 4500

    # Number of outputs
    self.coinbasetx += len(filtered_outputs).to_bytes(1, 'little').hex()

    for address, amount in filtered_outputs.items():
      # print(address)
      # print(amount)
      self.coinbasetx += struct.pack('Q', amount*10**8).hex()

      # Bytes in pubkey script
      self.coinbasetx += "19"

      # OP_DUP OP_HASH160 20
      self.coinbasetx += "76a914"
      self.coinbasetx += bitcoinlib.encoding.addr_to_pubkeyhash(address).hex()

      # OP_EQUALVERIFY OP_CHECKSIG
      self.coinbasetx += "88ac"

    # Locktime
    self.coinbasetx += "0"*8

    return self.coinbasetx

  """
  Constructs the JSON response for miners
  """
  def create_gbt(self, shares, diff):
    data = {
      "result": {
        "version" : 2,
        "previousblockhash" : self.previousblockhash,
        "transactions" : self.transactions,
        "coinbaseaux" : {
          "flags" : "062f503253482f"
        },
        "coinbasetxn": {
          "data": self.build_coinbase(shares)
        },
        "coinbasevalue" : 1000000000000,
        "target" : self.difficulty_to_target_hash(diff), 
        #"target" : "000000ff91120000000000000000000000000000000000000000000000000000",
        #"mintime" : 1574245037,
        "mutable" : [
          "coinbase/append"
        ],
        "noncerange" : "00000000ffffffff",
        "sigoplimit" : 20000,
        "sizelimit" : 1000000,
        #"curtime" : 1346886758,
        "curtime" : int(datetime.timestamp(datetime.now())),
        "expires": 30, 
        "bits" : self.bits,
        "height" : self.height,
      },
      "error": None,
      "id": 0
    }

    return data


  """
  Calculates the difficulty of the hash of a raw block submission. When
  miners use submitblock this is used to calculate the difficulty.
  """
  def get_submission_difficulty(self, block_hex):
    header_bin = codecs.decode(block_hex[:160], 'hex')
    pow_hash = scrypt.hash(header_bin, header_bin, 1024, 1, 1, 32)

    diff = DIFF_1 / int.from_bytes(pow_hash, 'little')

    return diff


  """
  Convert the header target field into a difficulty int
  """
  def target_to_difficulty(self, target):
    a = int.from_bytes(codecs.decode(target[2:], 'hex'), 'big')
    b = int.from_bytes(codecs.decode(target[:2], 'hex'), 'big')

    hash_hex = (a * 2**(8*(b - 3)) ).to_bytes(32, 'big').hex()

    return DIFF_1 / int.from_bytes(codecs.decode(hash_hex, 'hex'), 'big')


  """
  Convert difficulty int to a hash target for block template
  """
  def difficulty_to_target_hash(self, difficulty):
    return int(DIFF_1 / difficulty).to_bytes(32, 'big').hex()


