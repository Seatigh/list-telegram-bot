#IMPORTS
#import logging
import sys
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler

# ERRORS
initList_error = "Can't create the list. It already exists."
print_error = "Can't print the list. It doesn't exist."
add_error = "Can't add the task. The list doesn't exist."
removeTask_error = "Can't remove task from list. The list doesn't contain that task."

master_list = []
task_counter = 0

updater = Updater(token = '415067513:AAHA_qC7AnYLg58R51laH7EX_V0MXWXaRfc')
dispatcher = updater.dispatcher

class Task:
	def __init__(self, message):
		global task_counter
		self.id = task_counter
		task_counter += 1
		self.message = message

class List:
	def __init__(self, name):
		print("==INIT LIST==", flush = True)
		for l in master_list:
			if name == l.name:
				print("\t>"initList_error + " (List \'" + str(name) + "\')")
				return False
		self.name = name
		print("\t>name gived")
		self.id = len(master_list)
		print("\t>id gived")
		self.tasks = []
		print("\t>tasks list created")
		master_list.append(self)
		print("\t>list appended")

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

#############
# FUNCTIONS #
#############

def start(bot, update):
	print(">Starded")
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
	print(">New list called. Master list size: " + str(len(master_list)))
	new_list = List(args[0].title())
	bot.send_message(chat_id = update.message.chat_id, text = "List *" + args[0].title() + "* has been created!\nUse /addtask command to add some tasks.", parse_mode = ParseMode.MARKDOWN)

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
print("COOL LIST BOT RUNNING...")

while True:
	pass
#updater.stop()