# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs, MySQLdb, json, traceback
from MacDonaldAnalyse.items import MacDonaldItem\
    , BaiduTrafficItem, BaiduFoodItem, ParkingLotItem, SchoolItem, CommunityItem
import MySQLdb.cursors

class ScrapytestPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingTutorialPipeline(object):
    def __init__(self):
        self.file = codecs.open('MacDonaldAnalyse.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n\n'
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class MysqlTutorialPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            db='macdonald',
            user='root',  # replace with you user name
            passwd='',  # replace with you password
            charset='utf8',
            use_unicode=True,
        )

    def process_item(self, item, spider):
        self.conn.ping(True)
        try:
            cursor = self.conn.cursor()
            if isinstance(item, MacDonaldItem):
                sql = """
                    insert into macdonalditem(name,lat,lng,address,uid,detail_url,price,overall_rating)
                     values (%s,%s,%s,%s,%s,%s,%s,%s);
                """
                cursor.execute(sql, (item["name"], item["lat"], item["lng"], item["address"],
                                   item["uid"], item["detail_url"], item["price"], item["overall_rating"]))
                self.conn.commit()
            elif isinstance(item,BaiduTrafficItem):
                sql = """
                     insert into trafficitem(macDonaldId,trafficName,trafficlat,trafficlng
                     ,trafficLine,trafficuid,distance) values (%s,%s,%s,%s,%s,%s,%s);
                """
                cursor.execute(sql, (item['macDonaldId'], item['trafficName'], item['trafficlat']
                                , item['trafficlng'], item['trafficLine'], item['trafficuid'], item['distance']))
                self.conn.commit()

            elif isinstance(item,ParkingLotItem):
                sql = """
                    insert into parkinglotitem(macDonaldId,parkingLotname,parkingLotlat,parkingLotlng
                    ,parkingLotAdress,parkingLotUid,parkingLotDistance) values (%s,%s,%s,%s,%s,%s,%s);
                """
                cursor.execute(sql, (item['macDonaldId'], item['parkingLotname'], item['parkingLotlat']
                                          , item['parkingLotlng'], item['parkingLotAdress'], item['parkingLotUid'], item['parkingLotDistance']))
                self.conn.commit()

            elif isinstance(item,BaiduFoodItem):
                sql = """
                    insert into fooditem(macDonaldId,businessName,businesslat,businesslng
                    ,businessAddress,businessUid,businessDistance,businessDetail
                    ,businessPrice,businessOverall_rating) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """
                cursor.execute(sql, (item['macDonaldId'], item['businessName'], item['businesslat']
                                          , item['businesslng'], item['businessAddress'], item['businessUid']
                                          , item['businessDistance'],item['businessDetail'], item['businessPrice']
                                          , item['businessOverall_rating']))
                self.conn.commit()

            elif isinstance(item, SchoolItem):
                sql = """
                    insert into schoolitem(macDonaldId,scohoolName,schoollat,schoollng
                    ,schoolAddress,schooldUid,distance,schoolUrl,type,total)
                     values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """
                cursor.execute(sql, (item['macDonaldId'], item['schoolName'], item['schoollat']
                                          , item['schoollng'], item['schoolAddress'], item['schoolUid']
                                          , item['schoolDistance'],item['schoolDetail'], item['type']
                                          , item['total']))
                self.conn.commit()

            elif isinstance(item, CommunityItem):
                sql = """
                    insert into communityitem(macDonaldId,communityName,communitylat,communitylng
                    ,communityAddress,communityUid,communityDistance,communityBaiduDetail,
                    communityOtherDetail,communityPrice,communityTotal,belong_mac,type)
                     values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """
                cursor.execute(sql, (item['macDonaldId'], item['communityName'], item['communitylat']
                                          , item['communitylng'], item['communityAddress'], item['communityUid']
                                          , item['communityDistance'], item['communityBaiduDetail'], item['communityOtherDetail']
                                          , item['communityPrice'], item['communityTotal'], item['belong_mac']
                                          , item['type']))
                self.conn.commit()
        except Exception:
            print(traceback.format_exc())
            self.conn.rollback()
        finally:
            cursor.close()

    def spider_closed(self, spider):
        pass