
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

    # Bytes in coinbase (varint)
    self.coinbasetx += "???"

    # Bytes in height (varint)

    # Height

    # Coinbase arbitrary data / extra nounce

    # Zero sequence

    # Number of outputs

    return

  """
  Returns the block as a binary string.
  """
  def get_raw_block(self):
    return 0x00


