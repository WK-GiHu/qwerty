from pyfingerprint.pyfingerprint import PyFingerprint
import threading, time

class FingerprintThread(threading.Thread):
    def __init__(self, app):
        super().__init__(daemon = True)
        result = None
        self.template = None
        self.app = app
        #self.app.bind('<<GRANT_ACCESS>>', callback)
        self.start()

    def run(self):
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
        
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

        while True:
            retry = 0
            while True:
                print('Waiting for finger...')
                retry+=1
                try:
                    while (f.readImage() == False):
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
            f.convertImage(0x01)

                ## Searchs template
            self.template = f.searchTemplate()
            self.app.event_generate('<<FINGERPRINT>>', when='tail')


if __name__ == "__main__":
    import tkinter as tk

    def on_grant_access(event):
        print('on_grant_access()  positionNumber={},  accuracyScore={}'
              .format, fp.fingerprint[0], fp.fingerprint[1])

    root = tk.Tk()
    fp = FingerprintThread(root)
    root.bind('<<FINGERPRINT>>', on_grant_access)
    root.mainloop()

