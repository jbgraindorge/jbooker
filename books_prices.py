#!/usr/local/bin/python3-jb
from flask import Flask, render_template, request, url_for
import sys
import uuid
import csv
import time
import datetime
import requests
from lxml import html

#########################################################
## PRICES SEARCH ON ABE
#########################################################
def abebook_icheck(isbn_cleaned):
    print("check ABEBOOK 4 " + isbn_cleaned)
    ab_url="https://www.abebooks.fr/servlet/SearchResults?sts=t&an=&tn=&kn=&isbn=" + isbn_cleaned
    print(ab_url)
    time.sleep(1)
    ab_page = requests.get(ab_url)
    ab_tree = html.fromstring(ab_page.content)
    ab_prices = ab_tree.xpath('//span[@class="price"]/text()[not(ancestor::*[@class="shipping"])]')
    ab_prices = [x.replace('EUR ','') for x in ab_prices]
    ab_prices = [x.replace(',','.') for x in ab_prices]
    ab_prices = [float(k) for k in ab_prices]
    if ab_prices:
        #ab_cote=sum(ab_prices) / float(len(ab_prices))
        return(ab_prices)
    else:
        return(None)

#########################################################
## PRICES SEARCH ON AMAZON
#########################################################
def amazon_icheck(isbn_cleaned):
    print("check AMAZON 4 " + isbn_cleaned)
    az_url="https://www.amazon.fr/gp/search/ref=sr_adv_b/?search-alias=stripbooks&__mk_fr_FR=%C3%85M%C3%85Z%C3%95%C3%91&unfiltered=1&field-keywords=&field-author=&field-title=&field-isbn=" + isbn_cleaned + "&field-publisher=&field-collection=&node=&field-binding_browse-bin=&field-dateop=&field-datemod=&field-dateyear=&sort=relevancerank&Adv-Srch-Books-Submit.x=42&Adv-Srch-Books-Submit.y=3"
    print(az_url)
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.72 Safari/537.36'
    }
    time.sleep(1)
    az_page = requests.get(az_url, headers=headers)
    az_tree = html.fromstring(az_page.content)
    az_sec_url = az_tree.xpath('//a[@class="a-size-small a-link-normal a-text-normal"][1]/@href')
    if az_sec_url:
        az_sec_url = az_sec_url[0]
    else:
        return(None)
    time.sleep(1)
    az_page2 = requests.get(az_sec_url, headers=headers)
    az_tree2 = html.fromstring(az_page2.content)
    az_prices = az_tree2.xpath('//span[@class="a-size-large a-color-price olpOfferPrice a-text-bold"]/text()')
    az_prices = [x.replace(' ','') for x in az_prices]
    az_prices = [x.replace('.','') for x in az_prices]
    az_prices = [x.replace('EUR','') for x in az_prices]
    az_prices = [x.replace(',','.') for x in az_prices]
    az_prices = [float(k) for k in az_prices]
    if az_prices:
        #az_cote=sum(az_prices) / float(len(az_prices))
        print(az_prices)
        return(az_prices)
    else:
        print("NOTHING FROM AMAZON ICHECK")
        return(None)

