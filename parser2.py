'''
Created on Nov 27, 2013; Modified on June 11, 2015

@author: dmatt and mstock
'''
import urllib2_file
import time
import json
from mechanize import Browser
from bs4 import BeautifulSoup
import mechanize
import cookiejar
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import os

global basefilename

# Set filename
def getName():
    global basefilename

    # CHANGE!!!
    basefilename = "C:/Users/mstock/Dropbox/Public/CSV"

# Scrapes Prediction Tracker for NBA
def parsePT_NBA ():

    soup = BeautifulSoup(urllib2_file.urlopen('http://www.thepredictiontracker.com/prednba.html').read())
    if soup.get_text() == '':
        print( ("Sorry no games today for NBA (PT)"))
        return
    else:
        pre2 = soup.pre.next_sibling.next_sibling.pre.b.next_sibling
        split2 = pre2.splitlines()

        filename = basefilename+"/"+"PT_NBA"+time.strftime("%m_%d_%Y")+".csv"

        f = open(filename,"w")
        f.write("\n")
        split2.pop(0)
        for i in split2:
            temp = i.split("        ")
            temp[:] = (value for value in temp if value != u'')
            t1 = [temp[0],temp[1]]
            t2 = temp[2].split()
            temp = t1+t2
            for j in temp:
                f.write(j.strip())
                f.write(",")
            f.write("\n")
        f.close()

# Scrapes Prediction Tracker for NCAAB
def parsePT_NCAAB ():

    soup = BeautifulSoup(urllib2_file.urlopen('http://www.thepredictiontracker.com/predbb.html').read())
    if soup.get_text() == '':
        print( "Sorry no games today for NCAAB (PT)")
        return
    else:
        pre2 = soup.pre.next_sibling.next_sibling.pre.b.next_sibling
        split2 = pre2.splitlines()

        filename = basefilename+"/"+"PT_NCAAB"+time.strftime("%m_%d_%Y")+".csv"

        f = open(filename,"w")
        f.write("\n")
        split2.pop(0)
        for i in split2:
            temp = i.split("    ")
            temp[:] = (value for value in temp if value != u'')
            t1 = [temp[0],temp[1]]
            t2 = temp[2].split()
            temp = t1+t2
            for j in temp:
                f.write(j.strip())
                f.write(",")
            f.write("\n")
        f.close()

# Scrapes ESPN's Insider Pickcenter
def espnScrape():
    ncaab = 'http://insider.espn.go.com/insider/pickcenter/index?sport=ncb#'
    html = get_ESPN_pickcenter_html(ncaab)
    parseESPNPickcenterV2(html,"NCB")

    nba = 'http://insider.espn.go.com/insider/pickcenter/index?sport=nba#'
    html = get_ESPN_pickcenter_html(nba)
    parseESPNPickcenterV2(html,"NBA")

# Logs in to ESPN's Insider Pickcenter
def parseESPNPickcenter ():

    filename = basefilename+"/"+"ESPNPickcenter"+time.strftime("%m_%d_%Y")+".csv"
    f = open(filename,"w")

    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookiejar.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    br.addheaders = [('User-agent', 'Chrome')]

    # The site we will navigate into, handling it's session
    br.open('http://espn.go.com/login/')

    # Select the form
    br.select_form(nr=0)

    # User credentials
    br.form['username'] = 'lswmovies'
    br.form['gspw'] = 'dukesux'

    # Login
    br.submit()

    soupy = BeautifulSoup(br.open('http://insider.espn.go.com/insider/pickcenter/index?sport=mlb').read())
    soup = soupy.get_text()
    split2 = soup.splitlines()

    master = []
    ind = 0

    for i in split2:
        temp = i.split("PickCenter Details")
        ind += 1

        if temp[0].strip() == "TEAMRANKINGSNUMBERFIRE":
            x = ind
            for j in range(x+1,x+1+20):
                if split2[j].strip() != '':
                    master.append(split2[j].strip())
            master.append("break")

        elif temp[0].strip() == "TRNF":
            x = ind
            for j in range(x+1,x+1+35):
                if split2[j].strip() != '':
                    master.append(split2[j].strip())
            master.append("break")

    for n in master:
        if n == "break":
            f.write("\n")
        else:
            f.write(n.strip())
            f.write(",")
    f.close()

