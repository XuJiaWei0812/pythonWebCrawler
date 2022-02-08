import json
import time
import requests
from pathlib import Path
from threading import Thread
from datetime import datetime
from fake_useragent import UserAgent


class DailyPriceSpider:

    def __init__(self):
    
        # 重複使用 TCP 連線
        self.req = requests.Session()
        self.url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY"
        self.headers = self.req.headers
        
        # 偽裝 User-Agent
        ua = UserAgent()
        self.headers["User-Agent"] = ua.random
 
    # 供內部使用
    def __get(self, date, stock_no):
        res = self.req.get(self.url,
                           headers = self.headers,
                           params={
                               "response": "csv",  # 這次抓的是 csv 格式
                               "date": date,
                               "stockNo": stock_no
                           })
        return res
    
    # 供內部使用
    def __save_file(self, res_text, path):
        # 去掉 res_text 裡多餘的空白行
        res_text = '\n'.join(
            filter(None,
                   res_text.splitlines()
                   )
        )

        path = Path(path)
        # parents=True，如果父資料夾不存在則會一併創建
        # exist_ok=True，創建資料夾時，該資料夾已存在則不會 throw exception
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # 這邊我比較懶一點，是直接覆蓋整個檔案，可以依照個人喜好去修改
        with open(path, 'w', encoding="utf-8") as file:
            file.write(res_text)
        return
 
    # 把上面的兩個 function 整合成一個 function，供外部使用
    def scrape(self, date, stock_no, save_path=""):
        res = self.__get(date, stock_no)
        if save_path:
            res_text = res.text
            self.__save_file(res_text, save_path)
        # 雖然這邊沒用到但還是可以先 return response 保留日後擴充彈性
        return res

if __name__ == '__main__':
    SAVE_PATH_ROOT = "./daily_stock_price/"
    SLEEP_TIME = 3
    
    # 之前有實作過抓取股票清單的程式了，我們直接讀取清單裡的內容來使用
    # 程式實作篇章傳送門請至本篇文章最上面
    stock_info_list_file = {}
    with open("./stock_info_list.json", "r", encoding="utf-8") as f:
        stock_info_list_file = json.load(f)

    # 不管日期是幾號，他回傳都是給我們一整個月的，所以就固定設成1號就好
    # strftime()，把 datetime 輸出成我們要的格式
    today_date = "{}01".format(datetime.now().strftime("%Y%m"))

    stock_info_list = stock_info_list_file.get("stock", [])
    dps = DailyPriceSpider()
    req_thread_list = []

    for stock_info in stock_info_list:

        stock_no = stock_info.get("stockNo")
        stock_name = stock_info.get("stockName")
        stock_industry = stock_info.get("stockIndustry")
        file_name = "{}_{}_daily_price.csv".format(
            today_date[:-2],  # 字串只需要用到年跟月
            stock_no+stock_name)

        save_path = "{}/{}/{}/{}".format(SAVE_PATH_ROOT,
                                         stock_industry,
                                         stock_no+stock_name,
                                         file_name)

        if stock_no and stock_name and stock_industry:
            # daemon=True，就是 main 結束時，daemon=True 的執行緒也會跟著結束
            req_thread = Thread(target=dps.scrape,
                                args=(today_date, stock_no, save_path),
                                daemon=True)
            req_thread.start()
            req_thread_list.append(req_thread)
            time.sleep(SLEEP_TIME)

    for req_thread in req_thread_list:
        req_thread.join()

    print("Finished")