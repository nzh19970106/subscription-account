# -*-coding:utf-8 -*-
from hashlib import sha1
from flask import Flask, request

token = 'WeChatPython'

app = Flask(__name__)

def get_update(token, timestamp, nonce):
    arguments = ''
    for k in sorted([token, timestamp, nonce]):
        arguments = arguments + str(k)
    m = sha1()
    m.update(arguments.encode('utf8'))
    return m.hexdigest()

def check_signature():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    check = get_update(token, timestamp, nonce)
    return True if check == signature else False

def parse_xml(data):
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(data)
        datas = '<xml>'
        for child in root:
            if child.tag == 'ToUserName':
                toUser = child.text
                datas += '<FromUserName>%s</FromUserName>' % toUser
            elif child.tag == 'FromUserName':
                fromUser = child.text
                datas += '<ToUserName>%s</ToUserName>' % fromUser
            else:
                datas += '<' + child.tag + '>'
                datas += child.text
                datas += '</' + child.tag + '>'
        datas += '</xml>'
        return datas

@app.route('/WeChatPython', methods=['GET', 'POST'])
def weixinInterface():
    if check_signature:
        if request.method == 'GET':
            echostr = request.args.get('echostr', '')
            return echostr
        elif request.method == 'POST':
            data = request.data
            msg = parse_xml(data)
            return msg
    else:
        return 'signature error'

if __name__ == '__main__':
    app.run()