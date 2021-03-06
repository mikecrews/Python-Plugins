__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System

"""
    Class
"""


class RampFix:
    """
        Methods
    """

    def On_PluginInit(self):
        Util.ConsoleLog("RampFix by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def On_EntityDeployed(self, Player, Entity):
        if Entity is not None:
            if "Ramp" in Entity.Name or "Foundation" in Entity.Name:
                loott = Util.TryFindReturnType('LootableObject')
                lob = UnityEngine.Object.FindObjectsOfType(loott)
                for i in xrange(0, len(lob)):
                    one = lob[i].collider.bounds
                    two = Entity.Object.collider.bounds
                    if two.Intersects(one):
                        Entity.Destroy()
                        return
                stt = Util.TryFindReturnType('StructureComponent')
                sc = UnityEngine.Object.FindObjectsOfType(stt)
                for i in xrange(0, len(sc)):
                    if sc[i].name.index("Foundation") != -1 or sc[i] == Entity.Object:
                        continue

                    if sc[i].name.index("Ramp(Clone)") != -1:
                        one = sc[i].collider.bounds
                        two = Entity.Object.collider.bounds
                        if two.Intersects(one):
                            Entity.Destroy()
                            return