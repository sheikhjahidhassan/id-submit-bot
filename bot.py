import telebot
from telebot import types

API_TOKEN = '8577584723:AAGDCZQ_aq-Uycyvp3fW2HFlKsKisghtuvM'
ADMIN_ID = 7766097917

bot = telebot.TeleBot(API_TOKEN)

# ইউজারদের আইডি সেভ করার ফাইল
USER_FILE = "users.txt"

def save_user(user_id):
    """নতুন ইউজার আসলে আইডি সেভ করবে"""
    users = get_users()
    if str(user_id) not in users:
        with open(USER_FILE, "a") as f:
            f.write(f"{user_id}\n")

def get_users():
    """সব ইউজারের লিস্ট দিবে"""
    try:
        with open(USER_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id) # আইডি সেভ করা হচ্ছে
    bot.send_message(message.chat.id, "Welcome to Unknown World", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice'])
def handle_incoming_messages(message):
    if message.chat.id != ADMIN_ID:
        save_user(message.chat.id)
        
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("ID Received ✅", callback_data=f"rec_{message.chat.id}")
        markup.add(btn1)
        
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        bot.send_message(ADMIN_ID, f"👤 **নতুন মেসেজ!**\nUser ID: `{message.chat.id}`", 
                         parse_mode="Markdown", reply_markup=markup)
    
    else:
        # এডমিন যদি কারো মেসেজে রিপ্লাই না দিয়ে সরাসরি কিছু লেখে, তবে তা সবার কাছে যাবে (Broadcast)
        if not message.reply_to_message:
            all_users = get_users()
            count = 0
            for user in all_users:
                try:
                    bot.send_message(user, message.text)
                    count += 1
                except:
                    continue
            bot.send_message(ADMIN_ID, f"📢 ব্রডকাস্ট সম্পন্ন! {count} জনের কাছে মেসেজ পাঠানো হয়েছে।")

@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    action, user_id = call.data.split('_')
    if action == "rec":
        try:
            bot.send_message(user_id, "✅ আপনার আইডি/ফাইলটি সফলভাবে রিসিভ করা হয়েছে।")
            bot.answer_callback_query(call.id, "ইউজারকে জানানো হয়েছে।")
        except:
            bot.answer_callback_query(call.id, "ইউজারকে মেসেজ পাঠানো যায়নি।")

# এডমিন যখন স্পেসিফিক কাউকে রিপ্লাই দিবে
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and message.reply_to_message)
def admin_specific_reply(message):
    try:
        # ফরোয়ার্ড করা মেসেজ থেকে আইডি নেওয়ার চেষ্টা
        if message.reply_to_message.forward_from:
            target_id = message.reply_to_message.forward_from.id
        else:
            # টেক্সট থেকে আইডি খুঁজে বের করা
            text = message.reply_to_message.text
            target_id = text.split('User ID: ')[1].split('\n')[0].strip()

        bot.send_message(target_id, f"📩 **এডমিনের উত্তর:**\n\n{message.text}", parse_mode="Markdown")
        bot.send_message(ADMIN_ID, "✅ রিপ্লাইটি শুধুমাত্র ঐ ইউজারের কাছে পাঠানো হয়েছে।")
    except:
        bot.send_message(ADMIN_ID, "❌ আইডি পাওয়া যায়নি। রিপ্লাই দেওয়া সম্ভব হয়নি।")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
