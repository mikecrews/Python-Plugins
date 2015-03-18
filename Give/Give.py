__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""

class Give:

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def GetQuoted(self, array):
        text = str.join(" ", array)
        groups = text.split('"')
        n = len(groups)
        list = []
        for x in xrange(0, n):
            if x % 2 != 0:
                list.append(groups[x])
        return list

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
        systemname = "Give"
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
        if cmd == "give":
            if Player.Admin or self.isMod(Player.SteamID):
                if len(args) <= 2:
                    Player.MessageFrom('Give', 'Usage: /give "PlayerName" "ItemName" "Amount"')
                    Player.MessageFrom('Give', 'Quote signs (") are required.')
                    return
                array = self.GetQuoted(args)
                playerr = self.CheckV(Player, array[0])
                if playerr is None:
                    return
                if not array[2].isdigit():
                    Player.MessageFrom('Give', 'You must specify a quantity...')
                    return
                inventory = Player.Inventory
                inventory.AddItem(array[1], int(array[2]))
                Player.MessageFrom('Give', 'Given ' + str(array[2]) + " of " + str(array[1]) + " to " + playerr.Name)