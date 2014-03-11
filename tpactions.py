# -*- coding: UTF-8 -*-

import re
import itertools
import sys

class na:
	def __init__(self):
		debug = '''Inbox:

		Project 01:
		This is a parallel project with a parallel task with subtasks
			- Task 01
			- Task 02 @done
			- Task 03 with subtasks all parallel @done
			Lalalal:ala
				- Subtask 01
				- Subtask 02
				- Subtask 03
			- Task 04 @waiting(developer)

		Project 02:
		This is a parallel project with a sequential subproject
			- Task 01
			Subproject 01::
				- Subtask 01 @done
				- Subtask 02 @done
			- Task 02

		Project 03::
		This is a sequential project with a parallel subproject
			Subproject 01:
				- Subtask 01 @done
				- Subtask 02 @done
				- Subtask 03 @done
			- Task 01
			- Task 02 @waiting(developer)

		Project 04::
		This is a sequential project with a sequential subproject
			Subproject 01::
				- Subtask 01
				- Subtask 02
				- Subtask 03
			- Task 01 @hold
			- Task 02

		Project Nightmare::
		This is supposed to be the final proof of this concept
			Subproject 01::
				- Subtask 01
					- SubSubtask 01
					- SubSubtask 02
				- Subtask 02
			- Task 01
			- Task 02

		Project Supreme:
		This is the ultimate test for this script
			Subproject 01::
				- Subtask 01 @done
					- Subsubtask 01
					- Subsubtask 02
					Subsubproject 03::
						- Subsubsubtask 01
						- Subsubsubtask 02
					- Subsubtask 03
				- Subtask 02
			Pokemon 01:
				Subsubproject 02:: @done
					- Subsubsubsubtask 05
					- Subsubsubsubtask 04
				- Subsubtask 911'''
		try:
			projects = sys.argv[1] # Checks if the user submitted the tasks via Launch Center Pro or Drafts.
		except IndexError:
			try: # This block prompts the user for a file.
				import Tkinter, tkFileDialog # These modules are absent on Pythonista.
				Tkinter.Tk().withdraw()
				try:
					self.filePath = tkFileDialog.askopenfilename()
					file = open(self.filePath,'r') # This block checks if the user selected a file.
					projects = file.read()
					file.close()
				except IOError:
					projects = debug # Fallback if the user didn't select a file.
			except ImportError:
				projects = debug # Fallback if the user doesn't have the modules, probably on Pythonista.
		# Generates a concatenated list of our projects
		skipTags = ['@done','@waiting','@hold'] # Customizable list of tags to skip
		self.tags = '(%s)+?' % '|'.join(skipTags) # Converts the previous list into a string to be embed into the regular expression: (@done|@waiting|@hold)+?
		self.projects = [proj.splitlines() for proj in projects.split('\n\n')]

	# Checks for tasks that were supposed to be marked as done.
	def done(self,proj):
		tasks = [(x,y) for x,y in enumerate(proj) if re.search('\t*(-\s\w.+|.+:{1,2}(?!\s?\w)(\s@.+)?)',y)]
		for task in tasks:
			task_desc = task[1]
			task_count = task_desc.count('\t')
			task_index = tasks.index(task)
			try:
				next_task = tasks[tasks.index(task) + 1]
				next_count = next_task[1].count('\t')
			except IndexError:
				break
			if next_count > task_count:
				subtasks = list(itertools.takewhile(lambda x:x[1].count('\t') > task_count, tasks[task_index + 1:]))
				if '@done' in task_desc:
					for subtask in subtasks:
						if re.search('(?!.*@done)^.*', subtask[1]):
							proj[subtask[0]]+=' @done'
				else:
					if all('@done' in subtask[1] for subtask in subtasks):
						proj[task[0]]+=' @done'
						self.done(proj)
						break
		return proj

