import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from bot_token import BOT_TOKEN
from password import check_password, authorize_user, is_authorized, change_password, OWNER_ID

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}
GROUP_ID = -1002457077960  # Group ID for sending listings


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if is_authorized(chat_id):
        show_main_menu(chat_id)
    else:
        bot.send_message(chat_id, "🔑 Enter the access password:")
        user_data[chat_id] = {'step': 'awaiting_password'}


@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id

    if chat_id in user_data and user_data[chat_id]['step'] == 'awaiting_password':
        if check_password(chat_id, message.text):
            authorize_user(chat_id)
            bot.send_message(chat_id, "✅ Access granted!")
            show_main_menu(chat_id)
        else:
            bot.send_message(chat_id, "❌ Incorrect password. Please try again.")

    elif is_authorized(chat_id):
        step = user_data.get(chat_id, {}).get('step')
        if step == 'changing_password' and chat_id == OWNER_ID:
            change_password(message.text)
            bot.send_message(chat_id, "🔄 Password changed successfully!")
            user_data.pop(chat_id, None)
        else:
            handle_house_data(message)


def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🏠 Add housing information", callback_data="select_type"))
    if chat_id == OWNER_ID:
        markup.add(InlineKeyboardButton("🔑 Change password", callback_data="change_password"))
    bot.send_message(chat_id, "Choose an action:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "select_type")
def select_type(call):
    chat_id = call.message.chat.id
    markup = InlineKeyboardMarkup()
    types = ["House", "Apartment", "Room", "Hotel"]
    for t in types:
        markup.add(InlineKeyboardButton(t, callback_data=f"set_type_{t}"))
    bot.send_message(chat_id, "🏠 Choose the type of housing:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("set_type_"))
def set_type(call):
    chat_id = call.message.chat.id
    house_type = call.data.split("_")[2]

    user_data[chat_id] = {'type': house_type, 'step': 'rent_for', 'photos': []}
    bot.send_message(chat_id, f"🏠 You selected: {house_type}")
    bot.send_message(chat_id, "💁‍♂️ Who is the housing for?")


def handle_house_data(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        return

    step = user_data[chat_id]['step']

    if step == 'price':
        try:
            uzs, usd = message.text.split()
            user_data[chat_id]['price_uzs'] = f"{uzs} UZS"
            user_data[chat_id]['price_usd'] = f"{usd} USD"
            user_data[chat_id]['step'] = 'owner_lives'
        except ValueError:
            bot.send_message(chat_id, "❌ Error! Enter price in format: 1000000 85 (UZS USD)")
            return
    else:
        user_data[chat_id][step] = message.text

    steps = ['rent_for', 'price', 'owner_lives', 'family_members', 'rental_period',
             'address', 'renovation', 'issues', 'phone_number', 'additional_info']

    prompts = {
        'rent_for': "💁‍♂️ Who is the housing for?",
        'price': "💰 Enter the price (UZS USD) separated by space.",
        'owner_lives': "👤 Will the owner live with the tenant? (Yes/No)",
        'family_members': "👨‍👩‍👧‍👦 How many family members will live? (if none, write '0')",
        'rental_period': "📅 What is the rental period?",
        'address': "📍 Enter the address:",
        'renovation': "🛠 Is it renovated? (Yes/No)",
        'issues': "❗️ Any issues? (if none, write 'None')",
        'phone_number': "📞 Your contact phone number:",
        'additional_info': "ℹ️ Additional information (if none, write 'None')"
    }

    if step in steps:
        next_step_index = steps.index(step) + 1
        if next_step_index < len(steps):
            next_step = steps[next_step_index]
            user_data[chat_id]['step'] = next_step
            bot.send_message(chat_id, prompts[next_step])
        else:
            user_data[chat_id]['step'] = 'photo'
            bot.send_message(chat_id, "📸 Send 1 photo of the property.")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    if chat_id not in user_data or user_data[chat_id]['step'] != 'photo':
        return

    user_data[chat_id]['photos'].append(message.photo[-1].file_id)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("➕ Add another photo", callback_data="add_photo"))
    markup.add(InlineKeyboardButton("✅ Done", callback_data="finish"))

    bot.send_message(chat_id, "Choose an action:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["add_photo", "finish"])
def callback_handler(call):
    chat_id = call.message.chat.id

    if call.data == "add_photo":
        bot.send_message(chat_id, "📸 Send another photo.")
    elif call.data == "finish":
        send_post(chat_id)


def send_post(chat_id):
    data = user_data[chat_id]

    text = (
        f"🏠 Type: {data['type']}\n"
        f"💁‍♂️ For whom: {data['rent_for']}\n"
        f"💰 Price: {data['price_uzs']} / {data['price_usd']}\n"
        f"👤 Owner lives with tenant: {data['owner_lives']}\n"
        f"👨‍👩‍👧‍👦 Family members: {data.get('family_members', 'Not specified')}\n"
        f"📅 Rental period: {data['rental_period']}\n"
        f"📍 Address: {data['address']}\n"
        f"🛠 Renovation: {data['renovation']}\n"
        f"❗️ Issues: {data['issues']}\n"
        f"📞 Contact phone: {data['phone_number']}\n"
        f"ℹ️ Additional info: {data['additional_info']}\n"
    )

    media = [InputMediaPhoto(photo) for photo in data['photos']]
    media[0].caption = text

    # Send listing to user
    bot.send_media_group(chat_id, media)

    # Send listing to group
    bot.send_media_group(GROUP_ID, media)

    # Clear data after sending
    user_data.pop(chat_id, None)


@bot.callback_query_handler(func=lambda call: call.data == "send_to_group")
def send_to_group(call):
    chat_id = call.message.chat.id
    send_post(GROUP_ID)
    bot.send_message(chat_id, "✅ Post sent to group!")

    # Clean up user data after sending the post
    user_data.pop(chat_id, None)


bot.polling(none_stop=True)
