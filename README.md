# Codeforces-crawler
Codeforces crawler

Żeby projekt działał sensownie należy postawić dwa serwery redisa - jeden na porcie 6379, jeden na 6380 oraz serwer RabbitMQ na porcie 5672.

Scrapowanie:

Należy wejść w folder Crawler/Crawler, i tam w folderze spiders znajduje się crawler - codeforces_spider.py.
Extractor znajduje się w pliku extractor.py, zaś parser w parser.py, wszystkie odpala się przez python nazwa.

Serwer:

Żeby postawić serwer należy wejść do folderu CodeforcesCrawler i tam odpalić komendę python manage.py runserver (wymaga Django, redis-py oraz rabbita).
