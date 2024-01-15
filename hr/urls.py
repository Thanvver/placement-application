from django.urls import path
from hr import views

urlpatterns=[

    path("",views.SignInView.as_view(),name="signin"),
    path("index",views.DashBoardView.as_view(),name="index"),
    path("signout",views.SignoutView.as_view(),name="signout"),
    path("category",views.CategoryListCeateView.as_view(),name="category"),
    path("category/<int:pk>/remove/",views.CategoryDeleteView.as_view(),name="category-delete"),
    path("job/add",views.JobCreateView.as_view(),name="job-add"),
    path("job/list",views.JobListView.as_view(),name="job-list"),
    path("job/<int:pk>/remove/",views.JobDeleteView.as_view(),name="job-delete"),
    path("job/<int:pk>/change/",views.JobUpdateView.as_view(),name="job-edit"),
    path("job/<int:pk>/applications/",views.JobApplicationListview.as_view(),name="job-application"),
    path("applications/<int:pk>/",views.AppllicationDetailView.as_view(),name="application-detail"),
    path("applications/<int:pk>/change/",views.ApplicationUpdateView.as_view(),name="application-edit"),

]