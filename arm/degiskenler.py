from .temel_fonklar import *
from datetime import datetime


class degisken():
    __deger=None
    __primary_guncelle=False
    @property
    def deger(self):
        return self.__deger

    @deger.setter
    def deger(self,a):
        if('primarykey' in dir(self) and self.primarykey and not(self.__primary_guncelle)):
            raise ValueError("Primary Key değişken güncellenemez!")
            #Dikkatli ol burada Eğer çagırma işlemlerinde hata alırsak burada duzelt!
            #Halledildi!
        if(self.__name__ == "INT" or self.__name__=="INTEGER"):
            if(type(a)!=int):
                raise ValueError("Girilen değer 'int' tipinde olmalıdır.")
            else:
                self.__deger=a

        elif(self.__name__ == "FLOAT" or self.__name__=="DOUBLE"):
            if(type(a)!=float):
                raise ValueError("Girilen değer 'float' tipinde olmalıdır.")
            else:
                self.__deger=a
        elif(self.__name__ == "TEXT" or self.__name__=="VARCHAR"):
            print("gelen a:",a)
            if(type(a)!=str and a is not None):
                raise ValueError("Girilen değer 'string' tipinde olmalıdır.")
            else:
                self.__deger=a
        elif(self.__name__ == "DATETIME"):
            print("gelen aat:",type(a),type(datetime.now()))
            if(type(a)==type(datetime.now()) or type(a)==type(str())):
                self.__deger=a
            else:
                raise ValueError("Girilen değer 'string' tipinde olmalıdır.")
                
        self.__primary_guncelle=False
    def primary_guncelle_acik(self):
        self.__primary_guncelle=True
    value = deger
    
        

class INT(degisken):
    def __init__(self,notnull=False,primarykey=False,auto=False):
        #print("gelen:",primarykey)
        self.notnull=notnull
        self.primarykey=primarykey
        self.auto=auto
        isim_olustur(self)
    def sql_don(self):
        don="INTEGER"
        if(self.notnull):
            don+=" NOT NULL"
        if(self.primarykey):
            don+=" PRIMARY KEY"
        if(self.auto):
            don+=" AUTOINCREMENT"
        return don
INTEGER = INT

class FLOAT(degisken):
    def __init__(self,notnull=False):
        self.notnull=notnull
        isim_olustur(self)
    def sql_don(self):
        don="DOUBLE"
        if(self.notnull):
            don+=" NOT NULL"
        return don
DOUBLE = FLOAT

class DATETIME(degisken):
    def __init__(self,tarih=None,tarih_st="",notnull=False):
        self.tarih=tarih
        self.notnull=notnull
        self.tarih_st=tarih_st
        isim_olustur(self)
    def sql_don(self):
        don = "TEXT" #DATETIME
        if(self.notnull):
            don+=" NOT NULL"
        if(self.tarih!=None):
            pass # buraya mssql yada mysql kontrolu yapılacak!!  
        return don
    def datetime_don(self):
        if(len(self.tarih_st)>0):
            #varsayılan Tarih var demektir
            print("st->",self.tarih_st)
            tarih,saat = self.tarih_st.split(" ")
            y,a,g = tarih.split("_")
            h,d,s,sa = saat.split("_")
            y,a,g,h,d,s,sa = [int(i) for i in [y,a,g,h,d,s,sa]]
            dt = datetime(y,a,g,h,d,s,sa)
            self.tarih = dt;
            return dt

class TEXT(degisken):
    def __init__(self,n=8001,notnull=False):
        self.n=n
        self.notnull=notnull
        isim_olustur(self)
    def sql_don(self):
        tip = "VARCHAR("
        if(self.n>8000):
            tip="TEXT"
        else:
            tip+=f"{self.n})"

        if(self.notnull):
            tip+=" NOT NULL"
        return tip
VARCHAR= TEXT
