import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','calcalut.settings')

import django
django.setup()

import random
from FuturePlanning.models import Familys,Records,c_Events,c_Familys,c_Records
from faker import Faker

fakegen=Faker()

def population(N=5):

    FamilyList = Familys.objects.all()

    recTypes=["In","Exp","Sav","Loa"]
    recName=["A","B","C","D","E","F","G","H","I"]

    i=1
    for entry in range(N):
        fam=Familys.objects.get_or_create(Fam_name=fakegen.name(),Fam_id=i)[0]
        i=i+1
        for j in range(30):
            Sd=fakegen.date_between(start_date="today",end_date="+5y")
            Sds=Sd.strftime('%m %Y')
            Eds=fakegen.date_between(start_date=Sd,end_date="+5y").strftime('%m %Y')

            Records.objects.get_or_create(Family=fam,Rec_Type = random.choice(recTypes),Rec_Name=random.choice(recName),
                                            Start_Date=Sds,
                                            End_Date=Eds,
                                            Value=random.randrange(0, 2000, 200))
            print(fakegen.date_between(start_date="today",end_date="+10y").strftime('%m %Y'))







    # class Familys(models.Model):
    # Fam_name = models.CharField(max_length=80)
    # Fam_id = models.IntegerField(unique=True)


    # class Records(models.Model):
    # Family = models.ForeignKey(Familys,on_delete=models.CASCADE)
    # # testmy = models.CharField(max_length=50)
    # # type: In Exp Sav Loa Ass
    # Rec_Type = models.CharField(max_length=3,default='In')
    # Rec_Name = models.CharField(max_length=50,default='Name')
    # Start_Date = models.CharField(max_length=20,default='mm_yyyy')
    # End_Date = models.CharField(max_length=20,default='mm_yyyy')
    # Value = models.PositiveIntegerField(default=0)

if __name__=='__main__':
    print("start")
    population(2)
    print("end")
