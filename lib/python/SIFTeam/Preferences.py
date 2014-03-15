from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.SystemInfo import SystemInfo
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigBoolean
from Components.ActionMap import ActionMap
from Components.Button import Button

class Preferences(Screen, ConfigListScreen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.list = [
			getConfigListEntry(_("Start emulator at:"), config.sifteam.emudelay),
			getConfigListEntry(_("Skin developer mode:"), config.sifteam.skindevelopermode),
			getConfigListEntry(_("Video green switch enable 4:3 letterbox:"), config.sifteam.switch_4_3_letterbox),
			getConfigListEntry(_("Video green switch enable 4:3 panscan:"), config.sifteam.switch_4_3_panscan),
			getConfigListEntry(_("Video green switch enable 16:9:"), config.sifteam.switch_16_9),
			getConfigListEntry(_("Video green switch enable 16:9 always:"), config.sifteam.switch_16_9_always),
			getConfigListEntry(_("Video green switch enable 16:9 letterbox:"), config.sifteam.switch_16_9_letterbox),
			getConfigListEntry(_("Video green switch enable 16:10 letterbox:"), config.sifteam.switch_16_10_letterbox),
			getConfigListEntry(_("Video green switch enable 16:10 panscan:"), config.sifteam.switch_16_10_panscan)
		]

		
		ConfigListScreen.__init__(self, self.list, session = session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
				{
					"red": self.ok,
					#"green": self.green,
					"blue": self.keyCancel,
					"cancel": self.keyCancel,
				}, -2)
				
		self["key_green"] = Button("")
		self["key_red"] = Button(_("Ok"))
		self["key_blue"] = Button(_("Exit"))
		self["key_yellow"] = Button("")
		
	def ok(self):
		self.keySave()

