from django.db import models

# 用户id表
class UserInfo(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    user_id = models.CharField(max_length=32,unique=True)
    pwd = models.CharField(max_length=32, default="abcdef")

    def __str__(self):
        return self.user_id


# 城市景点id-名称表
class CityInfo(models.Model):
    spot_id = models.IntegerField(unique=True)
    spot_name = models.CharField(max_length=32)
    intro = models.CharField(max_length=300,default="简介完善中……")

    def __str__(self):
        return self.spot_name


# 用户旅游过的城市记录表
class UserToCity(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    spot_id = models.ForeignKey(CityInfo, on_delete=models.CASCADE)
    rating = models.FloatField()
    timestamp = models.IntegerField()


# 图片存储
class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    city = models.ForeignKey(CityInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        # 在Python3中使用 def __str__(self):
        return self.name

