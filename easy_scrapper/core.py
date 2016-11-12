import urllib2
import logging

from random import choice, randint
from os.path import exists
from time import sleep
from os import getenv

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
    datefmt="%d/%b/%Y %H:%M:%S",
    level=getenv('LOG_LEVEL', logging.DEBUG)
)
logger = logging.getLogger(__name__)


class EasyScrapper(object):
    """
    Simple and Fast Scrapper base object to implement dataset scrappers.
    It provides a set of method to make it faster and better.
    Support:
    - User Agents
    - Web Proxies
    """
    DEFAULT_USER_AGENTS = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
        'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    ]
    DEFAULT_PROXIES = [
        '97.77.104.22:80',
        '188.213.143.119:8118',
        '47.88.137.179:8080',
        '12.41.141.10:8080'
    ]

    def __init__(self, proxies_filename='./proxies.txt', user_agents_filename='./user_agents.txt'):
        """
        Initialize the ojects and all the needed resources.

        :param proxies_filename filename to the proxy list separated by new line
        :param user_agents_filename filename to the user agenst list separated by new line
        """
        self.proxies = self.load_data_list(proxies_filename, self.DEFAULT_PROXIES)
        self.user_agents = self.load_data_list(user_agents_filename, self.DEFAULT_USER_AGENTS)

    def load_data_list(self, filename, defaults):
        """
        Load an array from a file that contains one value per line. For example:
        ```
        a
        b
        c
        ```
        will return
        ['a', 'b', 'c']

        :param filename the filename containing the list
        :param defaults the default list if the file does not exist.
        :returns the array with all the loaded elements
        """
        logger.info("Loading data from {}...".format(filename))
        all_data = []
        if exists(filename):
            with open(filename, 'r+') as fp:
                data = fp.read()
                all_data = data.split("\n")
        else:
            return defaults
        return all_data

    def save_data_list(self, filename, data):
        """
        Save a list into a folder, one element per line.

        :param filename the filename to save/create/override
        :param data the list to save
        """
        logger.info("Saving data to {}...".format(filename))
        with open(filename, 'w+') as fp:
            fp.write("\n".join(data))

    def sleep(self, seconds_from, seconds_to):
        """
        Sleep a random number of seconds between seconds_from and seconds_to. For example:
        self.sleep(2, 30) will sleep ramdomly between 2 and 30 seconds.

        :param seconds_from lower limit for the seconds to sleep
        :param seconds_to upper limit for the seconds to sleep
        """
        time_to_sleep = randint(seconds_from, seconds_to)
        logger.info("Going to sleep for {} seconds...".format(time_to_sleep))
        sleep(time_to_sleep)

    def download_data(self, url, referer='http://www.google.com/', use_proxy=False, retries=1):
        """
        Download all the data from the url faking the referer and user-agent. This method has the
        power to use proxies and perform retries if the download fails.

        :param url the url of the file to download
        :param referer the url to send as referer (Identifies the address of the webpage that linked to the resource being requested)
        :param use_proxy if TRUE it will download the resource using a proxy listed in the proxies file, if FALSE it will download it directly.
        :param retries is the number of retries to try to download the resource if fails.
        :returns the url data
        """
        iteration = 0
        while iteration <= retries:
            try:
                the_proxy = choice(self.proxies)
                if use_proxy:
                    logger.info("Downloading {} through {} and retry {}/{} times.".format(url, the_proxy, iteration, retries))
                else:
                    logger.info("Downloading {} and retry {}/{} times.".format(url, iteration, retries))

                if use_proxy:
                    # Enable Proxies
                    urllib2.install_opener(
                        urllib2.build_opener(
                            urllib2.ProxyHandler({'http': the_proxy})
                        )
                    )

                req = urllib2.Request(url, headers={
                    'referer': referer,
                    'User-Agent': choice(self.user_agents)
                })
                data = urllib2.urlopen(req).read()

                if use_proxy:
                    # Disable all proxies
                    urllib2.install_opener(
                        urllib2.build_opener(
                            urllib2.ProxyHandler({})
                        )
                    )
                return data

            except Exception:
                iteration += 1
                logger.error("Download failed. Retry: {}".format(iteration))

        raise Exception("Download failed: {}".format(url))

    def start(self, *args, **kwargs):
        """
        Method to override and create all the needed logic you need.
        """
        raise NotImplemented
