import json

file = open("../data/data.json", "r+")

list_struct = {
	"id": "",
	"chat": "",
	"name": "",
	"tasks": {}
}

list1 = list_struct
list1["name"] = "lista_1"
list1["id"] = 1
list1["chat"] = 1

list2 = list_struct
list2["name"] = "lista_2"
list2["id"] = 2
list2["chat"] = 2

json.dump(list1, file)
json.dump(list2, file)

print(list1)
print(list_struct)

class List:
	def __init__(self, _id, _name):
		self.id = _id
		self.name = _name


class Task:
	def __init__(self, _list, _id):
		self.list = _list
		self.id = _id
		self.description = ""

	def addDescription(self, _desc):
		if self.description == "":
			self.description = _desc
		else:
			add_input = input("The task has a description already. Wanna append or modify it?\n\ta > append\n\tm > modify\n")
			if add_input == "a":
				self.description += _desc
			elif add_input == "m":
				self.description = _desc
			else:
				print(add_input + " not alowed. Function aborted!")

file.close()