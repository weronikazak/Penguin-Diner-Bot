import os
import pyautogui
import sys
import time
import cv2

input("Move mouse over bot window and press enter.")

w = pyautogui.locateOnScreen("locate.png")
if w is None:
	sys.exit("Couldn't find on screen. Is this game visible?")

win_right = w[0]
win_bottom = w[1]

print("------GAME FOUND-------")


# -----------------------
# UPGRADE MENU CONSTANTS
# -----------------------
upgrade_x_offset = 200
upgrade_y_offset = 150
upgrade_x_start = 300
upgrade_y_start = 250

back_button = (750, 640)
trash_bin = (550, 650)

# ------------
# START GAME
# ------------
pyautogui.click(win_right - 60, win_bottom - 180, interval=1)
pyautogui.click(win_right - 280, win_bottom - 200, interval=1) # in case if game was started earlier
pyautogui.click(back_button, interval=1)
pyautogui.click(back_button, interval=1)

time.sleep(6)

# ------------
# START ORDERS
# ------------

CLIENTS = []

ORDERS_PATH = os.getcwd() + "/orders"
MEALS_PATH = os.getcwd() + "/meals"

ORDERS = [ORDERS_PATH + "/" + order for order in os.listdir(ORDERS_PATH)]
MEALS = [MEALS_PATH + "/" + meal for meal in os.listdir(MEALS_PATH)]

MEAL2ORDER = dict()
for i, meal in enumerate(MEALS):
	order = ORDERS[i]
	MEAL2ORDER[meal] = order

# LOCATE CLIENTS
while True:
	# if the level is accomplished
	endgame = pyautogui.locateCenterOnScreen("end.png", grayscale=True, confidence=.9)
	if endgame is not None:
		print("------END OF THE DAY!------")
		# first, look for upgrades
		time.sleep(3)
		upgrades = pyautogui.locateCenterOnScreen("upgrades.png", confidence=.9)

		pyautogui.click(upgrades[0], upgrades[1],interval=.3)

		# click everything
		for x in range(3):
			for y in range(3):
				click_x = upgrade_x_start + x*upgrade_x_offset
				click_y = upgrade_y_start + y*upgrade_y_offset
				pyautogui.click(click_x, click_y, interval=.3)

		pyautogui.click(back_button, interval=.3)

		# start next level if available
		next_option = pyautogui.locateCenterOnScreen("nextlevel.png", confidence=.9)
		if next_option is None:
			# if not, start a new day or restart a day
			pyautogui.click(upgrades[0]-150, upgrades[1], interval=.3)
		else:
			print("\n------NEXT LEVEL!------\n")
			pyautogui.click(next_option, interval=1)
			pyautogui.click(back_button, interval=1)
			pyautogui.click(back_button, interval=1)

		time.sleep(6)
	else:
		print("Looking for a client......")
		client = pyautogui.locateCenterOnScreen("client.png", confidence=.9, region=(120,300, 80, 200))

		if client is not None:
			print("Found a client and directed them to a table.")
			pyautogui.click(client[0], client[1])
			
			free_table = pyautogui.locateCenterOnScreen("empty_table.png", confidence=.8)
			conf = .8
			while free_table is None and conf > .2:
				conf -= .1
				free_table = pyautogui.locateCenterOnScreen("empty_table.png", confidence=conf)
			
			pyautogui.click(free_table[0], free_table[1])

		# if there's a client, that wants to order something, take his order
		ordering_client = pyautogui.locateCenterOnScreen("client_order.png",grayscale=True,  confidence=.7)

		if ordering_client is not None:
			print("A client wants to order something!")
			pyautogui.click(ordering_client[0], ordering_client[1])

		# check if there are any meals awaiting for being served
		for meal in MEALS:
				meal_centered = pyautogui.locateCenterOnScreen(meal, confidence=.9, region=(0, 600, 490, 80))
				if meal_centered is not None:
					pyautogui.click(meal_centered[0], meal_centered[1])

					# look for coords of the client, who ordered the meal
					look_for_order = MEAL2ORDER[meal]
					order_centered = pyautogui.locateCenterOnScreen(look_for_order, confidence=.8)
					conf = .8

					while order_centered is None:
						conf -= .1
						order_centered = pyautogui.locateCenterOnScreen(look_for_order, confidence=conf)
					
					pyautogui.click(order_centered[0], order_centered[1])

					food_name = look_for_order.split("/")[-1][:-4]

					print(f"Serving the meal {food_name} to the client.")
					time.sleep(0.4)
					break


		# look whether there's money left. if ture, collect them and clean table
		money = pyautogui.locateCenterOnScreen("money.png", confidence=.8)
		if money is not None:
			print("Money collected.")
			pyautogui.click(money[0], money[1])


		if pyautogui.locateCenterOnScreen("pickup.png", grayscale=True, confidence=.8) is not None:
			pyautogui.click(trash_bin)

sys.exit()

