import sys
import time
import socket
import datetime
import struct
import ntplib

# Referenz zu NTP https://tools.ietf.org/html/rfc5905#page-19
# Die "Nummern" oben 2e Zeile symbolisieren 1 Bit.
# Jede Zeile z.B. "Root Delay" ist 32 Bit (4Byte) groß.
# Das gesamte NTP-Paket ist 48 Byte groß ohne extras.

def get_ntp_time_Lib(server):
    call = ntplib.NTPClient()
    response = call.request(server, version=3)
    t = datetime.datetime.fromtimestamp(response.orig_time)
    print(t.strftime("%a %b %d %H:%M:%S.%f"))

def make_ntp_packet():
    # Format erstes Byte vom NTP Datenpacket
    # 2Bit (11) -> LI (Leap Sekunde) == ?
    # 3Bit (100) -> VN (Version)     == Version 4
    # 3Bit (011) -> Mode             == client Modus
    packet = bytearray(48) # Gesamtes NTP-Paket ist 48 Bytes groß
    packet[0] = 0b11100011 # -> \xe3
    return packet

def get_timestamp_from_packet(ntp_packet):

    # Extrahiert das "Transmit Timestamp" Bytearray
    timestamp_selection_bytearray = ntp_packet[40:48] 

    # !II: '!' -> LsB oder MsB; 'II' -> 2*unsigned_int
    # erstes Byte (I) sind die Sekunden
    # zweites Byte (I) sind die Bruchteile einer Sekunde (0.Bruchteil sekunden)
    sekunden_Int, sekunden_bruchteil_Int = struct.unpack("!II", timestamp_selection_bytearray)

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

    return zeit_Ursprung + paket_Zeitstempel + offset_Zeitzone

def send_and_recieve_NTP_packet(Paket,adress="pool.ntp.org"):
    port = 123 # Standard NTP-Port
    buffer = 1024 # Puffergröße für das Antwortpacket
    address_with_port = (adress,port) # Zusammengesetzte Adresse
    verbindung = socket.socket( socket.AF_INET, socket.SOCK_DGRAM) # AF_INET -> IPv4; SOCK_DGRA -> UDP
    try:
        verbindung.sendto(Paket, address_with_port) # Sendet das Packet an die Adresse
    except socket.gaierror:
        print("Adress Error")
        return None

    verbindung.settimeout(10) # Stellt eine 10s verbindungs Timeout ein.
    try:
        antwort = verbindung.recv(buffer) # Erhalte Rückanwort, wartet blockierend bis Timeout
    except socket.timeout:
        print("Timeout Error")
        return None

    verbindung.close() # schließt die Verbindung
    return antwort

if __name__=='__main__':
 
    adresse = "0.de.pool.ntp.org"


    ntp_packet = make_ntp_packet()
    while True: # Diese Struktur hilft bei Code mit blockierendem warten
        Answer_packet = send_and_recieve_NTP_packet(ntp_packet,adresse)
        if Answer_packet:
            timestamp = get_timestamp_from_packet(Answer_packet)
            print(timestamp.strftime("%a %b %d %H:%M:%S.%f"))
            #print("Their clock read (in UTC): ", timestamp)
            break
        print("Keine Daten erhalten")
        break

    

    print(datetime.datetime.now().strftime("%a %b %d %H:%M:%S.%f"))


    get_ntp_time_Lib("0.de.pool.ntp.org")

    int(abs(timestamp - _to_int(timestamp)) * 2**n)
    pass


