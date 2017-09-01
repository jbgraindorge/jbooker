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

@app.route('/faq/')
def faq():
    print("this is the faq")
    return render_template('faq.html')

@app.route('/hello/', methods=['POST'])
def hello():
    if request.method == 'POST':
        ##IF RETURN IN POST
        if request.form.get('all'):
            print('LAUNCH GLOB PRICES SEARCH')
            from books_prices import glob_isearch
            gprices = glob_isearch(request.form['isbn13'],request.form['titre'],request.form['auteur'],request.form['annee'],request.form['editeur'],request.form['isbn10'])
            if gprices:
                return render_template('rez2.html', titre=request.form['titre'], isbn13=request.form['isbn13'], isbn10=request.form['isbn10'], editeur=request.form['editeur'], annee=request.form['annee'], auteur=request.form['auteur'], az_prices=gprices[0], pm_prices=gprices[3],eb_prices=gprices[2],ab_prices=gprices[1],lb_prices=gprices[4],booktry=gprices)
            else:
                return render_template('rez2.html', titre=request.form['titre'], isbn13=request.form['isbn13'], isbn10=request.form['isbn10'], editeur=request.form['editeur'], annee=request.form['annee'], auteur=request.form['auteur'])
        if request.form.get('amazon'): print("LAUNCH AN AMAZON PRICES SEARCH")
        if request.form.get('abebook'): print("LAUNCH AN ABEBOOK PRICES SEARCH")
        if request.form.get('ebay'): print("LAUNCH AN EBAY PRICES SEARCH")
        if request.form.get('priceminister'): print("LAUNCH A PRICEMINISTER PRICES SEARCH")
        if request.form.get('leboncoin'):
            print("LAUNCH A LEBONCOIN PRICES SEARCH")
            from books_prices import lbc_check
            need_details = True
            lbc_rez = lbc_check(request.form['titre'],request.form['auteur'],need_details)
            return render_template('rez2.html', lbc_rez=lbc_rez)
        if request.form['isbn10'] or request.form['isbn13']:
            isbn10=request.form['isbn10']
            isbn13=request.form['isbn13']
            from books_infos import isbn_check
            #from books_db import search_isbn, search_prices
            isbn10 = isbn_check(isbn10)
            isbn13 = isbn_check(isbn13)
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
    print("this is my search function")

@app.route('/inject/', methods=['POST'])
def inject():
    print("this is the injector func")

@app.route('/lbc_search/', methods=['POST'])
def lbc_search():
    print("this is lbc searcher")

@app.route('/amazon_search/', methods=['POST'])
def amazon_search():
    from books_prices import amazon_icheck, amazon_noisbn_price_check
    amazon_rez = amazon_noisbn_price_check(request.form['titre'],request.form['auteur'],request.form['annee'],request.form['editeur'])
    amazon_irez = None
    if request.form['isbn10']: amazon_irez = amazon_icheck(request.form['isbn10'])
    if request.form['isbn13']: amazon_irez = amazon_icheck(request.form['isbn13'])
    if amazon_irez is not None:
        return render_template('rez2.html', amazon_rez=amazon_rez, amazon_irez=amazon_irez)
    elif amazon_rez:
        return render_template('rez2.html', amazon_rez=amazon_rez)
    else:
        return render_template('rez2.html')
