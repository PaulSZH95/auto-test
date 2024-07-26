from console_src.skeletons.conversation import BaseConversation


class AutoTestConsole(BaseConversation):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
