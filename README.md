# jbooker
Books prices scraper (optimized for french market)

This python flask script / application, scrap several sources to get informations and prices about a book

Current sources : Amazon, Abebook, Ebay, Priceminister and LebonCoin (LeBonCoin is a very famous ads service in France, similar to Craigslist)

NB : I know this code is really awfull, I just made it quickly and I'm not a professionnal python developer, so any improvement, advice or tip is welcome. I just made it to answer my specific needs and I'll try to improve it on a regular basis.

## Requirements
```
Flask==0.12
gunicorn==19.7.1
requests==2.14.2
lxml==3.7.2
isbnlib==3.7.2
```

you can try it by running 

```
git clone https://github.com/jbgraindorge/jbooker.git
```

Then launch 

```
export FLASK_DEBUG=1  #run in debug mode to enable auto-reload
FLASK_APP=app.py flask run
```

Then go to 127.0.0.1:5000 to enjoy this wonderful killer-application :)

You can also push it on Heroku and host it on a free dyno
