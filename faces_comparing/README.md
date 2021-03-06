Rozpoznawanie twarzy
===
### Spis treści
1. [Wprowadzenie](#wprowadzenie)
2. [Niezbędne pliki](#pliki)
3. [Kolejność i schemat działania](#schemat)
4. [S3](#s3)
5. [Biblioteki](#biblioteki)
6. [Źródła](#zrodla)
---

<a name="wprowadzenie"></a>
### Wprowadzenie:

[Face comparison](https://aws.amazon.com/rekognition/) wykonuje porównywanie twarzy "źródłowej" z każdą twarzą docelową. 
Wszystkie obliczenia są przeprowadzone na serwerach AWS, więc od klienta wymaga się jedynie wysłanie wiadomości z obrazkami.
W moim projekcie są dwie możliwości rozpoznawania twarzy:
* rozpoznawanie z użyciem 3 zdjęć docelowych(wysyłane są 3 źądania do serwera) plik **fases_comparing_x.x.py**
* rozpoznawanie z użyciem kolekcji zdjęć(jest tworzona lista z meta danymi zdjęć docelowych) plik **fases_comparing_in_collection_x.x.py**

Zdjęcie źródłowe będzie zrobione kamerką Raspberry Pi. Wynik będzie w postaci wyświetlanej kłódki na małym wyświetlaczu.

<a name="pliki"></a>
### Niezbędne pliki

Nazwa pliku              | Opis
-------------------------|----------------------
fases_comparing_x.x.py   | Rozpoznawanie 3 zdjęć
fases_comparing_in_collection_x.x.py   | Rozpoznawanie z użyciem kolekcji
fases_comparing_sample.py| Uproszczony podstawowy skrypt do prezentacji działania 
closed.png               | Obraz zamkniętej kłódki
open.png                 | Obraz otwartej kłódki

<a name="schemat"></a>
### Kolejność i schemat działania:

Ten schemat pokazuje jak się odbywa porównanie twarzy:
![Podstawowy schemat działania](files/Schemat_dzialania.jpg "Rys.1 Pydstawowy schemat działania")

Początkiem jest uruchomienie skryptu Python:

    python3 fases_comparing_x.x.py
    
Znakiem poprawnego działania jest świecąca się zamknięta kłódka:

<img src="files/closed_view.jpg" width="200">

Dalej po 3 sekundach kamera zapisuje zrobiony obrazek "camera.jpg" w folder gdzie został umieszczony skrypt  *fases_comparing_x.x.py*.
Uruchamia się rozpoznawanie pierwszej osoby:

    if response_person_1()== True:

Tutaj skrypt generuje żądanie w postacie JSON, gdzie umieszcza obrazek *camera.jpg* i ścieżkę do obrazka docelowego w serwisie S3, a następnie wysyła do serwera AWS. Serwer po krótkim czasie dostarcza odpowiedź.
Parametr *"confidence"* jest ustalony na 80% sukcesu rozpoznawania. Mianowicie, jeśli rozpoznawanie jest powyżej 80%, metoda  *response_person* zwróci *True* i zaobserwujemy otwartą kłódkę na wyświetlaczu:

<img src="files/open_view.jpg" width="200">

W przypadku nie rozpoznawanie 1 osoby, następuje próba rozpoznawanie drugiej, a następnie trzeciej.

By dostosować ten projekt do swoich potrzeb/rozwiązań, należy w konkretnym miejscu w skrypcie umieścić swój kawałek kodu: 

        if response_person_1()== True:
            print("Hello Person_1!")
            oled("Person1")
            ~ twoj kod ~

        elif response_person_2()== True:
            print("Hello Person_2!")
            oled("Person2")
            ~ twoj kod ~
        elif response_person_3()== True:
            print("Hello Person_3!")
            oled("Person3")
            ~ twoj kod ~
        else:
            print("Photo is not recognise.")
           
<a name="s3"></a>           
# Amazon simple storage service(S3)
Jest to "magazyn obiektów" który pozwala na chronienie danych w serwisie chmurowym. W tym projekcie S3 służy do chronienia w nim zdjęć docelowych. By to działało, trzeba umieścic 3 zdjęcia w Bucket S3 i w skrypcie zamienić wartości zmienych **bucket, sourceFile_2, sourceFile_2, sourceFile_3**:

    bucket =''          #Nazwa bucket w Amazon S3
    sourceFile_1 =''    #Zdjęcie 1
    sourceFile_2 =''    #Zdjęcie 2
    sourceFile_3 =''    #Zdjęcie 3

<a name="biblioteki"></a>
### Biblioteki

Nazwa biblioteki         | Opis
-------------------------|---------------------------------------------------------------------
boto3                    | Pakiet programistyczny do wykorzystania Python w Amazon Web Services
picamera                 | Biblioteka do wykorzystania zasobów kamery Raspberry PI
time                     | Biblioteka do wyliczania czasu pracy skryptu
i2c                      | Biblioteka do realizacji komunikacji poprzez interfejs I2C
canvas                   | Służy do renderingu obrazu na wyświetlaczu
ssd1306                  | Biblioteka sterownika Wyświetlacza
 ImageFont, ImageDraw, Image | Dodatkowe biblioteki dla przekształcania obrazu na wyświetlaczu
 
 ---
<a name="zrodla"></a>
### Źródła

* [Opis bibliotek OLED](https://ssd1306.readthedocs.io/en/latest/python-usage.html)
* [Comparing Faces in Images AWS](https://docs.aws.amazon.com/rekognition/latest/dg/faces-comparefaces.html)
* [Analyzing Images Stored in an Amazon S3 Bucket](https://docs.aws.amazon.com/rekognition/latest/dg/images-s3.html)
* [Using Boto 3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation)
* [Ograniczenia w Amazon Rekognition](https://docs.aws.amazon.com/rekognition/latest/dg/limits.html)
* [Koszty usług Amazon Rekognition](https://aws.amazon.com/rekognition/pricing/)
