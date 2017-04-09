import urllib2
import os
import re
import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def gethtml(page_number):
    req = urllib2.Request('http://hk.jobsdb.com/hk/jobs/engineering/' + page_number)
    response = urllib2.urlopen(req)
    html = response.read()

    if not os.path.isdir('html'):
        os.mkdir('./html')
    filename = './html/' + page_number + '.html'
    with open(filename, 'w') as f:
        f.write(html)

def crawl(page_number):
    parser = HTMLParser.HTMLParser()
    with open('./html/' + page_number +'.html', 'r') as htmlfile:
        html = htmlfile.read()
        html = html.decode("utf-8")
        jdurls = re.findall('<a class="posLink" href="(.*?)".id="cp(.*?)">', html, re.S)

        for jdurl in jdurls:
            print jdurl
            jdreq = urllib2.Request(jdurl[0])
            jdresponse = urllib2.urlopen(jdreq)
            jdhtml = jdresponse.read()
            jdhtml = jdhtml.decode("utf-8")

            jobtitle = re.findall('<h1 itemprop="title" class="general-pos ad-y-auto-txt">(.*?)</h1>|<h1 class="general-pos ad-y-auto-txt2" itemprop="title">(.*?)</h1>', jdhtml, re.S)

            company = re.findall(r'<h2 itemprop="hiringOrganization" class="jobad-header-company">(.*?)</h2>|<h2 class="jobad-header-company ad-y-auto-txt1" itemprop="hiringOrganization">(.*?)</h2>', jdhtml, re.S)
            print company
            if company.__len__() > 0 and company[0].__len__() > 0:
                company_info = re.findall(r'<a href="(.*?)" target="_blank" class="popupInvoker">(.*?)</a>', company[0][0], re.S)
            if company_info.__len__()>0:
                company_link, company_name = company_info[0][0], company_info[0][1]
                print company_link, company_name
            else:
                if company.__len__() > 0 and company[0].__len__() > 0 and company[0][0].__len__() > 0:
                    company_name = company[0][0]
                elif company.__len__() > 0 and company[0].__len__() > 0 and company[0][1].__len__() > 0:
                    company_name = company[0][1]



            with open('./html/openings.txt', 'a') as jdfile:
                jdfile.write(parser.unescape(company_name.strip()) + ': \n\t')
                if jobtitle[0][0].__len__() > 0:
                    jdfile.write(parser.unescape(jobtitle[0][0].strip()) + '\n')
                elif jobtitle[0][1].__len__() > 0:
                    jdfile.write(parser.unescape(jobtitle[0][1].strip()) + '\n')
                jdfile.write('\n')

            jobrequire = re.findall(r'<div itemprop="responsibilities" class="jobad-primary-details col-xs-9">(.*?)</ul>', jdhtml, re.S)
            with open('./html/jd.txt', 'a') as jdfile:
                if jobrequire.__len__() > 0:
                    jdfile.write(jobrequire[0].strip() + '\n\n\n\n\n')


if __name__ == '__main__':
    for page_number in range(1, 100):
        print "crawling Page: ", page_number, "\n\n\n\n\n"
        gethtml(str(page_number))
        crawl(str(page_number))
