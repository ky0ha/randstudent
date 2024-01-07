class Class(object):
    cno = 0
    def __init__(self, ctime: int, member: list):
        self.ctime = ctime
        Class.cno += 1
        self.member = member
    
    def change(self, new_member: str):
        self.member.append(new_member)