from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout,authenticate
from .forms import UserRegisterForm, ProfileForm, CompanyRegisterForm,CompanyProfileForm,JobsForm,JobSearchForm,BlogPostForm
from django.urls import reverse
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Jobs,Application,Profile,BlogPost,CustomUser,CompanyProfile,Skill
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

def first(request):
   return render(request,'first.html')

#for jobseeker only
def home(request):
    if not request.user.is_authenticated or request.user.is_company:
        return redirect(reverse('login'))
    job_seekers_count = CustomUser.objects.filter(is_company=False).count()
    companies_count = CustomUser.objects.filter(is_company=True).count()

    context = {
        'job_seekers_count': job_seekers_count,
        'companies_count': companies_count
    }
    return render(request,'home.html',context)

#for jobseeker only
def register(request):
    if request.method=='POST':
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            messages.success(request,f'Hi {username}, your account is created successfully')
            login(request, user)
            return redirect('home')
    else:
        form= UserRegisterForm()
    return render(request,'job_seeker_register.html',{'form':form})

def profile(request):
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)  # Create the Profile instance but don't save it to the database yet
            profile.user = request.user
            form.save()
            return redirect('home')
    else:
        form=ProfileForm()
    return render(request,'job_seeker_profile.html',{'form':form})

def updateprofile(request):
    user_profile = Profile.objects.get(user=request.user)  # Assuming user is authenticated
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'update_profile.html', {'form': form})

#for company
def companyhome(request):
    if not request.user.is_authenticated or not request.user.is_company:
        return redirect(reverse('companylogin'))
    job_seekers_count = CustomUser.objects.filter(is_company=False).count()
    companies_count = CustomUser.objects.filter(is_company=True).count()

    context = {
        'job_seekers_count': job_seekers_count,
        'companies_count': companies_count
    }
    return render(request,'company_home.html',context)

#for company 
def companyregister(request):
    if request.method=='POST':
        form= CompanyRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            messages.success(request,f'Hi {username}, your account is created successfully')
            login(request, user)
            return redirect('companyhome')
    else:
        form= CompanyRegisterForm()
    return render(request,'company_register.html',{'form':form})

def companyprofile(request):
    
    if request.method=='POST':
        form=CompanyProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)  # Create the Profile instance but don't save it to the database yet
            profile.user = request.user
            form.save()
            return redirect('companyhome')
    else:
        form=CompanyProfileForm()
    return render(request,'company_profile.html',{'form':form})

def updatecompanyprofile(request):
    user_profile = CompanyProfile.objects.get(user=request.user)  # Assuming user is authenticated
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST,request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('companyprofile')
    else:
        form = CompanyProfileForm(instance=user_profile)
    return render(request, 'update_company_profile.html', {'form': form})

def createjob(request):
    if not request.user.is_authenticated or not request.user.is_company:
        return redirect(reverse('companylogin'))
    if request.method=='POST':
        form=JobsForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)  # Create the Profile instance but don't save it to the database yet
            job.user = request.user
            form.save()
            messages.success(request,f'Job is created successfully')
            return redirect('createjob')
    else:
        form=JobsForm()
    return render(request,'create_jobs.html',{'form':form})

# def updatejob(request):
#     if request.method=='POST':


from django.contrib.auth.views import LoginView
from .forms import CompanyLoginForm

class CompanyLoginView(LoginView):
    template_name = 'company_login.html'
    authentication_form = CompanyLoginForm

from django.contrib.auth import authenticate, login as auth_login
from .forms import CompanyLoginForm

def companylogin(request):
    if request.method == 'POST':
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('companyhome')
    else:
        form = CompanyLoginForm()
    return render(request, 'company_login.html', {'form': form})

def searchjob(request):
    jobs = Jobs.objects.all()  
    num_of_applicants={}
    for job in jobs:
        number = Application.objects.filter(job=job).count()
        num_of_applicants[job.id] = number

    form = JobSearchForm(request.POST or None)  
    if request.method == 'POST':
        form = JobSearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            jobtype = form.cleaned_data.get('jobtype')
            location = form.cleaned_data.get('location')
            req_skills = form.cleaned_data.get('req_skills')
            # skill = Skill.objects.get(name=req_skills)

            jobs = Jobs.objects.all()
            if title:
                jobs = jobs.filter(title__icontains=title)
            if jobtype:
                jobs = jobs.filter(jobtype__icontains=jobtype)
            if location:
                jobs = jobs.filter(location__icontains=location)
            if req_skills:
                jobs = jobs.filter(req_skills__name=req_skills)
                # jobs = Jobs.objects.filter(req_skills=skill)
                
            
    context = {
        'form': form,
        'jobs': jobs,
        'num_of_applicants': num_of_applicants
    }
    return render(request, 'find_jobs.html', context)


