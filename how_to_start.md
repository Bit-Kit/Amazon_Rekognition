Jak zacząć...
===
### Podstawą tego projektu są:
1. [Instalacja systemu](#instrukcja)
    1. [Pobieranie](#pobieranie)
    2. [Odpakowywanie oraz zapisywanie obrazu](#unzip)
    3. [Konfiguracja systemu](#sys)
2. [Komponenty i połączenie](#komp)
3. [AWS Command Line Interface](#cli)
4. [Python3](#python)
5. [Sterowniki kamery Raspberry Pi dla Python](#camera)
6. [Sterowniki wyświetlacza](#SSD1306)
7. [Źródła](#zrodla)
---
<a name="instrukcja"></a>
### Instrukcja instalacji systemu operacyjnego Raspberry Pi
<a name="pobieranie"></a>
#### Pobieranie

*Pobieranie oraz instalacja obrazu odbywa się na systemie UBUNTU*

System można pobrać z oficjalnej strony [www.raspberrypi.org](https://www.raspberrypi.org/downloads/)
Są dwie metody instalacji systemu. Za pomącą instalatora **NOOBS** i gotowego obrazu systemu **Raspbian**.
Z kolei Raspbian ma kilka wersji obrazu:
* **RASPBIAN STRETCH WITH DESKTOP AND RECOMMENDED SOFTWARE** - obraz zawierający podstawowe pakiety oraz pulpit
* **RASPBIAN STRETCH WITH DESKTOP** - obraz z pulpitem, ale bez podstawowych pakietów
* **RASPBIAN STRETCH LITE** - podstawowy obraz bez pulpitu i dodatków

Pobieramy system **"RASPBIAN STRETCH WITH DESKTOP AND RECOMMENDED SOFTWARE"**, by mięć od razu wszystkie narzędzia.
Po pobraniu zaobserwujemy plik *20XX-XX-XX-raspbian-stretch-full.zip*

<a name="unzip"></a>
#### Odpakowywanie oraz zapisywanie obrazu
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
    loop0    7:0    0   3,8M  1 loop 
    ................................


Znając pojemność naszej karty, możemy ją znaleść.
W moim przypadku jest to sdb1, która ma pojemność ok 16GB. Przed formatowaniem należy od montować kartę poleceniem:

    sudo umount /dev/sdb1
    
Następnie kasujemy wszystkie pliki:

    sudo dd if=/dev/zero of=/dev/sdb bs=4K && sync

To może trochę potrwać. Po tym tworzymy tabele rozdziałów:

    sudo fdisk /dev/sdb
    
Przywita nas aplikacja fdisk. Po uruchomieniu, należy podać kilka komend używając same litery. By wywołać pomoc, wpisz  ***'m'***.
Niżej jest pokazany przebieg poleceń:

    o - utworzenie nowej, pustej DOS-owej tablicy partycji
    n - dodanie nowej partycji
    p - tworzenie głównej partycji
    1 - numer partycji (1-4, default 1)
    Enter - określamy pierwszy sektor (2048-31116287, default 2048):
    Enter - określamy ostatni sektor, +sektorów lub +rozmiar{K,M,G,T,P} (2048-31116287, default 31116287):
    w - zapis tablicy partycji na dysk i zakończenie

Formatujemy kartę w formacie **vfat** poleceniem:

     sudo mkfs.vfat /dev/sdb1

Zapisujemy odraz Raspbian na kartę:

    sudo dd bs=4M if=20XX-XX-XX-raspbian-stretch-full.zip of=/dev/sdb0 conv=fsync
Bezpiecznie usuwamy kartę:

    sudo eject /dev/sdb
Wkładamy zapisaną kartę do Raspberry PI




<a name="sys"></a>
#### Konfiguracja systemu

Przy pierwszym uruchomieniu pojawi się pulpit z okienkiem przywitania. Należy wybrać język, lokalizację, ustalić hasło dla użytkownika i połączyć się z siecią Wi-Fi.
Dalej może być przeprowadzona automatyczna aktualizacja systemu.
Po rebucie włączamy SSH poprzez konfigurator Raspbian *raspi-config*:
    
    pi@raspberrypi:~ $ sudo raspi-config
    
Dalej wybieramy punkt 5 *Interfacing Options* > *SSH* > *Enable*. Następnie należy zrestartować system poleceniem:

     pi@raspberrypi:~ $ sudo reboot
Żeby się połączyć z urządzeniem po przez SSH powinniśmy wiedzieć adres IP Raspberry:

    pi@raspberrypi:~ $ ifconfig

I w zależności od rodzaju połączenia (LAN lub Wi-Fi) wyświetla się adres ip pod konkretnym interfejsem:
    
    pi@raspberrypi:~ $ ifconfig
    eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.69  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::cb4e:ecc5:58da:7052  prefixlen 64  scopeid 0x20<link>
        inet6 2a01:111f:b42:d100:4bb8:2ae:2dc3:2666  prefixlen 64  scopeid 0x0<g
W tym przypadku IP to *inet 192.168.1.69*
Teraz można sterować mikrokomputerem za pomocą PuTTy ze stacjonarnego komputera.
<a name="komp"></a>
# Komponenty i połączenie
![](scheme.jpg "Schemat")


<a name="cli"></a>
# AWS Command Line Interface
Jest to ujednolicone narzędzie do zarządzania usługami AWS. Za pomocą tego można kontrolować wiele usług AWS z poziomu wiersza poleceń i zautomatyzować je za pomocą skryptów.
By kożystać z serwisów Amazon przedewszystkim musimy dokonać [rejestrację.](https://portal.aws.amazon.com/billing/signup#/start) 

Po rejestracji można pobrać **awscli**:

    sudo pip awscli
  
Dalej przeprowadzamy konfigurację poleceniem *aws configure*
By wygenerować klucze dostępu należy zalogować się na stronie amazon, kliknąć *My Security Credentials* > *Access keys (access key ID and secret access key)* > klikamy *Create New Access Key*
Wyświetli się okienko do pobrania pliku .csv który zawiera identyfikator klucza dostępu i tajny klucz dostępu:
 identyfikatora klucza dostępu i tajnego klucza dostępu

        Access Key ID:XXXXXXXXXXXXXXXXX
        Secret Access Key:XXXXXXXXXXXXXXXXXXXXXXXXXXX
Należy te dane wprowadzić w konfiguracje aws.
Przy okazji można utworzyć "Bucket", czyli przestrzeń chmurową dla plików, w [S3](https://s3.console.aws.amazon.com/s3) > *Create buckets* > wprowadzić unikalną nazwe "Bucket".
Wracamy do konsoli:

    pi@raspberrypi:~ $ aws configure
    
    AWS Access Key ID [None]: //wprowadzamy klucz
    AWS Secret Access Key [None]://wprowadzamy klucz
    Default region name [None]: //wprowadzamy regon, typu "us-west-2"
    Default output format [None]: // wybieramy format "json"
Wszystkie wprowadzone dane znajdują się w plikach *config* i *credentials* w katalogu domowym .aws/.
Można sprawdzić połączenie za pomocą funkcji wyświetlania *"ls"*

    pi@raspberrypi:~ $aws s3 ls
W odpowiedzi dostaniemy nazwę utworzonego "Bucket" w serwisie S3.

<a name="#python"></a>
### Python3
Do tego obrazy Debian Python3 jest dołączony domyślnie. Można to sprawdzić poleceniem:

    pi@raspberrypi:~/.aws $ python --version  //dla Python-a drugiej wersji
    pi@raspberrypi:~/.aws $ python2 --version  //dla Python-a trzeciej wersji


<a name="camera"></a>
# Sterowniki kamery Raspberry Pi

By używać kamerę Raspberry Pi trzeba ją po pierwsze podłączyć do samego urządzenia po przez interfejs CSI, a następnie w 
menu konfiguracji *raspi-config* właczyć camerę:

    sudo raspi-config    
Wybieramy punkt *Interfacing Options* > *Camera* > *Enable*
Po włączeniu należy zresetować urządzenie. Po tym można sprawdzić łącznąść z kamerą poleceniem:

    vcgencmd get_camera
    
Wynik ma być taki:

    supported=1 detected=1
    
Teraz można zrobić pierwsze zdjęcie poleceniem:

    raspistill -o myphoto.jpg -t 2000
Zdjęcie domyślnie się zapisuje w katalogu domowym użytkownika.
By Python mógł używać zasoby kamery, należy zainstalować pakiet *picamera* poleceniem niżej:

    sudo apt-get install python-picamera python3-picamera
    
lub możemy dokonać pobranie za pomocą Python’s pip tool:

    sudo pip install picamera
    
Po installacji sprawdzimy działanie Python'a z kamerą. Twożymy plik z rozszerzeniem .py (Umaga! Nie tworzymy plików o nazwie **picamera.py**, ta nazwa jest zarezerwowana), i kopiujemy skrypt:

    from time import sleep
    from picamera import PiCamera

    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(5)
    camera.capture('photo.jpg')
    
Ten skrypt wyświetla okienko *"Preview"* które przedstawia nagrywanie kamery w czasie rzeczywistym i na końcu robi zdjęcie o nazwie "photo.jpg". Okienko "Preview"* będzie widoczne tylko i wyłącznie na wideo wyjściu urządzenia. Z poziomu aplikacja **PuTTy** nic nie zaobserwujemy.
Uruchomiamy poleceniem:

    python3 plik.py
    
<a name="SSD1306"></a>    
# Sterowniki wyświetlacza
W tym projekcie jaki dodatkową opcją wyprowadzenia informacji jest wyświetlacz na kontrolerze **ssd1306** z rozdzielcząścią **128X64**. Komynikacja pomiędzy Raspberry Pi i wyświetlaczem odbywa się po przez interfejs I2C.
Kontroler **ssd1306** obsługuje biblioteka [**Luma**](https://luma-oled.readthedocs.io/en/latest/intro.html).
Poniżej znajduje się instrukcja instalacji bibliotek Luma:

    sudo apt-get install python-dev python-pip libfreetype6-dev libjpeg-dev build-essential
    sudo -H pip install --upgrade luma.oled
    
Po instalacji w katalogu domowym pojawi się folder *codelectron_projects/Rpi/OLED* w którym znajdziemy napisane skrypty z przykładami uzycia tego wyświetlacza.



 ---
<a name="zrodla"></a>
### Źródła

* [Instrukcja instalacji os](https://www.raspberrypi.org/documentation/installation/installing-images/)
* [Pobranie systemu](https://www.raspberrypi.org/downloads/)
* [AWS Command Line Interface Getting Started](https://aws.amazon.com/cli/)
* [Getting started with picamera](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)
* [Installation picamera](https://picamera.readthedocs.io/en/release-1.13/install.html#raspbian-installation)
* [Luma.OLED Drivers](https://luma-oled.readthedocs.io/en/latest/index.html)

