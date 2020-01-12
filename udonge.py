import requests 
import sys

import os.path as op
from mastodon import Mastodon

# --------------------------------------------------

def main():

    mastodon = Mastodon(
        access_token = 'token.dat',
        api_base_url = 'https://social.inex.rocks/'
    )

    URL    = "https://danbooru.donmai.us/posts.json"
    PARAMS = { 'tags': 'reisen_udongein_inaba 1girl',
               'limit': 1,
               'random': True } 

    b_success = False
    while not b_success:
        r = requests.get(url = URL, params = PARAMS) 
        data = r.json()

        fileurl = data[0]['file_url']
        print('url ', fileurl)
        fileid = data[0]['id']
        print('id ', fileid)
        filescore = data[0]['fav_count']
        print('score ', filescore)
        filesafe = data[0]['rating']
        print('rating ', filesafe)
        filetagstring = data[0]['tag_string']

        # we don't want comics and lowscored arts
        if (filesafe == 's' and filescore >= 25
            and 'comic'   not in filetagstring
            and 'unhappy' not in filetagstring
            and 'nazi' not in filetagstring
            and 'blood' not in filetagstring):
            b_success = True

    fformat = op.splitext(fileurl)[1][1:]

    print(fformat)
    if (fformat == 'jpg'):
        fformat = 'jpeg'
    media = mastodon.media_post(requests.get(fileurl).content, f'image/{fformat}')
    tags = '#touhou #reisen #udongein #reisenbot'

    toot  = f':love_reisen: {tags}\nhttps://danbooru.donmai.us/posts/{fileid}'

    # is it 's'afe, free from swimsuits and underwear tags, etc
    b_sensetive = ('underwear' in filetagstring
                    or 'large_breasts' in filetagstring
                    or 'ass' in filetagstring
                    or 'swimsuit' in filetagstring)

    mastodon.status_post(toot, media_ids=[media], visibility='unlisted', sensitive=b_sensetive)

if __name__ == '__main__':
    sys.exit(main())
