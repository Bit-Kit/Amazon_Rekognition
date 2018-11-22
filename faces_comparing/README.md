Rozpoznawanie twarzy
===
### Spis treści
1. [Wprowadzenie](#wprowadzenie)
2. [Kolejność i schemat działania](#schemat)
3. [---](#uslugi_modelu_intserv)
4. [---](#protokol_rsvp)
5. [Źródła](#zrodla)
---
### Wprowadzenie:<a name="wprowadzenie"></a>

[Face comparison](https://aws.amazon.com/rekognition/) wykonuje porównywanie twarzy "źródłowej" z każdą twarzą docelową. 
Wszystkie obliczenia są przeprowadzone na serwerach AWS, więc od klienta wymaga się jedynie wysłanie wiadomości z obrazkami.
W moim projekcie będą wykorzystywane 3 zdjęcia docelowe i 1 zdjęcie źródłowe. Zdjęcie źródłowe będzie zrobione kamerką Raspberry Pi. Wynik będzie w postaci wyświetlanej kłódki na małym wyświetlaczu.

### Kolejność i schemat działania:<a name="schemat"></a>

Ten schemat pokazuje jak się odbywa porównanie twarzy:
![Podstawowy schemat działania](files/Schemat_dzialania.jpg "Rys.1 Pydstawowy schemat działania")
Przede wszystkim jest uruchomiany skrypt Python-a:

    python3 fases_comparing_x.x.py
Odrazu zaświeca się wyświetlacz z zamkniętą kłódką:

<img src="files/closed_view.jpg" width="200">

Dalej po 3 sekundach kamera zapisuje zrobiony obrazek "camera.jpg" w folder gdzie został umieszczony skrypt  *fases_comparing_x.x.py*.
Uruchamia się rozpoznawanie pierwszej osoby:

    if response_person_1()== True:

Tutaj skrypt generuje żądanie w postacie JSON, gdzie umieszcza obrazek *camera.jpg* i ścieżkę do obrazka docelowego w serwisie S3, a następnie wysyła do serwera AWS. Serwer po krótkim czasie dostarcza odpowiedź.
Parametr *"confidence"* jest ustalony na 80% sukcesu rozpoznawania. Mianowicie, jeśli rozpoznawanie jest powyżej 80%, zaobserwujemy otwartą kłódkę na wyświetlaczu:

<img src="files/open_view.jpg" width="200">

W przypadku nie rozpoznawanie 1 osoby, następuje próba rozpoznawanie drugiej:

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
           



