import requests
import json
from flask_sse import sse
import uuid

# api_key = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJjaGF1N3RpbkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJwb2lkIjoib3JnLWJKdDByQzl4NEdZV051TEpHTDk0T3VXNiIsInVzZXJfaWQiOiJ1c2VyLWtqUUY3VjdsdTF2QjRxUXk0Vm41eFBpWCJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDc5ODE3NjE3MTUzNjkxMDYxMjkiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzExODg4MjE3LCJleHAiOjE3MTI3NTIyMTcsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIG9mZmxpbmVfYWNjZXNzIn0.a0zKo8FJf2cAZayLE4JlLXMYevGd6eSrk-uW2wRIFPlgCB_oDPUVm8oPpXqjPspZWi4wBo5ipKsSEkOkw0i9pFyjMy3MYoFVK7om6j8mLiG31EUurOqfG1eOCJ-gk37yvD_e7jipd36vleaeK5vTS9rzXBqufXGqOpYphd46g_Bzpi87MxDJ5xh6dUvLfG845War7eWCWFQN1WPrnxrc3gHaUEi9InbnP4dcinWuJqNF6PsQawYBxjkg3fmrrpGTCevvJwZMrLAhjJyiFDau0f-soB8SlaMtgZRw_qcKvFCprypDtNg3hasrePanlu9Wd6kauJxq05kYwFb02BifVA'
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
user_token = ''
random_id = uuid.uuid4()

def getHeader():
    return {
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5,fr-FR;q=0.4,fr;q=0.3',
        'sec-ch-ua-mobile': '?0',
        'Content-Type': 'application/json',
        'sec-ch-ua-platform': '"Windows"',
        'accept': 'text/event-stream',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'User-Agent': f'{User_Agent}',
        'Openai-Sentinel-Chat-Requirements-Token': f'{user_token}',
        'cookie': 'intercom-device-id-dgkjq2bp=e13d3b94-86ea-4956-af57-92f86dc9971f; cf_clearance=GjTsFZxtsQ1G7z5_xpzLPXBPrGP0yl7swXJqMtA2EgA-1706364671-1-AWDM0ZPQjKMj6Ue/gvHRn4sBXFK/wzYnm3jJ5Wp44L/MYT0jj2no8PNLEXqtTzcHppug53gzHqSOmss2jFjLil4=; oai-did=ad7bf240-ff09-4f05-8071-454e0d1333d5; ajs_user_id=user-d9VACR4pJgIKBeISrw8bTKdE; ajs_anonymous_id=anon-cgpt-a38d39b7-08bc-483a-92f8-22d316256c58; cf_clearance=FFqzYr.7X78ouarQj1V3PBMeWEsqgMCpd_J.wIwMHSk-1712035915-1.0.1.1-NVuTAkXxn2DYOMfo1C0mRQ0OanaOHuUbruu2Fr_O.Apa14ifBwUW7FoGPog9ONM9drZzxlD2svY67.e84UqlzA; __Host-next-auth.csrf-token=2381a76e41b664c5cbeb92d31a7aabacaffe251e5d33113070b01ab140ffa1e6%7C2b64bbd36357e6abf9b31aa5291bb8d511e40b8dfb62b7e0e31bc40b01188e62; __cf_bm=C.wkwPKYIlvfYs5SK2IdoWupII.6bLhAeYpbTTcuaZg-1712077604-1.0.1.1-i79WzZsJANpigA6YkzNVUOwsvacareT9UfDfP8uoLNs1YlE7g2yaFKJWpe4xwdFkdshrW05HlDt1Acxr1VWAJQ; __cflb=0H28vVfF4aAyg2hkHFTZ1MVfKmWgNcKEruQuFyFVHEV; _cfuvid=ecTmr0.8_2xwEAnBDPbYTZ54srvEllbK3ZfTRaF.y8o-1712077604021-0.0.1.1-604800000; __Secure-next-auth.callback-url=https%3A%2F%2Fauth0.openai.com%2Fv2%2Flogout%3Fclient_id%3DTdJIcbe16WoTHtN95nyywh5E4yOo6ItG%26returnTo%3Dhttps%3A%2F%2Fchat.openai.com; intercom-session-dgkjq2bp=MHBkZGVsWlFiQkJLR2hhWHdUd3hvd1QxSytEK0ZDTzdmQXJNNTRxK2lGNkp3Qjh4V2ViTkZDei84QWFyRVhSbi0tY3luQWc4Z0VOMDk4NDQza09ZZkhGUT09--e63260a4841cd2a9e2a6a2d26d49fb3ec580f25e; _dd_s=rum=0&expire=1712078532240; __cf_bm=Fz2PJJ8vFesizueotgng.owvrM8.9wRCYI.FH7nGIVk-1712077961-1.0.1.1-3klZAyqssgLeF74E_Ly23v2MSEUwQCG.lw0DbMF518hAZef7WhNP13dj0jsLQBPAcB1x2uqFqz_VzEx5RzcV_w',
        'dnt': '1',
    }

