import urllib2
import socket
import os
import re
import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def gethtml(page_number):
    try:
        req = urllib2.Request('http://hk.jobsdb.com/hk/jobs/engineering/' + page_number)
        response = urllib2.urlopen(req)
        html = response.read()

        if not os.path.isdir('html'):
            os.mkdir('./html')
        filename = './html/' + page_number + '.html'
        with open(filename, 'w') as f:
            f.write(html)
    except Exception as e:
        print e

def writeopening(company_name, jobtitle, filename):
    try:
        # Write company name and job title info to file
        with open('./html/' + filename + '.txt', 'a') as jdfile:
            if company_name is not None:
                jdfile.write(parser.unescape(company_name.strip()) + ': \n\t')
            if jobtitle.__len__() > 0 and jobtitle[0].__len__() > 0:
                if jobtitle[0][0].__len__() > 0:
                    jdfile.write(parser.unescape(jobtitle[0][0].strip()) + '\n')
                elif jobtitle[0][1].__len__() > 0:
                    jdfile.write(parser.unescape(jobtitle[0][1].strip()) + '\n')
            jdfile.write('\n')
    except Exception as e:
        print e

def crawl(page_number):

    try:
        with open('./html/' + page_number +'.html', 'r') as htmlfile:
            html = htmlfile.read()
            html = html.decode("utf-8")
            jdurls = re.findall('<a class="posLink" href="(.*?)".id="cp(.*?)">', html, re.S)

            for jdurl in jdurls:
                print jdurl
                jdreq = urllib2.Request(jdurl[0])
                jdresponse = urllib2.urlopen(jdreq)
                jdhtml = jdresponse.read()

                # Get job title
                jobtitle = re.findall('<h1 itemprop="title" class="general-pos ad-y-auto-txt">(.*?)</h1>|<h1 class="general-pos ad-y-auto-txt2" itemprop="title">(.*?)</h1>', jdhtml, re.S)

                # Get company name
                company = re.findall(r'<h2 itemprop="hiringOrganization" class="jobad-header-company">(.*?)</h2>|<h2 class="jobad-header-company ad-y-auto-txt1" itemprop="hiringOrganization">(.*?)</h2>', jdhtml, re.S)
                print company

                # See if there is an url contained in the company name search result
                if company.__len__() > 0 and company[0].__len__() > 0:
                    company_info = re.findall(r'<a href="(.*?)" target="_blank" class="popupInvoker">(.*?)</a>', company[0][0], re.S)
                    if company_info.__len__()>0:
                        company_link, company_name = company_info[0][0], company_info[0][1]
                        print company_link, company_name
                    else:
                        if company[0][0].__len__() > 0:
                            company_name = company[0][0]
                        elif company[0][1].__len__() > 0:
                            company_name = company[0][1]

                writeopening(company_name, jobtitle, 'opening')
                writeopening(company_name, jobtitle, 'requirement')

                jobrequire = re.findall(r'<div itemprop="responsibilities" class="jobad-primary-details col-xs-9">(.*?)</div>|<div itemprop="responsibilities" class="jobad-primary-details">(.*?)</div>', jdhtml, re.S)
                with open('./html/requirement.txt', 'a') as jdfile:
                    if jobrequire.__len__() > 0 and jobrequire[0][0].__len__() > 0:
                        print jobrequire[0]
                        jobrequire_items = re.findall(r'>([\w ]+[^<>]+[\w ]+?)<', jobrequire[0][0], re.S)
                        if jobrequire_items is not None:
                            for jobrequire_item in jobrequire_items:
                                jdfile.write('\t\t' + jobrequire_item.strip() + '\n')
                    jdfile.write('\n')
    except Exception as e:
        print e


if __name__ == '__main__':
    socket.setdefaulttimeout(10)
    parser = HTMLParser.HTMLParser()
    for page_number in range(1, 200):
        print "crawling Page: ", page_number, "\n\n\n\n\n"
        gethtml(str(page_number))
        crawl(str(page_number))
