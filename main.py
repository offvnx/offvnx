import requests
import telebot
import tempfile
import random
import os
import io
import html
import threading
from urllib.parse import quote
from io import BytesIO
import time
import urllib.parse
from telebot import types
import logging
import atexit
from datetime import datetime, timezone, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputMediaPhoto
import urllib3
import re
from urllib.parse import urlparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
API_TOKEN = '7562722453:AAHCy0ZSncgmL1a5PtnENc8Sw60a3QFp9Ec'
bot = telebot.TeleBot(API_TOKEN, parse_mode='HTML')
# Khai báo biến toàn cục
ADMIN_ID = 6452283369
chat_id = -1002170831477
BASE_URL = "http://hunght1890.com/{}"
valid_keys = {}  # Lưu key thường
vip_keys = {}    # Lưu key VIP
user_video_info = {}
waiting_users = {}  # <--- Thêm dòng này ở đây
auto_buff_by_username = {}  # <--- Tự động buff theo từng username
WEATHER_API_KEY = '9185cfa59b9c2c2db6678b9dfc225065'
GOOGLE_MAPS_URL = "https://www.google.com/maps/search/?api=1&query="
logger = logging.getLogger(__name__)
QRND_API_URL = "https://qr.sepay.vn/img"
def get_vietnam_time():
    utc_now = datetime.now(timezone.utc)
    vietnam_now = utc_now + timedelta(hours=7)
    return vietnam_now.strftime("%d/%m/%Y %H:%M:%S")

# Hàm kiểm tra quyền truy cập nhóm
def is_allowed_group(chat_id):
    # Thay đổi ID nhóm hoặc username nhóm cho phù hợp
    allowed_groups = [-1002170831477, '@nhomspamcallsms']
    return chat_id in allowed_groups

def safe_text(value, default="Không có dữ liệu"):
    return html.escape(str(value)) if value else default

def safe_number(value, default="0"):
    return f"{int(value):,}" if str(value).isdigit() else default

def get_flag(region):
    flags = {
        "VN": "🇻🇳",
        "Thailand": "🇹🇭",
        "SG": "🇮🇩",
        "IND": "🇮🇳",
        "Brazil": "🇧🇷",
        "Mexico": "🇲🇽",
        "United States": "🇺🇸",
        "Russia": "🇷🇺",
        "Europe": "🇪🇺",
        "Others": "🏳"
    }
    return flags.get(region, "🏳")  # Mặc định là cờ trắng nếu không tìm thấy
#===================================#
@bot.message_handler(commands=['proxy'])
def send_proxy_directly(message):
    chat_id = message.chat.id

    # Xoá lệnh người dùng
    try:
        bot.delete_message(chat_id, message.message_id)
    except Exception as e:
        print(f"Lỗi khi xoá lệnh: {e}")

    # Lấy vị trí và thời gian
    city, region, country, lat, lon = get_location_by_ip()
    now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")

    # Caption gửi kèm
    caption = (
        f"📕 Danh sách proxy\n\n"
        f"🌍 Vị trí IP hiện tại\n"
        f"🗾 Thành phố: {city}\n"
        f"🏕️ Vùng: {region}\n"
        f"🌐 Quốc gia: {country}\n"
        f"🗺️ Toạ độ: {lat}, {lon}\n"
        f"⏰ Bây giờ là: {now}"
    )

    # Tải và gửi file proxy
    filename = download_proxies()
    with open(filename, "rb") as f:
        bot.send_document(chat_id, f, caption=caption)

# Tải proxy
def download_proxies():
    filename = "proxy.txt"
    urls = [
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=1000000&country=CN&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=10000000&country=VN&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=10099999900&country=UK&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=US&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=BR&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=ID&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=JP&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=NL&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=FI&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=ES&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=PL&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=BD&ssl=all&anonymity=all'
    ]
    with open(filename, "w") as f:
        for url in urls:
            try:
                r = requests.get(url)
                f.write(r.text)
            except:
                pass
    return filename

# Lấy vị trí IP
def get_location_by_ip():
    try:
        data = requests.get("https://ipinfo.io").json()
        city = data.get("city", "Không rõ")
        region = data.get("region", "")
        country = data.get("country", "")
        loc = data.get("loc", "0,0").split(",")
        return city, region, country, loc[0], loc[1]
    except:
        return "Không rõ", "", "", "0", "0"
#===================================#
@bot.message_handler(commands=['spotify'])
def handle_spotify_command(message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        bot.reply_to(message, "Vui lòng nhập đúng cú pháp:\nVí dụ: /spotify https://open.spotify.com/track/0xlWd9o8yjKpJ02WJy79kZ")
        return

    url = parts[1].strip()

    if 'spotify.com/playlist/' in url:
        bot.reply_to(message, "⚠️ Hiện tại bot chưa hỗ trợ tải playlist Spotify.")
        return
    elif 'spotify.com/album/' in url:
        bot.reply_to(message, "⚠️ Hiện tại bot chưa hỗ trợ tải album Spotify.")
        return
    elif 'spotify.com/track/' not in url:
        bot.reply_to(message, "❌ Đây không phải link bài hát Spotify hợp lệ.")
        return

    api_url = f"https://spotify-downloader.ma-coder-x.workers.dev/?url={url}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if data.get("status"):
            result = data["result"]
            duration_min = round(result["duration_ms"] / 60000, 2)
            title = result["title"]
            artist = result["artist"]
            image_url = result["image"]
            download_url = result["download"]

            caption = (
                f"<b>{title}</b>\n"
                f"👤 <i>Nghệ sĩ:</i> {artist}\n"
                f"⏱️ <i>Thời lượng:</i> {duration_min} phút\n"
                f"⬇️ <a href=\"{download_url}\">Tải MP3</a>\n\n"
            )

            bot.send_photo(
                chat_id=message.chat.id,
                photo=image_url,
                caption=caption,
                parse_mode='HTML'
            )

            # Xóa tin nhắn lệnh gốc của người dùng
            try:
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except Exception as del_err:
                print(f"Lỗi khi xóa tin nhắn: {del_err}")

        else:
            bot.reply_to(message, "Không thể xử lý link Spotify này.")
    except Exception as e:
        bot.reply_to(message, f"Lỗi xảy ra: {str(e)}")

@bot.message_handler(commands=['search'])
def search_music(message):
    query = message.text[len('/search '):].strip()
    if not query:
        bot.reply_to(message, "Vui lòng nhập tên bài hát. Ví dụ:\n/search Atif Aslam")
        return

    # Gọi API tìm kiếm bài hát
    url = f'https://spotify-search.ma-coder-x.workers.dev/?q={requests.utils.quote(query)}'
    try:
        res = requests.get(url).json()
        if res.get('status') and res.get('result'):
            for item in res['result'][:5]:  # 5 bài đầu
                title = item.get('title')
                artists = item.get('artists')
                duration = item.get('duration_ms') // 1000
                link = item.get('link')
                image = item.get('image')
                mp3_link = item.get('download')  # Đây là link tải MP3

                minutes = duration // 60
                seconds = duration % 60
                caption = (
                    f"<b>{title}</b>\n"
                    f"<i>Ca sĩ:</i> {artists}\n"
                    f"<i>Thời lượng:</i> {minutes}:{seconds:02d}\n\n"
                    f"<a href='{link}'>Mở trên Spotify</a>"
                )

                # Gửi ảnh và thông tin bài hát
                bot.send_photo(message.chat.id, image, caption=caption, parse_mode="HTML")

                # Gửi tệp âm thanh MP3 cho người dùng
                if mp3_link:
                    bot.send_audio(message.chat.id, mp3_link)
        else:
            bot.reply_to(message, "Không tìm thấy kết quả.")
    except Exception as e:
        bot.reply_to(message, f"Lỗi khi tìm kiếm: {str(e)}")

    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

@bot.message_handler(commands=['roblox'])
def roblox_info(message):
    args = message.text.strip().split()
    if len(args) < 2:
        bot.reply_to(message, "❗ Vui lòng nhập username. Ví dụ: /roblox PixelFXStaker")
        return

    username = args[1]
    url = f"https://offvn.x10.mx/php/roblox.php?username={username}"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()
    except Exception as e:
        bot.reply_to(message, f"🚫 Không thể kết nối đến API.\nLỗi: {e}")
        return

    if data.get("status") != "success" or not data.get("data"):
        bot.reply_to(message, "❗ Không tìm thấy thông tin cho username này.")
        return

    d = data["data"]
    info = d.get("basicInfo") if isinstance(d.get("basicInfo"), dict) else {}
    presence = d.get("presence") if isinstance(d.get("presence"), dict) else {}

    name = info.get("name", "Không rõ")
    display_name = info.get("displayName", "Không rõ")
    user_id = info.get("id", "Không rõ")
    account_creation_date = d.get("accountCreationDate")
    created = account_creation_date[:10] if account_creation_date else "Không rõ"
    is_banned = "✅ Không" if not info.get("isBanned", False) else "❌ Có"
    is_premium = "💎 Có" if d.get("isPremium", False) else "🚫 Không"
    friend_count = d.get("friendCount", 0)
    followers_count = d.get("followersCount", 0)
    last_location = presence.get("lastLocation", "Không rõ")
    description = info.get("description", "Không có mô tả.")
    avatar_url = d.get("avatar", "")

    msg = (
        f"🎮 <b>Thông tin Roblox</b> 🎮\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Username:</b> <code>{name}</code>\n"
        f"🪧 <b>Display Name:</b> <code>{display_name}</code>\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
        f"📆 <b>Ngày tạo:</b> <code>{created}</code>\n"
        f"🔒 <b>Banned:</b> {is_banned}\n"
        f"💠 <b>Premium:</b> {is_premium}\n"
        f"👥 <b>Bạn bè:</b> <b>{friend_count}</b>\n"
        f"👣 <b>Theo dõi:</b> <b>{followers_count}</b>\n"
        f"🌐 <b>Hoạt động gần nhất:</b> <code>{last_location}</code>\n"
        f"📝 <b>Mô tả:</b> <i>{description if description else 'Không có mô tả.'}</i>\n"
        f"━━━━━━━━━━━━━━━━━━"
    )

    # Gửi thông tin Roblox
    if avatar_url:
        bot.send_photo(message.chat.id, avatar_url, caption=msg, parse_mode="HTML")
    else:
        bot.reply_to(message, msg, parse_mode="HTML")

    # Xóa tin nhắn lệnh của người dùng
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        # Một số trường hợp bot không có quyền xóa (ví dụ: không phải admin group), có thể bỏ qua lỗi này.
        print(f"Không thể xóa lệnh: {e}")

#===================================#
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https') and parsed.netloc != ""
    except:
        return False

@bot.message_handler(commands=['code'])
def handle_code_command(message):
    command_args = message.text.split(maxsplit=1)
    if len(command_args) < 2:
        bot.reply_to(message, "❗ *Hướng dẫn sử dụng:*\nGõ `/code https://yourwebsite.com` để lấy mã nguồn HTML.", parse_mode="Markdown")
        return

    url = command_args[1].strip()
    if not is_valid_url(url):
        bot.reply_to(message, "⛔ *URL không hợp lệ!* Hãy nhập đúng định dạng: `https://yourwebsite.com`", parse_mode="Markdown")
        return

    domain = urlparse(url).netloc.replace(":", "_")
    file_name = f"{domain}.html"

    try:
        bot.send_chat_action(message.chat.id, 'upload_document')
        response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        content = response.text
        if len(content.encode('utf-8')) > MAX_FILE_SIZE:
            bot.reply_to(message, "⚠️ Trang web này quá lớn (trên 5MB), không thể gửi file mã nguồn!")
            return

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(content)

        with open(file_name, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption=f"✅ *Mã nguồn HTML của*: `{url}`",
                parse_mode="Markdown"
            )
        # Xóa lệnh của người dùng sau khi hoàn thành
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception:
            pass  # Bỏ qua lỗi nếu không xóa được

        # Gửi tin nhắn mới (không reply vào tin nhắn đã bị xóa)
        bot.send_message(message.chat.id, "🎉 Đã gửi file mã nguồn HTML cho bạn!")

    except requests.RequestException as e:
        bot.send_message(message.chat.id, f"❌ *Lỗi khi tải trang web:*\n`{e}`", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ *Lỗi hệ thống:*\n`{e}`", parse_mode="Markdown")

    finally:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
            except Exception as e:
                bot.send_message(message.chat.id, f"⚠️ *Lỗi khi xóa file tạm:*\n`{e}`", parse_mode="Markdown")

#===================================#
@bot.message_handler(commands=['id', 'ID'])
def handle_id_command(message):
    args = message.text.split()
    reply = None

    # Nếu reply vào một tin nhắn
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        reply = f"""
👤 <b>Thông tin người dùng (qua reply):</b>
- ID: <code>{user.id}</code>
- Tên: <b>{user.first_name or ''} {user.last_name or ''}</b>
- Username: @{user.username if user.username else 'Không có'}
        """
    # Nếu nhập /id @username
    elif len(args) == 2 and args[1].startswith('@'):
        try:
            username = args[1][1:]
            user = bot.get_chat(username)
            reply = f"""
👤 <b>Thông tin người dùng @{username}:</b>
- ID: <code>{user.id}</code>
- Tên: <b>{user.first_name or ''} {user.last_name or ''}</b>
- Username: @{user.username if user.username else 'Không có'}
            """
        except Exception as e:
            reply = "❌ Không tìm thấy người dùng này hoặc bot không đủ quyền."
    # Nếu là group/supergroup
    elif message.chat.type in ["group", "supergroup"]:
        reply = f"""
👥 <b>Thông tin nhóm:</b>
- ID nhóm: <code>{message.chat.id}</code>
- Tên nhóm: <b>{message.chat.title}</b>
        """
    # Nếu là riêng tư
    elif message.chat.type == 'private':
        user = message.from_user
        reply = f"""
👤 <b>Thông tin của bạn:</b>
- ID: <code>{user.id}</code>
- Tên: <b>{user.first_name or ''} {user.last_name or ''}</b>
- Username: @{user.username if user.username else 'Không có'}
        """
    else:
        reply = "❓ Không xác định được đối tượng cần lấy ID.\nHãy dùng /id, reply tin nhắn hoặc /id @username"

    # Trả lời cho người dùng
    bot.reply_to(message, reply, parse_mode='HTML')
    
    # Gửi thông tin tới admin (nếu lấy được id user, group)
    try:
        bot.send_message(ADMIN_ID, f"🔔 <b>Có người vừa dùng lệnh /id:</b>\n\n{reply}", parse_mode='HTML')
    except Exception as e:
        print(f"Lỗi khi gửi thông tin tới admin: {e}")

    # XÓA LỆNH SAU KHI ĐÃ TRẢ LỜI
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Lỗi khi xóa lệnh: {e}")

#===================================#
API_TT = "https://gaitiktok.onrender.com/random?apikey=randomtnt"
session = requests.Session()

def get_flag(region):
    if not region: return "🌍"
    return "".join(chr(127397 + ord(c)) for c in region.upper())

def download_video(url, path='tkvd.mp4', timeout=15, max_retries=3):
    headers = {"User-Agent": "Mozilla/5.0"}
    for attempt in range(max_retries):
        try:
            with session.get(url, stream=True, timeout=timeout, headers=headers) as response:
                if response.status_code == 200:
                    with open(path, 'wb') as f:
                        for chunk in response.iter_content(4096):
                            f.write(chunk)
                    return path
        except Exception as e:
            print(f"❌ Lỗi tải video (lần {attempt+1}): {e}")
    return None

def cleanup(file, delay=60):
    def do_remove():
        try: os.remove(file)
        except: pass
    threading.Timer(delay, do_remove).start()

def format_filesize(size_bytes):
    # Nếu không có dữ liệu
    if not size_bytes or size_bytes == 0:
        return ""
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name)-1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_name[i]}"

