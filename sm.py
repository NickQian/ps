
class StateMachine:

	def __init__(self):
		self.handlers = {}
		self.startState = None
		self.endState = []

	def add_state(self, name. handler, end_state=0):
		name = name.upper()
		self.handlers[name] = handler
		if end_state:
			self.endState.append(name)

	def
