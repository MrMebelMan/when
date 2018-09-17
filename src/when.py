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
    'ETH': ('ethereum', 'vitalik'),
    'DOGE': ('dogecoin', 'shibe', ),
    'LSK': ('lisk', ),
    'XTZ': ('tezos', ),
    'XRP': ('ripple', 'cripple' ),
    'IOTA': ('miota', 'idiota' ),
    'USDT': ('tether', ),
    'ADA': ('cardano', ),
    'TRX': ('tron', ),
    'ETC': ('ethereum classic', ),
    'BNB': ('binance', 'binance coin'),
    'VET': ('vechain mainnet', 'mainnet vechain'),
    'VEN': ('vechain'),
    'BTG': ('bitcoin gold', ),
    'BTS': ('bitshares', ),
    'XVG': ('verge', ),
}


def get_coin_name(string):
    coin_info = string.split(':')

    while True:
        try:
            magic = int(coin_info[-1])
        except ValueError:
            break

        if magic >= 0 and magic <= 2:
            del coin_info[-1]
        else:
            break

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


def check_firmware_support(coin, support_data, model='1') -> (str, bool):
    coin = coin.upper()
    for supported_coin in support_data['t' + model + '_supported']:
        coin_name = get_coin_name(supported_coin)
        if coin_name == coin:
            return (supported_coin, True)

    for supported_coin in support_data['t' + model + '_unsupported']:
        coin_name = get_coin_name(supported_coin)
        if coin_name == coin:
            return (supported_coin, False)

    return (None, False)


def parse_support_data(coin, support_data, model):
    supported_coin, supported = check_firmware_support(coin, support_data, model)

    if supported:
        support_info = support_data['t' + model + '_supported'][supported_coin]
        if support_info == 'soon':
            return 'Trezor %s: soon(TM)' % model.upper()
        else:
            return 'Trezor %s: supported since v%s.' % (model.upper(), support_info)
    else:
        if not supported_coin:
            return 'Trezor %s: not supported. No ETA.' % model.upper()
        reason = support_data['t' + model + '_unsupported'][supported_coin]
        return 'Trezor %s: not supported. Reason: %s.' % (model.upper(), reason.replace('(AUTO) ', ''))


def get_info(coin, support_data, webwallet_support):
    ret = ''

    for key, aliases in coin_aliases.items():
        if coin.lower() in aliases:
            coin = key
            break

    if coin.upper() in webwallet_support:
        ret = 'Already supported by Wallet.'
    else:
        ret += parse_support_data(coin, support_data, model='1') + '\n'
        ret += parse_support_data(coin, support_data, model='t')

    return ret
    

if __name__ == '__main__':
    support_json = get_support_json()

    webwallet_support_json = support_json['webwallet']['supported']
    support_data = {
        't1_supported':   support_json['trezor1']['supported'],
        't1_unsupported': support_json['trezor1']['unsupported'],
        'tt_supported':   support_json['trezor2']['supported'],
        'tt_unsupported': support_json['trezor2']['unsupported'],
    }

    webwallet_support = set([get_coin_name(coin.upper()) for coin, supported in webwallet_support_json.items() if supported])
    webwallet_support.add('ETH')

    if len(argv) >= 2:
        if argv[1] == 'lambo' or argv[1] == 'moon':
            print('soon(TM)')
        else:
            for strip in ['token', 'coin']:
                if strip.lower() in argv:
                    argv.remove(strip)

            print(get_info(' '.join(argv[1:]), support_data, webwallet_support))
    else:
        print('Usage: when coin_name')

