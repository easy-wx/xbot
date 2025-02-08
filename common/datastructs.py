class XBotMsg:
    def __init__(self, msg_type):
        self.msg_type = msg_type

    def type_name(self):
        return self.msg_type


class FileMsg(XBotMsg):
    def __init__(self, file_path):
        self.file_path = file_path
        super().__init__("file")


class MarkdownMsg(XBotMsg):
    def __init__(self, content=""):
        self.content = content
        super().__init__("markdown")
