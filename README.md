# ImdbScraper
Get rating of every episode of a show from IMDB and save it in a dictionary structure
Usage
```python
url = 'https://www.imdb.com/title/tt0165598/?ref_=nv_sr_1?ref_=nv_sr_1'
imdbshowrates = ImdbScraper(url=full_url)
episodes_dict = imdbshowrates.get_rates()
