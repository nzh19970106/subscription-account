# -*- coding: utf-8 -*-

import httplib
import md5
import urllib
import json
import random
from Tkinter import *
import tkMessageBox
from preprocess.utils import tools
import codecs
sys.path.append("./preprocess/data")

httpClient = None

class Application():

    def __init__(self):

        self._from = 'en'
        self._to = 'zh'
        self._appid = '**********'  # 安全起见，我就注释掉了
        self._key = '********'

        self.root = Tk()
        self.root.title("翻译小软件-赵越")
        self.root.geometry('800x800')

        self.load_sys()
        self.frm = Frame(self.root)
        Label(self.frm, text="需要翻译的句子").pack()
        self.l = Listbox(self.frm, width=80, height=20)
        self.l.pack()
        for item in self.text:
            self.l.insert(END, item)

        self.Button1 = Button(self.frm, text="翻译", command=self.GetResult)
        self.Button1.pack()
        self.Button2 = Button(self.frm, text="No Need", command=self.Getremove)
        self.Button2.pack()
        self.frm.pack()

    def load_sys(self):
        filename = tools.file_find("tweet_classification/train/tweets_test.txt")
        file_m = codecs.open(filename, 'r')
        self.text = []
        for line in file_m.readlines():
            line = line.strip().split('\t')
            texts = line[0]
            self.text.append(texts)


    def Getremove(self):
        self.l.delete(self.l.curselection())

    def GetResult(self):

        q = self.l.get(self.l.curselection())
        q = q.encode('utf8')
        myurl = '/api/trans/vip/translate'
        salt = random.randint(10001, 99999)
        sign = self._appid + q + str(salt) + self._key
        m1 = md5.new()
        m1.update(sign)
        sign = m1.hexdigest()

        myurl = myurl+'?appid='+self._appid+'&q='+urllib.quote(q)+'&from='+self._from+'&to='+self._to+'&salt='+str(salt)+'&sign='+sign
        try:
            httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            TransResult = response.read()
            data = json.loads(TransResult)
            # print data
            dst = data['trans_result'][0]['dst']
            # print dst
            tkMessageBox.showinfo('text', "text is: %s" % dst)
            # return self._dst
        except:
            print "error"

# ----------- 程序的入口 -----------
app = Application()
mainloop()