#########################################################
## PRICES SEARCH ON PRICEMINISTER
#########################################################
def priceminister_icheck(isbn_cleaned):
    print("check PRICEMINISTER 4 " + isbn_cleaned)
    pm_url="http://www.priceminister.com/s/" + isbn_cleaned + "?nav=Livres"
    print(pm_url)
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.72 Safari/537.36'
    }
    time.sleep(1)
    pm_page = requests.get(pm_url, headers=headers)
    pm_tree = html.fromstring(pm_page.content)
    pm_sec_url = pm_tree.xpath('//a[@class="price typeUsed"]/@href')
    if not pm_sec_url: return(None)
    pm_sec_url ="http://www.priceminister.fr" + pm_sec_url[0]
    time.sleep(1)
    pm_page2 = requests.get(pm_sec_url, headers=headers)
    pm_tree2 = html.fromstring(pm_page2.content)
    pm_prices1 = pm_tree2.xpath('//p[@class="price typeUsed spacerBottomXs"]/text()[not(ancestor::*[@class="infosPrice spacerBottomS "])]')
    pm_prices2 = pm_tree2.xpath('//p[@class="price typeCollec spacerBottomXs"]/text()[not(ancestor::*[@class="infosPrice spacerBottomS "])]')
    if pm_prices1 and pm_prices2:
        pm_prices = pm_prices1 + pm_prices2
    elif pm_prices1:
        pm_prices = pm_prices1
    elif pm_prices2:
        pm_prices = pm_prices2
    else:
        pm_prices = None
    #del pm_prices[0]#corrected with not ancestor at previous line
    if pm_prices:
        pm_prices = [x.replace('\xa0€','') for x in pm_prices]
        pm_prices = [x.replace(',','.') for x in pm_prices]
        pm_prices = [float(j) for j in pm_prices]
        print(pm_prices)
        #pm_cote=sum(pm_prices) / float(len(pm_prices))
        return(pm_prices)
    else:
        return(None)

#########################################################
## PRICES SEARCH ON EBAY
#########################################################
def ebay_icheck(isbn_cleaned):
    print("check EBAY 4 " + isbn_cleaned)
    eb_url="https://www.ebay.fr/sch/Livres-BD-revues/267/i.html?_from=R40&_nkw=" + isbn_cleaned
    print(eb_url)
    time.sleep(1)
    eb_page = requests.get(eb_url)
    eb_tree = html.fromstring(eb_page.content)
    eb_prices = eb_tree.xpath('//span[@class="bold"]/text()')
    eb_prices = [x.replace('\t','') for x in eb_prices]
    eb_prices = [x.replace('\n','') for x in eb_prices]
    eb_prices = [x.replace(' ','') for x in eb_prices]
    eb_prices = [x.replace(',','.') for x in eb_prices]
    eb_prices = [float(i) for i in eb_prices]
    #print(eb_prices)
    if eb_prices:
        #eb_cote=sum(eb_prices) / float(len(eb_prices))
        return(eb_prices)
    else:
        return(None)

