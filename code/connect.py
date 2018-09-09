#_*_coding:utf-8_*_
import falcon
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply,ImageReply,VoiceReply
from fanyi import search

class Connect(object):
    #get方法，连接微信前段，加上token
    def on_get(self, req, resp):
        print ("hello world1")
        query_string = req.query_string
        query_list = query_string.split('&')
        b = {}
        for i in query_list:
            b[i.split('=')[0]] = i.split('=')[1]
        try:
            print ("hello world2")
            check_signature(token='WeChatPython', signature=b['signature'], timestamp=b['timestamp'], nonce=b['nonce'])
            resp.body = (b['echostr'])
        except InvalidSignatureException:
            pass
        print ("hello world3")
        resp.status = falcon.HTTP_200

    #post方法
    def on_post(self,req,resp):
        #后台接受数据进行xml解析
        xml=req.stream.read()
        msg=parse_message(xml)
        print(msg)

        dict={}
        for name in dir(msg):
            value = getattr(msg, name)
            if not name.startswith('__') and not callable(value) and not name.startswith('_'):
                dict[name] = value
        print(dict)
        #print(type(dict))
        #对文本的处理
        if dict['type']=='text':
            ser=search()
            result,spaceCount,isChinese=ser.main(dict['content'])
            print(result)
            #print(spaceCount)

            # src = result_text['translateResult'][0][0]['src']
            tgt = result['translateResult'][0][0]['tgt']
            type=result['type']
            print("\ntgt:"+tgt)
            print(type)
            if spaceCount==0 and not isChinese:
                print("te")
                re_str=''
                if type == 'en2zh-CHS':
                    if "smartResult" in result:
                        re = result['smartResult']['entries']
                        while '' in re:
                            re.remove('')
                        while '  \r\n' in re:
                            re.remove('  \r\n')
                        re_str = ''.join(re[0:])
                    #print(re_str)
                    ret="基本解释\n"+tgt+"\n更多解释\n"+re_str
                else:
                    ret=tgt
                    if type == 'fr2zh-CHS':
                        ret = "法语,翻译--->" + tgt
                    elif type == 'de2zh-CHS':
                        ret = "德语，翻译--->" + tgt
            else:
                ret=tgt
                if type=='fr2zh-CHS':
                    ret="法语,翻译--->"+tgt
                elif type=='de2zh-CHS':
                    ret="德语，翻译--->"+tgt
            print(ret)
            reply=TextReply(content=ret,message=msg)
            xml=reply.render()
            resp.body=(xml)
            resp.status=falcon.HTTP_200
        #对图片的处理
        elif dict['type']=='image':
            print ("hello world5")
            reply = ImageReply(media_id=msg.media_id, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200
        #对事件的处理
        elif dict['type']=='event':
            if dict['event']=='subscribe':
                print("欢迎关注")
                reply = TextReply(content="欢迎关注，这是一个翻译小平台，",message=msg)
                xml = reply.render()
                resp.body = (xml)
                resp.status = falcon.HTTP_200
        #对音频的处理
        elif dict['type']=='voice':
                reply = VoiceReply(media_id=msg.media_id,message=msg)
                xml = reply.render()
                resp.body = (xml)
                resp.status = falcon.HTTP_200
#falcon为框架
app = falcon.API()

connect = Connect()
#定义后台路径
app.add_route('/connect', connect)