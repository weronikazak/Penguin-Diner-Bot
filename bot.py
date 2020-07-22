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

print("GAME FOUND")

win_h = 480
win_w = 640


# ------------
# START GAME
# ------------

pyautogui.click(win_right - 60, win_bottom - 180, interval=1)
pyautogui.click(win_right - 280, win_bottom - 200, interval=1) # in case if game was started earlier
pyautogui.click(win_right - 20, win_bottom - 10, interval=1)
pyautogui.click(win_right - 20, win_bottom - 10, interval=1) # in case if game was started earlier

time.sleep(5)

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
	endgame = pyautogui.locateCenterOnScreen("endgame.png", grayscale=True, confidence=.9)
	if endgame is not None:
		print("END OF THE DAY!")
		pyautogui.click(endgame[0], endgame[1])
		time.sleep(5)
	else:
		print("Looking for a client......")
		client = pyautogui.locateCenterOnScreen("client.png", confidence=.9, region=(120,300, 80, 200))

		if client is not None:
			print("Found a client and directed them to a table.")
			pyautogui.click(client[0], client[1])
			free_table = pyautogui.locateCenterOnScreen("empty_table.png", confidence=.9)
			pyautogui.click(free_table[0], free_table[1])

		# if there's a client, that wants to order something, take his order
		ordering_clients = pyautogui.locateAllOnScreen("client_order.png", confidence=.7)

		if ordering_clients is not None or len(ordering_clients) > 0:
			for waitinig_client_coords in ordering_clients:

				print("A client wants to order something!")

				ordering_client = pyautogui.center(waitinig_client_coords)
				pyautogui.click(ordering_client[0], ordering_client[1])

				# save the type of meal, they wants
				for food_order in ORDERS:
					is_order = pyautogui.locateOnScreen(food_order, confidence=.9)
					if is_order is not None:
						food_name = food_order.split("/")[-1][:-4]
						print(f"A client orders {food_name}.")

						# save client's coords and the meal they wants
						CLIENTS.append([ordering_client, food_order])
						break

		# check if there are any meals awaiting for being served
		for meal in MEALS:
				meal_centered = pyautogui.locateCenterOnScreen(meal, confidence=.9)
				if meal_centered is not None:
					pyautogui.click(meal_centered[0], meal_centered[1])

					# look for coords of the client, who ordered the meal
					look_for_order = MEAL2ORDER[meal]

					for _id, client_order in enumerate(CLIENTS):
						client, food_order = client_order
						if look_for_order == food_order:
							food_name = food_order.split("/")[-1][:-4]
							print(f"Serving the meal {food_name} to the client.")

							pyautogui.click(client[0], client[1])
							del CLIENTS[_id]
							time.sleep(0.5)
							break

		# look whether there's money left. if ture, collect them and clean table
		money = pyautogui.locateCenterOnScreen("money.png", confidence=.8)
		if money is not None:
			print("Money collected.")
			pyautogui.click(money[0], money[1])



		time.sleep(0.2)


sys.exit()

