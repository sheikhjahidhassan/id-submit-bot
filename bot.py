import os
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "Unknown World is Online!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive() # এটি সবার আগে কল করুন
import telebot
from telebot import types

API_TOKEN = '8577584723:AAGDCZQ_aq-Uycyvp3fW2HFlKsKisghtuvM'
ADMIN_ID = 7766097917

bot = telebot.TeleBot(API_TOKEN)

# ইউজার /start দিলে
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to Unknown World", reply_markup=types.ReplyKeyboardRemove())

# ইউজার যেকোনো কিছু (ফাইল, ফটো, টেক্সট) পাঠালে অ্যাডমিনের কাছে আসবে
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice'])
def handle_all_messages(message):
    if message.chat.id != ADMIN_ID:
        # অ্যাডমিনের জন্য বাটন তৈরি
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("ID Received ✅", callback_data=f"rec_{message.chat.id}")
        btn2 = types.InlineKeyboardButton("Fast ID Submit 🚀", callback_data=f"fast_{message.chat.id}")
        markup.add(btn1, btn2)
        
        # আপনার কাছে মেসেজ বা ফাইলটি ফরওয়ার্ড হবে
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        bot.send_message(ADMIN_ID, f"👤 নতুন ফাইল/মেসেজ এসেছে!\nUser ID: {message.chat.id}", reply_markup=markup)

# বাটন অ্যাকশন হ্যান্ডেল করা
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    data = call.data.split('_')
    action = data[0]
    user_id = data[1]
    
    try:
        if action == "rec":
            bot.send_message(user_id, "✅ আপনার আইডি/ফাইলটি সফলভাবে রিসিভ করা হয়েছে। ধন্যবাদ!")
            bot.edit_message_text(f"✅ ইউজারকে জানানো হয়েছে: ID Received", ADMIN_ID, call.message.message_id)
        elif action == "fast":
            bot.send_message(user_id, "🚀 অনুগ্রহ করে দ্রুত আপনার আইডিটি সাবমিট করুন।")
            bot.edit_message_text(f"🚀 ইউজারকে জানানো হয়েছে: Fast ID Submit", ADMIN_ID, call.message.message_id)
        bot.answer_callback_query(call.id)
    except Exception as e:
        bot.answer_callback_query(call.id, "Error occurred")

# অ্যাডমিন রিপ্লাই দিলে
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and message.reply_to_message)
def admin_reply(message):
    try:
        # ফাইল বা মেসেজ যাই হোক, তার অরিজিনাল ইউজার আইডি বের করা
        if message.reply_to_message.forward_from:
            user_id = message.reply_to_message.forward_from.id
            bot.send_message(user_id, message.text)
            bot.send_message(ADMIN_ID, "📩 রিপ্লাই পাঠানো হয়েছে।")
    except:
        bot.send_message(ADMIN_ID, "❌ সরাসরি রিপ্লাই দেওয়া যাচ্ছে না।")


bot.polling(none_stop=True)
