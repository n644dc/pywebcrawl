import crawler



#word, weight, occurance, value
terms = [['north', 5, 0, 0], ['pyongyang', 12, 0, 0], ['korea', 9, 0, 0], ['china', 5, 0, 0], ['navy', 3, 0, 0], ['nuke', 4, 0, 0], ['kim', 7, 0, 0]]
blacklist = ['reddit.com', 'javascript:',
             'redditgifts.com', 'zendesk.com',
             'apple.com', 'facebook.com',
             'pinterest.com', 'zerohedge.com',
             'lendingtree.com', 'twitter.com',
             'wikileaks.org', 'bleacherreport.com',
             'linkedin.com', 'youtube.com',
             'vox.com', 'independent.co.uk',
             't.co', 'archive.is']


urls = ['https://www.reddit.com/r/worldnews']
try:
    with open("runlist.txt") as f:
        content = f.readlines()
    urls = [x.strip() for x in content]
except Exception as e:
    print(e)



crawler.spider(urls, terms, blacklist, 10000)
