from wecom_bot_svr import WecomBotServer, RspTextMsg, RspMarkdownMsg, ReqMsg
from wecom_bot_svr.req_msg import TextReqMsg

import sync_async_proc
from cmd_process import handle_command
from common import logger, FileMsg, MarkdownMsg


def msg_handler(req_msg: ReqMsg, server: WecomBotServer):
    # @机器人 help 打印帮助信息
    if req_msg.msg_type == "text" and isinstance(req_msg, TextReqMsg):
        # chat_id是IM平台相关内容，不放在process_cmd中处理
        if req_msg.content.strip() == "chat_id":
            ret = RspTextMsg()
            ret.content = req_msg.chat_id
            return ret

        try:
            def task():
                return handle_command(req_msg.from_user.en_name, req_msg.content.lstrip())

            def cb(result):
                if isinstance(result, str):
                    send_ret = server.send_text(req_msg.chat_id, result)
                    logger.info(f"send text ret: {send_ret}")
                elif isinstance(result, MarkdownMsg):
                    send_ret = server.send_markdown(req_msg.chat_id, result.content)
                    logger.info(f"send markdown ret: {send_ret}")
                elif isinstance(result, FileMsg):
                    send_ret = server.send_file(req_msg.chat_id, result.file_path)
                    logger.info(f"send file ret: {send_ret}")
                else:
                    logger.error(f"Unknown result type: {result}")

            def fail_cb(result):
                logger.info(f"fail to process msg from {req_msg.from_user.en_name}: {req_msg.content.lstrip()}")

            cmd_ret = sync_async_proc.SyncAsyncRspProcessor(task, timeout=2, complete_cb=cb, fail_timeout=10,
                                                            fail_cb=fail_cb).get_result()
            if cmd_ret is not None:  # 即时消息，立马返回
                if isinstance(cmd_ret, str):
                    ret = RspTextMsg()
                    ret.content = cmd_ret
                    return ret
                elif isinstance(cmd_ret, MarkdownMsg):
                    ret = RspMarkdownMsg()
                    ret.content = cmd_ret.content
                    return ret
                elif isinstance(cmd_ret, FileMsg):
                    send_ret = server.send_file(req_msg.chat_id, cmd_ret.file_path)
                    logger.info(f"send file ret: {send_ret}")
            # 处理时间长，后续异步发送，先回空白消息；或者不需要处理的消息
            return RspTextMsg()
        except Exception as e:
            logger.error(f"Error: {e}")
            ret = RspTextMsg()
            ret.content = f"Error: {e}"
            return ret
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
    from config import wecom_token, wecom_aes_key, wecom_corp_id, wecom_bot_key, wecom_bot_name, wecom_svr_host, \
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
    logger.info(f"Server started at {wecom_svr_host}:{wecom_svr_port}{wecom_svr_path}")

    server.set_message_handler(msg_handler)
    server.set_event_handler(event_handler)
    server.run()


if __name__ == "__main__":
    main()
