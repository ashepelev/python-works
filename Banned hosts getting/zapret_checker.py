#!/usr/bin/env python
# -*- coding: utf-8 -*-
# yegorov-p.ru
from xml.etree.ElementTree import ElementTree
from datetime import datetime,timedelta
from zapretinfo import ZapretInfo
import time
import zipfile
import re
import os
import commands
from base64 import b64decode



XML_FILE_NAME = "/usr/local/ban-sites/request.xml"
P7S_FILE_NAME = "/usr/local/ban-sites/request.xml.sig"
ts=""
#���� ������ ����� ����������, �� ������� �������� �� ���� ������
try:
    ts=ElementTree().parse("/usr/local/ban-sites/dump.xml").attrib['updateTime']
    dt = datetime.strptime(ts[:19],'%Y-%m-%dT%H:%M:%S')
    fromFile=int(time.mktime(dt.timetuple()))
except:
    fromFile=0

opener=ZapretInfo()
try:
    lastDumpDate=opener.getLastDumpDate()
#    print 'lastDumpDate: %s' % (lastDumpDate)
#    print 'fromFileDate: %s' % (fromFile)
except:
    exit(0)
#���������, ��������� �� ������
if lastDumpDate/1000<>fromFile:
    ts=ElementTree().parse("/usr/local/ban-sites/dump.xml").attrib['updateTime']
#    print 'Base is outdated. Downloading new version...'
#    print 'Current base version: ' + ts
    #������ ���������. ���������� ������ �� ��������
    try:
        request=opener.sendRequest(XML_FILE_NAME,P7S_FILE_NAME)
    except:
        exit(0)
    #���������, ������ �� ������ � ���������
    if request['result']:
        #������ �� ������, ������� ���
        code=request['code']
        #print 'Got code %s' % (code)
        tstart = datetime.now()
        #print 'Trying to get result...'
        while 1:
            #�������� �������� ����� �� ����
            try:
                request=opener.getResult(code)
            except:
                exit(0)
            if request['result']:
                #����� �������, ��������� ��� � �������������
                tend = datetime.now()
                tdiff = tend - tstart
                #print 'Base ready.'
                #print 'Code was obtained in ' + str(tdiff.seconds) + ' seconds.'
				os.system("mv /usr/local/ban-sites/dump.xml /usr/local/ban-sites/dump.xml.old")
                file = open('/usr/local/ban-sites/result.zip', "wb")
                file.write(b64decode(request['registerZipArchive']))
                file.close()

                zip_file = zipfile.ZipFile('/usr/local/ban-sites/result.zip', 'r')
                zip_file.extract('dump.xml', '/usr/local/ban-sites/')
                zip_file.close()
                os.system("rm /usr/local/ban-sites/result.zip")
                ts=ElementTree().parse("/usr/local/ban-sites/dump.xml").attrib['updateTime']
                #print 'Base updated. New version: ' + ts
                file = open("/usr/local/ban-sites/dump.xml","r")
                data = file.read()
                file.close()
                os.system("mv /usr/local/ban-sites/hosts /usr/local/ban-sites/hosts.old")

                th = []
                result = re.finditer("\[CDATA\[[a-z0-9.-]+\]\]", data)
                for match in result :
                        th.append(match.group())

                file = open("/usr/local/ban-sites/tmp","w")
                for x in set(th):
                        t = x[:-2]
                        file.write(t[7:]+'\n')
                file.close()
                status, output = commands.getstatusoutput("sort /usr/local/ban-sites/tmp")
                file = open("/usr/local/ban-sites/hosts","w")
                file.write(output)
                file.close()
                os.system("rm /usr/local/ban-sites/tmp")

                status, output = commands.getstatusoutput("diff -u /usr/local/ban-sites/hosts.old /usr/local/ban-sites/hosts")
                if output:
                        print "Ban-domains list updated"
                        print "Current version: " + ts
                        print output
                break
            else:
                #����� �� �������, ��������� �������.
                if request['resultComment']=='������ ��������������':
                    #���� ��� ��������� �� ��������� �������, �� ������ ���� �������.
                    time.sleep(60)
                else:
                    #���� ��� ����� ������ ������, ������� �� � ���������� ������
                    print 'Error: %s' % request['resultComment']
                    break
    else:
        #������ �� ������, ���������� ������
        print 'Error: %s' % request['resultComment']
