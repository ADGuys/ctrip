import requests


def if_proxy(proxy):
    try:
        requests.get('https://m.ctrip.com/', proxies={"https": "https://" + proxy})
    except:
        return 0

if if_proxy('125.116.24.185:43751'):
    print('asdasd')
