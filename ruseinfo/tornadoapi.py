import sys
import codecs
import platform
plat = platform.system().lower()
if plat == 'linux':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import tornado.ioloop
import tornado.web
import json
import logtool

from auction import swuee
from auction import rmfysszc
from auction import hebaee
from auction import ejy365
from auction import cquae
from auction import cbex
from auction import chanjs
from auction import gscq
from auction import qzcq
from auction import cspea
from auction import qhcqjy
from auction import yqp
from auction import alipm
from auction import caa123
from news import newsletter
from news import focus
from news import forward

###西南联合产权交易所###
#http://127.0.0.1:8868/swuee/list?current=1&subject=01
class SwueeListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        queryResp = swuee.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/swuee/detail?id=1
class SwueeDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = swuee.queryDetail(id)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###河北产权市场###
#http://127.0.0.1:8868/hebaee/list?current=1&subject=01
class HebaeeListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        queryResp = hebaee.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/hebaee/detail?id=1
class HebaeeDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = hebaee.queryDetail(id)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###人民法院诉讼资产###
#http://127.0.0.1:8868/rmfysszc/list?current=1&subject=01
class RmfysszcListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        province = '' #省 self.get_argument('province')
        city = '' #市 self.get_argument('city')
        county = '' #县 self.get_argument('county')
        queryResp = rmfysszc.queryList(current,subject,province,city,county)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/rmfysszc/detail?id=1
class RmfysszcDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = rmfysszc.queryDetail(id,False)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###e交易###
#http://127.0.0.1:8868/ejy365/list?current=1&subject=01
class Ejy365ListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        queryResp = ejy365.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/ejy365/detail?id=1
class Ejy365DetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = ejy365.queryDetail(id,False)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###重庆产权交易网###
#http://127.0.0.1:8868/cquae/list?current=1&subject=01
class CquaeListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        queryResp = cquae.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/cquae/detail?id=1
class CquaeDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = cquae.queryDetail(id,False)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###北京产权交易所###
#http://127.0.0.1:8868/cbex/list?current=1
class CbexListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        #subject = self.get_argument('subject') #标的类型
        queryResp = cbex.queryList(current,'01')
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/cbex/detail?id=1
class CbexDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = cbex.queryDetail(id)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###杭州产金所###
#http://127.0.0.1:8868/chanjs/list?current=1&subject=01
class ChanjsListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        queryResp = chanjs.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/chanjs/detail?id=1
class ChanjsDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = chanjs.queryDetail(id,False)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###甘肃省产权交易所###
#http://127.0.0.1:8868/gscq/list?current=1&subject=01
class GscqListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        queryResp = gscq.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/gscq/detail?id=1
class GscqDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = gscq.queryDetail(id,False)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###泉州市产权交易中心###
#http://127.0.0.1:8868/qzcq/list?current=1&subject=01
class QzcqListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        queryResp = qzcq.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/qzcq/detail?id=1
class QzcqDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = qzcq.queryDetail(id,False)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###全国产权行业信息化综合服务平台###
#http://127.0.0.1:8868/cspea/list?current=1&subject=01
class CspeaListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        queryResp = cspea.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/cspea/detail?id=1
class CspeaDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = cspea.queryDetail(id,None)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###青海省产权交易市场###
#http://127.0.0.1:8868/qhcqjy/list?current=1&subject=01
class QhcqjyListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        queryResp = qhcqjy.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/qhcqjy/detail?id=1
class QhcqjyDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = qhcqjy.queryDetail(id,None)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###宜企拍###
#http://127.0.0.1:8868/yqp/list?current=1&subject=01
class YqpListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        queryResp = yqp.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/yqp/detail?id=1
class YqpDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = yqp.queryDetail(id)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###阿里拍卖###
#http://127.0.0.1:8868/alipm/list?current=1&subject=01
class AlipmListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        queryResp = alipm.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/alipm/detail?id=1
class AlipmDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = alipm.queryDetail(id)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###中拍平台###
#http://127.0.0.1:8868/caa123/list?current=1&subject=01
class Caa123ListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject') #标的类型
        queryResp = caa123.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/caa123/detail?id=1
class Caa123DetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = caa123.queryDetail(id)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###mysteel 快讯###
#http://127.0.0.1:8868/news/letter/list?current=1
class NewsletterListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        queryResp = newsletter.queryList(current)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###mysteel 综合资讯 > 聚焦###
#http://127.0.0.1:8868/news/focus/list?current=1
class FocusListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        queryResp = focus.queryList(current)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/news/focus/detail?id=1
class FocusDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = focus.queryDetail(id)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)

###mysteel 期货###
#http://127.0.0.1:8868/news/forward/list?current=1&subject=01
class ForwardListHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        current = self.get_argument('current') #页数
        subject = self.get_argument('subject')
        queryResp = forward.queryList(current,subject)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
#http://127.0.0.1:8868/news/forward/detail?id=1
class ForwardDetailHandler(tornado.web.RequestHandler):
    def get(self):
        logtool.info("remoteIp:" + self.request.remote_ip)
        id = self.get_argument('id')
        queryResp = forward.queryDetail(id)
        queryResp = json.dumps(queryResp,ensure_ascii=False)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.flush()
        self.finish(queryResp)
       
 
application = tornado.web.Application([
                (r"/swuee/list", SwueeListHandler), (r"/swuee/detail", SwueeDetailHandler),
                (r"/hebaee/list", HebaeeListHandler),(r"/hebaee/detail", HebaeeDetailHandler),
                (r"/rmfysszc/list", RmfysszcListHandler),(r"/rmfysszc/detail", RmfysszcDetailHandler),
                (r"/ejy365/list", Ejy365ListHandler),(r"/ejy365/detail", Ejy365DetailHandler),
                (r"/cquae/list", CquaeListHandler),(r"/cquae/detail", CquaeDetailHandler),
                (r"/cbex/list", CbexListHandler),(r"/cbex/detail", CbexDetailHandler),
                (r"/chanjs/list", ChanjsListHandler),(r"/chanjs/detail", ChanjsDetailHandler),
                (r"/gscq/list", GscqListHandler),(r"/gscq/detail", GscqDetailHandler),
                (r"/qzcq/list", QzcqListHandler),(r"/qzcq/detail", QzcqDetailHandler),
                (r"/cspea/list", CspeaListHandler),(r"/cspea/detail", CspeaDetailHandler),
                (r"/qhcqjy/list", QhcqjyListHandler),(r"/qhcqjy/detail", QhcqjyDetailHandler),
                (r"/yqp/list", YqpListHandler),(r"/yqp/detail", YqpDetailHandler),
                (r"/alipm/list", AlipmListHandler),(r"/alipm/detail", AlipmDetailHandler),
                (r"/caa123/list", Caa123ListHandler),(r"/caa123/detail", Caa123DetailHandler),
                (r"/news/letter/list", NewsletterListHandler),
                (r"/news/focus/list", FocusListHandler),(r"/news/focus/detail", FocusDetailHandler),
                (r"/news/forward/list", ForwardListHandler),(r"/news/forward/detail", ForwardDetailHandler)
            ])
 
if __name__ == "__main__":
    logtool.info("------tornado start------")
    application.listen(8868)
    logtool.info("------listen port: 8868------")
    tornado.ioloop.IOLoop.instance().start()