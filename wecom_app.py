from wecom_bot_svr import WecomBotServer, RspTextMsg, RspMarkdownMsg, ReqMsg
from wecom_bot_svr.req_msg import TextReqMsg

from .cmd_process import handle_command
from .common import logger


def msg_handler(req_msg: ReqMsg, server: WecomBotServer):
    # @机器人 help 打印帮助信息
    if req_msg.msg_type == "text" and isinstance(req_msg, TextReqMsg):
        try:
            handle_command(req_msg.from_user, req_msg.content, req_msg.chat_id)
        except Exception as e:
            logger.error(f"Error: {e}")
            ret = RspTextMsg()
            ret.content = f"Error: {e}"
            return RspTextMsg()
    else:
        ret = RspTextMsg()
        ret.content = f"暂不支持的消息类型，msg_type: {req_msg.msg_type}"
        return ret


def event_handler(req_msg):
    ret = RspMarkdownMsg()
    if req_msg.event_type == "add_to_chat":  # 入群事件处理
        ret.content = (
            f"msg_type: {req_msg.msg_type}\n群会话ID: {req_msg.chat_id}\n查询用法请回复: help"
        )
    return ret


def main():
    from .config import wecom_token, wecom_aes_key, wecom_corp_id, wecom_bot_key, wecom_bot_name, wecom_svr_host, \
        wecom_svr_port, wecom_svr_path

    server = WecomBotServer(
        wecom_bot_name,
        wecom_svr_host,
        wecom_svr_port,
        path=wecom_svr_path,
        token=wecom_token,
        aes_key=wecom_aes_key,
        corp_id=wecom_corp_id,
        bot_key=wecom_bot_key,
    )

    server.set_message_handler(msg_handler)
    server.set_event_handler(event_handler)
    server.run()


if __name__ == "__main__":
    main()
