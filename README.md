# Easy Scrapper Base Tool
Easy Dataset Scrapper base objet to make dataset scrapper in a faster and secure way.

# Instalation
1. Install the base tool
```
pip install git+https://github.com/iuga/easy_dataset_scrapper
```
2. Create a proxy list ( only if needed ) with `vim proxies.txt`:
```
97.77.104.22:80
188.213.143.119:8118
47.88.137.179:8080
12.41.141.10:8080
```
3. Create the user agents list to use ( only if needed ) with `vim user_agents.txt`:
```
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1
Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A
```
4. Extend and define your own scrapper:
```python
from easy_scrapper.core import EasyScrapper

class MyEasyScrapper(EasyScrapper):

    savePath = '../images'

    # You need to override this method
    def start(self, beginIndex, stopIndex):
        # For a fake iteration and dataset
        for idx in range(beginIndex, stopIndex, 1):
            # Create a fake image url and download it using a proxy in the list
            url = 'http://www.myrepo.com/images/{}.jpg'.format(idx)
            image_data = self.download_data(url, use_proxy=True)
            print(image_data)
            # Sleep between 1 and 5 seconds
            self.sleep(1, 5)

if __name__ == '__main__':
    scrapper = MyEasyScrapper()
    scrapper.start(1, 20)
```
5. Launch the scrapper:
```
python my_scrapper.py
```
