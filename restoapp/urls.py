from django.urls import path
from restoapp import views
from restaurant import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home',views.home),
    path('about',views.about),
    path('contact',views.contact),
    path('menu',views.menu),
    path('dishdetails/<did>',views.dish_details),
    path('viewcart',views.viewcart),
    path('register',views.register),
    path('login',views.ulogin),
    path('logout',views.ulogout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<did>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendusermail',views.sendusermail),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)