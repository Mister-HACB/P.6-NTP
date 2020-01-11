
import sys
import time
import socket
import datetime
import struct
import math

class MyNTP:
    
    def __init__(self,adresse="0.de.pool.ntp.org"):
        try:
            if type(adresse) == str:
                self.__antwort = self.__send_and_recieve_NTP_packet(self.__make_ntp_packet(),adresse)
            else:
                raise IOError
        except IOError:
            print("Nur str Datentyp erlaub für adresse")

        return

    #def __str__(self):
    #    string =  "Nutze get_timestamp_from_packet(Packetname,part)"
    #    string += "n/Part == 0 => Transmit Timestamp"
    #    string += "n/Part == 1 => Receive Timestamp"
    #    string += "n/Part == 2 => Origin Timestamp"
    #    return string

    def __make_ntp_packet(self):
        now = time.time() # Referenzzeit
        part_with_timestamp = struct.pack("!II", # Eigener Timestamp 2*4Byte (Sekunden, bruchteil-Sekunden)
            int(time.time()),
            int(abs(now - int(now)) * 2**32))

        packet = bytearray(24) + part_with_timestamp + bytearray(16) # Setzt das NTP-Packet zusammen
    
        # Format erstes Byte vom NTP Datenpacket
        # 2Bit (11) -> LI (Leap Indicator) == keine Synchronisation von Schaltsekunden
        # 3Bit (100) -> VN (Version)       == Version 4
        # 3Bit (011) -> Mode               == client Modus 
        packet[0] = 0b11100011 # -> \xe3

        # Gesamtes NTP-Paket ist 48 Bytes groß
        return packet

    def __send_and_recieve_NTP_packet(self,Paket,adress):
        port = 123 # Standard NTP-Port
        buffer = 1024 # Puffergröße für das Antwortpacket
        address_with_port = (adress,port) # Zusammengesetzte Adresse
        verbindung = socket.socket( socket.AF_INET, socket.SOCK_DGRAM) # AF_INET -> IPv4; SOCK_DGRA -> UDP
        try:
            zeitStart = time.time()
            verbindung.sendto(Paket, address_with_port) # Sendet das Packet an die Adresse
        except socket.gaierror:
            print("MyNTP Modul - Adress Error")
            return None
        except IOError:
            print("MyNTP Modul - IOError")
            return None
        verbindung.settimeout(5) # Stellt eine 5s verbindungs Timeout ein.
        try:
            antwort = verbindung.recv(buffer) # Erhalte Rückanwort, wartet blockierend bis Timeout
            zeitEnde = time.time()
        except socket.timeout:
            print("MyNTP Modul - Timeout Error")
            return None
        verbindung.close() # schließt die Verbindung
        return antwort, zeitStart, zeitEnde

    def get_timestamp_from_packet(self,part=0):
        if   part == 1:
            timestamp_auswahl = self.__antwort[1]
        elif part == 2:
            # Extrahiert den passenden Teil vom Bytearray für das gewünschte Timestamp
            timestamp_auswahl = self.__antwort[0][32:40] #Receive Timestamp (rec): Time at the server when the request arrived from the client, in NTP timestamp format.
        elif part == 3:
            # Extrahiert den passenden Teil vom Bytearray für das gewünschte Timestamp
            timestamp_auswahl = self.__antwort[0][40:48] #Transmit Timestamp (xmt): Time at the server when the response left for the client, in NTP timestamp format.
        elif part == 4:
            timestamp_auswahl = self.__antwort[2]
        else:
            timestamp_auswahl = None
            print("Part zwischen 1 bis 4 wählen")

        # Decodierung des Timestamps aus einem Bytearray
        # !II: '!' -> MsB; 'II' -> 2*unsigned_int
        # erstes Byte (I) sind die Sekunden
        # zweites Byte (I) sind die Bruchteile einer Sekunde (0.Bruchteil sekunden)
        if type(timestamp_auswahl) == bytes:
            sekunden_Int, sekunden_bruchteil_Int = struct.unpack("!II", timestamp_auswahl)

            # Timestamp Objekte bei 0 starten um 1.1.1900
            zeit_Ursprung = datetime.datetime(1900, 1, 1) # datetime.datetime Typ

            # Erkennt die Zeitzone auf dem aktuellen System
            offset_Zeitzone = datetime.timedelta(0, 0 - time.timezone) # datetime.timedelta Typ

            # Sekundenbruchteile sind in 32Bit aufgelöst (232 Picosekunden)
            sekunden_bruchteil = sekunden_bruchteil_Int / 2**32

            # Sekunden und Sekundenbruchteile vereinen
            sekunden_Zeit = sekunden_Int + sekunden_bruchteil

            # Umwandlung in "lesbare" Zeit; Tage, Sekunden, Mikrosekudnen, Millisekunden, Minuten, Stunden, Wochen
            # Wert wird in Sekunden mit dem Signalwort "seconds =" mitgegeben
            paket_Zeitstempel = datetime.timedelta(seconds = sekunden_Zeit)
            timestamp_auswahl_formatiert = zeit_Ursprung + paket_Zeitstempel + offset_Zeitzone
        else:
            timestamp_auswahl_formatiert = datetime.datetime.fromtimestamp(timestamp_auswahl)

        return timestamp_auswahl_formatiert

    @property
    def delay(self):
        T1 = self.get_timestamp_from_packet(1)
        T2 = self.get_timestamp_from_packet(2)
        T3 = self.get_timestamp_from_packet(3)
        T4 = self.get_timestamp_from_packet(4)

        # https://www.meinberg.de/german/info/ntp-packet.htm
        ergebnis = (T4-T1)-(T3-T2)
        return ergebnis #Timedelta-Typ

    @property
    def offset(self):
        T1 = self.get_timestamp_from_packet(1)
        T2 = self.get_timestamp_from_packet(2)
        T3 = self.get_timestamp_from_packet(3)
        T4 = self.get_timestamp_from_packet(4)

        # https://www.meinberg.de/german/info/ntp-packet.htm
        ergebnis = (T2 - T1)+(T3 - T4) / 2
        return ergebnis #Timedelta-Typ

    def Timedelta_String(offset_Timedelta):

        if(offset_Timedelta >= datetime.timedelta(0)):
            antwort = "Positiver "
        else: 
            offset_Timedelta = abs(offset_Timedelta)
            antwort = "Negativer "

        antwort += "Offset von:"
        d = offset_Timedelta.days
        s = offset_Timedelta.seconds
        m = offset_Timedelta.microseconds
        if(d > 0): # Gibt Differenz von Tagen an
            antwort += "\n{} Tage".format(d)

        if(math.floor(s / 3600 % 24)): # Gibt Differenz von Stunden an, 0 & 24 Stunden ausgenommen
            antwort += "\n{} Stunden".format(math.floor(s % 3600 % 24))

        if(math.floor(s / 60 % 60)): # Gibt Differenz von Minuten an, 0 & 60 Minuten ausgenommen
            antwort += "\n{} Minuten".format(math.floor((s / 60) % 60))

        if(math.floor(s % 60)): # Gibt Differenz von Sekunden an, 0 & 60 Sekunden ausgenommen
            antwort += "\n{} Sekunden".format(math.floor(s % 60))

        if(math.floor(m/1000)): # Gibt Differenz von Sekunden an, 0 & 60 Sekunden ausgenommen
            antwort += "\n{} Millisekunden".format(math.floor(m/1000))

        if(m % 1000):
            antwort += "\n{} Mikrosekunden".format(m % 1000)

        return antwort