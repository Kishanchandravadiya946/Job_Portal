from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    
    path('',views.first,name="first"),

    path('jobseeker/',views.home,name='home'),
    path('jobseeker/register',views.register,name='register'),
    path('jobseeker/profile/',views.profile,name='profile'),
    path('jobseeker/profile/update',views.updateprofile,name='update_profile'),
    
    # path('jobseeker/login/',auth_view.LoginView.as_view( redirect_field_name='next',
    #     success_url=settings.JOBSEEKER_LOGIN_REDIRECT_URL,
    #     template_name='job_seeker_login.html'),name='login'),
    path('jobseeker/login/',auth_view.LoginView.as_view(template_name='job_seeker_login.html'),name='login'),

    path('jobseeker/logout/',auth_view.LogoutView.as_view(template_name='job_seeker_logout.html'),name='logout'),
    path('jobseeker/searchjob/',views.searchjob,name='searchjob'),
    path('jobseeker/apply/<int:job_id>/', views.apply, name='apply'),
    path('jobseeker/applied_jobs/', views.applied_jobs, name='applied_jobs'),
    path('jobseeker/applied_jobs/withdraw/<application_id>/', views.withdraw, name='withdraw'),
   
    path('jobseeker/post/',views.post,name='post'),
    path('jobseeker/blogs/',views.blogs,name='blogs'),
    path('jobseeker/blogs/myblogs',views.my_blogs,name='my_blogs'),
    path('jobseeker/blogs/myblogs/delete/<int:blog_id>',views.delete_blog,name='delete_blog'),
    path('jobseeker/search/',views.search_profile,name='search_profile'),
    
  
    path('company/',views.companyhome,name='companyhome'),
    path('company/register/',views.companyregister,name='companyregister'),
    path('company/profile/',views.companyprofile,name='companyprofile'),
    path('company/profile/update',views.updatecompanyprofile,name='update_company_profile'),

    path('company/login/',views.companylogin,name='companylogin'),

    path('company/logout/',auth_view.LogoutView.as_view(template_name='company_logout.html'),name='companylogout'),
    path('company/createjob/',views.createjob,name='createjob'),
    path('company/jobs/', views.company_jobs, name='company_jobs'),
    path('company/jobs/delete_job/<int:job_id>', views.delete_job, name='delete_job'),
    path('company/jobs/<int:job_id>/applications/',views.view_applications,name='view_applications'),
    path('company/approve_application/<int:application_id>/<int:job_id>', views.approve_application, name='approve_application'),
    path('company/reject_application/<int:application_id>/<int:job_id>', views.reject_application, name='reject_application'),
    #change password
    path('jobseeker/change_password/',views.change_password,name='change_password'),
    path('company/change_password/',views.change_password,name='change_password')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



