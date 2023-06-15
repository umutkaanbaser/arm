from .temel_fonklar import *
from .degiskenler import *
import sqlite3
from datetime import datetime

con=None
cursor=None

print("arm dahil edildi !")

def kontrol(func):
    def wrap(*args,**kwargs):
        global con,cursor
        if(con==None or cursor==None):
            raise Exception("Veritabani objesinden kopya üretiniz!") #hata oluştur ve onu dön!
        return func(*args,**kwargs)
    return wrap


def veri_class_birlestir(sinif,veriler,secilen):
    #print("yer:",sinif,veriler,secilen)
    don = []
    sutunlar = sutunlari_don(sinif)
    yeni_sutunlar = []
    if(secilen=='*'):
        secilen=sutunlar
    for sutun in sutunlar:
        if(sutun in secilen):
            yeni_sutunlar.append(sutun)

    sutunlar = yeni_sutunlar
    print("gelen veriler:",veriler)
    for veri in veriler:
        olusturucu="sinif.__class__("
        for i,bilgi in enumerate(veri):
            sutun = secilen[i]
            if(type(bilgi)==str): 
                var = " "+sutun+"='"+bilgi+"',"
            elif(bilgi==None):
                continue
            else:
                var = " "+sutun+"="+str(bilgi)+","
            olusturucu+=var
        olusturucu=olusturucu[:-1]
        olusturucu+=")"
        print("Çalışan Oluşturucu:",olusturucu)
        olusmus = eval(olusturucu)
        don.append(olusmus)
    return don

    
class tablo_veri_don:
    def __init__(self,SQL,tablo,secilenler):
        self.tablo=tablo
        #print("gelen:Tablo",self.tablo)
        self.SQL=SQL
        self.secilenler=secilenler
        print("SQL:",self.SQL)
    @kontrol
    def listele(self):
        global con,cursor
        print("SQL:",self.SQL,"Con:",con,cursor)
        cursor.execute(self.SQL)
        veriler = cursor.fetchall()
        if veriler is None:
            veriler = []
        don = veri_class_birlestir(self.tablo,veriler,self.secilenler)
        return don
    @kontrol
    def ilkdon(self):
        global con,cursor
        print("SQL:",self.SQL)
        cursor.execute(self.SQL)
        veri = cursor.fetchone()
        if veri is None:
            veri = []
        else:
            veri = [veri]
        don = veri_class_birlestir(self.tablo,veri,self.secilenler)
        if(len(don)>0):
            return don[0]
        else:
            return []    
    @kontrol
    def adet(self,sayi):
        if(type(sayi)==int):
            SQL=self.SQL+f" LIMIT {sayi}"
            print("SQL:",SQL)
            cursor.execute(SQL)
            veriler = cursor.fetchall()
            if veriler is None:
                veriler = []
            don = veri_class_birlestir(self.tablo,veriler,self.secilenler)
            return don
        else:
            raise ValueError("Adet sayisi 'int' tipinde olmalıdır")

    tolist = listele
    first = ilkdon
    take = adet

class sec_obje:
    def __init__(self,kosul_sorgu,tablo):
        self.kosul_sorgu=kosul_sorgu
        self.tablo=tablo
    def sec(self,secilenler):
        
        if(secilenler=="*"):
            SQL =f"SELECT * FROM {self.tablo.__name__}"
            print(f"giden SQL:{SQL} ==>",len(self.kosul_sorgu))
            if(len(self.kosul_sorgu)>0):
                SQL+=f" WHERE{self.kosul_sorgu}"
            return tablo_veri_don(SQL,self.tablo,secilenler)
        elif(type(secilenler)==list and len(secilenler)>0):
            SQL = "SELECT"
            WHERE=""
            for secilen in secilenler:
                if(secilen in dir(self.tablo)):
                    SQL+=f" {secilen},"
                else:
                    if(('max' in secilen or 'MAX' in secilen) or ('min' in secilen or 'MIN' in secilen)):
                        func,var = secilen.split("(")
                        var = var[:-1]
                        if(var in dir(self.tablo)):
                            if(not(var in secilenler)):
                                SQL+=f" {var},"
                            WHERE+=f" {var}=(SELECT {secilen} FROM {self.tablo.__name__}) AND"
                        else:
                            raise ValueError(f"{secilen} sutünü {self.tablo.__name__} tablosunda bulunmamaktadır.")
                    else:
                        raise ValueError(f"{secilen} sutünü {self.tablo.__name__} tablosunda bulunmamaktadır.")
            SQL = SQL[:-1]
            SQL+=f" FROM {self.tablo.__name__}"
            #print("asdasdasdas")
            #print(f"SQL:{SQL} WHERE:{WHERE} KOSUL:{self.kosul_sorgu}",len(self.kosul_sorgu))
            if(len(WHERE)>4 or len(self.kosul_sorgu)>0):
                SQL+=" WHERE"
            if(len(WHERE)>4):
                WHERE=WHERE[:-4]
                SQL+=WHERE
            if(len(self.kosul_sorgu)>0):
                SQL+=self.kosul_sorgu
            print(f"giden SQL:{SQL} -->")
            return tablo_veri_don(SQL,self.tablo,secilenler)
        #burada donme işlemi yapılacak
        else:
            raise ValueError("'*' yada istediğiniz sütünlari içinde bulunduran bir liste veriniz")
    
    choice = sec
