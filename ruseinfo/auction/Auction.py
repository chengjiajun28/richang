import json
from dataclasses import dataclass

from ruseinfo.tools import date_parse


@dataclass
class Auction_Info(object):
    def __init__(self, origin_id="", auction_id="", assets_name="", announcement_start_time="",
                 announcement_end_time="", deposit="",
                 img_url="", img_prefix="", img_paths="", province="", city="", county="", website="", assets_type="",
                 detail_id="", onlookers="", state="", url="", sync_uat=False, sync_prd=False):
        self.origin_id = origin_id
        self.auction_id = auction_id
        self.assets_name = assets_name
        self.announcement_start_time = announcement_start_time
        self.announcement_end_time = announcement_end_time
        self.deposit = deposit
        self.img_url = img_url
        self.img_prefix = img_prefix
        self.img_paths = img_paths
        self.province = province
        self.city = city
        self.county = county
        self.website = website
        self.assets_type = assets_type
        self._id = detail_id
        self.onlookers = onlookers
        self.state = state
        self.url = url
        self.sync_uat = sync_uat
        self.sync_prd = sync_prd

    # 网站原始id
    origin_id: str
    # 拍卖标的ID
    auction_id: str
    # 拍卖公告名称
    assets_name: str
    # 报名开始时间
    announcement_start_time: str
    # 报名截止时间
    announcement_end_time: str
    # 保证金
    deposit: str
    # 图片url
    img_url: str
    # imgPaths前缀
    img_prefix: str
    # 图片路径，多个分隔
    img_paths: str
    # 省份
    province: str
    # 城市
    city: str
    # 县
    county: str
    # 拍卖网站 标识符 可以是域名
    website: str
    # 拍卖类型
    assets_type: str
    # 关注数
    onlookers: str
    # 状态
    state: str
    # 拍卖链接
    url: str
    sync_uat: bool = False
    sync_prd: bool = False

    def to_json(self):
        if self.img_paths and isinstance(self.img_paths, list):
            self.img_paths = ";".join(self.img_paths)
        if self.deposit:
            self.deposit = str(self.deposit)
        return {
            "auctionId": self.auction_id,
            "assetsName": self.assets_name,
            "announcementStartTime": date_parse(self.announcement_start_time),
            "announcementEndTime": date_parse(self.announcement_end_time),
            "deposit": self.deposit,
            "imgUrl": self.img_url,
            "imgPrefix": self.img_prefix,
            "imgPaths": self.img_paths,
            "province": self.province,
            "city": self.city,
            "county": self.county,
            "website": self.website,
            "assetsType": self.assets_type,
            "syncUat": self.sync_uat,
            "syncPrd": self.sync_prd
        }


@dataclass
class Auction_Detials(object):
    def __init__(self, state="", onlookers="", start_price="", detials="", listing_start_date="", listing_end_date="",
                 url="", tendering_org="", id=""):
        self.state = state
        self.url = url
        self.onlookers = onlookers
        self.start_price = start_price
        self.detials = detials
        self.listing_end_date = listing_end_date
        self.listing_start_date = listing_start_date
        self.tendering_org = tendering_org
        self.id = id

    id: str
    # 状态 1-未开始，2-正在报名，3-报名截止，4-竞价中，5-竞价截止，6-已成交
    # 拍卖链接
    url: str
    # 招标单位
    tendering_org = ""
    state: object
    # 围观数
    onlookers: str
    start_price: str
    detials: object
    listing_start_date: str
    listing_end_date: str

    def to_json(self):
        if isinstance(self.state, list):
            self.state = ",".join(self.state)
        if isinstance(self.detials, list):
            self.detials = json.dumps(self.detials, ensure_ascii=False)
        if self.start_price:
            self.start_price = str(self.start_price)
        return {
            "_id": self.id,
            "data": {
                "state": self.state,
                "url": self.url,
                "onlookers": self.onlookers,
                "startPrice": self.start_price,
                "detials": self.detials
            }
        }
