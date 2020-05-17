import telebot
from telebot import types

import config
import sqlite3
import time
import dialogs
import database
import images

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_proj(message):
    bot.send_message(message.chat.id, "Введите имя")
    bot.register_next_step_handler(message, start_message)


@bot.message_handler(content_types=['text'])
def start_message(message):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    bot.send_message(message.chat.id, f"Привет, {message.text}, Если вы не робот, напишите что-нибудь")
    name = message.text
    c.execute('INSERT INTO login(name) values (?)', (name,))
    conn.commit()

    conn.close()
    bot.register_next_step_handler(message, welcome_to_start)


def welcome_to_start(message):
    bot.register_next_step_handler(message, first)
    bot.send_photo(message.chat.id, images.poster)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Начать игру")
    markup.add(button1)
    bot.send_message(message.chat.id, database.welcome, reply_markup=markup)


def first(message):
    if message.text == 'Начать игру' or 'Начать заново':
        bot.register_next_step_handler(message, talk_with_policeman)
        bot.send_photo(message.chat.id, images.first_image)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Начать диалог с офицером")
        button2 = types.KeyboardButton("Послать его")

        markup.add(button1, button2)
        bot.send_message(message.chat.id, dialogs.greeting, reply_markup=markup)


def talk_with_policeman(message):
    if message.text == 'Начать диалог с офицером':
        bot.register_next_step_handler(message, look_or_die)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Осмотреться")
        button2 = types.KeyboardButton("Начать паниковать, кричать и звать на помощь")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, dialogs.dialog_with_police1)
        time.sleep(7)
        bot.send_photo(message.chat.id, images.second_image)
        bot.send_message(message.chat.id, dialogs.an_accident, reply_markup=markup)
        time.sleep(5)
    if message.text == 'Послать его':
        bot.register_next_step_handler(message, look_or_die)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Осмотреться")
        button2 = types.KeyboardButton("Начать паниковать, кричать и звать на помощь")
        markup.add(button1, button2)

        bot.send_message(message.chat.id, dialogs.dialog_with_police2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_with_police3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_with_police4)
        time.sleep(8)
        bot.send_photo(message.chat.id, images.second_image)
        bot.send_message(message.chat.id, dialogs.an_accident, reply_markup=markup)
        time.sleep(10)


def look_or_die(message):
    if message.text == 'Осмотреться':
        bot.register_next_step_handler(message, test)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = 'В кухню'
        button2 = 'В гостинную'
        markup.add(button1, button2)

        bot.send_message(message.chat.id, dialogs.look_around1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.go_to_police1)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.oficer_dead)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.go_to_police2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.headshot1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.headshot2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.shoot_sound)
        time.sleep(15)
        bot.send_photo(message.chat.id, images.go_away)
        bot.send_message(message.chat.id, dialogs.lucky_Lee)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.second_image_1)

        bot.send_message(message.chat.id, dialogs.choose_the_way, reply_markup=markup)
        time.sleep(5)

    if message.text == 'Начать паниковать, кричать и звать на помощь':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = "Начать заново"
        markup.row(button1)

        bot.send_message(message.chat.id, dialogs.dont_be_panic)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.fail_Lee)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.game_over, reply_markup=markup)
        time.sleep(5)


def test(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = 'Я не чудовище'
    button2 = 'Ты в порядке?'
    button3 = 'Кто это?'
    markup.add(button1, button2, button3)

    if message.text == 'В кухню' or 'Начать с последней точки сохранения':
        bot.register_next_step_handler(message, cont_d2)

        bot.send_message(message.chat.id, dialogs.go_to_the_kitchen)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set3, reply_markup=markup)
        time.sleep(5)
    if message.text == 'В гостинную':
        bot.register_next_step_handler(message, cont_d2)

        bot.send_message(message.chat.id, dialogs.children_picture)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.parents_situation1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.parents_situation2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.parents_situation3)
        bot.send_message(message.chat.id, 'Вы узнали что случилось с родителями ребёнка.')
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.reaction_to_ps)
        time.sleep(5)
        bot.send_message(message.chat.id, 'Ли: Теперь кухня.')
        bot.send_message(message.chat.id, dialogs.go_to_the_kitchen)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set2)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.hello_radio)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set3, reply_markup=markup)
        time.sleep(5)