def apply(request, job_id):
    if request.method == 'POST':
        if not request.user.is_authenticated or request.user.is_company:
            return redirect(reverse('login'))
        if not hasattr(request.user, 'profile'):
            return redirect('profile')
        job = Jobs.objects.get(id=job_id)

        if Application.objects.filter(profile=request.user.profile, job=job).exists():
            messages.warning(request, 'You have already applied for this job.')
            return redirect('searchjob')
        profile = request.user.profile
        # job = Jobs.objects.get(id=job_id)

        application = Application(profile=profile, job=job)
        application.save()
        messages.success(request,f'Application submitted successfully')
        # return redirect('job_details', job_id=job_id)  # Redirect to the job details page
        return redirect('searchjob')
    else:
        return redirect(reverse('login'))

def company_jobs(request):
    company_jobs = Jobs.objects.filter(user=request.user)
    return render(request, 'company_jobs.html', {'company_jobs': company_jobs})

def delete_job(request, job_id):
    job = Jobs.objects.get(id=job_id)
    if job.user == request.user:
        job.delete()
    return redirect('company_jobs')

def view_applications(request,job_id):
    job = Jobs.objects.get(id=job_id)
    if job.user != request.user:
        return render(request, 'company_home.html')
    applications = Application.objects.filter(job=job)

    return render(request, 'view_applications.html', {'job': job, 'applications': applications})

def approve_application(request, application_id,job_id):
    application = Application.objects.get(id=application_id)
    application.approve()
    return redirect(reverse('view_applications',args=[job_id]))

def reject_application(request, application_id,job_id):
    application = Application.objects.get(id=application_id)
    application.reject()
    return redirect(reverse('view_applications', args=[job_id]))


#job seeker
def applied_jobs(request):
    user = request.user
    applications = Application.objects.filter(profile__user=user)
    return render(request, 'my_applications.html', {'applications': applications})

def withdraw(request,application_id):
    application=Application.objects.get(id=application_id)
    if application.profile.user == request.user:
        application.delete()
    return redirect('applied_jobs')

def post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST,request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request,f'Posted successfully!')
            return redirect('home')
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})

def blogs(request):
    blogs= BlogPost.objects.all().order_by('-created_at')
    context = {
        'blogs':blogs,
    }
    return render(request, 'view_blogs.html', context)

def my_blogs(request):
    blogs= BlogPost.objects.filter(author=request.user)
    return render(request,'myblogs.html',{'blogs':blogs})

def delete_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, pk=blog_id)
    blog.delete()
    return redirect('my_blogs')

def search_profile(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        # if search_query:
        
        profiles = CompanyProfile.objects.filter(name__icontains=search_query)
        # company = get_object_or_404(CustomUser, username=search_query)
        companies = CustomUser.objects.filter(username__icontains=search_query)
        if companies.exists():
            company=companies.first()
        else:
            messages.success(request,f'No such company found')
            return redirect('search_profile')
        jobs = Jobs.objects.filter(user=company) 
        return render(request, 'search_result.html', {'profiles': profiles, 'search_query': search_query , 'jobs': jobs})
        # else:
            # return render(request, 'no_results.html')
    else:
        return render(request, 'view_blogs.html')
    
#change password
def  change_password(request):
    if request.method=='POST':
        fm=PasswordChangeForm(user=request.user,data=request.POST)
        if  fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)
            # messages.success(request,'Your password change')
            if request.user.is_company:
                messages.success(request,'Your password has changed successfully FOR COMPANY')
                return redirect('companyhome')
            else:
                messages.success(request,'Your password has changed successfully FOR JOBSEECKER')
                return redirect('home')
    else:   
        fm=PasswordChangeForm(user=request.user)
    return render(request,'change_password.html',{'fm':fm})


