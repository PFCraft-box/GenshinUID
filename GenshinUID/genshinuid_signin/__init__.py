import random

from .sign import sign_in, daily_sign
from ..all_import import *  # noqa: F403,F401
from ..utils.db_operation.db_operation import config_check


# 每日零点半执行米游社原神签到
@sv.scheduled_job('cron', hour='0', minute='30')
async def sign_at_night():
    if await config_check('SchedSignin'):
        await send_daily_sign()


# 群聊内 签到 功能
@sv.on_rex(r'^(gs|米游社)(签到)$')
async def get_sign_func(bot: HoshinoBot, ev: CQEvent):
    logger.info('开始执行[签到]')
    qid = int(ev.sender['user_id'])  # type: ignore
    logger.info('[签到]QQ号: {}'.format(qid))
    uid = await select_db(qid, mode='uid')
    logger.info('[签到]UID: {}'.format(uid))
    im = await sign_in(uid)
    await bot.send(ev, im, at_sender=True)


@sv.on_fullmatch('全部重签')
async def recheck(bot: HoshinoBot, ev: CQEvent):
    if ev.sender:
        qid = int(ev.sender['user_id'])
    else:
        return
    if qid not in bot.config.SUPERUSERS:
        return

    logger.info('开始执行[全部重签]')
    await bot.send(ev, '已开始执行')
    await send_daily_sign()
    await bot.send(ev, '执行完成')


async def send_daily_sign():
    logger.info('开始执行[每日全部签到]')
    bot = get_bot()
    # 执行签到 并获得推送消息
    result = await daily_sign()
    private_msg_list = result['private_msg_list']
    group_msg_list = result['group_msg_list']
    logger.info('[每日全部签到]完成')

    # 执行私聊推送
    for qid in private_msg_list:
        try:
            await bot.send_private_msg(
                user_id=qid,
                message=private_msg_list[qid],
            )
        except:
            logger.warning(f'[每日全部签到] QQ {qid} 私聊推送失败!')
        await asyncio.sleep(0.5)
    logger.info('[每日全部签到]私聊推送完成')

    # 执行群聊推送
    for gid in group_msg_list:
        # 根据succee数判断是否为简洁推送
        if group_msg_list[gid]['success'] >= 0:
            report = (
                '以下为签到失败报告：{}'.format(group_msg_list[gid]['push_message'])
                if group_msg_list[gid]['push_message'] != ''
                else ''
            )
            msg_title = '今日自动签到已完成！\n本群共签到成功{}人，共签到失败{}人。{}'.format(
                group_msg_list[gid]['success'],
                group_msg_list[gid]['failed'],
                report,
            )
        else:
            msg_title = group_msg_list[gid]['push_message']
        # 发送群消息
        try:
            await bot.send_group_msg(
                group_id=gid,
                message=msg_title,
            )
        except:
            logger.warning(f'[每日全部签到]群 {gid} 推送失败!')
        await asyncio.sleep(0.5 + random.randint(1, 3))
    logger.info('[每日全部签到]群聊推送完成')
