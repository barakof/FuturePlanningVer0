from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
import os
import pandas as pd
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import *

from FuturePlanning.models import MySettings,c_Familys,c_Records
from FuturePlanning.forms import DelC_Records,NewC_RecordForm,FamilyName,Event_Purches_Appartmant,NameForm,FileForm,UserForm,UserProfileInfoForm
from . import myconfig
# import xmltodict
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import pandas_read_xml as pdx

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# create dataframe that its columns start from start date till end date
# add a raw with total to the df
def f_create_dataframe(Start,End):
    #create list of dates with date python object from
    #start to end date interval month
    dates_list = pd.date_range(Start, End, freq='MS').strftime('%m %Y')
    #create pandas data frame object with the list of dates and "Total" Row
    df = pd.DataFrame(columns = dates_list,  index = ['Total'])

    return df,dates_list
#######################################################################

def f_create_balance_dataframe(Start,End,TotalBalance):
    dates_list = pd.date_range(Start, End, freq='MS').strftime('%m %Y')
    df = pd.DataFrame(columns = dates_list,index = ['Total'])

    i=0
    for month in dates_list:
        df[month]["Total"] = TotalBalance[i]
        i=i+1
    return df

def f_build_df_from_db(Rec_Type,Current_Family,Table_Month_List,In_Df,Simulate_Dic):

    total_for_loan=0
    # print("inside build df",Simulate_Dic)
    # if dic is not empty,it also means the function was called for sim values
    if(Simulate_Dic):
        Fam=c_Familys.objects.get_or_create(Fam_name=g_current_family[0].Fam_name)[0]
        # it will be deketed at the end of the function because its simulated
        # print("build df:save rec")
        c_Records.objects.create(Family=Fam,Rec_Type=Rec_Type,
                                        Rec_Name=Simulate_Dic["Rec_Name"],
                                        Start_Date=Simulate_Dic["Start_Date"],
                                        End_Date=Simulate_Dic["End_Date"],
                                        Value=Simulate_Dic["Value"])

    family_in_records=c_Records.objects.all().filter(Family__Fam_name=Current_Family).filter(Rec_Type=Rec_Type)

    for elemnt in family_in_records:

        data_dates = pd.date_range(elemnt.Start_Date, elemnt.End_Date, freq='MS').strftime('%m %Y').tolist()

        value_list=[]
        for month in Table_Month_List:
            if month in data_dates:
                value_list.append(int(elemnt.Value))
                total_for_loan=total_for_loan + int(elemnt.Value)
            else:
                value_list.append(0)
        index_length=(len(In_Df))
        line = pd.DataFrame({},index=[elemnt.Rec_Name])
        In_Df = pd.concat([In_Df.iloc[:index_length-1], line, In_Df.iloc[index_length-1:]])

        if (Rec_Type == "3"):
            value_list=[]
            j=0
            for month in Table_Month_List:
                if month in data_dates:
                    if j==0:
                        value_list.append(round(elemnt.Value+elemnt.Start_Value))
                    else:
                        value_list.append(round(value_list[-1]*(1+elemnt.Rate/12/100)+int(elemnt.Value)))
                    j=1
                else:
                    if(j>0):
                        value_list.append(value_list[-1])
                    else:
                        value_list.append(0)

        if (Rec_Type == "4"):
            value_list=[]
            i=0
            j=0
            for month in Table_Month_List:
                if month in data_dates:
                    if j==0:
                        value_list.append(int(total_for_loan-elemnt.Value))
                    else:
                        value_list.append(value_list[i-1]-elemnt.Value)
                    j=j+1
                else:
                    value_list.append(0)
            total_for_loan=0
        i=0
        for month in Table_Month_List:
            In_Df[month][elemnt.Rec_Name]=value_list[i]
            i=i+1
            x=In_Df[:-1][month].sum()
            In_Df[month]["Total"] = x
    # if dic is not empty,it also means the function was called for sim values delete sim rec
    if(Simulate_Dic):
        sim_family_in_records=c_Records.objects.all().filter(Family__Fam_name=Current_Family).filter(Rec_Type=Rec_Type).filter(Rec_Name=Simulate_Dic["Rec_Name"])
        # print("build df:del rec")
        sim_family_in_records[0].delete()
    return In_Df
