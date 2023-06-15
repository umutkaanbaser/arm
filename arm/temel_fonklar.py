DEGISKEN_TIPLERI = ["INT","FLOAT","DATETIME","TEXT","INTEGER","DOUBLE","VARCHAR"]

def isim_olustur(obje):
    tablo_isim = str(obje.__class__)
    tablo_isim = tablo_isim.split("'")[1] # <class 'arm.degiskenler.INT'> -> ['class' ,'arm.degiskenler.INT', '>']
    tablo_isim = tablo_isim.split(".")[-1] # arm.degiskenler.INT -> ['arm','degiskenler','INT']

    obje.__name__ = tablo_isim

def degisken_tip_getir(_str:str):
    print("_str: ",_str)
    _str = _str.split("'")[1] # <class 'arm.degiskenler.INT'> -> ['class' ,'arm.degiskenler.INT', '>']
    _str = _str.split(".")[-1] # arm.degiskenler.INT -> ['arm','degiskenler','INT']

    return _str

"""
def isim_olustur(obje):
    tablo_isim = str(obje.__class__)
    print("->",tablo_isim)
    tablo_isim = tablo_isim.split("'")[1] # <class 'arm.degiskenler.INT'> -> ['class' ,'arm.degiskenler.INT', '>']
    __tablo_isim = tablo_isim.split(".") # arm.degiskenler.INT -> ['arm','degiskenler','INT']
    for t_isim in __tablo_isim:
        if t_isim in DEGISKEN_TIPLERI:
            tablo_isim=t_isim
            break
    obje.__name__ = tablo_isim

def sutunlari_don(obje):
    sutunlar = dir(obje)
    index = sutunlar.index("__class__")
    asil_sutunlar = sutunlar[:index]
    return asil_sutunlar

"""
def sutun_don(obje):
    sutunlar = dir(obje)
    sutunlar = [i for i in sutunlar if not(i.startswith("__"))]
    don = []
    for sutun in sutunlar:
        tip = str(eval(f"type(obje.{sutun})"))
        #print("tip:",tip,sutun)
        tip = tip.split("'")[1]
        tip = tip.split(".")[0]
        #print("->tip:",tip)
        if(tip=='function' or tip=="method"):
            continue
        else:
            don.append(sutun)
    return don

sutunlari_don = sutun_don