#########################################################
## PRICES SEARCH ON LBC
#########################################################
def lbc_check(titre,auteur,need_details=None):
    import inspect
    print("check LBC 4 " + str(titre) + " " + str(auteur))
    ori=titre
    titre=titre.split()
    #print("TITRE TYPE : " + str(type(titre)))
    titre=[x.replace('\'','%20') for x in titre]
    titre=[x.replace('(','') for x in titre]
    titre=[x.replace(')','') for x in titre]
    titre=[x.replace(',','') for x in titre]
    keyword=max(titre, key=len)
    auteur=auteur.split()
    auteur=max(auteur, key=len)
    query=auteur + "%20" + keyword
    lbc_url="https://www.leboncoin.fr/livres/offres/?th=1&q=" + query
    print("FIRST LBC QUERY : " + lbc_url)
    time.sleep(3)
    proxy = {"https":"http://163.172.136.39:3128"}
    lbc_page = requests.get(lbc_url, proxies = proxy)
    lbc_tree = html.fromstring(lbc_page.content)
    lbc_prices = lbc_tree.xpath('//h3[@class="item_price"]/text()')
    lbc_prices = [x.replace(' ','') for x in lbc_prices]
    lbc_prices = [x.replace('\n','') for x in lbc_prices]
    lbc_prices = [x.replace('\xa0€','') for x in lbc_prices]
    lbc_prices = [float(k) for k in lbc_prices]
    print("FIRST LBC PRICES : " + str(lbc_prices))
    lbc_url = lbc_tree.xpath('//a[@class="list_item clearfix trackable"]/@href')
    lbc_titles = lbc_tree.xpath('//h2[@class="item_title"]/text()')
    lbc_titles = [x.replace('\n                            \t','') for x in lbc_titles]
    lbc_titles = [x.replace('\n                                \n                            \t\n\t\t\t\t\t\t\t','') for x in lbc_titles]
    lbc_titles = [x.replace('\n                                \n                                \t','') for x in lbc_titles]
    lbc_titles = [x.replace('\n                                \n\t\t\t\t\t\t\t','') for x in lbc_titles]
    print("LBC TITLES : " + str(len(lbc_titles)) + str(lbc_titles))
    print("LBC URLS : " + str(len(lbc_url)) + str(lbc_url))
    lbc_all_rez = zip(lbc_prices,lbc_url,lbc_titles)
    print(lbc_all_rez)
    print(inspect.stack()[1][3])
    if len(lbc_prices) > 10:
        print("I WILL TRY TO GIVE ANOTHER SHOT")
        titre2=sorted(titre,key=len,reverse=True)
        #print(titre2)
        #print("NEW TITRE SORTED IS : " + str(titre) + " so SECOND KEYWORD WILL BE : " + titre[1])
        query=auteur + "%20" + keyword + "%20" + titre[1]
        lbc_url="https://www.leboncoin.fr/livres/offres/?th=1&q=" + query
        time.sleep(3)
        lbc_page = requests.get(lbc_url, proxies = proxy)
        lbc_tree = html.fromstring(lbc_page.content)
        lbc_prices2 = lbc_tree.xpath('//h3[@class="item_price"]/text()')
        lbc_prices2 = [x.replace(' ','') for x in lbc_prices2]
        lbc_prices2 = [x.replace('\n','') for x in lbc_prices2]
        lbc_prices2 = [x.replace('\xa0€','') for x in lbc_prices2]
        lbc_prices2 = [float(k) for k in lbc_prices2]
        print("SECOND LBC PRICES : " + str(lbc_prices2))
        lbc_url = lbc_tree.xpath('//a[@class="list_item clearfix trackable"]/@href')
        lbc_titles = lbc_tree.xpath('//h2[@class="item_title"]/text()')
        lbc_titles = [x.replace('\n                            \t','') for x in lbc_titles]
        lbc_titles = [x.replace('\n                                \n                            \t\n\t\t\t\t\t\t\t','') for x in lbc_titles]
        lbc_titles = [x.replace('\n                                \n                                \t','') for x in lbc_titles]
        lbc_titles = [x.replace('\n                                \n\t\t\t\t\t\t\t','') for x in lbc_titles]
        print("LBC TITLES : " + str(len(lbc_titles)) + str(lbc_titles))
        print("LBC URLS : " + str(len(lbc_url)) + str(lbc_url))
        lbc_all_rez = zip(lbc_prices2,lbc_url,lbc_titles)
        print(lbc_all_rez)
        print(inspect.stack()[1][3])
        if len(lbc_prices2) > 10:
            print("STILL TOO MUCH, LAST CHANCE, STRICT SEARCH")
            query=str(ori)
            query=query.replace(' ', '%20')
            query=query.replace('\'', '%27')
            query=query.replace('é', '%E9')
            lbc_url="https://www.leboncoin.fr/livres/offres/?th=1&q=" + query + "&it=1"
            print("LAST TRY WILL BE ON")
            print(lbc_url)
            time.sleep(3)
            lbc_page = requests.get(lbc_url, proxies = proxy)
            lbc_tree = html.fromstring(lbc_page.content)
            lbc_prices3 = lbc_tree.xpath('//h3[@class="item_price"]/text()')
            lbc_prices3 = [x.replace(' ','') for x in lbc_prices3]
            lbc_prices3 = [x.replace('\n','') for x in lbc_prices3]
            lbc_prices3 = [x.replace('\xa0€','') for x in lbc_prices3]
            lbc_prices3 = [float(k) for k in lbc_prices3]
            lbc_url = lbc_tree.xpath('//a[@class="list_item clearfix trackable"]/@href')
            lbc_titles = lbc_tree.xpath('//h2[@class="item_title"]/text()')
            lbc_titles = [x.replace('\n                            \t','') for x in lbc_titles]
            lbc_titles = [x.replace('\n                                \n                            \t\n\t\t\t\t\t\t\t','') for x in lbc_titles]
            lbc_titles = [x.replace('\n                                \n                                \t','') for x in lbc_titles]
            lbc_titles = [x.replace('\n                                \n\t\t\t\t\t\t\t','') for x in lbc_titles]
            print("LBC TITLES : " + str(len(lbc_titles)) + str(lbc_titles))
            print("LBC URLS : " + str(len(lbc_url)) + str(lbc_url))
            print("LAST LBC PRICES : " + str(len(lbc_prices3)) + str(lbc_prices3))
            lbc_all_rez = zip(lbc_prices3,lbc_url,lbc_titles)
            print(lbc_all_rez)
            print(inspect.stack()[1][3])
            if need_details == True and lbc_all_rez: return(lbc_all_rez)
            if lbc_prices3:
                return(lbc_prices3)
        else:
            #if inspect.stack()[1][3] == 'lbc_search' and lbc_all_rez: return(lbc_all_rez)
            if need_details == True and lbc_all_rez: return(lbc_all_rez)
            if lbc_prices2:
                return(lbc_prices2)
    else:
        if need_details == True and lbc_all_rez: return(lbc_all_rez)
        if lbc_prices:
            return(lbc_prices)

