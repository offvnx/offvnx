import requests
import re
import uuid
from typing import Final
from telegram import Update
from urllib.parse import urlparse, parse_qs, unquote
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

Token: Final = "7539002658:AAG7e8mzgfZUDYZOUl5T9SF6EeKjI0L7QPw"
Bot_UserName: Final = "@EAAV6D7_bot"


def change_cookies_fb(cookies: str):
    result = {}
    try:
        for i in cookies.strip().split(';'):
            result.update({i.split('=')[0]: i.split('=')[1]})
        return result
    except(Exception,):
        for i in cookies.strip().split('; '):
            result.update({i.split('=')[0]: i.split('=')[1]})
        return result


def change_token(app_id, access_token):

    session_ap = requests.post(
        'https://api.facebook.com/method/auth.getSessionforApp', data={
            'access_token': access_token,
            'format': 'json',
            'new_app_id': app_id,
            'generate_session_cookies': '0'
        }
    ).json()["access_token"]
    requests.post(f"https://graph.facebook.com/me/permissions?method=DELETE&access_token={access_token}")
    return session_ap


def get_fb_dtsg(cookies: dict) -> str:
    get_data = requests.get(
        "https://www.facebook.com/v2.3/dialog/oauth", params={
            'redirect_uri': 'fbconnect://success',
            'response_type': 'token,code',
            'client_id': '356275264482347',
        }, cookies=cookies, headers={
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'dpr': '1.25',
            'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
            'sec-ch-ua-full-version-list': '"Chromium";v="117.0.5938.157", "Not;A=Brand";v="8.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'viewport-width': '1038',
        }
    ).text
    fb_dtsg = re.search('DTSGInitData",,{"token":"(.+?)"', get_data.replace('[]', '')).group(1)
    return fb_dtsg


