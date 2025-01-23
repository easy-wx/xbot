import importlib

from xbot import scene_dirs

from .auth import UserPermissionHelper
from .common import logger


def help_msg(cmd=None, subcmd=None):
    cmds = set()
    cmd_list = []

    return "Help message"


def handle_command(user_id, msg, chat_id=None):
    """
    处理命令
    :param user_id
    :param msg: 对话内容
    :param chat_id: 群聊时的群聊ID，用于延迟发送消息（部分处理可能耗时比较长，需要异步回复消息）
    :return:
    """
    if not msg:
        return "Empty command"

    if msg == "help":
        return help_msg()

    parts = msg.split(" ")
    if len(parts) == 1 and parts[0] == "help":
        return help_msg()
    if len(parts) == 2 and parts[0] == "help":
        return help_msg(parts[1])

    if len(parts) < 2:
        return "Invalid command format"

    cmd = parts[0]
    subcmd = parts[1]
    args = parts[2:]

    if cmd == "help":
        return help_msg(subcmd, args[0])

    # 检查处理函数是否存在
    func = None
    package = None
    for package in scene_dirs:
        try:
            module = importlib.import_module(f"{package}.{cmd}")
            func_name = f"cmd_{subcmd}"
            if hasattr(module, func_name):
                func = getattr(module, func_name)
                break
        except ImportError:
            continue
    if func is None:
        return "Unknown command"

    # 检查用户是否拥有权限
    if package != "public":
        p_helper = auth.UserPermissionHelper()
        if not p_helper.check_user_permission(user_id, cmd, subcmd):
            return "Permission denied"

    logger.info(f"User[{user_id}] execute command: {cmd} {subcmd} {args}")
    try:
        return func(*args, chat_id=chat_id)
    except TypeError:
        return func(*args)


# Example usage
if __name__ == "__main__":
    print(handle_command("jasonzxpan", "act_demo setup arg1 arg2"))
    print(handle_command("demo", "act_demo setup arg1 arg2", "chat_id"))
    print(handle_command("demo", "pub_demo setup arg1 arg2", "chat_id"))
