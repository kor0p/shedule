import telebot
from telebot import types
from datetime import date,datetime
import calendar
import random
k = date.today().weekday()
now = datetime.now()
token = '421515612:AAEhjzBeFxj4HVrclIJscEPw_JJKPtrKwf4'
bot = telebot.TeleBot(token)
what_time = []
j=o=0
shedule = [['англи','захисту','історії','геометрії','фіз-ри','заруби','біології'],
['алгебри.1/інфи','алгебри.2/фізики','англи','англи','фізики/алгебри.1','інфи/алгебри.2'],
['фізики','фізики','біології','укр літ','алгебри.1','алгебри.2','англи'],
['художньої','мови','фізики','алгебри.1','алгебри.2','історії','економіки'],
['фізики.1/геометрії.1','фізики.1/геометрії.2','геометрії.1/фізики.1','геометрії.2/фізики.2','англи','фіз-ри','укр літ'],
['інфи','хімії','історії','мови','фізики']]
weekdays = ['Понеділок','Вівторок','Середа','Четвер','П\'ятниця','Субота','Неділя']

def w_time():
	start = [[8,45],[9,40],[10,35],[11,40],[12,50],[14,0],[14,55],[0,0]]
	end = [[9,30],[10,25],[11,20],[12,25],[13,35],[14,45],[15,40],[0,0]]
	now = datetime.now()
	if weekdays[k] != 'Неділя' :
		lessons_num = len(shedule[k])
		if weekdays[k] == 'Субота' :
			start = [[8,45],[9,40],[10,35],[11,30],[12,25],[23,59]]
			end = [[9,30],[10,25],[11,20],[12,15],[13,10],[23,59]]
		s,e = [],[]
		time = now.hour*60+now.minute
		for i in range(lessons_num + 1):
			start[i] = start[i][0]*60+start[i][1]-1
			end[i] = end[i][0]*60+end[i][1]-1
			s.append(start[i]-time)
			e.append(end[i]-time)
		def t(j,a):
			wtime=['До початку %s залишилось %s:%s:%s' % (shedule[k][j],s[j]//60,s[j]%60,60 - now.second),
			'До кінця %s залишилось %s:%s:%s' % (shedule[k][j],e[j]//60,e[j]%60,60 - now.second),
			'До кінця %s залишилось %s:%s:%s\nДо початку %s залишилось %s:%s:%s' % (
			shedule[k][j],e[j]//60,e[j]%60,60 - now.second,shedule[k][j+1],s[j+1]//60,s[j+1]%60,60 - now.second)]
			what_time.append(wtime[a])
		for i in range(lessons_num):
			if 0<e[i]<45 and i < lessons_num:
				t(i,2)
			elif i == lessons_num and e[i] > 0:
				t(i,1)
			elif e[i]<0 and 0<s[i]<25 or (i == 0 and s[0] > 0):
				t(i,0)
			elif i==lessons_num and (e[i] < 0 or s[0] > 60):
				what_time.append('До початку наступного уроку ще довго')
	else:
		what_time.append('До початку наступного уроку ще довго')
	print(what_time[-1])
	return what_time[-1]
def time():
	global o
	now=datetime.now()
	td='%s %s.%s'% (weekdays[k],k+1,now.month+1)
	o+=random.randint(1,5)
	if o % 10 != 0:
		td = ''
	return '%s\n%s:%s:%s' % (td,now.hour,now.minute,now.second)
@bot.message_handler(commands=['t','start',' ',''])
def any_msg(m):
	o = 0
	keyboard = types.InlineKeyboardMarkup()
	callback_button = types.InlineKeyboardButton(text="Час", callback_data="test")
	keyboard.add(callback_button)
	bot.send_message(-1001158158821,'%s %s : %s'% (m.chat.first_name,m.chat.last_name,m.text))
	bot.send_message(m.chat.id, '%s\n%s' % (time(),w_time()), reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		if call.data == "test":
			o = 0
			keyboard = types.InlineKeyboardMarkup()
			callback_button = types.InlineKeyboardButton(text="Час", callback_data="test")
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
			text=time())
			keyboard.add(callback_button)
			bot.send_message(-1001158158821,'%s %s'% (call.message.chat.first_name,call.message.chat.last_name))
			bot.send_message(call.message.chat.id, w_time(), reply_markup=keyboard)
if __name__ == '__main__':
		bot.polling(none_stop=True)