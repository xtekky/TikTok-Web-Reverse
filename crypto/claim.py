from time            import time
from tls_client      import Session
from urllib.parse    import urlencode
from re              import findall
from utils.info      import mssdk_info
from utils.report    import report_enc
from utils.body      import get_body
from utils.ressource import enc_eq
from utils.bogus     import sign
from json            import loads, dumps

client    = Session(client_identifier='chrome_108')
username  = 'username'
sessionid = 'sessionid'

client.headers = {
    "host"              : "mssdk-va.tiktok.com",
    "connection"        : "keep-alive",
    "sec-ch-ua"         : "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
    "sec-ch-ua-mobile"  : "?0",
    "user-agent"        : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": "\"macOS\"",
    "accept"            : "*/*",
    "origin"            : "https://www.tiktok.com",
    "sec-fetch-site"    : "same-site",
    "sec-fetch-mode"    : "cors",
    "sec-fetch-dest"    : "empty",
    "referer"           : "https://www.tiktok.com/",
    "accept-encoding"   : "application/json",
    "accept-language"   : "en-GB,en-US;q=0.9,en;q=0.8",
}
client.cookies['sessionid'] = sessionid

init      = client.get('https://www.tiktok.com')
device_id = findall(r'wid":"([0-9]+)"', init.text)[0]

# get cookies
[client.get(url) for url in [
    'https://www.tiktok.com/manifest.json',
    'https://webcast.tiktok.com/webcast/wallet_api/diamond_buy/permission/',
    'https://www.tiktok.com/passport/web/account/info/?aid=1459&app_language=en&app_name=tiktok_web&battery_info=1&browser_language=en&browser_name=Mozilla&browser_online=True&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F110.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=True&device_id=7200449829465687557&device_platform=web_pc&focus_state=True&from_page=fyp&history_len=2&is_fullscreen=false&is_page_visible=True&os=mac&priority_region=FR&referer=&region=FR&screen_height=956&screen_width=1470&tz_name=Europe%2FZurich'
]]


if not client.cookies.get_dict().get('msToken'): client.get(f'https://mssdk-va.tiktok.com/web/resource', params = {
        'eq': enc_eq(urlencode({
            'aid'       : 1988,
            'region'    : 'va-tiktok',
            'location'  : 'www.tiktok.com'
        }))
    })

params = sign(f'msToken={client.cookies.get_dict()["msToken"]}', client.headers['user-agent'])
resp   = client.post(f"https://mssdk-va.tiktok.com/web/report?{params}", json = {
    "magic"         : 538969122,
    "version"       : 1,
    "dataType"      : 8,
    "strData"       : report_enc(get_body()),
    "tspFromClient" : int(time() * 1000)
})

print(resp.text.encode())


params = sign(urlencode({
    "aid"                : 1459,
    "account_sdk_source" : "web",
    "language"           : "en",
    
    "shark_extra": dumps({
        "aid"               : 1459,
        "app_name"          : "Tik_Tok_Login",
        "channel"           : "tiktok_web",
        "device_platform"   : "web_pc",
        "device_id"         : device_id,
        "region"            : "FR",
        "priority_region"   : "",
        "os"                : "mac",
        "referer"           : "",
        "cookie_enabled"    : True,
        "screen_width"      : 1470,
        "screen_height"     : 956,
        "browser_language"  : "en-GB",
        "browser_platform"  : "MacIntel",
        "browser_name"      : "Mozilla",
        "browser_version"   : "5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "browser_online"    : True,
        "app_language"      : "en",
        "webcast_language"  : "en",
        "tz_name"           : "Europe/Zurich",
        "is_page_visible"   : True,
        "focus_state"       : True,
        "is_fullscreen"     : True,
        "history_len"       : 2,
        "battery_info"      : None}, separators=(',', ':')),
    
    "msToken": client.cookies.get_dict()["msToken"]}), client.headers['user-agent'])

response = client.post(f"https://www.tiktok.com/passport/web/login_name/update/?{params}", data = {
    'login_name': username }, headers = {
        'x-mssdk-info': mssdk_info(int(time() * 1000))
})

print(response.text)