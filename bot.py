import os
import pyautogui
import time
import sys

class PenguinDinterBot():
	# ------------------
	# INITIATE VARIABLES
	# ------------------
	def __init__(self):
		ORDERS_PATH = os.getcwd() + "/orders"
		MEALS_PATH = os.getcwd() + "/meals"

		self.back_button = (750, 640)
		self.trash_bin = (550, 650)
		self.upgrade_button = (530, 550)
		self.new_level = (530-150, 550)


		self.ORDERS = [ORDERS_PATH + "/" + order for order in os.listdir(ORDERS_PATH)]
		self.MEALS = [MEALS_PATH + "/" + meal for meal in os.listdir(MEALS_PATH)]

		self.MEAL2ORDER = dict()
		for i, meal in enumerate(self.MEALS):
			order = self.ORDERS[i]
			self.MEAL2ORDER[meal] = order

		self.start_game()


	# ------------------
	# FIRST CUTSCENE
	# ------------------
	def cutscene_start(self):
		input("Move mouse over bot window and press enter.")

		w = pyautogui.locateOnScreen("locate.png")
		if w is None:
			sys.exit("Couldn't find on screen. Is this game visible?")

		win_right = w[0]
		win_bottom = w[1]

		print("------GAME FOUND-------")

		pyautogui.click(win_right - 60, win_bottom - 180, interval=1)
		pyautogui.click(win_right - 280, win_bottom - 200, interval=1) # in case if game was started earlier
		pyautogui.click(self.back_button, interval=1)
		pyautogui.click(self.back_button, interval=1)

		time.sleep(6)


	# ------------------
	#  LEVEL END
	# ------------------
	def end_level(self):
		print("------END OF THE DAY!------")
		time.sleep(3)
		
		# first, look for upgrades
		self.upgrade()

		# start next level if available
		self.start_level_or_restart()

		time.sleep(6)


	# ------------------
	# EQUIPMENT UPGRADES
	# ------------------
	def upgrade(self):
		pyautogui.click(self.upgrade_button,interval=.3)

		upgrade_x_offset = 200
		upgrade_y_offset = 150
		upgrade_x_start = 300
		upgrade_y_start = 250

		# since it's impossible to deal with numbers, click everything
		for x in range(3):
			for y in range(2, -1, -1):
				click_x = upgrade_x_start + x*upgrade_x_offset
				click_y = upgrade_y_start + y*upgrade_y_offset
				pyautogui.click(click_x, click_y, interval=.2)

		pyautogui.click(self.back_button, interval=.3)


	# --------------------------
	# START NEW LEVEL OR RESTART
	# --------------------------
	def start_level_or_restart(self):
		next_option = pyautogui.locateCenterOnScreen("nextlevel.png", confidence=.9)
		if next_option is None:
			# if not, start a new day or restart a day
			pyautogui.click(self.new_level, interval=.3)
		else:
			print("\n------NEXT LEVEL!------\n")
			pyautogui.click(next_option, interval=1)
			pyautogui.click(self.back_button, interval=1)
			pyautogui.click(self.back_button, interval=1)


	# --------------------------
	# LEAD CLIENT TO FREE TABLE
	# --------------------------
	def lead_to_table(self):
		client = pyautogui.locateCenterOnScreen("client.png", confidence=.9, region=(120,300, 80, 200))
		if client is not None:
			print("Found a client and led them to a table.")
			pyautogui.click(client[0], client[1])
			
			free_table = pyautogui.locateCenterOnScreen("empty_table.png", confidence=.8)
			conf = .8
			while free_table is None and conf > .2:
				conf -= .1
				free_table = pyautogui.locateCenterOnScreen("empty_table.png", confidence=conf)
			
			pyautogui.click(free_table[0], free_table[1])


	# --------------------
	# TAKE CLIENT'S ORDER
	# --------------------
	def take_order(self):
		ordering_client = pyautogui.locateCenterOnScreen("client_order.png",  confidence=.7)

		if ordering_client is not None:
			print("A client wants to order something!")
			pyautogui.click(ordering_client[0], ordering_client[1])

		# check for mad clients
		ordering_client = pyautogui.locateCenterOnScreen("mad_client.png",  confidence=.8)
		if ordering_client is not None:
			print("A mad client wants to order something!")
			pyautogui.click(ordering_client[0], ordering_client[1])

	
	# ---------------------
	# SERVE MEAL TO CLIENT
	# ---------------------
	def serve_meal(self):
		for meal in self.MEALS:
			meal_centered = pyautogui.locateCenterOnScreen(meal, confidence=.9, region=(0, 600, 490, 80))
			if meal_centered is not None:
				pyautogui.click(meal_centered[0], meal_centered[1])

				# find image reference
				look_for_order = self.MEAL2ORDER[meal]
				order_centered = pyautogui.locateCenterOnScreen(look_for_order, confidence=.8)
				conf = .8

				# if program doesn't recognize order, look for it until it succeed
				while order_centered is None:
					conf -= .1
					order_centered = pyautogui.locateCenterOnScreen(look_for_order, confidence=conf)
				
				pyautogui.click(order_centered[0], order_centered[1])

				food_name = look_for_order.split("/")[-1][:-4]

				print(f"Serving the meal {food_name} to the client.")
				time.sleep(0.3)
				break


	# ---------------
	# COLLECT MONEY
	# ---------------
	def collect_money(self):
		money = pyautogui.locateCenterOnScreen("money.png", confidence=.8)
		if money is not None:
			print("Money collected.")
			pyautogui.click(money[0], money[1])

		# if there are money left, but the main charater covers it, force to move
		if pyautogui.locateCenterOnScreen("pickup.png", grayscale=True, confidence=.8) is not None:
			pyautogui.click(self.trash_bin)



	# ---------------
	# GAME FLOW
	# ---------------
	def run_game(self):
		while True:
			# if the level is accomplished
			endgame = pyautogui.locateCenterOnScreen("end.png", grayscale=True, confidence=.9)
			if endgame is not None:
				self.end_level()
			else:
				print("Looking for a client......")
				
				self.lead_to_table()
				self.take_order()
				self.serve_meal()
				self.collect_money()


	# ---------------------------
	#
	#         GAME START
	#
	# ---------------------------
	def start_game(self):
		self.cutscene_start()
		self.run_game()




if __name__ == "__main__":
	bot = PenguinDinterBot()