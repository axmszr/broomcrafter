from crafter import Crafter

class Broom:
	DIFFS = (None,
			 (9, 9, 10),
			 (16, 16, 40),
			 (16, 30, 99))
	
	def __init__(self):
		while True:
			print("\n[0] Custom\n[1] Beginner\n[2] Intermediate\n[3] Expert")
			try:
				diff = int(input("Choose difficulty: "))
				if diff not in range(0, 4):
					raise ValueError("Input not in range [0, 3]")
				break
			except ValueError:
				continue
		
		if diff == 0:
			print("\nLol I haven't implemented that. Here's Expert.")
			diff = 3
		
		self.c = Crafter(*Broom.DIFFS[diff])
		self.c.run()

b = Broom()
