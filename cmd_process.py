import importlib

from config import scene_dirs, special_line_prefix
from auth import UserPermissionHelper
from common import logger, XBotMsg


def help_msg(cmd=None, subcmd=None):
    cmds = set()
    cmd_list = []

    return "Help message"


def handle_command(user_id, msg) -> str | XBotMsg:
    """
    处理命令
    :param user_id
    :param msg: 对话内容
    :param chat_id: 群聊时的群聊ID，用于延迟发送消息（部分处理可能耗时比较长，需要异步回复消息）
    :return:
    """
    if not msg:
        return "Empty command"

    logger.info(f"User[{user_id}] send message: {msg}")

    for prefix, handle_func in special_line_prefix:
        if msg.startswith(prefix):
            p_helper = UserPermissionHelper()
            if not p_helper.check_user_permission(user_id, prefix, ""):
                return "Permission denied"
            return handle_func(user_id, msg[len(prefix):])

    if msg == "help":
        return help_msg()

    if msg.find("\n") != -1:
        cmd_line, remaining = msg.split("\n", 1)
        parts = cmd_line.split(" ") + [remaining]
    else:
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
    logger.info(f"User[{user_id}], cmd: {cmd}, subcmd: {subcmd}, args: {args}")

    if cmd == "help":
        return help_msg(subcmd, args[0])

    # 检查处理函数是否存在
    func = None
    package = None
    for package in scene_dirs:
        try:
            module_name = f"{package}.{cmd}"
            module = importlib.import_module(module_name)
            func_name = f"cmd_{subcmd}"
            if hasattr(module, func_name):
                func = getattr(module, func_name)
                logger.info(f"Found command: {cmd} {subcmd}, module: {module_name}, function: {func_name}")
                break
            else:
                logger.info(f"Command not found: {cmd} {subcmd}, module: {module_name}")
        except ImportError as e:
            logger.error(f"Error: import error, {e}")
            continue
        except Exception as e:
            logger.error(f"Error: {e}")
    if func is None:
        return "Unknown command"

    # 检查用户是否拥有权限
    if package != "public":
        p_helper = UserPermissionHelper()
        if not p_helper.check_user_permission(user_id, cmd, subcmd):
            return "Permission denied"

    logger.info(f"User[{user_id}] execute command: {cmd} {subcmd} {args}")
    try:
        return func(*args)
    except TypeError:
        return func(args)


# Example usage
if __name__ == "__main__":
    print(handle_command("jasonzxpan", "act_demo setup arg1 arg2"))
    print(handle_command("demo", "act_demo setup arg1 arg2"))
    print(handle_command("demo", "pub_demo setup arg1 arg2"))
    print(handle_command("demo", "@pub_demo setup arg1 arg2"))
