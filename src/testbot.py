#IMPORTS
#import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler

# ERRORS
initList_error = "Can't create the list. It already exists."
print_error = "Can't print the list. It doesn't exist."
add_error = "Can't add the task. The list doesn't exist."
removeTask_error = "Can't remove task from list. The list doesn't contain that task."

master_list = []
task_counter = 0

updater = Updater(token = 'TOKEN')
dispatcher = updater.dispatcher

def start(bot, update):
	bot.send_message(chat_id = update.message.chat_id, text = "I\'m a bot, please talk to me!")

def echo(bot, update):
	bot.send_message(chat_id = update.message.chat_id, text = update.message.text)

def caps(bot, update, args):
	text_caps = ' '.join(args).upper()
	bot.send_message(chat_id = update.message.chat_id, text = text_caps)

def inline_caps(bot, update):
	query = update.inline_query.query
	if not query:
		return
	results = list()
	results.append(InlineQueryResultArticle(id = query.upper(), title = 'Caps', input_message_content = InputTextMessageContent(query.upper())))
	bot.answer_inline_query(update.inline_query.id, results)

def unknown(bot, update):
	bot.send_message(chat_id = update.message.chat_id, text = "Sorry, I didn\'t understand that command.")

def newlist(bot, update, args):
	list_name = ' '.join(args).title()
	new_list = List(list_name)
	if not new_list:
		bot.send_message(chat_id = update.message.chat_id, text = "List *" + list_name + "* already exists.", parse_mode = ParseMode.MARKDOWN)
		return
	bot.send_message(chat_id = update.message.chat_id, text = "List *" + list_name + "* has been created!\nUse /addtask command to add some tasks.", parse_mode = ParseMode.MARKDOWN)

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps, pass_args = True)
inline_caps_handler = InlineQueryHandler(inline_caps)
unknown_handler = MessageHandler(Filters.command, unknown)
newlist_handler = CommandHandler('newlist', newlist, pass_args = True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(inline_caps_handler)
dispatcher.add_handler(newlist_handler)

dispatcher.add_handler(unknown_handler) #Always add this handler the last one

updater.start_polling()
#updater.stop()

class Task:
	def __init__(self, message):
		global task_counter
		self.id = task_counter
		task_counter += 1
		self.message = message

class List:
	def __init__(self, name):
		for l in master_list:
			if name == l.name:
				print(initList_error + " (List \'" + str(name) + "\')")
				return False
		self.name = name
		self.id = len(master_list)
		self.tasks = []
		master_list.append(self)

	def printList(self):
		if self in master_list:
			print(self.tasks)
		else:
			print(print_error)

	def pprintList(self):
		if self in master_list:
			print("List " + str(self.id) + ":")
			for t in self.tasks:
				print("\t- " + str(t.message))
		else:
			print(print_error)

	def addTask(self, task):
		if self in master_list:
			self.tasks.append(task)
		else:
			print(add_error)

	def removeTask(self, id):
		for t in self.tasks:
			if t.id == id:
				self.tasks.remove(t)
				return
		print(removeTask_error)
