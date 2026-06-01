class GreetingService:
	def __init__(self, message: str):
		self.message = message

	def generate_greeting(self, name: str = "Guest") -> str:
		"""Генерує привітання для вказаного імені."""
		return f"{self.message} Вітаємо, {name}."