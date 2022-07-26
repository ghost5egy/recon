import requests,json,socket, sys
domain = sys.argv[1]
resp = requests.get('https://crt.sh/?q={}&output=json'.format(domain))
subdomains = []
for sub in resp.json():
        if sub['common_name'] in subdomains:
                continue
        subdomains.append(sub['common_name'])
with open(domain + "-subdomains", 'w+') as f:
        json.dump(subdomains, f)
domainips = dict()
for subdomain in subdomains:
        try:
                domainip = socket.gethostbyname(subdomain)
                domainips[subdomain] = domainip
        except:
                continue
with open(domain + "-subdomains-ips", 'w+') as f:
        json.dump(domainips, f)
