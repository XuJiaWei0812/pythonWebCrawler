import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

# 設置 index constant，數字代表我們要的資料在 list 的位置
TARGET_TABLE_INDEX = 1
STOCK_NO_INDEX = 2
STOCK_NAME_INDEX = 3
STOCK_INDUSTRY_INDEX = 6
# JSON settings
TITLE = "stock"
JSON_INDENT = 4

# 送出 HTTP Request
url = "https://isin.twse.com.tw/isin/class_main.jsp"
res = requests.get(url, params={
    "market": "1",
    "issuetype": "1",
    "Page": "1",
    "chklike": "Y"
}
, headers={
    "User-Agent": ua.random
})

# 處理編碼，使用預設 utf-8 的話 res.text 的內容會有亂碼
res.encoding = "MS950"
res_html = res.text

# Parse
soup = BeautifulSoup(res_html, "lxml")

# 因為這個 HTML 裡面有兩張 table
# 所以我們 find_all("table") 回傳的 list 的 length 會是 2
# 而我們要的資料在第二張
tr_list = soup.find_all("table")[TARGET_TABLE_INDEX].find_all("tr")

# tr_list 的第一個是 item 是欄位名稱
# 我們這邊用不到所以 pop 掉
tr_list.pop(0)

# 開始處理資料
result = []
for tr in tr_list:

    td_list = tr.find_all("td")

    # 股票代碼
    stock_no_val = td_list[STOCK_NO_INDEX].text

    # 股票名稱
    stock_name_val = td_list[STOCK_NAME_INDEX].text

    # 股票產業類別
    stock_industry_val = td_list[STOCK_INDUSTRY_INDEX].text

    # 整理成 dict 存起來
    result.append({
        "stockNo": stock_no_val,
        "stockName": stock_name_val,
        "stockIndustry": stock_industry_val
    })


# 將 dict 輸出成檔案
stock_list_dict = {TITLE: result}
with open("stock_info_list.json", "w", encoding="utf-8") as f:
    f.write(
        json.dumps(stock_list_dict,
                   indent=JSON_INDENT,
                   ensure_ascii=False)
    )