import re
import requests
from requests import URLRequired
import logging
from collections import OrderedDict
import pprint
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


class ImdbScraper:
    """ Get rating of every episode of a show from IMDB and save it in a
        dictionary structure
    """

    def __init__(self, url):
        """
            Args:
                url ('str'): Main imdb url of show
        """
        self.url = url

    def get_base_url(self):
        """ Extract base url from a full url
            Example: https://www.imdb.com/title/tt0944947/?ref_=nv_sr_1?ref_=nv_sr_1
            Extracts only https://www.imdb.com

            Args:
                url ('str'): Full url
            Returs:
                String: Base url
            Raises:
                ValueError: Could not fint base url in given url
        """

        r1 = re.compile(r"(?P<base_url>https*\:\/\/[\.\w\d]+).*")
        result = r1.match(self.url)
        if result:
            group = result.groupdict()
            base_url = group.get("base_url", None)
            log.info("Found base url {url}".format(url=base_url))
            return base_url

        raise ValueError(
            "Could not extract base url from {url}".format(url=self.url)
        )

    def get_page(self, url):
        """ Send a request and get page from url
            Args:
                url ('str'): Webpage url
            Returns:
                String: Webpage
            Raises:
                requests.URLRequired: Url is invalid
        """

        try:
            request = requests.get(url)
        except URLRequired as e:
            raise URLRequired("Provided URL is invalid")
        return request.text

    def get_seasons_url(self, html_doc):
        """ Get URL of each season and store each one in a dictionary
            Args:
                html_doc ('str'): HTML page
            Returns:
                dictionary: Mapping season number->url
            Raises:
                None

        """
        soup = BeautifulSoup(html_doc, "html.parser")
        seasons_section = soup.find("div", id="title-episode-widget")

        base_url = self.get_base_url()

        parsed_dict = {}

        for tag in seasons_section("a"):
            href = tag.attrs.get("href", None)
            if "episodes?season=" in href:
                parsed_dict[tag.text] = base_url + href

        return parsed_dict

    def get_all_episodes_rate(self, seasons_url_dict):
        """ Get rates of every episode of each season and save them in a dictionary object
            Args:
                seasons_url_dict ('dict'): Dict following bellow structure:
                    {season_number: season_url}
            Returns:
                dictionary: Dict with rates of every episode
            Raises:
                None

        """

        rates_dict = {}
        for season, url in seasons_url_dict.items():
            episodes_dict = self.get_season_episodes(url)
            rates_dict.setdefault("season", {}).setdefault(
                season, episodes_dict
            )

        return rates_dict

    def get_season_episodes(self, url):
        """ Get rates of each episode in a season
            Args:
                url: ('str'): Imdb url of a show season
            Returns:
                dictionary: following bellow structure:
                {
                    episode_name: rating
                }
            Raises:
                None
        """
        html_doc = self.get_page(url)
        soup = BeautifulSoup(html_doc, "html.parser")
        main = soup.find("div", id="main")
        episodes = main.findAll("div", {"itemprop": "episodes"})
        episodes_dict = OrderedDict()
        for episode in episodes:
            name = episode.findAll("a", {"itemprop": "name"})[0]
            title = name.attrs["title"]
            rating = episode.findAll(
                "span", {"class": "ipl-rating-star__rating"}
            )[0].getText()
            rating_dict = episodes_dict.setdefault(
                "title", OrderedDict()
            ).setdefault(title, {})
            rating_dict["rating"] = rating

        return episodes_dict

    def get_rates(self):
        """ Get rates of show
            Raises:
                None
            Returns:
                dictionary following bellow schema:
                {
                    'season': {
                        int(season number):
                            'title: {
                                str(title): {
                                    'rating': str(rating)
                                }
                            }
                    }

                }
        """
        page = self.get_page(self.url)
        seasons_url = self.get_seasons_url(page)
        all_ep_dict = self.get_all_episodes_rate(seasons_url)
        return all_ep_dict