@bot.message_handler(commands=['gaitt'])
def handle_gaitt(message):
    waiting = bot.reply_to(message, "🔎 <b>Đang lấy video TikTok...</b>", parse_mode='HTML')
    try:
        response = session.get(API_TT, timeout=10)
        if response.status_code != 200:
            raise Exception("⚠️ API không phản hồi!")
        data = response.json().get("data")
        if not data:
            raise Exception("⚠️ API không trả về dữ liệu!")
        video_url = data.get("play")
        if not video_url or not video_url.startswith("http"):
            raise Exception("⚠️ Không tìm thấy video hợp lệ!")

        bot.edit_message_text("📥 <i>Đang tải video...</i>", message.chat.id, waiting.message_id, parse_mode='HTML')
        video_path = download_video(video_url)
        if not video_path:
            raise Exception("⚠️ Không thể tải video!")

        # Lấy dữ liệu
        author = data.get('author', {})
        region = data.get('region', 'N/A')
        flag = get_flag(region)
        hashtags = " ".join(f"#{tag}" for tag in data.get("hashtags", [])) if data.get("hashtags") else ""
        tiktok_link = data.get("url", f"https://tiktok.com/@{author.get('unique_id','')}")
        duration = data.get("duration", 0)
        filesize = data.get("size", 0)  # Nếu API không có thì sẽ là 0
        create_time = data.get("create_time", 0)
        is_ad = data.get("is_ad", False)

        do_dai_video = f"⏳ Độ dài: {duration}s\n" if duration else ""
        dung_luong = f"💾 Dung lượng: {format_filesize(filesize)}\n" if filesize else ""
        la_ad = "📢 <b>Quảng cáo</b>\n" if is_ad else ""

        # Caption kiểu blockquote đẹp
        caption = (
            f"🎥 <strong>{data.get('title', 'Không có tiêu đề')}</strong>\n\n"
            f"<blockquote><i>"
            f"👤 Tác giả: <a href='https://www.tiktok.com/@{author.get('unique_id', '')}'>{author.get('nickname', 'N/A')}</a>\n"
            f"🌍 Khu Vực: {region} {flag}\n"
            f"{do_dai_video}"
            f"{dung_luong}"
            f"{la_ad}"
            f"---------------------------------------\n"
            f"▶️ Views: {data.get('play_count', 0)}\n"
            f"❤️ Likes: {data.get('digg_count', 0)}\n"
            f"💬 Comments: {data.get('comment_count', 0)}\n"
            f"🔄 Shares: {data.get('share_count', 0)}\n"
            f"⬇️ Downloads: {data.get('download_count', 0)}\n"
            f"📥 Favorites: {data.get('collect_count', 0)}"
            f"</i></blockquote>"
        )
        if hashtags:
            caption += f"\n<b>🎵 Hashtags:</b> <i>{hashtags}</i>"

        # Nút "Video khác"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 Video khác", callback_data="gaitt_new"))

        bot.delete_message(message.chat.id, waiting.message_id)
        bot.send_chat_action(message.chat.id, 'upload_video')
        with open(video_path, 'rb') as video:
            bot.send_video(
                message.chat.id, video=video, caption=caption,
                reply_to_message_id=message.message_id,
                parse_mode='HTML', supports_streaming=True, reply_markup=markup
            )
        cleanup(video_path, delay=60)

    except Exception as e:
        bot.edit_message_text(f"❌ <b>Lỗi:</b> {e}", message.chat.id, waiting.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "gaitt_new")
def handle_gaitt_new(call):
    handle_gaitt(call.message)
    bot.answer_callback_query(call.id, "Đang lấy video mới...")

#===================================#
LANGUAGES = {
    "en": ("Tiếng Anh", "🇬🇧"),
    "vi": ("Tiếng Việt", "🇻🇳"),
    "ja": ("Tiếng Nhật", "🇯🇵"),
    "ko": ("Tiếng Hàn", "🇰🇷"),
    "zh": ("Tiếng Trung", "🇨🇳"),
    "fr": ("Tiếng Pháp", "🇫🇷"),
    "de": ("Tiếng Đức", "🇩🇪"),
    "ru": ("Tiếng Nga", "🇷🇺"),
    "es": ("Tiếng Tây Ban Nha", "🇪🇸"),
    "it": ("Tiếng Ý", "🇮🇹"),
    "th": ("Tiếng Thái", "🇹🇭"),
    "id": ("Tiếng Indonesia", "🇮🇩"),
    "pt": ("Tiếng Bồ Đào Nha", "🇵🇹"),
    "hi": ("Tiếng Hindi", "🇮🇳"),
    "tr": ("Tiếng Thổ Nhĩ Kỳ", "🇹🇷"),
}

def get_lang_info(lang_code):
    name, flag = LANGUAGES.get(lang_code, (lang_code.upper(), "🌐"))
    return name, flag

@bot.message_handler(commands=['ggdich'])
def translate_message(message):
    content = message.text.split(" ", 2)
    if len(content) < 2 or not content[1].strip():
        bot.reply_to(message, (
            "⚠️ <b>Vui lòng cung cấp văn bản để dịch!</b>\n"
            "📌 <b>Cách dùng:</b> <code>/ggdich [ngôn_ngữ_đích] [văn_bản]</code>\n"
            "🌍 <b>Ví dụ:</b> <code>/ggdich en Xin chào cả nhà!</code>"
        ), parse_mode="HTML")
        return

    # Xác định ngôn ngữ đích & nội dung
    if len(content) == 2:
        target_lang = "vi"
        translate_this = content[1]
    else:
        target_lang = content[1].lower()
        translate_this = content[2]

    # Cảnh báo độ dài
    if len(translate_this) < 2:
        bot.reply_to(message, "🧐 <b>Văn bản quá ngắn để dịch!</b>", parse_mode="HTML")
        return
    if len(translate_this) > 1000:
        bot.reply_to(message, "🚫 <b>Văn bản quá dài (tối đa 1000 ký tự)!</b>", parse_mode="HTML")
        return

    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={requests.utils.quote(translate_this)}"

    try:
        response = requests.get(url, timeout=8)
        data = response.json()
        if not data or not data[0]:
            raise Exception("Không tìm thấy kết quả dịch.")

        translated_text = ''.join([item[0] for item in data[0] if item[0]])
        from_lang = data[2] if data[2] == data[8][0][0] else data[8][0][0]
        
        from_lang_name, from_flag = get_lang_info(from_lang)
        target_lang_name, to_flag = get_lang_info(target_lang)

        reply_message = (
            f"{from_flag} <b><u>{from_lang_name}</u></b> ➜ {to_flag} <b><u>{target_lang_name}</u></b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>🔸 Văn bản gốc:</b>\n<code>{translate_this}</code>\n"
            f"<b>🔹 Đã dịch:</b>\n<blockquote><i>{translated_text}</i></blockquote>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🧑‍💻 <b>HDSD:</b> <code>/ggdich [mã_ngôn_ngữ] [văn_bản]</code>\n"
            f"📌 <b>Ví dụ:</b> <code>/ggdich ja Tôi yêu tiếng Nhật</code>\n"
            f"🏷 <b>Mã phổ biến:</b> <code>en</code> (Anh), <code>vi</code> (Việt), <code>ja</code> (Nhật), <code>ko</code> (Hàn), <code>zh</code> (Trung), <code>fr</code> (Pháp)"
        )
        bot.reply_to(message, reply_message, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(
            message,
            f"❌ <b>Không thể dịch:</b> <code>{str(e)}</code>\n"
            "💡 <b>Đảm bảo bạn nhập đúng cú pháp và có kết nối mạng.</b>",
            parse_mode="HTML"
        )

#===================================#
def get_instagram_media(insta_url):
    api_url = f"https://insta-dl.hazex.workers.dev/?url={insta_url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data.get('result') and data['result'].get('url'):
            return data['result']['url'], data['result']['extension']
    return None, None

@bot.message_handler(commands=['downins'])
def insta_downloader(message):
    try:
        insta_url = message.text.replace("/downins", "").strip()
        if not insta_url:
            bot.reply_to(message, "⚠️ Vui lòng gửi kèm link Instagram sau lệnh /downins.\n💬 ví dụ: <code>/downins https://www.instagram.com/p/ChGhCPwpV0H/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA== </code>", parse_mode="HTML")
            return

        download_url, extension = get_instagram_media(insta_url)
        if download_url:
            if extension in ["mp4", "mkv"]:
                bot.send_chat_action(message.chat.id, "upload_video")
                bot.send_video(
                    message.chat.id,
                    video=download_url,
                    caption="🎥 Video Instagram",
                    reply_to_message_id=message.message_id
                )
            elif extension in ["jpg", "jpeg", "png"]:
                bot.send_chat_action(message.chat.id, "upload_photo")
                bot.send_photo(
                    message.chat.id,
                    photo=download_url,
                    caption="📸 Ảnh Instagram",
                    reply_to_message_id=message.message_id
                )
            else:
                bot.reply_to(message, "⚠️ Định dạng file không được hỗ trợ.")
                return
            # XÓA LỆNH SAU KHI GỬI FILE
            bot.delete_message(message.chat.id, message.message_id)
        else:
            bot.reply_to(message, "⚠️ Vui lòng gửi kèm link Instagram sau lệnh /downins.\n💬 ví dụ: <code>/downins https://www.instagram.com/p/ChGhCPwpV0H/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA== </code>", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, "⚠️ Đã xảy ra lỗi. Vui lòng thử lại sau.")

#===================================#
def parse_time(time_str):
    pattern = r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?"
    match = re.fullmatch(pattern, time_str.replace(" ", ""))
    if not match:
        return None
    days = int(match.group(1)) if match.group(1) else 0
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3)) if match.group(3) else 0
    if days == hours == minutes == 0:
        return None
    return timedelta(days=days, hours=hours, minutes=minutes)

def format_time(td):
    parts = []
    if td.days:
        parts.append(f"{td.days} ngày")
    hours = td.seconds // 3600
    if hours:
        parts.append(f"{hours} giờ")
    minutes = (td.seconds % 3600) // 60
    if minutes:
        parts.append(f"{minutes} phút")
    return " ".join(parts) if parts else "0 phút"

def get_vietnam_time(dt=None):
    if dt is None:
        utc_now = datetime.now(timezone.utc)
    else:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        utc_now = dt
    vietnam_now = utc_now + timedelta(hours=7)
    return vietnam_now.strftime("%d/%m/%Y %H:%M:%S")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔️ <b>Bạn không có quyền sử dụng lệnh này.</b>", parse_mode="HTML")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "❗️ <b>Hãy trả lời tin nhắn của người cần MUTE!</b>\n\n<b>Cú pháp:</b> <code>/mute 1h30m</code>", parse_mode="HTML")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❗️ <b>Bạn chưa nhập thời gian mute!</b>\n\n<b>Ví dụ:</b> <code>/mute 2h</code>", parse_mode="HTML")
        return

    time_str = args[1]
    delta = parse_time(time_str)
    if not delta:
        bot.reply_to(message, "❗️ <b>Định dạng thời gian chưa đúng!</b>\nVí dụ: <code>2h</code>, <code>1d3h15m</code>", parse_mode="HTML")
        return

    now_utc = datetime.now(timezone.utc)
    until_date = now_utc + delta
    user = message.reply_to_message.from_user
    user_id = user.id
    mention = f"<a href='tg://user?id={user_id}'>{user.first_name}</a>"

    try:
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=telebot.types.ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        bot.send_message(
            message.chat.id,
            f"""🔇 <b>{mention} đã bị mute trong {format_time(delta)}!</b>

⏰ <b>Bắt đầu:</b> {get_vietnam_time(now_utc)}
⏳ <b>Kết thúc:</b> {get_vietnam_time(until_date)}""",
            parse_mode="HTML",
            reply_to_message_id=message.reply_to_message.message_id
        )
        # XÓA lệnh /mute sau khi thành công
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        bot.reply_to(message, f"❌ <b>Không thể mute:</b> <code>{e}</code>", parse_mode="HTML")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔️ <b>Bạn không có quyền sử dụng lệnh này.</b>", parse_mode="HTML")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "❗️ <b>Hãy trả lời tin nhắn của người cần UNMUTE!</b>", parse_mode="HTML")
        return

    user = message.reply_to_message.from_user
    user_id = user.id
    mention = f"<a href='tg://user?id={user_id}'>{user.first_name}</a>"

    try:
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=telebot.types.ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_invite_users=True,
            )
        )
        bot.send_message(
            message.chat.id,
            f"🔊 <b>{mention} đã được unmute!</b>",
            parse_mode="HTML",
            reply_to_message_id=message.reply_to_message.message_id
        )
        # XÓA lệnh /unmute sau khi thành công
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        bot.reply_to(message, f"❌ <b>Không thể unmute:</b> <code>{e}</code>", parse_mode="HTML")

#===================================#
def get_flag(region):
    flags = {
        "VN": "🇻🇳", "TH": "🇹🇭", "BR": "🇧🇷", "ID": "🇮🇩",
        "SG": "🇸🇬", "US": "🇺🇸", "EU": "🇪🇺", "IN": "🇮🇳"
    }
    return flags.get(region.upper(), "🏳️")
@bot.message_handler(commands=['ff'])
def get_ff_info(message):
    chat_id = message.chat.id
    message_id = message.message_id
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Vui lòng nhập UID. Ví dụ: <code>/ff 12345678 SG</code>", parse_mode="HTML")
        return

    uid = args[1]
    region = args[2] if len(args) > 2 else "VN"  # Region mặc định là VN nếu không có
    url = f"https://ffwlxd-info.vercel.app/player-info?region={region}&uid={uid}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            bot.reply_to(message, "Không thể kết nối API, vui lòng thử lại sau.", parse_mode="HTML")
            return

        data = response.json()
        if not data.get("AccountInfo"):
            bot.reply_to(message, "Không tìm thấy thông tin người chơi!", parse_mode="HTML")
            return

        p = data["AccountInfo"]
        clan = data.get("GuildInfo", {})
        captain = data.get("captainBasicInfo", {})
        pet = data.get("petInfo", {})
        credit = data.get("creditScoreInfo", {})
        profile = data.get("AccountProfileInfo", {})
        social = data.get("socialinfo", {})

        info = f"""
<b>THÔNG TIN NGƯỜI CHƠI</b>
👤 <b>Nickname:</b> <code>{p.get('AccountName')}</code>
🆔 <b>UID:</b> <code>{uid}</code>
📈 <b>Level:</b> <code>{p.get('AccountLevel')}</code>
👍 <b>Like:</b> <code>{p.get('AccountLikes')}</code>
🧬 <b>XP:</b> <code>{p.get('AccountEXP')}</code>
🎖 <b>Rank:</b> <code>{p.get('BrMaxRank')} / {p.get('CsMaxRank')}</code>
🔥 <b>Điểm Rank:</b> <code>{p.get('BrRankPoint')} / {p.get('CsRankPoint')}</code>
📅 <b>Ngày tạo:</b> <code>{p.get('AccountCreateTime')}</code>
📆 <b>Đăng nhập cuối:</b> <code>{p.get('AccountLastLogin')}</code>
🌍 <b>Máy chủ:</b> <code>{p.get('AccountRegion')}</code>
⚙️ <b>Phiên bản:</b> <code>{p.get('ReleaseVersion')}</code>

<b>THÔNG TIN GUILD</b>
🏰 <b>Tên Quân Đoàn:</b> <code>{clan.get('GuildName')}</code>
🆔 <b>ID:</b> <code>{clan.get('GuildID')}</code>
📈 <b>Level:</b> <code>{clan.get('GuildLevel')}</code>
👥 <b>Thành viên:</b> <code>{clan.get('GuildMember')}/{clan.get('GuildCapacity')}</code>

<b>CHỦ QUÂN ĐOÀN</b>
👑 <b>Tên:</b> <code>{captain.get('nickname')}</code>
🆔 <b>UID:</b> <code>{captain.get('accountId')}</code>
📈 <b>Level:</b> <code>{captain.get('level')}</code>
👍 <b>Likes:</b> <code>{captain.get('liked')}</code>
📅 <b>Ngày tạo:</b> <code>{captain.get('createAt')}</code>

<b>THÔNG TIN PET</b>
🐾 <b>ID:</b> <code>{pet.get('id')}</code>
📈 <b>Level:</b> <code>{pet.get('level')}</code>
⚡️ <b>XP:</b> <code>{pet.get('exp')}</code>
🎯 <b>Kỹ năng:</b> <code>{pet.get('selectedSkillId')}</code>

<b>THÔNG TIN KHÁC</b>
❤️ <b>Credit Score:</b> <code>{credit.get('creditScore')}</code>
🧥 <b>Outfit:</b> <code>{profile.get('EquippedOutfit')}</code>
✍️ <b>Chữ ký:</b> <code>{social.get('AccountSignature')}</code>
"""

        # Avatar và Outfit
        avatar_url = f"https://aditya-banner-v3op.onrender.com/banner-image?uid={uid}&region={p.get('AccountRegion')}"
        outfit_url = f"https://outfitinfo.vercel.app/outfit-image?uid={uid}&region={p.get('AccountRegion')}&key=99day"
        info += f'\n<a href="{avatar_url}">🖼 Avatar của bạn</a>'

        bot.send_message(chat_id, info, reply_to_message_id=message_id, parse_mode="HTML")

        # Gửi ảnh outfit
        try:
            res_img = requests.get(outfit_url)
            if res_img.status_code == 200 and "image" in res_img.headers.get("Content-Type", ""):
                bot.send_photo(chat_id, BytesIO(res_img.content), caption="🧑‍🎤 Outfit của bạn")
            else:
                bot.send_message(chat_id, f"Không lấy được ảnh outfit. Xem tại đây: {outfit_url}")
        except Exception as e:
            print("Lỗi ảnh outfit:", e)
            bot.send_message(chat_id, f"Không lấy được ảnh outfit. Xem tại đây: {outfit_url}")

        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass

    except Exception as e:
        bot.reply_to(message, f"Lỗi xử lý: {str(e)}", parse_mode="HTML")