#****************************************************************************
g_record_to_edit=c_Records.objects.all()
#Global Variable to hold the start date of the simulation
g_start=""
#Global Variable to hold the end date of the simulation
g_end=""
#Read from DB the setting parameters per version request

g_my_settings = MySettings.objects.all().filter(simulation_version=1)[0]

#Set the global variable for the start and end of the simulation based on the settings

g_start=g_my_settings.simulation_start_date

g_end=g_my_settings.simulation_end_date

# g_current_family=c_Familys.objects.all().filter(Fam_name="Ofir")g_usernameforfamily

g_current_family=c_Familys.objects.all()

g_usernameforfamily=""

def v_f_event_action(request):

    return render(request,'FuturePlanning/v_f_select_family.html',{})

def f_get_active_family(request):


    if request.user.is_authenticated:

        logIn_family_q = c_Familys.objects.all().filter(Fam_name=request.user.username)

        if (logIn_family_q.count() != 0):
            logIn_family = logIn_family_q[0]
        else:
            logIn_family = c_Familys.objects.all().filter(Fam_name="Example")[0]
    else:
        logIn_family = c_Familys.objects.all().filter(Fam_name="Example")[0]

    return(logIn_family,logIn_family.Fam_name)


# def v_f_index(request):
#
#     logIn_family_obj,logIn_family_str = f_get_active_family(request)
#     print("log f string:",logIn_family_str)
#
#
#     incomes_records_in_family =c_Records.objects.all().filter(Family__Fam_name=logIn_family_str).filter(Rec_Type='1')
#     incomes_records_list = list(incomes_records_in_family.values())
#
#     expanses_records_in_family =c_Records.objects.all().filter(Family__Fam_name=logIn_family_str).filter(Rec_Type='2')
#     expanses_records_list = list(expanses_records_in_family.values())
#
#     savings_records_in_family =c_Records.objects.all().filter(Family__Fam_name=logIn_family_str).filter(Rec_Type='3')
#     savings_records_list = list(savings_records_in_family.values())
#
#     loans_records_in_family =c_Records.objects.all().filter(Family__Fam_name=logIn_family_str).filter(Rec_Type='4')
#     loans_records_list = list(loans_records_in_family.values())
#
#     #Create an empty adataframe object for the incomes and return df and month list
#     (g_income_table_df,g_table_month_list) = f_create_dataframe(g_start,g_end)
#
#     #Create an empty adataframe object for the Expanse and return df and month list
#     (g_expanse_table_df,g_table_month_list) = f_create_dataframe(g_start,g_end)
#
#     #Create an empty adataframe object for the savings and return df and month list
#     (g_savings_table_df,g_table_month_list) = f_create_dataframe(g_start,g_end)
#
#     #Create an empty adataframe object for the loans and return df and month list
#     (g_loans_table_df,g_table_month_list) = f_create_dataframe(g_start,g_end)
#
#     # build income df from db records for incomes
#     df_in=f_build_df_from_db(myconfig.g_types_list[0][0],logIn_family_str,g_table_month_list,g_income_table_df,{})
#     # print("views df_in: ",df_in)
#     # build expanse df from db records for expanses
#     df_exp=f_build_df_from_db(myconfig.g_types_list[1][0],logIn_family_str,g_table_month_list,g_expanse_table_df,{})
#
# ###########################################################################
#     rowTotalIncome = df_in.loc["Total"]
#     rowTotalExp = df_exp.loc["Total"]
#     MonthBalance = rowTotalIncome - rowTotalExp
#     TotalBalance=[]
#     TotalBalance.append(MonthBalance[0])
#     index=1
#     for i in range(len(MonthBalance)-1):
#         TotalBalance.append(TotalBalance[index-1]+MonthBalance[index])
#         index=index+1
#     df_balance = f_create_balance_dataframe(g_start,g_end,TotalBalance)
# ###########################################################################
#
#     # build savings df from db records for savings
#     df_save=f_build_df_from_db(myconfig.g_types_list[2][0],logIn_family_str,g_table_month_list,g_savings_table_df,{})
#     # print("views df_save: ",df_save)
#     # build loans df from db records for loans
#     df_loan=f_build_df_from_db(myconfig.g_types_list[3][0],logIn_family_str,g_table_month_list,g_loans_table_df,{})
#     # print("views df_loan: ",df_loan)
#     #transfer in comes df to html string
#     income_table_string = df_in.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tInTable")
#
#     #transfer expanse df to html string
#     expanse_table_string = df_exp.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tExpTable")
#
#     #transfer savings df to html string
#     savings_table_string = df_save.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tSaveTable")
#
#     #transfer expanse df to html string
#     loans_table_string = df_loan.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tLoanTable")
#
#     balance_table_string = df_balance.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tBalanceTable")
#
#     in_index_length=(len(df_in))
#
#
#     exp_index_length=(len(df_exp))
#     save_index_length=(len(df_save))
#     loan_index_length=(len(df_loan))
#     balance_index_length=(len(df_balance))
#
#     dates_list_plotly = pd.date_range(g_start, g_end, freq='MS').strftime('%Y-%m').tolist()
#
#     my_dict = {'InTable':income_table_string,
#                'ExpTable':expanse_table_string,
#                'SaveTable':savings_table_string,
#                'LoanTable':loans_table_string,
#                'BalanceTable':balance_table_string,
#
#
#                'IncomeYAxies':df_in.iloc[in_index_length-1].tolist(),
#                'IncomeXAxies':dates_list_plotly,
#                'ExpYAxies':df_exp.iloc[exp_index_length-1].tolist(),
#                'ExpXAxies':dates_list_plotly,
#
#                'SavingsYAxies':df_save.iloc[save_index_length-1].tolist(),
#                'SavingsXAxies':dates_list_plotly,
#                'LoansYAxies':df_loan.iloc[loan_index_length-1].tolist(),
#                'LoansXAxies':dates_list_plotly,
#
#                'BalanceYAxies':df_balance.iloc[balance_index_length-1].tolist(),
#                'BalanceXAxies':dates_list_plotly,
#
#                'family':logIn_family_str,
#                # g_current_family[0].Fam_name
#
#                'SavingsRecordList':savings_records_list,
#                'LoansRecordList':loans_records_list,
#
#                'IncomesRecordList': incomes_records_list,
#                'ExpansesRecordList': expanses_records_list,
#
#
#                }
#     return render(request,'FuturePlanning/v_f_index.html',context=my_dict)
def v_f_index_new(request):

    logIn_family_obj,logIn_family_str = f_get_active_family(request)

    incomes_records_in_family =c_Records.objects.all().filter(Family__Fam_name=logIn_family_str).filter(Rec_Type='1')
    incomes_records_list = list(incomes_records_in_family.values())
    expanses_records_in_family =c_Records.objects.all().filter(Family__Fam_name=logIn_family_str).filter(Rec_Type='2')
    expanses_records_list = list(expanses_records_in_family.values())
    savings_records_in_family =c_Records.objects.all().filter(Family__Fam_name=logIn_family_str).filter(Rec_Type='3')
    savings_records_list = list(savings_records_in_family.values())
    loans_records_in_family =c_Records.objects.all().filter(Family__Fam_name=logIn_family_str).filter(Rec_Type='4')
    loans_records_list = list(loans_records_in_family.values())

    dates_list_plotly = pd.date_range(g_start, g_end, freq='MS').strftime('%Y-%m').tolist()

    my_dict = {

               # 'IncomeYAxies':df_in.iloc[in_index_length-1].tolist(),
               'IncomeXAxies':dates_list_plotly,
               # 'ExpYAxies':df_exp.iloc[exp_index_length-1].tolist(),
               'ExpXAxies':dates_list_plotly,

               # 'SavingsYAxies':df_save.iloc[save_index_length-1].tolist(),
               'SavingsXAxies':dates_list_plotly,
               # 'LoansYAxies':df_loan.iloc[loan_index_length-1].tolist(),
               'LoansXAxies':dates_list_plotly,

               # 'BalanceYAxies':df_balance.iloc[balance_index_length-1].tolist(),
               'BalanceXAxies':dates_list_plotly,

               'family':logIn_family_str,

               'SavingsRecordList':savings_records_list,
               'LoansRecordList':loans_records_list,

               'IncomesRecordList': incomes_records_list,
               'ExpansesRecordList': expanses_records_list,
               }
    return render(request,'FuturePlanning/v_f_index_new.html',context=my_dict)

