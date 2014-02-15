# -*- coding: UTF-8 -*-

import re
import itertools

arg = 'Inbox:\n\nProject 01::\n\t- Task 1.01\n\t\t- Subtask 01\n\t\t- Subtask 02\n\t\t- Subtask 03\n\t- Task 02 @done\n\t- Task 03\n\nProject 02:\n\t- Task 01\n\tComentário que destruirá seu domingo\n\t\t- Primeira subtarefa\n\t\t- Segunda subtarefa\n\t\t- Terceira subtarefa @done\n\t\t- Quarta subtarefa\n\t\t\t- Primeira subsubtarefa\n\t\t\t- Segunda subsubtarefa @done\n\t\t- Quinta tarefa\n\t- Task 02\n\t- Task 03 @done\n\t- Task 04\n\nProject 03::\nSou um comentário extremamente complexo que quebrarei o seu script.\n\t- Task 01\n\t\t- Subtask 01 @done\n\t\t- Subtask 02\n\t- Task 02\n\t- Task 03\n\nProject 04::\n\t- Task 01\n\t\t- Subtask 01\n\t\t- Subtask 02 @done\n\t\t- Subtask 03\n\t\t\t- Subsubtask 01 @done\n\t\t\t- Subsubtask 02 @done\n\t\t- Subtask 04\n\t- Task 02\n\t- Task 03\n\nProject 05::\n\t- Task 01 @done\n\t- Task 02 @done\n\t- Task 03 @done\n\t- Task 04\n\t\t- Subtask 01 @done\n\t\t- Subtask 02 @done\n\t\t- Subtask 03 @done\n\t- Task 05\n\nProject 06::\n\t- Task 01 @done\n\t- Task 02\n\t\t- Subtask 01\n\t\tSou outro comentário maroto que arruinará o seu dia.\n\t\t- Subtask 02\n\t\tSou a primeira linha de um comentário maldoso.\n\t\tEsta é a segunda linha do comentário acima que te fará chorar.\n\t\t- Subtask 03\n\t- Task 03\n\nProject 7::\n\t- Lavar roupa\n\tSou a primeira linha de um comentário maldoso.\n\t\t- Cuecas @done\n\t\t- Meias @done\n\t- Cozinhar risoto @done\n\t\t- Lavar panela @done\n\t\t- Comprar arroz @done\n\t\t- Preparar caldo\n\nProject 08:\n\t- Task 01\n\tSou a primeira linha de um comentário maldoso.\n\nProject 09:\n\t- Task 01'

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
				if tasks[0][1].endswith('::'):
					subtasks = list(itertools.takewhile(lambda x:x[1].count('\t') > task[1].count('\t') or re.search('(?!.*:$)\t+\w.+', task[1]), tasks[tasks.index(task)+1:]))
					for subtask in subtasks:
						if re.search('(?!.*@done)\t+-\s.*', subtask[1]):
							proj[subtask[0]]+=' @next'
					proj[task[0]]+=' @next'
					break
				else:
					proj[task[0]]+=' @next'
	return projects


allTasks = arg.split('\n\n')
projects = [filter(None, proj.split('\n')) for proj in allTasks]
output = '\n\n'.join(['\n'.join([str(task) for task in proj]) for proj in nextActions(projects)])

#print arg
print output
