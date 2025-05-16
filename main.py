import telebot
import requests
from telebot import types
import re
import time
import schedule
import os
import threading
from threading import Thread
import subprocess
import random
from datetime import datetime, timedelta, timezone
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN_BOT = "8115420431:AAFCyTWxDiGbRdJDZGQc-4jeSxK0Ok_3c-M"
bot = telebot.TeleBot(TOKEN_BOT)
# Lưu thời gian bấm để chống spam
user_last_request = {}
ADMIN_IDS = [6452283369]
ADMIN_ID = 6452283369
chat_id = -1002170831477
VIP_FILE = "vip.json"
USER_FILE = "user.txt"
last_used = {}
processes = []
MOBILE_CARRIERS = {
    "032": "Viettel", "033": "Viettel", "034": "Viettel", "035": "Viettel", "036": "Viettel",
    "037": "Viettel", "038": "Viettel", "039": "Viettel", "086": "Viettel", "096": "Viettel",
    "097": "Viettel", "098": "Viettel",
    "070": "Mobifone", "079": "Mobifone", "077": "Mobifone", "076": "Mobifone", "078": "Mobifone",
    "090": "Mobifone", "093": "Mobifone", "089": "Mobifone",
    "083": "Vinaphone", "084": "Vinaphone", "085": "Vinaphone", "081": "Vinaphone", "082": "Vinaphone",
    "091": "Vinaphone", "094": "Vinaphone", "088": "Vinaphone",
    "056": "Vietnamobile", "058": "Vietnamobile",
    "059": "Gmobile"
}

def load_vip_data():
    # Định nghĩa hàm này để lấy dữ liệu VIP từ file hoặc database
    # Ví dụ:
    try:
        import json
        with open('vip_data.json', 'r', encoding='utf8') as f:
            return json.load(f)
    except:
        return {}

def save_vip_data(data):
    # Định nghĩa hàm này để lưu dữ liệu VIP
    import json
    with open('vip_data.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def checkvip(user_id):
    vip_data = load_vip_data()
    now = int(datetime.now().strftime("%Y%m%d%H%M%S"))
    return user_id in vip_data and vip_data[user_id]['tghethan'] > now

def get_carrier_info(phone_number):
    # Định nghĩa logic nhận diện nhà mạng/mã vùng ở đây
    prefix = phone_number[:3]
    carrier = "Không xác định"
    # ... logic phân tích carrier ...
    return prefix, carrier

def xoatn(message, delay):
    # Hàm xóa tin nhắn sau delay giây
    time.sleep(delay)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

def safe_load_json(filename, default=None):
    if not os.path.isfile(filename):
        return default if default is not None else {}
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except Exception:
            return default if default is not None else {}

def safe_save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def check_vip(user_id):
    now = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    vip_data = safe_load_json(VIP_FILE, {})
    if str(user_id) in vip_data:
        return now < vip_data[str(user_id)]['tghethan']
    return False

def delete_message_later(chat_id, message_id, delay=5):
    def _delete():
        time.sleep(delay)
        try:
            bot.delete_message(chat_id, message_id)
        except Exception:
            pass
    threading.Thread(target=_delete).start()

def get_carrier_info(phone_number):
    prefix = phone_number[:3]
    carrier = MOBILE_CARRIERS.get(prefix, "Không xác định")
    return prefix, carrier

def get_vn_time():
    vn_timezone = timezone(timedelta(hours=7))
    return datetime.now(vn_timezone)

def ensure_user_file():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, 'w', encoding='utf-8') as f:
            pass

