from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('1',views.index),
    path('2',views.create),
    path('3',views.Deposite),
    path('4',views.Payments),
    path('5',views.pin_generation,name='pin-generation'),
    path('6',views.about),


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)





# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)