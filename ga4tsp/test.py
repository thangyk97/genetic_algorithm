import numpy as np
import itertools


distances = np.array(     [[ 0,  4, 13, 15, 24,  4, 31, 18,  6, 21],
                           [ 4,  0,  8, 33,  9, 61,  7, 61,  7, 31],
                           [13,  8,  0, 22,  6, 33,  2, 33, 19, 41],
                           [15, 33, 22,  0,  3,  5, 62,  9, 41,  5],
                           [24,  9,  6,  3,  0, 18, 12,  4, 17,  9],
                           [ 4, 61, 33,  5, 18,  0,  1, 35,  9, 17],
                           [31,  7,  2, 62, 12,  1,  0, 19, 91,  8],
                           [18, 61, 33,  9,  4, 35, 19,  0, 77,  7],
                           [ 6,  7, 19, 41, 17,  9, 91, 77,  0, 11],
                           [21, 31, 41,  5,  9, 17,  8,  7, 11,  0]])

def cal_distance(routes):
    distance = 0
    for i in range(len(routes[:-1])):
        distance += distances[routes[i], routes[i+1]]
    return distance


a = list(range(distances.shape[0]))
list_routes = list(itertools.permutations(a[1:]))


min_distance = float('inf')
min_routes = []
for r in list_routes:
    r = (0,) + r + (0,)
    d = cal_distance(r)
    if d < min_distance:
        min_distance = d
        min_routes = r

print("min distance : ", min_distance)
print('route: ', min_routes)


























import scrapy
from scrapy.crawler import CrawlerProcess
import numpy as np 
from scipy.sparse import csc_matrix

# create list contain dicts {url_web_wiki: list_url}
wiki_pages = []
node = 1

class TestSpider(scrapy.Spider):
    name = 'test'
    start_urls = [
         'https://en.wikipedia.org/wiki/Information_system'
    ]
    
    def parse(self, response):
        global wiki_pages
        global node
        yield {
            'url': response.request.url, 
            'title': response.xpath("//title/text()").extract_first()
        }

        list_page = response.xpath("//a[starts-with(@href,'/wiki') and not(contains(@href,':'))]/@href").extract()
        dict = {response.request.url: list_page}
        wiki_pages.append(dict)
        # for link in list_page:
        #     if (link.startswith('/wiki/')):
        #         print("https://en.wikipedia.org" + link)
        #         nodes = nodes + 1
        if (list_page is not None) and node < 500:
            node = node + len(list_page)
            for next_page in list_page:
                yield response.follow(next_page, callback=self.parse)

def pageRank(G, s = .85, maxerr = .0001):
    """
    Computes the pagerank for each of the n states
    Parameters
    ----------
    G: matrix representing state transitions
       Gij is a binary value representing a transition from state i to j.
    s: probability of following a transition. 1-s probability of teleporting
       to another state.
    maxerr: if the sum of pageranks between iterations is bellow this we will
            have converged.
    """
    n = G.shape[0]

    # transform G into markov matrix A
    A = csc_matrix(G,dtype=np.float)
    rsums = np.array(A.sum(1))[:,0]
    ri, ci = A.nonzero()
    A.data /= rsums[ri]

    # bool array of sink states
    sink = rsums==0

    # Compute pagerank r until we converge
    ro, r = np.zeros(n), np.ones(n)
    while np.sum(np.abs(r-ro)) > maxerr:
        ro = r.copy()
        # calculate each pagerank at a time
        for i in range(n):
            # inlinks of state i
            Ai = np.array(A[:,i].todense())[:,0]
            # account for sink states
            Di = sink / float(n)
            # account for teleportation to state i
            Ei = np.ones(n) / float(n)

            r[i] = ro.dot( Ai*s + Di*s + Ei*(1-s) )

    # return normalized pagerank
    return r/float(sum(r))
def gen_matrix(list_dict):
    #print("wiki page ", len(list_dict))
    nodes = []
    seen = set()
    for ddic in list_dict:
        r_url = list(ddic.keys())[0]
        l_url = ddic.values()
        if r_url not in seen:
            seen.add(r_url)
            nodes.append(r_url)
        # for url in l_url:
        #     if url not in seen:
        #         seen.add(url)
        #         nodes.append(url)
    n = len(nodes)
    matrix = []
    # Create matix W
    # 1: visible
    # 0: invisible
    for i in range(n):
        # create list for node[i]
        val_link = []
        list_link = list(list_dict[i].values())
        for j in range(n):
            tmp = list(list_dict[j].keys())[0].replace("https://en.wikipedia.org","")
            if (tmp in list_link):
                val_link.append(1)
            else:
                val_link.append(0)
        matrix.append(val_link)
    matrix = np.array(matrix)
    print(matrix[1:10])
    return matrix

if _name_ == "_main_":
    # os.remove('result.json')
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })

    process.crawl(TestSpider)
    process.start()
    # Print list contain dicts 
    print(type(wiki_pages))
    print(pageRank(gen_matrix(wiki_pages)))