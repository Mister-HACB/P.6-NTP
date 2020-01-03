from MyNTP import MyNTP
import ntplib
import datetime
import math


# Referenz zu NTP https://tools.ietf.org/html/rfc5905#page-19
# Die "Nummern" oben 2e Zeile symbolisieren 1 Bit.
# Jede Zeile z.B. "Root Delay" ist 32 Bit (4Byte) groß.
# Das gesamte NTP-Paket ist 48 Byte groß ohne extras.

def get_ntp_time_Lib(server): # Timestamp über die NTP Libary
    call = ntplib.NTPClient()
    response = call.request(server, version=3)
    t = datetime.datetime.fromtimestamp(response.orig_time)
    return response.orig_time, response


if __name__=='__main__':
 
    adresse = "0.de.pool.ntp.org"

    packet = MyNTP(adresse)

    h = packet.offset
    g = packet.delay

    print("Offset: {}".format(h))
    h2 = print("Delay: {}".format(g))

    print(packet.offset_String)

    A1, m = get_ntp_time_Lib("0.de.pool.ntp.org")

    t = abs( m.offset - m.delay)

    print("\nNTP-Libary Berechnung")
    if t >= 0:
        text = "Positiver "
    else:
        text = "Negativer "
    print(text + "Offset von:")
    
    print("Millisekunden: ", math.floor(t/1000))
    print("Mikrosekunden: ", t % 1000)


    #print(datetime.datetime.now().strftime("%a %b %d %H:%M:%S.%f"))
    #print(ntp_Lib_Data.strftime("%a %b %d %H:%M:%S.%f"))

    pass