def cont_d2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = 'Ты в безопасности?'
    button2 = 'Где ты?'
    markup.add(button1, button2)

    if message.text == 'Я не чудовище':
        bot.register_next_step_handler(message, cont_d2_1)

        bot.send_message(message.chat.id, dialogs.Lee_not_monster)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set6)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set7, reply_markup=markup)
        time.sleep(5)
    if message.text == 'Ты в порядке?':
        bot.register_next_step_handler(message, cont_d2_1)

        bot.send_message(message.chat.id, dialogs.are_u_ok)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set6)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set7, reply_markup=markup)
        time.sleep(5)
    if message.text == 'Кто это?':
        bot.register_next_step_handler(message, cont_d2_1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = 'Ты в безопасности?'
        button2 = 'Где ты?'
        markup.add(button1, button2)

        bot.send_message(message.chat.id, 'Голос с рации: Меня зовут Клементина и я здесь живу.')
        bot.send_message(message.chat.id, dialogs.radio_set5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set6)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.radio_set7, reply_markup=markup)
        time.sleep(5)


def cont_d2_1(message):
    if message.text == 'Ты в безопасности?' or 'Где ты?':
        bot.register_next_step_handler(message, next_s)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = 'Поищем помощь пока не стемнело'
        button2 = 'Уйдём отсюда как только сядет солнце'
        markup.add(button1, button2)

        bot.send_message(message.chat.id, dialogs.clever_Klem)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.fifth_image)
        bot.send_message(message.chat.id, dialogs.scream_Klementine1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.scream_Klementine2)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.fourth_image)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.hammer)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_Lee_Klem1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_Lee_Klem2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_Lee_Klem3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_Lee_Klem4)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.first_meet_with_Klem)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_Lee_Klem5, reply_markup=markup)
        time.sleep(5)


def next_s(message):
    if message.text == 'Поищем помощь пока не стемнело':
        bot.register_next_step_handler(message, go_to_farm)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sidelka = '..её сиделка'
        sosed = '..её сосед'
        nikto = '..просто прохожий'
        markup.row(sidelka, sosed, nikto)

        bot.send_message(message.chat.id, dialogs.Chet_alive)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Shon_and_Chet1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Shon_and_Chet2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Shon_and_Chet3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Shon_and_Chet4)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.Shon)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Shon_and_Chet5)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.Chet)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Shon_and_Chet6)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Lee_is_not_father, reply_markup=markup)
        time.sleep(5)
    if message.text == 'Уйдём отсюда как только сядет солнце':
        bot.register_next_step_handler(message, stupid_attack)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = 'Напасть на него'
        button2 = 'Медленно выйти с поднятыми руками'
        button3 = 'Крикнуть: Не стреляйте, прошу!'
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, dialogs.Chet_not_alive)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Lee_and_Klem1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Lee_and_Klem2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Lee_and_Klem3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Lee_and_Klem4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.night)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.at_night)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me3)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.will_we_die)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me5, reply_markup=markup)
        time.sleep(5)


def stupid_attack(message):
    if message.text == 'Напасть на него':
        bot.register_next_step_handler(message, test)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = 'Начать c последней точки сохранения'
        markup.row(button1)
        bot.send_message(message.chat.id, dialogs.stupid_attack1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.stupid_attack2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.stupid_attack3, reply_markup=markup)
        time.sleep(5)

    if message.text == 'Медленно выйти с поднятыми руками':
        bot.register_next_step_handler(message, go_to_farm_2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = '..её сиделка'
        button2 = '..её сосед'
        button3 = '..просто прохожий'
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me6)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me7)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me9)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me10)
        bot.send_photo(message.chat.id, images.Shon_Andre)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.acquaintance1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.acquaintance2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.acquaintance3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.acquaintance4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Lee_is_not_father, reply_markup=markup)
        time.sleep(5)

    if message.text == 'Крикнуть: Не стреляйте, прошу!':
        bot.register_next_step_handler(message, go_to_farm_2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = '..её сиделка'
        button2 = '..её сосед'
        button3 = '..просто прохожий'
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, 'Ли: Не стреляйте! Я мирный!')
        time.sleep(5)
        bot.send_message(message.chat.id, 'Незнакомец: Медленно выходи с поднятыми руками!')
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me6)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.hands_up)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me7)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me9)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dont_shoot_me10)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.Shon_Andre)
        bot.send_message(message.chat.id, dialogs.acquaintance1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.acquaintance2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.acquaintance3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.acquaintance4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Lee_is_not_father, reply_markup=markup)