#########################################################
##  PRICES SEARCH ABEBOOK NO ISBN
#########################################################
def abebook_noisbn_price_check(titre=None,auteur=None,annee=None,editeur=None):
    print("PRICES CHECK ON ABEBOOK " + titre + auteur + editeur + annee)
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
    #ab_url="https://www.abebooks.fr/servlet/SearchResults?an=" + auteur + "&bi=0&bx=off&ds=30&pn=" + editeur + "&sortby=1&sts=t&tn=" + keyword + "&yrh=" + annee + "&yrl=" + annee
    ab_url="https://www.abebooks.fr/servlet/SearchResults?an=" + auteur + "&bi=0&bx=off&ds=30&pn=&sortby=1&sts=t&tn=" + keyword + "&yrh=" + annee + "&yrl=" + annee
    print(ab_url)
    #time.sleep(1)
    ab_page = requests.get(ab_url)
    ab_tree = html.fromstring(ab_page.content)
    ab_prices = ab_tree.xpath('//span[@class="price"]/text()[not(ancestor::*[@class="shipping"])]')
    ab_prices = [x.replace('EUR ','') for x in ab_prices]
    ab_prices = [x.replace(',','.') for x in ab_prices]
    ab_prices = [float(k) for k in ab_prices]
    if ab_prices:
        #ab_cote=sum(ab_prices) / float(len(ab_prices))
        return(ab_prices)
    else:
        return(None)

