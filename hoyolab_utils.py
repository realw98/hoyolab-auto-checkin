import json
import logging
from json_http_request import json_http_request

def build_cookie_string(no, cookie):
    if not type(cookie) is dict:
        logging.error(f"Cookie #{no} is not valid, check config.json format")
        return None
    ltuid_v2 = cookie.get('ltuid_v2', None)
    if ltuid_v2 is None:
        logging.error(f"Cookie #{no} is not valid, ltuid_v2 not found")
        return None
    ltoken_v2 = cookie.get('ltoken_v2', None)
    if ltoken_v2 is None:
        logging.error(f"Cookie #{no} is not valid, ltoken_v2 not found")
        return None
    ltmid_v2 = cookie.get('ltmid_v2', None)
    if ltmid_v2 is None:
        logging.error(f"Cookie #{no} is not valid, ltmid_v2 not found")
        return None    
    return f"ltuid_v2={ltuid_v2}; ltoken_v2={ltoken_v2}; ltmid_v2={ltmid_v2}; account_id_v2={ltuid_v2}; account_mid_v2={ltmid_v2}; cookie_token_v2={ltoken_v2}"


def is_valid_cookie(headers):
    res = json_http_request(
        'get',
        'https://api-account-os.hoyolab.com/auth/api/getUserAccountInfoByLToken',
        headers
    )
    return res.get('retcode', 0) == 0


def get_genshin_opts():
    act_id = 'e202102251931481'
    return {
        'game': 'Genshin Impact',
        'act_id': act_id,
        'info_url': f'https://sg-hk4e-api.hoyolab.com/event/sol/info?act_id={act_id}',
        'reward_url': f'https://sg-hk4e-api.hoyolab.com/event/sol/home?act_id={act_id}',
        'sign_url': f'https://sg-hk4e-api.hoyolab.com/event/sol/sign?act_id={act_id}',
        'title': 'Genshin Impact daily login',
        'color': 'E86D82',
        'author_name': 'Paimon',
        'author_url': 'https://genshin.hoyoverse.com',
        'author_icon': 'https://fastcdn.hoyoverse.com/static-resource-v2/2023/11/08/9db76fb146f82c045bc276956f86e047_6878380451593228482.png'
    }

def get_hi3_opts():
    act_id = 'e202110291205111'
    return {
        'game': 'Honkai Impact 3rd',
        'act_id': act_id,
        'info_url': f'https://sg-public-api.hoyolab.com/event/mani/info?act_id={act_id}',
        'reward_url': f'https://sg-public-api.hoyolab.com/event/mani/home?act_id={act_id}',
        'sign_url': f'https://sg-public-api.hoyolab.com/event/mani/sign?act_id={act_id}',
        'title': 'Honkai Impact 3rd daily login',
        'color': 'A3DE85',
        'author_name': 'Ai-chan',
        'author_url' : 'https://honkaiimpact3.hoyoverse.com',
        'author_icon' : 'https://webstatic-sea.hoyolab.com/communityweb/business/bh3_hoyoverse.png',
    }

def get_hsr_opts():
    act_id = 'e202303301540311'
    return {
        'game': 'Honkai: Star Rail',
        'act_id': act_id,
        'info_url' : f'https://sg-public-api.hoyolab.com/event/luna/os/info?act_id={act_id}',
        'reward_url' : f'https://sg-public-api.hoyolab.com/event/luna/os/home?act_id={act_id}',
        'sign_url' : f'https://sg-public-api.hoyolab.com/event/luna/os/sign?act_id={act_id}',
        'title' : 'Honkai: Star Rail daily login',
        'color' : 'A385DE',
        'author_name' : 'Pom-Pom',
        'author_url' : 'https://hsr.hoyoverse.com',
        'author_icon' : 'https://webstatic-sea.hoyolab.com/communityweb/business/starrail_hoyoverse.png'
    }

def get_zzz_opts():
    act_id = 'e202406031448091'
    return {
        'game': 'Zenless Zone Zero',
        'act_id': act_id,
        'info_url' : f'https://sg-act-nap-api.hoyolab.com/event/luna/zzz/os/info?act_id={act_id}',
        'reward_url' : f'https://sg-act-nap-api.hoyolab.com/event/luna/zzz/os/home?act_id={act_id}',
        'sign_url' : f'https://sg-act-nap-api.hoyolab.com/event/luna/zzz/os/sign?act_id={act_id}',
        'title' : 'Zenless Zone Zero daily login',
        'color' : '222222',
        'author_name' : 'Eous',
        'author_url' : 'https://zenless.hoyoverse.com',
        'author_icon' : 'https://static.wikia.nocookie.net/zenless-zone-zero/images/5/51/Bangboo.png/revision/latest'
    }


def get_biz_opts(biz):
    if biz == 'hk4e_global':
        return get_genshin_opts()
    if biz == 'bh3_global':
        return get_hi3_opts()
    if biz == 'hkrpg_global':
        return get_hsr_opts()
    if biz == 'nap_global':
        return get_zzz_opts()
    return None

def get_login_info(info_url, headers):
    res = json_http_request('get', info_url, headers)
    code = res.get('retcode', 1111)
    if code != 0:
        logging.error(f"get_login_info(): {res.get('message')}")
        return None;
    data = res.get('data', None)
    return data

def get_rewards_info(reward_url, headers):
    res = json_http_request('get', reward_url, headers)
    code = res.get('retcode', 1111)
    if code != 0:
        logging.error(f"get_rewards_info(): {res.get('message')}")
        return None;
    awards = res.get('data', {}).get('awards', None)
    return awards

def claim_rewards(sign_url, act_id, headers):
    data = json.dumps({ 'act_id': act_id }, ensure_ascii=False)
    return json_http_request('post', sign_url, headers, data=data)
