from tiktokapi.imports import *
from tiktokapi.crypto  import *

class Api:
    def __init__(this,
            user_agent : str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            cookies    : dict = {}
        ) -> None:

        this.user_agent     = user_agent
        this.msToken        = ''
        this.verify_fp      = ''
        
        this.client         = Session(f'chrome_108')
        this.client.cookies = cookies
        this.client.headers = {
            "host"                      : "www.tiktok.com",
            "connection"                : "keep-alive",
            "sec-ch-ua"                 : f"\"Chromium\";v=\"108\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"108\"",
            "sec-ch-ua-mobile"          : "?0",
            "sec-ch-ua-platform"        : "\"macOS\"",
            "upgrade-insecure-requests" : "1",
            "user-agent"                : user_agent,
            "accept"                    : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-fetch-site"            : "none",
            "sec-fetch-mode"            : "navigate",
            "sec-fetch-user"            : "?1",
            "sec-fetch-dest"            : "document",
            "accept-encoding"           : "gzip, deflate, br",
            "accept-language"           : "en-GB,en-US;q=0.9,en;q=0.8"
        }
        
        this.config = this.__get_config()
        
    def __get_config() -> dict:
        init      = client.get('https://www.tiktok.com')
        device_id = findall(r'wid":"([0-9]+)"', init.text)[0]
        
        return {
            'device_id': device_id,
            'ms'
        }
        
    def __base_params(this, extra: dict = {}) -> str:
        
        return Signer.sign(urlencode(extra | {
            "aid": "1988",
            "app_language": "en",
            "app_name": "tiktok_web",
            "battery_info": "0.94",
            "browser_language": "en-GB",
            "browser_name": "Mozilla",
            "browser_online": "true",
            "browser_platform": "MacIntel",
            "browser_version": this.user_agent,
            "channel": "tiktok_web",
            "cookie_enabled": "true",
            "device_platform": "web_pc",
            "focus_state": "true",
            "from_page": "fyp",
            "history_len": "3",
            "is_fullscreen": "false",
            "is_page_visible": "true",
            "os": "mac",
            "priority_region": "FR",
            "referer": "https://www.tiktok.com/",
            "region": "FR",
            "root_referer": "https://www.tiktok.com/",
            "screen_height": "956",
            "screen_width": "1470",
            "type": "1",
            "tz_name": "Europe/Paris",
            "verifyFp": this.verify_fp,
            "webcast_language": "en",
            "msToken": this.msToken
        }))