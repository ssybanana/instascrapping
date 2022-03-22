from instabot import Bot
import openpyxl
import os 
import glob
cookie_del = glob.glob("config/*cookie.json")
os.remove(cookie_del[0])

rowctr = 1
wb1 = openpyxl.load_workbook('./excel/follower_list_3.xlsx')
sheet1 = wb1['Sheet1']

bot = Bot()
bot.login(username="osakakuma", password="Okuma2020")


followers = bot.get_user_followers('osakakuma')

for follower in followers:
  print(follower)
  sheet1['A' + str(rowctr)] = follower
  rowctr = rowctr + 1
  #user_info = bot.get_user_info(follower)
  #print(user_info)
  #each_info = user_info.split(',')
  #columnctr = 1
  #for element in each_info:
    #c1 = sheet1.cell(row=rowctr, column=columnctr)
    #c1.value = each_info[columnctr-1]
    #columnctr += 1


print(rowctr)
wb1.save('./excel/follower_list_3.xlsx')
wb1.close()
