import requests
import re
import time
import logging
import datetime
from bs4 import BeautifulSoup

def fb_login(session, base_url, credentials):
    """
    Returns a Session object logged in with credentials.
    """
    login_form_url = '/login/device-based/regular/login/?refsrc=https%3A'\
        '%2F%2Fmobile.facebook.com%2Flogin%2Fdevice-based%2Fedit-user%2F&lwv=100'
    params = {'email':credentials['email'], 'pass':credentials['pass']}
    while True:
        time.sleep(3)
        logged_request = session.post(base_url+login_form_url, data=params)
        if logged_request.ok:
            logging.info('[*] Logged in.')
            break

def get_bs(session, url):
    """
    Makes a GET requests using the given Session object
    and returns a BeautifulSoup object.
    """
    r = None
    while True:
        r = session.get(url)
        time.sleep(3)
        if r.ok:
            break
    return BeautifulSoup(r.text, 'lxml')

def extract_comments(session, post_bs, post_url):
    """
    Extracts all coments from post
    """
    comments = list()
    show_more_url = post_bs.find('a', href=re.compile('/story\.php\?story'))['href']
    first_comment_page = True
##    logging.info('Scraping comments from {}.format(post_url))
    while True:
##        logging.info('[!] Scraping comments.')
        time.sleep(3)
        if first_comment_page:
            first_comment_page = False
        else:
            post_bs = get_bs(session, base_url+show_more_url)
            time.sleep(3)
        try:
            comments_elements = post_bs.find('div', id=re.compile('composer')).next_sibling\
                .find_all('div', id=re.compile('^\d+'))
        except Exception:
            pass
        if len(comments_elements) != 0:
            logging.info('[!] There are comments.')
        else:
            break
        for comment in comments_elements:
            comment_data = OrderedDict()
            comment_data['text'] = list()
            try:
                comment_strings = comment.find('h3').next_sibling.strings
                for string in comment_strings:
                    comment_data['text'].append(string)
            except Exception:
                pass
            try:
                media = comment.find('h3').next_sibling.next_sibling.children
                if media is not None:
                    for element in media:
                        comment_data['media_url'] = element['src']
                else:
                    comment_data['media_url'] = ''
            except Exception:
                pass
            comment_data['profile_name'] = comment.find('h3').a.string
            comment_data['profile_url'] = comment.find('h3').a['href'].split('?')[0]
            comments.append(dict(comment_data))
        show_more_url = post_bs.find('a', href=re.compile('/story\.php\?story'))
        if 'View more' in show_more_url.text:
            logging.info('[!] More comments.')
            show_more_url = show_more_url['href']
        else:
            break
    print(comments)
    return comments

def date_processor(post_raw_date):
    if '昨天' in post_raw_date:
        return datetime.date.today() - datetime.timedelta(days=1)
    elif '小時' in post_raw_date or '分鐘' in post_raw_date or '剛剛' in post_raw_date:
        return datetime.date.today()
    else:
        year = re.search('[0-9]{4}年')
        if year:
            year = year(0)[:-1]
        else:
            year = datetime.date.today().year
        month = re.search('[0-9]{1,2}月')
        month = month(0)[:-1]
        day = re.search('[0-9]{1,2}日')
        day = day(0)[:-1]
        return datetime.date(year, month, day)

def scrape_post(session, post_url):
    """
    Goes to post URL and extracts post data.
    """
    logging.info('Scraping the post at {}'.format(post_url))
    post_data = {}
    post_bs = get_bs(session, post_url)
    time.sleep(3)
    post_data['url'] = post_url
    try:
        post_raw_date = post_bs.find('abbr').contents[0]
        post_date = date_processor(post_raw_date)
        post_data['date'] = post_date
    except Exception:
        post_data['date'] = None
        print('Can\'t find date')
    try:
        post_data['comments'] = extract_comments(session, post_bs, post_url)
    except Exception:
        post_data['comments'] = None
    return post_data

def crawl_profile(session, base_url, profile_url):
    """
    Goes to profile URL, crawls it and extracts posts URLs.
    """
    story_url = base_url + '/story.php?story_'
    scraped_posts = [profile_url]
    print('')
    logging.info('Scraping the profile at {}'.format(profile_url))
    profile_bs = get_bs(session, profile_url)
    time.sleep(3)
    recents = profile_bs.find('div', id='recent')
    posts = recents.find('div').find('div').find_all('div', recursive=False)
    page_id = eval(posts[0]['data-ft'])['page_id']
    posts_ids = [eval(post['data-ft'])['top_level_post_id'] for post in posts]
    posts_urls = [story_url + 'fbid={}&id={}'.format(post_id, page_id) for post_id in posts_ids]
    print(posts_urls)
    for post_url in posts_urls:
        try:
            post_data = scrape_post(session, post_url)
            scraped_posts.append(post_data)
        except Exception as e:
            logging.info('Error: {}'.format(e))
    return scraped_posts

def save_data(data):
    """
    Writes data to txt.
    """
    with open('fb_data.txt', 'w') as output:
        for profile in data:
            output.write("{} posts where scraped from the profile at {}\n".format(len(profile)-1, profile[0]))
            for posts in profile[1:]:
                output.write("\n")
                for field in posts:
                    output.write("    {}: {}\n".format(field, posts[field]))
            output.write("\n")

def main():    
    logging.basicConfig(level=logging.INFO)
    base_url = 'https://mobile.facebook.com'
    session = requests.session()
    credentials = {
        "email":"**********",
        "pass":"**********",
        }
    profiles_urls = [
        "https://mobile.facebook.com/AAStocks.com.Limited/",
        "https://mobile.facebook.com/80shing/",
        ]
    fb_login(session, base_url, credentials)
    posts_data = []
    for profile_url in profiles_urls:
        posts_data.append(crawl_profile(session, base_url, profile_url))
        logging.info('[!] Finished scraping {}. Number of scraped posts: {}'.format(profile_url, len(posts_data)))
    print('')
    logging.info('[!] Saving.')
    save_data(posts_data)
    logging.info('[!] Done.')
    return(posts_data)

if __name__ == '__main__':
    main()
