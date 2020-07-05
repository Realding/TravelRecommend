# for i in range(1, 105):
#     models.UserInfo.objects.create(user_id=str(i), pwd="123456")

# with open('F:\\DjangoServer\\TravelRecommend\\Django\\TravelRecommend\\spotId.csv', 'r') as myFile:
#     lines = csv.reader(myFile)
#     for line in lines:
#         if line[0] == 'spotId':
#             continue
#         models.CityInfo.objects.create(spot_id=int(line[0]), spot_name=line[1])
#         print(line)
#     with open('F:\\DjangoServer\\TravelRecommend\\Django\\TravelRecommend\\TrainSet_data.csv', 'r') as myFile:
#         lines = csv.reader(myFile)
#         for line in lines:
#             if line[0] == 'userId':
#                 continue
#             models.UserToCity.objects.create(
#                 user_id=models.UserInfo.objects.get(user_id=line[0]),
#                 spot_id=models.CityInfo.objects.get(spot_id=int(line[1])),
#                 rating=line[2], timestamp=line[3])
#             print(line)

# 删除 主键 >1982 的项
# models.UserToCity.objects.filter(pk__gt=1982).delete()

# list_dir = os.listdir("F:\\DjangoServer\\TravelRecommend\\Django\\media\\热门城市景点")
#     models.IMG.objects.all().delete()
#     for d in list_dir:
#         print(d)
#         city_obj = models.CityInfo.objects.get(spot_name=d)
#
#         # with open("F:\\热门城市景点\\"+d+"\\简介.txt", 'r') as f:
#         #     intro = f.read()
#         #     print(intro)
#         #     city_obj.intro = intro
#         #     city_obj.save()
#
#         pics = os.listdir("F:\\DjangoServer\\TravelRecommend\\Django\\media\\热门城市景点\\"+d)
#         for pic in pics:
#             if pic.endswith('.jpg'):
#                 print('yes')
#                 new_img = models.IMG(
#                     name=pic.rsplit('.', 1)[0],
#                     img="F:\\DjangoServer\\TravelRecommend\\Django\\media\\热门城市景点\\"+d+"\\"+pic,
#                     city=city_obj
#                 )
#                 new_img.save()
