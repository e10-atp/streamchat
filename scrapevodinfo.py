from requests_html import HTMLSession
import os
import time


def read_urls():
    # urls should be in a format such as: https://www.twitch.tv/videos/582450357
    urls = list()
    relpath = os.path.dirname(__file__)
    filename = os.path.join(relpath, 'data', 'urls.txt')
    with open(filename, 'r') as f:
        for line in f:
            if line == '\n':
                continue
            urls.append(line.strip())
    return urls


def scrape_urls(urls):
    relpath = os.path.dirname(__file__)
    outname = os.path.join(relpath, 'data/vodinfos.csv')
    with open(outname, 'w+') as outfile:
        outfile.write('vodID,Streamer,Category,Views,Length\n')  # header
        for link in urls:
            session = HTMLSession()
            jpage = session.get(link)
            jpage.html.render()

            vodid = link.split('/')[-1]
            info = jpage.html.text
            finfo = info.split('\n')
            streamer = finfo[0].split(' ', 1)[0]
            cat, views, length = None, None, None
            for i, line in enumerate(finfo):
                if line.startswith('Category'):
                    cat = finfo[i + 1]
                elif line.startswith('Total Views'):
                    views = finfo[i - 1].replace(',', '')
                elif line.startswith('00:00:00'):
                    length = finfo[i + 1]
                if cat is not None and views is not None and length is not None:
                    break

            output = f'{vodid},{streamer},{cat},{views},{length}\n'
            print(output)
            outfile.write(output)
            session.close()
            time.sleep(10)  # prevents rate limit


if __name__ == '__main__':
    urls = read_urls()
    scrape_urls(urls)
