from MyNTP import MyNTP
#import ntplib
import datetime

# Referenz zu NTP https://tools.ietf.org/html/rfc5905#page-19
# Die "Nummern" oben 2e Zeile symbolisieren 1 Bit.
# Jede Zeile z.B. "Root Delay" ist 32 Bit (4Byte) groß.
# Das gesamte NTP-Paket ist 48 Byte groß ohne extras.

def get_ntp_time_Lib(server): # Timestamp über die NTP Libary
    call = ntplib.NTPClient()
    response = call.request(server, version=3)
    t = datetime.datetime.fromtimestamp(response.orig_time)
    print(t.strftime("%a %b %d %H:%M:%S.%f"))

def delay(MyNTP_Object):
    T1 = packet.get_timestamp_from_packet(1)
    T2 = packet.get_timestamp_from_packet(2)
    T3 = packet.get_timestamp_from_packet(3)
    T4 = packet.get_timestamp_from_packet(4)
    
    ergebnis = (T4-T1)-(T3-T2)

    return ergebnis.microseconds / 1000

def offset(timestamp):
    T1 = packet.get_timestamp_from_packet(1)
    T2 = packet.get_timestamp_from_packet(2)
    T3 = packet.get_timestamp_from_packet(3)
    T4 = packet.get_timestamp_from_packet(4)

    ergebnis = (T2 - T1)+(T3 - T4) / 2
    return ergebnis.microseconds / 1000

if __name__=='__main__':
 
    adresse = "0.de.pool.ntp.org"

    packet = MyNTP(adresse)

    print("Offset: {}ms".format(offset(packet)))
    h2 = print("Delay: {}ms".format(delay(packet)))



    #ntp_packet = make_ntp_packet()
    #while True: # Diese Struktur hilft bei Code mit blockierendem warten
    #    Answer_packet = send_and_recieve_NTP_packet(ntp_packet,adresse)
    #    if Answer_packet:
    #        timestamp = get_timestamp_from_packet(Answer_packet,2)
    #        print(timestamp.strftime("%a %b %d %H:%M:%S.%f"))
    #        break
    #    print("Keine Daten erhalten")
    #    break


    #print(datetime.datetime.now().strftime("%a %b %d %H:%M:%S.%f"))


    #get_ntp_time_Lib("0.de.pool.ntp.org")

    pass


