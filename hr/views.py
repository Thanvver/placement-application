from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,CreateView,ListView,UpdateView,DeleteView,DetailView
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from myapp.models import Category,Jobs,StudentProfile,Applications
from hr.forms import LoginForm,CategoryForm,JobForm,JobChangeForm
from django.core.mail import send_mail
from django.conf import settings
from jobseeker.views import signin_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages

def admin_permission_required(fn):

    def wrapper(request,*args,**kwargs):
        if not request.user.is_superuser:
            messages.error(request,"admin permission required")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[admin_permission_required,signin_required,never_cache]


class SignInView(FormView):

    template_name="login.html"
    form_class=LoginForm


    def post(self,request,*args,**kwags):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                print("login succesfull")
                if request.user.is_superuser:
                    return redirect("index")
                else:
                    return redirect("seeker-index")
                
            print("failed to login")
            return render(request,"login.html",{"form":form})

@method_decorator(decs,name="dispatch")
class DashBoardView(TemplateView):

    template_name="index.html"

@method_decorator(decs,name="dispatch")
class SignoutView(View):

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

@method_decorator(decs,name="dispatch")
class CategoryListCeateView(CreateView,ListView):

    template_name="category.html"
    form_class=CategoryForm
    success_url=reverse_lazy("category")
    context_object_name="data"
    model=Category

@method_decorator(decs,name="dispatch")    
class CategoryDeleteView(View):
     
     def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Category.objects.filter(id=id).delete()
        return redirect("category")

@method_decorator(decs,name="dispatch")
class JobCreateView(CreateView):

    template_name="job_add.html"
    form_class=JobForm
    success_url=reverse_lazy("index")

@method_decorator(decs,name="dispatch")
class JobListView(ListView):

    template_name="job_list.html"
    context_object_name="jobs"
    model=Jobs

    def get(self,request,*args,**kwargs):

        qs=Jobs.objects.all()
        if "status" in request.GET:
            value=request.GET.get("status")
            qs=qs.filter(status=value)
        return render(request,self.template_name,{"jobs":qs})

@method_decorator(decs,name="dispatch")    
class JobDeleteView(View):

     def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Jobs.objects.filter(id=id).delete()
        return redirect("job-list")

@method_decorator(decs,name="dispatch")     
class JobUpdateView(UpdateView):

    form_class=JobChangeForm
    template_name="job_edit.html"
    model=Jobs
    success_url=reverse_lazy("index")

@method_decorator(decs,name="dispatch")
class JobApplicationListview(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        job_obj=Jobs.objects.get(id=id)
        qs=Applications.objects.filter(job=job_obj)
        return render(request,"applications.html",{"data":qs})

@method_decorator(decs,name="dispatch")
class AppllicationDetailView(DetailView):

    template_name="application_detail.html"
    context_object_name="application"
    model=Applications

@method_decorator(decs,name="dispatch")
class ApplicationUpdateView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        application_obj=Applications.objects.get(id=id)
        applicant_mail=application_obj.student.email
        value=request.POST.get("status")
        Applications.objects.filter(id=id).update(status=value)
        if value=="shortlisted":
             send_mail("your application status has been changed","your application status changed"
                  ,"mohdthanveer579@gmail.com"
                  ,["mohammedali12277@gmail.com"],
                  fail_silently=False)
        return redirect("index")