import platform
systemIsWindows = False if platform.system()[0:5] == "Linux" else True

if not systemIsWindows:
    import dbus
    import dbus.service
    import dbus.mainloop.glib

    class Bluetoothplayer:
        def __init__(self):
            self.player_path = ""
            self.player = None
            self.bus = None
            self.manager = None
            self.objects = None
            self.Playing = False

        def getPlayer(self):
            self.bus = dbus.SystemBus()
            self.manager = dbus.Interface(self.bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager")
            self.objects = self.manager.GetManagedObjects()

            for path, ifaces in self.objects.items():
                if "org.bluez.MediaPlayer1" in ifaces:
                    self.player_path = path
                    self.player = self.bus.get_object("org.bluez", self.player_path)
                    return True
            return False

        def play(self):
            if self.player_path and self.Playing is False:
                self.player.Play(dbus_interface="org.bluez.MediaPlayer1")
                self.Playing = True
            else:
                print("No media player found. Check Bluetooth connection")

        def pause(self):
            if self.player_path and self.Playing is True:
                self.player.Pause(dbus_interface="org.bluez.MediaPlayer1")
                self.Playing = False
            else:
                print("No media player found. Check Bluetooth connection")

        def nextTrack(self):
            if self.player_path:
                self.player.Next(dbus_interface="org.bluez.MediaPlayer1")
            else:
                print("No media player found. Check Bluetooth connection")

        def prevTrack(self):
            if self.player_path:
                self.player.Previous(dbus_interface="org.bluez.MediaPlayer1")
            else:
                print("No media player found. Check Bluetooth connection")

        #yet to implement:
        def volumeUP(self):
            pass

        #yet to implement:
        def volumeDown(self):
            pass

    pls = Bluetoothplayer()
    pls.getPlayer()
    print(pls.player_path)
