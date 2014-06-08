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
	startTime = raw_input("Start Time(eg: 2013060612): ")#"2014"#
	endTime = raw_input("End Time(eg: 201361712): ")
	stnm = raw_input("Station name (eg: 72318): ")#"72318"#
	return [startTime,endTime,stnm]

def tgetInput():
	return ["2014050612","2014051712","72318"]

def crawler(url,ofName):
	data = urllib2.urlopen(url).readlines()
	oFile = open(ofName,"w")
	for line in data:
		line = stripTags(line)
		if line[0:11] == "Description":
			break
		oFile.write(line)
	oFile.close()

def getSvLoc():
	return tkFileDialog.askdirectory(title="Please select your directory") 

def tgetSvLoc():
	return "Data"

def getDateStr(st):
	return [int(st[0:4]),int(st[4:6]),int(st[6:8]),int(st[8:])]

def dateRange(sdate,edate):
	print sdate,edate
	for n in range(int((sdate-edate).days)):
		yield sdate+timedelta(n)

def uwyoCrawler():
	[sTime,eTime,stnm] = tgetInput()
	[syear,smonth,sday,shour] = getDateStr(sTime)
	[eyear,emonth,eday,ehour] = getDateStr(eTime)
	svloc = tgetSvLoc()
	date1 = date(syear,smonth,sday)
	date2 = date(eyear,emonth,eday)
	intv = (date2-date1).days
	for days in range(intv):
		idate = date1+timedelta(days)
		iurl = url%(idate.year,idate.month,idate.day,"00",idate.day,"00",stnm)
		ofName = svloc+os.sep+stnm+'-'+idate.strftime("%Y%m%d")+"00.txt"
		crawler(iurl,ofName)

		iurl = url%(idate.year,idate.month,idate.day,"12",idate.day,"12",stnm)
		ofName = svloc+os.sep+stnm+'-'+idate.strftime("%Y%m%d")+"12.txt"
		crawler(iurl,ofName)
		print iurl,ofName


if __name__ == '__main__':
	# print getDateStr("2014061712")
	uwyoCrawler()
	# print stripTags("<HTML> ss")