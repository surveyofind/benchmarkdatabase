
from django.urls import path
from.import views

urlpatterns = [
    path('',views.login_view,name='login'),
    path('signup',views.signup,name='signup'),
    path('gtstationdashboard',views.gtstationdashboard,name='gtstationdashboard'),
    path('gcpdashboard',views.gcpdashboard,name='gcpdashboard'),
    path('sbmdashboard',views.sbmdashboard,name='sbmdashboard'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('edit_gcpdata/<str:id>/',views.edit_gcpdata, name='edit_gcpdata'),
    path('edit_gtstationdata/<str:id>/',views.edit_gtstationdata, name='edit_gtstationdata'),
    path('edit_sbmdata/<str:id>/',views.edit_sbmdata, name='edit_sbmdata'),
     path('addsbm',views.addsbm, name='addsbm'),
    path('addgtstation',views.addgtstation, name='addgtstation'),
    path('admin_login',views.admin_login, name='admin_login'),
    path('admin_dashboard',views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboardgcpdata',views.admin_dashboardgcpdata, name='admin_dashboardgcpdata'),
    path('admin_dashboardSBMdata',views.admin_dashboardSBMdata, name='admin_dashboardSBMdata'),
    path('gcp_log',views.gcp_log, name='gcp_log'),
    path('gtstation_log',views.gtstation_log, name='gtstation_log'),
    path('sbm_log',views.sbm_log, name='sbm_log'),
    path('gtstationdownload_csv',views.gtstationdownload_csv, name='gtstationdownload_csv'),
    path('download_gcp_data_csv',views.download_gcp_data_csv, name='download_gcp_data_csv'),
    path('download_sbm_data_csv',views.download_sbm_data_csv, name='download_sbm_data_csv'),
    path('benchmark_sbmdata_download',views.benchmark_sbmdata_download, name='benchmark_sbmdata_download'),
    path('benchmark_gcpdata_download',views.benchmark_gcpdata_download, name='benchmark_gcpdata_download'),
    path('benchmark_gtstation_download',views.benchmark_gtstation_download, name='benchmark_gtstation_download'),
    
    
]
