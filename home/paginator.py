# coding=utf-8
import json
import datetime
from django.forms.models import model_to_dict


class Paginator:

    # obj_list:传入的对象列表; count:每一页记录的条数
    def __init__(self, obj_list, count, index):
        self.obj_list = obj_list
        self.count = count
        self.index = index

    # 计算总页数
    def page_num(self):
        length = len(self.obj_list)
        if length % self.count != 0:
            return length // self.count + 1
        else:
            return length / self.count

    # 计算当前索引页记录条数
    def page_index_num(self):
        pre_obj_count = self.count * (self.index - 1)
        if pre_obj_count + self.count > len(self.obj_list):
            return len(self.obj_list) - pre_obj_count
        else:
            return self.count

    # 返回当前页记录的json集合
    def page(self):
        json_list = []
        day = datetime.datetime.now()
        page_index_num = self.page_index_num()
        # 循环当前页
        for i in range(self.count*(self.index-1), self.count*(self.index-1)+page_index_num):
            attr_dic = self.obj_list[i].__dict__    # 取得记录对象的所有属性
            del attr_dic['_state']  # 删除不需要的属性
            if '_puser_cache' in attr_dic:  # 外键json化
                attr_dic['_puser_cache'] = model_to_dict(attr_dic['_puser_cache'])
                # datetime类型无法直接转化，这里没有用到此属性，故删除，如有需要参照下面的方法json化
                del attr_dic['_puser_cache']['ulogintime']
            for key in attr_dic:
                if type(attr_dic[key]) == type(day):
                    json_time = {'year': attr_dic[key].year, 'month': attr_dic[key].month, 'day': attr_dic[key].day,
                                 'hour': attr_dic[key].hour, 'minute': attr_dic[key].minute}
                    attr_dic[key] = json_time
            json_list.append(attr_dic)
        # print(json_list)
        return json_list
