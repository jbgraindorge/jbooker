#!/usr/local/bin/python3-jb
from flask import Flask, render_template, request, url_for
import sys
import uuid
import csv
import time
import datetime
import requests
from lxml import html

def isbn_check(isbn):
    isbn_final=''.join(e for e in isbn if e.isalnum())
    return(isbn_final)

#########################################################
## INFOS SEARCH ON AMAZON BY ISBN
#########################################################
def az_isearch(isbn10=None,isbn13=None):
    if isbn13:
        isbn = isbn13
        print("SEARCH AMAZON 4 ISBN13 : " + isbn)
        az_url="https://www.amazon.fr/gp/search/ref=sr_adv_b/?search-alias=stripbooks&__mk_fr_FR=%C3%85M%C3%85Z%C3%95%C3%91&unfiltered=1&field-keywords=&field-author=&field-title=&field-isbn=" + isbn + "&field-publisher=&field-collection=&node=&field-binding_browse-bin=&field-dateop=&field-datemod=&field-dateyear=&sort=relevancerank&Adv-Srch-Books-Submit.x=42&Adv-Srch-Books-Submit.y=3"
        print(az_url)
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.72 Safari/537.36'
        }
        #time.sleep(1)
        az_page = requests.get(az_url, headers=headers)
        az_tree = html.fromstring(az_page.content)
        az_tit = az_tree.xpath('//h2/text()[1][not(ancestor::*[@class="s-first-column"])]')
        print(az_tit)
        az_date = az_tree.xpath('//div[contains(@class, \'a-row a-spacing-none\')][1]/span[contains(@class, \'a-size-small a-color-secondary\')]/text()[1]')
        if az_date: az_date = str(az_date[0]).split()
        if az_date: print(az_date)
        if len(az_date) >= 1 and isinstance(az_date, list):
            az_date = az_date[len(az_date)-1]
        else:
            if az_date: az_date = az_date[len(az_date)]
        #az_aut = az_tree.xpath('//span[contains(@class, \'a-size-small a-color-secondary\')]/a[contains(@class, \'a-link-normal a-text-normal\')]/text()')
        #az_aut = az_tree.xpath('//span[contains(@class, \'a-size-small a-color-secondary\')][2]/text()')
        az_aut = az_tree.xpath('//span[contains(@class, \'a-size-small a-color-secondary\')]/a[contains(@class, \'a-link-normal a-text-normal\')]/text()')
        if not az_aut: az_aut = az_tree.xpath('//span[contains(@class, \'a-size-small a-color-secondary\')][2]/text()')
        print(az_aut)
        az_listings = az_tree.xpath('//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"][1]/@href')
        if az_listings:
            print("SECOND URL IS : " + str(az_listings))
            az_page2 = requests.get(az_listings[0], headers=headers)
            az_tree2 = html.fromstring(az_page2.content)
            az_isbn13 = az_tree2.xpath('//div[contains(@class, \'content\')]/ul/li[6]/text()')
            az_isbn10 = az_tree2.xpath('//div[contains(@class, \'content\')]/ul/li[5]/text()')
            print(az_isbn13,az_isbn10)
            az_isbn13 = [x.replace(' ','') for x in az_isbn13]
            az_isbn13 = [x.replace('-','') for x in az_isbn13]
            az_isbn10 = [x.replace(' ','') for x in az_isbn10]
            az_isbn10 = [x.replace('-','') for x in az_isbn10]
            print(az_isbn13,az_isbn10)
            if not az_isbn13 or not az_isbn10 or ',' in az_isbn13[0] or ',' in az_isbn10[0] or '\n' in az_isbn10[0] or '\n' in az_isbn13[0]:
                print("TATA")
                az_isbn13 = az_tree2.xpath('//div[contains(@class, \'content\')]/ul/li[5]/text()')
                az_isbn10 = az_tree2.xpath('//div[contains(@class, \'content\')]/ul/li[4]/text()')
                print(az_isbn13,az_isbn10)
                az_isbn13 = [x.replace(' ','') for x in az_isbn13]
                az_isbn13 = [x.replace('-','') for x in az_isbn13]
                az_isbn10 = [x.replace(' ','') for x in az_isbn10]
                az_isbn10 = [x.replace('-','') for x in az_isbn10]
                print(az_isbn13,az_isbn10)
            if not az_aut:
                az_aut = az_tree2.xpath('//span[contains(@class, \'author notFaded\')]/a[contains(@class, \'a-link-normal\')]/text()')
            #if az_isbn:
            #return(az_isbn13,az_isbn10)
            az_pub = az_tree2.xpath('//div[contains(@class, \'content\')]/ul/li[2]/text()')
            print("DEBUG")
            print(type(az_pub))
            print(az_pub[0])
            print(type(az_date))
            print(az_date)
            print(type(az_tit))
            print(az_tit[0])
            print(type(az_aut))
            print(az_aut)
            print(type(az_isbn10))
            print(az_isbn10)
            print(type(az_isbn13))
            print(az_isbn13)
            renvoi_info13 = {'editeur' : az_pub[0] , 'date' : az_date, 'titre' : az_tit[0], 'auteur' : az_aut[0], 'isbn10' : az_isbn10[0], 'isbn13' : isbn}
        else:
            ## IF NOT SECOND URL = NO RESULTS
            renvoi_info13 = None
    else:
        renvoi_info13 = None
    if isbn10:
        isbn = isbn10
        print("SEARCH AMAZON 4 " + isbn)
        az_url="https://www.amazon.fr/gp/search/ref=sr_adv_b/?search-alias=stripbooks&__mk_fr_FR=%C3%85M%C3%85Z%C3%95%C3%91&unfiltered=1&field-keywords=&field-author=&field-title=&field-isbn=" + isbn + "&field-publisher=&field-collection=&node=&field-binding_browse-bin=&field-dateop=&field-datemod=&field-dateyear=&sort=relevancerank&Adv-Srch-Books-Submit.x=42&Adv-Srch-Books-Submit.y=3"
        print(az_url)
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.72 Safari/537.36'
        }
        #time.sleep(1)
        az_page = requests.get(az_url, headers=headers)
        az_tree = html.fromstring(az_page.content)
        az_tit = az_tree.xpath('//h2/text()[1][not(ancestor::*[@class="s-first-column"])]')
        print(az_tit)
        az_date = az_tree.xpath('//div[contains(@class, \'a-row a-spacing-none\')][1]/span[contains(@class, \'a-size-small a-color-secondary\')]/text()[1]')
        print("DATE : " + str(az_date))
        if az_date: az_date = str(az_date[0]).split()
        print("DATE : " + str(az_date))
        if az_date: print(az_date)
        if len(az_date) >= 1 and isinstance(az_date, list):
            az_date = az_date[len(az_date)-1]
            print("DATE : " + str(az_date))
        else:
            #print(len(az_date))
            #az_date = az_date[len(az_date)]
            print("DATE : " + str(az_date))
        #az_aut = az_tree.xpath('//span[contains(@class, \'a-size-small a-color-secondary\')]/a[contains(@class, \'a-link-normal a-text-normal\')]/text()')
        #az_aut = az_tree.xpath('//span[contains(@class, \'a-size-small a-color-secondary\')][2]/text()')
        az_aut = az_tree.xpath('//span[contains(@class, \'a-size-small a-color-secondary\')]/a[contains(@class, \'a-link-normal a-text-normal\')]/text()')
        if not az_aut: az_aut = az_tree.xpath('//span[contains(@class, \'a-size-small a-color-secondary\')][2]/text()')
        print(az_aut)
        az_listings = az_tree.xpath('//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"][1]/@href')
        if az_listings:
            print("SECOND URL IS : " + str(az_listings))
            az_page2 = requests.get(az_listings[0], headers=headers)
            az_tree2 = html.fromstring(az_page2.content)
            az_isbn13 = az_tree2.xpath('//div[contains(@class, \'content\')]/ul/li[6]/text()')
            az_isbn10 = az_tree2.xpath('//div[contains(@class, \'content\')]/ul/li[5]/text()')
            print(az_isbn13,az_isbn10)
            az_isbn13 = [x.replace(' ','') for x in az_isbn13]
            az_isbn13 = [x.replace('-','') for x in az_isbn13]
            az_isbn10 = [x.replace(' ','') for x in az_isbn10]
            az_isbn13 = [x.replace('\n','') for x in az_isbn13]
            az_isbn10 = [x.replace('-','') for x in az_isbn10]
            print(az_isbn13,az_isbn10)
            if not az_isbn13 or not az_isbn10 or ',' in az_isbn13[0] or ',' in az_isbn10[0]:
                print("TATA")
                az_isbn13 = az_tree2.xpath('//div[contains(@class, \'content\')]/ul/li[5]/text()')
                az_isbn10 = az_tree2.xpath('//div[contains(@class, \'content\')]/ul/li[4]/text()')
                print(az_isbn13,az_isbn10)
                az_isbn13 = [x.replace(' ','') for x in az_isbn13]
                az_isbn13 = [x.replace('-','') for x in az_isbn13]
                az_isbn10 = [x.replace(' ','') for x in az_isbn10]
                az_isbn10 = [x.replace('-','') for x in az_isbn10]
                print(az_isbn13,az_isbn10)
            #if az_isbn:
            #return(az_isbn13,az_isbn10)
            az_pub = az_tree2.xpath('//div[contains(@class, \'content\')]/ul/li[2]/text()')
            print("DEBUG")
            print(type(az_pub))
            print(az_pub[0])
            print(type(az_date))
            print(az_date)
            print(type(az_tit))
            print(az_tit[0])
            print(type(az_aut))
            print(az_aut)
            print(type(az_isbn10))
            print(az_isbn10)
            print(len(az_isbn10[0]))
            print(type(az_isbn13))
            print(az_isbn13)
            if len(az_isbn10[0]) == 13:
                renvoi_info10 = {'editeur' : az_pub[0] , 'date' : az_date, 'titre' : az_tit[0], 'auteur' : az_aut[0], 'isbn13' : az_isbn10[0], 'isbn10' : isbn}
            else:
                renvoi_info10 = {'editeur' : az_pub[0] , 'date' : az_date, 'titre' : az_tit[0], 'auteur' : az_aut[0], 'isbn13' : az_isbn13[0], 'isbn10' : isbn}
        else:
            renvoi_info10 = None
    else:
        renvoi_info10 = None
    return(renvoi_info10,renvoi_info13)

