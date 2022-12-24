import telebot
from telebot import types
import time
import datetime
import requests
postdate=datetime.datetime.today().strftime("%Y-%m-%d  %H:%M:%S")
admin_pin=int(3112)
token = "1049906501:AAFgMq_1u1IofxgVnztgQPvIdHv_S4J5F-U"
bot = telebot.TeleBot(token)

#дані користувачів та адміна
admin=521734339
user0=302824429
admin_pin=str(3112)

#координати КПП
x=48.46704
y=24.998334



    

@bot.message_handler(commands=["all"])
def autorization(message):
    Pin = bot.send_message(message.chat.id, "Для продовження введіть пароль")
    bot.register_next_step_handler(Pin, every)


def every(message):
    iduser=message.from_user.id
    Pin = message.text
    if iduser==admin and Pin==admin_pin:
        outlog=open('log_file.txt','r')
        doc=open('database.txt','rb')
        bot.send_message(message.chat.id,'можете переглягути журал активності нижче')
        bot.send_document(admin, doc)
        bot.send_document(admin, outlog)
        outlog.close()
        doc.close()
    else:
        bot.send_message(message.chat.id, "Ви не можете використовувати дану команду")
           
    

    
@bot.message_handler(commands=["log"])#відкриває і надсилає адміну
def autorization(message):
    Pin = bot.send_message(message.chat.id, "Для продовження введіть пароль")
    bot.register_next_step_handler(Pin, outlog)

def outlog(message):
    Pin = message.text
    #iduser=message.from_user.id
    if iduser==admin and Pin==admin_pin:
        outlog=open('log_file.txt','r')
        bot.send_document(admin, outlog)
        outlog.close()
    else:
        bot.send_message(message.chat.id, "Ви не можете використовувати дану команду")


#геолокація(інтерфейс)
@bot.message_handler(commands=["open"])
def geo(message):
    
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Підтверджую", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Підтверджуєте, що надаєте згоду на обробку ваших даних?", reply_markup=keyboard)
    
#БД інтерфейс
@bot.message_handler(commands=["base"])
def autorization(message):
    Pin = bot.send_message(message.chat.id, "Для продовження введіть пароль")
    bot.register_next_step_handler(Pin, db)
    
    

#####
    
#БД (оперції)
def db(message):
    
    Pin = message.text
    if iduser==admin:
        if Pin==admin_pin:
            doc=open('database.txt','rb')
            pin = bot.send_message(message.chat.id,'можете переглягути журал активності нижче')
            bot.send_document(admin, doc)
        else:
            pin = bot.send_message(message.chat.id,"перевірти правильність комнади чи Pin")
    else:
        bot.send_document(admin, "ви не можете виконати цю команду")

@bot.message_handler(commands=['close'])
def closse(message): #записує все надіслане йому в файл
     response = requests.get('http://192.168.0.33/4/off')
     bot.send_message(message.chat.id,"доступ закрито")


@bot.message_handler(commands=['on'])
def closse(message): #записує все надіслане йому в файл
     response = requests.get('http://192.168.0.33/5/on')
     bot.send_message(message.chat.id,"світлодіод увімкнуто")
     

@bot.message_handler(commands=['off'])
def closse(message): #записує все надіслане йому в файл
     response = requests.get('http://192.168.0.33/5/off')
     bot.send_message(message.chat.id,"світлодіод вимкнуто")

@bot.message_handler(commands=['help'])
def closser(message): # команда хелп
    iduser=message.from_user.id
    if iduser==user0: 
        bot.send_message(message.chat.id,"Вітаю ось список усіх доступних відкритих команд:\n"
        "/on	Вмикання світлодіода\n"
        "/off	Вимкнення світлодіода\n" 
        "/open	Переведення замка в позицію відімкнуто\n" 
        "/close	Переведення замка в позицію замкнено\n"
        "/help	Виводить опис телеграм бота з функціями\n"
        )
    elif iduser==admin:
        bot.send_message(message.chat.id,"Вітаю ось список команд:\n"
        "/on	Вмикання світлодіода\n"
        "/off	Вимкнення світлодіода\n" 
        "/open	Переведення замка в позицію відімкнуто\n" 
        "/close	Переведення замка в позицію замкнено\n"
        "/help	Виводить опис телеграм бота з функціями\n"
        "/all	Надсилання двох файлів"  
        "/log	Надсилання файлу log_file.txt"
        "/base	Надсилання файлу database.txt"                        
        )
    else:
        bot.send_message(message.chat.id,"Мені шкода, але вам не доступний даний синтаксис")
        
                
    

       
#локація (операцій)
@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)

        idchat=message.chat.id
        iduser=message.from_user.id
        firstname=message.from_user.first_name
        lastname=message.from_user.last_name
        username=message.from_user.username
        long=str(message.location.longitude)
        lat=str(message.location.latitude)
        
        #пересилання запитів адміну
        bot.send_message(admin, postdate+' | '+username+' | '+str(iduser)+' | '+firstname+ ' [ '+long+'  '+lat+' ]')
        bd=open('database.txt', 'a')
        


        if iduser==admin or iduser==user0:
            bot.send_message(message.chat.id,  "Доступ дозволено")
          
            print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
            #bot.send_message(message.chat.id,  message.location.latitude) #довжина
            #bot.send_message(message.chat.id,  message.location.longitude) #ширина
            
            

            x1=message.location.latitude
            y1=message.location.longitude
            z1=x1+0.001
            z2=x1-0.001
            z3=y1+0.001
            z4=y1-0.001
            if z1<x or z2<x or z1==x or z2==x:
                if z3<y or z4<y or z3==y or z4==y:
                    bot.send_message(admin, "Доступ дозволено")
                    response = requests.get('http://192.168.0.33/4/on')
                    bd.write(postdate + ' | ' + username + ' | '+str(iduser)+ ' | '+firstname+' | '+ long+' '+lat+' | '+'ID дозволено '+' | '+'GEO дозволено'+'\n')
                    time.sleep(20)
                    response = requests.get('http://192.168.0.33/4/off')
                    bot.send_message(admin, "Доступ закрито")
                else:
                    bd.write(postdate + ' | ' + username + ' | '+str(iduser)+ ' | '+firstname+' | '+ long+' '+lat+' | '+'ID дозволено '+' | '+'GEO заборонено'+'\n')
            else:
                bd.write(postdate + ' | ' + username + ' | '+str(iduser)+ ' | '+firstname+' | '+ long+' '+lat+' | '+'ID заборонено '+ ' | '+'GEO заборонено'+'\n')
        else:
            bot.send_message(message.chat.id, "Доступ заборонено")
            bot.send_message(admin, "Доступ заборонено")
            bd.write(postdate + ' | ' + username +' | '+str(iduser)+ ' | '+firstname+' | '+ long+' '+lat+' | '+'ID Заборонено'+'|'+'GEO заборонено'+'\n')        

        bd.close()

        
##обовязково логування в кінці

@bot.message_handler(content_types=['text'])
def logger(message): #записує все надіслане йому в файл
    idchat=message.chat.id
    bot.send_message(message.chat.id, "вибачте, але я вас не розумію")
    mes=message.text
    iduser=message.from_user.id
    firstname=message.from_user.first_name
    log=open('log_file.txt', 'a')
    log.write(str(iduser)+'  '+firstname+' '+str(idchat)+' '+mes+' '+str(postdate)+'\n')

bot.polling()
