# 场景ID
from spec_line_proc_funcs import hash_proc

# 场景分布的目录，按照顺序来搜索命令处理模块
scene_dirs = ["services", "activities", "public"]

# 特殊处理函数
special_line_prefix = [("#", hash_proc.handle_command)]

# 企业微信配置
wecom_token = "xxx"  # 3个x
wecom_aes_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 43个x
wecom_corp_id = ""
wecom_bot_key = "xxxxx"  # 机器人配置中的webhook key
wecom_bot_name = "jasonzxpan-bot"  # 这里要跟机器人名字一样，用于切分群组聊天中的@消息
wecom_svr_host = "0.0.0.0"
wecom_svr_port = 5001
wecom_svr_path = "/wecom_bot"
