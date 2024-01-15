from django.urls import path
from jobseeker import views

urlpatterns=[

    path("register/",views.SignupView.as_view(),name="signup"),
    path("signout/",views.SignoutView.as_view(),name="signout"),
    path("index/",views.StudentIndexView.as_view(),name="seeker-index"),
    path("profile/add/",views.ProfileCreateView.as_view(),name="profile-add"),
    path("profile/<int:pk>/",views.ProfileDetailView.as_view(),name="profile-detail"),
    path("profile/<int:pk>/change/",views.ProfileEditView.as_view(),name="profile-edit"),
    path("jobs/<int:pk>/detail/",views.JobDetailView.as_view(),name="job-detail"),
    path("jobs/<int:pk>/apply/",views.ApplyJobView.as_view(),name="job-apply"),
    path("applications/all/",views.ApplicationListView.as_view(),name="myapplications"),
    path("jobs/<int:pk>/save/",views.JobSaveView.as_view(),name="job-save"),
    path("jobs/saved/all/",views.SavedJobListView.as_view(),name="saved-jobs"),



]