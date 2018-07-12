# Prima Iterazione

È stato installato [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/ "Download Raspbian") su un Raspberry Pi 3b+

È stata abilitata l'SSH sul raspberry creando un file vuoto con nome **SSH** nella partizione *boot* della microSD.

Alla prima accensione il raspberry è stato collegato tramite cavo ethernet al pc, che è stato configurato per condividere la connessione su questa interfaccia. Ho sempre lavorato in questo modo perchè mi è stato più semplice conoscere l'ip del raspberry, è comunque possibile lavorare collegandolo su wi-fi, ma è necessario uno schermo e una tastiera.

È stato possibile quindi controlare il raspberry tramite SSH con il comando

```bash
$ ssh pi@<ip address>
```

Prima di tutto è necessario verificare che siano installate le librerie GPIO per poter interfacciare Python con i pin del raspberry e quindi con il tasto.

``` bash
$ sudo apt-get install python-rpi.gpio python3-rpi.gpio
```

Successivamente sono stati scritti due script in python per registrare la pressione del tasto e scrivere un messaggio sul terminale (*pushbutton.py* e *pushbutton_event.py*).
Il secondo script sfrutta gli eventi associati ai pin GPIO per richiamare una funzione che stampa su terminale.

Gli script sono stati copiati sul raspberry tramite *scp*
```bash
$ scp ~/Documents/pushbutton.py pi@<ip address>

```

I collegamenti del tasto sono stati fatti seguendo questo schema 
![pin raspberry](https://www.raspberrypi-spy.co.uk/wp-content/uploads/2012/06/Raspberry-Pi-GPIO-Layout-Model-B-Plus-rotated-2700x900.png "Pin Raspberry")

Gli script possono essere lanciati con il seguente comando
```bash
$ python3 pushbutton.py
```

