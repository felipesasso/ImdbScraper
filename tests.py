import unittest

from imdb_scraper import ImdbScraper


class BaseUrlUT(unittest.TestCase):

    def setUp(self):
        pass

    def test_base_url_https(self):
        full_url = 'https://www.imdb.com/title/tt0944947/?ref_=nv_sr_1?ref_=nv_sr_1'
        expected_base_url = 'https://www.imdb.com'
        imdbshowrates = ImdbScraper(url=full_url)
        self.assertEqual(imdbshowrates.get_base_url(), expected_base_url)

    def test_base_url_http(self):
        full_url = 'http://www.imdb.com/title/tt0944947/?ref_=nv_sr_1?ref_=nv_sr_1'
        expected_base_url = 'http://www.imdb.com'
        imdbshowrates = ImdbScraper(url=full_url)
        self.assertEqual(imdbshowrates.get_base_url(), expected_base_url)

    def test_base_url_not_found(self):
        full_url = 'www.imdb.com/title/tt0944947/?ref_=nv_sr_1?ref_=nv_sr_1'
        imdbshowrates = ImdbScraper(url=full_url)
        with self.assertRaises(ValueError):
            imdbshowrates.get_base_url()

class SeasonDictUT(unittest.TestCase):

    def test_is_dict(self):
        full_url = 'https://www.imdb.com/title/tt0944947/?ref_=nv_sr_1?ref_=nv_sr_1'
        imdbshowrates = ImdbScraper(url=full_url)
        page = imdbshowrates.get_page(full_url)
        season_url = imdbshowrates.get_seasons_url(page)
        self.assertEqual(isinstance(season_url, dict), True)

    def test_get_episodes_dict(self):
        full_url = 'https://www.imdb.com/title/tt0165598/?ref_=nv_sr_1?ref_=nv_sr_1'
        imdbshowrates = ImdbScraper(url=full_url)
        episodes_dict = imdbshowrates.get_rates()
        self.assertEqual(isinstance(episodes_dict, dict), True)


if __name__ == '__main__':
    unittest.main()