#########################################################
## PRICES SEARCH AMAZON NO ISBN
#########################################################
def amazon_noisbn_price_check(titre=None,auteur=None,annee=None,editeur=None):
    print("PRICES CHECK ON AMAZON " + titre + " " + auteur + " " + editeur + " " + annee)
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
    az_url="https://www.amazon.fr/gp/search/ref=sr_adv_b/?search-alias=stripbooks&__mk_fr_FR=%C3%85M%C3%85Z%C3%95%C3%91&unfiltered=1&field-keywords=&field-author=" + auteur + "&field-title=" + keyword + "&field-isbn=&field-publisher=&field-collection=&node=&field-binding_browse-bin=&field-dateop=&field-datemod=&field-dateyear=&sort=relevancerank&Adv-Srch-Books-Submit.x=42&Adv-Srch-Books-Submit.y=3"
    print(az_url)
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.72 Safari/537.36'
    }
    #time.sleep(1)
    az_page = requests.get(az_url, headers=headers)
    az_tree = html.fromstring(az_page.content)
    az_listings = az_tree.xpath('//a[@class="a-size-small a-link-normal a-text-normal"][1]/@href')
    #print(az_sec_url)
    #print(type(az_sec_url))
    all_az_prices = []
    if az_listings:
        if len(az_listings) > 3:
            ## HARDENING SEARCH
            auteur2=sorted(auteur_ori.split(),key=len,reverse=True)
            if len(auteur2) >= 1:
                az_url="https://www.amazon.fr/gp/search/ref=sr_adv_b/?search-alias=stripbooks&__mk_fr_FR=%C3%85M%C3%85Z%C3%95%C3%91&unfiltered=1&field-keywords=&field-author=" + auteur + "%20" + auteur2[1] + "&field-title=" + keyword + "&field-isbn=&field-publisher=&field-collection=&node=&field-binding_browse-bin=&field-dateop=&field-datemod=&field-dateyear=&sort=relevancerank&Adv-Srch-Books-Submit.x=42&Adv-Srch-Books-Submit.y=3"
            else:
                az_url="https://www.amazon.fr/gp/search/ref=sr_adv_b/?search-alias=stripbooks&__mk_fr_FR=%C3%85M%C3%85Z%C3%95%C3%91&unfiltered=1&field-keywords=&field-author=" + auteur + "%20" + auteur2[1] + "&field-title=" + keyword + "&field-isbn=&field-publisher=&field-collection=&node=&field-binding_browse-bin=&field-dateop=&field-datemod=&field-dateyear=&sort=relevancerank&Adv-Srch-Books-Submit.x=42&Adv-Srch-Books-Submit.y=3"
            print("SECOND AMAZON URL : " + az_url)
            az_page = requests.get(az_url, headers=headers)
            az_tree = html.fromstring(az_page.content)
            az_listings2 = az_tree.xpath('//a[@class="a-size-small a-link-normal a-text-normal"][1]/@href')
            if az_listings2:
                if len(az_listings2) < 3:
                    for link in az_listings2:
                        print(link)
                        time.sleep(4)
                        az_page2 = requests.get(link, headers=headers)
                        az_tree2 = html.fromstring(az_page2.content)
                        az_prices = az_tree2.xpath('//span[@class="a-size-large a-color-price olpOfferPrice a-text-bold"]/text()')
                        az_prices = [x.replace(' ','') for x in az_prices]
                        az_prices = [x.replace('EUR','') for x in az_prices]
                        az_prices = [x.replace(',','.') for x in az_prices]
                        az_prices = [float(k) for k in az_prices]
                        all_az_prices = all_az_prices + az_prices
                        print(all_az_prices)
                    return(all_az_prices)
            else:
                ## HAVE TO FIND ANOTHER request
                return(None)
        else:
            print(az_listings)
            for link in az_listings:
                print(link)
                time.sleep(4)
                az_page2 = requests.get(link, headers=headers)
                az_tree2 = html.fromstring(az_page2.content)
                az_prices = az_tree2.xpath('//span[@class="a-size-large a-color-price olpOfferPrice a-text-bold"]/text()')
                az_prices = [x.replace(' ','') for x in az_prices]
                az_prices = [x.replace('EUR','') for x in az_prices]
                az_prices = [x.replace(',','.') for x in az_prices]
                az_prices = [float(k) for k in az_prices]
                all_az_prices = all_az_prices + az_prices
                print(all_az_prices)
            return(all_az_prices)
    else:
        return(None)

