#!/usr/local/bin/python3-jb
from flask import Flask, render_template, request, url_for
import sys
import uuid
import csv
import time
import datetime
import requests
from lxml import html

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('rez2.html')

@app.route('/hello/', methods=['POST'])
def hello():
    if request.method == 'POST':
        ##IF RETURN IN POST
        if request.form['isbn10'] or request.form['isbn13']:
            isbn10=request.form['isbn10']
            isbn13=request.form['isbn13']
            from books_infos import isbn_check
            #from books_db import search_isbn, search_prices
            isbn10 = isbn_check(isbn10)
            isbn13 = isbn_check(isbn13)
            #search_rez = search_isbn(isbn10,isbn13)
            #print(search_rez)
            #if search_rez:
                ##IF INFOS IN CASSANDRA , TRY TO DISPLAY PRICES
            #    gprices = search_prices(search_rez[4])
            #    if gprices:
                    ## IF PRICES , DISPLAY IT
            #        return render_template('rez2.html', titre=search_rez[1], isbn13=search_rez[5], editeur=search_rez[0], annee=search_rez[2], auteur=search_rez[3], az_prices=gprices[0], pm_prices=gprices[3], eb_prices=gprices[2], ab_prices=gprices[1], lb_prices=gprices[4], booktry=gprices, isbn10=search_rez[6])
            #    else:
                    #print("DONT HAVE PRICE")
            #        return render_template('rez2.html', titre=search_rez[1], isbn13=search_rez[5], editeur=search_rez[0], annee=search_rez[2], auteur=search_rez[3], isbn10=search_rez[6])
            #else:
            ##IF NO INFO IN CASSANDRA, GET INFO ON WEB
            from books_infos import imetafromweb
            #if isbn10 and isbn13:
            imeta = imetafromweb(isbn10,isbn13)
            #if isbn10: imeta = imetafromweb(isbn10)
            #if isbn13: imeta = imetafromweb(isbn13)
            if not imeta:
                ##IF 0 INFO FOUND ON WEB
                zeroeverywhere=True
                return render_template('rez2.html', zeroeverywhere=zeroeverywhere)
            else:
                ##IF INFOS FOUND DISPLAY THEM (BUT NO WEB PRICE SEARCH)
                return render_template('rez2.html', titre=imeta['titre'], isbn13=imeta['isbn13'], editeur=imeta['editeur'], annee=imeta['date'], auteur=imeta['auteur'], isbn10=imeta['isbn10'])

        elif request.form['titre'] or request.form['auteur'] or request.form['annee'] or request.form['editeur']:
            ##IF POST SOMETHING ELSE THAN ISBN
            #from books_db import search_cass, search_prices
            ##SEARCH INFOS IN CASSANDRA
            #booktry=search_cass(request.form['titre'],request.form['auteur'],request.form['annee'],request.form['editeur'])
            #print(booktry)
            #if booktry:
                ##IF RESULTS, DISPLAY THEM
            #    gprices = search_prices(booktry[6])
            #    print(gprices)
            #    if gprices:
            #        return render_template('rez2.html', titre=booktry[1], editeur=booktry[0], annee=booktry[2], auteur=booktry[3], az_prices=gprices[0], pm_prices=gprices[3], eb_prices=gprices[2], ab_prices=gprices[1], lb_prices=gprices[4], booktry=gprices)
            #    else:
            #        return render_template('rez2.html', titre=booktry[1], editeur=booktry[0], annee=booktry[2], auteur=booktry[3])
            #else:
            ##IF NO RESULT, NEED TO SEARCH AGAIN. STILL NO ISBN
            from books_infos import metafromweb
            metas = metafromweb(request.form['titre'],request.form['auteur'],request.form['annee'],request.form['editeur'])
            print(metas)
            if metas:
                if len(metas) > 4:
                    return render_template('rez2.html', titre=metas[2], editeur=metas[0], annee=metas[1], auteur=metas[3], isbn13=metas[4], isbn10=metas[5])
                elif isinstance(metas, list):
                    return render_template('rez2.html', titre=metas[2], editeur=metas[0], annee=metas[1], auteur=metas[3])
                else:
                    toomuch=True
                    return render_template('rez2.html', toomuch=toomuch, titre=request.form['titre'], auteur=request.form['auteur'], annee=request.form['annee'], editeur=request.form['editeur'])
            else:
                return render_template('rez2.html', titre=request.form['titre'], auteur=request.form['auteur'], annee=request.form['annee'], editeur=request.form['editeur'])
        else:
            ##IF POSTMETHOD BUT NOTHING SENT IN FORM
            return render_template('rez2.html')
    else:
        return render_template('rez2.html')

