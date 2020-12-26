from django.core.paginator import Paginator
from django.db.models.fields.files import FileField
from core.models import AdImage, AdVideo, Category, City, Ad, News, NewsImage, NewsVideo, SponsorContent
from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
import os.path
from os import path
from django.core.files import File


class ApiV1:
    def getCities(request):
        cities = City.objects.all()
        cityData = []
        for city in cities:
            cityData.append({
                'id': city.id,
                'name': city.name
            })

        data = {}
        data['result'] = "success"
        data['data'] = cityData

        return JsonResponse(data, safe=True)

    def getCategories(request):

        categoriesData = []
        for category in Category.objects.all():
            categoriesData.append({
                'id': category.id,
                'name': category.name,
                'iconUrl': category.icon.url,
            })

        data = {"result": "success", "data": categoriesData}
        return JsonResponse(data, safe=False)

    def getAds(request):
        isShare = request.GET.get('isShare', False) == 'True'
        adsCity = request.GET.get('city', None)
        adsCategory = request.GET.get('category', 'Все')
        pageNumber = int(request.GET.get('page', 0))
        itemsPerPage = 10

        ads = []
        if adsCategory != 'Все':
            ads = Ad.objects.all().order_by(
                '-timestamp').filter(category__name__contains=adsCategory).filter(is_share=isShare)
        else:
            ads = Ad.objects.all().order_by('-timestamp').filter(is_share=isShare)

        totalItems = ads.count()
        totalPages = max(totalItems // itemsPerPage, 1)
        totalPages = totalItems // itemsPerPage

        startIndex = pageNumber * itemsPerPage
        endIndex = min(startIndex + itemsPerPage, totalItems)

        ads = ads[startIndex:endIndex]

        adsData = []

        for ad in ads:
            adImages = AdImage.objects.filter(
                ad__id=ad.id
            )
            adImagesData = []
            for adImage in adImages:
                adImagesData.append({
                    "type": "image",
                    "position": adImage.position,
                    "imageUrl": adImage.image.url,
                })

            adVideos = AdVideo.objects.filter(
                ad__id=ad.id
            )
            adVideosData = []
            for adVideo in adVideos:
                adVideosData.append({
                    "type": "video",
                    "position": adVideo.position,
                    "videoUrl": adVideo.videoUrl,
                    "thumbnailUrl": adVideo.thumbnailUrl
                })

            adsData.append({
                'isShare': ad.is_share,
                'categoryName': ad.category.name,
                'description': ad.description,
                'phoneNumber': ad.phone_number,
                'isWhatsAppNumber': ad.is_whatsapp_number,
                'category': ad.category.name,
                'timestamp': ad.timestamp,
                'expireDate': ad.expire_date,
                'content': [*adImagesData, *adVideosData]
            })

        data = {
            "result": "success",
            "adsCity": adsCity,
            "adsCategory": adsCategory,
            "pageNumber": pageNumber,
            "minPage": 1,
            "maxPage": totalPages,
            "totalItems": totalItems,
            "data": adsData,
        }
        return JsonResponse(data, safe=True)

    def getNews(request):
        pageNumber = int(request.GET.get('page', 0))
        itemsPerPage = 10

        # TODO: pull only news that are not expired yet
        allNews = News.objects.all().order_by('-expire_date')
        totalItems = allNews.count()
        totalPages = max(totalItems // itemsPerPage, 1)
        totalPages = totalItems // itemsPerPage

        startIndex = pageNumber * itemsPerPage
        endIndex = min(startIndex + itemsPerPage, totalItems)

        allNews = allNews[startIndex:endIndex]

        adsData = []

        for news in allNews:
            adImages = NewsImage.objects.filter(
                news__id=news.id
            )
            adImagesData = []
            for adImage in adImages:
                adImagesData.append({
                    "type": "image",
                    "position": adImage.position,
                    "imageUrl": adImage.image.url,
                })

            adVideos = NewsVideo.objects.filter(
                news__id=news.id
            )
            adVideosData = []
            for adVideo in adVideos:
                adVideosData.append({
                    "type": "video",
                    "position": adVideo.position,
                    "videoUrl": adVideo.videoUrl,
                    "thumbnailUrl": adVideo.thumbnailUrl
                })

            adsData.append({
                'description': news.description,
                'expireDate': news.expire_date,
                'content': [*adImagesData, *adVideosData]
            })

        data = {
            "result": "success",
            "pageNumber": pageNumber,
            "minPage": 1,
            "maxPage": totalPages,
            "totalItems": totalItems,
            "data": adsData,
        }
        return JsonResponse(data, safe=True)

    def getSponsoredAds(request):
        pageNumber = 0
        itemsPerPage = 10
        # TODO: only show sponsored content
        sponsoredContents = SponsorContent.objects.all().order_by('-timestamp')

        data = {
            "result": "success",
            'data': [],
        }

        for sponsoredContent in sponsoredContents:
            sponsoredContentBannerImage = AdImage.objects.filter(
                ad__id=sponsoredContent.id).first()
            data['data'].append({
                'description': sponsoredContent.description,
                'sponsorName': sponsoredContent.sponsor_name,
                'redirectUrl': sponsoredContent.redirect_url,
                'bannerImage': sponsoredContentBannerImage.image.url,
            })

        return JsonResponse(data, safe=False)

    def prepopulateFromJson(request):
        canPrepopulateFromJson = True

        defaultCity, defaultCityCreated = City.objects.get_or_create(
            name="Кара-Балта")

        if canPrepopulateFromJson:
            import os
            from pathlib import Path
            BASE_DIR = Path(__file__).resolve().parent.parent

            fixture_file_path = os.path.join(BASE_DIR, 'karabalta_data.json')
            with open(fixture_file_path) as json_file:
                data = json.load(json_file)['data']

                for idx, categoryData in enumerate(data):
                    categoryName = categoryData['name']

                    category, categoryCreated = Category.objects.get_or_create(
                        name=categoryName)

                    for adData in categoryData['ads']:
                        ad, adCreated = Ad.objects.get_or_create(
                            description=adData['title'],
                            phone_number=adData['number'],
                            category=category,
                            expire_date=adData['date'].split(' ')[0],
                        )

                        if adCreated:
                            ad.regions.add(defaultCity)
                            ad.save()

                        # TODO: add images

                return JsonResponse({
                    'success': True,
                }, safe=True)

            # TODO: return response
            pass
        else:
            # TODO: return response (can do only in development mode)
            pass

    def prepopulateMedia(request):
        canPrepopulateMedia = True

        defaultCity, defaultCityCreated = City.objects.get_or_create(
            name="Кара-Балта")

        if canPrepopulateMedia:
            import os
            from pathlib import Path
            BASE_DIR = Path(__file__).resolve().parent.parent

            fixture_file_path = os.path.join(BASE_DIR, 'karabalta_data.json')
            with open(fixture_file_path) as json_file:
                data = json.load(json_file)['data']

                for idx, categoryData in enumerate(data):
                    if idx == 0:
                        continue

                    categoryName = categoryData['name']

                    category, categoryCreated = Category.objects.get_or_create(
                        name=categoryName)
                    iconUrl = categoryData['icon']

                    fileName = categoryName + '_' + \
                        iconUrl.split('/')[-1] + '.svg'

                    filePath = os.path.join(
                        BASE_DIR, 'tmp/media/icons/' + fileName)

                    # TODO: add category images
                    if not category.icon.name or not path.exists(filePath):
                        # TODO: download category image

                        r = requests.get(iconUrl)
                        open(filePath, 'wb').write(r.content)

                        category.icon.save(
                            fileName, File(open(filePath, 'rb')))

                    adsData = categoryData['ads']
                    for adData in adsData:
                        ad, adCreated = Ad.objects.get_or_create(
                            description=adData['title'],
                            phone_number=adData['number'],
                            category=category,
                            expire_date=adData['date'].split(' ')[0],
                        )

                        if adCreated:
                            ad.regions.add(defaultCity)
                            ad.save()

                        if len(adData['images_tag']) > 0:
                            for position, imageTag in enumerate(adData['images_tag']):

                                imageUrl = imageTag
                                # imageUrl = imagesTagPlacholder[position]

                                r = requests.get(
                                    imageUrl, allow_redirects=True)
                                contentType = r.headers['Content-Type']
                                imageFormat = contentType.split('/')[-1]

                                fileName = categoryName + '_' + \
                                    imageTag.split('/')[-1] + '.' + imageFormat

                                filePath = os.path.join(
                                    BASE_DIR, 'tmp/media/images/' + fileName)

                                if not path.exists(filePath):

                                    open(filePath, 'wb').write(r.content)
                                    adImage = AdImage(position=position, ad=ad)
                                    adImage.image.save(
                                        fileName, File(open(filePath, 'rb')))

                return JsonResponse({
                    'success': True,
                }, safe=True)

            # TODO: return response
            pass
        else:
            # TODO: return response (can do only in development mode)
            pass


def listing(request):
    contact_list = Ad.objects.all()
    paginator = Paginator(contact_list, 25)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})
