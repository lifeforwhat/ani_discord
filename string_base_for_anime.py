import re, os
media_ext_list = ['mkv','avi','qtff','mp4','asf','mov','wmv','mpg','mpeg','mpe','asf','asx','flv','ts','tp','3gp','bik','webm','av1']

subtitle_ext_list = ['srt','ass','smi','sub','sami','vtt','usf','ssa','psb']

def FindFirst (first, word):
    Remover_1 = word.find(first)
    Result = word[Remover_1:]
    return Result

def FindExceptFirst (first, word):
    Remover_1 = word.find(first)
    Result = word[Remover_1 + len(first):]
    return Result

def FindEnd (end, word):
    Remover_2 = word.find(end)
    Result = word[:Remover_2]
    return Result

def mpaa_translate(word):
    word = word.lower().replace('tv-y','6')
    word = word.lower().replace('tv-y7', '9')
    word = word.lower().replace('tv-g', '6')
    word = word.lower().replace('tv-pg', '12')
    word = word.lower().replace('tv-14', '15')
    word = word.lower().replace('tv-ma', '19')
    return word


def Clear_All_Bracket(word): #'(' , ')' , '[' , ']' 을 지운다
    while word.count('<')>0 and word.count('>')>0:
        if word.find('<') > word.find('>'):
            word = word[:word.find(r'<')]
        word = word[:word.find(r'<')] + word[word.find(r'>')+1:]
    while word.count('(')>0 and word.count(')')>0:
        if word.find('(') > word.find(')'):
            word = word[:word.find(r'(')]
        word = word[:word.find(r'(')] + word[word.find(r')')+1:]
    while word.count('[')>0 and word.count(']')>0:
        if word.find('[') > word.find(']'):
            word = word[:word.find(r'[')]
        word = word[:word.find(r'[')] + word[word.find(r']')+1:]
    word = word.replace('  ', '').strip()
    return word

def Except_First_To_And_After_Except_Second(first, second, word): #first까지 자르고 그 후 다시 찾아서 second까지 자름
    result = FindExceptFirst(first, word)
    result = FindEnd(second , result)
    return result

def find_year(text):
    year_list = re.findall('\d{4}', text)
    for year in year_list:
        try:
            year = int(year)
        except:
            continue
        if year > 1900 and year < 2030 and year != 1920:
            break
        year = "NO"
    try:
        int(year)
    except:
        return ""
    return year


def text_normalize_for_foldername(text):
    text = text.replace(':','-')
    text = text.replace('\\',' ')
    text = text.replace('/', ' ')
    text = text.replace('*', ' ')
    text = text.replace('?', '？')
    text = text.replace('"', ' ')
    text = text.replace('<', '《')
    text = text.replace('>', ' 》')
    text = text.replace('|', '｜')
    return text

