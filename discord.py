import logging
from discord_webhook import DiscordWebhook, DiscordEmbed

def send_discord_notification(discord_webhook_url, opts, result):
    logging.debug(f'Sending discord notification...')
    webhook = DiscordWebhook(url=discord_webhook_url)
    embed = DiscordEmbed(title=opts['title'], description=opts.get('description', ''), color=opts.get('color', ''))
    if (result['award_icon']):
        embed.set_thumbnail(url=result['award_icon'])
    embed.set_author(
        name=opts['author_name'],
        url=opts['author_url'],
        icon_url=opts['author_icon'],
    )
    embed.set_footer(text=f'Hoyolab Auto Check-in', icon_url='https://img-os-static.hoyolab.com/favicon.ico')
    embed.set_timestamp()
    embed.add_embed_field(name="Today's rewards", value=f"{result['award_name']} x {result['award_cnt']}")
    embed.add_embed_field(name="Total Daily Check-In", value=result['total_sign_day'])
    embed.add_embed_field(name="Check-in result:", value=result['status'], inline=False)
    webhook.add_embed(embed)
    response = webhook.execute()
    if (response.status_code == 200):
        logging.info(f'Discord notification sent successfully')
    else:
        logging.error(f'Discord notification failure\n{response}')