def run_get(cookie_re, app_id="350685531728"):
    cookies = change_cookies_fb(cookie_re)
    c_user = cookies["c_user"]
    fb_dtsg = get_fb_dtsg(cookies)
    headers = {
        'authority': 'www.facebook.com',
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'origin': 'https://www.facebook.com',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
        'sec-ch-ua-full-version-list': '"Chromium";v="117.0.5938.157", "Not;A=Brand";v="8.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-fb-friendly-name': 'useCometConsentPromptEndOfFlowBatchedMutation',
    }

    data = {
        'av': str(c_user),
        '__user': str(c_user),
        'fb_dtsg': fb_dtsg,
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'useCometConsentPromptEndOfFlowBatchedMutation',
        'variables': '{"input":{"client_mutation_id":"4","actor_id":"' + c_user + '","config_enum":"GDP_CONFIRM","device_id":null,"experience_id":"' + str(
            uuid.uuid4()
            ) + '","extra_params_json":"{\\"app_id\\":\\"' + app_id + '\\",\\"kid_directed_site\\":\\"false\\",\\"logger_id\\":\\"\\\\\\"' + str(
            uuid.uuid4()
            ) + '\\\\\\"\\",\\"next\\":\\"\\\\\\"confirm\\\\\\"\\",\\"redirect_uri\\":\\"\\\\\\"https:\\\\\\\\\\\\/\\\\\\\\\\\\/www.facebook.com\\\\\\\\\\\\/connect\\\\\\\\\\\\/login_success.html\\\\\\"\\",\\"response_type\\":\\"\\\\\\"token\\\\\\"\\",\\"return_scopes\\":\\"false\\",\\"scope\\":\\"[\\\\\\"user_subscriptions\\\\\\",\\\\\\"user_videos\\\\\\",\\\\\\"user_website\\\\\\",\\\\\\"user_work_history\\\\\\",\\\\\\"friends_about_me\\\\\\",\\\\\\"friends_actions.books\\\\\\",\\\\\\"friends_actions.music\\\\\\",\\\\\\"friends_actions.news\\\\\\",\\\\\\"friends_actions.video\\\\\\",\\\\\\"friends_activities\\\\\\",\\\\\\"friends_birthday\\\\\\",\\\\\\"friends_education_history\\\\\\",\\\\\\"friends_events\\\\\\",\\\\\\"friends_games_activity\\\\\\",\\\\\\"friends_groups\\\\\\",\\\\\\"friends_hometown\\\\\\",\\\\\\"friends_interests\\\\\\",\\\\\\"friends_likes\\\\\\",\\\\\\"friends_location\\\\\\",\\\\\\"friends_notes\\\\\\",\\\\\\"friends_photos\\\\\\",\\\\\\"friends_questions\\\\\\",\\\\\\"friends_relationship_details\\\\\\",\\\\\\"friends_relationships\\\\\\",\\\\\\"friends_religion_politics\\\\\\",\\\\\\"friends_status\\\\\\",\\\\\\"friends_subscriptions\\\\\\",\\\\\\"friends_videos\\\\\\",\\\\\\"friends_website\\\\\\",\\\\\\"friends_work_history\\\\\\",\\\\\\"ads_management\\\\\\",\\\\\\"create_event\\\\\\",\\\\\\"create_note\\\\\\",\\\\\\"export_stream\\\\\\",\\\\\\"friends_online_presence\\\\\\",\\\\\\"manage_friendlists\\\\\\",\\\\\\"manage_notifications\\\\\\",\\\\\\"manage_pages\\\\\\",\\\\\\"photo_upload\\\\\\",\\\\\\"publish_stream\\\\\\",\\\\\\"read_friendlists\\\\\\",\\\\\\"read_insights\\\\\\",\\\\\\"read_mailbox\\\\\\",\\\\\\"read_page_mailboxes\\\\\\",\\\\\\"read_requests\\\\\\",\\\\\\"read_stream\\\\\\",\\\\\\"rsvp_event\\\\\\",\\\\\\"share_item\\\\\\",\\\\\\"sms\\\\\\",\\\\\\"status_update\\\\\\",\\\\\\"user_online_presence\\\\\\",\\\\\\"video_upload\\\\\\",\\\\\\"xmpp_login\\\\\\"]\\",\\"steps\\":\\"{}\\",\\"tp\\":\\"\\\\\\"unspecified\\\\\\"\\",\\"cui_gk\\":\\"\\\\\\"[PASS]:\\\\\\"\\",\\"is_limited_login_shim\\":\\"false\\"}","flow_name":"GDP","flow_step_type":"STANDALONE","outcome":"APPROVED","source":"gdp_delegated","surface":"FACEBOOK_COMET"}}',
        'server_timestamps': 'true',
        'doc_id': '6494107973937368',
    }
    response = requests.post(
        'https://www.facebook.com/api/graphql/', cookies=cookies, headers=headers, data=data
    ).json()
    uri = response["data"]["run_post_flow_action"]["uri"]

    parsed_url = urlparse(uri)

    # Lấy giá trị close_uri từ query string
    query_params = parse_qs(parsed_url.query)
    close_uri = query_params.get("close_uri", [None])[0]

    # Giải mã close_uri để lấy phần chứa access_token
    decoded_close_uri = unquote(close_uri)

    # Phân tích phần fragment của close_uri
    fragment = urlparse(decoded_close_uri).fragment
    fragment_params = parse_qs(fragment)

    # Lấy giá trị access_token
    access_token = fragment_params.get("access_token", [None])[0]
    return access_token


async def get_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy tham số từ lệnh (context.args chứa danh sách tham số)
    if context.args:  # Kiểm tra nếu người dùng có nhập tham số
        cookie_input = " ".join(context.args).strip()
        cookie_re = re.sub(r"\s+", "", cookie_input, flags=re.UNICODE)
        token = run_get(cookie_re=cookie_re)
        # Phản hồi lại người dùng

        await update.message.reply_text(f"{change_token('275254692598279', token)}")
    else:
        # Nếu không có tham số, gửi hướng dẫn
        await update.message.reply_text("Vui lòng nhập token sau lệnh /gettoken.\nVí dụ: /gettoken EAAA")


# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Xin chào! Tôi là bot Get Token Facebook Lite")


# Hàm xử lý tin nhắn văn bản
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Bạn vừa nói: {update.message.text}")

# Hàm chính
if __name__ == "__main__":
    # Khởi tạo bot với token
    app = Application.builder().token(Token).build()

    # Thêm các handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gettoken", get_token))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Chạy bot
    print("Bot đang chạy...")
    app.run_polling()
