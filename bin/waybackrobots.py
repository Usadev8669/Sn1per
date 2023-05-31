import requests
import re
import sys
from multiprocessing.dummy import Pool


def robots(host):
    r = requests.get(
        'https://web.archive.org/cdx/search/cdx\
        ?url=%s/robots.txt&output=json&fl=timestamp,original&filter=statuscode:200&collapse=digest' % host)
    results = r.json()
    if len(results) == 0: # might find nothing
        return []
    results.pop(0)  # The first item is ['timestamp', 'original']
    return results


def getpaths(snapshot):
    url = 'https://web.archive.org/web/{0}/{1}'.format(snapshot[0], snapshot[1])
    robotstext = requests.get(url).text
    return re.findall('/.*', robotstext) if 'Disallow:' in robotstext else []


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage:\n\tpython3 waybackrobots.py <domain-name>')
        sys.exit()

    host = sys.argv[1]

    snapshots = robots(host)
    print(f'Found {len(snapshots)} unique results')
    if len(snapshots) == 0:
        sys.exit()
    print('This may take some time...')
    pool = Pool(4)
    paths = pool.map(getpaths, snapshots)
    unique_paths = set()
    for i in paths:
        unique_paths.update(i)
    filename = f'{host}-robots.txt'
    with open(filename, 'w') as f:
        f.write('\n'.join(unique_paths))
    print(f'[*] Saved results to {filename}')