def read_filename_analyze_v2(file):
    season_list = []
    title_list = []

    if len(re.findall('s\d+', file, re.I)) > 0:
        s = re.findall('s\d+', file, re.I)[0]

        title = file[: file.find(s)]
        title_list.append(title.replace('.', ' ').strip().lower())

        s = re.findall('\d+', s, re.I)[0]
        season_list.append(int(s))

    if len(re.findall('Season\d+', file, re.I)) > 0:
        s = re.findall('Season\d+', file, re.I)[0]

        title = file[: file.find(s)]
        title_list.append(title.replace('.', ' ').strip().lower())

        s = re.findall('\d+', s, re.I)[0]
        season_list.append(int(s))

    if len(re.findall('\d+x\d+', file, re.I)) > 0:
        s = re.findall('\d+x\d+', file, re.I)[0]

        title = file[: file.find(s)]
        title_list.append(title.replace('.', ' ').strip().lower())

        s = re.findall('\d+x', s, re.I)[0].replace('x', '').replace('X', '').strip()
        season_list.append(int(s))

    if len(re.findall('시즌\d+', file, re.I)) > 0:
        s = re.findall('시즌\d+', file, re.I)[0]

        title = file[: file.find(s)]
        title_list.append(title.replace('.', ' ').strip().lower())

        s = re.findall('\d+', s, re.I)[0].replace('x', '').strip()
        season_list.append(int(s))

    if len(re.findall('\d+-\d+', file, re.I)) > 0:
        s = re.findall('\d+-\d+', file, re.I)[0]

        title = file[: file.find(s)]
        title_list.append(title.replace('.', ' ').strip().lower())

        s = re.findall('-\d+', s, re.I)[0].replace('-', '').strip()
        season_list.append(int(s))

    episode_list = []

    if len(re.findall('e\d+', file, re.I)) > 0:
        e = re.findall('e\d+', file, re.I)[0]
        e = re.findall('\d+', e, re.I)[0]
        episode_list.append(int(e))

    if len(re.findall('Season\d+ \d+', file, re.I)) > 0:
        e = re.findall('Season\d+ \d+', file, re.I)[0]
        e = re.findall(' \d+', e, re.I)[0].replace(' ', '').strip()
        episode_list.append(int(e))

    if len(re.findall('\d+x\d+', file, re.I)) > 0:
        e = re.findall('\d+x\d+', file, re.I)[0]
        e = re.findall('x\d+', e, re.I)[0].replace('x', '').replace('X', '').strip()
        episode_list.append(int(e))

    if len(re.findall('ep\d+', file, re.I)) > 0:
        e = re.findall('ep\d+', file, re.I)[0]
        e = re.findall('\d+', e, re.I)[0].replace('x', '').strip()
        episode_list.append(int(e))

    if len(re.findall('s\d+_\d+', file, re.I)) > 0:
        e = re.findall('s\d+_\d+', file, re.I)[0]
        e = re.findall('_\d+', e, re.I)[0].replace('_', '').strip()
        episode_list.append(int(e))

    if len(re.findall('\d+화', file, re.I)) > 0:
        e = re.findall('\d+화', file, re.I)[0]
        e = re.findall('\d+', e, re.I)[0].replace('_', '').strip()
        episode_list.append(int(e))

    if len(re.findall('\d+회', file, re.I)) > 0:
        e = re.findall('\d+회', file, re.I)[0]
        e = re.findall('\d+', e, re.I)[0].replace('_', '').strip()
        episode_list.append(int(e))

    if len(re.findall('\.\d+\.', file, re.I)) > 0:
        e = re.findall('\.\d+\.', file, re.I)[0]
        e = re.findall('\d+', e, re.I)[0].replace('.', '').strip()
        episode_list.append(int(e))

    if len(re.findall('시즌\d+_\d+', file, re.I)) > 0:
        e = re.findall('시즌\d+_\d+', file, re.I)[0]
        e = re.findall('_\d+', e, re.I)[0].replace('_', '').strip()
        episode_list.append(int(e))

    if len(re.findall('시즌\d+-\d+', file, re.I)) > 0:
        e = re.findall('시즌\d+-\d+', file, re.I)[0]
        e = re.findall('-\d+', e, re.I)[0].replace('-', '').strip()
        episode_list.append(int(e))

    if len(re.findall('시즌\d+ \d+', file, re.I)) > 0:
        e = re.findall('시즌\d+ \d+', file, re.I)[0]
        e = re.findall(' \d+', e, re.I)[0].replace(' ', '').strip()
        episode_list.append(int(e))

    ext = os.path.splitext(file)[1].lower()
    if len(season_list) == 0 :
        if len(episode_list) == 0 :
            print(file, '에서 시즌을 찾을 수 없습니다.')
            return ""
        elif len(episode_list) != 0 :
            season_list = "1"
    if len(episode_list) == 0 :
        print(file, '에서 에피소드를 찾을 수 없습니다.')
        return ""

    filename = file.lower()
    source = ""
    if filename.count('web') > 0 : source = 'web'
    elif filename.count('brrip') > 0 : source = 'bluray'
    elif filename.count('bdrip') > 0:
        source = 'bluray'
    elif filename.count('bluray') > 0 : source = 'bluray'
    elif filename.count('hdtv') > 0:
        source = 'hdtv'
    return {'title': title.strip(), 'filename': file.strip(), 'season': str(season_list[0]).strip(), 'episode': str(episode_list[0]).strip(), 'source': source,
            'folder_name': "", 'ext': ext}

