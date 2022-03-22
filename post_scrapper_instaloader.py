import time
import instaloader
import openpyxl

L = instaloader.Instaloader() 
L.login('osakakuma', 'Okuma2020')  
profile = instaloader.Profile.from_username(L.context, 'osakakuma') 

wb1 = openpyxl.load_workbook('./excel/post_list.xlsx')
sheet1 = wb1['Sheet1']
rowctr = 2
count = 1

for post in profile.get_posts():
    if count > 30 and count < 60:
        print(count)
        sheet1['A' + str(rowctr)] = post.shortcode
        sheet1['B' + str(rowctr)] = post.caption
        post_likes = post.get_likes()
        post_comments = post.get_comments()

        likectr = 0
        for likee in post_likes:
            clike = sheet1['C' + str(rowctr+likectr)]
            clike.value = likee.username
            likectr += 1

        time.sleep(2)

        ccommenter_dict = {}
        for comment in post_comments:
            if (comment.owner.username not in ccommenter_dict):
                repost_list = []
                ccomment_text_list = comment.text
                ccomment_text_words = ccomment_text_list.split()
                for word in ccomment_text_words:
                    if word.startswith('@'):
                        repost_list.append(word)
                ccommenter_dict[comment.owner.username] = repost_list
            else: 
                curr_repost_list = ccommenter_dict[comment.owner.username]
                repost_list = []
                ccomment_text_list = comment.text
                ccomment_text_words = ccomment_text_list.split()
                for word in ccomment_text_words:
                    if word.startswith('@'):
                        repost_list.append(word)
                final_repost_list = curr_repost_list + repost_list
                ccommenter_dict[comment.owner.username] = final_repost_list

        commentctr = 0 
        for key in ccommenter_dict:
            sheet1['D' + str(rowctr+commentctr)] = key
            sheet1['E' + str(rowctr+commentctr)] = str(ccommenter_dict[key])
            commentctr += 1

        if likectr > commentctr:
            rowctr = rowctr + likectr
        elif likectr < commentctr:
            rowctr = rowctr + commentctr
        
        rowctr += 1
        count += 1

    else:
        count += 1
        continue

wb1.save('./excel/post_list.xlsx')
wb1.close()