from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo
# from django.core import validators
from FuturePlanning.models import c_Records,c_Familys

from django.forms import Textarea,CharField
from . import myconfig

FAMILY_CHOICES =[]

for fam in c_Familys.objects.all():
    FAMILY_CHOICES.append((fam,fam))

fam_1=c_Familys.objects.all()[0]
fam_2=c_Familys.objects.all()[1]


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')

# g_types_list=[("1","In"),("2","Exp"),("3","Savings"),("4","Loans")]
class NameForm(forms.Form):
    # your_name = forms.CharField(label='Your name', max_length=100)
    # Records_List = forms.CharField(initial='Records list',widget= forms.TextInput(attrs={'id':'Records_List_Jason','size':1000}))
    file = forms.FileField()

class FileForm(forms.Form):
    # your_name = forms.CharField(label='Your name', max_length=100)
    # Records_List = forms.CharField(initial='Records list',widget= forms.TextInput(attrs={'id':'Records_List_Jason','size':1000}))
    InputFile = forms.FileField(widget= forms.ClearableFileInput(attrs={'id':"selectExcelFIle",'onchange':"selectFileChanged()",'onclick':"selectFileclicked()",'style':"opacity:0"}))
    # InputFile = forms.FileField(widget= forms.ClearableFileInput(attrs={'style':"opacity:0;"}))





class DelC_Records(forms.Form):
    # Rec_Type = forms.CharField(max_length=3)
    # Rec_Type=forms.ChoiceField(choices = g_types_list,)
    Rec_Type=forms.ChoiceField(choices = myconfig.g_types_list,widget=forms.Select(attrs={'onchange':"myFunction1();"}))
    # Rec_Name = forms.CharField(max_length=50)

    Rec_Name = forms.IntegerField(widget=forms.Select(attrs={'onchange':"myFunction();"}))


    # widgets = {
    #     'Rec_Name': Textarea(attrs={'cols': 80, 'rows': 20,'onchange':"myFunction();"}),
    # }

class NewC_RecordForm(forms.ModelForm):

    class Meta():
        model = c_Records
        fields = '__all__'
        exclude = ('Family',)

class FamilyName(forms.Form):

    family_name = forms.ChoiceField(choices = FAMILY_CHOICES)


class Event_Purches_Appartmant(forms.Form):

    # Rec_Name = models.CharField(max_length=50,default='Name')
    Event_Name = forms.CharField(initial='Event_Name',widget= forms.TextInput(attrs={'id':'Event_Name','size':10}))
    Event_Cost = forms.IntegerField(initial=0,widget= forms.NumberInput(attrs={'id':'Event_Cost','style':"width:8em"}))
    Event_Date = forms.CharField(initial='07 2021',widget= forms.TextInput(attrs={'id':'Event_Date','size':10}))
    # Event_Update_DB = forms.BooleanField(required=False,widget= forms.CheckboxInput(attrs={'id':'Event_Save_Data','style':"width:7em"}))
    # Event_Balance = forms.IntegerField(initial=0,widget= forms.NumberInput(attrs={'id':'Event_Balance','style':"width:7em"}))
    Savings_At_Date = forms.IntegerField(initial=0,widget= forms.NumberInput(attrs={'id':'Event_Savings','style':"width:7em"}))
    Loans_At_Date = forms.IntegerField(initial=0,widget= forms.NumberInput(attrs={'id':'Event_Loans','style':"width:7em"}))
    Balance_At_Date = forms.IntegerField(initial=0,widget= forms.NumberInput(attrs={'id':'Event_Balance','style':"width:7em"}))

    Event_In_Start_Date = forms.CharField(initial='08 2021',widget= forms.TextInput(attrs={'id':'Event_In_Start_Date','style':"width:7em",'onchange':"EventInPost();"}))
    Event_In_End_Date = forms.CharField(initial='08 2022',widget= forms.TextInput(attrs={'id':'Event_In_End_Date','style':"width:7em",'onchange':"EventInPost();"}))
    Event_In_Monthly_Value = forms.IntegerField(initial=1000,widget= forms.NumberInput(attrs={'id':'Event_In_Value','style':"width:7em",'onchange':"EventInPost();"}))
    Event_In_Post_Data = forms.BooleanField(required=False,widget= forms.CheckboxInput(attrs={'id':'Event_In_Post','style':"width:7em",'onchange':"EventInPost();"}))

    Event_Exp_Start_Date = forms.CharField(initial='07 2021',widget= forms.TextInput(attrs={'id':'Event_Exp_Start_Date','style':"width:7em",'onchange':"EventExpPost();"}))
    Event_Exp_End_Date = forms.CharField(initial='07 2022',widget= forms.TextInput(attrs={'id':'Event_Exp_End_Date','style':"width:7em",'onchange':"EventExpPost();"}))
    Event_Exp_Monthly_Value = forms.IntegerField(initial=1000,widget= forms.NumberInput(attrs={'id':'Event_Exp_Value','style':"width:7em",'onchange':"EventExpPost();"}))
    Event_Exp_Post_Data = forms.BooleanField(required=False,widget= forms.CheckboxInput(attrs={'id':'Event_Exp_Post','style':"width:7em",'onchange':"EventExpPost();"}))
