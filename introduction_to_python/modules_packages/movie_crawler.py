import requests

url = 'https://movies.yahoo.com.tw/movie_thisweek.html'
res = requests.get(url)
print(res.text)