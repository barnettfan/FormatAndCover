class GlobalData:
    # BaseUrl = 'https://www.seejav.cloud'
    BaseUrl = 'https://www.javbus.com'
    Proxy = '127.0.0.1:10809'

    def get_proxy():
        proxies={
            'http':'http://'+ GlobalData.Proxy,
            'https':'http://'+ GlobalData.Proxy
        }
        return proxies
