import json
import requests

HOST = "http://localhost:3000"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/0.0.0.0 Safari/537.36 Edg/0.0.0.0"
################################ TRANSLATE FUNCTION ############################
def translate_text(text, language):
    from googletrans import Translator
    translator = Translator()
    result = translator.translate(text, dest= language).text
    return result
################################ STEP_1.LOGIN USER ACCOUNT #####################
def get_cookie_login_by_phoneAndPassword(phone, password):
    request_url = HOST+f"/login/cellphone"
    data = {
        "phone": phone,
        "password": password
    }
    response = requests.post(request_url, data=data)
    if response.status_code == 400:
        header = {"User-Agent": USER_AGENT, "Cookie": response.headers["set-cookie"]}
        response = requests.get(request_url, headers=header, data=data)
    if "cookie" in response.request.headers:
        key, value = response.request.headers['cookie'].split(";")[0].split("=")
    else:
        key, value = response.headers["set-cookie"].split(";")[0].split("=")
    identify_cookie = {key: value}
    return json.loads(response.text), identify_cookie

################################ STEP_2.GET USER ACCOUNT #####################
def get_user_account(cookie):
    request_url = HOST + "/user/account"
    response = requests.get(request_url, cookies=cookie)
    return json.loads(response.text)
def refresh_cookie(cookie):
    request_url = HOST + "/login/refresh"
    response = requests.get(request_url, cookies=cookie)
    return json.loads(response.text)

################################ STEP_3.PLAYLIST OPERATION #####################
def create_playlist(name, cookie, type=None, privacy=False):
    request_url = HOST + f"/playlist/create?name={name}"
    if type is not None:
        request_url += f"&Type={type}"
    if privacy == 10:
        request_url += f"&privacy={privacy}"
    response = requests.get(request_url, cookies=cookie)
    return json.loads(response.text)

def update_playlist(cookie, id, name, desc, tags):
    request_url = HOST + f"/playlist/update?id={id}&name={name}&desc={desc}&tags={tags}"
    response = requests.get(request_url, cookies=cookie)
    return json.loads(response.text)

def delete_playlist(cookie, id):
    request_url = HOST + f"/playlist/delete?id={id}"
    response = requests.get(request_url, cookies=cookie)
    return json.loads(response.text)

def get_playlist_by_uid(uid):
    request_url = HOST + f"/user/playlist?uid={uid}"
    response = requests.get(request_url)
    return json.loads(response.text)

################################ STEP_4. RECOMMENDATION #####################
def get_songs_from_artists(ID):
    request_url = HOST + f"/simi/song?id={ID}"
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(request_url, headers=headers)
    return json.loads(response.text)

def daily_recommendation(cookie):
    request_url = HOST + "/recommend/resource"
    response = requests.get(request_url, cookies=cookie)
    return json.loads(response.text)

def get_recommendation():
    request_url = HOST + "/personalized/newsong"
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(request_url, headers=headers)
    return json.loads(response.text)


