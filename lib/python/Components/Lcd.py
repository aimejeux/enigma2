from config import config, ConfigSubsection, ConfigSelection, ConfigSlider, ConfigYesNo, ConfigNothing
from enigma import eDBoxLCD
from Components.SystemInfo import SystemInfo
from Tools.Directories import fileExists

class LCD:
	def __init__(self):
		pass

	def setBright(self, value):
		value *= 255
		value /= 10
		if value > 255:
			value = 255
		eDBoxLCD.getInstance().setLCDBrightness(value)

	def setContrast(self, value):
		value *= 63
		value /= 20
		if value > 63:
			value = 63
		eDBoxLCD.getInstance().setLCDContrast(value)

	def setInverted(self, value):
		if value:
			value = 255
		eDBoxLCD.getInstance().setInverted(value)

	def setFlipped(self, value):
		eDBoxLCD.getInstance().setFlipped(value)

	def isOled(self):
		return eDBoxLCD.getInstance().isOled()

def leaveStandby():
	config.lcd.bright.apply()

def standbyCounterChanged(configElement):
	from Screens.Standby import inStandby
	inStandby.onClose.append(leaveStandby)
	config.lcd.standby.apply()

def InitLcd():
	if config.misc.boxtype.value == 'gb800se' or config.misc.boxtype.value == 'gb800solo' or config.misc.boxtype.value == 'gb800seplus':
		detected = False
	else:
		detected = eDBoxLCD.getInstance().detected()
	SystemInfo["Display"] = detected
	config.lcd = ConfigSubsection();

	if fileExists("/proc/stb/lcd/mode"):
		f = open("/proc/stb/lcd/mode", "r")
		can_lcdmodechecking = f.read().strip().split(" ")
		f.close()
	else:
		can_lcdmodechecking = False
	
	SystemInfo["LCDMiniTV"] = can_lcdmodechecking

	if detected:
		if can_lcdmodechecking:
			def setLCDModeMinitTV(configElement):
				try:
					f = open("/proc/stb/lcd/mode", "w")
					f.write(configElement.value)
					f.close()
				except:
					pass
			def setMiniTVFPS(configElement):
				try:
					f = open("/proc/stb/lcd/fps", "w")
					f.write("%d \n" % configElement.value)
					f.close()
				except:
					pass
			def setLCDModePiP(configElement):
				pass

			config.lcd.modepip = ConfigSelection(choices={
					"0": _("off"),
					"5": _("PIP"),
					"7": _("PIP with OSD")},
					default = "0")
			if config.misc.boxtype.value == 'gbquad' or config.misc.boxtype.value == 'gbquadplus':
				config.lcd.modepip.addNotifier(setLCDModePiP)
			else:		
				config.lcd.modepip = ConfigNothing()

			config.lcd.modeminitv = ConfigSelection(choices={
					"0": _("normal"),
					"1": _("MiniTV"),
					"2": _("OSD"),
					"3": _("MiniTV with OSD")},					
					default = "0")						
			config.lcd.fpsminitv = ConfigSlider(default=30, limits=(0, 30))
			config.lcd.modeminitv.addNotifier(setLCDModeMinitTV)
			config.lcd.fpsminitv.addNotifier(setMiniTVFPS)
		else:
			config.lcd.modeminitv = ConfigNothing()
			config.lcd.modepip = ConfigNothing()
			config.lcd.fpsminitv = ConfigNothing()
			
		def setLCDbright(configElement):
			ilcd.setBright(configElement.value);

		def setLCDcontrast(configElement):
			ilcd.setContrast(configElement.value);

		def setLCDinverted(configElement):
			ilcd.setInverted(configElement.value);

		def setLCDflipped(configElement):
			ilcd.setFlipped(configElement.value);

		standby_default = 0

		ilcd = LCD()

		if not ilcd.isOled():
			config.lcd.contrast = ConfigSlider(default=5, limits=(0, 20))
			config.lcd.contrast.addNotifier(setLCDcontrast);
		else:
			config.lcd.contrast = ConfigNothing()
			standby_default = 1

		config.lcd.standby = ConfigSlider(default=standby_default, limits=(0, 10))
		config.lcd.standby.addNotifier(setLCDbright);
		config.lcd.standby.apply = lambda : setLCDbright(config.lcd.standby)
		config.lcd.bright = ConfigSlider(default=5, limits=(0, 10))
		config.lcd.bright.addNotifier(setLCDbright);
		config.lcd.bright.apply = lambda : setLCDbright(config.lcd.bright)
		config.lcd.bright.callNotifiersOnSaveAndCancel = True
		config.lcd.invert = ConfigYesNo(default=False)
		config.lcd.invert.addNotifier(setLCDinverted);
		config.lcd.flip = ConfigYesNo(default=False)
		config.lcd.flip.addNotifier(setLCDflipped);
	else:
		def doNothing():
			pass
		config.lcd.contrast = ConfigNothing()
		config.lcd.bright = ConfigNothing()
		config.lcd.standby = ConfigNothing()
		config.lcd.bright.apply = lambda : doNothing()
		config.lcd.standby.apply = lambda : doNothing()

	config.misc.standbyCounter.addNotifier(standbyCounterChanged, initial_call = False)

