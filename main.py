import json
import os
import logging
import sys
from discord import send_discord_notification
from urllib.parse import urlparse
import hoyolab_utils

if __name__ != "__main__":
    raise Exception('Run main.py as main')

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    current_dir = os.path.dirname(sys.executable)
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(os.path.join(current_dir, "hoyolab-auto-checkin.log"), encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info('Hoyolab Auto Check-in starting ...')

config = {}

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    except AttributeError:
        return False
    


def init_config():
    global config
    config_required_params = ['accounts', 'user_agent']

    try:
        with open(os.path.join(current_dir, 'config.json'), 'r') as f:
            try:
                config = json.load(f)
            except Exception as e:
                logging.error('config.json is not valid JSON')
                logging.error(e)
                exit(1)
            for param in config_required_params:
                if param not in config:
                    logging.error(f'Incomplete config,json, parameter "{param}" not found')
                    exit(1)
    except OSError as e:
        logging.error('config.json missing, follow instruction in README carefully')


def process_game(biz, opts, headers):
    result = {
        'failed': False
    }
    logging.info(f"Processing game {biz}")

    login_info = hoyolab_utils.get_login_info(opts.get('info_url'), headers)
    if login_info is None:
        result['status'] = 'Cannot get login info'
        result['failed'] = True
        return result

    total_sign_day = result['total_sign_day'] = login_info.get('total_sign_day')

    logging.info(f"Get daily login reward info for game {biz}")
    rewards = hoyolab_utils.get_rewards_info(opts.get('reward_url'), headers)

    if login_info.get('first_bind') is True:
        result['status'] = 'Please check in manually once'
        result['failed'] = True
    elif login_info.get('is_sign') is True:
        result['award_name'] = rewards[total_sign_day - 1]['name']
        result['award_cnt'] = rewards[total_sign_day - 1]['cnt']
        result['award_icon'] = rewards[total_sign_day - 1]['icon']
        result['status'] = "You've already checked in today"
    else:
        result['award_name'] = rewards[total_sign_day]['name']
        result['award_cnt'] = rewards[total_sign_day]['cnt']
        result['award_icon'] = rewards[total_sign_day]['icon']
        logging.info("Rewards available, claiming it now...")
        try:
            res = hoyolab_utils.claim_rewards(opts['sign_url'], opts['act_id'], headers)
        except Exception as e:
            result['status'] = 'Unhandled exception'
            result['failed'] = True
        code = res.get('retcode', -1)
        if code == 0:
            result['status'] = 'Daily reward claimed successfully'
            result['total_sign_day'] = result['total_sign_day'] + 1
        else:
            result['status'] = f"Something went wrong.\n {res.get('message', '')}"
            result['failed'] = True

    return result


def process_account(no, account, discord_url):

    logging.debug(f'Processing account #{no}')
    cookie_string = hoyolab_utils.build_cookie_string(no, account.get('cookies', {}))
    if cookie_string is None:
        logging.error(f"Cannot process account #{no}")
        return 1
    
    headers = {
        'User-Agent': config['user_agent'],
        'Referer': 'https://act.hoyolab.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': cookie_string
    }
    failed = 0

    if(hoyolab_utils.is_valid_cookie(headers)):
        logging.info(f'Cookies for account #{no} is valid')
    else:
        logging.error(f'Cookies #{no} not valid (expired?)')
        return 1  

    games = account.get('games', [])

    logging.info(f'Found games {repr(games)}')
    
    for biz in games:
        opts = hoyolab_utils.get_biz_opts(biz)
        if opts is None:
            logging.warning(f"Unknown game '{biz}'")
            continue
        result = process_game(biz, opts, headers)
        if result['failed']:
            logging.error(result['status'])
            failed += 1
        else:
            logging.info(result['status'])
            if discord_url is not None:
                send_discord_notification(discord_url, opts, result)

    return failed


#region Main

init_config()

discord_url = config.get('discord_webhook_url', None)
discord_valid = is_valid_url(discord_url)
print(discord_valid)
if not discord_valid:
    logging.info('No valid discord url, not sending notification')
    discord_url = None

accounts = config.get('accounts')
num_accounts = len(accounts)
logging.info(f'Number of accounts is {num_accounts}')

failed = 0
for i in range(num_accounts):
    try:
        failed += process_account(i+1, accounts[i], discord_url)
    except Exception as e:
        logging.error(e.args)
        failed+=1


if failed > 0:
    logging.error(f"Failed to process {failed} account(s)")

logging.info('Hoyolab Auto Check-in successfully finished')

#endregion
