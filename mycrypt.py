from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

def crypt_and_store(plaintext, path):
  key = get_random_bytes(16)
  cipher = AES.new(key, AES.MODE_EAX)

  ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))

  with open(path, 'wb') as f:
    f.write(ciphertext)

  os.environ['CIPHER_KEY'] = key.hex()
  os.environ['CIPHER_TAG'] = tag.hex()
  os.environ['CIPHER_NONCE'] = cipher.nonce.hex()

def decrypt_and_restore(path):
  cipherkey = bytes.fromhex(os.environ['CIPHER_KEY'])
  ciphertag =bytes.fromhex( os.environ['CIPHER_TAG'])
  ciphernonce =bytes.fromhex( os.environ['CIPHER_NONCE'])

  cipher_dec = AES.new(cipherkey, AES.MODE_EAX, ciphernonce)

  with open(path, 'rb') as f:
    ciphertext = f.read()
    data = cipher_dec.decrypt_and_verify(ciphertext, ciphertag)

  return data.decode('utf-8')


# ref:
#   [組み込み型 — Python 3.11.2 ドキュメント](https://docs.python.org/ja/3/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview)
#   [AES対応のPython暗号化ライブラリを比較検証してみた | DevelopersIO](https://dev.classmethod.jp/articles/python-crypto-libraries/)