def v_f_select_family(request):
    global g_current_family
    form = FamilyName()
    # print("select family form:",form)
    if request.method == 'POST':
        form = FamilyName(request.POST)

        if form.is_valid():


            g_current_family=c_Familys.objects.all().filter(Fam_name=form.cleaned_data['family_name'])
            # g_current_family=c_Familys.objects.all().filter(Fam_name="Ofir")
            return redirect("FuturePlanning:index")


    return render(request,'FuturePlanning/v_f_select_family.html',{'form':form})

def v_f_load_credit_xml(request):

    g_load_credit_state = 0
    l_fileForm = FileForm()
    PythonBackToJsData={}

    logIn_family_obj,logIn_family_str = f_get_active_family(request)

    if request.method == "POST":

        if  ("LoadXmlFile" in request.POST):
            print("load form post")
            l_fileForm = FileForm(request.POST, request.FILES)

            if l_fileForm.is_valid():

                upload_file=request.FILES['InputFile']

                filename, file_extension = os.path.splitext(upload_file.name)
                print("fe",file_extension)

                if (  (file_extension != ".xml") ):
                    #  or (file_extension != ".xls") )
                    print("error file type")
                    g_load_credit_state=9
                else:

                    myfiledata=upload_file.read()
                    mystr=myfiledata.decode("UTF-8")
                    df = pdx.read_xml(mystr)
                    PythonBackToJsData=df.to_json()
                    # print("jason",PythonBackToJsData)
                    g_load_credit_state=1

        if  ("SaveRecords" in request.POST):
            print("save records")
            # python dictionary of records to save, got a json form js
            res = json.loads(request.POST['Records_List'])
            # print(request.POST['Records_List'])
            for key in res:
                sFamily=logIn_family_obj
                sType=res[key]["Rec_Type"]
                sName=res[key]["Rec_Name"]
                sStartDate=res[key]["Start_Date"]
                sEndDate=res[key]["End_Date"]
                sValue=res[key]["Value"]

                c_Records.objects.get_or_create(Family=sFamily,Rec_Type=sType,Rec_Name=sName,Start_Date=sStartDate,End_Date=sEndDate,Value=sValue)
                print(sFamily,sType,sName,sStartDate,sEndDate,sValue)
            return redirect("FuturePlanning:index")

    my_dict = {
                'g_start_date':g_start,
                'g_end_date':g_end,
                'CreditLoadingForm':l_fileForm,
                'state':g_load_credit_state,
                'XmlInJsonFormat':PythonBackToJsData,
                'family':logIn_family_str
                }

    return render(request,'FuturePlanning/v_f_load_credit_xml.html', context=my_dict)


