from django.core.paginator import Paginator
from core.models import AdImage, AdVideo, Category, City, Ad
from django.shortcuts import render
from django.http import JsonResponse


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
            })

        data = {"result": "success", "data": categoriesData}
        return JsonResponse(data, safe=False)

    def getAds(request):
        adsCity = request.GET.get('city', 'Все')
        print(adsCity)

        adsCategory = request.GET.get('catgory', 'Все')
        pageNumber = request.GET.get('page', 1)

        # ads = Ad.objects.all()
        # .filter(
        #     regions__display_name=adsRegion
        # ).filter(
        #     category__title=adsCategory
        # )

        # TODO: add filter
        ads = Ad.objects.all().filter(category__name__contains=adsCity)

        paginator = Paginator(ads, 1)  # Show 25 contacts per page.
        page_number = request.GET.get('page', 1)

        # get_page seems more safe
        pageAds = paginator.get_page(page_number)

        # pageAds = paginator.page(page_number)

        adsData = []

        for ad in pageAds:
            adImages = AdImage.objects.filter(
                ad__id=ad.id
            )
            adImagesData = []
            for adVideo in adImages:
                adImagesData.append({
                    "type": "image",
                    "position": adVideo.position,
                    "imageUrl": adVideo.image.url,
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
                'description': ad.description,
                'phoneNumber': ad.phone_number,
                'category': ad.category.name,
                'content': [*adImagesData, *adVideosData]
            })

        data = {
            "result": "success",
            "adsCity": adsCity,
            "adsCategory": adsCategory,
            "pageNumber": pageNumber,
            "minPage": 1,
            "maxPage": paginator.num_pages,
            "totalItems": paginator.count,
            "data": adsData,
        }
        return JsonResponse(data, safe=False)

    def getSponsoredAds(request):
        data = [{"result": "TODO: return sponsored ads"}]
        return JsonResponse(data, safe=False)


def listing(request):
    contact_list = Ad.objects.all()
    paginator = Paginator(contact_list, 25)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})
