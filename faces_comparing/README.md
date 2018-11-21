Rozpoznawanie twarzy
===
Spis treści
1. [Wprowadzenie](#wprowadzenie)
2. [Kolejność i schemat działania](#schemat)
3. [---](#uslugi_modelu_intserv)
4. [---](#protokol_rsvp)
5. [Źródła](#zrodla)
---
Wprowadzenie:<a name="wprowadzenie"></a>

[Face comparison](https://aws.amazon.com/rekognition/) wykonuje porównywanie twarzy "źródłowej" z każdą twarzą docelową. 
Wszystkie obliczenia są przeprowadzone na serwerach AWS, więc od klienta wymaga się jedynie wysłanie wiadomości z obrazkami.
W moim projekcie będą wykorzystywane 3 zdjęcia docelowe i 1 zdjęcie źródłowe. Zdjęcie źródłowe będzie zrobione kamerką Raspberry Pi. Wynik będzie w postaci wyświetlanej kłódki na małym wyświetlaczu.

Kolejność i schemat działania:<a name="schemat"></a>

Ten schemat pokazuje jak się odbywa porównanie twarzy:

![Pydstawowy schemat działania](files/Schemat_dzialania.jpg "Rys.1 Pydstawowy schemat działania")

*
