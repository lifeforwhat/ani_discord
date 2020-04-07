import os
import requests
import shutil

import string_base_for_anime
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook , DiscordEmbed

def trObjToDiction(tr):
    try:
        s = tr.select('td')
        s0 = s[0]
        s1 = s[1]
        title = s1.select('a')[-1].text
        s2 = s[2]
        magnet = s2.select('a')[-1]['href']
        s3 = s[3]
        size = s3.text
        s4 = s[4]
        date = s4.text
        s5 = s[5]
        seeder = s5.text
        if int(seeder) == 0 :
            return False
        s6 = s[6]
        leecher = s6.text
        s7 = s[7]
        downloaded = s7.text
        result = {'title' : title , 'size' : size, 'date':date, 'seeder' : seeder , 'leecher' : leecher, 'downloaded' : downloaded , 'magnet' : magnet}
        return result
    except:
        return False



def find_suitable_torrents(name):
    res = requests.get('https://nyaa.si/?f=0&c=0_0&q='+name)
    soup = BeautifulSoup(res.text , 'html.parser')
    table = soup.select('tr')
    list = []
    for item in table:
        info_dict = trObjToDiction(item)
        if info_dict == False:
            continue
        list.append(info_dict)
    return list

import time, random
def myanime_search(name):
    # https://myanimelist.net/search/prefix.json?type=all&keyword=Ace%20of%20Diamond%20Act%20II%20-%2052%20%5B1080p%5D%20&v=1
    new_name = string_base_for_anime.Clear_All_Bracket(name)
    res = requests.get('https://myanimelist.net/search/prefix.json?type=all&keyword=%s&v=1' % (os.path.splitext(new_name.strip())[0]).strip())
    if res.status_code != 200:
        time.sleep(random.randint(3,10))
        return myanime_search(name)
    return  res.json()

def input_subtitle(subPath):
    filename = os.path.split(subPath)[1]

    search_name_for_myanime = myanime_search(filename)
    try:
        img = search_name_for_myanime['categories'][0]['items'][0]['image_url']
    except:
        img = ""

    info = find_suitable_torrents(os.path.splitext(filename)[0])
    if filename.count('720') > 0:
        info += find_suitable_torrents(os.path.splitext(filename.replace('720','1080'))[0])
    if len(info) == 0 :
        return False
    webhook = DiscordWebhook(
        url='', ############################################ 웹훅
        username='애니')
    description = ""
    for item in info:
        n_magnet = item['magnet']
        n_magnet = n_magnet[:n_magnet.find('&')]
        description = description + "\n\ntitle : %s \n size : %s \n date : %s \n S,L,D : %s , %s , %s \n magnet : %s" % (item['title'].strip(), item['size'], item['date'] , item['seeder'], item['leecher'] , item['downloaded'] , n_magnet)
    #embed = DiscordEmbed(title=filename)
    try:
        rec_title = search_name_for_myanime['categories'][0]['items'][0]['name']
    except:
        rec_title = os.path.splitext(filename)[0]
    embed = DiscordEmbed(title = rec_title)
    #embed.set_author(name='Author Name', url='author url', icon_url='author icon url')
    embed.set_image(url=img)
    embed.set_footer(text=description.strip())
    with open(subPath, "rb") as f:
        filename = os.path.split(subPath)[1]
        webhook.add_file(file=f.read(), filename=filename)
        webhook.add_embed(embed)
    response = webhook.execute()
    pass

# [Ohys-Raws]
def file_keep_going(file):
    if file[0] != '[':
        return "NO"
    a = string_base_for_anime.find_korean_syllable(file)
    if len(a) == 0:
        return "YES"
    return "NO"

if __name__ == '__main__':
    while True:
        import os
        from sqlitedict import SqliteDict
        src = r'C:\자막'
        for (path, dir, files) in os.walk(src):
            for filename in files:
                f_go = file_keep_going(filename)
                if f_go != "YES":
                    continue
                ext = os.path.splitext(filename)[-1].lower()
                if ext in ['.smi' , '.ass']:
                    with SqliteDict('업로드완료.db') as db:
                        if filename in db:
                            continue
                    full = os.path.join(path, filename)
                    result = input_subtitle(full)
                    with SqliteDict('업로드완료.db') as db:
                        if filename not in db:
                            db[filename] = True
                            db.commit()
                    if result == False:
                        continue
        time.sleep(300)