def go_to_farm_2(message):
    bot.register_next_step_handler(message, in_the_farm2_2)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = 'Хорошо, спасибо вам за помощь'
    markup.add(button1)

    if message.text == '..просто прохожий':
        bot.send_message(message.chat.id, dialogs.be_quick_2)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.zombie_Chet)
        bot.send_message(message.chat.id, dialogs.is_it_Chet1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.is_it_Chet2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm1_2_1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm1_2_2)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.bye_Andre)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm1)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.Hershel)
        bot.send_message(message.chat.id, dialogs.Chet_dead1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Chet_dead2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Chet_dead3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm4)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.at_the_farm)
        bot.send_message(message.chat.id, dialogs.foot_Lee1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee5, reply_markup=markup)
        time.sleep(10)
        bot.send_photo(message.chat.id, images.sleep)
        time.sleep(5)
    if message.text == '..её сосед':
        bot.send_message(message.chat.id, dialogs.be_quick_2)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.zombie_Chet)
        bot.send_message(message.chat.id, dialogs.is_it_Chet1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.is_it_Chet2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm1_2_1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm1_2_2)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.bye_Andre)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Chet_dead1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Chet_dead2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Chet_dead3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.not_father1)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.at_the_farm)
        bot.send_message(message.chat.id, dialogs.foot_Lee1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee5, reply_markup=markup)
        time.sleep(10)
        bot.send_photo(message.chat.id, images.sleep)
        time.sleep(5)
    if message.text == '..её сиделка':
        bot.send_message(message.chat.id, dialogs.be_quick_2)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.zombie_Chet)
        bot.send_message(message.chat.id, dialogs.is_it_Chet1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.is_it_Chet2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm1_2_1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm1_2_2)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.bye_Andre)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Chet_dead1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Chet_dead2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Chet_dead3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.not_father2)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.at_the_farm)
        bot.send_message(message.chat.id, dialogs.foot_Lee1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee5, reply_markup=markup)
        time.sleep(10)
        bot.send_photo(message.chat.id, images.sleep)
        time.sleep(10)


def go_to_farm(message):
    bot.register_next_step_handler(message, in_the_farm2)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = 'Я видел мёртвых людей, ходячих.'
    button2 = 'Я видел как мёртвый коп полз по земле.'
    markup.add(button1, button2)

    if message.text == '..просто прохожий':
        bot.send_message(message.chat.id, dialogs.be_quick)
        bot.send_photo(message.chat.id, images.be_quick)
        time.sleep(15)
        bot.send_photo(message.chat.id, images.bye_Chet)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm1)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.Hershel)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm3)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.at_the_farm)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.zombies_are_coming1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.zombies_are_coming2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.zombies_are_coming3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.zombies_are_coming4, reply_markup=markup)
        bot.send_photo(message.chat.id, images.about_zombies)
        time.sleep(10)

    if message.text == '..её сосед':
        bot.send_message(message.chat.id, dialogs.be_quick)
        bot.send_photo(message.chat.id, images.be_quick)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.bye_Chet)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm1)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.Hershel)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm3)
        bot.send_photo(message.chat.id, images.at_the_farm)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.not_father1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.zombies_are_coming1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.zombies_are_coming2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.zombies_are_coming3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.zombies_are_coming4, reply_markup=markup)
        bot.send_photo(message.chat.id, images.about_zombies)
        time.sleep(10)

    if message.text == '..её сиделка':
        bot.send_message(message.chat.id, dialogs.be_quick)
        bot.send_photo(message.chat.id, images.be_quick)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.bye_Chet)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm1)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.Hershel)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.welcome_to_farm3)
        bot.send_photo(message.chat.id, images.at_the_farm)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.not_father2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.zombies_are_coming1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.zombies_are_coming2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.zombies_are_coming3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.zombies_are_coming4, reply_markup=markup)
        bot.send_photo(message.chat.id, images.about_zombies)
        time.sleep(10)


