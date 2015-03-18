__author__ = 'DreTaX'
__version__ = '1.1'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""

green = "[color #009900]"
white = "[color #FFFFFF]"
teal = "[color #00FFFF]"
red = "[color #FF0000]"
class PM:

    def On_PluginInit(self):
        DataStore.Flush("PmSys")
        Util.ConsoleLog("PM by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def GetQuoted(self, array, Player):
        text = str.join(" ", array)
        if not '"' in text:
            Player.MessageFrom('PrivateMessage', 'Usage: /report "PlayerName" "message"')
            Player.MessageFrom('PrivateMessage', 'Quote signs (") are required.')
            return False
        groups = text.split('"')
        n = len(groups)
        list = []
        for x in xrange(0, n):
            if x % 2 != 0:
                list.append(str(groups[x]).strip('\\'))
        if len(list) < 2:
            return False
        return list

    def FindPlayerById(self, id):
        try:
            p = Server.FindPlayer(id)
            return p
        except:
            return None
    
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
        systemname = "PrivateMessage"
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

    def On_Command(self, Player, cmd, args):
        if cmd == "pm":
            if len(args) <= 1:
                Player.MessageFrom('PrivateMessage', 'Usage: /pm "PlayerName" "message"')
                Player.MessageFrom('PrivateMessage', 'Quote signs (") are required.')
                return
            array = self.GetQuoted(args, Player)
            if not array:
                return
            playerr = self.CheckV(Player, array[0])
            if playerr is None:
                return
            playerr.MessageFrom("PrivateMessage", green + "(" + Player.Name + " -> You):  " + teal + array[1])
            Player.MessageFrom("PrivateMessage", green + "(You -> " + playerr.Name + "):  " + teal + array[1])
            DataStore.Add("PmSys", Player.SteamID, playerr.SteamID)
            DataStore.Add("PmSys", playerr.SteamID, Player.SteamID)
        elif cmd == "r":
            if len(args) == 0:
                Player.MessageFrom('PrivateMessage', 'Usage: /r message')
                return
            if not DataStore.ContainsKey("PmSys", Player.SteamID):
                Player.MessageFrom('PrivateMessage', 'You have to send a Private Message first via /pm')
                return
            id = DataStore.Get("PmSys", Player.SteamID)
            text = str.join(" ", args)
            playerr = self.FindPlayerById(id)
            if playerr is None:
                DataStore.Remove("PmSys", Player.SteamID)
                Player.MessageFrom('PrivateMessage', red + "Player must be offline. Removing from /r")
                return
            playerr.MessageFrom("PrivateMessage", green + "(" + Player.Name + " -> You):  " + teal + text)
            Player.MessageFrom("PrivateMessage", green + "(You -> " + playerr.Name + "):  " + teal + text)

    def On_PlayerDisconnected(self, Player):
        id = Player.SteamID
        DataStore.Remove("PmSys", id)