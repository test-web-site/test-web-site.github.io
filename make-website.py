import os
import sys
import shutil
import requests

from pytube import Playlist
from pytube import YouTube

SERMON_INJ = '''
                <div class="col-lg-4 templatemo-item-col all">
                  <div class="meeting-item">
                    <a href="%s">
                    <div class="thumb">
                      <div class="price">
                        <span><i class="fa fa-play" aria-hidden="true"></i></span>
                      </div>
                      <img src="%s" alt="">
                    </div>
                    </a>
                    <div class="down-content">
                      <div class="date">
                          <h6>%s년 %s월 <span>%s일</span></h6>
                      </div>
                      <a href="https://www.youtube.com/watch?v=hdJuxKBK3FE&list=PLYVmVd0kt83di-vtfFo6FY68Zm8IEhS5M&index=1"><h4>%s</h4></a>
                      <p>위남환 목사<br>%s</p>
                    </div>
                  </div>
                </div>
'''



def rmdir(dir):
    try: shutil.rmtree(dir)
    except: pass

def mkdir(dir):
    try: os.makedirs(dir)
    except: pass

def copy(src_path, dst_path):
    try: shutil.copy2(src_path, dst_path)
    except: pass

def download_img(url, target_path):
    img_data = requests.get(url).content
    with open(os.path.join(target_path), 'wb') as handler:
        handler.write(img_data)

def get_description(yt):
    for n in range(6):
        try:
            description =  yt.initial_data["engagementPanels"][n]["engagementPanelSectionListRenderer"]["content"]["structuredDescriptionContentRenderer"]["items"][1]["expandableVideoDescriptionBodyRenderer"]["attributedDescriptionBodyText"]["content"]
            return description
        except:
            continue
    return False

def make_sermon():
    tmp_name = "sermon_template.html"
    rmdir("sermon")
    mkdir("sermon")
    mkdir("sermon/thumbnail")
    URL_PLAYLIST = "https://www.youtube.com/playlist?list=PLYVmVd0kt83di-vtfFo6FY68Zm8IEhS5M"

    # Retrieve URLs of videos from playlist
    playlist = Playlist(URL_PLAYLIST)
    len_playlist = len(playlist.video_urls)
    print('Number Of videos in sermon playlist: %s' % len_playlist)

    page_num = int(len_playlist/9) + 1

    urls = []
    for url in playlist:
        urls.append(url)

    print (SERMON_INJ)

    for page in range(page_num):
        plus_num = 9
        if page == int(len_playlist/9):
            plus_num = int(len_playlist % 9)

        with open(tmp_name, "r") as f:
            sermon_template = f.read()

        sermon_list = ""


        start_url_idx = page * 9
        print ("go")

        for video_idx in range(start_url_idx, start_url_idx + plus_num):
            url = urls[video_idx]
            id = url.split("=")[-1]
            thumbnail_url = "sermon/thumbnail/%s.jpg" % id

            yt = YouTube(url)
            stream = yt.streams.first()
            description = get_description(yt)
            sermon_description = ""
            if description != False:
                sermon_description = description.split("본문")[1].split(":", 1)[1].split("\n")[0].strip()

            sermon_title = yt.title.split("]")[-1].strip().rsplit(" ", 1)[0]
            sermon_date = yt.title.split("]")[-1].strip().rsplit(" ", 1)[1].split("-")
            sermon_year = sermon_date[0]
            sermon_month = sermon_date[1]
            if len(sermon_month)== 2 and sermon_month[0] == '0':
                sermon_month = sermon_month[1]
            sermon_day = sermon_date[2]
            if len(sermon_day) == 2 and sermon_day[0] == '0':
                sermon_day = sermon_day[1]

            print (sermon_title, sermon_year, sermon_month, sermon_day)

            download_img("https://img.youtube.com/vi/%s/maxresdefault.jpg" % id, thumbnail_url)

            sermon_list += SERMON_INJ % (url, "thumbnail/%s.jpg" % id, sermon_year, sermon_month, sermon_day, sermon_title, sermon_description)
            sermon_list += "\n"

        real_page_count = page + 1
        final_page = sermon_template.replace("[SERMON_LIST]", sermon_list)

        ## Pagenation
        last_page_id = int((page_num-1) / 5) + 1
        print (last_page_id)

        pagenation = ""
        if real_page_count >= 6:
            pagenation += '''
                  <li><a href="%s"><i class="fa fa-angle-left"></i></a></li>
''' % ("%s.html" % (int((real_page_count-1)/5) * 5))

        page_holder = (int((real_page_count-1) / 5) +1) * 5

        last = 0
        if int((real_page_count-1)/5)+1 != last_page_id:
            last = page_holder + 1
        else:
            last = page_num + 1

        for i in range(page_holder - 4, last):
            if real_page_count == i:
                pagenation += '''
                  <li class="active"><a href="%s.html">%s</a></li>
''' % (i, i)
            else:
                pagenation += '''
                  <li><a href="%s.html">%s</a></li>
''' % (i, i)
                  ##<li class="active"><a href="#">2</a></li>

        if int((real_page_count-1)/5)+1 != last_page_id:
            pagenation += '''
                  <li><a href="%s"><i class="fa fa-angle-right"></i></a></li>
''' % ("%s.html" % (((int((real_page_count-1) / 5) +1) * 5) + 1))



        final_page = final_page.replace("[PAGE_NATION]", pagenation)


        with open("sermon/%s.html" % real_page_count, "w") as f:
            f.write(final_page)
        print()


    print(urls)



make_sermon()