def in_the_farm2_2(message):
    if message.text == 'Хорошо, спасибо вам за помощь':
        bot.register_next_step_handler(message, in_the_farm3)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = 'Дак?'
        button2 = 'Не слушается, или крякает?'
        button3 = 'Когда еще родители называли своих детей Дак?'
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, dialogs.meeting_Kenny1)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.first_meet_with_Kenny)
        bot.send_message(message.chat.id, dialogs.meeting_Kenny2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.meeting_Kenny3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.meeting_Kenny4)
        time.sleep(10)
        bot.send_message(message.chat.id, dialogs.meeting_Kenny5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.meeting_Kenny6)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_is_my_name1)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.first_meet_with_Dac)
        bot.send_message(message.chat.id, dialogs.Dac_is_my_name2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_is_my_name3, reply_markup=markup)
        time.sleep(10)


def in_the_farm2(message):
    if message.text == 'Я видел мёртвых людей, ходячих.' or 'Я видел как мёртвый коп полз по земле.':
        bot.register_next_step_handler(message, in_the_farm3)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = 'Дак?'
        button2 = 'Не слушается, или крякает?'
        button3 = 'Когда еще родители называли своих детей Дак?'
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, dialogs.still_not_trusting1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.foot_Lee5)
        bot.send_photo(message.chat.id, images.sleep)
        time.sleep(10)
        bot.send_message(message.chat.id, dialogs.meeting_Kenny1)
        bot.send_photo(message.chat.id, images.first_meet_with_Kenny)
        bot.send_message(message.chat.id, dialogs.meeting_Kenny2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.meeting_Kenny3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.meeting_Kenny4)
        time.sleep(10)
        bot.send_message(message.chat.id, dialogs.meeting_Kenny5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.meeting_Kenny6)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_is_my_name1)
        bot.send_photo(message.chat.id, images.first_meet_with_Dac)
        bot.send_message(message.chat.id, dialogs.Dac_is_my_name2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_is_my_name3, reply_markup=markup)
        time.sleep(10)


def in_the_farm3(message):
    bot.register_next_step_handler(message, talk_with_wife_Kenny)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = 'К Клементине и жене Кенни[ДОП]'
    button2 = 'Пойти в хлев[СЮЖЕТ]'
    button3 = 'Подойти к Кенни[ДОП]'
    markup.add(button1, button2, button3)

    if message.text == 'Дак?':
        bot.send_message(message.chat.id, dialogs.Dac_is_my_name4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_is_my_name5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.is_it_racism)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Kennys_wife)
        bot.send_photo(message.chat.id, images.first_meet_with_wife)
        bot.send_message(message.chat.id, dialogs.build_fence)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.come_Shon)
        bot.send_message(message.chat.id, dialogs.Dac_and_Shon1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_and_Shon2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_and_Shon3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_and_Shon4, reply_markup=markup)
        time.sleep(5)

    if message.text == 'Не слушается, или крякает?':
        bot.send_message(message.chat.id, dialogs.Joke_Dac_name)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_is_my_name5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.is_it_racism)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Kennys_wife)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.first_meet_with_wife)
        bot.send_message(message.chat.id, dialogs.build_fence)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.come_Shon)
        bot.send_message(message.chat.id, dialogs.Dac_and_Shon1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_and_Shon2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_and_Shon3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_and_Shon4, reply_markup=markup)
        time.sleep(5)

    if message.text == 'Когда еще родители называли своих детей Дак?':
        bot.send_message(message.chat.id, dialogs.Dac_name)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_is_my_name5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.is_it_racism)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Kennys_wife)
        bot.send_photo(message.chat.id, images.first_meet_with_wife)
        bot.send_message(message.chat.id, dialogs.build_fence)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.come_Shon)
        bot.send_message(message.chat.id, dialogs.Dac_and_Shon1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_and_Shon2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_and_Shon3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_and_Shon4, reply_markup=markup)
        time.sleep(10)


