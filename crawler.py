import html.parser
import urllib.request
import urllib.parse
import re

class LinkParser(html.parser.HTMLParser):


    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        proxy_url = 'dfw-proxy.ext.ray.com:80'
        s_proxy_url = 'dfw-proxy.ext.ray.com:80'
        proxy_support = urllib.request.ProxyHandler({'http': proxy_url})
        s_proxy_support = urllib.request.ProxyHandler({'https': s_proxy_url})
        opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler)
        opener.add_handler(s_proxy_support)
        urllib.request.install_opener(opener)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = urllib.parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]
        if tag == 'meta':
                descFound = False
                for (key, value) in attrs:
                    if descFound and key == 'content' and 'reddit: the' in value:
                        if 'reddit.com' not in self.baseUrl:
                            self.isRedditMasked = True
                            break

                    if key == 'name' and value == 'description':
                        descFound = True

    def getLinks(self, url):
        try:
            self.links = []
            self.baseUrl = url
            user_agent = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' #pass bot stuff
            headers = {'User-Agent': user_agent}

            request = urllib.request.Request(self.baseUrl, data=None, headers=headers, unverifiable=False, method='GET')
            response = urllib.request.urlopen(request)

            if response.getheader('Content-Type').lower().startswith('text/html'):
                htmlBytes = response.read()
                htmlString = htmlBytes.decode("utf-8")
                self.isRedditMasked = False
                self.feed(htmlString)
                return htmlString.lower(), self.links, self.isRedditMasked
            else:
                return "", [], False
        except Exception as e:
            print(e)
            return "", [], False
    isRedditMasked = False

def spider(urls, terms, blacklist, maxPages):
    parser = LinkParser()
    pagesToVisit = urls[:]
    searchTerms = terms[:]
    numberVisited = 0

    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited + 1

        #Get First Page
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        with open("runlist.txt", "w") as save:
            for pageToVisit in pagesToVisit:
                print(pageToVisit, file=save)

        print(numberVisited, ": ", url)
        data, links, isRedditMasked = parser.getLinks(url)

        if isRedditMasked:
            print("- SKIPPED - ...Is actually reddit masked")
            continue

        #Find Page Worth
        relevance = 0
        for term in searchTerms:
            term[2] = len(re.findall(term[0], data))  # occurances
            term[3] = term[1] * term[2]  # value
            relevance += term[3]

        #Remove Blacklisted Domains
        relevant = False
        if relevance > 700:
            for link in links:
                avoid = False
                for aTerm in blacklist:
                    if aTerm in link:
                        avoid = True
                        break
                if not avoid:
                    if link not in pagesToVisit:
                        pagesToVisit.append(link)
            relevant = True

        if relevant:
            print("- GOOD - Relevant: ", relevance)
            if relevance > 900:
                with open("site.txt", "a") as text:
                    print("\"{0}\",{1}".format(url, relevance), file=text)
        else:
            print("Page SKIPPED - Not Relevant: ", relevance)
