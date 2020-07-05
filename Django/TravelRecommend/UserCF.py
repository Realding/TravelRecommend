# coding = utf-8

# 基于用户的协同过滤推荐算法实现
# import csv
# import sqlite3
import random
import math
from TravelRecommend import models
from operator import itemgetter


class UserBasedCF():
    # 初始化相关参数
    def __init__(self):
        # 找到与目标用户兴趣相似的20个用户，为其推荐10个旅游城市
        self.n_sim_user = 20
        self.n_rec_spot = 10

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}
        self.user_spot = {}

        # 用户相似度矩阵
        self.user_sim_matrix = {}
        self.spot_count = 0

        print('Similar user number = %d' % self.n_sim_user)
        print('Recommended spot number = %d' % self.n_rec_spot)

    # 读文件得到“用户-景点”数据
    def get_dataset(self, pivot=0.75):
        trainSet_len = 0
        testSet_len = 0

        for line_train in models.UserToCity.objects.all()\
                .values_list('user_id__user_id', 'spot_id__spot_id', 'rating', 'timestamp'):
            user, spot, rating, timestamp = line_train
            if user not in self.user_spot:
                self.user_spot[user] = [spot]
            else:
                self.user_spot[user].append(spot)

            self.trainSet.setdefault(user, {})
            self.trainSet[user][spot] = rating
            trainSet_len += 1

            if random.random() < 1-pivot:
                self.testSet.setdefault(user, {})
                self.testSet[user][spot] = rating
                testSet_len += 1

        print('Split trainingSet and testSet success!')
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)

    # 读文件，返回文件的每一行
    def load_file(self, filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:  # 去掉文件第一行的title
                    continue
                yield line.strip('\r\n')
        print('Load %s success!' % filename)

    # 计算用户之间的相似度
    def calc_user_sim(self):
        # 构建“景点-用户”倒排索引
        # key = spotID, value = list of userIDs who have seen this spot
        print('Building spot-user table ...')
        spot_user = {}
        for user, spots in self.trainSet.items():
            for spot in spots:
                if spot not in spot_user:
                    spot_user[spot] = set()
                spot_user[spot].add(user)
        print('Build spot-user table success!')

        self.spot_count = len(spot_user)
        print('Total spots number = %d' % self.spot_count)

        print('Build user co-rated spots matrix ...')
        for spot, users in spot_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {})
                    self.user_sim_matrix[u].setdefault(v, 0)
                    self.user_sim_matrix[u][v] += 1
        print('Build user co-rated spots matrix success!')

        # 计算相似性
        print('Calculating user similarity matrix ...')
        for u, related_users in self.user_sim_matrix.items():
            for v, count in related_users.items():
                self.user_sim_matrix[u][v] = count / math.sqrt(len(self.trainSet[u]) * len(self.trainSet[v]))
        print('Calculate user similarity matrix success!')

    # 针对目标用户U，找到其最相似的K个用户，产生N个推荐
    def recommend(self, user):
        K = self.n_sim_user
        N = self.n_rec_spot
        rank = {}
        watched_spots = self.trainSet[user]

        # v=similar user, wuv=similar factor
        for v, wuv in sorted(self.user_sim_matrix[user].items(), key=itemgetter(1), reverse=True)[0:K]:
            for spot in self.trainSet[v]:
                if spot in watched_spots:
                    continue
                rank.setdefault(spot, 0)
                rank[spot] += wuv
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]

    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self):
        print("Evaluation start ...")
        N = self.n_rec_spot
        # 准确率和召回率
        hit = 0
        rec_count = 0
        test_count = 0
        # 覆盖率
        all_rec_spots = set()

        for i, user, in enumerate(self.trainSet):
            test_spots = self.testSet.get(user, {})
            rec_spots = self.recommend(user)
            for spot, w in rec_spots:
                if spot in test_spots:
                    hit += 1
                all_rec_spots.add(spot)
            rec_count += N
            test_count += len(test_spots)

        precision = 1 - hit / (1.0 * rec_count)

        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_spots) / (1.0 * self.spot_count)
        print('precisioin=%.4f\trecall=%.4f\tcoverage=%.4f' % (precision, recall, coverage))

    # 根据用户id查询用户足迹，到过的城市
    @classmethod
    def my_route(cls, uid):

        user_cf = UserBasedCF()
        user_cf.get_dataset()
        user_cf.calc_user_sim()
        user_cf.evaluate()
        user_id = str(uid)
        city = []

        for spot_id in user_cf.user_spot[user_id]:
            obj = models.CityInfo.objects.get(spot_id=spot_id)
            city.append(obj.spot_name)

        return city

    # 根据推荐算法得出用户推荐城市
    @classmethod
    def user_recommend(cls, uid):

        user_cf = UserBasedCF()
        user_cf.get_dataset()
        user_cf.calc_user_sim()
        user_cf.evaluate()
        user_id = str(uid)
        city = []

        for result in user_cf.recommend(user_id):
            spot_id, pipe_idu = result
            obj = models.CityInfo.objects.get(spot_id=spot_id)
            city.append(obj.spot_name)

        return city