#########################################################
## INFOS SEARCH ON ABE BY ISBN
#########################################################
def ab_isearch(isbn13=None,isbn10=None):
    if isbn13:
        isbn = isbn13
        print("SEARCH ABEBOOK 4 " + isbn)
        ab_url="https://www.abebooks.fr/servlet/SearchResults?sts=t&an=&tn=&kn=&isbn=" + isbn
        print(ab_url)
        #time.sleep(1)
        ab_page = requests.get(ab_url)
        ab_tree = html.fromstring(ab_page.content)
        ab_pub = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span/text()[1]')
        ab_date = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span[2]/text()')
        print(ab_pub[0])
        ab_date = [x.replace('(','') for x in ab_date]
        ab_date = [x.replace(')','') for x in ab_date]
        ab_date = ab_date[0]
        print(ab_date)
        return(ab_pub[0],ab_date)
    elif isbn10:
        isbn = isbn10
        print("SEARCH ABEBOOK 4 " + isbn)
        ab_url="https://www.abebooks.fr/servlet/SearchResults?sts=t&an=&tn=&kn=&isbn=" + isbn
        print(ab_url)
        #time.sleep(1)
        ab_page = requests.get(ab_url)
        ab_tree = html.fromstring(ab_page.content)
        ab_pub = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span/text()[1]')
        ab_date = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span[2]/text()')
        print(ab_pub[0])
        ab_date = [x.replace('(','') for x in ab_date]
        ab_date = [x.replace(')','') for x in ab_date]
        ab_date = ab_date[0]
        print(ab_date)
        return(ab_pub[0],ab_date)
    else:
        return(None)

