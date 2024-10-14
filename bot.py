import telebot
import requests
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot_token = "7302390454:AAG10RLLFfWYQJtYbVGIGIYB0CfPcUfP_40"
bot = telebot.TeleBot(bot_token)

channel_id = "XXXTED5"

def tik(py_php):
    headers = {
        'origin': 'https://lovetik.com',
        'referer': 'https://lovetik.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-A105F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/18.0 Chrome/99.0.4844.88 Mobile Safari/537.36',
        'cookie': '_ga_30X9VRGZQ4=GS1.1.1662950739.1.0.1662950739.0.0.0',
    }
    
    data = {'query': py_php}
    
    response = requests.post("https://lovetik.com/api/ajax/search", headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(channel_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False
       
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not check_subscription(message.from_user.id):
        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton(text="🔗", url=f"https://t.me/{channel_id[1:]}")
        markup.add(btn)
        bot.send_message(message.chat.id, "لأستخدام البوت، يجب عليك الاشتراك في القناة أولاً.", reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        my_account_btn = InlineKeyboardButton(text="🔗", url=f"https://t.me/{channel_id[1:]}")
        markup.add(my_account_btn)
        bot.send_message(message.chat.id, "- مرحبًا بك عزيزي \n- أرسل لي رابط فيديو TikTok وسأقوم بتحميله لك .", reply_markup=markup)
                
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not check_subscription(message.from_user.id):
        bot.send_message(message.chat.id, "لأستخدام البوت، يجب عليك الاشتراك في القناة أولاً.")
        return

    url = message.text
    if "tiktok" in url:
        sent_msg = bot.reply_to(message, "🫧 | انتظر قليلاً ...", reply_to_message_id=message.message_id)
        video_info = tik(url)        
        if video_info and 'links' in video_info and len(video_info['links']) > 0:
            download_link = video_info['links'][0]['a']
            video_content = requests.get(download_link, stream=True)            
            if video_content.status_code == 200:
                video_file = "video.mp4"
                with open(video_file, "wb") as f:
                    for chunk in video_content.iter_content(chunk_size=1024):  
                        if chunk:
                            f.write(chunk)
                bot.delete_message(message.chat.id, sent_msg.message_id)
                success_msg = bot.reply_to(message, "- تم التحميل بنجاح ✅\n- جارٍ إرسال الفيديو .", reply_to_message_id=message.message_id)
                with open(video_file, "rb") as video:
                    bot.send_video(message.chat.id, video)
                bot.delete_message(message.chat.id, success_msg.message_id)  
                if os.path.exists(video_file):
                    os.remove(video_file)
            else:
                bot.send_message(message.chat.id, "حدث خطأ أثناء تحميل الفيديو.")
        else:
            bot.send_message(message.chat.id, "لم أتمكن من تحميل الفيديو. تأكد من الرابط وحاول مرة أخرى.")
    else:
        bot.send_message(message.chat.id, "الرجاء إرسال رابط فيديو TikTok.")

bot.infinity_polling()
