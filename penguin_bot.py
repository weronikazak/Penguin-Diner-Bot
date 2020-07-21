import os
import pyautogui
import sys

input("Mve mouse over bot window and press enter.")
WINDOW = pyautogui.position()

w = pyautogui.locateOnScreen("locate.png")
if w is None:
	sys.exit("Couldn't find on screen. Is this game visible?")

win_right = w[0]
win_bottom = w[1]

print("Found game at: ", win_right, win_bottom)

win_h = 480
win_w = 640


# ------------
# START GAME
# ------------

pyautogui.click(win_right - 60, win_bottom - 180, interval=1)
pyautogui.click(win_right - 280, win_bottom - 200, interval=1) # in case if game was started earlier
pyautogui.click(win_right - 20, win_bottom - 10, interval=1)
pyautogui.click(win_right - 20, win_bottom - 10, interval=1) # in case if game was started earlier

# ------------
# START ORDERS
# ------------

ORDERS_PATH = os.getcwd() + "/orders/"
IMAGES_PATH = os.getcwd() + "/images/"

ORDERS = [ORDERS_PATH + order for order in os.dirlist(ORDERS_PATH)]

# LOCATE CLIENTS


while True:
	command = input("> ")

	if command == "quit":
		sys.exit()

	elif command == "":
		pyautogui.locateOnScreen()


for food_order in ORDERS:
	num_orders = len(list(pyautogui.locateAllOnScreen(food_order)))
	if num_orders > 0:
		print(food_order, num_orders)

