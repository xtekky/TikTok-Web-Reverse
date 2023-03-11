from ctypes import c_int32 as int32
from time   import time
from utils.base import node_b64
# from execjs import compile ; b64 = compile('e=(a=>btoa(a));d=(y=>atob(y));')
from random import choices
from string import ascii_letters as letters

def uint32_to_str(uInt32Array, length):
    numElements = len(uInt32Array)
    numBytes    = numElements << 2
    
    if length:
        lastElement = uInt32Array[numElements - 1]
        if lastElement < (numBytes - 4) - 3 or lastElement > numBytes:
            return None
        numBytes = lastElement
        
    for i in range(numElements):
        uInt32Array[i] = chr(255 & uInt32Array[i]) + chr(uInt32Array[i] >> 8 & 255) + chr(uInt32Array[i] >> 16 & 255) + chr(uInt32Array[i] >> 24 & 255)
    
    str = "".join(uInt32Array)
    
    return str[:numBytes] if length else str

def pad(e):
    if len(e) < 4:
        e += '0' * (4 - len(e))
    return e

def str_to_word_array(string, add_length):
    length = len(string)
    words = length >> 2
    
    if 0 != (3 & length):
        words += 1

    if add_length:
        w_array = [0] * (words + 1)
        w_array[words] = length
    else:
        w_array = [0] * words

    for index in range(length):
        w_array[index >> 2] |= ord(string[index]) << ((3 & index) << 3)

    return w_array

def truncateTo32Bits(val):
    return -1 & int32(val).value

def calc_hash(var1, var2, var3, var4, var5, var6):

    r1 = ((var3 & 0xffffffff) >> 5) & 0xffffffff
    r2 = int32(int32(var2).value << 2).value
    r3 = ((var2 & 0xffffffff) >> 3) & 0xffffffff
    r4 = ((var3 << 4) & 0xffffffff) - (1 << 32) if (var3 << 4) & (1 << 31) else (var3 << 4)

    a1 = (r1 ^ r2)
    a2 = (r3 ^ r4)
    a3 = (var1 ^ var2)
    a4 = (int(var6[3 & var4 ^ var5]) ^ var3)

    s1 = a1 + a2
    s2 = a3 + a4

    return (s1 ^ s2) & ((2 ** 32) - 1)

def enc_hash(input_array, key, magic):
    num = len(input_array)
    index = num - 1
    accumulator = input_array[index]
    blockIndex = 0
    shiftAmount = 6 + 52 // num
    for i in range(shiftAmount):
        blockIndex = truncateTo32Bits(blockIndex + magic)
        rounds = blockIndex >> 2 & 3
        for j in range(index):
            tempValue = input_array[j + 1]
            accumulator = input_array[j] = truncateTo32Bits(input_array[j] + calc_hash(blockIndex, tempValue, accumulator, j, rounds, key))
        tempValue = input_array[0]
        accumulator = input_array[index] = truncateTo32Bits(input_array[index] + calc_hash(blockIndex, tempValue, accumulator, index, rounds, key))
    return input_array

def generateMssdkInfo(plain_str):
    magic = 2654435769
    key = ''.join(choices(letters, k=4)) #  "SWAZ" # ranstr(4)
    
    plain_enc = str_to_word_array(plain_str, True)
    key_enc = pad(str_to_word_array(key, False))
    base_enc = enc_hash(plain_enc, key_enc, magic)
    
    #return (key + b64.call('e', uint32_to_str(base_enc, False))).replace('+', '-').replace('/', '.')
    return (key + node_b64(uint32_to_str(base_enc, False))).replace('+', '-').replace('/', '.')

def mssdk_info(ts: int) -> str:
    # ts = int(time() * 1000)
    info = '{"navigator":{"appCodeName":"Mozilla","appName":"Netscape","platform":"Linux x86_64","product":"Gecko","productSub":"20030107","hardwareConcurrency":8,"cpuClass":false,"maxTouchPoints":0,"oscpu":false,"vendor":"Google Inc.","vendorSub":"","doNotTrack":false,"vibrate":true,"credentials":true,"storage":true,"requestMediaKeySystemAccess":true,"bluetooth":false},"window":{"Image":true,"innerHeight":961,"innerWidth":165,"screenX":0,"screenY":0,"isSecureContext":true,"devicePixelRatio":1,"toolbar":true,"locationbar":true,"ActiveXObject":false,"external":true,"mozRTCPeerConnection":false,"postMessage":true,"webkitRequestAnimationFrame":true,"BluetoothUUID":false,"netscape":false},"document":{"characterSet":"UTF-8","compatMode":"CSS1Compat","documentMode":false,"layers":false,"images":true,"location":"https://www.tiktok.com/foryou"},"webgl":{"supportedExtensions":["ANGLE_instanced_arrays","EXT_blend_minmax","EXT_color_buffer_half_float","EXT_disjoint_timer_query","EXT_float_blend","EXT_frag_depth","EXT_shader_texture_lod","EXT_texture_compression_bptc","EXT_texture_compression_rgtc","EXT_texture_filter_anisotropic","EXT_sRGB","OES_element_index_uint","OES_fbo_render_mipmap","OES_standard_derivatives","OES_texture_float","OES_texture_float_linear","OES_texture_half_float","OES_texture_half_float_linear","OES_vertex_array_object","WEBGL_color_buffer_float","WEBGL_compressed_texture_s3tc","WEBGL_compressed_texture_s3tc_srgb","WEBGL_debug_renderer_info","WEBGL_depth_texture","WEBGL_draw_buffers","WEBGL_lose_context","WEBGL_multi_draw"],"antialias":true,"blueBits":8,"depthBits":24,"greenBits":8,"maxAnisotropy":16,"maxCombinedTextureImageUnits":64,"maxCubeMapTextureSize":32768,"maxFragmentUniformVectors":4096,"maxRenderbufferSize":32768,"maxTextureImageUnits":32,"maxTextureSize":32768,"maxVaryingVectors":31,"maxVertexAttribs":16,"maxVertexTextureImageUnits":32,"maxVertexUniformVectors":4096,"shadingLanguageVersion":"WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)","stencilBits":0,"version":"WebGL 1.0 (OpenGL ES 2.0 Chromium)"},"gpu":"Google Inc. (NVIDIA)/ANGLE (NVIDIA, Vulkan 1.3.194 (NVIDIA NVIDIA GeForce GTX 1660 SUPER (0x000021C4)), NVIDIA)","plugins":"Chrome PDF Plugininternal-pdf-viewerapplication/x-google-chrome-pdf##Chrome PDF Viewermhjfbmdgcfjbbpaeojofohoefgiehjaiapplication/pdf##Native Clientinternal-nacl-pluginapplication/x-naclapplication/x-pnacl","timestamp":' + str(ts) + '}'

    return generateMssdkInfo(info)