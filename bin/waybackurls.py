import requests
import sys
import json


def waybackurls(host, with_subs):
    if with_subs:
        url = f'http://web.archive.org/cdx/search/cdx?url=*.{host}/*&output=json&fl=original&collapse=urlkey'
    else:
        url = f'http://web.archive.org/cdx/search/cdx?url={host}/*&output=json&fl=original&collapse=urlkey'
    r = requests.get(url)
    results = r.json()
    return results[1:]


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2:
        print('Usage:\n\tpython3 waybackurls.py <url> <include_subdomains:optional>')
        sys.exit()

    host = sys.argv[1]
    with_subs = argc > 3
    urls = waybackurls(host, with_subs)
    json_urls = json.dumps(urls)
    if urls:
        filename = f'{host}-waybackurls.json'
        with open(filename, 'w') as f:
            f.write(json_urls)
        print(f'[*] Saved results to {filename}')
    else:
        print('[-] Found nothing')
