
# pywebcrawl
Crawls the web looking for provided content. Assigns pages thresholds for recording or throwing away the page. 


## Add terms and words that are used calculate a pages relevance to a certain topic
# word, weight, occurance, value
terms = [['north', 5, 0, 0], ['pyongyang', 12, 0, 0], ['korea', 9, 0, 0], ['china', 5, 0, 0], ['navy', 3, 0, 0], ['nuke', 4, 0, 0], ['kim', 7, 0, 0]]


## Blacklist pesky sites that have a bunch of irrelevant content or contain gross amounts of meta-data
blacklist = ['reddit.com', 'javascript:',

             'redditgifts.com', 'zendesk.com',

             'apple.com', 'facebook.com',

             'pinterest.com', 'zerohedge.com',

             'lendingtree.com', 'twitter.com',

             'wikileaks.org', 'bleacherreport.com',

             'linkedin.com', 'youtube.com',

             'vox.com', 'independent.co.uk',

             't.co', 'archive.is']




## Seed your search with a few sites. You can also provide a list of sites in a text file. 
urls = ['https://www.reddit.com/r/worldnews']
