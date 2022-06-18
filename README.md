# pythonWebCrawler python網路爬蟲
 
必要套件:
pip install requests
pip install Beautifulsoup4
pip install UserAgent

img_donwnload.py : 用來爬取並下載照片

lotto.py : 爬取大樂透對獎號碼

ppt.py : 爬取ppt文章標題及連結

stock_no.py、stock_info.py : 先執行stock_no產生stock_info_list.json檔案(爬取股票代號、名稱、行業類別)，再利用json檔案去執行stock_info(爬取股票代號、名稱、行業類別、交易金額等詳細資料)