'''
['{"prepercent_4": "1.88025754965793e-08", "prepercent_2": "0.297897070646286", "prepercent_1": "0.0048279925249517", "prepercent_0": "0.231880813837051", "purl": "/static/images/picture/4/201913091333_8.png", "pstatus": "1", "preresult": "9", "id": "36", "_state": "<django.db.models.base.ModelState object at 0x7f653e8bd9b0>", "prepercent_8": "0.000219512905459851", "pretime": "3.74", "prepercent_5": "0.00811338424682617", "pcreatetime": "2019-01-30 09:13:33.266208+00:00", "prepercent_6": "3.1406111133947e-07", "prepercent_7": "0.000241397996433079", "prepercent_3": "0.0101550947874784", "puser_id": "4", "prepercent_9": "0.446664333343506"}', '{"prepercent_4": "4.80434609926306e-05", "prepercent_2": "4.29356941822334e-06", "prepercent_1": "0.999379992485046", "prepercent_0": "2.31868466471497e-06", "purl": "/static/images/picture/4/201913010494_3.png", "pstatus": "1", "preresult": "1", "id": "37", "_state": "<django.db.models.base.ModelState object at 0x7f653e8bda20>", "prepercent_8": "0.000128902946016751", "pretime": "2.9", "prepercent_5": "3.15294329311655e-07", "pcreatetime": "2019-01-30 10:49:04.063037+00:00", "prepercent_6": "6.88323416397907e-05", "prepercent_7": "1.36640394998722e-07", "prepercent_3": "0.000252112717134878", "puser_id": "4", "prepercent_9": "0.000114991285954602"}', '{"prepercent_4": "1.36242363169004e-06", "prepercent_2": "4.98188934550114e-10", "prepercent_1": "5.70297444824064e-08", "prepercent_0": "5.17736054916895e-07", "purl": "/static/images/picture/4/2019130105134_4.png", "pstatus": "1", "preresult": "8", "id": "38", "_state": "<django.db.models.base.ModelState object at 0x7f653e8bda90>", "prepercent_8": "0.99355149269104", "pretime": "1.27", "prepercent_5": "1.8964030459756e-05", "pcreatetime": "2019-01-30 10:51:34.764372+00:00", "prepercent_6": "0.00642525870352983", "prepercent_7": "1.65597020895802e-06", "prepercent_3": "2.90006485492711e-09", "puser_id": "4", "prepercent_9": "6.7747981802313e-07"}', '{"prepercent_4": "6.9341922426247e-06", "prepercent_2": "0.505852341651917", "prepercent_1": "0.396681874990463", "prepercent_0": "0.0969242006540298", "purl": "/static/images/picture/4/2019130105146_3.png", "pstatus": "1", "preresult": "2", "id": "39", "_state": "<django.db.models.base.ModelState object at 0x7f653e8bdb00>", "prepercent_8": "8.15658211195114e-07", "pretime": "1.35", "prepercent_5": "4.90548409288749e-05", "pcreatetime": "2019-01-30 10:51:46.164684+00:00", "prepercent_6": "4.90092934342101e-05", "prepercent_7": "1.92844442636897e-08", "prepercent_3": "8.32870427984744e-05", "puser_id": "4", "prepercent_9": "0.000352392933564261"}', '{"prepercent_4": "0.219130918383598", "prepercent_2": "0.0198956541717052", "prepercent_1": "0.000236632025917061", "prepercent_0": "5.77401237933373e-07", "purl": "/static/images/picture/4/2019130105155_5.png", "pstatus": "1", "preresult": "6", "id": "40", "_state": "<django.db.models.base.ModelState object at 0x7f653e8bdb70>", "prepercent_8": "3.76778916688636e-05", "pretime": "1.35", "prepercent_5": "9.04000208024058e-10", "pcreatetime": "2019-01-30 10:51:55.703676+00:00", "prepercent_6": "0.757649838924408", "prepercent_7": "5.40819382877089e-06", "prepercent_3": "5.24946017321781e-06", "puser_id": "4", "prepercent_9": "0.00303804152645171"}', '{"prepercent_4": "2.03780126106778e-09", "prepercent_2": "0.999672055244446", "prepercent_1": "1.45071107904293e-10", "prepercent_0": "2.60383966992073e-12", "purl": "/static/images/picture/4/201913010526_0.png", "pstatus": "1", "preresult": "2", "id": "41", "_state": "<django.db.models.base.ModelState object at 0x7f653e8bdbe0>", "prepercent_8": "1.49057740372882e-07", "pretime": "1.13", "prepercent_5": "7.59813588047109e-07", "pcreatetime": "2019-01-30 10:52:06.417068+00:00", "prepercent_6": "6.84773158315943e-12", "prepercent_7": "9.38467837841017e-06", "prepercent_3": "4.66155152673009e-12", "puser_id": "4", "prepercent_9": "0.00031766842585057"}', '{"prepercent_4": "1.37929350785271e-06", "prepercent_2": "1.40414675442457e-08", "prepercent_1": "0.000621846644207835", "prepercent_0": "0.217709198594093", "purl": "/static/images/picture/4/2019130105219_9.png", "pstatus": "1", "preresult": "8", "id": "42", "_state": "<django.db.models.base.ModelState object at 0x7f653e8bdc50>", "prepercent_8": "0.778241157531738", "pretime": "1.14", "prepercent_5": "0.00161680299788713", "pcreatetime": "2019-01-30 10:52:19.940440+00:00", "prepercent_6": "0.00155578309204429", "prepercent_7": "1.51791607549967e-06", "prepercent_3": "0.000242550988332368", "puser_id": "4", "prepercent_9": "9.71256486081984e-06"}', '{"prepercent_4": "2.21549521484121e-06", "prepercent_2": "1.34124929900281e-05", "prepercent_1": "2.12652539630653e-05", "prepercent_0": "1.35032109938038e-06", "purl": "/static/images/picture/4/2019130105240_6.png", "pstatus": "1", "preresult": "3", "id": "43", "_state": "<django.db.models.base.ModelState object at 0x7f653e8bdcc0>", "prepercent_8": "0.00100935122463852", "pretime": "1.39", "prepercent_5": "1.85408945141408e-11", "pcreatetime": "2019-01-30 10:52:40.089372+00:00", "prepercent_6": "0.0013120073126629", "prepercent_7": "0.167832791805267", "prepercent_3": "0.82980751991272", "puser_id": "4", "prepercent_9": "4.48121788565459e-08"}', '{"prepercent_4": "0.000704434991348535", "prepercent_2": "3.36415354240671e-07", "prepercent_1": "1.14544185247922e-09", "prepercent_0": "1.67616548196747e-07", "purl": "/static/images/picture/4/2019130105250_9_1.png", "pstatus": "1", "preresult": "6", "id": "44", "_state": "<django.db.models.base.ModelState object at 0x7f653e8bdd30>", "prepercent_8": "9.75196940089518e-07", "pretime": "1.39", "prepercent_5": "0.0136971361935139", "pcreatetime": "2019-01-30 10:52:50.769811+00:00", "prepercent_6": "0.985596835613251", "prepercent_7": "1.28630828211129e-09", "prepercent_3": "6.12374861930221e-09", "puser_id": "4", "prepercent_9": "3.07777128227826e-08"}', '{"prepercent_4": "2.27748230940961e-07", "prepercent_2": "0.0148196145892143", "prepercent_1": "0.00214253808371723", "prepercent_0": "0.98176783323288", "purl": "/static/images/picture/4/201913010530_1.png", "pstatus": "1", "preresult": "0", "id": "45", "_state": "<django.db.models.base.ModelState object at 0x7f653e8bdda0>", "prepercent_8": "5.92800297738449e-08", "pretime": "1.16", "prepercent_5": "0.000209475139854476", "pcreatetime": "2019-01-30 10:53:00.465129+00:00", "prepercent_6": "1.28527644847054e-05", "prepercent_7": "0.00104657839983702", "prepercent_3": "8.05259787739487e-07", "puser_id": "4", "prepercent_9": "1.01782040573539e-08"}']

'''