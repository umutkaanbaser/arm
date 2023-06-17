# ARM 
ARM veritabanı ve nesne tabanlı programlamayı eşleştiren bir ORM (Object–relational mapping) yazılımıdır. Temel seviye işlemlerde kolayca kullanabileceğiniz bir yazılım geliştirme aracıdır. Şimdilik sadece sqlite veritabanında çalışmaktadır.

It is an ORM (Object–relational mapping) software that maps ARM database and object-oriented programming. It is a software development tool that you can easily use for basic level operations.It run on sqlite database now.

# ARM İLE NELER YAPILABİLİR ? | WHAT CAN DO WITH ARM ?
* arm nesne tabanı ile kolayca nesneler olusturabilir, veritabanı ayağa kaldırabilirsiniz. 
* arm ile sql dilinde hiç kod yazmadan veritabanına ekleme, silme, güncelleme ve sorgulama işlemleri yapabilirsiniz.
* olusturmus oldugunuz veri tabanı ile nesneleri ilişkilendirerek nesne yönelimli programalayla daha okunaklı ve hatadan uzak bir kodlama yapabilirsiniz.

* You can easily create objects and raise the database with the arm object base.
* With arm, you can insert, delete, update and select the database without writing any code in sql language.
* By associating the objects with the database you have created, you can make a more readable and error-free coding with object-oriented programming.

# ARM NASIL KULLANILIR ? | HOW USE ARM ?
### dizin yapısı | directory struct
```
project/
|
|-- arm/
|   |-- __init__.py
|   |-- arm.py
|   |-- degiskenler.py
|   |-- tablo_vb.py
|   |-- temel_fonklar.py
|
| # diğer kod dosyaları ve klasörler
| # other code file and directories
|
|-- main.py # from arm.arm import *

```
### dahil etme | including
```python
from arm.arm import *
```
### tablo oluşturma | create a table
```python
class ogrenci(Tablo):
    Id=INT(primarykey=True,auto=True)
    isim_soyisim=VARCHAR(100)
    sinif=INT()

class student(Tablo):
    Id=INT(primarykey=True,auto=True)
    name_surname=VARCHAR(100)
    class_number=INT()
```
tablo oluştururken 'Tablo' sınıfından kalıtım almalısınız. Altında doğrudan değişken isimlerini tanımlayıp değişken tiplerini bildiriniz. Veritabanında verimiş olduğunz isimler ile oluşacaklardır. Değikenlerin kendilerine ait parametreleri bulunmaktadır burada 'primarykey=True' diyerek birincil anahtar olduğunu bildirdik ve 'auto=True' diyerek ise kendisi artıcak şekilde tanımladık.

when creating a table you must inherit from the 'Tablo' class. Define the variable names directly below and declare the variable types. They will be created with the names you have given in the database. Variables have their own parameters, here we declared that it is the primary key by saying 'primarykey=True', and we defined it to auto increment with 'auto=True'.

### veritabanı oluşturma | create a database
```python
class DataBase(VeriTabani):
    def __init__(self,*args,**kwargs):
        self.ogrenci = ogrenci()
        self.student = student()
        super().__init__(*args,**kwargs)
```
veritabanı ayağa kaldırırmak için 'VeriTabani' nesneninden kalıtım alan bir nesne oluşturmanız gerekmektedir. O nesnenin içine __init__ fonksiyonunun altına tablolardan kopya oluşturarak veriniz. Unutmayınız *args ve **kwargs değişkenlerini mutlaka kalıtım alınan nesneye iletiniz 5. satırda olduğu gibi.


To raise the database, you need to create an object that inherits from the 'VeriTabani' object. Submit it under the __init__ function by creating a copy of the tables inside that object. Do not forget to pass *args and **kwargs variables to the inherited object, as in line 5.

```python
db = DataBase("_sqlite.db")
```
ardından oluşturmuş olduğunuz nesneden bir kopya ürettiğinizde __init__ fonksiyonu çalışır ve vermiş olduğunuz isim ile veritabanını ayağa kaldırır. Eğer bu isimde veritabanı var ise sadece ona bağlanacaktır.

Then, when you produce a copy of the object you created, the __init__ function runs and restores the database with the name you have given. If there is a database with this name, it will only connect to it.

### ekleme işlemi | Insert
```python
eklenecek_veri = ogrenci(isim_soyisim='ornek isim',sinif=5)
db.ogrenci.ekle(eklenecek_veri)

add_value = ogrenci(name_surname='ornek isim',class_number=5)
db.student.insert(add_value)
```
veri tabanına veri eklemek için ise tablo sınıfından bir örnek oluşturup içine verilerinizi veriniz. Arından 'VeriTabani' nesnesinden kalıtım alarak oluşturdugunuz nesne de gerekli sütunun 'ekle' methodunu kullanarak kolayca ekleyebilirisiniz.

To add data to the database, create an example from the table class and insert your data into it. Then you can easily add the object you created by inheriting from the 'VeriTabani' object by using the 'insert' method of the required column.


### veri güncelleme | Update
```python
degistirilecek_obje = db.ogrenci.sorgula({"Id":"1"}).sec("*").ilkdon()
degistirilecek_obje.isim_soyisim.deger = "ornek2"
db.Personel.guncelle(degistirilecek_obje)

change_obje = db.student.select({"Id":"1"}).choice("*").first()
change_obje.name_surname.value = "example3"
db.Personel.update(degistirilecek_obje)
```
güncellemek için sadece hangi sütunu değiştirmek istiyorsanız o Sütunun 'deger' özelliğine yeniden güncellemeniz yeterlidir. Ardından '.güncelle' methoduna veriniz.
To update it, simply update the 'value' property of the column you want to change.Then give the object to the '.update' method.


### veri silme | Delete
```python
silinecek_obje = db.ogrenci.sorgula({"Id":"2"}).sec("*").ilkdon()
db.ogrenci.sil(silinecek_obje)

delete_object = db.student.select({"Id":"2"}).choice("*").first()
db.student.delete(delete_object)
```
veritabani nesnesine gerekli tablonun .sil methoduna silincek objeyi vererek kolayca silebilirsiniz.

You can easily delete the database object by giving the object to be deleted to the .delete method of the required table.

### veri sorgulama | Select
```python

```
sorgulama işlemi 3 adımda yapılır ilk olarak 'sorgula' methoduyla sutünlarda olması istenilen veriler yazılır. Ardından 'sec' methoduyla hangi sütunların geri dönüleceği söylenir. ve sonuncu adım olarakta liste olarak mı , tek 1 veri mi yoksa koşulu sağlayan belli sayıda ki veriler mi dönülsün onu söyleriz.

The query process is done in 3 steps. First, the data that is required to be in the columns is written using the 'select' method. Then it is told which columns to return with the 'choice' method. And as the last step, we tell you whether to return as a list, single data or a certain number of data satisfying the condition.