class Tablo:
    def __init__(self,**kwargs):
        keys = kwargs.keys()
        asil_sutunlar = sutunlari_don(self)
        for sutun in asil_sutunlar:
            obje = eval(f"self.{sutun}")
            tip = str(obje.__class__).split("'")[1]
            tip = tip.split(".")[-1]

            #print(dir(obje))
            obje_degiskenleri = sutunlari_don(obje)
            #print("obje_degiskenleri:",obje_degiskenleri)
            
            yeni_sutun = eval(f"{tip}()")
            #print("yeni sutun:",type(yeni_sutun),type(obje),yeni_sutun,obje)
            for degisken in obje_degiskenleri:
                if(degisken=='deger' or degisken=='value' or degisken.startswith("_degisken")):
                    continue
                #print("guncelleme:",f"yeni_sutun.{degisken}=obje.{degisken}")
                exec(f"yeni_sutun.{degisken}=obje.{degisken}")

            exec(f"self.{sutun}=yeni_sutun")
        for key in keys:
            if(key in asil_sutunlar):
                obje = eval(f"self.{key}")
                obje.primary_guncelle_acik()
                
                
                if type(obje)==type(DATETIME()):
                    if type(kwargs[key])==type(datetime.now()):
                        date = kwargs[key]
                        y = date.year
                        mo = date.month
                        d = date.day
                        h = date.hour
                        m = date.minute
                        s = date.second
                        ms = date.microsecond
                        obje.tarih_st= f"{y}_{mo}_{d} {h}_{m}_{s}_{ms}"
                        print("-->",obje.tarih_st)
                    else:
                        obje.tarih_st=kwargs[key]
                    obje.deger = obje.tarih_st
                else:
                    obje.deger= kwargs[key]
            else:
                raise ValueError(f"'{key}' sutünü tabloda bulunmuyor!")
        #print(dir(self))

    @kontrol
    def ekle(self,tablo):
        global con,cursor
        isim_olustur(self)
        if(type(tablo)==type(self)):
            SQL = f"INSERT INTO {self.__name__}("
            asil_sutunlar = sutunlari_don(self)
            sutun_sql=""
            value_sql=""
            degerler=[]
            for sutun in asil_sutunlar:
                stn = eval(f"self.{sutun}")
                if('auto' in dir(stn) and stn.auto):
                    continue
                else:
                    stn_sql = f" {sutun},"
                    tablo_degeri = eval(f"tablo.{sutun}")
                    sutun_degeri = tablo_degeri.deger
                    if(stn.notnull and tablo_degeri.deger==None):
                        raise ValueError("'notnull' ibaresi işaretli olan nesneye değer verilmesi gerekmektedir.")
                    elif(sutun_degeri==None):
                        continue
                    sutun_sql+=stn_sql
                    vl_sql = f" ?,"
                    value_sql+=vl_sql
                    suan_deger = tablo_degeri.deger
                    degerler.append(suan_deger)
            SQL = SQL+sutun_sql
            SQL = SQL[:-1]
            SQL +=") VALUES("
            SQL= SQL+value_sql
            SQL = SQL[:-1]
            SQL+=")"

            print("SQL:",SQL,degerler)
            degerler = tuple(degerler)

            cursor.execute(SQL,(degerler))
            con.commit()
        else:
            raise ValueError(f"Lütfen {self.__name__} sınıfından bir koypa veriniz!")
    
    @kontrol
    def sil(self,tablo):
        global con,cursor
        isim_olustur(self)
        if(type(tablo)==type(self)):
            asil_sutunlar = sutunlari_don(self)
            primary_sutun=""
            for sutun in asil_sutunlar:
                tablo_sutun_sutunlari = sutunlari_don(eval(f"tablo.{sutun}"))
                if('primarykey' in tablo_sutun_sutunlari):
                    primary_key = eval(f"tablo.{sutun}.primarykey")
                    if(primary_key):
                        primary_sutun = sutun
                        break
                else:
                    continue
            SQL=""
            if(len(primary_sutun)>0):
                primary_deger = eval(f"tablo.{primary_sutun}.deger")
                SQL = f"DELETE FROM {self.__name__} WHERE {primary_sutun}={primary_deger}"
                cursor.execute(SQL)
            else:
                SQL = f"DELETE FROM {self.__name__} WHERE "
                degerler=[]
                for sutun in asil_sutunlar:
                    sutun_degeri = eval(f"tablo.{sutun}.deger")
                    degerler.append(sutun_degeri)
                    sql_ekle = f"{sutun}=? AND "
                    SQL+=sql_ekle
                SQL = SQL[:-5]
                cursor.execute(SQL,tuple(degerler))
            print("SQL:",SQL)
            
            con.commit()
        else:
            raise ValueError(f"Lütfen {self.__name__} sınıfından bir koypa veriniz!")
    
    @kontrol
    def guncelle(self,tablo):
        global con,cursor
        isim_olustur(self)
        if(type(tablo)==type(self)):
            asil_sutunlar = sutunlari_don(self)
            primary_sutun=""
            for sutun in asil_sutunlar:
                tablo_sutun_sutunlari = sutunlari_don(eval(f"tablo.{sutun}"))
                if('primarykey' in tablo_sutun_sutunlari):
                    primary_key = eval(f"tablo.{sutun}.primarykey")
                    if(primary_key):
                        primary_sutun = sutun
                        break
                else:
                    continue
            if(len(primary_sutun)<0):
                raise Exception(f"Güncelleme işlemleri için primary key'e sahip bir sütün gerekli!")
            SQL = f"UPDATE {self.__name__} SET"
            degerler=[]
            for sutun in asil_sutunlar:
                if(sutun==primary_sutun):
                    continue
                degeri = eval(f"tablo.{sutun}.deger")
                sql_ekle = f" {sutun}=?,"
                SQL+=sql_ekle
                degerler.append(degeri)
            SQL=SQL[:-1]
            SQL+=f" WHERE {primary_sutun}=?"
            degerler.append(eval(f"tablo.{primary_sutun}.deger"))
            print(SQL,degerler)
            cursor.execute(SQL,tuple(degerler))
            con.commit()
        else:
            raise ValueError(f"Lütfen {self.__name__} sınıfından bir koypa veriniz!")
    
    @kontrol
    def sorgula(self,sorgu):#Sorgu bir sözlüktür
        global con,cursor
        if(type(sorgu)==dict or sorgu==None):
            isim_olustur(self)
            keys = sorgu.keys()
            asil_sutunlar = sutunlari_don(self)
            SORGU=""
            if(type(sorgu)==dict):
                degerler=[]
                for key in keys:
                    if(key in asil_sutunlar):
                        tur = eval(f"type(self.{key}).__name__")
                        degeri=""
                        deger=sorgu[key]
                        if(tur=='VARCHAR' or tur=="TEXT"):
                            degeri=f"'{deger}'"
                        else:
                            degeri=str(deger)
                        sorgu_sql = f" {key}={degeri} AND"
                        SORGU+=sorgu_sql
                        degeri = sorgu[key]
                        degerler.append(degeri)
                    else:
                        raise ValueError(f"{key}, tablodaki sütünlar arasında bulunmuyor!")
                SORGU = SORGU[:-4]
            return sec_obje(SORGU,self)
            #Secim class'ı olusturulcaktır.

        else:
            raise ValueError("Lütfen bir sözlük veriniz!")   
        #sorgu ve secim gibi ozellikler yazılacak! rburada birer sınıf donucek

    add = ekle
    delete = sil
    update = guncelle
    select = sorgula
class VeriTabani():
    def __init__(self,tabanUrl="taban.db"):
        self.tabanUrl=tabanUrl
        self.veritabani_yap()
    
    def veritabani_yap(self):
        global con,cursor
        con = sqlite3.connect(self.tabanUrl)
        cursor = con.cursor()
        self.con=con
        self.cursor=cursor
        nesneler = dir(self)
        #print("nesneler",nesneler)
        index = nesneler.index("__class__")
        #print("index:",index)
        tablolar = nesneler[:index]
        #print("tablolar:",tablolar)
        for tablo in tablolar:
            sutun_nesne = eval(f"dir(self.{tablo})")
            #print("sutun_nesne",sutun_nesne,tablo)
            index = sutun_nesne.index("__class__")
            sutunlar = sutun_nesne[:index]
            SQL = f"Create Table If Not Exists {tablo}("
            for sutun in sutunlar:
                name = sutun
                #print(f"self.{tablo}.{sutun}.sql_don()")
                tip = eval(f"self.{tablo}.{sutun}.sql_don()")
                sql_sutun = name+" "+tip+","
                SQL+=sql_sutun
            SQL = SQL[:-1]
            SQL+=")"
            print("SQL:",SQL)
            self.cursor.execute(SQL)
            self.con.commit()