def is_key_used_today(user_id, key):
    vn_now = get_vn_time()
    today_str = vn_now.strftime('%d/%m/%Y')
    with open(USER_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                uid, used_key, date_str = line.strip().split('|')
                if str(user_id) == uid and used_key == key and date_str == today_str:
                    return True
            except:
                continue
    return False

def save_user_key(user_id, key):
    vn_now = get_vn_time()
    today_str = vn_now.strftime('%d/%m/%Y')
    with open(USER_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{user_id}|{key}|{today_str}\n")

def delete_message_later(chat_id, message_id, delay=0):
    # Nếu muốn xóa tin nhắn sau thời gian, có thể dùng threading.Timer
    pass  # Giữ nguyên nếu chưa cần tính năng này

@bot.message_handler(commands=['getkey'])
def getkey_cmd(message):
    import random  # Thêm import nếu chưa có
    user_id = int(message.from_user.id)
    full_name = message.from_user.full_name
    vn_now = get_vn_time()
    ngay = int(vn_now.strftime('%d'))
    tgsuccess = vn_now.strftime("%d/%m/%Y %H:%M:%S")
    keyso = str(ngay * 8276383 + 93732373 * user_id + user_id * user_id - ngay)
    key = "BOT/" + keyso
    url = f"https://link4m.co/api-shorten/v2?api=6506fd36fba45f6d07613987&url=https://offvn.x10.mx?key={key}"

    try:
        data = requests.get(url, timeout=10).json()
        linkvuot = data.get('shortenedUrl', 'LỖI API')
    except Exception:
        linkvuot = 'LỖI API'

    # Danh sách video
    videos = [
        "https://offvn.click/1.mp4",
        "https://spamcallsms.x10.mx/4.mp4",
        "https://spamcallsms.x10.mx/11.mp4",
        "https://spamcallsms.x10.mx/2.mp4",
        "https://spamcallsms.x10.mx/3.mp4",
        "https://spamcallsms.x10.mx/5.mp4",
        "https://spamcallsms.x10.mx/6.mp4",
        "https://spamcallsms.x10.mx/7.mp4",
        "https://spamcallsms.x10.mx/8.mp4",
        "https://spamcallsms.x10.mx/9.mp4",
        "https://spamcallsms.x10.mx/10.mp4"
    ]

    video = random.choice(videos)  # Chọn ngẫu nhiên video

    help_text = (
        f'''Xin Chào ! <a href="tg://user?id={user_id}">{full_name}</a>\n'''
        f'''<blockquote>╭─────────────⭓\n│<b>KEY NGÀY: </b>{tgsuccess}\n│{linkvuot}\n╰─────────────⭓</blockquote>\n'''
        f'''<b>⚠️ Vượt xong nhập key sau lệnh /key\n💭 Ví dụ: /key BOT/{keyso}</b>'''
    )

    bot.send_video(
        message.chat.id, video=video, caption=help_text,
        reply_to_message_id=message.message_id, supports_streaming=True, parse_mode='HTML'
    )

    threading.Thread(target=xoatn, args=(message, 0)).start()
@bot.message_handler(commands=['key'])
def nhapkey(message):
    args = message.text.split(maxsplit=1)
    user_id = int(message.from_user.id)
    full_name = message.from_user.full_name
    vn_now = get_vn_time()
    ngay = int(vn_now.strftime('%d'))
    keyso = str(ngay * 8276383 + 93732373 * user_id + user_id * user_id - ngay)
    key = "BOT/" + keyso

    if len(args) < 2:
        bot.reply_to(
            message,
            "⚠️ Vui Lòng Sử Dụng Key Đã Vượt Sau Lệnh /key\n💬 Ví Dụ: /key BOT/42236748505343623944"
        )
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    input_key = args[1].strip()
    ensure_user_file()
    if input_key == key:
        if is_key_used_today(user_id, key):
            bot.reply_to(message, "✅ Bạn đã nhập key thành công hôm nay rồi!")
            threading.Thread(target=xoatn, args=(message, 0)).start()
            return
        save_user_key(user_id, key)
        bot.reply_to(
            message,
            f"✅ Chúc Mừng Bạn Đã Nhập Key Chính Xác Lúc {vn_now.strftime('%H:%M:%S %d/%m/%Y')}!\nVà Giờ Có Thể Sử Dụng Lệnh /spam"
        )
        for admin_id in ADMIN_IDS:
            try:
                bot.send_message(
                    admin_id,
                    f"🔑 *Người dùng đã xác nhận key!*\n"
                    f"👤 *User:* [{full_name}](tg://user?id={user_id})\n"
                    f"🆔 *ID:* `{user_id}`\n"
                    f"🔐 *Key:* `{key}`\n"
                    f"⏰ *Thời gian:* `{vn_now.strftime('%H:%M:%S %d/%m/%Y')}`",
                    parse_mode="Markdown"
                )
            except Exception:
                pass
    else:
        bot.reply_to(message, "❌ Key không hợp lệ. Hãy lấy lại key với /getkey.")
    threading.Thread(target=xoatn, args=(message, 0)).start()

@bot.message_handler(commands=['spam'])
def handle_sms_command(message):
    user_id = int(message.from_user.id)
    full_name = message.from_user.full_name
    args = message.text.split()
    vn_now = get_vn_time()
    ensure_user_file()

    if user_id in last_used:
        elapsed_time = vn_now - last_used[user_id]
        if elapsed_time.total_seconds() < 300:
            remaining_time = int(300 - elapsed_time.total_seconds())
            bot.reply_to(
                message,
                f"❌ Xin Lỗi !\n\nLệnh FREE Đợi 300 Giây, Mới Được Sử Dụng Lại.\n"
                f"⚠️ Vui lòng thử lại sau {remaining_time} giây\nHoặc Mua VIP Để Sử Dụng Tốt Hơn"
            )
            threading.Thread(target=xoatn, args=(message, 0)).start()
            return

    ngay = int(vn_now.strftime('%d'))
    keyso = str(ngay * 8276383 + 93732373 * user_id + user_id * user_id - ngay)
    key = "BOT/" + keyso

    with open(USER_FILE, 'r') as f:
        lines = f.read().splitlines()
        allowed = any(str(user_id) in line and key in line for line in lines)
    if not allowed:
        bot.reply_to(
            message,
            "⚠️ Bạn Chưa Lấy Key Ngày Hôm Nay.\n💬 Vui Lòng Nhập Lệnh /getkey\nĐể Lấy Key Ngày Hôm Nay."
        )
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    if len(args) < 3:
        bot.reply_to(message, "⚠️ Hướng Dẫn Sử Dụng Lệnh /spam\n💬 Ví Dụ: /spam 0969549113 5")
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    phone_number = args[1]
    try:
        solan = int(args[2])
    except:
        bot.reply_to(message, "⚠️ Số lần gửi phải là số nguyên. Ví dụ: /spam 0969549113 5")
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    if not re.search(r"^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[1-6|8|9]|9[0-4|6-9])[0-9]{7}$", phone_number):
        bot.reply_to(message, '❌ SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ !')
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    if phone_number in ["0763633372"]:
        bot.reply_to(message, "Số Điện Thoại Này Không Thể Spam Được ❌")
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    if solan > 5:
        bot.reply_to(
            message,
            "⚠️ Chỉ Có Lệnh VIP Mới Được Sử Dụng Số Lặp Lớn Hơn 5. \n💬 Mua VIP Xin Liên Hệ: @off_vn Hoặc Nhập Lệnh /muavip."
        )
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    dache = phone_number[:2] + "******" + phone_number[8:]
    prefix, carrier = get_carrier_info(phone_number)
    tg_hethan_free = datetime.now().replace(hour=23, minute=59, second=59).strftime("%d/%m/%Y %H:%M:%S")
    video = "https://offvn.io.vn/sms.mp4"
    keyboard1 = InlineKeyboardMarkup(row_width=1)
    keyboard1.add(
        InlineKeyboardButton(text="💬 Liên Hệ ADMIN", url='https://t.me/off_vn'),
    )

    guidi = f"""📲 <b>TẤN CÔNG ĐÃ GỬI ĐI</b>
<blockquote><i>👤 Name: <a href='tg://user?id={user_id}'>{full_name}</a>
🆔 ID: <a href='tg://user?id={user_id}'>{user_id}</a>
⏰ Thời gian: {vn_now.strftime('%H:%M:%S %d/%m/%Y')}
📵 Phone: {dache}
🔄 Lặp: {solan}
🔢 Mã vùng: {prefix}
📡 Nhà mạng: {carrier}
💰 Plan: Free
⏳ Hết hạn key: {tg_hethan_free}</i></blockquote>"""

    bot.send_video(
        message.chat.id,
        video=video,
        caption=guidi,
        reply_to_message_id=message.message_id,
        supports_streaming=True,
        parse_mode='HTML',
        reply_markup=keyboard1
    )
    threading.Thread(target=xoatn, args=(message, 0)).start()
    # Gửi SMS và hiển thị báo cáo
    try:
        process = subprocess.Popen(['python3', 'sms.py', phone_number, str(solan)],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        try:
            result = json.loads(stdout)
            success = result.get("success", 0)
            fail = result.get("fail", 0)
        except:
            success = solan
            fail = 0

        report = f"""📊 <b>BÁO CÁO GỬI TIN NHẮN</b>
📱 Số điện thoại: <b>{dache}</b>
✅ Thành công: <b>{success}</b>
❌ Thất bại: <b>{fail}</b>"""

        bot.send_message(message.chat.id, report, parse_mode='HTML')
        last_used[user_id] = vn_now

    except Exception as e:
        bot.send_message(message.chat.id, f"Lỗi khi gửi SMS: {e}")
        
@bot.message_handler(commands=['adduser'])
def adduser(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, "Bạn không được phép sử dụng lệnh này!")
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "Sử dụng: /adduser {id người dùng} {số ngày}")
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    user_id_add = args[1]
    try:
        songay = int(args[2])
    except ValueError:
        bot.reply_to(message, "Số ngày không hợp lệ!")
        return

    # Lấy thông tin người dùng từ Telegram
    try:
        user_info = bot.get_chat(user_id_add)
        buyer_name = user_info.first_name
        if hasattr(user_info, 'last_name') and user_info.last_name:
            buyer_name += f" {user_info.last_name}"
    except Exception:
        buyer_name = "Không xác định"

    vn_now = get_vn_time()
    ngayhethan = vn_now + timedelta(days=songay)
    ngayhethan_int = int(ngayhethan.strftime("%Y%m%d%H%M%S"))
    ngayhethan_str = ngayhethan.strftime("%Y-%m-%d %H:%M:%S")

    vip_data = load_vip_data()
    vip_data[user_id_add] = {
        "buyer": buyer_name,
        "tghethan": ngayhethan_int
    }
    save_vip_data(vip_data)

    bot.send_message(
        message.chat.id, 
        f"🎉 Thành viên mới đã được thêm vào VIP!\n👤 Tên: {buyer_name}\n🆔 ID: {user_id_add}\n🗓️ Hết hạn: {ngayhethan_str}"
    )
    threading.Thread(target=xoatn, args=(message,0)).start()
last_used = {}

@bot.message_handler(commands=['spamvip'])
def handle_sms_command(message):
    user_id = str(message.from_user.id)
    full_name = message.from_user.full_name or ""
    vn_now = get_vn_time()

    if user_id in last_used:
        elapsed_time = (vn_now - last_used[user_id]).total_seconds()
        if elapsed_time < 100:
            remaining_time = 100 - elapsed_time
            bot.reply_to(message, f"💬 Lưu Ý: Lệnh VIP Đợi 100 Giây Mới Được Sử Dụng Lại.\n⚠️ Vui lòng thử lại sau {int(remaining_time)} giây.")
            return

    if not checkvip(user_id):
        bot.reply_to(message, "⚠️ Bạn Chưa Mua Vip, Không Được Phép Sử Dụng Lệnh Này!\n💬 Nhập Lệnh /muavip Để Mua VIP.")
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "⚠️ Hướng Dẫn Sử Dụng Lệnh /spamvip\n💬 Ví Dụ: /spamvip 0969549113 50")
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    phone_number = args[1]
    if not re.fullmatch(r"^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$", phone_number):
        bot.reply_to(message, '❌ SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ!')
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    if phone_number in ["0763633372"]:
        bot.reply_to(message, "Số Điện Thoại Này Không Thể Spam Được ❌")
        threading.Thread(target=xoatn, args=(message, 0)).start()
        return

    try:
        solan = int(args[2])
        if solan > 50 or solan < 1:
            bot.reply_to(message, "⚠️ Lệnh VIP Được Sử Dụng Số Lặp Tối Đa 50.\n💬 Ví Dụ: /spamvip 0969549113 50")
            threading.Thread(target=xoatn, args=(message, 0)).start()
            return
    except Exception:
        bot.reply_to(message, "Số lặp không hợp lệ!")
        return

    vip_data = load_vip_data()
    if user_id in vip_data:
        expiration_timestamp = vip_data[user_id]['tghethan']
        expiration_time = datetime.strptime(str(expiration_timestamp), "%Y%m%d%H%M%S")
        vip_expiry_str = expiration_time.strftime("%d/%m/%Y %H:%M:%S")
        plan_vip = "VIP"
    else:
        vip_expiry_str = "Không có"
        plan_vip = "Không xác định"

    prefix, carrier = get_carrier_info(phone_number)
    dache = phone_number[:2] + "******" + phone_number[8:]
    video = random.choice(["https://offvn.io.vn/sms.mp4"])
    keyboard1 = InlineKeyboardMarkup(row_width=2)
    keyboard1.add(
        InlineKeyboardButton(text="💬 Liên Hệ ADMIN", url='https://t.me/off_vn'),
    )

    guidi = f"""📲 <b>TẤN CÔNG ĐÃ GỬI ĐI</b>
<blockquote><i>👤 Name: <a href='tg://user?id={user_id}'>{full_name}</a>
🆔 ID: <a href='tg://user?id={user_id}'>{user_id}</a>
⏰ Thời gian: {vn_now.strftime('%H:%M:%S %d/%m/%Y')}
📵 Phone: {dache}
🔄 Lặp: {solan}
🔢 Mã vùng: {prefix}
📡 Nhà mạng: {carrier}
💰 Plan: {plan_vip}
⏳ Hết hạn VIP: {vip_expiry_str}</i></blockquote>"""

    bot.send_video(message.chat.id, video=video, caption=guidi, reply_to_message_id=message.message_id, supports_streaming=True, parse_mode='HTML', reply_markup=keyboard1)
    threading.Thread(target=xoatn, args=(message, 0)).start()
    # Gọi script vip.py và báo cáo kết quả
    try:
        process = subprocess.Popen(['python3', 'vip.py', phone_number, str(solan)],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        try:
            result = json.loads(stdout)
            success = result.get("success", 0)
            fail = result.get("fail", 0)
        except:
            success = solan
            fail = 0

        report = f"""📊 <b>BÁO CÁO GỬI TIN NHẮN</b>
📱 Số điện thoại: <b>{dache}</b>
✅ Thành công: <b>{success}</b>
❌ Thất bại: <b>{fail}</b>"""

        bot.send_message(message.chat.id, report, parse_mode='HTML')
        last_used[user_id] = vn_now

    except Exception as e:
        bot.send_message(message.chat.id, f"Lỗi khi gửi SMS: {e}")
@bot.message_handler(commands=['muavip'])
def handle_muavip(message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username if message.from_user.username else "Không có"

    # Chống spam: 60s mới cho bấm lại
    now = int(time.time())
    if user_id in user_last_request and now - user_last_request[user_id] < 60:
        bot.reply_to(message, "⏳ Vui lòng chờ 1 phút trước khi thực hiện lại.")
        return
    user_last_request[user_id] = now

    # Thông tin thanh toán
    bank_name = "MB Bank"
    stk = "444888365"
    chu_tk = "HOANG DUY TU"
    price = "40.000 VNĐ / 1 tháng"
    nd_chuyen_khoan = f"muavip_{user_id}"

    # QR code động với nội dung chuyển khoản
    qr_link = (
        f"https://img.vietqr.io/image/MBBank-{stk}-compact.png?amount=40000&addInfo={nd_chuyen_khoan}"
    )

    # Bàn phím chỉ có nút liên hệ admin
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📩 Liên hệ Admin", url="https://t.me/off_vn")
    )

    # Nội dung hiển thị
    caption = (
        "🌟 <b>THÔNG TIN MUA VIP</b> 🌟\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Người mua:</b> {full_name} ({'@'+username if username != 'Không có' else 'Ẩn'})\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🏦 <b>Ngân hàng:</b> {bank_name}\n"
        f"💳 <b>STK:</b> <code>{stk}</code>\n"
        f"👑 <b>Chủ tài khoản:</b> <b>{chu_tk}</b>\n"
        f"💰 <b>Số tiền:</b> <code>{price}</code>\n"
        f"📝 <b>Nội dung CK:</b> <code>{nd_chuyen_khoan}</code>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⚠️ <b>Lưu ý:</b> <i>Chuyển đúng nội dung và gửi ảnh biên lai cho admin để được kích hoạt VIP siêu tốc!</i>"
    )

    # Gửi ảnh QR kèm thông tin
    bot.send_photo(
        message.chat.id, qr_link, caption, parse_mode="HTML", reply_markup=keyboard
    )

    # Xóa tin nhắn lệnh gốc
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Lỗi khi xóa tin nhắn: {e}")
@bot.message_handler(commands=['hd'])
def handle_help(message):
    full_name = message.from_user.full_name
    user_id = message.from_user.id
    help_text = f'''
<b>HELLO! </b><a href="tg://user?id={user_id}">{full_name}</a>

<b>DƯỚI ĐÂY LÀ DANH SÁCH LỆNH SPAM 📵
/getkey - Lấy Key SPAM SMS CALL
/key - [ KEY ĐÃ VƯỢT LINK ]
/spam - [ SĐT ] [ SỐ LẦN ] [ MIỄN PHÍ ]
/spamvip - [ SĐT ] [ SỐ LẦN ] [ VIP ]
/checkvip - Để xem thông tin VIP của bạn
/muavip - MUA VIP SPAM SMS CALL</b>
💬 LƯU Ý: Bạn có thể bấm vào các lệnh để xem hướng dẫn sử dụng.'''

    # Tạo nút "Đóng"
    markup = types.InlineKeyboardMarkup()
    close_btn = types.InlineKeyboardButton("Đóng", callback_data='close_help')
    markup.add(close_btn)

    # Gửi tin nhắn trợ giúp
    bot.send_message(message.chat.id, help_text, parse_mode='HTML', reply_markup=markup)

    # Xóa lệnh gốc của người dùng
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Không thể xóa lệnh gốc: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'close_help')
def close_help_callback(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(f"Không thể xóa tin nhắn khi nhấn nút: {e}")

@bot.message_handler(commands=['checkvip'])
def check_vip_status(message):
    user_id = str(message.from_user.id)
    vip_data = load_vip_data()
    now = datetime.now()

    close_button = InlineKeyboardMarkup()
    close_button.add(InlineKeyboardButton("❌ Đóng", callback_data="close_msg"))

    if not vip_data:
        bot.reply_to(message, "❌ <b>Không có ai trong danh sách VIP.</b>", reply_markup=close_button, parse_mode="HTML")
        bot.delete_message(message.chat.id, message.message_id)  # Delete message after responding
        return

    if user_id in ADMIN_IDS:
        response = "📜 <b>DANH SÁCH NGƯỜI MUA VIP</b>\n"
        response += "╔══════════════════════╗\n"
        vip_count = expired_vips = expiring_soon_vips = 0
        detail_lines = []

        for idx, (uid, info) in enumerate(vip_data.items(), 1):
            buyer = info.get("buyer", "Không rõ")
            expiration_timestamp = info.get("tghethan", 0)

            try:
                expiration_time = datetime.strptime(str(expiration_timestamp), "%Y%m%d%H%M%S")
            except Exception:
                expiration_time = now

            remaining_days = (expiration_time - now).days

            if remaining_days < 0:
                expired_vips += 1
            elif remaining_days <= 3:
                expiring_soon_vips += 1

            vip_count += 1

            try:
                user_info = bot.get_chat(int(uid))
                username = f"@{user_info.username}" if user_info.username else "(Không có)"
            except Exception:
                username = "(Không lấy được)"

            detail_lines.append(
                f"🌟 <b>{idx}.</b> <b>{buyer}</b>\n"
                f"🆔 <code>{uid}</code>\n"
                f"🔗 Username: {username}\n"
                f"⏳ <b>{max(0, remaining_days)} ngày</b>\n"
                f"📅 <i>{expiration_time.strftime('%d/%m/%Y %H:%M:%S')}</i>\n"
                "╠═════════════════════"
            )

        response += '\n'.join(detail_lines)
        response += "\n╚═════════════════════╝"
        response += (
            f"\n💡 <b>Tổng số VIP:</b> {vip_count}\n"
            f"🚫 <b>VIP đã hết hạn:</b> {expired_vips}\n"
            f"⚠️ <b>VIP sắp hết hạn (≤ 3 ngày):</b> {expiring_soon_vips}"
        )
        bot.reply_to(message, response, parse_mode="HTML", reply_markup=close_button)
        bot.delete_message(message.chat.id, message.message_id)  # Delete message after responding

    else:
        if user_id not in vip_data:
            bot.reply_to(message, "❌ <b>Bạn chưa mua VIP hoặc đã hết hạn.</b>", reply_markup=close_button, parse_mode="HTML")
            bot.delete_message(message.chat.id, message.message_id)  # Delete message after responding
            return

        info = vip_data[user_id]
        buyer = info.get("buyer", "Không rõ")
        expiration_timestamp = info.get("tghethan", 0)

        try:
            expiration_time = datetime.strptime(str(expiration_timestamp), "%Y%m%d%H%M%S")
        except Exception:
            expiration_time = now

        remaining_days = (expiration_time - now).days

        response = (
            "📜 <b>THÔNG TIN VIP CỦA BẠN</b>\n"
            "╔══════════════════╗\n"
            f"👤 <b>Người mua:</b> {buyer}\n"
            f"🆔 <b>ID:</b> {user_id}\n"
            f"⏳ <b>Còn lại:</b> {max(0, remaining_days)} ngày\n"
            f"📅 <b>Hết hạn:</b> {expiration_time.strftime('%d/%m/%Y %H:%M:%S')}\n"
            "╚══════════════════╝"
        )
        bot.reply_to(message, response, parse_mode="HTML", reply_markup=close_button)
        bot.delete_message(message.chat.id, message.message_id)  # Delete message after responding

    # Gửi cảnh báo nếu sắp hết hạn
    for uid, info in vip_data.items():
        expiration_timestamp = info.get("tghethan", 0)
        try:
            expiration_time = datetime.strptime(str(expiration_timestamp), "%Y%m%d%H%M%S")
        except Exception:
            continue
        remaining_days = (expiration_time - now).days
        if 0 <= remaining_days <= 3:
            buyer = info.get("buyer", "Không rõ")
            try:
                bot.send_message(
                    int(uid),
                    f"⚠️ Chào {buyer}, VIP của bạn sẽ hết hạn trong {remaining_days} ngày nữa! Hãy gia hạn sớm.",
                    parse_mode="HTML"
                )
            except Exception:
                pass

# Xử lý nút đóng
@bot.callback_query_handler(func=lambda call: call.data == "close_msg")
def close_message(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "✅ <b>Tin nhắn đã được đóng.</b>", parse_mode="HTML")
    except Exception:
        pass
@bot.message_handler(commands=['xoavip'])
def remove_vip_user(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "Bạn không được phép sử dụng lệnh này!")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Sử dụng: /xoavip {id người dùng}")
        return

    user_id_remove = args[1].strip()
    vip_data = load_vip_data()
    if user_id_remove not in vip_data:
        bot.reply_to(message, "❌ Người này không có trong danh sách VIP.")
        return

    buyer_name = vip_data[user_id_remove]["buyer"]
    deleted_by = message.from_user.full_name
    vn_now = get_vn_time()

    del vip_data[user_id_remove]
    save_vip_data(vip_data)

    # Gửi thông báo vào nhóm
    bot.send_message(
        chat_id,
        f"⚠️ <b>Thành viên đã bị xóa khỏi VIP!</b>\n"
        f"👤 <b>Tên:</b> {buyer_name}\n"
        f"🆔 <b>ID:</b> {user_id_remove}\n"
        f"🗓️ <b>Ngày xóa:</b> {vn_now.strftime('%H:%M:%S %d/%m/%Y')}\n"
        f"👮‍♂️ <b>Xóa bởi:</b> {deleted_by}",
        parse_mode="HTML"
    )
    threading.Thread(target=xoatn, args=(message, 0)).start()

    # Gửi tin nhắn riêng cho người bị xóa
    try:
        bot.send_message(
            int(user_id_remove),  # Phải truyền kiểu int nếu là user_id Telegram
            f"⚠️ Bạn đã bị xóa khỏi danh sách VIP.\n"
            f"🗓️ Ngày xóa: {vn_now.strftime('%H:%M:%S %d/%m/%Y')}\n"
            f"👮‍♂️ Xóa bởi: {deleted_by}",
            parse_mode="HTML"
        )
        threading.Thread(target=xoatn, args=(message, 0)).start()
    except Exception:
        bot.send_message(
            message.chat.id,
            f"Không thể gửi tin nhắn cho {buyer_name} (ID: {user_id_remove})."
        )


def clear_users_daily():
    try:
        with open("user.txt", "w") as file:
            file.truncate(0)
        print(f"[{datetime.now()}] Đã xóa danh sách người dùng trong user.txt")
    except Exception as e:
        print(f"[{datetime.now()}] Lỗi khi xóa user.txt: {e}")

def run_scheduler():
    schedule.every().day.at("00:00").do(clear_users_daily)
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler, daemon=True).start()
if __name__ == "__main__":
    ensure_user_file()
    bot.infinity_polling()
