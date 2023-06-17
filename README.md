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


