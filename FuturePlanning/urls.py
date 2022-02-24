from django.conf.urls import url
from FuturePlanning import views
from django.urls import path


# SET THE NAMESPACE!
app_name = 'FuturePlanning'

urlpatterns = [

path('',views.v_f_index_new),
# path('',views.v_f_select_family),
path('home/',views.v_f_index_new,name="index"),
path('new_record/',views.v_f_new_c_record),
path('del_record/',views.v_f_del_c_record),
path('edit_record/',views.v_f_edit_c_record),
path('edit_record_data/',views.v_f_edit_c_record_data,name='edit_record_data'),
path('select_family/',views.v_f_select_family),
path('new_event/',views.v_f_new_event),
path('event_action/',views.v_f_event_action),
path('load_excel/',views.v_f_load_excel),
path('load_credit_xml/',views.v_f_load_credit_xml),
path('registration/',views.v_f_registration),
path('logout/',views.user_logout),
path('login/',views.user_login)


]
