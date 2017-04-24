import os
import feedparser
from cloudant.client import Cloudant
from cloudant.document import Document
from urllib.request import urlopen
from bs4 import BeautifulSoup

#
# read rss
#
url = "https://news.yahoo.co.jp/pickup/rss.xml"

response = feedparser.parse(url)
for entry in response.entries:
    id = entry.id
    title = entry.title
    link  = entry.link
    updated = entry.updated
    print (id,title,link,updated)

#
# connect Cloudant
#
userName = os.environ["NEWSFEEDDB_USERNAME"]
password = os.environ["NEWSFEEDDB_PASSWORD"]
account = os.environ["NEWSFEEDDB_ACCOUNT"]
client = Cloudant(userName, password, account=account, connect=True,auto_renew=True)
session = client.session()
print('Username: {0}'.format(session['userCtx']['name']))
print('Databases: {0}'.format(client.all_dbs()))

my_database = client['newsfeeds']

#Delete All Documents
for document in my_database:
    document.delete()

#Create Document
#for entry in response.entries:
#    my_document = my_database.create_document(entry)
for entry in response.entries:
    with Document(my_database, entry.id) as document:
        document['title'] = entry.title
        document['link'] = entry.link
        document['updated'] = entry.updated

#Get All Documents
for document in my_database:
    print (document)

#HTML Parser
for document in my_database:
    f = urlopen(document['link'])
    soup = BeautifulSoup(f, 'lxml')
    print(soup.title)
    print(soup.title.string)

client.disconnect()
