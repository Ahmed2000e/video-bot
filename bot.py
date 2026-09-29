import os
import telebot
import yt_dlp

TOKEN = os.getenv('BOT_TOKEN', '8748427478:AAH7yzhHaY6PYf_8qadGBySyy3rWfeWqKi0')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(bot_message):
    bot.reply_to(bot_message, "أهلاً بك! أرسل لي أي رابط فيديو وسأقوم بتحميله وإرساله لك فوراً 📥")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if not url.startswith('http'):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يبدأ بـ http أو https")
        return

    msg = bot.reply_to(message, "⏳ جاري المعالجة والتحميل، يرجى الانتظار...")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video.mp4',
        'max_filesize': 50 * 1024 * 1024,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption="تم التنزيل بنجاح بواسطة البوت ✅")
        
        os.remove('video.mp4')
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"حدث خطأ أثناء التحميل: تأكد من أن الرابط مدعم أو أن حجم الفيديو مناسب.", message.chat.id, msg.message_id)
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')

if __name__ == '__main__':
    bot.infinity_polling()
