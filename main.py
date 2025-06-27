import asyncio
import re
from astrbot import logger
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
from astrbot.core.config.astrbot_config import AstrBotConfig
from astrbot.core.message.components import Reply
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import (
    AiocqhttpMessageEvent,
)


@register(
    "astrbot_plugin_monitor",
    "Zhalslar",
    "[仅aiocqhttp] 群消息互通插件",
    "1.0.0",
    "https://github.com/Zhalslar/astrbot_plugin_monitor",
)
class Relationship(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        # 监听群 -> 被监听群
        self.monitor_map: dict[int, int] = {}

    # ---------- 工具函数 ----------
    def extract_group_ids(self, text: str) -> list[int]:
        return [int(gid) for gid in re.findall(r"\d{6,10}", text)]

    def get_group_ids(self, event: AiocqhttpMessageEvent) -> list[int]:
        reply_seg = next(
            (seg for seg in event.get_messages() if isinstance(seg, Reply)), None
        )
        ref_text = reply_seg.message_str if reply_seg else ""
        return self.extract_group_ids(ref_text or event.message_str)



    async def build_forward_nodes(
        self, messages: list[dict], user_id: int | None = None
    ):
        nodes = []
        for msg in messages:
            if user_id and msg["sender"]["user_id"] != user_id:
                continue
            nodes.append(
                {
                    "type": "node",
                    "data": {
                        "name": msg["sender"]["nickname"],
                        "uin": msg["sender"]["user_id"],
                        "content": msg["message"],
                    },
                }
            )
        return nodes


    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("抽查")
    async def check_messages(
        self,
        event: AiocqhttpMessageEvent,
        group_id: int | None = None,
        user_id: int | None = None,
    ):
        """抽查 [群号] [数量]"""
        args = event.message_str.split()
        count = next(
            (int(arg) for arg in args if arg.isdigit() and int(arg) < 1000), 20
        )

        group_ids = [group_id] if group_id else self.get_group_ids(event)
        if not group_ids:
            yield event.plain_result("未指定要抽查的群号")
            return
        target_group = int(event.get_group_id())
        target_user = int(event.get_sender_id())
        async def check_single(gid: int):
            try:
                result = await event.bot.get_group_msg_history(
                    group_id=gid, count=count
                )
                nodes = await self.build_forward_nodes(result["messages"], user_id)
                if not nodes:
                    return
                if target_group:
                    await event.bot.send_group_forward_msg(
                        group_id=target_group, messages=nodes
                    )
                else:
                    await event.bot.send_private_forward_msg(
                        user_id=target_user, messages=nodes
                    )
            except Exception as e:
                logger.error(f"抽查群({gid})失败: {e}")

        await asyncio.gather(*(check_single(gid) for gid in group_ids))
        event.stop_event()

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("回复")
    async def reply(self, event: AiocqhttpMessageEvent):
        """(引用群号)回复 [内容]"""
        msg = event.message_str.removeprefix("回复 ").strip()
        if not msg:
            yield event.plain_result("未输入回复内容")
            return

        group_ids = self.get_group_ids(event)
        if not group_ids:
            yield event.plain_result("未指定要回复的群")
            return
        target_group = group_ids[0]
        try:
            await event.bot.send_group_msg(group_id=target_group, message=msg)
        except Exception as e:
            logger.warning(f"发送到群 {target_group} 失败：{e}")
            yield event.plain_result(f"发送到群 {target_group} 失败：{e}")
        event.stop_event()


    @filter.command("监听")
    async def monitor(self, event: AiocqhttpMessageEvent, group_id: int | None = None):
        """监听 [群号]"""
        from_gid = int(event.get_group_id())
        if not from_gid:
            yield event.plain_result("只能在群聊中使用监听命令")
            return

        group_ids = self.get_group_ids(event) if not group_id else [group_id]
        target_gid= group_ids[0]
        # 覆盖监听目标
        old_target = self.monitor_map.get(from_gid)
        self.monitor_map[from_gid] = target_gid

        if old_target == target_gid:
            yield event.plain_result(f"你已经在监听群 {target_gid}")
        else:
            yield event.plain_result(f"开始监听群 {target_gid}")

    @filter.command("取消监听")
    async def unmonitor(
        self, event: AiocqhttpMessageEvent
    ):
        """取消监听"""
        from_gid = int(event.get_group_id())
        if not from_gid:
            yield event.plain_result("只能在群聊中使用取消监听命令")
            return
        if from_gid in self.monitor_map:
            target_gid = self.monitor_map.pop(from_gid)
            yield event.plain_result(f"已取消监听群聊: {target_gid}")
        else:
            yield event.plain_result("你当前没有监听任何群")

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_message(self, event: AiocqhttpMessageEvent):
        if not event.message_str or any(isinstance(seg, Reply) for seg in event.get_messages()):
            return

        # 找出所有监听 source_gid 的监听者群
        source_gid = int(event.get_group_id())
        listeners = [from_gid for from_gid, target_gid in self.monitor_map.items() if target_gid == source_gid]
        if not listeners:
            return
        sender_name = event.get_sender_name()
        forward_msg = f"[来自群{source_gid}的{sender_name}]\n{event.message_str}"

        for from_gid in listeners:
            try:
                await event.bot.send_group_msg(group_id=from_gid, message=forward_msg)
            except Exception as e:
                logger.warning(f"转发到群 {from_gid} 失败: {e}")

        event.stop_event()
