# -*- coding: UTF-8 -*-

import re
import itertools

arg = [
'/var/mobile/Applications/EE962478-374F-46A3-BAA9-6A276B8EB00D/Documents/grabArgs.py', 
'Project Done:\n\t- Task 01 @done\n\t\t- Subtask 1.01\n\t\tEste é um comentário malandro\n\t\t- Subtask 1.02\n\t\t\t- Subsubtask 1.01 @done\n\t\t\tEste é outro comentário malandro\n\t\t\t- Subsubtask 1.02\n\t\t\t\t- Subsubsubtask 1.01\n\t\t\t- Subsubtask 1.03\n\t\t- Subtask 1.03\n\t\t- Subtask 1.04\n\t- Task 02 @done\n\t\t- Subtask 2.01 @done\n\t\t- Subtask 2.02\n\t\t\t- Subsubtask 2.01 @done\n\t\t\t- Subsubtask 2.02\n\t\t\t\t- Subsubsubtask 2.01 @done\n\t\t\t- Subsubtask 2.03 @done\n\t\t- Subtask 2.03 @done\n\t\t- Subtask 2.04 @done\n\t- Task 03 @done\n\t\t- Subtask 3.01 @done\n\t\t- Subtask 3.02\n\t- Task 04 @done\n\t\t- Subtask 4.01 @done\n\t\t- Subtask 4.02 @done\n\t- Task 05 @done\n\t\t- Subtask 5.01 @done\n\t\t- Subtask 5.02 @done\n\t\t\t- Subsubtask 5.03 @done\n\t\t- Subtask 5.03 @done\n\t- Task 06 @done\n\t\t- Subtask 6.01\n\t\t\t- Subsubtask 6.01 @done\n\t\t\t- Subsubtask 6.02 @done\n\t\t- Subtask 6.02 @done\n\t- Task 07 @done\n\t\t- Subtask 7.01\n\t\t\t- Subsubtask 7.01 @done\n\t\t- Subtask 7.02\n\t\t\t- Subsubtask 7.02 @done\n\t- Task 08 @done\n\t\t- Subtask 8.01\n\t\t\t- Subsubtask 8.01 @done\n\t\t\t- Subsubtask 8.02\n\t\t\t\t- Subsubsubtask 8.01 @done\n\t\t\t\t- Subsubsubtask 8.02\n\t\t\t\t\t- Subsubsubsubtask 8.01 @done\n\t\t\t\t- Subsubsubtask 8.03 @done\n\t\t\t- Subsubtask 8.03 @done\n\t\t- Subtask 8.02 @done\n\t\t- Subtask 8.03\n\t\t\t- Subsubtask 8.04 @done\n\t\t\t- Subsubtask 8.05\n\t\t\t\t- Subsubsubtask 8.04\n\t\t\t\t\t- Subsubsubsubtask 8.02 @done\n\t\t\t- Subsubtask 8.06 @done\n\t- Task 09 @done\n\tThis is a comment\n\t\t- Subtask 9.01 @done\n\t\tThis is a subtask comment\n\t\t- Subtask 9.02\n\t\tAnother comment\n\t\t\t- Subsubtask 9.01 @done\n\t\t\t- Subsubtask 9.02 @done\n\t\t\tWhy so many comments?\n\t\t\t- Subsubtask 9.03\n\t\t\t\t- Subsubsubtask 9.01 @done\n\t\t\t\tJust another comment to break your code\n\t\t\t\t- Subsubsubtask 9.02\n\t\t\t\tBreak, break, break\n\t\t\t\t\t- Subsubsubsubtask 9.01 @done\n\t\t\t\t\tThis is the last comment, I promise\n\t\t\t\t- Subsubsubtask 9.03 @done\n\t\t\t\tI lied.\n\t\t\t- Subsubtask 9.04\n\t\t\t\t- Subsubsubtask 9.03 @done\n\t\t\t\tI love lying\n\t\t\t- Subsubtask 9.05 @done\n\t\t- Subtask 9.03 @done\n\t\tOk, this is truly the last comment.\n\t\tNah.',
'Project Done:\nThis is a project comment\n\t- Task 09\n\tThis is a comment\n\t\t- Subtask 9.01 @done\n\t\tThis is a subtask comment\n\t\t- Subtask 9.02\n\t\tAnother comment\n\t\t\t- Subsubtask 9.01 @done\n\t\t\t- Subsubtask 9.02 @done\n\t\t\tWhy so many comments?\n\t\t\t- Subsubtask 9.03\n\t\t\t\t- Subsubsubtask 9.01 @done\n\t\t\t\tJust another comment to break your code\n\t\t\t\t- Subsubsubtask 9.02\n\t\t\t\tBreak, break, break\n\t\t\t\t\t- Subsubsubsubtask 9.01 @done\n\t\t\t\t\tThis is the last comment, I promise\n\t\t\t\t- Subsubsubtask 9.03 @done\n\t\t\t\tI lied.\n\t\t\t- Subsubtask 9.04\n\t\t\t\t- Subsubsubtask 9.03 @done\n\t\t\t\tI love lying\n\t\t\t- Subsubtask 9.05 @done\n\t\t- Subtask 9.03 @done\n\t\tOk, this is truly the last comment.\n\t\tNah.',
'Inbox:\n\nProject 01:\n\t- Task 1.01\n\t\t- Subtask 01\n\t\t- Subtask 02\n\t\t- Subtask 03\n\t- Task 02 @done\n\t- Task 03\n\n/Project 02:\n\t- Task 01\n\tComentário que destruirá seu domingo\n\t\t- Primeira subtarefa\n\t\t- Segunda subtarefa\n\t\t- Terceira subtarefa @done\n\t\t- Quarta subtarefa\n\t\t\t- Primeira subsubtarefa\n\t\t\t- Segunda subsubtarefa @done\n\t\t- Quinta tarefa\n\t- Task 02\n\t- Task 03 @done\n\t- Task 04\n\nProject 03:\nSou um comentário extremamente complexo que quebrarei o seu script.\n\t- Task 01\n\t\t- Subtask 01 @done\n\t\t- Subtask 02\n\t- Task 02\n\t- Task 03\n\nProject 04:\n\t- Task 01\n\t\t- Subtask 01\n\t\t- Subtask 02 @done\n\t\t- Subtask 03\n\t\t\t- Subsubtask 01 @done\n\t\t\t- Subsubtask 02 @done\n\t\t- Subtask 04\n\t- Task 02\n\t- Task 03\n\nProject 05:\n\t- Task 01 @done\n\t- Task 02 @done\n\t- Task 03 @done\n\t- Task 04\n\t\t- Subtask 01 @done\n\t\t- Subtask 02 @done\n\t\t- Subtask 03 @done\n\t- Task 05\n\nProject 06:\n\t- Task 01 @done\n\t- Task 02\n\t\t- Subtask 01\n\t\tSou outro comentário maroto que arruinará o seu dia.\n\t\t- Subtask 02\n\t\tSou a primeira linha de um comentário maldoso.\n\t\tEsta é a segunda linha do comentário acima que te fará chorar.\n\t\t- Subtask 03\n\t- Task 03\n\nProject 7:\n\t- Lavar roupa\n\tSou a primeira linha de um comentário maldoso.\n\t\t- Cuecas @done\n\t\t- Meias @done\n\t- Cozinhar risoto @done\n\t\t- Lavar panela @done\n\t\t- Comprar arroz @done\n\t\t- Preparar caldo\n\nProject 08:\n\t- Task 01\n\tSou a primeira linha de um comentário maldoso.\n\nProject 09:\n\t- Task 01']

