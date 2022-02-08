import requests
import bs4


def getData(infor):
    headers = {"cookie": "over18=1"}
    # 建立headers用來放要附加的cookie
    request = requests.get(infor[0], headers=headers)
    # 將網頁資料利用requests套件GET下來並附上cookie
    data = bs4.BeautifulSoup(request.text, "html.parser")
    titles = data.find_all("div", class_="title")
    # 解析網頁原始碼
    infor = [""]
    # 將infor內清空
    i = 1
    for title in titles:
        if title.a != None:
            if "兔" not in title.a.text:
                infor.insert(i, "https://www.ptt.cc" +title.a["href"]+" "+title.a.text+"\n")
                i = i+1
    # 利用for迴圈把資料放進infor[1]開始的位置內並篩選掉已被刪除的文章
    prePage = data.find("a", class_="btn wide", text="‹ 上頁")
    newUrl = "https://www.ptt.cc"+prePage["href"]
    # 抓取上頁按鈕內URL
    infor[0] = newUrl
    return infor


    # 將newUrl放進infor[0]再把infor傳出去
infor = ["https://www.ptt.cc/bbs/Pet_Get/index.html"]
# 抓PTT領養版的網頁原始碼
Number_of_files = 3
Number_of_pages = 5
# 設變數方便設定檔案數跟頁數
for x in range(1, Number_of_files+1, 1):
    file = open("Pet_Get"+str(x)+".txt", "w", encoding="utf-8")
    for i in range(1, Number_of_pages+1, 1):
        file.write("--------------------第" +str(Number_of_pages*(x-1)+i)+"頁--------------------\n")
        file.write(infor[0]+"\n")
        infor = getData(infor)
        for inf in infor[1:]:
            file.write(inf)
    file.close()
# 寫入資料
for x in range(1, Number_of_files+1, 1):
    read = open("Pet_Get"+str(x)+".txt", encoding="utf-8")
    print(read.read())
    read.close()
# 讀取檔案中資料並印出
