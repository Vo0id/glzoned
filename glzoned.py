#!/usr/bin python3

import re
import sys
import click
import requests as req
from bs4 import BeautifulSoup as bs
import concurrent.futures

mirror_id = []

@click.command()
@click.argument('attacker_id')
@click.option('-p', '--pages', help='How Many Pages', default=1)
@click.option('-t', '--threads', help='How Many Executions At Once', default=15)

def main(attacker_id, pages, threads):
    for i in range(1, pages+1):
        url = f'https://zone-d.org/attacker/id/{attacker_id}/{i}'
        r = req.get(url)
        soup = bs(r.text, 'html.parser')

        def load_a(link):
            href = re.findall(r'https://zone-d.org/mirror/id/\w+', link['href'])
            return href
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as e:
            futures = {e.submit(load_a, a): a for a in soup.find_all('a')}
            for future in concurrent.futures.as_completed(futures):
                for r_link in future.result():
                    mirror_id.append(r_link)

    def load_s(j):
        r = req.get(j)
        soup = bs(r.text, 'html.parser')

        for strong in soup.find('strong'):
            return strong

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as e:
        futures = {e.submit(load_s, j): j for j in mirror_id}
        for future in concurrent.futures.as_completed(futures):
            r_result = re.findall('http[s]?://.*?/', future.result())[0]
            print(r_result)
            f = open('link_result', 'a')
            f.write(f'{r_result}\n')
            f.close()


if __name__ == '__main__':
    main()
