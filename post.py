class Post:
    def __init__(self, pid, context, ptime):
        self.pid = pid
        self.context = context
        self.time = ptime
        self.replies = []

    def add_reply(self, name, context, rtime):
        self.replies.append(Reply(name, context, rtime))


class Reply:
    def __init__(self, name, context, rtime):
        self.name = name
        self.context = context
        self.time = rtime