__author__ = 'DreTaX'
__version__ = '1.4'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""


class BannedPeople:
    """
        Methods
    """

    def On_PluginInit(self):
        Util.ConsoleLog("BannedPeople by " + __author__ + " Version: " + __version__ + " loaded.", False)

    red = "[color #FF0000]"
    green = "[color #009900]"
    white = "[color #FFFFFF]"


    def BannedPeopleConfig(self):
        if not Plugin.IniExists("BannedPeopleConfig"):
            ini = Plugin.CreateIni("BannedPeopleConfig")
            ini.AddSetting("Main", "Name", "[Equinox-BanSystem]")
            ini.AddSetting("Main", "BannedDrop", "You were banned from this server.")
            ini.Save()
        return Plugin.GetIni("BannedPeopleConfig")

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.1
    """

    def GetPlayerName(self, namee):
        try:
            name = namee.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

    def CheckV(self, Player, args):
        ini = self.BannedPeopleConfig()
        systemname = ini.GetSetting("Main", "Name")
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.join(" ", args))
            if p is not None:
                return p
            for pl in Server.Players:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            nargs = str(args).lower()
            p = self.GetPlayerName(nargs)
            if p is not None:
                return p
            for pl in Server.Players:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found [color#FF0000]" + str(count) + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None


    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def BannedPeopleIni(self):
        if not Plugin.IniExists("BannedPeople"):
            ini = Plugin.CreateIni("BannedPeople")
            ini.Save()
        return Plugin.GetIni("BannedPeople")

    def GetPlayerUnBannedID(self, name):
        namee = name.lower()
        ini = self.BannedPeopleIni()
        checkdist = ini.EnumSection("NameIds")
        for pl in checkdist:
            nameid = ini.GetSetting("NameIds", pl)
            lower = pl.lower()
            if nameid is None:
                return
            if lower == namee or namee in lower:
                return pl
        return None


    def GetPlayerUnBannedIP(self, name):
        namee = name.lower()
        ini = self.BannedPeopleIni()
        checkdist = ini.EnumSection("NameIps")
        for pl in checkdist:
            nameid = ini.GetSetting("NameIps", pl)
            lower = pl.lower()
            if nameid is None:
                return
            if lower == namee or namee in lower:
                return pl
        return None

    def On_Command(self, Player, cmd, args):
        if cmd == "banip":
            ini = self.BannedPeopleConfig()
            sysname = ini.GetSetting("Main", "Name")
            if Player.Admin or self.isMod(Player.SteamID):
                if len(args) > 0:
                    playerr = self.CheckV(Player, args)
                    if playerr is None:
                        return

                    else:
                        ini = self.BannedPeopleIni()
                        if playerr.Admin or self.isMod(playerr.SteamID):
                            Player.MessageFrom(sysname, "You cannot ban admins!")
                            return

                        id = playerr.SteamID
                        ip = playerr.IP
                        name = playerr.Name
                        loc = str(playerr.Location)
                        for pl in Server.Players:
                            if pl.Admin: pl.MessageFrom(sysname, "Message to Admins: " + self.red +  name + self.white + " was banned by: " + Player.Name)

                        ini.AddSetting("Ips", ip, "1")
                        ini.AddSetting("Ids", id, "1")
                        ini.AddSetting("NameIps", name, ip)
                        ini.AddSetting("NameIds", name, id)
                        ini.AddSetting("AdminWhoBanned", name, Player.Name)
                        ini.Save()
                        Player.Message("You banned " + name)
                        Player.Message("Player's IP: " + ip)
                        Player.Message("Player's ID: " + id)
                        Player.Message("Player's Location: " + loc)
                        playerr.Message("You were banned from the server")
                        checking = DataStore.Get("BanIp", Player.SteamID)
                        if checking == "true":
                            playerr.MessageFrom(sysname, self.red + "Admin, who banned you: UNKNOWN - Admin in Casing mode")

                        elif checking == "false" or checking is None:
                            playerr.MessageFrom(sysname, self.red + "Admin, who banned you: " + Player.Name)

                        playerr.Disconnect()
                else:
                    Player.MessageFrom(sysname, "Specify a Name!")
            else:
                Player.MessageFrom(sysname, "You aren't an admin!")

        elif cmd == "unbanip":
            if Player.Admin or self.isMod(Player.SteamID):
                ini = self.BannedPeopleConfig()
                sysname = ini.GetSetting("Main", "Name")
                if len(args) > 0:
                    name = self.argsToText(args)
                    id = self.GetPlayerUnBannedID(name)
                    ip = self.GetPlayerUnBannedIP(name)
                    if id is None:
                        Player.Message("Target: " + name + " isn't in the database, or you misspelled It!")

                    else:
                        ini = self.BannedPeopleIni()
                        name = id
                        iprq = ini.GetSetting("NameIps", ip)
                        idrq = ini.GetSetting("NameIds", id)
                        ini.DeleteSetting("Ips", iprq)
                        ini.DeleteSetting("Ids", idrq)
                        ini.DeleteSetting("NameIps", name)
                        ini.DeleteSetting("NameIds", name)
                        ini.Save()
                        for pl in Server.Players:
                            if pl.Admin:
                                pl.MessageFrom(sysname, self.red + name + self.white + " was unbanned by: " + self.green + Player.Name)

                        Player.MessageFrom(sysname, "Player " + name + " unbanned!")
                else:
                    Player.MessageFrom(sysname, "Specify a Name!")
        elif cmd == "banhidename":
            if Player.Admin or self.isMod(Player.SteamID):
                ini = self.BannedPeopleConfig()
                sysname = ini.GetSetting("Main", "Name")
                if not DataStore.ContainsKey("BanIp", Player.SteamID):
                    DataStore.Add("BanIp", Player.SteamID, "true")
                    Player.MessageFrom(sysname, "Now hiding your name!")
                else:
                    DataStore.Remove("BanIp", Player.SteamID)
                    Player.MessageFrom(sysname, "Now displaying your name!")
        elif cmd == "bans":
            if Player.Admin or self.isMod(Player.SteamID):
                ini = self.BannedPeopleConfig()
                sysname = ini.GetSetting("Main", "Name")
                checkdist = ini.EnumSection("NameIds")
                Player.MessageFrom(sysname, self.red + "Current Bans:")
                for pl in checkdist:
                    Player.MessageFrom(sysname, str(pl))
        elif cmd == "munbanip":
            if Player.Admin or self.isMod(Player.SteamID):
                ini = self.BannedPeopleIni()
                cfg = self.BannedPeopleConfig()
                sysname = cfg.GetSetting("Main", "Name")
                if len(args) == 0 or len(args) > 1:
                    Player.MessageFrom(sysname, "Usage: /munbanip IDorIP")
                    return
                v = str(args[0])
                if ini.GetSetting("Ips", v) is not None and ini.GetSetting("Ips", v):
                    ini.DeleteSetting("Ips", v)
                    ini.Save()
                    Player.MessageFrom(sysname, "Unbanned.")
                    return
                if ini.GetSetting("Ids", v) is not None and ini.GetSetting("Ids", v):
                    ini.DeleteSetting("Ids", v)
                    ini.Save()
                    Player.MessageFrom(sysname, "Unbanned.")
                    return
                Player.MessageFrom(sysname, "Couldn't find " + v)

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        ip = Player.IP
        ini = self.BannedPeopleConfig()
        sysname = ini.GetSetting("Main", "Name")
        bannedreason = ini.GetSetting("Main", "BannedDrop")
        ini = self.BannedPeopleIni()
        if ini.GetSetting("Ips", ip) is not None and ini.GetSetting("Ips", ip):
            if ini.GetSetting("Ids", id) is None:
                ini.AddSetting("Ids", id, Player.Name + " Connected from a banned IP: " + ip)
                ini.AddSetting("NameIps", Player.Name, ip)
                ini.AddSetting("NameIds", Player.Name, id)
                ini.Save()
            Player.MessageFrom(sysname, bannedreason)
            Player.Disconnect()
            return
        if ini.GetSetting("Ids", id) is not None and ini.GetSetting("Ids", id):
            if ini.GetSetting("Ips", ip) is None:
                ini.AddSetting("Ips", ip, Player.Name + " Connected from a banned ID " + id)
                ini.AddSetting("NameIps", Player.Name, ip)
                ini.AddSetting("NameIds", Player.Name, id)
                ini.Save()
            Player.MessageFrom(sysname, bannedreason)
            Player.Disconnect()