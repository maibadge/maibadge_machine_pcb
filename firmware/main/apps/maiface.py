from hardware.buttons import buttons
from apps.template import AppTemplate
from machine import Timer, Pin
import time
import gc

img = [
        #"./images/maibear1.jpg", "./images/maibear_study_atb.jpg", "./images/maibear_og.jpg",
       #"./images/maibear_clown.jpg", "./images/maibear2.jpg", "./images/maibear_study_work_harder.jpg",  "./images/maibear_study_water_thing.jpg",
       "./images/maisongselect.jpg",  "./images/maisongchosen.jpg", "./images/maigameplay1.jpg", "./images/maigameplay2.jpg",
       "./images/screenimages/m1.jpg",
       "./images/screenimages/m2.jpg",
       "./images/screenimages/m3.jpg",
       "./images/screenimages/cc1.jpg",
       "./images/screenimages/cc2.jpg",
       "./images/screenimages/cc3.jpg",
       "./images/screenimages/cc4.jpg",
       "./images/screenimages/cc6.jpg",
       "./images/screenimages/cc7.jpg",
       "./images/screenimages/cc8.jpg",
       "./images/screenimages/cc9.jpg",
       "./images/screenimages/cc10.jpg",
       "./images/screenimages/cc11.jpg",
       "./images/screenimages/cc12.jpg",
       "./images/screenimages/cc13.jpg",
       "./images/menu_graphics/menu_foreground_1.jpg", 
       ]


previous_button_press = 0
def enable_handlers(function, ref):
    def handler(pin):
        # Software debouncing logic (100ms)
        global previous_button_press
        if (time.ticks_ms() - previous_button_press) < 1000:
            previous_button_press = time.ticks_ms()
            return
        previous_button_press = time.ticks_ms()
        function(pin)
    
    for b in ref["buttons"].values():
        b.irq(trigger=Pin.IRQ_FALLING, handler=handler) #detect pull down

class MaiFace(AppTemplate):
    def __init__(self, hardware):
        super().__init__(hardware)
        self.image_index = 0

    def load(self, exit_callback=None):
        self.exit_callback = exit_callback
        self.hardware["face"]["tft"].jpg(img[self.image_index], 0, 0)
        enable_handlers(self.on_press, self.hardware)
        
        self.tim0 = Timer(0)
        self.tim0.init(period=1000, mode=Timer.PERIODIC, callback=self.touchpads)
        
    def unload(self):
        # Clear interrupts
        ref = self.hardware
        for b in ref["buttons"].values():
            b.irq(trigger=Pin.IRQ_FALLING, handler=None)
        # Clear timer
        self.tim0.deinit()
        
        # Return
        if (self.exit_callback != None):
            self.exit_callback()
        
    ## Input
    def touchpads(self, t):
        ref = self.hardware
        for touchpad in ref["touchpads"]:
            if touchpad == "R3" and ref["touchpads"][touchpad].is_pressed():
                self.image_index = (self.image_index+1) % len(img)
                print(img[self.image_index])
                self.hardware["face"]["tft"].jpg(img[self.image_index], 0, 0)
            
            if touchpad == "L3" and ref["touchpads"][touchpad].is_pressed():
                self.image_index = (self.image_index-1) % len(img)
                print(img[self.image_index])
                self.hardware["face"]["tft"].jpg(img[self.image_index], 0, 0)
                    
            if touchpad == "L4" and ref["touchpads"][touchpad].is_pressed():
                # open maiface app
                self.unload()
        
            
    
    def on_press(self, pin):
        if pin == buttons['B']: 
            self.image_index = (self.image_index+1) % len(img)
            print(img[self.image_index])
            try:
                self.hardware["face"]["tft"].jpg(img[self.image_index], 0, 0)
            except Exception as e:
                print(e)
                self.image_index = (self.image_index-1) % len(img)
            gc.collect()

        ### Extra Code for ######################################################
        if pin == buttons['A']: 
            # open maiface app
            self.unload()
        #########################################################################
