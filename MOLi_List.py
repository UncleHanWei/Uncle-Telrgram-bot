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
    global nowCmd
    content_type, chat_type, chat_id = telepot.glance(msg)
    # print(content_type, chat_type, chat_id)
    # print(msg)
    # if content_type == 'text':
    # bot.sendMessage(chat_id, msg['text'])
    # bot.sendMessage(chat_id, 'Hi')
    if nowCmd == '/new' :
        # 把收到的使用者訊息分成 list 再存入清單
        tmp = msg['text'].split('\n')
        # 檢查輸入的資料
        for i in tmp :
            if i not in myRead() :
                myWrite(i)
                bot.sendMessage(chat_id, 'done', reply_to_message_id = msg['message_id'])
            else :
                bot.sendMessage(chat_id, i + ' is already in the list !', reply_to_message_id = msg['message_id'])
        nowCmd = ''
    
    elif nowCmd == '/delete' :
        tmp = msg['text'].split('\n')
        for i in tmp :
            if i in myRead() :
                myDel(i)
                bot.sendMessage(chat_id, 'done', reply_to_message_id = msg['message_id'])
            else :
                bot.sendMessage(chat_id, i + ' is not in the list !', reply_to_message_id = msg['message_id'])
        nowCmd = ''
    
    else:
        if msg['text'] == '/list' :
            bot.sendMessage(chat_id, 'Here it is', reply_to_message_id = msg['message_id'])
            bot.sendMessage(chat_id, myRead())
        
        if msg['text'] == '/new' :
            nowCmd = '/new'
            bot.sendMessage(chat_id, 'now please send me items you want to add')
        
        if msg['text'] == '/delete':
            nowCmd = '/delete'
            bot.sendMessage(chat_id, 'now please send me items you want to delete')

nowCmd = ''
myFile = open('TOKEN.txt')
TOKEN = myFile.read().strip()
# TOKEN = lines[0]
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)