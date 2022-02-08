import requests  # 用來對網站發出請求的套件
import os  # 用來處理資料夾的套件
import bs4  # 用來解析HTML的套件


def saveImage(postUrl):  # 建立函式方便使用
    request = requests.get(postUrl)  # 對網頁發出請求
    data = bs4.BeautifulSoup(request.text, "html.parser")  # 以HTML格式解析網頁原始碼
    imageData = data.find_all('img')  # 抓取所有有<img>標籤內的資料
    path = r"D:\img"  # 存放照片的路徑
    if (os.path.exists(path) == False):  # 判斷主資料夾是否存在
        os.makedirs(path)  # 不存在就建立一個
    imgList = []  # 建立LIST用來放圖片URL
    lenth = len(imageData)  # 建立變數紀錄imageData內有幾筆資料
    for x in range(lenth):  # 建立用來迴圈放全部圖片URL 有幾個就放幾次
        imgList.insert(x, imageData[x].attrs["src"])  # 抓到src內的圖片連結並新增進imgList內
    for i in range(lenth):  # 用來印出全部圖片
        getImage = requests.get(imgList[i])  # 抓取圖片URL
        image = getImage.content  # 將圖片資訊轉成二進位制
        imageSave = open(path+"\img"+str(i)+".png", "wb")  # 建立檔案
        imageSave.write(image)  # 將圖片資訊寫入檔案內
        imageSave.close()  # 關檔
        print("img"+str(i)+".png"+"下載成功")  # 告知該圖片儲存成功


postUrl = "https://www.ptt.cc/bbs/Pet_Get/M.1631051441.A.6C7.html"  # 欲抓取圖片之網頁的URL
saveImage(postUrl)  # 執行函式
print("下載完成")  # 告知程式結束