def v_f_load_excel(request):

    g_load_excel_state = 0
    l_fileForm = FileForm()
    ExcelDfStringHtmlTable="no xls file"


    logIn_family_obj,logIn_family_str = f_get_active_family(request)

    if request.method == "POST":

        if  ("SaveOsIncomesExpanses" in request.POST):
            g_load_excel_state=0
            print("save xls form post")
            # print("expanses:",request.POST["ExpansesAverage"])
            # print("Incomes:",request.POST["IncomeAverage"])
            res = json.loads(request.POST['Os_Records_List'])
            for key in res:
                # sFamily=current_family=g_current_family[0]
                sFamily=logIn_family_obj
                print("family:",sFamily)
                sType=res[key]["Rec_Type"]
                sName=res[key]["Rec_Name"]
                sStartDate=res[key]["Start_Date"]
                sEndDate=res[key]["End_Date"]
                sValue=res[key]["Value"]
                print("key:",res[key])
                c_Records.objects.get_or_create(Family=sFamily,Rec_Type=sType,Rec_Name=sName,Start_Date=sStartDate,End_Date=sEndDate,Value=sValue)
            return redirect("FuturePlanning:index")

        if  ("LoadXlsFile" in request.POST):

            print("load xls form post")
            ExcelForm = FileForm(request.POST, request.FILES)
            if ExcelForm.is_valid():
                upload_file=request.FILES['InputFile']
                filename, file_extension = os.path.splitext(upload_file.name)
                print("fe",file_extension)

                if (  (file_extension != ".xlsx") and (file_extension != ".xls") ):
                    #  or (file_extension != ".xls") )
                    print("error file type")
                    g_load_excel_state=9
                else:
                    print("good file type")
                    g_load_excel_state=1
                    myfiledata=upload_file.read()
                    # support files xls, xlsx, xlsm, xlsb, odf, ods and odt
                    ExcelDf=pd.read_excel(myfiledata)
                    ExcelDf = ExcelDf[ExcelDf.columns[::-1]]
                    # xlsDfStringHtmlTable = xlsDf.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tXlsTable")
                    ExcelDfStringHtmlTable = ExcelDf.to_html(classes="table-bordered table-striped table-responsivek",table_id="tXlsTable")
                    # print(type (xlsDfStringHtmlTable),xlsDfStringHtmlTable)
                    ExcelDfStringHtmlTable = ExcelDfStringHtmlTable.replace("NaN","")
                    ExcelDfStringHtmlTable = ExcelDfStringHtmlTable.replace("Unnamed:","")
                    # print(xlsDfStringHtmlTable)

    my_dict = {
                'g_start_date':g_start,
                'g_end_date':g_end,
                'xlsTableHtml':ExcelDfStringHtmlTable,
                'ExcelLoadingForm':l_fileForm,
                'family':logIn_family_str,
                'state':g_load_excel_state
                }


    return render(request,'FuturePlanning/v_f_load_excel.html', context=my_dict)


