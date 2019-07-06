# CrawlEncuentra24
Crawler for obtaining pricing information from encuentra24's property selling

## How to setup the enviroment
  It is recommended to use a venv for the project. On this venv install Scrapy and ScrapyJs with the following commands:
  
  `pip install scrapy`
  
  `pip install scrapy-splash`

  You must also [install Splash and start the docker image](https://splash.readthedocs.io/en/latest/install.html)
  
## How to run
To tun the crawl for the Encuentra24 website, you can run  th following command:

`scrapy crawl CrawlEncuentra24 -o info.csv`

This will create a csv file called info with the result of the crawl. You can change the format to JSON or XML by simply changing the extension of the filename (which is also customizable)
