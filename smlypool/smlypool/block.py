import struct
import bitcoinlib
import scrypt
import codecs

DIFF_1 = 0x00000000FFFF0000000000000000000000000000000000000000000000000000

class Block:
  def __init__(self):
    # Block header
    self.version = 0
    self.prevhash = 0
    self.merkleroot = 0
    self.timestamp = 0
    self.target = 0
    self.height = 0

    # Block body
    self.coinbasetx = 0
    self.txns = []

  """
  Builds the coinbase for the block, addr is a list of addresses
  and shares is a list of corresponding shares such that sum(shares) = 1
  https://bitcoin.org/en/developer-reference#raw-transaction-format
  """
  def build_coinbase(self, addr, shares):
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

    # Coinbase arbitrary data / extra nounce (length 22 bytes)
    self.coinbasetx += "030d25090103062f42534d4c59504f4f4c2fffffffff"

    outputs = {
      'BEppJqTLw5ByePPbZwm7hByqqwcmsCtVfK': 500,
      'B61eFL4bvYznW1UEXJgHcESHD588wyAfR7': 300,
      'B8XGCWSvQUKGbXRF9ScWsFp7nMTqq6P7zM': 200,
      'BRgKfFuPEVFHNKWUfSnobX2byUVmUMVhux': 4500,
      'BQTar7kTE2hu4f4LrRmomjkbsqSW9rbMvy': 4500,
      }

    # Number of outputs
    self.coinbasetx += len(outputs).to_bytes(1, 'little').hex()

    for address, amount in outputs.items():
      print(address)
      print(amount)
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
  Calculates the difficulty of the hash of a raw block.
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