def MarkAsDone(project):
	tasks = [(x,y) for x,y in enumerate(project) if re.search('\t+-\s.*',y)]
	for index_task in tasks:
		try:
			nt = tasks[tasks.index(index_task) + 1]
			next_count = nt[1].count('\t')
		except IndexError:
			break
		task_desc = index_task[1]
		task_count = task_desc.count('\t')
		task_index = tasks.index(index_task)
		if next_count > task_count:
			subtasks = list(itertools.takewhile(lambda x:x[1].count('\t') > task_count, tasks[task_index + 1:]))
			if re.search('\t+-\s.*@done.*', task_desc):
				for subtask in subtasks:
					if re.search('(?!.*@done)\t+-\s.*', subtask[1]):
						project[subtask[0]]+=' @done'
			else:
				if all('@done' in subtask[1] for subtask in subtasks):
					project[index_task[0]]+=' @done'
					MarkAsDone(project)
					break
	return project

def nextActions(projects):
	for proj in projects:
		tasks = [(x,y) for x,y in enumerate(MarkAsDone(proj))]
		for task in tasks:
			if re.search('(?!.*@done)\t+-\s.*', task[1]):
				if tasks[0][1].startswith('/'):
					proj[task[0]]+=' @next'
				else:
					subtasks = list(itertools.takewhile(lambda x:x[1].count('\t') > task[1].count('\t') or re.search('(?!.*:$)\t+\w.+', task[1]), tasks[tasks.index(task)+1:]))
					for subtask in subtasks:
						if re.search('(?!.*@done)\t+-\s.*', subtask[1]):
							proj[subtask[0]]+=' @next'
					proj[task[0]]+=' @next'
					break
	return projects

					
allTasks = arg[3].split('\n\n')
projects = [filter(None, proj.split('\n')) for proj in allTasks]
output = '\n\n'.join(['\n'.join([str(task) for task in proj]) for proj in nextActions(projects)])

print output