def v_f_new_c_record(request):

    logIn_family_obj,logIn_family_str = f_get_active_family(request)


    error_list=[]
    # PythonBackToJsData={}
    # PythonSavingsBackToJsData={}
    # xlsDfStringHtmlTable="no xls file"
    form = NewC_RecordForm()
    # Xmlform = NameForm()
    # XmlSavingForm = NameForm()
    if request.method == "POST":

        if  ("AddRecord" in request.POST):
            print("Add Record post")
            form = NewC_RecordForm(request.POST)
            if form.is_valid():
                current_family=logIn_family_str
                record_type=form.cleaned_data['Rec_Type']
                records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=record_type)
                name_list=[]
                for element in records_list:
                    name_list.append(element.Rec_Name)
                if (form.cleaned_data['Rec_Name'] not in name_list):
                    print(form.cleaned_data)
                    sFamily=logIn_family_obj
                    sType=form.cleaned_data["Rec_Type"]
                    sName=form.cleaned_data['Rec_Name']
                    sStartDate=form.cleaned_data["Start_Date"]
                    sEndDate=form.cleaned_data["End_Date"]
                    sValue=form.cleaned_data["Value"]
                    c_Records.objects.get_or_create(Family=sFamily,Rec_Type=sType,Rec_Name=sName,Start_Date=sStartDate,End_Date=sEndDate,Value=sValue)
                    # form.save(commit=True)
                    return redirect("FuturePlanning:index")
                else:
                    error_list.append("record name already exist in DB")
            else:
                error_list.append("for not valid")
    # print("xxx:",xlsDfStringHtmlTable)
    return render(request,'FuturePlanning/v_f_new_c_record.html',{'c_record_form':form,'erros':error_list,'family':logIn_family_str})

