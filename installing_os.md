Instrukcja instalacji systemu operacyjnego Raspberry Pi
===
Spis treści
1. [Pobieranie](#pobieranie)
2. [Odpakowywanie oraz zapisywanie obrazu](#unzip)
3. [Źródła](#zrodla)
---

<a name="pobieranie"></a>
### Pobieranie

*Pobieranie oraz instalacja obrazu odbywa się na systemie UBUNTU*

System można pobrać z oficjalnej strony [www.raspberrypi.org](https://www.raspberrypi.org/downloads/)
Są dwie metody instalacji systemu. Za pomącą instalatora **NOOBS** i gotowego obrazu systemu **Raspbian**.
Z kolei Raspbian ma kilka wersji obrazu:
* RASPBIAN STRETCH WITH DESKTOP AND RECOMMENDED SOFTWARE - obraz zawierający podstawowe pakiety oraz pulpit
* RASPBIAN STRETCH WITH DESKTOP - obraz z pulpitem, ale bez podstawowych pakietów
* RASPBIAN STRETCH LITE - podstawowy obraz bez pulpitu i dodatków

Pobieramy system **"RASPBIAN STRETCH WITH DESKTOP AND RECOMMENDED SOFTWARE"**, by mięć od razu wszystkie narzędzia.
Po pobraniu zaobserwujemy plik *20XX-XX-XX-raspbian-stretch-full.zip*

<a name="unzip"></a>
### Odpakowywanie oraz zapisywanie obrazu
By odpakować pobrany obraz Raspbian użyjemy polecenie:
  
    unzip 20XX-XX-XX-raspbian-stretch-full.zip
  
Na jakiś czas Terminal może się zawiesić. Dalej wkładamy kartę microSD do czytnika, w moim przypadku jest to przejściówka SD-microSD.
Wykrywamy w systemie naszą kartę poleceniem:
    
    lsblk
    
Wyświetla się coś takiego:

    NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
    sda      8:0    0 465,8G  0 disk
    ├─sda1   8:1    0   100M  0 part
    ├─sda2   8:2    0   178G  0 part
    ├─sda3   8:3    0     1K  0 part
    ├─sda4   8:4    0  21,9G  0 part
    ├─sda5   8:5    0 128,8G  0 part /media/user/E2D6493ED64913E7
    ├─sda6   8:6    0  28,2G  0 part /
    ├─sda7   8:7    0   2,5G  0 part [SWAP]
    └─sda8   8:8    0 106,2G  0 part /home
    sdb      8:16   1  14,9G  0 disk
    └─sdb1   8:17   1  14,9G  0 part
    sr0     11:0    1  1024M  0 rom
    loop0    7:0    0   3,8M  1 loop /snap/notepad-plus-plus/167
    loop1    7:1    0 825,3M  1 loop /snap/play0ad/53
    loop2    7:2    0   3,8M  1 loop /snap/notepad-plus-plus/156
    loop3    7:3    0  88,2M  1 loop /snap/core/5897
    loop4    7:4    0     4M  1 loop /snap/notepad-plus-plus/140
    loop5    7:5    0 237,9M  1 loop /snap/wine-platform-i386/25
    loop6    7:6    0  87,9M  1 loop /snap/core/5742
    loop7    7:7    0  87,9M  1 loop /snap/core/5662
    loop8    7:8    0 227,3M  1 loop /snap/wine-platform-i386/23
    loop9    7:9    0  75,3M  1 loop /snap/play0ad/83

Znając pojemność naszej karty, możemy ją znaleść.
W moim przypadku jest to sdb1 która ma pojemność ok 16GB. Przed formatowaniem należy odmontować kartę poleceniem:

    sudo umount /dev/sdb1
    
Następnie dokonujemy formatowanie:

    sudo dd if=/dev/zero of=/dev/sdb bs=4K && sync

To może trochę potrwac. Po formatowaniu zapisujemy obraz pobranego systemu na kartę:

    sudo dd bs=4M if=20XX-XX-XX-raspbian-stretch-full.zip of=/dev/sdb0 conv=fsync

---
<a name="zrodla"></a>
### Źródła 

* [Instrukcja instalacji os](https://www.raspberrypi.org/documentation/installation/installing-images/)
* [Pobranie systemu](https://www.raspberrypi.org/downloads/)
