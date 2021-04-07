import random
import requests

class Fun_Class():
    
    def gif_api(self, search):
        apikey = "LIVDSRZULELA"  # test value
        lmt = 20

        # our test search
        search_term = search
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
        d = r.json()

        g = []

        for t in d['results']:
            for gt in t['media']:
                g.append(gt['gif']['url'])
        
        return random.choice(g)