def v_f_del_c_record(request):

    logIn_family_obj,logIn_family_str = f_get_active_family(request)

    error_list=[]
    form = DelC_Records()
    current_family=logIn_family_str

    records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=myconfig.g_types_list[0][0])
    in_name_list=[]
    for element in records_list:
        in_name_list.append(element.Rec_Name)

    records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=myconfig.g_types_list[1][0])
    exp_name_list=[]
    for element in records_list:
        exp_name_list.append(element.Rec_Name)

    records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=myconfig.g_types_list[2][0])
    save_name_list=[]
    for element in records_list:
        save_name_list.append(element.Rec_Name)

    records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=myconfig.g_types_list[3][0])
    loan_name_list=[]
    for element in records_list:
        loan_name_list.append(element.Rec_Name)



    if request.method == "POST":
        # print("in post del",request.POST)
        form = DelC_Records(request.POST)

        if form.is_valid():
            current_family=logIn_family_str

            record_type=form.cleaned_data['Rec_Type']
            if (record_type == myconfig.g_types_list[0][0]) :
                record_name=in_name_list[form.cleaned_data['Rec_Name']]
            if (record_type == myconfig.g_types_list[1][0]):
                record_name=exp_name_list[form.cleaned_data['Rec_Name']]
            if (record_type == myconfig.g_types_list[2][0]):
                record_name=save_name_list[form.cleaned_data['Rec_Name']]
            if (record_type == myconfig.g_types_list[3][0]):
                record_name=loan_name_list[form.cleaned_data['Rec_Name']]
            # print(record_name)
            record_to_delete=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=record_type).filter(Rec_Name=record_name)
            if len(record_to_delete)==1:
                record_to_delete[0].delete()
                return redirect("FuturePlanning:index")
                # return index(request)
            else:
                if len(record_to_delete)==0:
                    error_list.append("no record found")
                else:
                    if len(record_to_delete)>1:
                        error_list.append("There is more then one record with this name, contact admin")
                    else:
                        error_list.append("fatak error, contact admin")

        else:
            print('ERROR FORM INVALID')

    my_dict = {
                'del_c_record_form':form,
                'erros':error_list,
                'Indata':in_name_list,
                'Expdata':exp_name_list,
                'Savedata':save_name_list,
                'Loandata':loan_name_list,

                'family':logIn_family_str
                }


    return render(request,'FuturePlanning/v_f_del_c_record.html',context=my_dict)

def v_f_edit_c_record(request):
        global g_record_to_edit

        logIn_family_obj,logIn_family_str = f_get_active_family(request)

        error_list=[]
        form = DelC_Records()
        current_family=logIn_family_str

        records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=myconfig.g_types_list[0][0])
        in_name_list=[]
        for element in records_list:
            in_name_list.append(element.Rec_Name)

        records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=myconfig.g_types_list[1][0])
        exp_name_list=[]
        for element in records_list:
            exp_name_list.append(element.Rec_Name)

        records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=myconfig.g_types_list[2][0])
        save_name_list=[]
        for element in records_list:
            save_name_list.append(element.Rec_Name)

        records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=myconfig.g_types_list[3][0])
        loan_name_list=[]
        for element in records_list:
            loan_name_list.append(element.Rec_Name)

        if request.method == "POST":

            form = DelC_Records(request.POST)
            if form.is_valid():
                current_family=logIn_family_str

                record_type=form.cleaned_data['Rec_Type']
                if (record_type == myconfig.g_types_list[0][0]) :
                    record_name=in_name_list[form.cleaned_data['Rec_Name']]
                if (record_type == myconfig.g_types_list[1][0]):
                    record_name=exp_name_list[form.cleaned_data['Rec_Name']]

                if (record_type == myconfig.g_types_list[2][0]) :
                    record_name=save_name_list[form.cleaned_data['Rec_Name']]
                if (record_type == myconfig.g_types_list[3][0]):
                    record_name=loan_name_list[form.cleaned_data['Rec_Name']]



                g_record_to_edit=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=record_type).filter(Rec_Name=record_name)
                return redirect("FuturePlanning:edit_record_data")


                # print("4",request.POST)
            else:
                # print("5",request.POST)
                error_list.append("no record found")

        # print("6",request.POST)
        return render(request,'FuturePlanning/v_f_edit_c_record.html',{'del_c_record_form':form,'erros':error_list,'Indata':in_name_list,'Expdata':exp_name_list,'Savedata':save_name_list,'Loandata':loan_name_list,'family':logIn_family_str })


