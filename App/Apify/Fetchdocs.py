from apify_client import ApifyClient
from io import BytesIO
import os
from apify_client.consts import ActorJobStatus
from newspaper import Article
from bs4 import BeautifulSoup
from readability.readability import Document as Paper
import pandas
import re
import pytz
import datetime
import requests
import platform
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from .FetchImages import FetchImages



apify_client = ApifyClient('apify_api_u7SvWyXqqq4ettHS6miRCaEg4GbSrI00wSp5')
done = {}
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class FetchDocuments():
    
    
    def __init__(self,learn,layman):
        self.learn = learn
        self.layman = layman
        
        
    def Learnspliting(self,Splitstr):
        learn_split = Splitstr.lower().split()
        return learn_split
    
    def learn_outcome_gen(self):
        if self.layman == 'yes':
            learn_layman =self.learn+ ' in layman terms.'
            #print(learn_layman)
            learn_split = self.Learnspliting(learn_layman)
            #print(learn_split)
            learn_join = '+'.join(learn_split)
            learn_out= self.learn + r" \nhttps://www.google.com/search?q="+ learn_join
            return learn_out
        elif self.layman == 'no':
            learn_split = self.Learnspliting(self.learn)
            learn_join = '+'.join(learn_split)
            learn_out= self.learn + r" \nhttps://www.google.com/search?q="+ learn_join
            return learn_out
        else:
            return None
        
    
    def GetLinks(self):
        learn_out = self.learn_outcome_gen()
        sss = {
        "queries": learn_out,
        "resultsPerPage": 100,
        "maxPagesPerQuery": 7,
        "mobileResults": False,
        "csvFriendlyOutput": False,
        "saveHtml": False,
        "saveHtmlToKeyValueStore": False,
        "includeUnfilteredResults": False,
        "customDataFunction": "async ({ input, $, request, response, html }) => {\n  return {\n    pageTitle: $('name').text(),\n  };\n};"
        }
    
        actor_call = apify_client.actor('apify/google-search-scraper').call(run_input = sss)
        urls=[]
        titles = []
        descriptions = []
        for item in apify_client.dataset(actor_call['defaultDatasetId']).iterate_items():
        #     print(item)
            dict_org_result = ((item.get('organicResults', {})))
        #     print(dict_org_result)
            for item in dict_org_result:
                url = item.get('url', {})
                urls.append(url)
                title = item.get('title', {})
                titles.append(title)
                description = item.get('description', {})
                descriptions.append(description)
                
        link = urls[:7]
        return link
    
    
    def textgetter(self,url):
        global done
        TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'li']

        # regex for url check
        s = re.compile('(http://|https://)([A-Za-z0-9_\.-]+)')
        u = re.compile("(http://|https://)(www.)?(.*)(\.[A-Za-z0-9]{1,4})$")
        if s.search(url):
            site = u.search(s.search(url).group()).group(3)
        else:
            site = None
        answer = {}
        # check that its an url
        if s.search(url):
            if url in done.keys():
                yield done[url]
                pass
            try:
                # make a request to the url
                r = requests.get(url, verify=False, timeout=1)
                if r.status_code != 200:
                    done[url] = "Unable to reach website."
                    answer['author'] = None
                    answer['base'] = s.search(url).group()
                    answer['provider']=site
                    answer['published_date']=None
                    answer['text'] = "Unable to reach website."
                    answer['title'] = None
                    answer['top_image'] = None
                    answer['url'] = url
                    answer['keywords']=None
                    answer['summary']=None
                if len(r.content)>500:
                    # set article url
                    article = Article(url)
                    # test for python version because of html different parameters
                    if int(platform.python_version_tuple()[0])==3:
                        article.download(input_html=r.content)
                    elif int(platform.python_version_tuple()[0])==2:
                        article.download(html=r.content)
                    # parse the url
                    article.parse()
                    article.nlp()
                    # if parse doesn't pull text fill the rest of the data
                    if len(article.text) >= 200:
                        answer['author'] = ", ".join(article.authors)
                        answer['base'] = s.search(url).group()
                        answer['provider']=site
                        answer['published_date'] = article.publish_date
                        answer['keywords']=article.keywords
                        answer['summary']=article.summary
                        # convert the data to isoformat; exception for naive date
                        if isinstance(article.publish_date,datetime.datetime):
                            try:
                                answer['published_date']=article.publish_date.astimezone(pytz.utc).isoformat()
                            except:
                                answer['published_date']=article.publish_date.isoformat()
                        

                        answer['text'] = article.text
                        answer['title'] = article.title
                        answer['top_image'] = article.top_image
                        answer['url'] = url
                        
                        

                        # if previous didn't work, try another library
                    else:
                        doc = Paper(r.content)
                        data = doc.summary()
                        title = doc.title()
                        soup = BeautifulSoup(data, 'lxml')
                        newstext = " ".join([l.text for l in soup.find_all(TAGS)])

                        # as we did above, pull text if it's greater than 200 length
                        if len(newstext) > 200:
                            answer['author'] = None
                            answer['base'] = s.search(url).group()
                            answer['provider']=site
                            answer['published_date']=None
                            answer['text'] = newstext
                            answer['title'] = title
                            answer['top_image'] = None
                            answer['url'] = url
                            answer['keywords']=None
                            answer['summary']=None
                        # if nothing works above, use beautiful soup
                        else:
                            newstext = " ".join([
                                l.text
                                for l in soup.find_all(
                                    'div', class_='field-item even')
                            ])
                            done[url] = newstext
                            answer['author'] = None
                            answer['base'] = s.search(url).group()
                            answer['provider']=site
                            answer['published_date']=None
                            answer['text'] = newstext
                            answer['title'] = title
                            answer['top_image'] = None
                            answer['url'] = url
                            answer['keywords']=None
                            answer['summary']=None
                    # if nothing works, fill with empty values
                else:
                    answer['author'] = None
                    answer['base'] = s.search(url).group()
                    answer['provider']=site
                    answer['published_date']=None
                    answer['text'] = 'No text returned'
                    answer['title'] = None
                    answer['top_image'] = None
                    answer['url'] = url
                    answer['keywords']=None
                    answer['summary']=None
                    yield answer
                yield answer
                    
                
            except:
                # if the url does not return data, set to empty values
                done[url] = "Unable to reach website."
                answer['author'] = None
                answer['base'] = s.search(url).group()
                answer['provider']=site
                answer['published_date']=None
                answer['text'] = "Unable to reach website."
                answer['title'] = None
                answer['top_image'] = None
                answer['url'] = url
                answer['keywords']=None
                answer['summary']=None
                yield answer
        else:
            answer['author'] = None
            answer['base'] = s.search(url).group()
            answer['provider']=site
            answer['published_date']=None
            answer['text'] = 'This is not a proper url'
            answer['title'] = None
            answer['top_image'] = None
            answer['url'] = url
            answer['keywords']=None
            answer['summary']=None
            yield answer
        
        
            
    def Feteched_Data(self):
        Items = []
        links = self.GetLinks()
        for i in links:
            l = list(self.textgetter(i))
            Items.append(l)
        
        for item in l:
            dict_org_result = ((item.get('text', {})))
            dict_title = ((item.get('title', {})))
            print(dict_org_result)
            print(dict_title)
            return dict_org_result, dict_title
        
        
    def GetCleanedFetchedData(self):
        dict_org_result,title = self.Feteched_Data()
        result = dict_org_result.splitlines()
        result = [i for i in result if i]
        results = str(result).split("',")
        #import time
        desc = []
        for r in results:
#           time.sleep(2)
            desc.append(r)
        
        Images = FetchImages(quary=self.learn)
        ListofLinks = Images.Downlaod_Images()
        return desc, title , ListofLinks
        
                    
                
            
