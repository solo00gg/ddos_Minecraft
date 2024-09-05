import json
import datetime
import requests
import re
import sys
from concurrent.futures import ThreadPoolExecutor

class DownloadProxies:
    def __init__(self) -> None:
        self.api = {
           'socks4':[
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",
                "https://www.proxy-list.download/api/v1/get?type=socks4",
                "https://www.proxyscan.io/download?type=socks4",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
                "https://api.openproxylist.xyz/socks4.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
                "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
                'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt',
                'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt',
                'https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt',
                'https://proxylist.live/nodes/socks4_1.php?page=1&showall=1',
                'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt',
                'https://openproxy.space/list/socks4',
                'https://github.com/hanwayTech/free-proxy-list/blob/main/socks4.txt',
                'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt',
                'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/socks4.txt',
                'https://proxyspace.pro/socks4.txt',
                'https://raw.githubusercontent.com/ObcbO/getproxy/master/socks4.txt',
                'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt'
            ],
            'socks5': [
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&simplified=true",
                "https://www.proxy-list.download/api/v1/get?type=socks5",
                "https://www.proxyscan.io/download?type=socks5",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
                "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
                "https://api.openproxylist.xyz/socks5.txt",
                "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
                'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt',
                'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt',
                'https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt',
                'https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt',
                'https://github.com/hanwayTech/free-proxy-list/blob/main/socks5.txt',
                'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt',
                'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt',
                'https://openproxy.space/list/socks5',
                'https://proxylist.live/nodes/socks5_1.php?page=1&showall=1',
                'https://spys.me/socks.txt',
                'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/socks5.txt',
                'https://proxyspace.pro/socks5.txt',
                'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt',
            ],
            'http': [
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
                "https://www.proxy-list.download/api/v1/get?type=http",
                'https://www.proxy-list.download/api/v1/get?type=https',
                "https://www.proxyscan.io/download?type=http",
                "https://spys.me/proxy.txt",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
                "https://api.openproxylist.xyz/http.txt",
                "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
                "http://alexa.lr2b.com/proxylist.txt",
                "http://rootjazz.com/proxies/proxies.txt",
                "http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http",
                "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
                "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
                "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
                "https://proxy-spider.com/api/proxies.example.txt",
                "https://multiproxy.org/txt_all/proxy.txt",
                "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
                "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt",
                "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/https.txt",
                'https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt',
                'https://openproxy.space/list/http',
                'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
                'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
                'https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt',
                'https://raw.githubusercontent.com/almroot/proxylist/master/list.txt',
                'https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt',
                'https://raw.githubusercontent.com/saisuiu/uiu/main/free.txt',
                'https://proxylist.live/nodes/free_1.php?page=1&showall=1',
                'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/http.txt',
                'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/https.txt',
                'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt',
                'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt',
                'https://raw.githubusercontent.com/rx443/proxy-list/online/all.txt',
                'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/http.txt',
                'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/https.txt',
                'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt',
                'https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxy-list/data.txt',
                'https://raw.githubusercontent.com/andigwandi/free-proxy/main/proxy_list.txt',
                'https://raw.githubusercontent.com/ObcbO/getproxy/master/http.txt',
                'https://raw.githubusercontent.com/ObcbO/getproxy/master/https.txt',
                'https://sheesh.rip/http.txt',
                'https://proxyspace.pro/http.txt',
                'https://proxyspace.pro/https.txt',
                'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt'
            ]
        }
        self.proxy_dict = {'socks4': [], 'socks5': [], 'http': []}

    def get_special1(self):
        proxy_list = []
        try:
            r = requests.get("https://www.socks-proxy.net/", timeout=5)
            part = str(r.text)
            part = part.split("<tbody>")
            part = part[1].split("</tbody>")
            part = part[0].split("<tr><td>")
            for proxy in part:
                proxy = proxy.split("</td><td>")
                try:
                    proxy_list.append(proxy[0] + ":" + proxy[1])
                except:
                    pass
            return proxy_list
        except:
            return []

    def get_special2(self):
        for i in range(json.loads(requests.get('https://proxylist.geonode.com/api/proxy-summary').text)["summary"]['proxiesOnline'] // 100):
            proxies = json.loads(requests.get('https://proxylist.geonode.com/api/proxy-list?limit=100&page={}&sort_by=lastChecked&sort_type=desc'.format(i)).text)
            for p in proxies['data']:
                if p['protocols'][0] == 'https':
                    protocol = 'http'
                else:
                    protocol = p['protocols'][0]
                self.proxy_dict[protocol].append('{}:{}'.format(p['ip'], p['port']))
        return

    def get_proxy_from_api(self, api):
        try:
            r = requests.get(api, timeout=5)
            if r.status_code == requests.codes.ok:
                proxies = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}', r.text)
                print(f'> {len(proxies)} proxies fetched from {api}')
                return proxies
        except:
            return []
        return []

    def get(self, proxy_type):
        total_proxies = 0
        if proxy_type == 'socks4':
            special_proxies = self.get_special1()
            self.proxy_dict['socks4'] += special_proxies
            print(f'> {len(special_proxies)} proxies fetched from special source 1')
            total_proxies += len(special_proxies)
        # self.get_special2()          # Uncomment if needed

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.get_proxy_from_api, api) for api in self.api[proxy_type]]
            for future in futures:
                proxies = future.result()
                self.proxy_dict[proxy_type] += proxies
                total_proxies += len(proxies)

        self.proxy_dict[proxy_type] = list(set(self.proxy_dict[proxy_type]))
        print(f'> Get {proxy_type} proxies done. Total: {total_proxies} proxies.')

    def get_extra(self):
        for q in range(20):
            self.count = {'http': 0, 'socks5': 0}
            self.day = datetime.date.today() + datetime.timedelta(-q)
            try:
                self.r = requests.get(f'https://checkerproxy.net/api/archive/{self.day.year}-{self.day.month}-{self.day.day}', timeout=5)
                if self.r.text != '[]': 
                    self.json_result = json.loads(self.r.text)
                    for i in self.json_result:
                        if re.match(r'172\.\d{1,3}\.\d{1,3}\.\d{1,3}', i['ip']):
                            if i['type'] in [1, 2] and i['addr'] in self.proxy_dict['http']:
                                self.proxy_dict['http'].remove(i['addr'])
                            if i['type'] == 4 and i['addr'] in self.proxy_dict['socks5']:
                                self.proxy_dict['socks5'].remove(i['addr'])
                        else:
                            if i['type'] in [1, 2]:
                                self.count['http'] += 1
                                self.proxy_dict['http'].append(i['addr'])
                            if i['type'] == 4:
                                self.count['socks5'] += 1
                                self.proxy_dict['socks5'].append(i['addr'])
                    print(f'> Get {self.count["http"]} http proxy ips from {self.r.url}')
                    print(f'> Get {self.count["socks5"]} socks5 proxy ips from {self.r.url}')
            except:
                pass
        
        self.proxy_dict['socks4'] = list(set(self.proxy_dict['socks4']))
        self.proxy_dict['socks5'] = list(set(self.proxy_dict['socks5']))
        self.proxy_dict['http'] = list(set(self.proxy_dict['http']))
        
        print('> Get extra proxies done')

    def save(self, proxy_type=None, filename='proxies.txt'):
        if proxy_type:
            self.proxy_dict[proxy_type] = list(set(self.proxy_dict[proxy_type]))
            with open(filename, 'w') as f:
                for i in self.proxy_dict[proxy_type]:
                    if '#' in i or i == '\n':
                        self.proxy_dict[proxy_type].remove(i)
                    else:
                        f.write(i + '\n')
            print(f"> Have already saved {len(self.proxy_dict[proxy_type])} {proxy_type} proxies list as {filename}")
        else:
            with open(filename, 'w') as f:
                total_proxies = 0
                for proxy_type in ['http', 'socks4', 'socks5']:
                    self.proxy_dict[proxy_type] = list(set(self.proxy_dict[proxy_type]))
                    total_proxies += len(self.proxy_dict[proxy_type])
                    for i in self.proxy_dict[proxy_type]:
                        if '#' in i or i == '\n':
                            self.proxy_dict[proxy_type].remove(i)
                        else:
                            f.write(i + '\n')
                print(f"> Have already saved all proxies list as {filename}. Total: {total_proxies} proxies.")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage:")
        print("1: Download HTTP proxies")
        print("2: Download SOCKS4 proxies")
        print("3: Download SOCKS5 proxies")
        print("4: Download all types of proxies")
    elif len(sys.argv) >= 2:
        d = DownloadProxies()
        option = sys.argv[1]
        filename = 'proxies.txt' if len(sys.argv) == 2 else sys.argv[2]
        if option == '1':
            proxy_type = 'http'
            d.get(proxy_type)
            d.save(proxy_type, filename)
        elif option == '2':
            proxy_type = 'socks4'
            d.get(proxy_type)
            d.save(proxy_type, filename)
        elif option == '3':
            proxy_type = 'socks5'
            d.get(proxy_type)
            d.save(proxy_type, filename)
        elif option == '4':
            for proxy_type in ['http', 'socks4', 'socks5']:
                d.get(proxy_type)
            d.save(filename=filename)
        else:
            print("Invalid option. Please use 1 for HTTP, 2 for SOCKS4, 3 for SOCKS5, or 4 for all types.")
            sys.exit(1)