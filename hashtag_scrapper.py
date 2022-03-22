import re
import bs4
from bs4.element import Comment 
import requests
import json
import openpyxl


SEARCHLIM = 30

wb1 = openpyxl.load_workbook('./excel/hashtag_competitor.xlsx')
sheet1 = wb1['Sheet1']
rowctr = 2

def clean_input(tag):
    tag = tag.replace(" ", "")
    if tag.startswith('#'):
        return tag[1:].lower()
    else:
        return tag.lower()

def extract_shared_data(doc):
    for script_tag in doc.find_all("script"):
        if script_tag.text.startswith("window._sharedData ="):
            shared_data = re.sub("^window\._sharedData = ", "", script_tag.text)
            shared_data = re.sub(";$", "", shared_data)
            shared_data = json.loads(shared_data)
            return shared_data

def return_all_hashtags(tweets, tag):
    all_hashtags = []
    for tweet in tweets:
        for word in tweet.split():
            if word.startswith('#') and word.lower() != '#' + tag.lower():
                all_hashtags.append(word.lower())
    return all_hashtags

def get_related_hashtags(shared_data):
    
    media = shared_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']

    captions = []
    count = 1 
    for post in media:
      if count < SEARCHLIM:
        if post['node']['edge_media_to_caption']['edges'] != []:
            captions.append(post['node']['edge_media_to_caption']['edges'][0]['node']['text'])
            count += 1

    all_tags = return_all_hashtags(captions, tag)
    frequency = {}
    for item in set(all_tags):
        frequency[item] = all_tags.count(item)
    return {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1], reverse=True)}

def get_media_count(shared_data):
  media_count = shared_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['count']
  return media_count

def get_hashtag_post(shared_data):
  hashtag_post = shared_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']

  posts = []
  count = 1 
  for post in hashtag_post:
    if count < SEARCHLIM:
      if post['node']['edge_media_to_caption']['edges'] != []:
          posts.append(post['node']['shortcode'])
          count += 1

  return posts

def get_like_count(shared_data):
  media = shared_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
  likectr_list = []
  count = 1
  for post in media:
    if count < SEARCHLIM:
      if post['node']['edge_media_to_caption']['edges'] != []:
          likectr_list.append(post['node']['edge_liked_by']['count'])
          count += 1
  return likectr_list

def get_comment_count(shared_data):
  media = shared_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
  commentctr_list = []
  count = 1
  for post in media:
    if count < SEARCHLIM:
      if post['node']['edge_media_to_caption']['edges'] != []:
          commentctr_list.append(post['node']['edge_media_to_comment']['count'])
          count += 1
  return  commentctr_list

def get_post_owner(shared_data):
  hashtag_post = shared_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
  owner_list = []
  count = 1 
  for post in hashtag_post:
    if count < SEARCHLIM:
      if post['node']['edge_media_to_caption']['edges'] != []:
          owner_list.append(post['node']['owner']['id'])
          count += 1

  return owner_list

def get_data(tag):
  search_tag = clean_input(tag)

  url_string = "https://www.instagram.com/explore/tags/%s/" % search_tag
  response = bs4.BeautifulSoup(requests.get(url_string).text, "html.parser")
  shared_data = extract_shared_data(response)

  with open('hashtag_data.json', 'w', encoding='utf-8') as f:
    json.dump(shared_data, f, ensure_ascii=False, indent=4)

  return shared_data




tag = input("Enter hashtag:")
shared_data = get_data(tag)
media_count = get_media_count(shared_data)
print(media_count)
#rowctr = 2
#for row in sheet1.iter_rows():
#    tag = sheet1['B'+ str(rowctr)].value
#    print(tag)
#    shared_data = get_data(tag)
#    print(media_count)
#    sheet1['D' + str(rowctr)] = media_count
#    rowctr += 1
#    time.sleep(2)

    

#all_tags = get_related_hashtags(shared_data)
#relatedctr = 0
#for item in all_tags:
#  sheet1['F' + str(rowctr+relatedctr)] = item
#  sheet1['G' + str(rowctr+relatedctr)] = all_tags[item]
#  relatedctr = relatedctr + 1

wb1.save('./excel/hashtag_competitor.xlsx')
wb1.close()

#https://knawab.medium.com/find-relevant-top-hashtags-using-python-part-2-88fc00fec63