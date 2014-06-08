#!/bin/python

import urllib2,re,os,tkFileDialog,time
from datetime import date,timedelta

url = "http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%%3ALIST&YEAR=%d&MONTH=%02d&FROM=%02d%s&TO=%02d%s&STNM=%s"

def stripTags(line):
	p = re.compile(r'<.*?>')
	line = p.sub('', line)
	# print line
	return line

def getInput():
	startTime = raw_input("Start Time(eg: 20130606): ")#"2014"#
	endTime = raw_input("End Time(eg: 20130712): ")
	stnm = raw_input("Station name (eg: 72318): ")#"72318"#
	return [startTime,endTime,stnm]

def tgetInput():
	return ["20140506","20140517","72318"]

def findMonthEnd(d0):
	de = d0
	while(d0.month==de.month):
		d0 = d0+timedelta(1)
	return d0-timedelta(1)

def crawler(d1,d2,stnm,svloc):
	iurl = url%(d1.year,d1.month,d1.day,"00",d2.day,"12",stnm)
	print iurl
	timeflag = True
	conFlag = False
	data = urllib2.urlopen(iurl).readlines()
	for il in data:
		il = stripTags(il)
		if il[0:5] == stnm:
			conFlag = True
			ofName = svloc+os.sep+stnm+'-'+d1.strftime("%Y%m%d")
			if timeflag:
				ofName+="00.txt"
			else:
				ofName+="12.txt"
				d1 += timedelta(1)
			timeflag = not timeflag
			oFile = open(ofName,"w")
		if il[0:11] == "Description":
			break	
		if conFlag:
			oFile.write(il)

def preCrawler(d1,d2,stnm,svloc):
	while(d1<d2):
		ed = findMonthEnd(d1)
		ed = min(ed,d2)
		crawler(d1,ed,stnm,svloc)
		d1 = ed+timedelta(1)


def getSvLoc():
	return tkFileDialog.askdirectory(title="Please select your directory") 

def tgetSvLoc():
	return "Data"

def getDateStr(st):
	return [int(st[0:4]),int(st[4:6]),int(st[6:])]

def dateRange(sdate,edate):
	print sdate,edate
	for n in range(int((sdate-edate).days)):
		yield sdate+timedelta(n)

def uwyoCrawler():
	[sTime,eTime,stnm] = getInput()
	[syear,smonth,sday] = getDateStr(sTime)
	[eyear,emonth,eday] = getDateStr(eTime)
	svloc = getSvLoc()
	date1 = date(syear,smonth,sday)
	date2 = date(eyear,emonth,eday)
	intv = (date2-date1).days
	preCrawler(date1,date2,stnm,svloc)


if __name__ == '__main__':
	uwyoCrawler()
	# print findMonthEnd(date(2013,2,1))
	# crawler(date(2013,02,2),date(2013,02,5),"72318","Data")
	# preCrawler(date(2013,02,2),date(2013,03,5),"72318","Data")