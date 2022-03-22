import time
import instaloader
import openpyxl

L = instaloader.Instaloader() 
L.login('osakakuma', 'Okuma2020')


rowctr = 2
hashtag_list = ['egg']
#for htag in hashtag_list:
hashtag = instaloader.Hashtag.from_name(L.context, 'egg')
postctr = 0
tagctr = 0
wb1 = openpyxl.load_workbook('hashtag_list.xlsx')
sheet1 = wb1['Sheet1']

hashtag_name  = sheet1['A' + str(rowctr)] 
hashtag_name.value = hashtag.name

media_count = sheet1['B' + str(rowctr)]
media_count.value = hashtag.mediacount


for tag in hashtag.get_related_tags():
    tag_name = sheet1['C' + str(rowctr)]
    tag_name.value = tag.name
    rowctr += 1
    tagctr += 1
tagctr -= 1

rowctr = rowctr - tagctr


for post in hashtag.get_top_posts():
    if postctr < 6:
        post_name = sheet1['C' + str(rowctr)]
        post_name.value = post.shorturl
        rowctr += 1
        postctr += 1
postctr -= 1

rowctr = rowctr - postctr

if postctr > tagctr:
    rowctr = rowctr + postctr
if postctr < tagctr:
    rowctr = rowctr + tagctr

rowctr += 1

   
wb1.save('post_list.xlsx')
wb1.close()


#https://kevinjnguyen.medium.com/scraping-hashtags-on-instagram-python-and-instaloader-subtle-clothing-collection-a50c7c229c95
#https://github.com/instaloader/instaloader/issues/874#issuecomment-731561430