def v_f_edit_c_record_data(request):
    global g_record_to_edit

    logIn_family_obj,logIn_family_str = f_get_active_family(request)
    # print("in record data")
    error_list=[]
    form = NewC_RecordForm(instance=g_record_to_edit[0])
    if request.method == "POST":
        form = NewC_RecordForm(request.POST)
        if form.is_valid():
            print("clean:",form.cleaned_data)
            g_record_to_edit.delete()

            # ######################
            sFamily=logIn_family_obj
            sType=form.cleaned_data["Rec_Type"]
            sName=form.cleaned_data['Rec_Name']
            sStartDate=form.cleaned_data["Start_Date"]
            sEndDate=form.cleaned_data["End_Date"]
            sValue=form.cleaned_data["Value"]
            c_Records.objects.get_or_create(Family=sFamily,Rec_Type=sType,Rec_Name=sName,Start_Date=sStartDate,End_Date=sEndDate,Value=sValue)
            ########################

            return redirect("FuturePlanning:index")
        else:
                error_list.append("error saving new data")

    return render(request,'FuturePlanning/v_f_new_c_record_edit.html',{'c_record_form':form,'erros':error_list,'family':g_current_family[0].Fam_name})

# ***************************************************************
# ***************************************************************
# ***************************************************************
# ***************************************************************

def v_f_new_event(request):

    # form = NameForm()
    print("get req")

    global g_current_family

    logIn_family_obj,logIn_family_str = f_get_active_family(request)

    incomes_records_in_family =c_Records.objects.all().filter(Family__Fam_name=logIn_family_str).filter(Rec_Type='1')
    incomes_records_list = list(incomes_records_in_family.values())

    expanses_records_in_family =c_Records.objects.all().filter(Family__Fam_name=logIn_family_str).filter(Rec_Type='2')
    expanses_records_list = list(expanses_records_in_family.values())

    savings_records_in_family =c_Records.objects.all().filter(Family__Fam_name=logIn_family_str).filter(Rec_Type='3')
    savings_records_list = list(savings_records_in_family.values())

    loans_records_in_family =c_Records.objects.all().filter(Family__Fam_name=logIn_family_str).filter(Rec_Type='4')
    loans_records_list = list(loans_records_in_family.values())