# Broswer for ESPN Pickcenter
def get_ESPN_pickcenter_html(source):
    browser = webdriver.Firefox()
    browser.get(source)
    browser.find_element_by_id('ins_signin').click()
    browser.switch_to_frame('disneyid-iframe')
    browser.find_element_by_css_selector('input[ng-model="vm.username"]').send_keys('lswmovies')
    browser.find_element_by_css_selector('input[ng-model="vm.password"]').send_keys('dukesux')
    browser.find_element_by_css_selector('button[type="submit"]').click()
    browser.get(source)
    return browser.page_source

# Parses TeamRankings, NumberFire from ESPN Pickcenter
def parseESPNPickcenterV2(html,name):
    filename = basefilename+"/"+"ESPNPickcenter"+name+time.strftime("%m_%d_%Y")+".csv"

    soupy = BeautifulSoup(html)
    soup = soupy.get_text()
    split2 = soup.splitlines()

    master = []
    ind = 0

    for i in split2:
        temp = i.split("PickCenter Details")
        ind += 1

        if temp[0].strip() == "TEAMRANKINGSNUMBERFIRE":
            x = ind
            for j in range(x+1,x+1+20):
                if split2[j].strip() != '':
                    master.append(split2[j].strip())
            master.append("break")

        elif temp[0].strip() == "TRNF":
            x = ind
            for j in range(x+1,x+1+35):
                if split2[j].strip() != '':
                    master.append(split2[j].strip())
            master.append("break")

    with open(filename, 'w') as f:
        for n in master:
            if n == "break":
                f.write("\n")
            else:
                if re.match('\d\d?', n.strip()) and len(n.strip()) <= 2:
                    #eat the ranking
                    continue
                f.write(n.strip())
                f.write(",")
        f.close()

# Scrapes MLB from Massey
def parseM_MLB ():
    soup = BeautifulSoup(urllib2_file.urlopen('http://masseyratings.com/predjson.php?s=mlb&sub=14342&&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_MLB"+time.strftime("%m_%d_%Y")+".csv"

    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,TotalPred\n")
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        totalPred = str(i[14][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+totalPred+'\n')

# Scrapes NHL from Massey
def parseM_NHL ():
    soup = BeautifulSoup(urllib2_file.urlopen('http://masseyratings.com/predjson.php?s=nhl&&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_NHL"+time.strftime("%m_%d_%Y")+".csv"

    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,TotalPred\n")
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        totalPred = str(i[14][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+totalPred+'\n')

# Scrapes NBA from Massey
def parseM_NBA ():
    soup = BeautifulSoup(urllib2_file.urlopen('http://masseyratings.com/predjson.php?s=nba&&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_NBA"+time.strftime("%m_%d_%Y")+".csv"

    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,TotalPred\n")
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        totalPred = str(i[14][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+totalPred+'\n')

# Scrapes NCAAB from Massey
def parseM_NCAAB ():
    soup = BeautifulSoup(urllib2_file.urlopen('http://masseyratings.com/predjson.php?s=cb&sub=11590').read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_NCAAB"+time.strftime("%m_%d_%Y")+".csv"

    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,TotalPred\n")
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        totalPred = str(i[14][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+totalPred+'\n')

# Scrapes MLS from Massey
def parseM_MLS ():
    soup = BeautifulSoup(urllib2_file.urlopen('http://masseyratings.com/predjson.php?s=mls&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_MLS"+time.strftime("%m_%d_%Y")+".csv"

    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

# Scrapes WNBA from Massey
def parseM_WNBA ():
    soup = BeautifulSoup(urllib2_file.urlopen('http://masseyratings.com/predjson.php?s=wnba&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_WNBA"+time.strftime("%m_%d_%Y")+".csv"

    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

# Scrapes CFL from Massey
def parseM_CFL ():
    soup = BeautifulSoup(urllib2_file.urlopen('http://masseyratings.com/predjson.php?s=cfl&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_CFL"+time.strftime("%m_%d_%Y")+".csv"

    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

getName()
parsePT_NBA()
#parsePT_NCAAB()

#parseM_NCAAB()
parseM_MLB()
parseM_NBA()
parseM_NHL()
parseM_MLS()
parseM_WNBA()
parseM_CFL()

#espnScrape()
