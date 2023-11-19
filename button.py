#Button untuk menampilkan tombol yang berguna dalam interaksi tampilan UI Home/Main Screen
class Button():
	# Inisialisasi tombol
	def __init__(self, x_pos, y_pos, text_show, font, base_color, hovering_color):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_show = text_show
		self.text = self.font.render(self.text_show, True, self.base_color)
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	# Melakukan pembaruan UI supaya tombol dapat ditampilkan
	def update(self, screen):
		screen.blit(self.text, self.text_rect)

	# Mengecek klik mouse 
	def checkMouseInput(self, position):
		if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
			return True
		return False

	# Memberikan hover color
	def hoverColor(self, position):
		if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
			self.text = self.font.render(self.text_show, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_show, True, self.base_color)