def NewChat_ChatGPT(message: str, id):
    global user_token
    reqHeaders = getHeader()
    reqBody = json.dumps({
        "action": "next",
        "messages": [
            {
                "author": {
                    "role": "user"
                },
                "content": {
                    "content_type": "text",
                    "parts": [
                        message
                    ]
                },
                "metadata": {}
            }
        ],
        "parent_message_id": f"{random_id}",
        "model": "text-davinci-002-render-sha",
        "timezone_offset_min": -420,
        "suggestions": [],
        "history_and_training_disabled": False,
        "conversation_mode": {
            "kind": "primary_assistant"
        },
        "force_paragen": False,
        "force_paragen_model_slug": "",
        "force_nulligen": False,
        "force_rate_limit": False,
    })
    with POST_CURL('https://chat.openai.com/backend-api/conversation', reqHeaders, reqBody) as response:
        for line in response.iter_lines(decode_unicode=True):
            # print(f'{user_token}')
            if line.startswith("data: "):
                try:
                    data = json.loads(line.lstrip("data: "))
                    if (
                        data
                        and "message" in data
                        and data["message"] is not None
                        and "content" in data["message"]
                        and "parts" in data["message"]["content"]
                    ):
                        parts = data["message"]["content"]["parts"]
                        sse.publish({"phien": data["conversation_id"], "id": id, "message": parts}, type='message')
                except json.JSONDecodeError as e:
                    print(e)
            else:
                try:
                    detail = json.loads(line)['detail']
                    if detail:
                        user_token = getToken()
                        NewChat_ChatGPT(message, id)
                        return
                except json.decoder.JSONDecodeError as e:
                    sse.publish({"id": id, "message": 'Vui Lòng Thử Lại'}, type='message')
                    

def Chat_ChatGPT(message: str, id, phien):
    global user_token
    reqHeaders = getHeader()
    reqBody = json.dumps({
        "action": "next",
        "messages": [
            {
                "author": {
                    "role": "user"
                },
                "content": {
                    "content_type": "text",
                    "parts": [
                        message
                    ]
                },
                "metadata": {}
            }
        ],
        "conversation_id": f"{phien}",
        "parent_message_id": f"{random_id}",
        "model": "text-davinci-002-render-sha",
        "timezone_offset_min": -420,
        "suggestions": [],
        "history_and_training_disabled": False,
        "conversation_mode": {
            "kind": "primary_assistant",
        },
        "force_paragen": False,
        "force_paragen_model_slug": "",
        "force_nulligen": False,
        "force_rate_limit": False,
        "websocket_request_id": "67845c66-bb50-4a83-be89-51aa7d79a5dd"
    })
    with POST_CURL('https://chat.openai.com/backend-api/conversation', reqHeaders, reqBody) as response:
        for line in response.iter_lines(decode_unicode=True):
                if line.startswith("data: "):
                    try:
                        data = json.loads(line.lstrip("data: "))
                        if (
                            data
                            and "message" in data
                            and data["message"] is not None
                            and "content" in data["message"]
                            and "parts" in data["message"]["content"]
                        ):
                            parts = data["message"]["content"]["parts"]
                            sse.publish({"phien": data["conversation_id"], "id": id, "message": parts}, type='message')
                    except json.JSONDecodeError as e:
                        print(e)
                else:
                    try:
                        detail = json.loads(line)['detail']
                        if detail:
                            user_token = getToken()
                            Chat_ChatGPT(message, id, phien)
                            return
                    except json.decoder.JSONDecodeError as e:
                        sse.publish({"id": id, "message": 'Vui Lòng Thử Lại'}, type='message')

def getToken():
    reqHeaders = getHeader()
    reqBody = json.dumps({})
    while(True):
        response = POST_CURL('https://chat.openai.com/backend-api/sentinel/chat-requirements', reqHeaders, reqBody)
        if response.status_code == 200:
            data = response.json()
            if data.get('token'):
                return data.get('token')


def POST_CURL(api_url, reqHeaders, reqBody):
    proxy_url = 'http://muaproxy_scMLA:IJ70V5KshM@103.214.44.131:11222'
    proxies = {
        'http': proxy_url,
        'https': proxy_url,
    }
    try:
        return requests.request("POST", api_url, headers=reqHeaders, data=reqBody, stream=True, proxies=proxies)
    except requests.exceptions.RequestException as e:
        return(f"Request failed with error: {e}")