def talk_with_wife_Kenny(message):
    if message.text == 'К Клементине и жене Кенни[ДОП]':
        bot.register_next_step_handler(message, talk_with_wife_Kenny_2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go_to_hlev = 'Пойти в хлев[СЮЖЕТ]'
        go_to_Kenny = 'Подойти к Кенни[ДОП]'
        markup.add(go_to_hlev, go_to_Kenny)
        bot.send_message(message.chat.id, dialogs.wife_and_Klem1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.wife_and_Klem2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.wife_and_Klem3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.wife_and_Klem4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.wife_and_Klem5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.wife_and_Klem6, reply_markup=markup)
        time.sleep(5)

    if message.text == 'Подойти к Кенни[ДОП]':
        bot.register_next_step_handler(message, talk_with_wife_Kenny_2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go_to_khlev = 'Пойти в хлев[СЮЖЕТ]'
        go_to_wife = 'К Клементине и жене Кенни[ДОП]'
        markup.add(go_to_khlev, go_to_wife)
        bot.send_message(message.chat.id, dialogs.talk_with_Kenny1)
        bot.send_photo(message.chat.id, images.help_Kenny)
        bot.send_message(message.chat.id, dialogs.talk_with_Kenny2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.talk_with_Kenny3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.talk_with_Kenny4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.talk_with_Kenny5, reply_markup=markup)
        time.sleep(5)

    if message.text == 'Пойти в хлев[СЮЖЕТ]':
        bot.register_next_step_handler(message, continue_story_2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        yes = 'Да, конечно.'
        no = 'Занимайся своим делом.'
        ok = 'Какой?'
        markup.add(yes, no, ok)
        bot.send_photo(message.chat.id, images.in_khlev)
        bot.send_message(message.chat.id, dialogs.dialog_with_Hershel1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_with_Hershel2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_with_Hershel3, reply_markup=markup)
        time.sleep(10)


def talk_with_wife_Kenny_2(message):
    if message.text == 'К Клементине и жене Кенни[ДОП]' or 'Подойти к Кенни[ДОП]':
        bot.register_next_step_handler(message, continue_story)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go_to_hlev = 'Пойти в хлев[СЮЖЕТ]'
        markup.add(go_to_hlev)
        bot.send_message(message.chat.id, dialogs.wife_and_Klem1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.wife_and_Klem2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.wife_and_Klem3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.wife_and_Klem4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.wife_and_Klem5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.wife_and_Klem6, reply_markup=markup)
        time.sleep(5)

    if message.text == 'Подойти к Кенни[ДОП]':
        bot.register_next_step_handler(message, continue_story)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go_to_khlev = 'Пойти в хлев[СЮЖЕТ]'
        markup.add(go_to_khlev)
        bot.send_message(message.chat.id, dialogs.talk_with_Kenny1)
        bot.send_photo(message.chat.id, images.help_Kenny)
        bot.send_message(message.chat.id, dialogs.talk_with_Kenny2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.talk_with_Kenny3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.talk_with_Kenny4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.talk_with_Kenny5, reply_markup=markup)
        time.sleep(10)


def continue_story(message):
    bot.register_next_step_handler(message, continue_story_2)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes = 'Да, конечно.'
    no = 'Занимайся своим делом.'
    ok = 'Какой?'
    markup.add(yes, no, ok)
    if message.text == 'Пойти в хлев[СЮЖЕТ]':
        bot.send_photo(message.chat.id, images.in_khlev)
        bot.send_message(message.chat.id, dialogs.dialog_with_Hershel1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_with_Hershel2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_with_Hershel3, reply_markup=markup)
        time.sleep(10)


def continue_story_2(message):
    bot.register_next_step_handler(message, Dac_or_Shon)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    save_Shon = 'Помочь Шону'
    save_Dac = 'Помочь Даку'
    markup.add(save_Shon, save_Dac)

    if message.text == 'Да, конечно.' or 'Какой?':
        bot.send_message(message.chat.id, dialogs.dialog_with_Hershel4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_with_Hershel5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_with_Hershel6)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.shon_scream1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.shon_scream2)
        bot.send_photo(message.chat.id, images.Shon_Scream)
        bot.send_message(message.chat.id, dialogs.shon_scream3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.shon_scream4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_or_Shon1)
        bot.send_photo(message.chat.id, images.Shon_or_Dac)
        bot.send_message(message.chat.id, dialogs.Dac_or_Shon2, reply_markup=markup)
        time.sleep(10)

    if message.text == 'Занимайся своим делом':
        bot.send_message(message.chat.id, dialogs.dialog_with_Hershel)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_with_Hershel4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.dialog_with_Hershel5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.shon_scream1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.shon_scream2)
        bot.send_photo(message.chat.id, images.Shon_Scream)
        bot.send_message(message.chat.id, dialogs.shon_scream3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.shon_scream4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.Dac_or_Shon1)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.Shon_or_Dac)
        bot.send_message(message.chat.id, dialogs.Dac_or_Shon2, reply_markup=markup)
        time.sleep(10)


