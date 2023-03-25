import requests , json , socket , sys, os

domain = sys.argv[1]
resp = requests.get('https://crt.sh/?q={}&output=json'.format(domain))
subdomains = []

for sub in resp.json():
        if sub['common_name'] in subdomains or domain not in sub['common_name']:
                continue
        subdomains.append(sub['common_name'])

with os.popen('subfinder -d {} -silent'.format(domain)) as f:
    output = f.read().strip().split('\n')
    subdomains.extend(output)

subdomains = list(set(subdomains))
print("{} subdomains found".format(len(subdomains)))

with open(domain + "-subdomains", 'w+') as f:
        json.dump(subdomains, f)

domainips = []
iplist = []

for subdomain in subdomains:
        try:
                domainip = socket.gethostbyname(subdomain)
                print('{} subdomain on ip {} '.format(subdomain, domainip))
                if domainip in iplist:
                    domainips.append(dict(subdomain = subdomain , ip = domainip, ports = [0] ))
                else:
                    iplist.append(domainip)
                    start_port = 0
                    end_port = 1000
                    open_ports = []
                    for port in range(start_port, end_port+1):
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        result = sock.connect_ex((domainip, port))
                        if result == 0:
                            print("{} subdomain has ip {} with port {} open".format(subdomain, domainip, port))
                            open_ports.append(port)
                        sock.close()
                    domainips.append(dict(subdomain = subdomain , ip = domainip, ports = open_ports ))
        except:
                print('{} subdomain not live '.format(subdomain))
                continue

with open(domain + "-subdomains-ips", 'w+') as f:
        json.dump(domainips, f)

for index, subdomain in enumerate(domainips):
    if subdomain["ports"][0] == 0:
        continue
    ports = ','.join([str(number) for number in subdomain["ports"]])
    print(ports)
    host = subdomain["subdomain"]
    with os.popen('httpx -u {} -ports {} -silent'.format(host, ports)) as f:
        output = f.read().strip().split('\n')
        domainips[index]["http"] = output

with open(domain + "-subdomains-ips-http-ports", 'w+') as f:
        json.dump(domainips, f)
