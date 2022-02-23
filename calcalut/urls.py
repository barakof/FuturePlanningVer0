"""calcalut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from FuturePlanning import views
from django.conf.urls import url
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # path('',views.v_f_index,name="index"),
    # path('new_record/',views.v_f_new_c_record),
    # path('del_record/',views.v_f_del_c_record),
    # path('edit_record/',views.v_f_edit_c_record),
    # path('edit_record_data/',views.v_f_edit_c_record_data,name='edit_record_data'),
    # path(r'^FuturePlanning/',include('FuturePlanning.urls')),
    path('',include('FuturePlanning.urls')),
    path('admin/', admin.site.urls),
    # path(r'^formpage/',views.form_name_view,name='form_name'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
