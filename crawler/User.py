#-*- coding: UTF-8 -*-
class User:
    name = ""
    uid = ''
    brief =''
    link = ""
    follow = 0
    follower = 0
    weibo = 0
    card = ''
    tag = ''
    verify = ''

    def __init__(self, name, uid, brief, link, follow, follower, weibo, card, tag, verify):
        self.name = name
        self.uid = uid
        self.brief = brief
        self.link = link
        self.follow = follow
        self.follower = follower
        self.weibo = weibo
        self.card = card
        self.tag = tag
        self.verify = verify

    def show(self):
        print "name: ",self.name
        print "uid: ", self.uid
        print "brief: ", self.brief
        print "link: ", self.link
        print "follow: ", self.follow
        print "follower: ", self.follower
        print "weibo: ", self.weibo
        print "card: ", self.card
        print "tag: ", self.tag
        print "verify: ", self.verify
        print