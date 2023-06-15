
# Dahil etme 
#-----------
# Dogrudan bu şekilde dahil ederek kullanırsanız değişkenlere daha kolay ulaşım sağlarsınız
from arm.arm import *
from datetime import datetime

#Tablo Oluşturma
#--------------
#  Aşşağıda basitce tablo oluşturma ornekleri gösterilmiştir.
class Yetki(Tablo):
    Id=INT(primarykey=True,auto=True)
    YetkiIsim=VARCHAR(100)
    Derece=INT()

class Encoding(Tablo):
    Id=INT(primarykey=True,auto=True)
    PersonelId=INT()
    Resim = VARCHAR(100)
    CodingList=TEXT()

class Personel(Tablo):
    Id=INTEGER(primarykey=True,auto=True)
    YetkiId=INT()
    Isim=VARCHAR(100) #isim soy isim
    Telefon=VARCHAR(100)
    Adres=VARCHAR(100)
    IlkGun=DATETIME()
    PersonelId=INT()

class GirisLog(Tablo):
    Id=INT(primarykey=True,auto=True)
    PersonelId=INT()
    GirisSaati=VARCHAR(100)
    CikisSaati=VARCHAR(100)
    Tarih=VARCHAR(100)

class Log(Tablo):
    Id=INT(primarykey=True,auto=True)
    PersonelId=INT()
    Islem=VARCHAR(100)
    Tarih=DATETIME()


#Tabloları veri tabanına kayıt edip veri tabanını ayağa kaldırma
#----------------------------------------------------------------
class DataBase(VeriTabani):
    def __init__(self,*args,**kwargs):
        self.Yetki=Yetki()
        self.Encoding=Encoding()
        self.Personel=Personel()
        self.GirisLog=GirisLog()
        self.Log=Log()
        super().__init__(*args,**kwargs)


# !! olusturmus oldugunuz veri tabanından bir örnek oluşturunca init fonksyionu devreye girip veri tabanını olusturur
db = DataBase("yenitaban.db")


# veri Ekleme INSERT
# -----------------
#SQL: INSERT INTO Yetki( Derece, YetkiIsim) VALUES( ?, ?) [1, 'developer']
eklenecek_veri_yetki = Yetki(YetkiIsim="developer",Derece=1)
db.Yetki.ekle(eklenecek_veri_yetki)

# in english code
#db.Yetki.add(eklenecek_veri_yetki)


#SQL: INSERT INTO Personel( IlkGun, Isim, Telefon, YetkiId) VALUES( ?, ?, ?, ?) [datetime.datetime(2023, 6, 14, 17, 23, 32, 260133), 'kaan', '+90 50****', 1]
eklenecek_veri_personel = Personel(YetkiId=1,Isim="Umut Kaan Baser",Telefon="+90 50****",IlkGun=datetime.now())
db.Personel.ekle(eklenecek_veri_personel)

# in english code
#db.Personel.add(eklenecek_veri_personel)


#SQL: INSERT INTO Personel( IlkGun, Isim, Telefon, YetkiId) VALUES( ?, ?, ?, ?) [datetime.datetime(2023, 6, 14, 17, 24, 23, 447143), 'degistir', '+90 50****', 1]
eklenecek_veri_personel = Personel(YetkiId=1,Isim="degistir",Telefon="+90 50****",IlkGun=datetime.now())
db.Personel.ekle(eklenecek_veri_personel)

# in english code
#db.Personel.add(eklenecek_veri_personel)


#veri Degistirme Cekme UPDATE
#---------------------
degistirilecek_obje = db.Personel.sorgula({"Isim":"degistir"}).sec("*").ilkdon()
degistirilecek_obje.Isim.deger = "Memet"
#SQL : UPDATE Personel SET Adres=?, IlkGun=?, Isim=?, PersonelId=?, Telefon=?, YetkiId=? WHERE Id=? [None, '2023_6_15 18_56_45_883707', 'Memet', None, '+90 50****', 1, 2]
db.Personel.guncelle(degistirilecek_obje)

#in english code
#db.Personel.update(degistirilecek_obje)


# veri silme DELETE
# ----------------
silinecek_obje = db.Personel.sorgula({"Id":"2"}).sec("*").ilkdon()
#SQL : DELETE FROM Personel WHERE Id=3
db.Personel.sil(silinecek_obje)

# in english code 
#db.Personel.delete(silinecek_obje)


# veri sorgulama çekme SELECT
# --------------------------

# id'den tek veriyi alma
tek_veri_cekme = db.Personel.sorgula({"Id":"1"}).sec("*").ilkdon()
print(f"gelen Id:{tek_veri_cekme.Id.deger} isim:{tek_veri_cekme.Isim.deger}")

#id'den tek veriyi istenilen sütünlarını almak
istenilen_veri = db.Personel.sorgula({"Id":"1"}).sec(["Id","Isim"]).ilkdon()
print(f"gelen Id:{tek_veri_cekme.Id.deger} isim:{tek_veri_cekme.Isim.deger}")

#sorguya gore gelen verilerin istenilen sütünlarını almak
coklu_veriler = db.Personel.sorgula({"YetkiId":"1"}).sec(["Isim"]).listele()
for i,veri in enumerate(coklu_veriler):
    print(f"{i}. isim:{veri.Isim.deger}")

#sorguya gore gelen istenilen kadar verilerinin istenilen sütünlarını almak
coklu_veriler = db.Personel.sorgula({"YetkiId":"1"}).sec(["Isim"]).adet(3)
for i,veri in enumerate(coklu_veriler):
    print(f"{i}. isim:{veri.Isim.deger}")


# get data in english code SELECT
# ------------------------------
print ("""
|-------------------------------|
|  this is english code at now  |
|-------------------------------|
""")
tek_veri_cekme = db.Personel.select({"Id":"1"}).choice("*").first()
print(f"gelen Id:{tek_veri_cekme.Id.deger} isim:{tek_veri_cekme.Isim.deger}")

#id'den tek veriyi istenilen sütünlarını almak
istenilen_veri = db.Personel.select({"Id":"1"}).choice(["Id","Isim"]).first()
print(f"gelen Id:{tek_veri_cekme.Id.deger} isim:{tek_veri_cekme.Isim.deger}")

#sorguya gore gelen verilerin istenilen sütünlarını almak
coklu_veriler = db.Personel.select({"YetkiId":"1"}).choice(["Isim"]).tolist()
for i,veri in enumerate(coklu_veriler):
    print(f"{i}. isim:{veri.Isim.deger}")

#sorguya gore gelen istenilen kadar verilerinin istenilen sütünlarını almak
coklu_veriler = db.Personel.select({"YetkiId":"1"}).choice(["Isim"]).take(3)
for i,veri in enumerate(coklu_veriler):
    print(f"{i}. isim:{veri.Isim.deger}")