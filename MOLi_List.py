import time
import telepot
from telepot.loop import MessageLoop

# content of the automatic reply
def myDel(message) :
    MOLi_list = open('MOLi_list.txt', mode = 'r+', encoding = 'utf8')
    allList = MOLi_list.readlines()
    MOLi_list.seek(0)
    for i in allList :
        if i.strip() != message :
            MOLi_list.write(i)
    MOLi_list.truncate()
    MOLi_list.close()

def myWrite(message) :
    MOLi_list = open('MOLi_list.txt', mode = 'a+', encoding = 'utf8')
    MOLi_list.write('\n' + message.replace('MOLi_new', '').replace(' ', ''))
    MOLi_list.close()


def myRead() :
    MOLi_list = open('MOLi_list.txt', mode = 'r', encoding = 'utf8')
    allList = MOLi_list.readlines()
    message = ''
    for i in allList :
        message = message + i
    MOLi_list.close()
    return message

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # print(content_type, chat_type, chat_id)
    # print(msg)
    # if content_type == 'text':
    # bot.sendMessage(chat_id, msg['text'])
    # bot.sendMessage(chat_id, 'Hi')


    if msg['text'] == 'MOLi_list' :
        bot.sendMessage(chat_id, 'Here it is', reply_to_message_id = msg['message_id'])
        bot.sendMessage(chat_id, myRead())
    if 'MOLi_new' in msg['text'] :
        if msg['text'].replace('MOLi_new', '').replace(' ', '') not in myRead() :
            myWrite(msg['text'])
            bot.sendMessage(chat_id, 'done', reply_to_message_id = msg['message_id'])
        else :
            bot.sendMessage(chat_id, 'It\'s already in the list !', reply_to_message_id = msg['message_id'])
    if 'MOLi_del' in msg['text'] :
        if msg['text'].replace('MOLi_del', '').replace(' ', '') in myRead() :
            myDel(msg['text'].replace('MOLi_del', '').replace(' ', ''))
            bot.sendMessage(chat_id, 'done', reply_to_message_id = msg['message_id'])
        else :
            bot.sendMessage(chat_id, 'It\'s not in the list !', reply_to_message_id = msg['message_id'])


myFile = open('TOKEN.txt')
TOKEN = myFile.read()
# TOKEN = lines[0]
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)