import random

class Crafter:
	AROUND_MATRIX = ((-1, -1),
					 (-1, 0),
					 (-1, 1),
					 (0, -1),
					 (0, 1),
					 (1, -1),
					 (1, 0),
					 (1, 1))
	
	def __init__(self, rows, cols, tnts):
		if rows < 1:
			raise Exception(f"Too few rows: {rows} < 1")
		
		if cols < 1:
			raise Exception(f"Too few columns: {cols} < 1")
		
		if tnts < 1:
			raise Exception(f"Too little TNT: {tnts} < 1")
		
		if tnts >= rows * cols:
			raise Exception(f"Too much TNT: {tnts} > {rows * cols}")
		
		self.rows = rows
		self.cols = cols
		self.tnts = tnts
		self.flags = tnts
		self.grid = [[False for col in range(cols)] for row in range(rows)]
		self.gui = [[' ' for col in range(cols)] for row in range(rows)]
		self.ready = False
	
	def show_gui(self):
		print(f"TNT remaining: {self.tnts - self.flags}")
		hor = "- " * self.cols
		print(f"/ {hor}\\")
		
		for row in self.gui:
			print(f"| {' '.join(row)} |")
		
		print(f"\\ {hor}/")
	
	def random_row_col(self):
		return (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
	
	def is_in_grid(self, row, col):
		return (0 <= row < self.rows) and (0 <= col < self.cols)
	
	def is_tnt(self, row, col):
		if not self.is_in_grid(row, col):
			return False
		
		return self.grid[row][col]
	
	def place_tnt(self, row, col):
		if self.ready or not self.is_in_grid(row, col):
			return
		
		self.grid[row][col] = True
	
	def set_tnts(self, seed_row, seed_col):
		if self.ready:
			return

		while self.flags > 0:
			row, col = self.random_row_col()
			if (row, col) == (seed_row, seed_col):
				continue
			if self.is_tnt(row, col):
				continue

			self.place_tnt(row, col)
			self.flags -= 1
		
		self.ready = True
	
	def tnts_around(self, row, col):
		if not (self.ready and self.is_in_grid(row, col)):
			return 0
		
		count = 0
		
		for around in Crafter.AROUND_MATRIX:
			new_row = row + around[0]
			new_col = col + around[1]
			if self.is_tnt(new_row, new_col):
				count += 1
		
		return count
	
	def is_undug(self, row, col):
		return self.ready and self.is_in_grid(row, col) and self.gui[row][col] in (' ', 'F')
	
	def reveal(self, row, col):
		if not self.is_undug(row, col):
			return
		
		if self.is_tnt(row, col):
			self.gui[row][col] = 'X'
			return
		
		around = self.tnts_around(row, col)
		self.gui[row][col] = str(around)
		
		if around == 0:
			for around in Crafter.AROUND_MATRIX:
				new_row = row + around[0]
				new_col = col + around[1]
				self.reveal(new_row, new_col)
	
	def dig(self, row, col):
		if not self.is_in_grid(row, col):
			return False
		
		if not self.ready:
			self.set_tnts(row, col)
		
		self.reveal(row, col)
		return not self.is_tnt(row, col)
	
	def flag(self, row, col):
		if not self.is_undug(row, col) or self.gui[row][col] == 'F':
			return False
		
		self.gui[row][col] = 'F'
		self.flags += 1
		return True

	def unflag(self, row, col):
		if not self.is_undug(row, col) or self.gui[row][col] == ' ':
			return False
		
		self.gui[row][col] = ' '
		self.flags -= 1
		return True
	
	def num_dug(self):
		count = 0
		
		for row in range(self.rows):
			for col in range(self.cols):
				if not self.is_undug(row, col):
					count += 1
		
		return count
	
	def reveal_all(self):
		for row in range(self.rows):
			for col in range(self.cols):
				self.reveal(row, col)
	
	def is_done(self):
		return self.num_dug() + self.tnts == self.rows * self.cols
	
	def run(self):
		self.show_gui()
		win = True
		while not self.is_done():
			print("\n[0] Dig\n[1] Flag\n[2] Unflag")
			
			try:
				command = int(input("Action: "))
				if command not in range(0, 3):
					raise ValueError("Input not in range [0, 2]")
				
				row = int(input("Row: "))
				col = int(input("Column: "))
				
				has_change = False
				match command:
					case 0:
						has_change = self.dig(row, col)
						if self.is_tnt(row, col):
							win = False
							break
					case 1:
						has_change = self.flag(row, col)
					case 2:
						has_change = self.flag(row, col)
					case _:
						raise ValueError("Something went really wrong.")

			except ValueError:
				continue
				
			self.show_gui()
		
		if win:
			print("\nYou win!!")
		else:
			print("\nAw, you lost :(")
			self.reveal_all()
			self.show_gui()
