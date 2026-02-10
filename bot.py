import telebot
from telebot import types

# আপনার দেওয়া টোকেন ও আইডি
API_TOKEN = '8577584723:AAGDCZQ_aq-Uycyvp3fW2HFlKsKisghtuvM'
ADMIN_ID = 7766097917

bot = telebot.TeleBot(API_TOKEN)

# মেম্বাররা /start দিলে যা দেখবে
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn = types.KeyboardButton("Fast ID Submit")
    markup.add(btn)
    
    welcome_msg = "Welcome to Unknown\n\nআপনি এই বটের মাধ্যমে আমাদের সাথে সরাসরি যোগাযোগ করতে পারেন।"
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup)

# 'Fast ID Submit' বাটনের কাজ
@bot.message_handler(func=lambda message: message.text == "Fast ID Submit")
def fast_id(message):
    bot.reply_to(message, "অনুগ্রহ করে আপনার আইডিটি এখানে লিখে পাঠিয়ে দিন।")

# মেম্বারদের মেসেজ অ্যাডমিনের কাছে আসা
@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def forward_to_admin(message):
    # আপনার কাছে মেসেজ ফরওয়ার্ড হবে
    markup = types.InlineKeyboardMarkup()
    # Received বাটন যা ক্লিক করলে ইউজারের কাছে কনফার্মেশন যাবে
    btn = types.InlineKeyboardButton("Received ✅", callback_data=f"rec_{message.chat.id}")
    markup.add(btn)
    
    # আপনার কাছে নোটিফিকেশন আসবে
    bot.send_message(ADMIN_ID, f"🔔 নতুন মেসেজ এসেছে!\n👤 User ID: {message.chat.id}")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, "মেসেজটি পেয়েছেন? কনফার্ম করতে নিচের বাটনে ক্লিক করুন:", reply_markup=markup)

# 'Received' বাটনে ক্লিক করলে মেম্বারের কাছে অটো রিপ্লাই যাবে
@bot.callback_query_handler(func=lambda call: call.data.startswith('rec_'))
def handle_received_button(call):
    user_id = int(call.data.split('_')[1])
    try:
        bot.send_message(user_id, "✅ আপনার মেসেজটি আমরা পেয়েছি। কিছুক্ষণের মধ্যে আপনার সাথে যোগাযোগ করা হবে।")
        bot.edit_message_text("মেসেজটি রিসিভ করা হয়েছে এবং ইউজারকে জানানো হয়েছে।", ADMIN_ID, call.message.message_id)
        bot.answer_callback_query(call.id, "User notified successfully!")
    except Exception as e:
        bot.answer_callback_query(call.id, "Error: মেসেজ পাঠানো যায়নি।")

# অ্যাডমিন যখন কোনো মেসেজের রিপ্লাই দিবে
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and message.reply_to_message)
def admin_reply(message):
    try:
        # ফরওয়ার্ড করা মেসেজ থেকে ইউজার আইডি বের করা
        if message.reply_to_message.forward_from:
            user_id = message.reply_to_message.forward_from.id
            bot.send_message(user_id, f"📩 Admin Reply:\n\n{message.text}")
            bot.send_message(ADMIN_ID, "✅ রিপ্লাই পাঠানো হয়েছে।")
        else:
            bot.send_message(ADMIN_ID, "❌ ইউজারের প্রাইভেসি সেটিং এর কারণে সরাসরি রিপ্লাই যাচ্ছে না।")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ ভুল হয়েছে: {e}")

print("Bot is running...")
bot.polling(none_stop=True)