# ========== Hàm gửi tin nhắn rồi xóa sau delay giây ==========
def send_temp_message(chat_id, text, parse_mode=None, reply_to_message_id=None, delay=3):
    msg = bot.send_message(chat_id, text, parse_mode=parse_mode, reply_to_message_id=reply_to_message_id)
    threading.Timer(delay, lambda: safe_delete(msg)).start()
    return msg

def safe_delete(msg):
    try:
        bot.delete_message(msg.chat.id, msg.message_id)
    except:
        pass


# ========== Hàm gửi tạm thời (giả định) ==========
def send_temp_message(chat_id, text):
    bot.send_message(chat_id, text, parse_mode="HTML")  # hoặc tùy chỉnh

# ========== Hàm kiểm tra trạng thái hết hạn (giả định) ==========
def get_expired_status(user_id):
    # Trả về (expired, expired_type)
    return False, ""

# ========== Hàm kiểm tra quyền nhóm (giả định) ==========
def is_allowed_group(chat_id):
    return True
# ========== Hàm tự động buff ==========
def schedule_auto_buff(chat_id, username, message, user_id):
    WAIT_TIME = 900  # 15 phút
    send_temp_message(chat_id, f"⏳ [Auto Buff] Sẽ tự động buff lại @{username} sau 15 phút nữa (kể cả khi lỗi)!")
    threading.Timer(WAIT_TIME, do_buff_follow, args=(chat_id, username, message, user_id, True)).start()

# ========== Hàm buff follow ==========
def do_buff_follow(chat_id, username, message, user_id, is_auto=False):
    api2 = f"https://offvn.x10.mx/php/tttik.php?id={username}&key=offvnx"
    try:
        response2 = requests.get(api2, timeout=60, verify=False)
        if response2.status_code != 200:
            raise Exception("API response not OK")
        data_api = response2.json()
    except:
        send_temp_message(chat_id, f"❌ [Auto Buff] Lỗi Khi Lấy Thông Tin Tài Khoản @{username}")
        if auto_buff_by_username.get(username.lower(), False):
            schedule_auto_buff(chat_id, username, message, user_id)
        return

    if "data" not in data_api or "user_id" not in data_api["data"]:
        send_temp_message(chat_id, f"❌ [Auto Buff] Không Tìm Thấy Tài Khoản @{username}")
        if auto_buff_by_username.get(username.lower(), False):
            schedule_auto_buff(chat_id, username, message, user_id)
        return

    info = data_api["data"]
    profile_pic = info.get('profile_pic', '')
    create_time = info.get('create_time', 'N/A')

    followers_raw = info.get("followers", "0")
    try:
        follower_before = int(followers_raw.replace(",", "").strip())
    except ValueError:
        send_temp_message(chat_id, f"❌ [Auto Buff] Số follower của @{username} không hợp lệ: {followers_raw}")
        if auto_buff_by_username.get(username.lower(), False):
            schedule_auto_buff(chat_id, username, message, user_id)
        return

    # Tiến hành buff
    api1 = f"https://offvn.x10.mx/fl.php?username={username}"
    try:
        response1 = requests.get(api1, timeout=60, verify=False)
        if response1.status_code != 200:
            raise Exception("API response not OK")
        response1_data = response1.json()
        if response1_data.get("success") is False:
            message_text = response1_data.get("message", "")
            send_temp_message(chat_id, f"❌ [Auto Buff] Tăng Follow Thất Bại @{username}\nLý do: {html.escape(message_text)}")
            if auto_buff_by_username.get(username.lower(), False):
                schedule_auto_buff(chat_id, username, message, user_id)
            return
    except:
        send_temp_message(chat_id, f"❌ [Auto Buff] Tăng Follow Thất Bại (Lỗi khi gọi API) @{username}")
        if auto_buff_by_username.get(username.lower(), False):
            schedule_auto_buff(chat_id, username, message, user_id)
        return

    # Lấy lại số follower mới
    try:
        response_check = requests.get(api2, timeout=60, verify=False)
        if response_check.status_code != 200:
            raise Exception("API response not OK")
        new_info = response_check.json().get("data", {})
        followers_after_raw = new_info.get("followers", "0")
        try:
            follower_after = int(followers_after_raw.replace(",", "").strip())
        except ValueError:
            follower_after = follower_before
    except:
        follower_after = follower_before

    follower_diff = follower_after - follower_before

    # === Xác định trạng thái ===
    if follower_diff > 0:
        trang_thai = "Thành công ✅"
    else:
        trang_thai = "Thất Bại ❌"

    caption = f"""<blockquote>╭─────────────⭓
│<b>👤 Name:</b> {html.escape(info.get('nickname', 'N/A'))}
│<b>🆔 UID:</b> {info.get('user_id', 'N/A')}
│<b>🔗 Username:</b> @{html.escape(username)}
│<b>🗓️ Ngày tạo:</b> {html.escape(create_time)}
├─────────────⭔
│<b>📉 FOLLOW BAN ĐẦU:</b> {follower_before:,} Followers
│<b>📊 FOLLOW HIỆN TẠI:</b> {follower_after:,} Followers
│<b>📈 FOLLOW ĐÃ TĂNG:</b> +{follower_diff:,}
│<b>📋 TRẠNG THÁI:</b> {trang_thai}
╰─────────────⭓</blockquote>
<i> NẾU MUỐN TREO TỰ ĐỘNG HÃY NHẮN TIN 📩 @off_vn ĐỂ HỖ TRỢ.</i>
    """

    try:
        if profile_pic:
            bot.send_photo(chat_id, photo=profile_pic, caption=caption, parse_mode="HTML")
        else:
            raise Exception("No profile pic")
    except:
        bot.send_message(chat_id, caption, parse_mode="HTML")

    if auto_buff_by_username.get(username.lower(), False):
        schedule_auto_buff(chat_id, username, message, user_id)
# ========== Handler cho lệnh /auto ==========
@bot.message_handler(commands=['auto'])
def toggle_auto_buff_user(message):
    if message.from_user.id != ADMIN_ID:
        send_temp_message(message.chat.id, "⛔️ Bạn không có quyền sử dụng lệnh này!")
        return

    args = message.text.split()
    if len(args) < 3 or args[1].lower() not in ['on', 'off']:
        send_temp_message(
            message.chat.id, 
            "⚠️ Sử dụng\nNếu bật ✅ thì nhập /auto on [username]\nNếu tắt ❌ nhập /auto off [username]"
        )
        return

    status = args[1].lower()
    username = args[2].strip().lower()
    auto_buff_by_username[username] = (status == 'on')

    if status == 'on':
        send_temp_message(
            message.chat.id, 
            f"✅ Đã bật tự động buff lại sau 15 phút cho @{username}"
        )
    else:
        send_temp_message(
            message.chat.id, 
            f"❌ Đã tắt tự động buff lại sau 15 phút cho @{username}"
        )
    
    # Xóa lệnh sau khi thành công
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

# Hàm gửi tin nhắn tạm thời và tự xóa sau `delay` giây
def send_temp_message(chat_id, text, delay=3):
    msg = bot.send_message(chat_id, text)
    threading.Timer(delay, lambda: delete_message_safe(chat_id, msg.message_id)).start()

