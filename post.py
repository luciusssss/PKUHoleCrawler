class Post:
    def __init__(self, pid, pcontent, ptime):
        self.id = pid
        self.content = pcontent
        self.time = ptime
        self.replies = []

    def add_reply(self, rid, name, rcontent, rtime):
        self.replies.append(Reply(rid, name, rcontent, rtime))


class Reply:
    def __init__(self, rid, name, rcontent, rtime):
        self.id = rid
        self.name = name
        self.content = rcontent
        self.time = rtime