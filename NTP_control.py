
from MyNTP import MyNTP
import ntplib
import datetime
import math

class NTP_control():

    # Referenz zu NTP https://tools.ietf.org/html/rfc5905#page-19
    # Die "Nummern" oben 2e Zeile symbolisieren 1 Bit.
    # Jede Zeile z.B. "Root Delay" ist 32 Bit (4Byte) groß.
    # Das gesamte NTP-Paket ist 48 Byte groß ohne extras.

    # Dies ist eine fremde Libary
    def get_ntp_time_Lib(server): # Timestamp über die NTP Libary
        call = ntplib.NTPClient()
        response = call.request(server, version=3)
        #t = datetime.datetime.fromtimestamp(response.orig_time)
        return response


    def NTP_GUI_interface(Adresse="0.de.pool.ntp.org", Anzahl=1, Modus=1):
        print("Anzahl: ",Anzahl)
        print("Modus: ",Modus)
        if Modus == 1 or Anzahl == 1:
            packetList = [MyNTP(str(Adresse))]
            OffsetReturn = MyNTP.Timedelta_String(packetList[0].offset)

        else: 
            packetList = Anzahl * [float()]
            index = 0
            while(Anzahl-1 >= index):
                packetList[index] = MyNTP(str(Adresse))
                index += 1

            if Modus == 2:
                sum = datetime.timedelta()
                for packet in packetList:
                    sum += packet.offset
                durchschnitt = sum/Anzahl #offsetAverage
                OffsetReturn = MyNTP.Timedelta_String(durchschnitt)
            elif Modus == 3:
                delayList = []
                for index, packet in enumerate(packetList):
                    try:
                        delayList.append(packet.delay)
                    except Exception:
                        print("Packet ist unvollständig")
                PacketIndex = delayList.index(min(delayList))
                minPacket = packetList[PacketIndex].offset

                OffsetReturn = MyNTP.Timedelta_String(minPacket)

        PC_Zeit = packetList[0].get_timestamp_from_packet(1)
        Server_Zeit = packetList[0].get_timestamp_from_packet(2)

        return PC_Zeit, Server_Zeit, OffsetReturn

    if __name__=='__main__':
 
        adresse = "0.de.pool.ntp.org"

        packet = MyNTP(adresse)

        h = packet.offset
        g = packet.delay

        print("Offset: {}".format(h))
        h2 = print("Delay: {}".format(g))

        print(packet.offset_String)

        A1, m = get_ntp_time_Lib("0.de.pool.ntp.org")

        t = abs( m.offset )

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