#     #Create an empty adataframe object for the incomes and return df and month list
#     (g_income_table_df,g_table_month_list) = f_create_dataframe(g_start,g_end)
#
#     #Create an empty adataframe object for the Expanse and return df and month list
#     (g_expanse_table_df,g_table_month_list) = f_create_dataframe(g_start,g_end)
#
#     #Create an empty adataframe object for the savings and return df and month list
#     (g_savings_table_df,g_table_month_list) = f_create_dataframe(g_start,g_end)
#
#     #Create an empty adataframe object for the loans and return df and month list
#     (g_loans_table_df,g_table_month_list) = f_create_dataframe(g_start,g_end)
#
#     # build income df from db records for incomes
#     df_in=f_build_df_from_db(myconfig.g_types_list[0][0],logIn_family_str,g_table_month_list,g_income_table_df,{})
#     # print("views df_in: ",df_in)
#     # build expanse df from db records for expanses
#     df_exp=f_build_df_from_db(myconfig.g_types_list[1][0],logIn_family_str,g_table_month_list,g_expanse_table_df,{})
#
# ###########################################################################
#     rowTotalIncome = df_in.loc["Total"]
#     rowTotalExp = df_exp.loc["Total"]
#     MonthBalance = rowTotalIncome - rowTotalExp
#     TotalBalance=[]
#     TotalBalance.append(MonthBalance[0])
#     index=1
#     for i in range(len(MonthBalance)-1):
#         TotalBalance.append(TotalBalance[index-1]+MonthBalance[index])
#         index=index+1
#     df_balance = f_create_balance_dataframe(g_start,g_end,TotalBalance)
# ###########################################################################
#
#     # build savings df from db records for savings
#     df_save=f_build_df_from_db(myconfig.g_types_list[2][0],logIn_family_str,g_table_month_list,g_savings_table_df,{})
#     # print("views df_save: ",df_save)
#     # build loans df from db records for loans
#     df_loan=f_build_df_from_db(myconfig.g_types_list[3][0],logIn_family_str,g_table_month_list,g_loans_table_df,{})
#     # print("views df_loan: ",df_loan)
#     #transfer in comes df to html string
#     income_table_string = df_in.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tInTable")
#
#
#     #transfer expanse df to html string
#     expanse_table_string = df_exp.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tExpTable")
#
#     #transfer savings df to html string
#     savings_table_string = df_save.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tSaveTable")
#
#     #transfer expanse df to html string
#     loans_table_string = df_loan.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tLoanTable")
#
#     balance_table_string = df_balance.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tBalanceTable")
#
#     in_index_length=(len(df_in))
#
#
#     exp_index_length=(len(df_exp))
#     save_index_length=(len(df_save))
#     loan_index_length=(len(df_loan))
#     balance_index_length=(len(df_balance))

    dates_list_plotly = pd.date_range(g_start, g_end, freq='MS').strftime('%Y-%m').tolist()

    my_dict = {
               #  'InTable':income_table_string,
               # 'ExpTable':expanse_table_string,
               # 'SaveTable':savings_table_string,
               # 'LoanTable':loans_table_string,
               # 'BalanceTable':balance_table_string,


               # 'IncomeYAxies':df_in.iloc[in_index_length-1].tolist(),
               'IncomeXAxies':dates_list_plotly,
               # 'ExpYAxies':df_exp.iloc[exp_index_length-1].tolist(),
               'ExpXAxies':dates_list_plotly,

               # 'SavingsYAxies':df_save.iloc[save_index_length-1].tolist(),
               'SavingsXAxies':dates_list_plotly,
               # 'LoansYAxies':df_loan.iloc[loan_index_length-1].tolist(),
               'LoansXAxies':dates_list_plotly,

               # 'BalanceYAxies':df_balance.iloc[balance_index_length-1].tolist(),
               'BalanceXAxies':dates_list_plotly,

               'family':logIn_family_str,

               'SavingsRecordList':savings_records_list,
               'LoansRecordList':loans_records_list,

               'IncomesRecordList': incomes_records_list,
               'ExpansesRecordList': expanses_records_list,
               # 'form': form
               # 'datajsonread': PythonBackToJsData

               }
    return render(request,'FuturePlanning/v_f_new_event.html',context=my_dict)

def v_f_registration(request):
    registered = False
    print("reg:",registered)
    global g_usernameforfamily

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()
            g_usernameforfamily=user.username
            # print("user name:",usernameforfamily)
            # print("gFamily before save family:",g_current_family[0])
            c_Familys.objects.get_or_create(Fam_name=g_usernameforfamily)
            # print("gFamily after save family::",g_current_family[0].Fam_name,g_current_family[1].Fam_name)
            # g_current_family[0].Fam_name=usernameforfamily
            # print("gFamily after update list:",g_current_family[0].Fam_name,g_current_family[1].Fam_name)
            # print("type:",type(g_current_family))
            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True
            return redirect("FuturePlanning:index")

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'FuturePlanning/register.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

@login_required
def user_logout(request):
    global g_usernameforfamily
    # Log out the user.
    logout(request)
    g_usernameforfamily=""
    # Return to homepage.
    return redirect("FuturePlanning:index")

def user_login(request):
    global g_usernameforfamily
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                g_usernameforfamily=user.username
                # Send the user back to some page.
                # In this case their homepage.
                return redirect("FuturePlanning:index")
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'FuturePlanning/login.html', {})
