from api.views import ApiV1
from django.urls import path


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('v1/getCities', ApiV1.getCities, name='getCitiesV1'),
    path('v1/getCategories', ApiV1.getCategories, name="getCategoriesV1"),
    path('v1/getSponsoredAds', ApiV1.getSponsoredAds, name="getSponsoredAdsV1"),
    path('v1/prepopulateFromJson', ApiV1.prepopulateFromJson,
         name="prepopulateFromJsonV1"),
    path('v1/prepopulateMedia', ApiV1.prepopulateMedia,
         name="prepopulateMediaV1"),
    path('v1/getAds', ApiV1.getAds, name="getAdsV1"),
]
