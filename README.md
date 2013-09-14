
checkout the repo
```
git clone http://github.com/enjalot/sparcscraps.git
```

make sure you have Scrapy [installed](http://doc.scrapy.org/en/0.18/intro/install.html):
```
sudo pip install Scrapy
sudo pip install --upgrade zope.interface
```

create a JSON file from SPARC SF menu
```
scrapy crawl menu -o items.json -t json
more items.json
```
