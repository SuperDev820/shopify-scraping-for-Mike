from django.conf.urls import url 
from api import views 
 
urlpatterns = [ 
    # url(r'^api/scrap$', views.scrapOnWindow),
    # url(r'^api/scrap$', views.scrapOnLinux),
    url(r'^api/scrap$', views.scrapOnLinux),
]