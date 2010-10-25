#!/usr/bin/python
# coding=utf8

"""
  SmoothAlarmClock 0.0.1a
"""

import pygst
pygst.require('0.10')
import gst
import glib, gobject
import sys, time, random, thread
reload(sys)
sys.setdefaultencoding( "utf-8" )



playlist = {
    't' : u"/media/a44432ae-d031-41f7-8187-02ffef0b8fa5/Enter Shikari (FLAC)/Take To The Skies/qiwitemp._flac_"
	}

class Main():
        def __init__(self):
                self.player = gst.element_factory_make("playbin2", "player")
                bus = self.player.get_bus()
                bus.add_signal_watch()	
                bus.connect("message", self.on_message)
                
        
        def on_message(self, bus, message):
                t = message.type
                if (t == gst.MESSAGE_EOS or t == gst.MESSAGE_ERROR):
                        self.player.set_state(gst.STATE_NULL)
                        self.playmode = False

        def play(self):
                uri = 'file://'+unicode(playlist.values()[random.randint(0, len(playlist) - 1)])
                self.playmode = True
                self.player.set_property('uri', uri)
                self.player.set_state(gst.STATE_PLAYING) 
                self.player.set_property('volume', 0.0)
                """ Плавное увеличение громкости """
                for i in range(10, 100):
                        self.player.set_property('volume', i/100.0)
                        time.sleep(1)
                
                print "done"
                
                while self.playmode:
                        time.sleep(1)
                loop.quit()


                print "Volume: ", self.player.get_property('volume')

""" Я так и не понял всей этой магии с тредами, но без неё нормально работать отказывалось. """
main = Main()
thread.start_new_thread(main.play, ())
gobject.threads_init()
loop = glib.MainLoop()
loop.run()
