import instaloader
import openpyxl
import time


L = instaloader.Instaloader()

L.login('osakakuma', 'Okuma2020') 

wb1 = openpyxl.load_workbook('./excel/follower_list_1.xlsx')
sheet1 = wb1['Sheet1']
sheet2 = wb1['Sheet2']
# Obtain profile metadata
profile = instaloader.Profile.from_username(L.context, 'osakakuma')

followercount = 0

for follower in profile.get_followers():
    username = follower.username
    sheet1['A' + str(followercount+1)] = username
    followercount += 1
    time.sleep(0.5)

followeecount = 0
for followee in profile.get_followees():
    username = followee.username
    sheet2['A' + str(followeecount+1)] = username
    followeecount += 1
    time.sleep(0.5)
    
print(followercount)
print(followeecount)
wb1.save('./excel/follower_list_1.xlsx')
wb1.close()


#https://kevinjnguyen.medium.com/scraping-hashtags-on-instagram-python-and-instaloader-subtle-clothing-collection-a50c7c229c95