def read_filename_analyze(fullFilename):
    folder_name = os.path.split(os.path.split(fullFilename)[0])[0].lower()
    filename = os.path.split(fullFilename)[1].lower()
    ext = os.path.splitext(fullFilename)[1].lower()
    if len(re.findall('s\d+', filename, re.I)) > 0 :
        season = re.findall('s\d+', filename, re.I)[0].replace('s','').replace('S','').strip()
        title = filename[: filename.find(season) -1 ].lower().replace('.', ' ').strip()
    elif len(re.findall('\d+x\d+', filename, re.I)) :
        season = re.findall('\d+x\d+', filename, re.I)[0]
        season = re.findall('\d+x',season,re.I)[0].replace('x','').strip()
        title = filename[: filename.find(season)].lower().replace('.', ' ').strip()
    elif len(re.findall('season\d+ \d+', filename, re.I)) :
        season = re.findall('season\d+ \d+', filename, re.I)[0]
        season = re.sub('season','',re.findall('season\d+',season,re.I)[0].strip(), re.I)
        title = filename[: filename.find(season) -6].lower().replace('.', ' ').strip()

    try: season
    except:
        print(fullFilename,'에서 시즌을 찾을 수 없습니다.')
        return ""
    if len(re.findall('e\d+',filename , re.I)) > 0 :
        episode = re.findall('e\d+',filename , re.I)[0].replace('e','').replace('E','').strip()
    elif len(re.findall('\d+x\d+', filename, re.I)):
        episode = re.findall('\d+x\d+', filename, re.I)[0]
        episode = re.findall('x\d+', episode, re.I)[0].replace('x', '').strip()
    elif len(re.findall('ep\d+', filename, re.I)):
        episode = re.findall('ep\d+', filename, re.I)[0]
        episode = re.findall('\d+', episode, re.I)[0].strip()
    elif len(re.findall('season\d+ \d+', filename, re.I)) :
        episode = re.findall('season\d+ \d+', filename, re.I)[0]
        episode = re.findall('\d+',episode,re.I)[-1]
    try:episode
    except:
        print(fullFilename,'에서 에피소드를 찾을 수 없습니다.')
        return ""

    source = ""
    if filename.count('web') > 0 : source = 'web'
    elif filename.count('brrip') > 0 : source = 'bluray'
    elif filename.count('bluray') > 0 : source = 'bluray'
    elif filename.count('hdtv') > 0:
        source = 'hdtv'
    return {'title' : title, 'filename' : filename, 'season' : season , 'episode' : episode, 'source' : source , 'folder_name' : folder_name, 'ext' : ext}

def file_renamer_for_mid(fullFilename):
    if os.path.isdir(fullFilename) == True:
        return ""
    file_info = read_filename_analyze(fullFilename)
    file = file_info['title'] + " S" + file_info['season'] + "E" + file_info['episode'] + " " + file_info['source']
    file = file.strip() + file_info['ext']
    try:os.renames(fullFilename, os.path.join(os.path.split(fullFilename)[0], file))
    except FileExistsError :
        os.remove(fullFilename)

def clear_folder_name_for_daum(text):
    # 년도까지 짤라주고, 그 가운데에 영어 시작점부터 년도 시작하는 점까지 잘라준다.
    year_list = re.findall('\d{4}', text)
    for year in year_list:
        try:
            year = int(year)
        except:
            continue
        if year > 1900 and year < 2030 and year != 1920:
            break
    try:
        int(year)
    except:
        print(text, '에서 year를 찾을 수 없습니다. 최대한 CLEAR 합니다.')
        text = text.lower()
        clear_list = open('clear.txt', 'r').read().split('\n')
        for a in clear_list:
            if a.count("#") > 0:  # 샾이 들어가면 좌 우 스페이스를 고려해준다.
                text = text.replace(' ' + a + ' ', '').strip()
                continue
            text = text.replace(a, '').replace('  ', ' ').strip()
        print(text)
        return text

    korean_name = find_korean(text)
    total_name = korean_name + "(" + str(year) + ")"
    return total_name

def find_korean(text):
    hangul = re.compile('[ㄱ-ㅣ가-힣|\d|\s]+')
    result = hangul.findall(text)
    try:
        return result[0]
    except:
        text

def find_korean_syllable(text):
    hangul = re.compile('[ㄱ-ㅎ가-힇]')
    result = hangul.findall(text)
    return result

def subtitle_is_english_or_korea(text) :
    hangul = re.compile('[ㄱ-ㅣ가-힣|]+')
    result = hangul.findall(text)
    if len(result) > 100 : # 적어도 한글 단어가 10개 이상 있으면 한글 자막이라고 판단한다.
        return "ko"
    return ""

def clear_folder_name(text):
    text = text.lower()
    clear_list = open('clear.txt','r').read().split('\n')
    for a in clear_list:
        if a.count("#") > 0 : # 샾이 들어가면 좌 우 스페이스를 고려해준다.
            text = text.replace(' '+a+' ','').strip
            continue
        text = text.replace(a, '').replace('  ',' ').strip()

    return text