# Loops through subtasks if the task has any
	def subtasking(self,subtasks,sequential):
		txSubTasks = [y for x,y in subtasks] # This is a list of string, equivalent to our proj from the main loop
		enumSubTasks = [(x,y) for x,y in enumerate(txSubTasks)] # This is a enumerated list, equivalent to our tasks from the main loop
		for subtask in enumSubTasks:
			subtask_desc = subtask[1] # Description of subtask
			subtask_count = subtask_desc.count('\t') # Tab count for subtask
			subtask_index = enumSubTasks.index(subtask) # Location of the subtask in the enumerated list
			if subtask_desc in self.control: # Checks if the task was already modified and, therefore, in our control list
				continue
			else: # Adds the task description to the control list if it hasn't been there. This is the version without modifications.
				self.control.update([subtask_desc])
			try: # Checks if the task has a next task
				next_subtask = enumSubTasks[subtask_index + 1] # Full next task
				next_subcount = next_subtask[1].count('\t') # Tab count on next task
			except IndexError:
				next_subcount = subtask_count # To avoid errors, this allows the script to run without hacks
			if next_subcount > subtask_count: # This task has subtasks
				subsubtasks = list(itertools.takewhile(lambda x:x[1].count('\t') > subtask_count, enumSubTasks[subtask_index + 1:]))
				if subtask_desc.endswith('::'): # Checks if the task is a sequential subproject
					subsequential = True
				else:
					subsequential = False
				masterSubtasks = zip([x for x,y in subsubtasks], self.subtasking(subsubtasks,subsequential)) # Merges the outcome from the loop with the subtasks from the current task, giving you the updated task with the correct index.
				for st in masterSubtasks:
					self.control.update([st[1]]) # Includes the updated task to the control list
					txSubTasks[st[0]]=st[1] # Converts the string task, which will be returned, to the modified task.
			txSubTasks[subtask[0]]+=' @next' # Includes @next to the task in question
			if sequential: # Breaks the loop if the parent task is sequential, modifying only the first task and its children (if any)
				break
		for sub in txSubTasks:
			yield sub

#Defining our next actions function.
	def actions(self):
		for proj in self.projects:
			self.control = set()
			self.enum = [(x,y) for x,y in enumerate(self.done(proj)) if re.search('(?!.*%s)\t*(-\s\w.+|.+:{1,2}(?!\s?\w)(\s@.+)?)' % self.tags,y)]
			if len(self.enum) > 1: # Proceeds if the project is not empty.
				for task in self.enum[1:]: # Loops skipping the project name.
					task_desc = task[1] # Description of task
					task_count = task_desc.count('\t') # Tab count for task
					task_index = self.enum.index(task) # Location of the task in proj
					if task_desc in self.control:
						continue
					try: # Checks if the task has a next task
						next_task = self.enum[self.enum.index(task) + 1] # Full next task
						next_count = next_task[1].count('\t') # Tab count on next task
					except IndexError:
						next_count = task_count
					if next_count > task_count: # This task has subtasks
						subtasks = list(itertools.takewhile(lambda x:x[1].count('\t') > task_count, self.enum[task_index + 1:]))
						if task_desc.endswith('::'):
							sequential = True
						else:
							sequential = False
						masterSubtasks = zip([x for x,y in subtasks], self.subtasking(subtasks,sequential))
						for st in masterSubtasks:
							self.control.update([st[1]])
							proj[st[0]]=st[1]
					proj[task[0]]+=' @next'
					if proj[0].endswith('::'): # Breaks if project is sequential.
						break
		return self.output()
	def output(self):
		projects = '\n\n'.join(['\n'.join([str(task) for task in proj]) for proj in self.projects])
		try:
			import webbrowser
			if webbrowser.can_open('drafts://'):
				from urllib import quote
				webbrowser.open('drafts://x-callback-url/create?text=%s&action=Update%20TaskPaper' % quote(projects))
			else:
				print projects
		except:
				try:
					file = open(self.filePath,'w')
					projects = file.write(projects)
					file.close()
				except:
					print projects
					
na = na()
na.actions()