#########################################################
## INFOS SEARCH ON ABE NO ISBN
#########################################################
def ab_search(titre=None,auteur=None,annee=None,editeur=None):
    print("SEARCH ABEBOOK 4 " + titre + auteur + annee + editeur)
    ##SEARCH ON EVERYTHING
    ab_url="https://www.abebooks.fr/servlet/SearchResults?an=" + auteur + "&bi=0&bx=off&ds=30&pn=" + editeur + "&sortby=1&sts=t&tn=" + titre + "&yrh=" + annee + "&yrl=" + annee
    print(ab_url)
    #time.sleep(1)
    ab_page = requests.get(ab_url)
    ab_tree = html.fromstring(ab_page.content)
    ab_count = ab_tree.xpath('//b[@id=\'topbar-search-result-count\']/text()')
    ##TEST SI ON A DES RESULTATS avec les 4 infos
    if ab_count:
        ab_counts = int(ab_count[0])
    else:
        ##SI Y EN A PAS ON SUPPRIME EDITEUR ET ANNEE ET ON RETRY
        ab_url="https://www.abebooks.fr/servlet/SearchResults?an=" + auteur + "&bi=0&bx=off&ds=30&pn=&sortby=1&sts=t&tn=" + titre
        print(ab_url)
        #time.sleep(1)
        ab_page = requests.get(ab_url)
        ab_tree = html.fromstring(ab_page.content)
        ab_count = ab_tree.xpath('//b[@id=\'topbar-search-result-count\']/text()')
        ##TEST SI ON A DES RESULTATS
        if ab_count:
            ab_counts = int(ab_count[0])
        else:
            ## SI Y A PAS DE RESULTAT JUSTE SUR TITRE/AUTEUR PLUS RIEN A VOIR SUR ABE
            return(None)
    if ab_counts > 10:
        ##SI TROP DE RESULT AVEC les 4 infos ON SORT
        toomuch=True
        return(toomuch)
    ##SINON ON EXTRACT EN CROISANT LES DOIGTS
    ab_pub = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span[1]/text()')
    ab_date = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span[2]/text()')
    ab_tit = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/h2/a/span/text()')
    ab_aut = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/p[contains(@class, \'author\')]/strong/text()')
    #ab_prices = [x.replace('EUR ','') for x in ab_prices]
    if ab_pub:
        print("EDITEUR " + str(ab_pub))
    else:
        print('I have to do another check for publisher')
        ab_pub = ab_tree.xpath('//div[@id=\'book-2\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span[1]/text()')
        print("EDITEUR " + str(ab_pub))
    if ab_date:
        print("DATE " + str(ab_date))
    else:
        print('I have to do another check for date')
        ab_date = ab_tree.xpath('//div[@id=\'book-2\']/meta[@itemprop=\'datePublished\']/@content')
        #ab_date = ab_date[0]
        if not ab_date:
            ab_date = ab_tree.xpath('//p/span[2]/text()')
        print("DATE " + str(ab_date))
    if ab_date is not str:
        ab_date = [x.replace('(','') for x in ab_date]
        ab_date = [x.replace(')','') for x in ab_date]
    #ab_date = ab_date[0]
    print("TITRE " + str(ab_tit))
    print("AUTEUR " + str(ab_aut))
    print(type(ab_date))
    print(type(ab_tit))
    print(type(ab_aut))
    print(type(ab_pub))
    envoi_info = ab_pub + ab_date + ab_tit + ab_aut
    print("ALL" + str(envoi_info))
    #print(len(envoi_info))
    return(envoi_info)

#########################################################
## INFOS SEARCH ON ABE BIS BY ISBN
#########################################################
def ab_isearch2(isbn13=None,isbn10=None):
    print("SEARCH2 ABEBOOK 4 " + isbn13 + " " + isbn10)
    if isbn13:
        ab_url="https://www.abebooks.fr/servlet/SearchResults?sts=t&an=&tn=&kn=&isbn=" + isbn13 + "&sortby=1"
    elif isbn10:
        ab_url="https://www.abebooks.fr/servlet/SearchResults?sts=t&an=&tn=&kn=&isbn=" + isbn10 + "&sortby=1"
    #ab_url="https://www.abebooks.fr/servlet/SearchResults?sts=t&an=&tn=&kn=&isbn=" + isbn13 + "&sortby=1"
    print(ab_url)
    #time.sleep(1)
    ab_page = requests.get(ab_url)
    ab_tree = html.fromstring(ab_page.content)
    ab_pub = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span[1]/text()')
    ab_date = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span[2]/text()')
    ab_tit = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/h2/a/span/text()')
    ab_aut = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/p[contains(@class, \'author\')]/strong/text()')
    #ab_prices = [x.replace('EUR ','') for x in ab_prices]
    if ab_pub:
        print(ab_pub)
    else:
        print('I have to do another check for publisher')
        ab_pub = ab_tree.xpath('//div[@id=\'book-2\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span[1]/text()')
        print(ab_pub)
    if ab_date:
        print(ab_date)
    else:
        print('I have to do another check for date')
        ab_date = ab_tree.xpath('//p[@id=\'publisher\']/span[2]/text()')
        #ab_date = [x.replace('(','') for x in ab_date]
        #ab_date = [x.replace(')','') for x in ab_date]
        print(ab_date)
    if ab_date is not str:
        ab_date = [x.replace('(','') for x in ab_date]
        ab_date = [x.replace(')','') for x in ab_date]
    #ab_date = ab_date[0]
    print(ab_tit)
    print(ab_aut)
    envoi_info = ab_pub + ab_date + ab_tit + ab_aut
    print("ALL" + str(envoi_info))
    #print(len(envoi_info))
    return(envoi_info)

#########################################################
## INFOS SEARCH FROM ISBNLIB
#########################################################
def imetafrom_isbnlib(isbn10=None,isbn13=None):
    import isbnlib
    #TRY FIRST WITH ISBNLIB
    print("TRY FIRST WITH ISBNLIB")
    if isbn10: isbn13 = isbnlib.to_isbn13(isbn10)
    if isbn13: isbn10 = isbnlib.to_isbn10(isbn13)
    #if isbnlib.is_isbn10(isbn10) or isbnlib.is_isbn13(isbn13) or isbnlib.is_isbn10(isbn13) or isbnlib.is_isbn13(isbn10):
    primar_info10 = isbnlib.meta(isbn10, service='default', cache='default')
    primar_info13 = isbnlib.meta(isbn13, service='default', cache='default')
    if primar_info10: print(primar_info10)
    if primar_info13: print(primar_info13)
    if primar_info10 and primar_info13:
        return(isbn10,isbn13,primar_info10,primar_info13)
    elif primar_info10:
        return(isbn10,isbn13,primar_info10)
    elif primar_info13:
        return(isbn10,isbn13,primar_info13)
    else:
        return(None)

#########################################################
## INFOS SEARCH FROM GOOGLE BOOKS
#########################################################
def imetafrom_goob(isbn10=None,isbn13=None):
    import googlebook
    #THEN TRY WITH GOOGLEBOOK
    print("TRY TO GET INFOS FROM GOOGLEBOOK API")
    gapi = googlebook.Api()
    if isbn10:
        qury10 = "isbn:" + isbn10
        rez10 = gapi.list(qury10)
    else:
        rez10 = None
    if isbn13:
        qury13 = "isbn:" + isbn13
        rez13 = gapi.list(qury13)
    else:
        rez13 = None
    return(rez10,rez13)

#########################################################
## INFOS SEARCH FROM ABEBOOKS
#########################################################
def imetafrom_abe(isbn10=None,isbn13=None):
    print("SEARCH2 ABEBOOK 4 " + isbn13 + " " + isbn10)
    if isbn13:
        ab_url="https://www.abebooks.fr/servlet/SearchResults?sts=t&an=&tn=&kn=&isbn=" + isbn13 + "&sortby=1"
        print(ab_url)
        #time.sleep(1)
        ab_page = requests.get(ab_url)
        ab_tree = html.fromstring(ab_page.content)
        ab_pub = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span[1]/text()')
        ab_date = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span[2]/text()')
        ab_tit = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/h2/a/span/text()')
        ab_aut = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/p[contains(@class, \'author\')]/strong/text()')
        ab_isbn10 = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[contains(@class, \'isbn small\')]/span[1]/a/text()')
        abe_info13 = ab_tit + ab_aut + ab_pub + ab_date + ab_isbn10
    else:
        abe_info13 = None
    if isbn10:
        ab_url="https://www.abebooks.fr/servlet/SearchResults?sts=t&an=&tn=&kn=&isbn=" + isbn10 + "&sortby=1"
        print(ab_url)
        #time.sleep(1)
        ab_page = requests.get(ab_url)
        ab_tree = html.fromstring(ab_page.content)
        ab_pub = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span[1]/text()')
        ab_date = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[@id=\'publisher\']/span[2]/text()')
        ab_tit = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/h2/a/span/text()')
        ab_aut = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/p[contains(@class, \'author\')]/strong/text()')
        ab_isbn13 = ab_tree.xpath('//div[@id=\'book-1\']/div[contains(@class, \'result-data col-xs-9 cf\')]/div[contains(@class, \'result-detail col-xs-8\')]/div[contains(@class, \'m-md-b\')]/p[contains(@class, \'isbn small\')]/span[2]/a/text()')
        abe_info10 = ab_tit + ab_aut + ab_pub + ab_date + ab_isbn13
    else:
        abe_info10 = None
    return(abe_info10,abe_info13)

#########################################################
## INFOS SEARCH ON WEB FROM ISBN
#########################################################
def imetafromweb(isbn10=None,isbn13=None):
    if isbn10: print("ISBN10 : " + isbn10)
    if isbn13: print("ISBN13 : " + isbn13)
    if imetafrom_isbnlib(isbn10,isbn13):
        isbn10,isbn13,isbnlib_info10,isbnlib_info13 = imetafrom_isbnlib(isbn10,isbn13)
    else:
        isbnlib_info10 = None
        isbnlib_info13 = None
    goob_info10,goob_info13 = imetafrom_goob(isbn10,isbn13)
    amazon_info10,amazon_info13 = az_isearch(isbn10,isbn13)
    abe_info10,abe_info13 = imetafrom_abe(isbn10,isbn13)
    print('####### AMAZON INFOS ###########')
    print(amazon_info10,amazon_info13)
    print('####### GOOB INFOS ###########')
    print(goob_info10,goob_info13)
    print('####### ISBNLIB INFOS ###########')
    print(isbn10,isbn13,isbnlib_info10,isbnlib_info13)
    print('####### ABEBOOKS INFOS ###########')
    print(abe_info10,abe_info13)
    ############# FIN DE LA CONSOLIDATION ET RETURN DES INFOS
    if isbnlib_info10 and isbnlib_info10['Title']:
        isbnlibinfo10 = {'titre' : isbnlib_info10['Title'], 'auteur' : isbnlib_info10['Authors'][0], 'date' : isbnlib_info10['Year'], 'editeur': isbnlib_info10['Publisher'], 'isbn10' : isbn10 , 'isbn13' : isbnlib_info10['ISBN-13'] }
        return(isbnlibinfo10)
    elif isbnlib_info13 and isbnlib_info13['Title']:
        isbnlibinfo13 = {'titre' : isbnlib_info13['Title'], 'auteur' : isbnlib_info13['Authors'][0], 'date' : isbnlib_info13['Year'], 'editeur': isbnlib_info13['Publisher'], 'isbn13' : isbnlib_info10['ISBN-13'], 'isbn10' : abe_info13[4]}
        return(isbnlibinfo13)
    ############ CONSOLIDATION DES INFOS
    if amazon_info13:
        print("RETOUR 1")
        return(amazon_info13)
    elif amazon_info10:
        print("RETOUR 2")
        return(amazon_info10)
    elif abe_info10:
        print("RETOUR 3")
        return(abe_info10)
    elif abe_info13:
        print("RETOUR 4")
        return(abe_info13)
    #renvoi2 = ab_isearch2(isbn13,isbn10)
    #print(renvoi2)
    #renvoi = ab_isearch(isbn13,isbn10)
    #print(renvoi)
    #az_rez10,az_rez13 = az_isearch(isbn13,isbn10)
    #if rez10['totalItems'] == 0 or rez13['totalItems'] == 0:
    #print("TRY TO GET INFOS FROM ABEBOOK")
    #if renvoi2:
    #return([str(renvoi2[2]), isbn13, str(renvoi2[0]), str(renvoi2[1]), str(renvoi2[3]), isbn10])
    #else :
    ##IF NOT ON ABE, TRY AMAZON
    #return(renvoi_info)
    #elif 'publisher' not in rez2['items'][0]['volumeInfo']:
    ##IF GOOB NOT COMPLETE, SEARCH ON ABE
    #renvoi = ab_isearch(isbn13,isbn10)
    #return([rez['items'][0]['volumeInfo']['title'], isbn13, str(renvoi[0]), str(renvoi[1]), rez['items'][0]['volumeInfo']['authors'][0],isbn10])
    #else:
    #GOOB RESULTS RESTITUTION
    #if rez2['items'][0]['volumeInfo']['title']: titre=rez2['items'][0]['volumeInfo']['title']
    #if rez2['items'][0]['volumeInfo']['authors'][0]: auteur=rez2['items'][0]['volumeInfo']['authors'][0]
    #if rez2['items'][0]['volumeInfo']['publishedDate']: annee=rez2['items'][0]['volumeInfo']['publishedDate']
    #if rez2['items'][0]['volumeInfo']['publisher']: editeur=rez2['items'][0]['volumeInfo']['publisher']
    #return([titre, isbn13, editeur, annee, auteur,isbn10])
    #elif 'publisher' not in rez['items'][0]['volumeInfo']:
    ##IF GOOB NOT COMPLETE, SEARCH ON ABE
    #return([rez['items'][0]['volumeInfo']['title'], isbn13, str(renvoi[0]), str(renvoi[1]), rez['items'][0]['volumeInfo']['authors'][0],isbn10])
    #else:
    #GOOB RESULTS RESTITUTION
    #if rez['items'][0]['volumeInfo']['title']: titre=rez['items'][0]['volumeInfo']['title']
    #if rez['items'][0]['volumeInfo']['authors'][0]: auteur=rez['items'][0]['volumeInfo']['authors'][0]
    #if rez['items'][0]['volumeInfo']['publishedDate']: annee=rez['items'][0]['volumeInfo']['publishedDate']
    #if rez['items'][0]['volumeInfo']['publisher']: editeur=rez['items'][0]['volumeInfo']['publisher']
    #return([titre, isbn13, editeur, annee, auteur,isbn10])

#########################################################
## GET ISBN FROM AMAZON
#########################################################
def get_isbn_amazon(abmeta):
    titre = abmeta[2]
    auteur = abmeta[3]
    annee = abmeta[1]
    editeur = abmeta[0]
    print("ISBN SCRAP ON AMAZON " + str(abmeta) + " " + str(auteur) + " " + str(editeur) + " " + str(annee))
    titre_ori=titre
    auteur_ori=auteur
    titre=titre.split()
    #print("TITRE TYPE : " + str(type(titre)))
    titre=[x.replace('\'','%20') for x in titre]
    titre=[x.replace('(','') for x in titre]
    titre=[x.replace(')','') for x in titre]
    titre=[x.replace(',','') for x in titre]
    keyword=max(titre, key=len)
    auteur=auteur.split()
    auteur=max(auteur, key=len)
    #az_url="https://www.amazon.fr/gp/search/ref=sr_adv_b/?search-alias=stripbooks&__mk_fr_FR=%C3%85M%C3%85Z%C3%95%C3%91&unfiltered=1&field-keywords=&field-author=" + auteur + "&field-title=" + titre + "&field-isbn=&field-publisher=" + editeur + "&field-collection=&node=&field-binding_browse-bin=&field-dateop=&field-datemod=&field-dateyear=" + annee + "&sort=relevancerank&Adv-Srch-Books-Submit.x=42&Adv-Srch-Books-Submit.y=3"
    az_url="https://www.amazon.fr/gp/search/ref=sr_adv_b/?search-alias=stripbooks&unfiltered=1&field-keywords=&field-author=" + auteur + "&field-title=" + keyword + "&field-isbn=&field-publisher=&field-collection=&node=&field-binding_browse-bin=&field-dateop=&field-datemod=&field-dateyear=&sort=relevancerank&Adv-Srch-Books-Submit.x=42&Adv-Srch-Books-Submit.y=3"
    print(az_url)
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.72 Safari/537.36'
    }
    print("I GOT PRODUCT URL")
    #time.sleep(1)
    az_page = requests.get(az_url, headers=headers)
    az_tree = html.fromstring(az_page.content)
    az_listings = az_tree.xpath('//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"][1]/@href')
    if len(az_listings) >= 4:
        t2 = titre_ori.replace(" ", "+")
        az_url="https://www.amazon.fr/s/ref=nb_sb_noss_2?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Dstripbooks&field-keywords=" + t2
        print(az_url)
        az_page = requests.get(az_url, headers=headers)
        az_tree = html.fromstring(az_page.content)
        az_listings = az_tree.xpath('//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"][1]/@href')
        print("SECOND URL IS : " + str(az_listings))
        az_page = requests.get(az_listings[0], headers=headers)
        az_tree = html.fromstring(az_page.content)
        az_isbn13 = az_tree.xpath('//div[contains(@class, \'content\')]/ul/li[6]/text()')
        az_isbn10 = az_tree.xpath('//div[contains(@class, \'content\')]/ul/li[5]/text()')
        az_isbn13 = [x.replace(' ','') for x in az_isbn13]
        az_isbn13 = [x.replace('-','') for x in az_isbn13]
        az_isbn10 = [x.replace(' ','') for x in az_isbn10]
        az_isbn10 = [x.replace('-','') for x in az_isbn10]
        if ',' in az_isbn13[0] or ',' in az_isbn10[0]:
            print("TOTO")
            az_isbn13 = az_tree.xpath('//div[contains(@class, \'content\')]/ul/li[5]/text()')
            az_isbn10 = az_tree.xpath('//div[contains(@class, \'content\')]/ul/li[4]/text()')
            az_isbn13 = [x.replace(' ','') for x in az_isbn13]
            az_isbn13 = [x.replace('-','') for x in az_isbn13]
            az_isbn10 = [x.replace(' ','') for x in az_isbn10]
            az_isbn10 = [x.replace('-','') for x in az_isbn10]
        #if az_isbn:
        print(az_isbn13,az_isbn10)
        return(az_isbn13,az_isbn10)
    else:
        print("SECOND URL IS : " + str(az_listings))
        az_page = requests.get(az_listings[0], headers=headers)
        az_tree = html.fromstring(az_page.content)
        az_isbn13 = az_tree.xpath('//div[contains(@class, \'content\')]/ul/li[6]/text()')
        az_isbn10 = az_tree.xpath('//div[contains(@class, \'content\')]/ul/li[5]/text()')
        az_isbn13 = [x.replace('','') for x in az_isbn13]
        az_isbn13 = [x.replace('-','') for x in az_isbn13]
        az_isbn10 = [x.replace(' ','') for x in az_isbn10]
        az_isbn10 = [x.replace('-','') for x in az_isbn10]
        if ',' in az_isbn13[0] or ',' in az_isbn10[0]:
            print("TATA")
            az_isbn13 = az_tree.xpath('//div[contains(@class, \'content\')]/ul/li[5]/text()')
            az_isbn10 = az_tree.xpath('//div[contains(@class, \'content\')]/ul/li[4]/text()')
            az_isbn13 = [x.replace(' ','') for x in az_isbn13]
            az_isbn13 = [x.replace('-','') for x in az_isbn13]
            az_isbn10 = [x.replace(' ','') for x in az_isbn10]
            az_isbn10 = [x.replace('-','') for x in az_isbn10]
        #if az_isbn:
        print(az_isbn13,az_isbn10)
        return(az_isbn13,az_isbn10)

#########################################################
## INFOS SEARCH ON WEB NO ISBN
#########################################################
def metafromweb(titre=None,auteur=None,annee=None,editeur=None):
    if not titre and not auteur and not annee and not editeur:
        return(None)
    else:
        print('OK I CHECK THIS ON INTERNET')
        abmeta = ab_search(titre,auteur,annee,editeur)
        if isinstance(abmeta, list):
            print("AB-META : " + str(abmeta))
            print('NOW I HAVE META FROM ABE, I TRY TO GET AN ISBN')
            if int(abmeta[1]) < 1976:
                return(abmeta)
            else:
                az_isbn13,az_isbn10 = get_isbn_amazon(abmeta)
                if az_isbn13 and az_isbn10:
                    metas = abmeta + az_isbn13 + az_isbn10
                    return(metas)
                else:
                    return(abmeta)
        else:
            return(abmeta)