@app.route('/mysearch/', methods=['POST'])
def mysearch():
    ####NEED TO IMPROVE SAME FUNCTION AS INJECTOR ROUTE
    #from books_db import selector, insertor, search_prices
    from books_prices import glob_isearch
    ##GET DB RESULTS
    #bookid = selector(request.form['isbn10'],request.form['isbn13'],request.form['titre'],request.form['auteur'],request.form['annee'],request.form['editeur'])
    #if bookid:
    #    print("ALREADY INSERTED" + str(bookid))
    #else:
    #    print("NEED TO INSERT")
    #    bookid = insertor(request.form['isbn13'],request.form['titre'],request.form['auteur'],request.form['annee'],request.form['editeur'],request.form['isbn10'])
    glob_isearch(bookid,request.form['isbn13'],request.form['titre'],request.form['auteur'],request.form['annee'],request.form['editeur'],request.form['isbn10'])
    gprices = search_prices(bookid)
    if gprices:
        return render_template('rez2.html', titre=request.form['titre'], isbn13=request.form['isbn13'], isbn10=request.form['isbn10'], editeur=request.form['editeur'], annee=request.form['annee'], auteur=request.form['auteur'], az_prices=gprices[0], pm_prices=gprices[3],eb_prices=gprices[2],ab_prices=gprices[1],lb_prices=gprices[4])
    else:
        return render_template('rez2.html', titre=request.form['titre'], isbn13=request.form['isbn13'], isbn10=request.form['isbn10'], editeur=request.form['editeur'], annee=request.form['annee'], auteur=request.form['auteur'])

@app.route('/inject/', methods=['POST'])
def inject():
    from books_db import selector, insertor
    ##GET DB RESULTS
    bookid = selector(request.form['isbn10'],request.form['isbn13'],request.form['titre'],request.form['auteur'],request.form['annee'],request.form['editeur'])
    if bookid:
        print("ALREADY INSERTED" + str(bookid))
    else:
        print("NEED TO INSERT")
        bookid = insertor(request.form['isbn13'],request.form['titre'],request.form['auteur'],request.form['annee'],request.form['editeur'],request.form['isbn10'])
    ##SEND BACK THE INFOS
    return render_template('rez2.html', titre=request.form['titre'], isbn13=request.form['isbn13'], editeur=request.form['editeur'], annee=request.form['annee'], auteur=request.form['auteur'], isbn10=request.form['isbn10'])

@app.route('/lbc_search/', methods=['POST'])
def lbc_search():
    from books_prices import lbc_check
    lbc_rez = lbc_check(request.form['titre'],request.form['auteur'])
    return render_template('rez2.html', lbc_rez=lbc_rez)

@app.route('/amazon_search/', methods=['POST'])
def amazon_search():
    from books_prices import amazon_icheck, amazon_noisbn_price_check
    amazon_rez = amazon_noisbn_price_check(request.form['titre'],request.form['auteur'],request.form['annee'],request.form['editeur'])
    if request.form['isbn10']: amazon_irez = amazon_icheck(request.form['isbn10'])
    if request.form['isbn13']: amazon_irez = amazon_icheck(request.form['isbn13'])
    return render_template('rez2.html', amazon_rez=amazon_rez, amazon_irez=amazon_irez)
