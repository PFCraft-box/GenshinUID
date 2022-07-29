from .draw_abyss_card import draw_abyss_img
from ..all_import import *  # noqa: F403,F401
from ..utils.db_operation.db_operation import select_db

get_abyss_info = on_regex(
    '^(\[CQ:at,qq=[0-9]+\] )?'
    '(uid|查询|mys)?([0-9]{9})?(上期)?(深渊|sy)'
    '(9|10|11|12|九|十|十一|十二)?(层)?'
    '(\[CQ:at,qq=[0-9]+\])?$'
)


@get_abyss_info.handle()
@handle_exception('查询深渊信息')
async def send_abyss_info(
    event: Union[GroupMessageEvent, PrivateMessageEvent],
    matcher: Matcher,
    args: Tuple[Any, ...] = RegexGroup(),
    custom: ImageAndAt = Depends(),
):
    at = custom.get_first_at()
    if at:
        qid = at
    else:
        qid = event.user_id

    if args[1] == 'mys':
        mode = 'mys'
    else:
        mode = 'uid'

    # 判断uid
    if args[2] is None:
        try:
            uid = await select_db(qid, mode='uid')
            uid = uid[0]
        except TypeError:
            await matcher.finish(UID_HINT)
    else:
        uid = args[2]

    # 判断深渊期数
    if args[3] is None:
        schedule_type = '1'
    else:
        schedule_type = '2'

    if args[5] in ['九', '十', '十一', '十二']:
        floor = (
            args[5]
            .replace('九', '9')
            .replace('十一', '11')
            .replace('十二', '12')
            .replace('十', '10')
        )
    else:
        floor = args[5]
    im = await draw_abyss_img(uid, floor, mode, schedule_type)
    if isinstance(im, str):
        await matcher.finish(im)
    elif isinstance(im, bytes):
        await matcher.finish(MessageSegment.image(im))
    else:
        await matcher.finish('发生了未知错误,请联系管理员检查后台输出!')
