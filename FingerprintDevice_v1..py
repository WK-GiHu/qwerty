from pyfingerprint.pyfingerprint import PyFingerprint
import threading, time

class FingerprintThread(threading.Thread):
    def __init__(self, app):
        super().__init__(daemon = True)
        #FingerprintThread.template = None
        self.app = app
        self._continue = threading.Event()
        #self.app.bind('<<GRANT_ACCESS>>', callback)
        self.start()

    def run(self):
        try:
            self.f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( self.f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
        
        print('Currently used templates: ' + str(self.f.getTemplateCount()) +'/'+ str(self.f.getStorageCapacity()))

        while True:
            retry = 0
            while True:
                print('Waiting for finger...')
                retry+=1
                try:
                    while (self.f.readImage() == False):
                        #print('looping .readImage()')
                        time.sleep(0.5)
                        
                        pass
                    break
                except Exception as e:
                     print('PyFingerprint:{}, try {} of 3'.format(e, retry))
                     if retry == 3:
                         raise Exception('PyFingerprint: Failed to read image 3 times, exiting.')

                     # delay 2 seconds before next try
                     time.sleep(2)
                
            ## Converts read image to characteristics and stores it in charbuffer 1
            #f.convertImage(0x01)

                ## Searchs template
            #FingerprintThread.template = f.searchTemplate()
            self.app.event_generate('<<FINGERPRINT>>', when='tail')
            self._continue.clear()
            self._continue.wait()
            
    def searchTemplate(self):
        self.f.convertImage(0x01)
        template = self.f.searchTemplate()
        #print('_continue.set()')
        self._continue.set()
        return template

if __name__ == "__main__":
    import tkinter as tk

    def on_fingerprint(event):
        template = fp.searchTemplate()
        print('on_fingerprint()  positionNumber={},  accuracyScore={}'
              .format(template[0], template[1]))

    root = tk.Tk()
    fp = FingerprintThread(root)
    root.bind('<<FINGERPRINT>>', on_fingerprint)
    root.mainloop()