#########################################################
## PRICES SEARCH EBAY NO ISBN
#########################################################
def ebay_noisbn_price_check(titre=None,auteur=None,annee=None,editeur=None):
    print("PRICES CHECK ON EBAY " + titre + auteur + editeur + annee)
    titre_ori = titre
    titre = titre.split()
    auteur_ori = auteur
    auteur = auteur.split()
    editeur_ori = editeur
    editeur = editeur.split()
    #print("TITRE TYPE : " + str(type(titre)))
    titre=[x.replace('\'','%20') for x in titre]
    titre=[x.replace('(','') for x in titre]
    titre=[x.replace(')','') for x in titre]
    titre=[x.replace(',','') for x in titre]
    auteur=max(auteur, key=len)
    keyword=max(titre, key=len)
    editeur=max(editeur, key=len)
    eb_url="https://www.ebay.fr/sch/Livres-BD-revues/267/i.html?_from=R40&_nkw=" + keyword + "+" + auteur + "+" + editeur
    print(eb_url)
    time.sleep(1)
    eb_page = requests.get(eb_url)
    eb_tree = html.fromstring(eb_page.content)
    #eb_prices = eb_tree.xpath('//span[@class="bold"]/text()')
    eb_prices = eb_tree.xpath('//span[@class="bold"]/text()[not(preceding::*[@class="lvresult clearfix li"])]')
    eb_prices = [x.replace('\t','') for x in eb_prices]
    eb_prices = [x.replace('\n','') for x in eb_prices]
    eb_prices = [x.replace(' ','') for x in eb_prices]
    eb_prices = [x.replace(',','.') for x in eb_prices]
    eb_prices = [float(i) for i in eb_prices]
    #print(eb_prices)
    if eb_prices:
        #eb_cote=sum(eb_prices) / float(len(eb_prices))
        if len(eb_prices) > 10:
            ##DO ANOTHER CHECK
            eb_url="https://www.ebay.fr/sch/Livres-BD-revues/267/i.html?_from=R40&_nkw=" + titre[0] + "+" + auteur + "+" + editeur
            print("2ND CHECK ON EBAY : " + eb_url)
            time.sleep(1)
            eb_page = requests.get(eb_url)
            eb_tree = html.fromstring(eb_page.content)
            print(eb_tree)
            #eb_prices2 = eb_tree.xpath('//span[@class="bold"]/text()')
            eb_prices2 = eb_tree.xpath('//span[@class="bold"]/text()[not(preceding::*[@class="lvresult clearfix li"])]')
            eb_prices2 = [x.replace('\t','') for x in eb_prices2]
            eb_prices2 = [x.replace('\n','') for x in eb_prices2]
            eb_prices2 = [x.replace(' ','') for x in eb_prices2]
            eb_prices2 = [x.replace(',','.') for x in eb_prices2]
            eb_prices2 = [float(i) for i in eb_prices2]
            if eb_prices2:
                return(eb_prices2)
        else:
            return(eb_prices)
    else:
        eb_url="https://www.ebay.fr/sch/Livres-BD-revues/267/i.html?_from=R40&_nkw=" + titre[0] + "+" + auteur + "+" + editeur
        print("2ND CHECK ON EBAY : " + eb_url)
        time.sleep(1)
        eb_page = requests.get(eb_url)
        eb_tree = html.fromstring(eb_page.content)
        print(eb_tree)
        #eb_prices2 = eb_tree.xpath('//span[@class="bold"]/text()')
        eb_prices2 = eb_tree.xpath('//span[@class="bold"]/text()[not(preceding::*[@class="lvresult clearfix li"])]')
        eb_prices2 = [x.replace('\t','') for x in eb_prices2]
        eb_prices2 = [x.replace('\n','') for x in eb_prices2]
        eb_prices2 = [x.replace(' ','') for x in eb_prices2]
        eb_prices2 = [x.replace(',','.') for x in eb_prices2]
        eb_prices2 = [float(i) for i in eb_prices2]
        if eb_prices2:
            return(eb_prices2)
        else:
            return(None)

