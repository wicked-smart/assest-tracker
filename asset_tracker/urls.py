from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("asset_types/", views.asset_types, name="asset_types"),
    path("chartjs/", views.testing_chart, name="testing_chart"),
    path("asset_type_detail/<int:asset_type_id>", views.asset_types_detail, name="asset_type_detail"),
    path("asset_type_update/<int:asset_type_id>", views.assset_type_update, name="asset_type_update"),
    path("asset_type_add", views.asset_type_add, name="asset_type_add"),
    path("asset_type_delete/<int:asset_type_id>", views.asset_type_delete, name="asset_type_delete"),
    path("asset_delete/<int:asset_id>", views.asset_delete, name="asset_delete"),
    path("assets", views.assets, name="assets"),
    path("asset_add", views.asset_add, name="asset_add"),
    path("asset_detail/<int:asset_id>", views.asset_detail, name="asset_detail"),
    path('asset/download-csv', views.generate_csv, name='download_csv'),
    path("asset_update/<int:asset_id>", views.assset_update, name="asset_update")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


