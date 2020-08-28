import requests

#URL = "https://api.themoviedb.org/3/movie/550?api_key=629b1dbf49450758fdd0904c55158104"

site = "https://api.themoviedb.org/3/movie/"
movieID = "280"
api_key = "?api_key=629b1dbf49450758fdd0904c55158104"

URL = site+movieID+api_key

r = requests.get(url = URL)

data = r.json()

print(data['title'] )
print('\n')
print(data['genres'] )
