from aiogram import Bot, Dispatcher, executor, types
from utils.config import BOT_TOKEN
import utils.api_utils as au


series = input("Enter series: ")
number = input("Enter number: ")

print("Received series:", series)
print("Received number:", number)

if series == pbf_data["series"] and number == pbf_data["number"]:
    print("Series and number match with data from API.")
else:
    print("Series and number do not match with data from API.")