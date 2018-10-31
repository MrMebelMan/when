#!/usr/bin/env python3

from requests import get as requests_get
from json import loads as json_loads
from sys import argv, exit

coin_aliases = {
    'BTC': ('bitcoin', 'corn', 'beethoven', ),
    'LTC': ('chikun', 'litecoin', ),
    'XMR': ('monero', ),
    'BCH': ('bitcoin cash', 'bcash', 'bcrash', 'btrash', ),
    'ZEC': ('zcash', ),
    'ETH': ('ethereum', 'vitalik', ),
    'DOGE': ('dogecoin', 'shibe', ),
    'LSK': ('lisk', ),
    'XTZ': ('tezos', ),
    'XRP': ('ripple', 'cripple', ),
    'IOTA': ('miota', 'idiota', ),
    'USDT': ('tether', ),
    'ADA': ('cardano', ),
    'TRX': ('tron', ),
    'ETC': ('ethereum classic', ),
    'BNB': ('binance', 'binance coin', ),
    'VET': ('vechain mainnet', 'mainnet vechain', ),
    'VEN': ('vechain', ),
    'BTG': ('bitcoin gold', ),
    'BTS': ('bitshares', ),
    'XVG': ('verge', ),
    'DGB': ('digibyte', ),
    'ICX': ('icon', ),
}


def get_coin_name(string):
    coin_info = string.split(':')

    try:
        int(coin_info[-1])
        del coin_info[-1]
    except ValueError:
        pass

    return coin_info[-1].split(' ')[0].upper()


def get_support_json():
    support_json_url='https://raw.githubusercontent.com/trezor/trezor-common/master/defs/support.json'

    try:
        response = requests_get(support_json_url)
    except Exception as e:
        print(e)
        exit(1)

    if response.status_code != 200:
        print("%s returned %d" % (support_json_url, response.status_code)) 
        exit(1)

    return json_loads(response.text)


def parse_support_data(coin, support_data, model):
    for supported_coin in support_data['supported']:
        if get_coin_name(supported_coin) == coin.upper():
            support_info = support_data['supported'][supported_coin]
            if support_info == 'soon':
                return 'Trezor %s: soon™' % model
            else:
                return 'Trezor %s: supported since v%s.' % (model, support_info)

    for supported_coin in support_data['unsupported']:
        if get_coin_name(supported_coin) == coin.upper():
            reason = support_data['unsupported'][supported_coin].replace('(AUTO) ', '')
            return 'Trezor %s: not supported. Reason: %s.' % (model, reason)

    return 'Trezor %s: not supported. No ETA.' % model


if __name__ == '__main__':
    support_json = get_support_json()
    webwallet_support_json = support_json['webwallet']['supported']

    webwallet_support = set([get_coin_name(coin) for coin, supported in webwallet_support_json.items() if supported])
    webwallet_support.add('ETH')

    if len(argv) >= 2:
        if argv[1] in ['lambo', 'moon']:
            print('soon™')
        else:
            for strip in ['token', 'coin']:
                if strip.lower() in argv:
                    argv.remove(strip)

            coin = ' '.join(argv[1:])
            
            for key, aliases in coin_aliases.items():
                if coin.lower() in aliases:
                    coin = key
                    break

            ret = ''
            if coin.upper() in webwallet_support:
                ret = 'Already supported by Wallet.\n'
            ret += parse_support_data(coin, support_json['trezor1'], model='1') + '\n'
            ret += parse_support_data(coin, support_json['trezor2'], model='T')
            print(ret)
    else:
        print('Usage: when coin_name')