def Dac_or_Shon(message):
    bot.register_next_step_handler(message, end_of_the_game)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sorry_Hershel = 'Мне жаль'
    paniced = 'Я запаниковал'
    both = 'Я думал что помогу им обоим'
    markup.add(sorry_Hershel, paniced, both)
    if message.text == 'Помочь Шону':
        bot.send_message(message.chat.id, dialogs.help_Shon1)
        bot.send_photo(message.chat.id, images.help_Shon1)
        bot.send_message(message.chat.id, dialogs.help_Shon2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.help_Shon3)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.help_Shon2)
        bot.send_message(message.chat.id, dialogs.help_Shon4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.help_Shon5)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.help_Shon6)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.help_Shon7)
        bot.send_photo(message.chat.id, images.Shon_dead)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.help_Shon8)
        bot.send_photo(message.chat.id, images.killer_Hershel)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.angry_Hershel1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.angry_Hershel2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.angry_Hershel3)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.Kenny_styd)
        bot.send_message(message.chat.id, dialogs.angry_Hershel4)
        time.sleep(5)
        bot.send_message(message.chat.id, 'Кенни запомнил ваш выбор.', reply_markup=markup)
        time.sleep(10)

    if message.text == 'Помочь Даку':
        bot.send_message(message.chat.id, dialogs.help_Dac1)
        bot.send_photo(message.chat.id, images.help_Dac)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.help_Dac2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.help_Dac3)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.help_Dac4)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.Shon_dead)
        bot.send_message(message.chat.id, dialogs.help_Shon8)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.killer_Hershel)
        bot.send_message(message.chat.id, dialogs.angry_Hershel1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.angry_Hershel2)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.angry_Hershel3)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.Kenny_styd)
        bot.send_message(message.chat.id, dialogs.angry_Hershel5)
        time.sleep(5)
        bot.send_message(message.chat.id, 'Кенни запомнил ваш выбор.', reply_markup=markup)
        time.sleep(10)


def end_of_the_game(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    game_over = 'Завершить игру!'
    markup.add(game_over)
    if message.text == 'Мне жаль' or 'Я запаниковал' or 'Я думал что помогу им обоим':
        bot.send_message(message.chat.id, dialogs.angry_Hershell)
        bot.send_photo(message.chat.id, images.bye_Hershel)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.the_end1)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.the_end2)
        bot.send_photo(message.chat.id, images.hello_Maicon1)
        bot.send_message(message.chat.id, dialogs.the_end3)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.hello_Maicon2)
        bot.send_message(message.chat.id, dialogs.the_end4)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.the_end5)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.hello_Maicon2)
        bot.send_message(message.chat.id, dialogs.the_end6)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.who_is_it)
        bot.send_message(message.chat.id, dialogs.the_end7)
        time.sleep(5)
        bot.send_photo(message.chat.id, images.is_Dac_dead)
        time.sleep(5)
        bot.send_message(message.chat.id, dialogs.the_end8, reply_markup=markup)
        bot.send_photo(message.chat.id, images.the_end)


bot.polling()