def delete_message_safe(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

# ========== Handler cho lệnh /fl ==========
@bot.message_handler(commands=['fl'])
def handle_fl(message):
    chat_id = message.chat.id
    message_id = message.message_id
    user_id = message.from_user.id
    expired, expired_type = get_expired_status(user_id)

    if expired:
        bot.send_message(chat_id, f"🔒 Key {expired_type} của bạn đã hết hạn! Hãy lấy lại key bằng lệnh /laykey.", parse_mode="Markdown")
        return

    if user_id not in valid_keys and user_id not in vip_keys:
        bot.send_message(
            chat_id,
            "⚠️ Bạn chưa có key hoặc key không hợp lệ. Lấy key bằng lệnh /laykey và nhập lại với /k.",
            parse_mode="Markdown"
        )
        return

    if not is_allowed_group(chat_id):
        bot.send_message(chat_id, "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.", reply_to_message_id=message_id)
        return

    args = message.text.split()
    if len(args) < 2:
        bot.send_message(
            chat_id,
            "<b>⚠️ Vui Lòng Nhập Username TikTok</b> \n\nVí dụ: \n<code>/fl fanduonghoang</code>",
            parse_mode="HTML"
        )
        return

    username = args[1].strip().lower()
    auto_status = auto_buff_by_username.get(username, False)
    send_temp_message(chat_id, f"Chức năng tự động của @{username} hiện tại {'BẬT ✅' if auto_status else 'TẮT ❌'}")

    # Kiểm tra xem người dùng đã chờ chưa
    if chat_id in waiting_users and username in waiting_users[chat_id]:
        remaining_time = int(waiting_users[chat_id][username] - time.time())
        if remaining_time > 0:
            send_temp_message(chat_id, f"⏳ Bạn vẫn phải chờ {remaining_time // 60} phút trước khi thử lại @{username}.")
            return
        else:
            del waiting_users[chat_id][username]

    # Hiển thị thông báo tiến trình
    processing_msg = bot.send_message(
        chat_id,
        f"""
⏳ <b>Đang tiến hành buff FOLLOW</b> @{html.escape(username)}
<i>🔄 Vui lòng chờ trong giây lát...</i>
        """,
        parse_mode="HTML"
    )

    try:
        do_buff_follow(chat_id, username, message, user_id, is_auto=False)
    finally:
        try:
            bot.delete_message(processing_msg.chat.id, processing_msg.message_id)
        except:
            pass

    # Đặt thời gian chờ cho username đó
    WAIT_TIME = 900  # 15 phút
    if chat_id not in waiting_users:
        waiting_users[chat_id] = {}
    waiting_users[chat_id][username] = time.time() + WAIT_TIME

    # Xóa message gốc để tránh spam
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
#===================================#
@bot.message_handler(commands=['downfb'])
def download_fb_video(message):
    chat_id = message.chat.id
    message_id = message.message_id
    if not is_allowed_group(chat_id):
        bot.reply_to(message, "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.")
        return
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Vui lòng nhập URL Facebook hợp lệ. Ví dụ: /downfb https://www.facebook.com/share/r/1E1nqWLhyz/")
        return

    fb_url = args[1]
    api_url = f"https://subhatde.id.vn/fb/download?url={fb_url}"

    try:
        res = requests.get(api_url)
        data = res.json()

        if not data.get("medias"):
            bot.reply_to(message, "❌ Không tìm thấy video. Vui lòng kiểm tra lại URL.")
            return

        medias = data["medias"]
        links = {media["quality"]: media["url"] for media in medias if media["type"] == "video"}

        if not links:
            bot.reply_to(message, "❌ Không tìm thấy video.")
            return

        user_video_info[message.from_user.id] = {"links": links, "command_msg_id": message.message_id}

        markup = InlineKeyboardMarkup()
        if "HD" in links:
            markup.add(InlineKeyboardButton("Tải HD", callback_data="download_HD"))
        if "SD" in links:
            markup.add(InlineKeyboardButton("Tải SD", callback_data="download_SD"))

        bot.send_message(
            message.chat.id,
            "<b>Chọn chất lượng để tải video:</b>",
            parse_mode="HTML",
            reply_markup=markup
        )

    except Exception as e:
        bot.reply_to(message, f"Lỗi: {str(e)}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("download_"))
def callback_download_video(call):
    user_id = call.from_user.id
    info = user_video_info.get(user_id)
    if not info:
        bot.answer_callback_query(call.id, "❌ Không tìm thấy thông tin video!")
        return

    quality = call.data.split("_")[1]
    video_url = info["links"].get(quality)
    if not video_url:
        bot.answer_callback_query(call.id, f"❌ Không có video chất lượng {quality}")
        return

    try:
        filename = f"temp_{user_id}_{quality}.mp4"
        video_data = requests.get(video_url)
        with open(filename, 'wb') as f:
            f.write(video_data.content)

        # Xóa inline keyboard trên message cũ
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )

        # Tạo nút cho các chất lượng còn lại (nếu có)
        other_qualities = [q for q in info["links"] if q != quality]
        markup = None
        if other_qualities:
            markup = InlineKeyboardMarkup()
            for q in other_qualities:
                markup.add(InlineKeyboardButton(f"Tải {q}", callback_data=f"download_{q}"))

        safe_quality = html.escape(quality)
        with open(filename, 'rb') as video:
            bot.send_video(
                call.message.chat.id,
                video,
                caption=f"<b>Chất lượng:</b> {safe_quality}",
                parse_mode="HTML",
                reply_markup=markup
            )
        os.remove(filename)
        bot.answer_callback_query(call.id, f"Đã gửi video {quality}!")

        # Xóa lệnh gốc của user (/downfb ...)
        if "command_msg_id" in info:
            try:
                bot.delete_message(call.message.chat.id, info["command_msg_id"])
            except:
                pass

        # Nếu đã tải hết mọi chất lượng, xóa luôn info
        if not other_qualities:
            user_video_info.pop(user_id, None)

    except Exception as e:
        bot.answer_callback_query(call.id, "Lỗi khi tải/gửi video!")
        bot.send_message(call.message.chat.id, f"Lỗi: {str(e)}")

#===================================#
VN_WEATHER = {
    "clear sky": "Trời quang",
    "few clouds": "Ít mây",
    "scattered clouds": "Mây rải rác",
    "broken clouds": "Mây từng phần",
    "overcast clouds": "Nhiều mây",
    "shower rain": "Mưa rào",
    "light rain": "Mưa nhẹ",
    "rain": "Mưa",
    "moderate rain": "Mưa vừa",
    "heavy intensity rain": "Mưa to",
    "thunderstorm": "Dông",
    "snow": "Tuyết",
    "mist": "Sương mù",
    "haze": "Mù khô",
    "fog": "Sương mù",
    "drizzle": "Mưa phùn"
}

def get_geocode(city):
    try:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={WEATHER_API_KEY}"
        res = requests.get(url).json()
        if res:
            return res[0]['lat'], res[0]['lon']
        return None, None
    except Exception as e:
        logger.error("Lỗi geocode: %s", e)
        return None, None

def get_weather(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?appid={WEATHER_API_KEY}&lat={lat}&lon={lon}&units=metric"
        return requests.get(url).json()
    except Exception as e:
        logger.error("Lỗi weather: %s", e)
        return {}

def get_uv_index(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/uvi?appid={WEATHER_API_KEY}&lat={lat}&lon={lon}"
        res = requests.get(url).json()
        return res.get('value')
    except Exception as e:
        logger.error("Lỗi UV Index: %s", e)
        return None

def format_weather(data, city):
    if not data or data.get('cod') != 200:
        return f"❌ Không tìm thấy {city}"

    weather = data['weather'][0]
    desc_en = weather['description']
    desc_vn = VN_WEATHER.get(desc_en, desc_en.capitalize())
    main = data['main']
    wind = data.get('wind', {})
    clouds = data.get('clouds', {}).get('all', 0)
    sys = data.get('sys', {})
    rain = data.get('rain', {}).get('1h', 0)
    snow = data.get('snow', {}).get('1h', 0)
    visibility = data.get('visibility', 0)
    lat, lon = data['coord']['lat'], data['coord']['lon']
    timezone_offset = data.get('timezone', 0)
    sunrise = sys.get('sunrise')
    sunset = sys.get('sunset')

    def unixtime_to_str(utime):
        if utime is None: return "?"
        # Chuẩn theo khuyến nghị mới, không còn DeprecationWarning
        local_time = datetime.fromtimestamp(utime, tz=timezone.utc) + timedelta(seconds=timezone_offset)
        return local_time.strftime('%H:%M')

    # AQI
    try:
        aqi = None
        air_pollution = requests.get(
            f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
        ).json()
        if air_pollution and air_pollution.get('list'):
            aqi = air_pollution['list'][0]['main']['aqi']
    except Exception:
        aqi = None

    # UV Index
    uv_index = get_uv_index(lat, lon)

    # Định dạng tin nhắn
    msg = f"🌦 <b>{city.title()}, {sys.get('country','')}</b> | <i>{desc_vn}</i>\n"
    msg += f"🌡 Nhiệt độ: <b>{main['temp']}°C</b> (cảm giác như {main['feels_like']}°C)\n"
    msg += f"⬆️ Max: {main['temp_max']}°C\n"
    msg += f"⬇️ Min: {main['temp_min']}°C\n"
    msg += f"💧 Độ ẩm: {main['humidity']}%\n"
    msg += f"🍃 Áp suất: {main['pressure']} hPa\n"
    msg += f"☁️ Mây: {clouds}%\n"
    msg += f"💨 Gió: {wind.get('speed',0)} m/s, hướng {wind.get('deg','?')}°\n"
    msg += f"👁️ Tầm nhìn: {visibility/1000:.1f} km\n"
    if rain: msg += f"🌧️ Mưa (1h): {rain} mm\n"
    if snow: msg += f"❄️ Tuyết (1h): {snow} mm\n"
    if aqi: msg += f"?? Chất lượng không khí (AQI): {aqi}/5\n"
    if uv_index: msg += f"☀️ Chỉ số UV: {uv_index}\n"
    msg += f"🌅 Mặt trời mọc: {unixtime_to_str(sunrise)}\n"
    msg += f"🌇 Mặt trời lặn: {unixtime_to_str(sunset)}\n"
    msg += f"🗺 <a href='{GOOGLE_MAPS_URL}{lat},{lon}'>Vị trí trên bản đồ</a>"
    return msg

# Handler thời tiết
@bot.message_handler(commands=['thoitiet'])
def thoitiet(message):
    chat_id = message.chat.id
    message_id = message.message_id
    if not is_allowed_group(chat_id):
        bot.reply_to(message, "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.")
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        # Không dùng dấu < > để tránh lỗi HTML parse
        bot.reply_to(message, "📝 Dùng: /thoitiet [tên thành phố]")
        return
    city = args[1]
    lat, lon = get_geocode(city)
    if lat and lon:
        data = get_weather(lat, lon)
        msg = format_weather(data, city)
        # Nếu msg có HTML thì mới dùng parse_mode='HTML'
        bot.reply_to(message, msg, parse_mode='HTML', disable_web_page_preview=True)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_location(message.chat.id, latitude=lat, longitude=lon)
    else:
        bot.reply_to(message, "❌ Không tìm thấy tọa độ thành phố.")

#===================================#
start_time = time.time()

def format_time_unit(value, singular, plural):
    return f"{value} {singular if value == 1 else plural}"

def format_uptime(uptime_seconds):
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []
    if days:
        parts.append(format_time_unit(days, "ngày", "ngày"))
    if hours:
        parts.append(format_time_unit(hours, "giờ", "giờ"))
    if minutes:
        parts.append(format_time_unit(minutes, "phút", "phút"))
    parts.append(format_time_unit(seconds, "giây", "giây"))
    return ', '.join(parts)

def delete_message_later(chat_id, message_id, delay=10):
    """Xóa tin nhắn sau 'delay' giây."""
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Không thể xóa tin nhắn: {e}")

@bot.message_handler(commands=['time'])
def bot_uptime(message):
    chat_id = message.chat.id
    message_id = message.message_id
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)
    uptime_str = format_uptime(uptime_seconds)

    boot_time = datetime.fromtimestamp(start_time, tz=timezone(timedelta(hours=7)))
    now_time = datetime.now(timezone(timedelta(hours=7)))

    response = f"""
<b>⏰ Thời gian hoạt động của bot</b>

<b>🔋 Uptime:</b> <code>{uptime_str}</code>
<b>🟢 Bot khởi động lúc:</b> <code>{boot_time.strftime('%d/%m/%Y %H:%M:%S')}</code>
<b>⌚ Thời gian hiện tại:</b> <code>{now_time.strftime('%d/%m/%Y %H:%M:%S')}</code>
    """.strip()

    # Gửi trả lời
    reply = bot.reply_to(message, response, parse_mode='HTML')

    # Xóa tin nhắn lệnh của user
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Không thể xóa lệnh của user: {e}")

    # (Tùy chọn) Xóa tin nhắn trả lời của bot sau 10 giây
    # Nếu không cần thì có thể bỏ phần này
    delay_seconds = 20
    threading.Thread(target=delete_message_later, args=(reply.chat.id, reply.message_id, delay_seconds)).start()

#===================================#
def get_expired_status(user_id):
    """Trả về (True, loại_key) nếu user key hết hạn, ngược lại (False, None)"""
    now = datetime.now()
    if user_id in valid_keys:
        exp = valid_keys[user_id].get('expiration')
        if exp and now > datetime.strptime(exp, "%d/%m/%Y %H:%M:%S"):
            valid_keys.pop(user_id, None)
            return True, "thường"
    if user_id in vip_keys:
        exp = vip_keys[user_id].get('expiration')
        if exp and now > datetime.strptime(exp, "%d/%m/%Y %H:%M:%S"):
            vip_keys.pop(user_id, None)
            return True, "VIP"
    return False, None

def get_key_info(user_id):
    """Trả về dict info key (bao gồm loại, trạng thái, ngày hết hạn,...)"""
    now = datetime.now()
    info = {}
    if user_id in vip_keys:
        key_data = vip_keys[user_id]
        exp = datetime.strptime(key_data['expiration'], "%d/%m/%Y %H:%M:%S")
        info = {
            'type': 'VIP',
            'key': key_data['key'],
            'created': (exp - timedelta(days=30)).strftime("%d/%m/%Y %H:%M:%S"),
            'expired': key_data['expiration'],
            'status': '🟢 Còn hạn' if now < exp else '🔴 Hết hạn'
        }
    elif user_id in valid_keys:
        key_data = valid_keys[user_id]
        exp = datetime.strptime(key_data['expiration'], "%d/%m/%Y %H:%M:%S")
        info = {
            'type': 'Thường',
            'key': key_data['key'],
            'created': (exp - timedelta(days=1)).strftime("%d/%m/%Y %H:%M:%S"),
            'expired': key_data['expiration'],
            'status': '🟢 Còn hạn' if now < exp else '🔴 Hết hạn'
        }
    return info

@bot.message_handler(commands=['laykey'])
def getkey_cmd(message):
    user_id = int(message.from_user.id)
    current_date = get_vietnam_time()
    full_name = message.from_user.full_name
    current_day = int(datetime.now().strftime('%d'))
    keyso = str(current_day * 8276383 + 93732373 * user_id + user_id * user_id - current_day)
    key = f"BOT/{keyso}"
    url = f"https://link4m.co/api-shorten/v2?api=6506fd36fba45f6d07613987&url=https://offvn.x10.mx?key={key}"
    data = requests.get(url).json()
    linkvuot = data.get('shortenedUrl', 'Lỗi lấy link')
    tgsuccess = datetime.now().strftime("%d/%m/%Y")
    video = random.choice([
    "https://spamcallsms.x10.mx/4.mp4",
    "https://spamcallsms.x10.mx/11.mp4",
    "https://spamcallsms.x10.mx/2.mp4",
    "https://spamcallsms.x10.mx/3.mp4",
    "https://spamcallsms.x10.mx/5.mp4",
    "https://spamcallsms.x10.mx/6.mp4",
    "https://spamcallsms.x10.mx/7.mp4",
    "https://spamcallsms.x10.mx/8.mp4",
    "https://spamcallsms.x10.mx/9.mp4",
    "https://spamcallsms.x10.mx/10.mp4",
])

    help_text = (
        f"👋 Xin chào <a href='tg://user?id={user_id}'>{full_name}</a>!\n\n"
        f"📅 <b>Ngày:</b> {current_date}\n"
        f"🌐 <b>Link nhận key:</b> {linkvuot}\n\n"
        f"⚠️ <b>HƯỚNG DẪN:</b>\n"
        f"1️⃣ Truy cập link trên, lấy key vượt link.\n"
        f"2️⃣ Dùng lệnh <code>/k [KEY]</code> để xác thực key.\n"
        f"💡 <b>Ví dụ:</b> <code>/k BOT/42236748505484322438</code>\n"
        f"📩 Sau khi xác thực, bạn có thể dùng được lệnh\n"
    )

    bot.send_video(
        message.chat.id, 
        video=video, 
        caption=help_text, 
        reply_to_message_id=message.message_id, 
        supports_streaming=True, 
        parse_mode='HTML'
    )

@bot.message_handler(commands=['k'])
def key_cmd(message):
    args = message.text.split(" ")
    user_id = message.from_user.id

    if len(args) < 2:
        bot.reply_to(message, "⚠️ Vui lòng nhập key hợp lệ. Ví dụ: `/k BOT/42236748505409835000`", parse_mode="Markdown")
        return

    input_key = args[1]
    current_day = int(datetime.now().strftime('%d'))
    correct_key = f"BOT/{str(current_day * 8276383 + 93732373 * user_id + user_id * user_id - current_day)}"

    # Check key VIP hoặc key ngày
    expired, expired_type = get_expired_status(user_id)
    if expired:
        bot.reply_to(message, f"🔒 Key {expired_type} của bạn đã hết hạn! Hãy lấy lại key mới với lệnh /laykey.", parse_mode="Markdown")
        return

    if (input_key == correct_key) or (user_id in vip_keys):
        if user_id in vip_keys:
            info = get_key_info(user_id)
            bot.reply_to(
                message,
                f"✅ Bạn đã có key VIP ({info['key']})\n"
                f"⏰ Hết hạn: {info['expired']}\n"
                f"Trạng thái: {info['status']}\n\n"
                f"<b>Bây giờ bạn có thể dùng được lệnh</b>",
                parse_mode="HTML"
            )
            return

        expiration_date = datetime.now() + timedelta(days=1)
        expiration_str = expiration_date.strftime("%d/%m/%Y %H:%M:%S")
        valid_keys[user_id] = {'key': input_key, 'day': current_day, 'expiration': expiration_str}
        bot.reply_to(
            message,
            f"✅ Xác thực key thành công!\n"
            f"🔑 Key: <code>{input_key}</code>\n"
            f"⏰ Thời hạn: {expiration_str}\n"
            f"<b>Bây giờ bạn có thể dùng được lệnh</b>",
            parse_mode="HTML"
        )
    else:
        bot.reply_to(message, "❌ Key không hợp lệ. Vui lòng kiểm tra lại hoặc lấy key mới với /laykey.", parse_mode="Markdown")

@bot.message_handler(commands=['themvip'])
def add_vip_direct(message):
    user_id = message.from_user.id

    if user_id != ADMIN_ID:
        bot.reply_to(
            message,
            "⚠️ Bạn không có quyền sử dụng lệnh này. Chỉ admin mới được cấp quyền VIP.",
            parse_mode="Markdown"
        )
        return

    args = message.text.strip().split(" ")
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(
            message,
            "⚠️ Vui lòng nhập đúng Telegram user ID. Ví dụ: `/themvip 6452283369 365`",
            parse_mode="Markdown"
        )
        return

    target_user_id = int(args[1])
    days = 30
    if len(args) >= 3 and args[2].isdigit():
        days = int(args[2])
        if days <= 0 or days > 365:
            bot.reply_to(
                message,
                "⚠️ Số ngày VIP phải trong khoảng 1-365.",
                parse_mode="Markdown"
            )
            return

    expired, _ = get_expired_status(target_user_id)
    if target_user_id in vip_keys and not expired:
        key_info = get_key_info(target_user_id)
        bot.reply_to(
            message,
            f"❗ Người dùng này đã có quyền VIP còn hạn!\n"
            f"⏰ Hết hạn: {key_info.get('expired', '')}",
            parse_mode="Markdown"
        )
        return

    expiration_date = datetime.now() + timedelta(days=days)
    expiration_str = expiration_date.strftime("%d/%m/%Y %H:%M:%S")
    vip_keys[target_user_id] = {"key": "no-key", "expiration": expiration_str}

    bot.reply_to(
        message,
        f"✅ Đã cấp quyền VIP trực tiếp cho user `{target_user_id}` trong {days} ngày!\n"
        f"⏰ Hết hạn: {expiration_str}",
        parse_mode="Markdown"
    )

    try:
        bot.send_message(
            target_user_id,
            f"✅ Bạn đã được cấp quyền VIP trong {days} ngày!\n"
            f"⏰ Hết hạn: {expiration_str}\n"
            f"➡️ Các tính năng VIP hiện đã được mở khóa.",
            parse_mode="Markdown"
        )
    except Exception:
        pass

    # Xóa lệnh gốc
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception:
        pass
@bot.message_handler(commands=['mail'])
def create_mail(message):
    chat_id = message.chat.id
    message_id = message.message_id
    if not is_allowed_group(chat_id):
        bot.send_message(chat_id, "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.", reply_to_message_id=message_id)
        return
    user_id = message.from_user.id
    expired, expired_type = get_expired_status(user_id)
    if expired:
        bot.reply_to(message, f"🔒 Key {expired_type} của bạn đã hết hạn! Hãy lấy lại key bằng lệnh /laykey.", parse_mode="Markdown")
        return

    if user_id not in valid_keys and user_id not in vip_keys:
        bot.reply_to(
            message,
            "⚠️ Bạn chưa có key hoặc key không hợp lệ. Lấy key bằng lệnh /laykey và nhập lại với /k.",
            parse_mode="Markdown"
        )
        return

    args = message.text.strip().split(" ")
    if len(args) < 2:
        bot.reply_to(
            message,
            "❌ Vui lòng nhập tên email. Ví dụ: `/mail offvnx`, không cần nhập @hunght1890.com phía sau.",
            parse_mode="Markdown"
        )
        return
        
    email_name = args[1]
    email = f"{email_name}@hunght1890.com"
    info = get_key_info(user_id)
    bot.reply_to(
        message,
        f"📧 Email của bạn là: `{email}`\n"
        f"🔑 Loại key: {info.get('type', 'Không xác định')}\n"
        f"⏰ Hạn key: {info.get('expired', 'N/A')}\n"
        f"✅ Sau khi tạo mail thành công, nhập lệnh `/sms {email_name}` để kiểm tra hộp thư.",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['sms'])
def check_inbox(message):
    chat_id = message.chat.id
    message_id = message.message_id
    if not is_allowed_group(chat_id):
        bot.send_message(chat_id, "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.", reply_to_message_id=message_id)
        return
    user_id = message.from_user.id
    expired, expired_type = get_expired_status(user_id)
    if expired:
        bot.reply_to(
            message,
            f"🔒 Key {expired_type} của bạn đã hết hạn! Hãy lấy lại key bằng lệnh /laykey.",
            parse_mode="Markdown"
        )
        return

    if user_id not in valid_keys and user_id not in vip_keys:
        bot.reply_to(
            message,
            "⚠️ Bạn chưa có key hoặc key không hợp lệ. Vui lòng nhập key bằng lệnh `/k` trước!",
            parse_mode="Markdown"
        )
        return

    args = message.text.strip().split(" ")
    if len(args) < 2:
        bot.reply_to(
            message,
            "❌ Vui lòng nhập tên email để kiểm tra hộp thư. Ví dụ: `/sms offvnx`",
            parse_mode="Markdown"
        )
        return

    email_name = args[1]
    email = f"{email_name}@hunght1890.com"
    url = BASE_URL.format(email)

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 404:
            bot.reply_to(
                message,
                f"📭 Hộp thư `{email}` hiện chưa có thư nào.",
                parse_mode="Markdown"
            )
            return
        elif response.status_code == 500:
            bot.reply_to(
                message,
                "❌ Lỗi server, vui lòng thử lại sau.",
                parse_mode="Markdown"
            )
            return
        elif response.status_code == 200:
            emails = response.json()
            if not emails:
                bot.reply_to(
                    message,
                    f"📭 Hộp thư `{email}` hiện chưa có thư nào.",
                    parse_mode="Markdown"
                )
                return

            reply_msg = f"📥 *Hộp thư của `{email}`*:\n"
            for idx, mail in enumerate(emails[:3], 1):
                reply_msg += (
                    f"\n━━━━━━━━━━ {idx} ━━━━━━━━━━"
                    f"\n✉️ *Từ*: `{mail.get('from', 'Không rõ')}`"
                    f"\n📌 *Tiêu đề*: `{mail.get('subject', 'Không rõ')}`"
                    f"\n📥 *Gửi đến*: `{mail.get('to', 'Không rõ')}`"
                    f"\n🕒 *Thời gian*: `{mail.get('date', 'Không rõ')}`\n"
                )
            reply_msg += "\n\n💡 Xem thêm bằng cách truy cập lại sau hoặc nhập lại lệnh."

            bot.reply_to(
                message,
                reply_msg,
                parse_mode="Markdown"
            )
            return
        else:
            bot.reply_to(
                message,
                "❌ Lỗi không xác định, vui lòng thử lại.",
                parse_mode="Markdown"
            )
    except requests.RequestException:
        bot.reply_to(
            message,
            "❌ Không thể kết nối đến API, vui lòng thử lại sau.",
            parse_mode="Markdown"
        )

#===================================#
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    chat_id = message.chat.id
    message_id = message.message_id
    help_text = (
        "<b>DƯỚI ĐÂY LÀ DANH SÁCH LỆNH\n"
        "╔═══════════════╗\n"
        "╠ /proxy - Reg Proxy\n"
        "╠ /search - Tìm kiếm bài hát trên Spotify\n"
        "╠ /spotify - Download nhạc trên Spotify\n"
        "╠ /roblox - Check thông tin roblox\n"
        "╠ /code - Lấy source HTML website\n"
        "╠ /id - Xem id nhóm hoặc id bản thân\n"
        "╠ /ggdich - Dịch ngôn ngữ\n"
        "╠ /gaitt - Random gái xinh tiktok\n"
        "╠ /downins - Tải video + ảnh Instagram\n"
        "╠ /ff - Check Thông Tin Free Fire\n"
        "╠ /fl - Buff follow Tiktok 🆕\n"
        "╠ /thoitiet - Lấy thông tin thời tiết\n"
        "╠ /ip - Check Thông Tin IP\n"
        "╠ /github - Lấy thông tin github\n"
        "╠ /scr - Tải source bot telegram 📁\n"
        "╠ /downfb - Tải video từ facebook\n"
        "╠ /mail - Tạo mail và đọc hộp thư mail 📮\n"
        "╠ /qrnd - Tạo QR Bank Có Nội Dung\n"
        "╠ /2fa - Lấy mã Two-Factor Authentication\n"
        "╠ /fb - Check Thông Tin Facebook\n"
        "╠ /vipham - Check Phạt Nguội Xe Máy, Xe Ô Tô\n"
        "╠ /kqxs - Xem Kết Quả Xổ Số Hôm Nay\n"
        "╠ /qrbank - Tạo QR Chuyển Khoản\n"
        "╠ /qrcode - Tạo mã QR Từ Văn Bản\n"
        "╠ /tt - Check Info Nick Tiktok\n"
        "╠ /idfb - Lấy ID Facebook\n"
        "╠ /thongtin - Xem Thông Tin Nick Telegram\n"
        "╠ /ask - Trả Lời Tất Cả Câu Hỏi Chat Gemini\n"
        "╠ /tv - Đổi Tiếng Việt Trên Telegram\n"
        "╠ /tiktok - Tải Video Không Logo Tiktok\n"
        "╚═══════════════╝</b>\n"
        "💬 LƯU Ý: Bạn có thể bấm vào các lệnh để xem hướng dẫn sử dụng."
    )

    bot.send_message(
        chat_id,
        help_text,
        parse_mode="HTML",
        reply_to_message_id=message_id
    )

    # Xóa tin nhắn lệnh
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass

#===================================#
languages = [
    ["Tiếng Việt", "VN", "https://t.me/setlanguage/abcxyz"],
    ["Tiếng Việt Beta", "VN", "https://t.me/setlanguage/vi-beta"],
    ["English", "GB", "https://t.me/setlanguage/en"],
    ["Français", "FR", "https://t.me/setlanguage/fr"],
    ["Español", "ES", "https://t.me/setlanguage/es"],
    ["Deutsch", "DE", "https://t.me/setlanguage/de"],
    ["Русский", "RU", "https://t.me/setlanguage/ru"],
    ["中文", "CN", "https://t.me/setlanguage/zh-hans"],
    ["日本語", "JP", "https://t.me/setlanguage/ja"],
]

# Hàm lấy emoji cờ quốc gia từ mã quốc gia
def get_flag(code):
    if code and len(code) == 2:
        return chr(0x1F1E6 + ord(code[0].upper()) - ord('A')) + chr(0x1F1E6 + ord(code[1].upper()) - ord('A'))
    return "🏳"

@bot.message_handler(commands=['tv'])
def handle_tv(message):
    chat_id = message.chat.id
    message_id = message.message_id
    if not is_allowed_group(chat_id):
        bot.reply_to(message, "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.")
        return

    # Tạo inline keyboard chọn ngôn ngữ
    markup = InlineKeyboardMarkup()
    for name, code, url in languages:
        flag = get_flag(code)
        btn = InlineKeyboardButton(text=f"{name} {flag}", url=url)
        markup.add(btn)

    # Gửi tin nhắn chọn ngôn ngữ
    bot.send_message(
        chat_id,
        "🌐 <b>Chọn ngôn ngữ:</b>",
        reply_markup=markup,
        parse_mode="HTML"
    )

    # Xóa tin nhắn lệnh gốc
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass  # Nếu không xóa được thì thôi

#===================================#
# Hàm chọn icon ngẫu nhiên
def get_reaction():
    reactions = ['✨', '⚡', '🔥', '✅', '💡', '🔍', '🤖']
    return reactions[int(time.time()) % len(reactions)]

@bot.message_handler(commands=['ask'])
def handle_ask(message):
    query = message.text[len('/ask '):].strip()
    
    if not query:
        bot.reply_to(message, "❗ *Vui lòng nhập câu hỏi sau lệnh `/ask`.*", parse_mode="Markdown")
        return

    bot.send_chat_action(message.chat.id, 'typing')
    start_time = time.time()

    try:
        url = f'https://blackbox-pro.bjcoderx.workers.dev/?q={query}'
        response = requests.get(url, timeout=20)  # Tăng timeout lên 20 giây
        data = response.json()
        elapsed = time.time() - start_time

        if data.get("status") == "success":
            result = data["data"].get("result", "").strip()

            if not result or len(result) < 3:
                result = "_Không tìm thấy câu trả lời phù hợp._"

            reply_text = (
                f"{get_reaction()} *Trả lời cho câu hỏi của bạn:*\n"
                f"——————————————\n"
                f"❓ *Câu hỏi:* `{query}`\n"
                f"💬 *Trả lời:* {result}\n"
                f"——————————————\n"
                f"_⏱ Thời gian phản hồi: {elapsed:.2f} giây_"
            )
        else:
            reply_text = "❌ *API không trả về kết quả thành công.*"

    except requests.exceptions.Timeout:
        reply_text = "⏳ *Máy chủ mất quá nhiều thời gian để phản hồi. Vui lòng thử lại sau!*"
    except Exception as e:
        reply_text = f"⚠️ *Đã xảy ra lỗi:* `{str(e)}`"

    # Trả lời người dùng
    bot.reply_to(message, reply_text, parse_mode="Markdown")

    # Xoá tin nhắn gốc của người dùng sau 2 giây
    time.sleep(0.1)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

#===================================#
def get_facebook_info(url):
    api_url = "https://offvn.x10.mx/php/convertID.php?url=" + requests.utils.quote(url)
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        return {
            'id': data.get('id'),
            'name': data.get('name')
        }
    except Exception:
        return None

@bot.message_handler(commands=['idfb'])
def handle_idfb(message):
    chat_id = message.chat.id
    message_id = message.message_id
    user = message.from_user
    current_date = get_vietnam_time()

    if not is_allowed_group(chat_id):
        bot.send_message(
            chat_id,
            "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.",
            reply_to_message_id=message_id
        )
        return

    params = message.text.split(" ", 1)
    if len(params) < 2:
        bot.send_message(
            chat_id,
            "❌ Vui lòng nhập đúng định dạng: /idfb [link hoặc id]",
            parse_mode="HTML",
            reply_to_message_id=message_id
        )
        return

    parameter = params[1].strip()
    facebook_id = parameter if parameter.isdigit() else None
    facebook_name = None

    if not facebook_id:
        if "facebook.com" not in parameter:
            bot.send_message(
                chat_id,
                "❌ Liên kết không hợp lệ.",
                parse_mode="HTML",
                reply_to_message_id=message_id
            )
            return

        fb_info = get_facebook_info(parameter)
        if not fb_info or not fb_info.get('id'):
            bot.send_message(
                chat_id,
                "❌ Không thể lấy ID từ liên kết Facebook.",
                parse_mode="HTML",
                reply_to_message_id=message_id
            )
            return
        facebook_id = fb_info.get('id')
        facebook_name = fb_info.get('name')
    else:
        facebook_name = "Không lấy được"

    avatar_url = f"https://graph.facebook.com/{facebook_id}/picture?width=1500&height=1500&access_token=2712477385668128|b429aeb53369951d411e1cae8e810640"

    caption = (
        f"<b>UID Facebook:</b> <code>{facebook_id}</code>\n"
        f"<b>Họ tên Facebook:</b> <code>{facebook_name or 'Không lấy được'}</code>\n"
        f"<b>Link Facebook:</b> https://www.facebook.com/profile.php?id={facebook_id}\n\n"
        f"<b>🗓️ Ngày lấy dữ liệu:</b> <i>{current_date} (GMT+7)</i>\n"
    )

    bot.send_photo(
        chat_id,
        avatar_url,
        caption=caption,
        parse_mode="HTML",
        reply_to_message_id=message_id
    )

    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass

#===================================#
# Hàm lấy thông tin IP
def get_ip_info(ip):
    url = f"https://ip-info.bjcoderx.workers.dev/?ip={requests.utils.quote(ip)}"
    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception:
        return None

@bot.message_handler(commands=['ip'])
def handle_ip(message):
    chat_id = message.chat.id
    message_id = message.message_id
    if not is_allowed_group(chat_id):
        bot.send_message(
            chat_id,
            "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.",
            reply_to_message_id=message_id
        )
        return

    params = message.text.split(" ", 1)
    if len(params) < 2:
        bot.send_message(
            chat_id,
            "❌ Vui lòng nhập địa chỉ IP sau lệnh /ip\nVí dụ: <code>/ip 14.191.136.129</code>.",
            parse_mode="HTML",
            reply_to_message_id=message_id
        )
        return

    ip = params[1].strip()
    data = get_ip_info(ip)

    if not data or "ip" not in data:
        bot.send_message(
            chat_id,
            "Không thể lấy thông tin. Vui lòng thử lại sau.",
            reply_to_message_id=message_id
        )
        bot.delete_message(chat_id, message_id)
        return

    # Tạo nội dung trả về
    def get_val(obj, key, default=""):
        return obj.get(key, default) if obj else default

    tz = get_val(data, 'time_zone')
    currency = get_val(data, 'currency')

    response_text = (
        f"<b>Địa chỉ IP:</b> {get_val(data, 'ip')}\n"
        f"<b>Châu lục:</b> {get_val(data, 'continent_name')} ({get_val(data, 'continent_code')})\n"
        f"<b>Quốc gia:</b> {get_val(data, 'country_name')} ({get_val(data, 'country_code2')})\n"
        f"<b>Thành phố:</b> {get_val(data, 'city')}\n"
        f"<b>Bang/Tỉnh:</b> {get_val(data, 'state_prov')}\n"
        f"<b>Quận/Huyện:</b> {get_val(data, 'district')}\n"
        f"<b>Vĩ độ:</b> {get_val(data, 'latitude')}\n"
        f"<b>Kinh độ:</b> {get_val(data, 'longitude')}\n"
        f"<b>Múi giờ:</b> {get_val(tz, 'name')} (Offset: {get_val(tz, 'offset')})\n"
        f"<b>Tiền tệ:</b> {get_val(currency, 'name')} ({get_val(currency, 'symbol')})\n"
        f"<b>Cung cấp dịch vụ internet (ISP):</b> {get_val(data, 'isp')}\n"
        f"<b>Tổ chức:</b> {get_val(data, 'organization')}\n"
        f"<b>Flag quốc gia:</b> {get_val(data, 'country_flag')}\n"
        f"<b>Biểu tượng quốc gia:</b> {get_val(data, 'country_emoji')}\n"
        f"<b>Geo Name ID:</b> {get_val(data, 'geoname_id')}\n"
        f"<b>Ngôn ngữ:</b> {get_val(data, 'languages')}\n"
        f"<b>Thủ đô:</b> {get_val(data, 'country_capital')}\n"
        f"<b>Mã bưu chính:</b> {get_val(data, 'zipcode')}\n"
        f"<b>Mã gọi quốc gia:</b> {get_val(data, 'calling_code')}\n"
        f"<b>Tên quốc gia chính thức:</b> {get_val(data, 'country_name_official')}\n"
        f"<b>Thời gian hiện tại (theo múi giờ của IP):</b> {get_val(tz, 'current_time')}\n"
    )

    bot.send_message(
        chat_id,
        response_text,
        parse_mode="HTML",
        reply_to_message_id=message_id
    )
    bot.delete_message(chat_id, message_id)

#===================================#
@bot.message_handler(commands=['qrcode'])
def handle_qrcode(message):
    chat_id = message.chat.id
    message_id = message.message_id
    user_id = message.from_user.id
    current_date = get_vietnam_time()

    if not is_allowed_group(chat_id):
        bot.send_message(
            chat_id,
            "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.",
            reply_to_message_id=message_id
        )
        return

    params = message.text.split(" ", 1)
    if len(params) < 2:
        bot.send_message(
            chat_id,
            "⚠️ Vui lòng sử dụng lệnh /qrcode {nội dung}\nVí dụ: /qrcode Hello.",
            reply_to_message_id=message_id
        )
        bot.delete_message(chat_id, message_id)
        return

    noidung = urllib.parse.quote(params[1])
    qr_code_url = f"https://offvn.x10.mx/php/qr.php?text={noidung}"

    caption = (
        f"<b>Nội dung QR Code:</b> <code>{params[1]}</code>\n"
        f"<b>Thông tin bổ sung:</b>\n"
        f"<i>ID Người Dùng:</i> <code>{user_id}</code>\n"
        f"<i>Message ID:</i> <code>{message_id}</code>\n"
        f"<b>Thời gian tạo:</b> <i>{current_date}</i>\n"
    )

    bot.send_photo(
        chat_id,
        qr_code_url,
        caption=caption,
        parse_mode="HTML",
        reply_to_message_id=message_id
    )
    bot.delete_message(chat_id, message_id)

#===================================#
# Hàm lấy dữ liệu vi phạm
def get_violation_data(bsx, loaixe):
    url = f"https://vietcheckcar.com/api/api.php?api_key=sfund&bsx={requests.utils.quote(bsx)}&bypass_cache=0&loaixe={loaixe}&vip=0"
    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception:
        return None

# Hàm định dạng thông tin vi phạm
def format_violation_info(data, vehicle_type):
    if data and data.get('code') == 1:
        biensoxe = data.get('biensoxe', "N/A")
        total = data.get('totalViolations', 0)
        violation = data.get('violations', [{}])[0] if data.get('violations') else None

        if violation:
            image_url = violation.get('image_url', None)
            text = (
                f"<b>{vehicle_type.upper()} - {biensoxe}</b>\n"
                f"• Tổng vi phạm: {total}\n"
                f"• Trạng thái: {violation.get('trang_thai', 'N/A')}\n"
                f"• Thời gian: {violation.get('thoi_gian_vi_pham', 'N/A')}\n"
                f"• Địa điểm: {violation.get('dia_diem_vi_pham', 'N/A')}\n"
                f"• Hành vi: {violation.get('hanh_vi_vi_pham', 'N/A')}\n"
                f"• Mức phạt: {violation.get('muc_phat', 'N/A')}\n\n"
            )
            return text, image_url
        else:
            return f"<b>{vehicle_type.upper()}:</b> Không có vi phạm.\n\n", None
    return "", None

@bot.message_handler(commands=['vipham'])
def handle_vipham(message):
    chat_id = message.chat.id
    message_id = message.message_id
    if not is_allowed_group(chat_id):
        bot.send_message(
            chat_id,
            "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.",
            reply_to_message_id=message_id
        )
        return

    params = message.text.strip().split()
    if len(params) < 2:
        bot.send_message(
            chat_id,
            "Vui lòng nhập biển số. Ví dụ: /vipham 98B304452",
            reply_to_message_id=message_id
        )
        bot.delete_message(chat_id, message_id)
        return

    bsx = params[1].strip()
    text_xemay, img_xemay = format_violation_info(get_violation_data(bsx, 2), "xe máy")
    text_oto, img_oto = format_violation_info(get_violation_data(bsx, 1), "ô tô")

    message_text = text_xemay + text_oto
    if not message_text.strip():
        message_text = "Không tìm thấy dữ liệu."

    bot.send_message(
        chat_id,
        message_text,
        parse_mode="HTML",
        reply_to_message_id=message_id
    )

    if img_xemay:
        bot.send_photo(chat_id, img_xemay, caption="Ảnh vi phạm xe máy")
    if img_oto:
        bot.send_photo(chat_id, img_oto, caption="Ảnh vi phạm ô tô")

#===================================#
@bot.message_handler(commands=['kqxs'])
def handle_kqxs(message):
    chat_id = message.chat.id
    message_id = message.message_id
    if not is_allowed_group(chat_id):
        bot.send_message(
            chat_id,
            "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.",
            reply_to_message_id=message_id
        )
        return

    api_url = "https://nguyenmanh.name.vn/api/xsmb?apikey=OUEaxPOl"
    try:
        response = requests.get(api_url, timeout=5)
        data = response.json()
        if data and data.get("status") == 200:
            result = data.get("result", "Không có dữ liệu.")
            bot.send_message(
                chat_id,
                f"<b>{result}</b>",
                parse_mode="HTML",
                reply_to_message_id=message_id
            )
            bot.delete_message(chat_id, message_id)
        else:
            bot.send_message(
                chat_id,
                "Lỗi khi lấy kết quả xổ số.",
                reply_to_message_id=message_id
            )
    except Exception as e:
        bot.send_message(
            chat_id,
            "Lỗi khi kết nối tới API hoặc xử lý dữ liệu.",
            reply_to_message_id=message_id
        )

#===================================#
@bot.message_handler(commands=['2fa'])
def handle_2fa(message):
    chat_id = message.chat.id
    message_id = message.message_id

    if not is_allowed_group(chat_id):
        bot.send_message(
            chat_id,
            "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.",
            reply_to_message_id=message_id
        )
        return

    params = message.text.strip().split()
    if len(params) == 1:
        msg = bot.send_message(
            chat_id,
            "⚠️ <b>Dùng mã sau lệnh /2fa</b>\nVí dụ: <code>/2fa 242RIHRGMWYHZ76GDDEZSP3XKK5TUJSQ</code>",
            reply_to_message_id=message_id,
            parse_mode="HTML"
        )
        threading.Timer(15, lambda: safe_delete(chat_id, msg.message_id)).start()
        return

    ma2fa = params[1].strip().upper()

    try:
        response = requests.get(f"https://2fa.live/tok/{ma2fa}", timeout=5)
        res = response.json()
        code = res.get("token")
        if not code or not code.isdigit() or len(code) != 6:
            code = "Không hợp lệ"
            ok = False
        else:
            ok = True
    except Exception:
        code = "Không hợp lệ"
        ok = False

    current_date = get_vietnam_time()
    video = "https://offvn.io.vn/bot.gif"

    caption = (
        f"<b>{current_date}\n─────────────\n🔑 Mã 2FA là:</b> <code>{code}</code>"
        + ("\n\n✅ <i>Mã hợp lệ!</i>" if ok else "\n\n❌ <i>Mã 2FA không hợp lệ, vui lòng kiểm tra lại.</i>")
    )

    bot.send_video(
        chat_id,
        video,
        caption=caption,
        reply_to_message_id=message_id,
        supports_streaming=True,
        parse_mode="HTML"
    )

    threading.Timer(10, lambda: safe_delete(chat_id, message_id)).start()

def safe_delete(chat_id, msg_id):
    try:
        bot.delete_message(chat_id, msg_id)
    except Exception:
        pass

#===================================#
def get_qr_url(bank, stk):
    return f"https://img.vietqr.io/image/{bank}-{stk}-compact.png"
@bot.message_handler(commands=['qrbank'])
def handle_qrbank(message):
    chat_id = message.chat.id
    message_id = message.message_id
    text = message.text

    if not is_allowed_group(chat_id):
        bot.send_message(chat_id, "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.")
        return

    args = text.split()
    if len(args) < 3:
        bot.send_message(
            chat_id,
            "⚠️ Vui lòng sử dụng lệnh đúng định dạng: /qrbank {STK} {Ngân hàng}\n💬 Ví dụ: /qrbank 444888365 MBbank."
        )
        return

    stk = args[1]
    bank = args[2]
    qr_url = get_qr_url(bank, stk)

    # Kiểm tra xem ảnh QR có tồn tại không
    try:
        resp = requests.head(qr_url, timeout=10)
        if resp.status_code != 200:
            bot.send_message(
                chat_id,
                "⚠️ Không thể tạo mã QR, có thể bạn đã nhập sai số tài khoản hoặc ngân hàng."
            )
            return
    except Exception:
        bot.send_message(
            chat_id,
            "⚠️ Không thể kiểm tra mã QR, vui lòng thử lại sau."
        )
        return

    # Lấy ngày giờ hiện tại
    current_date = get_vietnam_time()

    # Nội dung chú thích gửi kèm
    bank_info = f"STK: <code>{stk}</code>\nNgân hàng: {bank}\n\n"
    bank_info += f"📅 Ngày tạo QR: {current_date}"
    caption = f"<b>Thông tin tài khoản:</b>\n{bank_info}"

    bot.send_photo(
        chat_id=chat_id,
        photo=qr_url,
        caption=caption,
        parse_mode='HTML'
    )

    # Xóa lệnh sau khi thành công
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        # Nếu không xóa được cũng không sao, có thể log lỗi nếu muốn
        print(f"Lỗi khi xóa tin nhắn: {e}")

#===================================#
@bot.message_handler(commands=['github'])
def handle_github(message):
    chat_id = message.chat.id
    message_id = message.message_id
    text = message.text

    # Kiểm tra quyền nhóm
    if not is_allowed_group(chat_id):
        bot.send_message(chat_id, "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.")
        return

    # Lấy username
    username = text.replace('/github', '').strip()
    if not username:
        bot.send_message(chat_id, "❌ Vui lòng cung cấp tên người dùng GitHub sau lệnh /github.")
        return

    url = f"https://api.github.com/users/{username}"
    headers = {'User-Agent': 'request'}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()

            info = (
                f"🔍 <b>Thông tin GitHub của <a href=\"{data.get('html_url', '')}\">{username}</a></b>\n\n"
                f"👤 <b>Tên đăng nhập:</b> {data.get('login', 'Không có')}\n"
                f"🆔 <b>ID:</b> {data.get('id', 'Không rõ')}\n"
                f"📝 <b>Tên đầy đủ:</b> {data.get('name', 'Không có tên')}\n"
                f"🔗 <b>URL hồ sơ:</b> <a href=\"{data.get('html_url', '')}\">{data.get('html_url', '')}</a>\n"
                f"🏢 <b>Công ty:</b> {data.get('company', 'Không có thông tin')}\n"
                f"📍 <b>Vị trí:</b> {data.get('location', 'Không có thông tin')}\n"
                f"📧 <b>Email:</b> {data.get('email', 'Không công khai')}\n"
                f"💼 <b>Hireable:</b> {'Có thể thuê' if data.get('hireable') else 'Không thể thuê hoặc không công khai'}\n"
                f"💬 <b>Bio:</b> {data.get('bio', 'Không có thông tin')}\n"
                f"🌐 <b>Blog:</b> {data.get('blog', 'Không có URL blog')}\n"
                f"🐦 <b>Twitter:</b> {data.get('twitter_username', 'Không có Twitter')}\n"
                f"🕒 <b>Ngày tạo tài khoản:</b> {data.get('created_at', 'Không rõ')}\n"
                f"🕒 <b>Ngày cập nhật:</b> {data.get('updated_at', 'Không rõ')}\n"
                f"📂 <b>Repositories công khai:</b> {data.get('public_repos', 0)}\n"
                f"📂 <b>Gists công khai:</b> {data.get('public_gists', 0)}\n"
                f"🔒 <b>Repositories riêng tư:</b> {data.get('total_private_repos', 'Không rõ')}\n"
                f"⭐ <b>Số follower:</b> {data.get('followers', 0)} | <b>Đang follow:</b> {data.get('following', 0)}\n"
                f"🏷️ <b>Loại tài khoản:</b> {data.get('type', 'Không rõ')}\n"
                f"🔗 <b>Site admin:</b> {'✅' if data.get('site_admin') else '❌'}\n"
                f"🔗 <b>API endpoint:</b> {data.get('url', '')}\n"
                f"🛡️ <b>Avatar ID:</b> {data.get('node_id', '')}\n"
            )

            avatar_url = data.get('avatar_url', None)
            try:
                bot.delete_message(chat_id, message_id)
            except Exception:
                pass

            # ĐÃ SỬA LẠI CHỈ GIỮ THAM SỐ HỢP LỆ
            if avatar_url:
                sent = bot.send_photo(chat_id, avatar_url, caption=info, parse_mode='HTML')
            else:
                sent = bot.send_message(chat_id, info, parse_mode='HTML', disable_web_page_preview=True)

        elif resp.status_code == 404:
            bot.send_message(chat_id, "❌ Không tìm thấy người dùng GitHub này.")
        elif resp.status_code == 403:
            bot.send_message(chat_id, "❌ Đã vượt giới hạn truy vấn API GitHub. Vui lòng thử lại sau.")
        else:
            bot.send_message(chat_id, f"❌ Lỗi không xác định từ GitHub (mã {resp.status_code}).")
    except requests.exceptions.Timeout:
        bot.send_message(chat_id, "❌ Quá thời gian chờ phản hồi từ GitHub.")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Đã xảy ra lỗi khi lấy thông tin từ GitHub: {e}")

#===================================#
BANK_LIST = [
    "mbbank", "dongabank", "viettinbank", "vietcombank", "techcombank",
    "bidv", "acb", "sacombank", "vpbank", "agribank",
    "hdbank", "tpbank", "shb", "eximbank", "ocb",
    "seabank", "bacabank", "pvcombank", "scb", "vib",
    "namabank", "abbank", "lpbank", "vietabank", "msb",
    "nvbank", "pgbank", "publicbank", "cimbbank", "uob"
]

def qrlink(so_tai_khoan, ten_ngan_hang, so_tien, noi_dung, download):
    return f"{QRND_API_URL}?acc={so_tai_khoan}&bank={ten_ngan_hang}&amount={so_tien}&des={noi_dung}&template=compact&download={download}"

def download_qr_image(url, noi_dung, chat_id):
    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code == 200:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp.write(resp.content)
                tmp_path = tmp.name
            with open(tmp_path, "rb") as qr_img:
                bot.send_photo(chat_id, qr_img, caption=noi_dung)
            os.remove(tmp_path)
        else:
            bot.send_message(chat_id, "❌ Không thể tải QR code. Vui lòng kiểm tra lại!")
    except Exception:
        bot.send_message(chat_id, "❌ Không thể tải QR code. Vui lòng kiểm tra lại!")

@bot.message_handler(commands=['qrnd'])
def handle_qrnd(message):
    chat_id = message.chat.id
    message_id = message.message_id
    text = message.text

    if not is_allowed_group(chat_id):
        bot.send_message(chat_id, "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.")
        return

    parts = text.split(' ', 4)
    if len(parts) < 4:
        bot.send_message(chat_id, "Cú pháp: /qrnd [Số tài khoản] [Mã ngân hàng] [Số tiền] [Nội dung]")
        return

    so_tai_khoan = parts[1]
    ma_ngan_hang = parts[2].lower()
    so_tien_str = parts[3]
    noi_dung = parts[4] if len(parts) > 4 else ""

    # Kiểm tra hợp lệ mã ngân hàng
    if ma_ngan_hang not in BANK_LIST:
        bot.send_message(chat_id, "❌ Mã ngân hàng không hợp lệ!")
        return

    # Kiểm tra hợp lệ số tiền
    if not so_tien_str.isdigit():
        bot.send_message(chat_id, "❌ Số tiền phải là số nguyên dương (hoặc 0).")
        return
    so_tien = int(so_tien_str)

    # Tạo link QR code
    link = qrlink(so_tai_khoan, ma_ngan_hang, so_tien, noi_dung, 'true')

    # Nội dung gửi kèm ảnh
    noi_dung_thong_tin = (
        "📌 THÔNG TIN QR CODE\n"
        "──────────────\n"
        f"🏦 Ngân Hàng: {ma_ngan_hang.upper()}\n"
        f"💳 Số TK: {so_tai_khoan}\n"
        f"💵 Số Tiền: {so_tien:,} VNĐ\n"
        f"📝 Nội Dung: {noi_dung}\n"
        "──────────────"
    )

    # Gửi ảnh QR
    download_qr_image(link, noi_dung_thong_tin, chat_id)

#===================================#
@bot.message_handler(commands=['scr'])
def handle_scr(message):
    chat_id = message.chat.id
    message_id = message.message_id
    help_text = """
<b>
📂 SOURCE BOT REG FACEBOOK
https://link4m.com/XWlBAW
📂 SOURCE BOT SEARCH YOUTUBE
https://link4m.com/0K0xYj
📂 SOURCE BOT TẢI NHẠC TỪ SPOTIFY
https://link4m.com/0cCHE
📂 SOURCE BOT QR CODE VĂN BẢN ĐẸP
https://link4m.com/MjNtHCk
📂 SOURCE BOT CHECK INFO GITHUB
https://link4m.com/vdTqHXr
📂 SOURCE BOT CHECK INFO TIKTOK
https://link4m.com/CayF3
📂 SOURCE BOT VOICE CHUYỂN VĂN BẢN SANG GIỌNG NÓI
https://link4m.com/ZR8IUSK
📂 SOURCE BOT VIDEO SEX 🆕
https://link4m.com/DadlL
📂 SOURCE BOT TẢI VIDEO TIKTOK 🆕
https://link4m.com/VJQSxEB
📂 SOURCE BOT RANDOM VIDEO TIKTOK 🆕
https://link4m.com/aec3F
📂 SOURCE BOT CHECK THÔNG TIN TELEGRAM 🆕
https://link4m.com/cufRuMeY
SOURCE BOT CHUYỂN NGÔN NGỮ TIẾNG VIỆT 🇻🇳
https://link4m.com/VCpb9FL
📂 SOURCE BOT XEM THỜI GIAN HOẠT ĐỘNG BOT ⏰
https://link4m.com/sMIj4iP
SOURCE BOT KIỂM TRA THÔNG TIN QUỐC GIA 🌍
https://link4m.com/P5RTXt0S
📂 SOURCE BOT GOOGLE DỊCH 🌐
https://link4m.com/WmYVYx0i
📂 SOURCE BOT XEM THỜI TIẾT 🌦️
https://link4m.com/AS5lW
📂 SOURCE BOT XEM KẾT QUẢ XỔ SỐ
https://link4m.com/eiCAF
📂 SOURCE BOT TRẢ LỜI GPT-4o AI Bot 🧠
https://link4m.com/6SX6T
</b>
"""

    # Gửi nội dung help_text và lưu lại message_id của tin nhắn bot gửi ra
    sent_msg = bot.send_message(
        chat_id,
        help_text,
        parse_mode='HTML'
    )

    # Xóa tin nhắn gốc của người dùng
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass

    # Hàm xóa tin nhắn sau 10 giây
    def delete_sent():
        time.sleep(20)
        try:
            bot.delete_message(chat_id, sent_msg.message_id)
        except Exception:
            pass

    # Chạy xóa sau 10 giây trong thread riêng (không block bot)
    threading.Thread(target=delete_sent).start()

#===================================#
LANG_FLAG_MAP = {
    'vi': ('Việt Nam', '🇻🇳'),
    'en': ('English', '🇬🇧'),
    'ru': ('Nga', '🇷🇺'),
    'ja': ('Nhật Bản', '🇯🇵'),
    'ko': ('Hàn Quốc', '🇰🇷'),
    'zh': ('Trung Quốc', '🇨🇳'),
    'fr': ('Pháp', '🇫🇷'),
    'de': ('Đức', '🇩🇪'),
    'es': ('Tây Ban Nha', '🇪🇸'),
    'it': ('Ý', '🇮🇹'),
    'tr': ('Thổ Nhĩ Kỳ', '🇹🇷'),
    'th': ('Thái Lan', '🇹🇭'),
    'id': ('Indonesia', '🇮🇩'),
    # Thêm nếu muốn...
}

@bot.message_handler(commands=['thongtin'])
def handle_check(message):
    chat_id = message.chat.id
    message_id = message.message_id

    if not is_allowed_group(chat_id):
        send_message(chat_id, "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.", message_id)
        return

    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user

    user_info = {
        'ID': user.id,
        'Tên': f"{user.first_name or ''} {user.last_name or ''}".strip(),
        'Username': f"@{user.username}" if user.username else "Không có",
    }

    lang_code = getattr(user, 'language_code', 'Không xác định')
    country, flag = LANG_FLAG_MAP.get(lang_code, ('Không xác định', '🏳️'))
    user_info['Ngôn ngữ'] = f"{country} {flag} <i>({lang_code})</i>"

    try:
        bio = bot.get_chat(user.id).bio or "Không có"
    except Exception:
        bio = "Không có"

    try:
        member = bot.get_chat_member(chat_id, user.id)
        status = member.status
    except Exception:
        status = "Không xác định"

    status_dict = {
        "creator": "Quản trị viên (Admin chính)",
        "administrator": "Quản trị viên",
        "member": "Thành viên",
        "restricted": "Bị hạn chế",
        "left": "Rời nhóm",
        "kicked": "Bị đuổi"
    }

    user_info['Quyền trong nhóm'] = status_dict.get(status, "Không xác định")
    user_info['Trạng thái'] = status_dict.get(status, "Không xác định")
    user_info['Bio'] = bio
    user_info['Premium'] = "⭐ <b>Tài khoản Premium</b>" if getattr(user, 'is_premium', False) else "Không"

    user_photos = bot.get_user_profile_photos(user.id)
    avatar_count = user_photos.total_count
    has_avatar = avatar_count > 0
    avatar_text = "Đã có avatar" if has_avatar else "Chưa có avatar"
    user_info['Số đại diện'] = str(avatar_count)

    profile_url = f"https://t.me/{user.username}" if user.username else f"https://t.me/user?id={user.id}"

    caption = (
        f"🌟 <b>Thông Tin {'Của Bạn' if user.id == message.from_user.id else 'Người Dùng'}</b>\n"
        "<blockquote>"
        f"┌ <b>ID:</b> <code>{user_info['ID']}</code>\n"
        f"├ <b>Tên:</b> {user_info['Tên']}\n"
        f"├ <b>Username:</b> {user_info['Username']}\n"
        f"├ <b>Link profile:</b> <a href=\"{profile_url}\">{profile_url}</a>\n"
        f"├ <b>Ngôn ngữ:</b> {user_info['Ngôn ngữ']}\n"
        f"├ <b>Quyền trong nhóm:</b> {user_info['Quyền trong nhóm']}\n"
        f"├ <b>Bio:</b> {user_info['Bio']}\n"
        f"├ <b>Premium:</b> {user_info['Premium']}\n"
        f"├ <b>Số đại diện:</b> {user_info['Số đại diện']}\n"
        f"└ <b>Avatar:</b> {avatar_text}\n"
        "</blockquote>"
    )

    if has_avatar:
        avatar_file_id = user_photos.photos[0][-1].file_id
        bot.send_photo(chat_id, avatar_file_id, caption=caption, parse_mode='HTML', reply_to_message_id=message_id)
    else:
        bot.send_message(chat_id, caption, parse_mode='HTML', reply_to_message_id=message_id)

    # XÓA LỆNH GỐC SAU KHI THỰC HIỆN
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass  # Tránh lỗi nếu bot không có quyền xóa
#===================================#
keyboard1 = InlineKeyboardMarkup(row_width=2)
keyboard1.add(
    InlineKeyboardButton(text="👤Admin", url='https://t.me/off_vn'),
    InlineKeyboardButton(text="🤖Bot", url='https://t.me/tiktokqb_bot')
)

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    if message.chat.type in ['group', 'supergroup']:
        # Lấy số lượng thành viên hiện tại
        try:
            member_count = bot.get_chat_members_count(message.chat.id)
        except:
            member_count = 'không xác định'

        for member in message.new_chat_members:
            chat_id = message.chat.id
            chat_title = message.chat.title
            id = member.id
            first_name = member.first_name or ''
            last_name = member.last_name or ''
            full_name = f"{first_name} {last_name}".strip()
            try:
                text = (
                    f'Xin chào 👋 <a href="tg://user?id={id}">{full_name}</a>!\n'
                    f'<blockquote>Chào mừng bạn đã tham gia nhóm {chat_title}\n'
                    f'Số thành viên hiện tại: <b>{member_count}</b>.\n'
                    f'Sử dụng lệnh /start để xem chi tiết.</blockquote>'
                )
                bot.send_video(
                    chat_id, 
                    'https://offvn.io.vn/welcome.mp4', 
                    caption=text, 
                    parse_mode='HTML', 
                    reply_markup=keyboard1
                )
            except Exception as e:
                print(f"Lỗi gửi tin nhắn chào mừng: {e}")

#===================================#
def country_flag(locale):
    if locale and "_" in locale:
        country_code = locale.split('_')[1]
        return ''.join([chr(127397 + ord(c.upper())) for c in country_code])
    return ''

def relationship_status_text(status):
    mapping = {
        "Single": "💔 Độc thân",
        "In a relationship": "💑 Đang hẹn hò",
        "Engaged": "💍 Đã đính hôn",
        "Married": "💒 Đã kết hôn",
        "It's complicated": "🤔 Phức tạp",
        "Separated": "💔 Đã ly thân",
        "Divorced": "💔 Đã ly hôn",
        "Widowed": "🖤 Đã góa",
        "In an open relationship": "🔗 Mối quan hệ mở",
        "In a civil union": "👬 Liên minh dân sự",
        "In a domestic partnership": "🏠 Đối tác chung sống",
        "Không công khai": "❓ Không công khai",
        "Chưa thiết lập": "❓ Không công khai",
        "": "❓ Không công khai"
    }
    return mapping.get(status, status if status else "❓ Không công khai")


@bot.message_handler(commands=['fb'])
def send_facebook_info(message):
    chat_id = message.chat.id
    message_id = message.message_id
    if not is_allowed_group(chat_id):
        bot.send_message(
            chat_id,
            "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.",
            reply_to_message_id=message_id
        )
        return

    waiting = bot.reply_to(message, "🔍")
    user_input = message.text.split(maxsplit=1)
    if len(user_input) < 2:
        bot.send_message(chat_id, "❌ Vui lòng nhập UID hoặc Link sau lệnh /fb\n\n💬 Ví Dụ: <code>/fb 61574395204757</code> hoặc <code>/fb https://facebook.com/zuck</code>")
        bot.delete_message(chat_id, waiting.message_id)
        return

    fb_input = user_input[1].strip()

    # Kiểm tra xem input là UID (toàn số) hay link
    if fb_input.isdigit():
        fb_id = fb_input
    else:
        # Nhận link Facebook, convert sang UID
        # Xử lý link cho an toàn
        fb_link = fb_input
        # Xử lý link có thể thiếu http
        if not fb_link.startswith("http"):
            fb_link = "https://" + fb_link

        convert_api = f"https://offvn.x10.mx/php/convertID.php?url={fb_link}"
        try:
            convert_res = requests.get(convert_api)
            if convert_res.status_code == 200:
                convert_data = convert_res.json()
                fb_id = str(convert_data.get("id", ""))
                if not fb_id.isdigit():
                    bot.send_message(chat_id, "❌ Không thể lấy UID từ link Facebook này! Vui lòng kiểm tra lại.")
                    bot.delete_message(chat_id, waiting.message_id)
                    return
            else:
                bot.send_message(chat_id, "❌ Lỗi khi kết nối API lấy UID.")
                bot.delete_message(chat_id, waiting.message_id)
                return
        except Exception as e:
            bot.send_message(chat_id, f"❌ Lỗi khi lấy UID từ link: {e}")
            bot.delete_message(chat_id, waiting.message_id)
            return

    # Tới đây fb_id chắc chắn là UID
    api_url = f"https://offvn.x10.mx/php/apiCheck.php?id={fb_id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        try:
            data = response.json().get("result", {})

            if not isinstance(data, dict):
                bot.send_message(chat_id, "❌ Vui lòng kiểm tra lại, Có Thể Bạn Đã Nhập Sai Định Dạng")
                return

            # ... (Phần xử lý data bên dưới giữ nguyên như bạn đã làm) ...
            # Copy nguyên phần xử lý data của bạn ở trên (từ: name = data.get("name", ...) cho đến cuối)
            # Chỉ sửa lại biến message.chat.id => chat_id cho đồng bộ

            # -- CODE XỬ LÝ DATA Ở ĐÂY (NHƯ CỦA BẠN) --
            name = data.get("name", "Không công khai")
            username = data.get("username", "Chưa thiết lập")
            profile_id = data.get("id", "Chưa thiết lập")
            link = data.get("link", "https://www.facebook.com/")
            is_verified = data.get("is_verified", False)
            picture = data.get("picture", {}).get("data", {}).get("url", "")
            created_time = data.get("created_time", "Không công khai")
            about = data.get("about", "Không công khai")
            locale = data.get("locale", "Không công khai")
            gender = data.get("gender", "Không công khai").capitalize()
            hometown = data.get("hometown", {}).get("name", "Không công khai")
            location = data.get("location", {}).get("name", "Không công khai")
            updated_time = data.get("updated_time", "Không công khai")
            timezone = data.get("timezone", "Không công khai")
            work = data.get("work", [])
            cover_photo = data.get("cover", {}).get("source", "")
            followers = data.get("followers", "Không công khai")
            following = data.get("following", "Không rõ số lượng đang theo dõi")
            relationship = data.get("relationship_status","Không công khai")
            significant_other = data.get("significant_other", {})
            significant_other_name = significant_other.get("name", "Không công khai")
            significant_other_id = significant_other.get("id", "Không công khai")

            flag = country_flag(locale)

            work_info = ""
            if work:
                for job in work:
                    position = job.get("position", {}).get("name", "")
                    employer = job.get("employer", {}).get("name", "")
                    work_info += f"\n│ -> Làm việc tại {position} <a href='https://facebook.com/{username}'>{employer}</a>"
            else:
                work_info = "Không công khai"

            education_info = ""
            education = data.get("education", [])
            if education:
                for edu in education:
                    school = edu.get("school", {}).get("name", "Không công khai")
                    education_info += f"\n│ -> Học {edu.get('concentration', [{'name': ''}])[0]['name']} tại <a href='https://facebook.com/{username}'>{school}</a>"
            else:
                education_info = "Không công khai"

            verification_status = "Đã Xác Minh ✅" if is_verified else "Chưa xác minh ❌"
            picture_status = "Có ảnh đại diện 👤" if not data.get("picture", {}).get("data", {}).get("is_silhouette", True) else "Không có ảnh đại diện ❌"

            relationship_icon_text = relationship_status_text(relationship)

            significant_other_line = ""
            if significant_other_id not in ["Không công khai", "Chưa thiết lập", None, ""]:
                significant_other_line = (
                    f"│ -> 💍 Đã kết hôn với: <a href='https://facebook.com/{significant_other_id}'>{significant_other_name}</a>\n"
                    f"│ -> 🔗 Link UID: <code>https://facebook.com/{significant_other_id}</code>"
                )

            if cover_photo:
                cover_photo_line = f"│ 𝗖𝗼𝘃𝗲𝗿 𝗣𝗵𝗼𝘁𝗼: <a href='{cover_photo}'>🖼️ Xem ảnh bìa</a>"
            else:
                cover_photo_line = "│ 𝗖𝗼𝘃𝗲𝗿 𝗣𝗵𝗼𝘁𝗼: Không có ảnh bìa ❌"

            fb_info = f"""
<blockquote>╭─────────────⭓
│ 𝗡𝗮𝗺𝗲: <a href='{picture}'>{name}</a>
│ 𝗨𝗜𝗗: <a href='https://facebook.com/{profile_id}'>{profile_id}</a>
│ 𝗨𝘀𝗲𝗿 𝗡𝗮𝗺𝗲: <a href='https://facebook.com/{username}'>{username}</a>
{cover_photo_line}
│ -> {picture_status}
│ 𝗟𝗶𝗻𝗸: {link}
│ 𝗕𝗶𝗿𝘁𝗵𝗱𝗮𝘆: {data.get("birthday", "Không hiển thị ngày sinh")}
│ 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀: <a href='https://facebook.com/{profile_id}'>{followers}</a> Người theo dõi
│ 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴: {following}
│ 𝗗𝗮𝘁𝗲 𝗖𝗿𝗲𝗮𝘁𝗲𝗱: {created_time}
│ 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝘁𝗶𝗼𝗻: {verification_status}
│ 𝗦𝘁𝗮𝘁𝘂𝘀: {relationship_icon_text}
{significant_other_line}
│ 𝗕𝗶𝗼: {about}
│ 𝗚𝗲𝗻𝗱𝗲𝗿: {gender}
│ 𝗛𝗼𝗺𝗲𝘁𝗼𝘄𝗻: {hometown}
│ 𝗟𝗼𝗰𝗮𝘁𝗶𝗼𝗻: {location}
│ 𝗪𝗼𝗿𝗸: {work_info}
│ 𝗘𝗱𝘂𝗰𝗮𝘁𝗶𝗼𝗻: {education_info}
│ 𝗔𝗯𝗼𝘂𝘁𝘀: {data.get("quotes", "Không có trích dẫn")}
├─────────────⭔
│ 𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲: {locale} {flag}
│ 𝗧𝗶𝗺𝗲 𝗨𝗽𝗱𝗮𝘁𝗲: {updated_time}
╰─────────────⭓
</blockquote>
            """
            bot.send_message(chat_id, fb_info, parse_mode='HTML')
            bot.delete_message(chat_id, waiting.message_id)
        except Exception as e:
            bot.send_message(chat_id, f"Đã xảy ra lỗi khi xử lý dữ liệu: {str(e)}")
            bot.delete_message(chat_id, waiting.message_id)
    else:
        bot.send_message(chat_id, "❌ Vui lòng kiểm tra lại, Có Thể Bạn Đã Nhập Sai Định Dạng")
        bot.delete_message(chat_id, waiting.message_id)
    # XÓA TIN NHẮN CHỨA LỆNH SAU KHI BOT TRẢ LỜI
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Lỗi xóa lệnh: {e}")

#===================================#
def get_tiktok_info(username):
    url = f"https://offvn.x10.mx/php/tt.php?input={username}&key=offvnx"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data.get("success") or "userInfo" not in data["data"]:
            return "Không tìm thấy thông tin TikTok.", None

        user_info = data['data']['userInfo']['user']
        stats = data['data']['userInfo']['stats']

        # Lấy thêm các trường thông tin mới
        short_id = user_info.get('shortId', 'Không có')
        open_favorite = "Công khai" if user_info.get('openFavorite') else "Riêng tư"
        comment_setting = user_info.get('commentSetting', 0)
        duet_setting = user_info.get('duetSetting', 0)
        stitch_setting = user_info.get('stitchSetting', 0)
        download_setting = user_info.get('downloadSetting', 0)
        is_ad_virtual = "Có" if user_info.get('isADVirtual') else "Không"
        tt_seller = "Có" if user_info.get('ttSeller') else "Không"
        is_organization = "Tổ chức" if user_info.get('isOrganization') else "Cá nhân"
        profile_embed_permission = "Cho phép" if user_info.get('profileEmbedPermission') else "Không cho phép"
        can_exp_playlist = "Có" if user_info.get('canExpPlaylist') else "Không"

        # Giải thích quyền riêng tư
        def explain_privacy(val):
            return {
                0: "Mọi người",
                1: "Bạn bè",
                2: "Chỉ mình tôi",
                3: "Cấm tải"
            }.get(val, str(val))

        avatar_url = user_info.get("avatarLarger") or user_info.get("avatarMedium") or user_info.get("avatarThumb")
        create_time = user_info.get('createTime', 'Không rõ')
        nick_update_time = user_info.get('nickNameModifyTime', 'Không rõ')
        region_flag = user_info.get('region_flag', user_info.get('region', 'Không rõ'))
        language = user_info.get('language', 'Không rõ')

        music_tab = "Có" if user_info.get('profileTab', {}).get('showMusicTab') else "Không"
        question_tab = "Có" if user_info.get('profileTab', {}).get('showQuestionTab') else "Không"
        has_playlist = "Có" if user_info.get('profileTab', {}).get('showPlayListTab') else "Không"
        commerce_type = "Thương mại/Shop 🛒" if user_info.get("commerceUserInfo", {}).get("commerceUser") else "Cá nhân"
        is_verified = "Đã xác minh ✅" if user_info.get('verified') else "Chưa xác minh ❌"
        account_status = "Công Khai" if not user_info.get('privateAccount') else "Riêng Tư"
        following_visibility = (
            "Danh sách following đã bị ẩn" if user_info.get('followingVisibility') == 2 else "Danh sách following hiển thị"
        )

        result = f"""
<blockquote>╭─────────────⭓
│ ‎𝗡𝗮𝗺𝗲: {user_info.get('nickname', 'Không rõ')}
│ 𝗜𝗗: {user_info.get('id', 'Không rõ')} (ShortID: {short_id})
│ 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: {user_info.get('uniqueId', 'Không rõ')}
│ 𝗟𝗶𝗻𝗸: <a href="https://www.tiktok.com/@{user_info.get('uniqueId', '')}">https://www.tiktok.com/@{user_info.get('uniqueId', '')}</a>
│ 𝗟𝗶𝗸𝗲 𝗣𝘂𝗯𝗹𝗶𝗰: {open_favorite}
│ 𝗩𝗲𝗿𝗶𝗳𝗶𝗲𝗱: {is_verified}
│ 𝗦𝘁𝗮𝘁𝘂𝘀:
│ | -> <i>Tab nhạc: {music_tab}</i>
│ | -> <i>Tab hỏi đáp: {question_tab}</i>
│ | -> <i>Danh sách phát: {has_playlist}</i>
│ | -> <i>Loại tài khoản: {commerce_type}</i>
│ | -> <i>Tài khoản này đang ở chế độ {account_status}</i>
│ | -> <i>{following_visibility}</i>
│ | -> <i>Là tổ chức: {is_organization}</i>
│ | -> <i>Cho phép nhúng profile: {profile_embed_permission}</i>
│ | -> <i>Có thể tạo playlist: {can_exp_playlist}</i>
│ | -> <i>Là tài khoản quảng cáo/ảo: {is_ad_virtual}</i>
│ | -> <i>Shop TikTok Seller: {tt_seller}</i>
│ 𝗣𝗿𝗶𝘃𝗮𝗰𝘆:
│ | -> Bình luận: {explain_privacy(comment_setting)}
│ | -> Duet: {explain_privacy(duet_setting)}
│ | -> Stitch: {explain_privacy(stitch_setting)}
│ | -> Tải video: {explain_privacy(download_setting)}
│ 𝗕𝗶𝗼: {user_info.get('signature', '')}
│ 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀: {stats.get('followerCount', 0):,} Follower
│ 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴: {stats.get('followingCount', 0)} Đang Follow
│ 𝗙𝗿𝗶𝗲𝗻𝗱𝘀: {stats.get('friendCount', 0)} Bạn Bè
│ 𝗟𝗶𝗸𝗲𝘀: {stats.get('heartCount', 0):,} Thích
│ 𝗩𝗶𝗱𝗲𝗼𝘀: {stats.get('videoCount', 0)} Video
├─────────────⭔
│ 𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗧𝗶𝗺𝗲: {create_time}
│ 𝗡𝗮𝗺𝗲 𝗨𝗽𝗱𝗮𝘁𝗲: {nick_update_time}
│ 𝗥𝗲𝗴𝗶𝗼𝗻: {region_flag}
│ 𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲: {language}
╰─────────────⭓
</blockquote>
        """
        return result, avatar_url
    except requests.RequestException as e:
        return f"Không thể lấy dữ liệu từ API. Lỗi: {e}", None

@bot.message_handler(commands=['tt'])
def handle_tiktok_info(message):
    chat_id = message.chat.id
    message_id = message.message_id
    if not is_allowed_group(chat_id):
        bot.send_message(chat_id, "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.", reply_to_message_id=message_id)
        return
    try:
        # Lấy username sau lệnh /tt
        parts = message.text.split(' ', 1)
        if len(parts) < 2 or not parts[1].strip():
            bot.reply_to(
                message,
                "⚠️ Vui lòng nhập username hoặc link TikTok sau lệnh /tt\n💬 Ví dụ: <code>/tt fanduonghoang</code>",
                parse_mode='HTML')
            return
        username = parts[1].strip()
        result, avatar_url = get_tiktok_info(username)
        if avatar_url:
            bot.send_photo(message.chat.id, avatar_url, caption=result, parse_mode='HTML')
        else:
            bot.reply_to(message, result, parse_mode='HTML')
        # Xóa lệnh của người dùng sau khi gửi kết quả thành công
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            print(f"Lỗi xóa tin nhắn: {e}")
    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi: {e}")

#===================================#
@bot.message_handler(commands=['tiktok'])
def handle_tiktok(message):
    chat_id = message.chat.id
    message_id = message.message_id
    if not is_allowed_group(chat_id):
        bot.send_message(chat_id, "❌ Bạn không có quyền sử dụng lệnh này. Vui lòng truy cập nhóm @nhomspamcallsms để sử dụng các lệnh.", reply_to_message_id=message_id)
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Vui lòng nhập <strong>link video Tiktok</strong> sau /tiktok.\n\n💭 Ví dụ: <code>/tiktok https://vt.tiktok.com/ZNdNkdBQY/</code>")
        return

    url = args[1].strip()
    api_url = f'https://offvn.x10.mx/php/video.php?url={requests.utils.quote(url)}'
    try:
        res = requests.get(api_url)
        data = res.json()
    except Exception as e:
        bot.reply_to(message, "❌ Lỗi khi truy cập API.")
        return

    if data.get('msg') != 'success' or 'data' not in data:
        bot.reply_to(message, "❌ Không thể tải <strong>video</strong> từ <strong>URL</strong> được cung cấp.")
        return

    d = data['data']
    video_url = d.get('play')
    music_url = d.get('music')

    do_dai_video = f"🎮 Độ Dài Video: {d.get('duration')} giây" if d.get('duration') else f"🎶 Độ Dài Nhạc: {d['music_info']['duration']} giây"
    dung_luong = f"🗂️ Dung Lượng: {d.get('size')} MB\n" if d.get('size') else ""
    la_ad = "📢 Là Video Quảng Cáo\n" if d.get('is_ad') else ""

    caption = (
        f"🎥 <strong>{d.get('title')}</strong>\n\n"
        f"<blockquote><i>"
        f"👤 Tác giả: <a href='https://www.tiktok.com/@{d['author']['unique_id']}'>{d['author']['nickname']}</a>\n"
        f"🌍 Khu Vực: {d.get('region')}\n"
        f"{do_dai_video}\n"
        f"{dung_luong}"
        f"🗓️ Ngày Đăng: {d.get('create_time')}\n"
        f"{la_ad}"
        f"---------------------------------------\n"
        f"▶️ Views: {d.get('play_count')}\n"
        f"❤️ Likes: {d.get('digg_count')}\n"
        f"💬 Comments: {d.get('comment_count')}\n"
        f"🔄 Shares: {d.get('share_count')}\n"
        f"⬇️ Downloads: {d.get('download_count')}\n"
        f"📥 Favorites: {d.get('collect_count')}"
        f"</i></blockquote>"
    )

    kb = InlineKeyboardMarkup()
    if d.get('size', 0) > 20:
        kb.add(
            InlineKeyboardButton("🎥 Link Download Video", url=f"https://api.zm.io.vn/download/?url={video_url}&extension=mp4&name=downvideott_bot&quality=watermark")
        )
        kb.add(
            InlineKeyboardButton("🎵 Link Download Nhạc", url=f"https://api.zm.io.vn/download/?url={music_url}&extension=mp3&name=downvideott_bot&quality=audio")
        )
        bot.reply_to(message, f"{caption}\n⚠️ Video quá lớn để gửi trực tiếp. Bạn có thể tải video từ liên kết dưới đây:", reply_markup=kb)
        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception as e:
            print(f"Lỗi xóa tin nhắn: {e}")
    else:
        if video_url and 'mp4' in video_url:
            bot.send_chat_action(chat_id, 'upload_video')
            bot.send_video(chat_id, video_url, caption=caption, reply_markup=kb)
            try:
                bot.delete_message(chat_id, message.message_id)
            except Exception as e:
                print(f"Lỗi xóa tin nhắn: {e}")
        elif 'images' in d and d['images']:
            images = d['images']
            bot.send_chat_action(chat_id, 'upload_photo')
            try:
                # Chia ảnh thành nhiều album nhỏ, mỗi album tối đa 10 ảnh
                for i in range(0, len(images), 10):
                    batch = images[i:i+10]
                    media = []
                    for idx, img in enumerate(batch):
                        if idx == 0:
                            media.append(InputMediaPhoto(media=img, caption=caption))
                        else:
                            media.append(InputMediaPhoto(media=img))
                    if len(batch) > 1:
                        bot.send_media_group(chat_id, media)
                    else:
                        bot.send_photo(chat_id, batch[0], caption=caption)
                try:
                    bot.delete_message(chat_id, message.message_id)
                except Exception as e:
                    print(f"Lỗi xóa tin nhắn: {e}")
            except Exception as e:
                print(f"Lỗi gửi media group: {e}")
                # Nếu lỗi, gửi từng ảnh
                for img in images:
                    bot.send_photo(chat_id, img)
                try:
                    bot.delete_message(chat_id, message.message_id)
                except Exception as e:
                    print(f"Lỗi xóa tin nhắn: {e}")
            # Gửi audio từ bộ nhớ
            send_audio(bot, chat_id, music_url, d['music_info']['title'], d['music_info']['author'], d['music_info']['cover'], caption)
        else:
            bot.reply_to(message, "⚠️ Không tìm thấy <strong>ảnh</strong> để gửi hoặc link không ở <strong>chế độ công khai</strong>.")
            try:
                bot.delete_message(chat_id, message.message_id)
            except Exception as e:
                print(f"Lỗi xóa tin nhắn: {e}")

def send_audio(bot, chat_id, audio_url, title, performer, thumb_url, caption):
    try:
        audio_data = requests.get(audio_url).content
        thumb_data = requests.get(thumb_url).content

        audio_file = BytesIO(audio_data)
        audio_file.name = "audio.mp3"
        thumb_file = BytesIO(thumb_data)
        thumb_file.name = "thumb.jpg"

        bot.send_audio(
            chat_id,
            audio_file,
            title=title,
            performer=performer,
            caption=caption,
            thumb=thumb_file
        )
    except Exception as e:
        print(f"Lỗi gửi audio: {e}")

bot.infinity_polling()