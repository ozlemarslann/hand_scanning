
import cv2  # opencv-python(bu paket ile kameradan görüntü alınır.)
import mediapipe # mediapipe (elimizi taratıp noktalar arası bağlantıları çizebilir) paketleri kurulmali.

import pyttsx3 # yazilan metni sesli olarak donut verebilmesini saglar.
from pyttsx3 import engine # surekli olarak izin verildi yazisinin cikti alinmasini onler.

Kamera = cv2.VideoCapture(0) # bilgisayarda birden fazla kamera varsa bunlar arasında gezinilebilinir.
 # tek kamera olduğu için indeks olarak '0' verildi. Boylece kamera secildi.
# bu tanimlama dongu disinda yapilmalidir.

dinleme_motoru =pyttsx3.init() # kullaniciya geri donut verebilmek icin gelisen olayalri dinleme motoru

el_noktalari = mediapipe.solutions.hands # elinde 21 tane nokta olusmasini ve noktalar arasindaki baglantilarin gerceklesmesini saglayacak
el_objesi = el_noktalari.Hands() #bir el objesi olacaktir. Yukarida olusan constructor ile yapildi.
# resim icindeki eli tarayacak ve noktalari gonderildi. Parametreli default olarak birakildi.

nokta_cizimi = mediapipe.solutions.drawing_utils # elde edilen noktalari kamerada gosterilebilmesi icin bu metot kullanildi.
# RGB formatina donusturulen goruntuyu el_objesinin icine gonderilmesi gerekli return olarak landmarks [noktalarin bulundugu arry] donduruldu.

dinleme_kontrol = False

while True:
    # Kamera secildikten sonra frame yakalanmalı read() metodu kullanilarak yapilir. Bu metot geriye bir tane boolean bir tane de img
    # yani yakalanmis olan frame dondurecek eger kamera hicbir sey yakalamamissa sonuc false doner ve img bos resim olarak doner.
    sonuc , img = Kamera.read()

    resim_donusturme_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # cvtColor() metodu iki tane parametre  aliyor ilk olarak kaynak goruntuyu alirken
    # ikinci olarak hangi formattan goruntuye donusturmek istedigini belirtmen gerekli.

    nokta_dizisi = el_objesi.process(resim_donusturme_RGB)
   # print(nokta_dizisi.multi_hand_landmarks)
    # process() metodu formati degistirilmis goruntuyu alir. Elin uzerinde bulunan noktalari tutacaktir.
    # bu noktalarin konumlarini gormek istersek:
    # print(nokta_dizisi.multi_hand_landmarks) yazilirsa 21 elemanli arry ekrana yazilir. Arry da x,y,z elemanlari bulunur bu degerler ile
    # pencere boyutunu carparsan noktanin elin icinde nerede bulundugunu gorebilirisin eger kamerada el algilanmazssa none yazısı bastirilir.

    genislik, yukseklik, kanal = img.shape # pencere yuksekligi ve genisligi dondurur.

    if nokta_dizisi.multi_hand_landmarks:
        # print(len(nokta_dizisi.multi_hand_landmarks)) bu ifade kaç tane elin kamerada bulundugunu yazar.
        # if kullanilmasinin sebebi goruntude el algilanmissa bazi islemlere baslanmasi icindir
        for handlandmarks in nokta_dizisi.multi_hand_landmarks:
            # 21 elemanli arrayin her bir elemani icin ekrana for in dongusu kullanildi.
            # fingerNum: eleman indeksi, landmark: obje
            # pencerenin  boyutunu ogrenmek icin: shape kullanildi.
            for parmak_numrasi, koordinatlar in enumerate(handlandmarks.landmark):
                koordinat_X, koordinat_Y = int(koordinatlar.x * yukseklik), int(koordinatlar.y * genislik)
                # pencere genisligi ile x koordinati pencere yuksekigi ile y koordinati carpilir.
                # boylece herbir parmak icin pozisyon hesaplanmis olundu.
                if parmak_numrasi==4: # bas parmagin uzerine bir daire yerlestirme islemi
                    cv2.circle(img,(koordinat_X,koordinat_Y),15,(189,89,246),cv2.FILLED)



            #cv2.putText(img,str(parmak_numrasi),(koordinat_X,koordinat_Y), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0)) bu islem
            # elin icindeki noktalarin uzerine sayi yazma kismi
             # bas parmagin hareketi kontrol etmek icin


                if parmak_numrasi > 4 and koordinatlar.y < handlandmarks.landmark[2].y:
                    break
                #bas parmagin sayisal karsiligi 4 eger kullanici bas parmagini hareket ettirince sistem sesli donut verip kapanacak.

                if parmak_numrasi == 20 and koordinatlar.y > handlandmarks.landmark[2].y: # islem basarili bir sekilde tamamlanmis olur.
                    print("izin verildi")
                    checkThumbsUp = True

            nokta_cizimi.draw_landmarks(img, handlandmarks, el_noktalari.HAND_CONNECTIONS) # bu metot parametre olarak kaynak img alir
            # bu img uzerine cizimler gerceklesir.elin uzerindeki noktalar arasindaki cizgileri olusturur.

    cv2.imshow("Kamera aktif ", img) # imshow() metodu iki tane parametre alir. Bir tanesi videoyu gostermek istedigimiz pencere ismi
    # diger parametresi ise pencere icinde ne gostermek istedigimiz burada yukarida yakalamis oldugumuz img gosterilsin
    # surekli frame yakalamak istedigimiz icin bu islemi bir dongu icinde yapmamiz gerekli ancak bu sekilde bir video akisi elde edilir.

    if dinleme_kontrol: # desiken true ise sistem kapaniyor diye uyari verilir.
        dinleme_motoru.say("system shuts down")
        dinleme_motoru.runAndWait() # cumle bitene kadar bekler
        break # sistem kapatilir.

    if cv2.waitKey(1) & 0xFF == ord("e"):
        # waitKey() metodu sayesinde kullanicinin istedigi dogrultusunda bu akis saglanacak
        # metot icine '0' yazarsan sonsuza kadar kullanicinin herhangi bir tusa basmasini bekler ve bastigin anda yeni bir frame yaklar
        # bu sebeple donuk bir resim gorunur. Parametre olarak 1 yazinca i milisaniye boyunca bir input girisi bekler eger kullanici
        # herhangi bir tusa basmazsa dongu biter ve en bastan bir frame yakalar.Yeni frame yakaladikca kamera bir videoya donusur.
        # waitKey() metodu 32 bitlik bir int dondurur ama temsil etmek icin 8 bite ihtiyac var  & 0xFF bu ifade sayesinde 8 bite cevirir.
        # kamerayi kapatmak icin ord() metodu ile icine verilen ifadeyi int e cevirir. kullanici 'e' harfine basarsa kamera kapatilacaktir.
        # kameradan goruntu alindi bu goruntuyu mediapipe'a gonderip isleme yapilacak ama bu asamadan once elde edilen resmi RGB formatina cevirmemiz gerekli
        break