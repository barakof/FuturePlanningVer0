
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','calcalut.settings')

import django
django.setup()

from FuturePlanning.models import Familys,Records,c_Events,c_Familys,c_Records

c_Familys.objects.get_or_create(Fam_name="Ofir")
c_Familys.objects.get_or_create(Fam_name="Zinger")
c_Familys.objects.get_or_create(Fam_name="Gal")

OfirFam=c_Familys.objects.get_or_create(Fam_name="Ofir")[0]
ZingerFam=c_Familys.objects.get_or_create(Fam_name="Zinger")[0]

c_Records.objects.get_or_create(Family=OfirFam,Rec_Type="In",Rec_Name="Barak",Start_Date="01 2021",End_Date="09 2021",Value=13000)
c_Records.objects.get_or_create(Family=OfirFam,Rec_Type="In",Rec_Name="Hadas",Start_Date="01 2021",End_Date="09 2021",Value=12000)
c_Records.objects.get_or_create(Family=OfirFam,Rec_Type="Exp",Rec_Name="Barak",Start_Date="01 2021",End_Date="09 2021",Value=5000)
c_Records.objects.get_or_create(Family=OfirFam,Rec_Type="Exp",Rec_Name="Hadas",Start_Date="01 2021",End_Date="09 2021",Value=6000)

c_Records.objects.get_or_create(Family=ZingerFam,Rec_Type="In",Rec_Name="Yoval",Start_Date="01 2021",End_Date="09 2021",Value=13000)
c_Records.objects.get_or_create(Family=ZingerFam,Rec_Type="In",Rec_Name="Ravit",Start_Date="01 2021",End_Date="09 2021",Value=12000)
c_Records.objects.get_or_create(Family=ZingerFam,Rec_Type="Exp",Rec_Name="Yoval",Start_Date="01 2021",End_Date="09 2021",Value=5000)
c_Records.objects.get_or_create(Family=ZingerFam,Rec_Type="Exp",Rec_Name="Ravit",Start_Date="01 2021",End_Date="09 2021",Value=6000)

c_Events.objects.get_or_create(Family=ZingerFam,Rec_Name="Yoval",Rec_Type="In",Eve_Name="Trip")
c_Events.objects.get_or_create(Family=ZingerFam,Rec_Name="Ravit",Rec_Type="Exp",Eve_Name="Trip")
c_Events.objects.get_or_create(Family=OfirFam,Rec_Name="Barak",Rec_Type="In",Eve_Name="Hotel")
c_Events.objects.get_or_create(Family=OfirFam,Rec_Name="Hadas",Rec_Type="Exp",Eve_Name="Hotel")


# print all records in event trip of zinger familys
records_of_event=c_Events.objects.all().filter(Eve_Name="Trip").filter(Family=ZingerFam)
for element in records_of_event:
    # print(element.Rec_Name)
    # print(element.Family)
    # print(element.Rec_Type)
    records=c_Records.objects.all().filter(Family=element.Family).filter(Rec_Name=element.Rec_Name).filter(Rec_Type=element.Rec_Type)
    print("event records:")
    for element_1 in records:
        print(element_1.Rec_Name)
        print(element_1.Family)
        print(element_1.Rec_Type)
        print(element_1.Start_Date)
        print(element_1.End_Date)
        print(element_1.Value)







print(records_of_event)


if __name__=='__main__':
    print("start")

    print("end")
