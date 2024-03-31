from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import Profile,CustomUser,CompanyProfile,Jobs,BlogPost
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class UserRegisterForm(forms.ModelForm):
    email= forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model= CustomUser
        fields=['username','email','password']
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.is_company = False  # Set is_company to False for user accounts
        if commit:
            user.save()
        return user

class CompanyRegisterForm(forms.ModelForm):  
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser  
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super(CompanyRegisterForm, self).save(commit=False)
        user.is_company = True  # Set is_company to True for company accounts
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['name','education','bio','contact','age','resume','gender','location','header','pic']

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model= CompanyProfile
        fields=['name','description','contact','location','pic']

class JobsForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields=['title','description','salary','jobtype','location','apply_by','req_skills']

class CompanyLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class JobSearchForm(forms.Form):
    title = forms.CharField(required=False)
    jobtype = forms.CharField(required=False)
    location = forms.CharField(required=False)
    # req_skill = forms.CharField(required=False)

# class ApplyForm(forms.Form):
#     pass
class BlogPostForm(forms.ModelForm):
    class Meta:
        model= BlogPost
        fields=['content','image']