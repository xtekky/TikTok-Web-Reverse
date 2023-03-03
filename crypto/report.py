from re               import sub
#from execjs           import compile ; b64 = compile('e=(a=>btoa(a));d=(y=>atob(y));')
from utils.compress   import LZWCompressor
from utils.base import node_b64
from random import randint


def b64_shift(b64_string):
    return sub(r"[A-Za-z0-9+/=]",
        lambda shift_table: "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="[ 
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".index(shift_table.group(0))
        ], b64_string
    )

def b64_unshift(b64_string):
    return sub(r"[A-Za-z0-9+/=]",
        lambda shift_table: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="[ 
            "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=".index(shift_table.group(0))
        ], b64_string
    )

def rc4_crypt(plain_text: str, key: str) -> str:
    s_box           = [_ for _ in range(256)]
    j               = 0
    encrypted_text  = ""
    
    for i in range(256):
        j        = (j + s_box[i] + ord(key[i % len(key)])) % 256
        temp     = s_box[i]
        s_box[i] = s_box[j]
        s_box[j] = temp

    i = 0
    j = 0
    for index in range(len(plain_text)):
        i        = (i + 1) % 256
        j        = (j + s_box[i]) % 256
        temp     = s_box[i]
        s_box[i] = s_box[j]
        s_box[j] = temp
        
        encrypted_text += chr(255 & (ord(plain_text[index]) ^ s_box[(s_box[i] + s_box[j]) % 256]))

    return encrypted_text

def mssdk_enc(plain_text: str):
    key     = chr(randint(0, 255))
    rc4_enc = rc4_crypt(plain_text, key)
    b64_enc = node_b64("A" + key + rc4_enc)
    
    return b64_shift(b64_enc)

# def mssdk_dec(enc_string):
#     plain = b64.call('d', b64_unshift(enc_string))
    
#     return rc4_crypt(plain[2:], chr(ord(plain[1:2])))

def report_enc(base_string):
    compressed = LZWCompressor().compress(base_string)
    
    return mssdk_enc(''.join([chr(_) for _ in compressed])).replace('f6sm1', 'fLsm1') # temporary fix