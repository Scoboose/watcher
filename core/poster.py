from HTMLParser import HTMLParser
import urllib2, os, shutil

import logging
logging = logging.getLogger(__name__)



class Poster():

    def __init__(self):
        self.poster_folder = 'static/images/posters/'

    def save_poster(self, imdbid, poster_url):

        logging.info('Grabbing poster for {}.'.format(imdbid))

        new_poster_path = '{}{}.jpg'.format(self.poster_folder, imdbid)

        if os.path.exists(new_poster_path) ==  False:
            logging.info('Saving poster to {}'.format(new_poster_path))

            if poster_url == 'images/missing_poster.jpg':
                shutil.copy2(poster_url, new_poster_path)

            else:
                request = urllib2.Request( poster_url, headers={'User-Agent' : 'Mozilla/5.0'} )
                try:
                    result = urllib2.urlopen( request ).read()
                except (SystemExit, KeyboardInterrupt):
                    raise
                except Exception, e:
                    logging.error('Poster save_poster get', exc_info=True)

                try:
                    with open(new_poster_path, 'wb') as output:
                        output.write(result)
                except (SystemExit, KeyboardInterrupt):
                    raise
                except Exception, e:
                    logging.error('Poster save_poster write', exc_info=True)

            logging.info('Poster saved to {}'.format(new_poster_path))
        else:
            logging.info('{} already exists.'.format(new_poster_path))

    def remove_poster(self, imdbid):
        logging.info('Removing poster for {}'.format(imdbid))
        path = '{}{}.jpg'.format(self.poster_folder, imdbid)
        if os.path.exists(path):
            os.remove(path)
        else:
            logging.info('{} doesn\'t seem to exist.'.format(path))

    # vestigial method to parse yahoo results for a poster. I'll keep it just in case
    def find_poster(self, search_term):
        lParser = parseImages()

        search_term = search_term.replace(" ","+")
        search_string = "https://images.search.yahoo.com/search/images?p={}{}".format(search_term, "+poster")

        request = urllib2.Request( search_string, headers={'User-Agent' : 'Mozilla/5.0'} )

        html = urllib2.urlopen(request)

        lParser.feed(html.read().decode('utf-8'))
        lParser.close()

        return lParser.imgs[1]


class parseImages(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs = dict(attrs)
            if 'class' in attrs:
                if 'process' in attrs['class']:
                    self.imgs.append(attrs['data-src'])

    def feed(self, data):
        self.imgs = []
        HTMLParser.feed(self, data)