#########################################################
##  PRICES SEARCH PRICEMINISTER NO ISBN
#########################################################
def pminister_noisbn_price_check(titre=None,auteur=None,annee=None,editeur=None):
    print("PRICES CHECK ON PRICEMINISTER " + titre + auteur + editeur + annee)
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
    pm_url="http://www.priceminister.com/s/" + keyword + "+" + auteur + "?nav=Livres"
    print(pm_url)
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.72 Safari/537.36'
    }
    time.sleep(1)
    pm_page = requests.get(pm_url, headers=headers)
    pm_tree = html.fromstring(pm_page.content)
    pm_listings = pm_tree.xpath('//div[contains(@class, \'marketPlace\')]/div[contains(@class, \'allOffers\')]/div[contains(@class, \'offer usedOffers\')]/span[contains(@class, \'totalOffers\')]/a/@href')
    if not pm_listings: return(None)
    all_pm_prices = []
    if pm_listings:
        print(pm_listings)
        if len(pm_listings) > 4:
            ##HARDENING SEARCH
            titre_ori=titre_ori.split()
            titre2=sorted(titre_ori,key=len,reverse=True)
            pm_url="http://www.priceminister.com/s/" + keyword + "+" + titre2[1] + "+" + auteur + "?nav=Livres"
            print(pm_url)
            headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.72 Safari/537.36'
            }
            time.sleep(1)
            pm_page = requests.get(pm_url, headers=headers)
            pm_tree = html.fromstring(pm_page.content)
            pm_listings2 = pm_tree.xpath('//p/a[contains(@class, \'price typeNew\')]/@href')
            if not pm_listings2: return(None)
            if pm_listings2:
                for link in pm_listings2:
                    pm_temp_url ="http://www.priceminister.fr" + link
                    print(pm_temp_url)
                    time.sleep(1)
                    pm_page2 = requests.get(pm_temp_url, headers=headers)
                    pm_tree2 = html.fromstring(pm_page2.content)
                    pm_prices1 = pm_tree2.xpath('//p[@class="price typeUsed spacerBottomXs"]/text()[not(ancestor::*[@class="infosPrice spacerBottomS "])]')
                    pm_prices2 = pm_tree2.xpath('//p[@class="price typeCollec spacerBottomXs"]/text()[not(ancestor::*[@class="infosPrice spacerBottomS "])]')
                    pm_prices3 = pm_tree2.xpath('//p[@class="price typeNew spacerBottomXs"]/text()[not(ancestor::*[@class="infosPrice spacerBottomS "])]')
                    #if pm_prices1 and pm_prices2 and pm_prices3:
                    #    all_pm_prices = all_pm_prices + pm_prices1 + pm_prices2 + pm_prices3
                    if pm_prices1:
                        all_pm_prices = all_pm_prices + pm_prices1
                    if pm_prices2:
                        all_pm_prices = all_pm_prices + pm_prices2
                    if pm_prices3:
                        all_pm_prices = all_pm_prices + pm_prices3
                    #del pm_prices[0]#corrected with not ancestor at previous line
                if all_pm_prices:
                    all_pm_prices = [x.replace('\xa0€','') for x in all_pm_prices]
                    all_pm_prices = [x.replace(',','.') for x in all_pm_prices]
                    all_pm_prices = [float(j) for j in all_pm_prices]
                    print(all_pm_prices)
                    #pm_cote=sum(pm_prices) / float(len(pm_prices))
                    return(all_pm_prices)
                else:
                    return(None)
        else:
            for link in pm_listings:
                pm_temp_url ="http://www.priceminister.fr" + link
                time.sleep(1)
                pm_page2 = requests.get(pm_temp_url, headers=headers)
                pm_tree2 = html.fromstring(pm_page2.content)
                pm_prices1 = pm_tree2.xpath('//p[@class="price typeUsed spacerBottomXs"]/text()[not(ancestor::*[@class="infosPrice spacerBottomS "])]')
                pm_prices2 = pm_tree2.xpath('//p[@class="price typeCollec spacerBottomXs"]/text()[not(ancestor::*[@class="infosPrice spacerBottomS "])]')
                if pm_prices1 and pm_prices2:
                    all_pm_prices = all_pm_prices + pm_prices1 + pm_prices2
                elif pm_prices1:
                    all_pm_prices = all_pm_prices + pm_prices1
                elif pm_prices2:
                    all_pm_prices = all_pm_prices + pm_prices2
                #del pm_prices[0]#corrected with not ancestor at previous line
            if all_pm_prices:
                all_pm_prices = [x.replace('\xa0€','') for x in all_pm_prices]
                all_pm_prices = [x.replace(',','.') for x in all_pm_prices]
                all_pm_prices = [float(j) for j in all_pm_prices]
                print(all_pm_prices)
                #pm_cote=sum(pm_prices) / float(len(pm_prices))
                return(all_pm_prices)
            else:
                return(None)

