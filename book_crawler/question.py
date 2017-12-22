import string
import pprint

# Todo: 匯入你需要的函式庫 (hint: requests, BeautifulSoup, csv)
# import
# import
# import


# 用來清除字串中不要的標點符號
def strclear(text, newsign=''):
    signtext = string.punctuation + ' ' + '｜' + '、' + '：' + '－' + newsign
    signrepl = '@' * len(signtext)
    signtable = str.maketrans(signtext, signrepl)
    return text.translate(signtable).replace('@', '')


# Todo: 定義你要爬的連結們，可以分別上兩個網站去看一下
# TENLONG_URL =
# BOOKS_URL =


# Todo: 完成下面的函式，取得天瓏書局的搜尋結果
def get_tenlong_page(url, keyword):
    params = {
        # 這三個欄位可以從 dev tool -> network 取得
        # 'utf8': '<here>',
        # 'authenticity_token': '<here>',
        # 'top-search-btn': None,
        
        # 這兩個欄位是自訂的關鍵字與頁數 
        # 'keyword': <here>,
        # 'page': <here>,
    }

    headers = {
        # User-Agent 是用來假裝自己是瀏覽器用的， 也可以從 dev tool -> network 取得
        # 'User-Agent': '<here>',
    }

    # 使用 requests 跟天瓏書局的伺服器要資料
    resp = requests.get(url, params=params, headers=headers)

    # status_code = 200 代表你成功要到電話了，其他都是要不到電話的，還記得嗎？
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        # pprint.pprint(resp.text)
        return resp.text


# Todo: 完成下面的函式，對天瓏書局的搜尋結果做資料處理，擷取我們要的書籍清單
def get_book_list(response):
    # Todo: 完成下面這一行，用 BeautifulSoup 來幫你將網頁內容(string) 轉為 DOM tree
    # soup = BeautifulSoup(<here>, 'html.parser')

    # Todo: 完成下面這一行，使用標籤名稱以及 class name 來取出所有的書本
    # books = soup.find_all('<here>', {'class': '<here>'})

    # result 用來存放所有的書籍資訊(空的筆記本)
    result = []

    # 將每一本書的資訊寫入筆記本中，除了最後一本(可以看網頁就知道為什麼要排除最後一本書)
    for book in books[:-1]:
        # 取得書名，並且對書名做預先處理，拿掉括號後面的文字，去除多餘字元
        title = book.h3.text.split('(')[0].strip()
        title = strclear(title)

        # 取得作者
        author = book.find('span', {'class': 'author'}).text.strip()
        
        # 取得價錢
        price = book.find('span', {'class': 'price'}
                          ).text.split('$')[1].strip()

        # Todo: 完成下面這一行，將結果存入 result 
        # result.append([{'title': <here>, 'author': <here>, 'price': <here>}])

    return result


# Todo: 完成下面的函式，取得博客來的搜尋結果
def get_books_page(url, keyword):
    # 將 url 中的 <keyword> 置換成我們要查詢的書名
    # url = url.replace('<keyword>', <here>)

    # 使用 requests 跟博客來的伺服器要資料
    resp = requests.get(url)

    # status_code = 200 代表你成功要到電話了，其他都是要不到電話的，還記得嗎？
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


# Todo: 完成下面的函式，對博客來的搜尋結果做資料處理，擷取我們要的書本資訊
def find_the_same_book(response, target_book):
    # Todo: 完成下面這一行，用 BeautifulSoup 來幫你將網頁內容(string) 轉為 DOM tree
    # soup = BeautifulSoup(<here>, 'html.parser')

    # 取得所有的書籍
    books = soup.find_all('li', {'class': 'item'})

    print('searching ', target_book, ' ...')

    # 在所有書籍當中找到我們要的那本書
    for book in books:
        # 取得書名
        title = book.a['title']

        # 對書名做處理，濾掉多餘的字元
        title = strclear(title)

        # 如果找到了同一本書，再去擷取這本書的作者與價錢，否則就繼續處理下一本書的書名
        if title == target_book:
            print('find the book, extracting the authors and price ...')

            # 取得作者(們)
            author = []
            for e in book.find_all('a', {'rel': 'go_author'}):
                author.append(e.text)

            # 取得價錢
            price = book.find('span', {'class': 'price'})('strong')[-1].b.text

            # Todo: 完成下面這一行，將書名、作者、價錢傳回去
            # return {'title': <here>, 'author': <here>, 'price': <here>}
    
    # 搜尋完所有的書，並沒有找到一樣的書，表示博客來可能沒有賣這本書
    print('Fail: can not find this book.')
    
    return {None}


# 搜尋某個關鍵字
def crawl_keyword(keyword):
    # get_tenlong_page 可以取得在天瓏書局搜尋某個關鍵字的網頁結果
    page = get_tenlong_page(TENLONG_URL, keyword)

    # 如果有取得網頁結果，則從其中取出我們要的書籍清單
    if page:
        book_list = extract_book_list(page)
    
    # 在博客來中搜尋我們整理好的書籍清單，每次搜尋一本書
    for book in book_list:
        # 取得書名
        book_name = book[0]['title']

        # get_books_page 以書名為關鍵字去搜尋博客來
        page = get_books_page(BOOKS_URL, book_name)

        # 如果有取得網頁結果，則從其中取出書籍資訊，並且存入book中，否則存 None
        if page:
            book_info = find_the_same_book(page, book_name)
            book.append(book_info)
        else:
            book.append({None})
    
    return book_list


# Todo: 完成下面的函式，將結果輸出成 CSV 檔
def output_to_csv(csvCursor, data, category):
    for entry in data:
        # Todo: 完成下面這一行，只有當這本書在兩個書局都有搜尋到，才要輸出
        # if entry[1] != <here>:
            csvCursor.writerow([
                # Todo: 完成下面這一行，可以看一下 CSV 標題的第一欄是什麼
                # <here>,
                
                entry[0]['title'],
                entry[0]['author'],
                entry[0]['price'],
                entry[1]['price']
            ])


if __name__ == '__main__':
    # Todo: 完成下面這一行，定義你要爬的關鍵字們
    # keywords = <here>

    # Todo: 完成下面這三行，建立用來輸出結果的物件，並且設定好標題欄位
    # file = <here>
    # csvCursor = <here>
    # csvHeader = <here>

    csvCursor.writerow(csvHeader)

    for keyword in keywords:
        result = crawl_keyword(keyword)
        output_to_csv(csvCursor, result, keyword)

    file.close()
