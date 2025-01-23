from wecom_bot_svr import WecomBotServer, RspTextMsg, RspMarkdownMsg, ReqMsg
from wecom_bot_svr.req_msg import TextReqMsg

import cmd_process
from common import logger


def help_md():
    return """### Help 列表
- [给项目点赞](https://github.com/easy-wx/wecom-bot-svr)
- 其他功能请自行开发
"""


def msg_handler(req_msg: ReqMsg, server: WecomBotServer):
    # @机器人 help 打印帮助信息
    if req_msg.msg_type == 'text' and isinstance(req_msg, TextReqMsg):
        try:
            cmd_process.handle_command(req_msg.from_user, req_msg.content, req_msg.chat_id)
        except Exception as e:
            logger.error(f'Error: {e}')
            ret = RspTextMsg()
            ret.content = f'Error: {e}'
            return RspTextMsg()
    else:
        ret = RspTextMsg()
        ret.content = f'暂不支持的消息类型，msg_type: {req_msg.msg_type}'
        return ret


def event_handler(req_msg):
    ret = RspMarkdownMsg()
    if req_msg.event_type == 'add_to_chat':  # 入群事件处理
        ret.content = f'msg_type: {req_msg.msg_type}\n群会话ID: {req_msg.chat_id}\n查询用法请回复: help'
    return ret


def main():
    token = 'xxx'  # 3个x
    aes_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # 43个x
    corp_id = ''
    host = '0.0.0.0'
    port = 5001
    bot_key = 'xxxxx'  # 机器人配置中的webhook key

    # 这里要跟机器人名字一样，用于切分群组聊天中的@消息
    bot_name = 'jasonzxpan-bot'
    server = WecomBotServer(bot_name, host, port, path='/wecom_bot', token=token, aes_key=aes_key, corp_id=corp_id,
                            bot_key=bot_key)

    server.set_message_handler(msg_handler)
    server.set_event_handler(event_handler)
    server.run()


if __name__ == '__main__':
    main()
