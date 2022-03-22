import instaloader
from instascrape import *
import bs4
from bs4.element import Comment 
import requests
import openpyxl
import time


#SESSIONID = '27862748908%3AIJseVR4VqgJiin%3A11'
#headers = {
#    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
#    "cookie": "sessionid={SESSIONID};"
#}

compet_list1 = ['sephorasg','tokyuhands.sg','isetansg','maccosmeticssg', 'novela_sg']
compet_list2 = ['essentials', 'welciabhg', 'donkisg','fairpricesg','unitysg','watsonssg']

full_compet_list = ['sephorasg','tokyuhands.sg','isetansg','maccosmeticssg', 'novela_sg', 
                    'essentials', 'welciabhg', 'donkisg','fairpricesg','unitysg','watsonssg']

L = instaloader.Instaloader() 
L.login('osakakuma', 'Okuma2020')

wb1 = openpyxl.load_workbook('./excel/hashtag_competitor.xlsx')
sheet1 = wb1['Sheet1']

hashtag_dict = {}

def get_hashtag_dict(compet_list):
  for compet in compet_list:
    profile = instaloader.Profile.from_username(L.context, compet)
    print(compet)
    count = 1
    posts_sorted_by_likes = sorted(profile.get_posts(), key=lambda p: p.likes + p.comments, reverse=True)
    time.sleep(2)
    for post in posts_sorted_by_likes:
      if count < 31:
        print(count)
        count += 1
        if post.caption != []:
          hashtag_list = []
          hashtag_list = post.caption_hashtags 
          for hashtag in hashtag_list:
            time.sleep(1)
            if hashtag not in hashtag_dict:
              hashtag_dict[hashtag] = 1
            else:
              curr_count = hashtag_dict[hashtag]
              final_count = curr_count + 1
              hashtag_dict[hashtag] = final_count
      else:
        break

  return hashtag_dict

def get_and_save_fdict(hashtag_dict):
  rowctr = 2
  for compet in full_compet_list:
    sheet1['A' + str(rowctr)] = compet
    rowctr += 1

  sorted_dt = {key: value for key, value in sorted(hashtag_dict.items(), key=lambda item: item[1], reverse = True)}
  rowctr = 2
  new_hashtag_dict = {}
  for key in sorted_dt:
    new_key = "#"+str(key)
    new_hashtag_dict[new_key] = sorted_dt[key]

    sheet1['B' + str(rowctr)] = new_key
    sheet1['C' + str(rowctr)] = str(new_hashtag_dict[new_key])
    rowctr += 1

  return new_hashtag_dict



hashtag_dict = get_hashtag_dict(compet_list1)
time.sleep(800)
hashtag_dict = get_hashtag_dict(compet_list2)
final_hashtag_dict = get_and_save_fdict(hashtag_dict)

#rowctr = 2
#for key in final_hashtag_dict:
#  search_tag = key[1:]
#  url_string = "https://www.instagram.com/explore/tags/%s/" % search_tag
#  response = bs4.BeautifulSoup(requests.get(url_string).text, "html.parser")
#  for script_tag in response.find_all("script"):
#      if script_tag.text.startswith("window._sharedData ="):
#          shared_data = re.sub("^window\._sharedData = ", "", script_tag.text)
#          shared_data = re.sub(";$", "", shared_data)
#          shared_data = json.loads(shared_data)
#  media_count = media_count = shared_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['count']
#  sheet1['D' + str(rowctr)] = media_count
#  print(media_count)
#  rowctr += 1
#  time.sleep(2)

wb1.save('./excel/hashtag_competitor.xlsx')
wb1.close()