#########################################################
## PRICES CHECK ON WEB NO ISBN
#########################################################
def glob_search(titre=None,auteur=None,annee=None,editeur=None):

    abebook_noisbn_prices = abebook_noisbn_price_check(titre,auteur,editeur,annee)
    amazon_noisbn_prices = amazon_noisbn_price_check(titre,auteur,editeur,annee)
    ebay_noisbn_prices = ebay_noisbn_price_check(titre,auteur,editeur,annee)
    pminister_noisbn_prices = pminister_noisbn_price_check(titre,auteur,editeur,annee)
    lbc_noisbn_prices = lbc_check(titre,auteur)
    #session.execute("INSERT INTO keyspace1.history (id, bookid, abebook, amazon, ebay, priceminister, lbc) VALUES (%s, %s, %s, %s, %s, %s, %s)", (cassandra.util.uuid_from_time(time.time()), bookid, abebook_noisbn_prices, amazon_noisbn_prices, ebay_noisbn_prices, pminister_noisbn_prices, lbc_noisbn_prices))
    globsearch = []
    globsearch.append(amazon_noisbn_prices)
    globsearch.append(abebook_noisbn_prices)
    globsearch.append(ebay_noisbn_prices)
    globsearch.append(pminister_noisbn_prices)
    globsearch.append(lbc_noisbn_prices)
    print(globsearch)
    return(globsearch)
    #return(None)

#########################################################
## LAUNCH ALL PRICES SEARCH AND INSERT THEM IN CASSANDRA
#########################################################
def glob_isearch(isbn13=None,titre=None,auteur=None,annee=None,editeur=None,isbn10=None):
    if isbn10 or isbn13:
        az_icheck_rez=amazon_icheck(isbn13)
        if not az_icheck_rez: az_icheck_rez=amazon_icheck(isbn10)
        ab_icheck_rez=abebook_icheck(isbn13)
        if not ab_icheck_rez: ab_icheck_rez=abebook_icheck(isbn10)
        pm_icheck_rez=priceminister_icheck(isbn13)
        if not pm_icheck_rez: pm_icheck_rez=priceminister_icheck(isbn10)
        eb_icheck_rez=ebay_icheck(isbn13)
        if not eb_icheck_rez: eb_icheck_rez=ebay_icheck(isbn10)
        lbc_check_rez=lbc_check(titre,auteur)
        #session.execute("INSERT INTO keyspace1.history (id, bookid, abebook, amazon, ebay, priceminister, lbc) VALUES (%s, %s, %s, %s, %s, %s, %s)", (cassandra.util.uuid_from_time(time.time()), bookid, ab_icheck_rez, az_icheck_rez, eb_icheck_rez, pm_icheck_rez, lbc_check_rez))
        print('amazon price is : ' + str(az_icheck_rez))
        print('abebook price is : ' + str(ab_icheck_rez))
        print('ebay price is : ' + str(eb_icheck_rez))
        print('priceminister price is : ' + str(pm_icheck_rez))
        print('lbc price is : ' + str(lbc_check_rez))
        globsearch = []
        globsearch.append(az_icheck_rez)
        globsearch.append(ab_icheck_rez)
        globsearch.append(eb_icheck_rez)
        globsearch.append(pm_icheck_rez)
        globsearch.append(lbc_check_rez)
        print(globsearch)
        return(globsearch)
        #return(None)
    else:
        ###CALL TO PRICES CHECK NO ISBN
        globsearch = glob_search(titre,auteur,editeur,annee)
        return(globsearch)
