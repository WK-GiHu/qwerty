from pyfingerprint.pyfingerprint import PyFingerprint
import threading, time

SEARCH = 1
REGISTER = 2

class FingerprintThread(threading.Thread):
    MODE = SEARCH
    template = None
    
    def __init__(self, app):
        super().__init__(daemon=True)
        
        self.app = app
        self.f = None
        self._continue = threading.Event()
        self._continue.set()
        self.start()
        
    def delete_template(self, positionNumber):
        # wait readImage
        self._continue.clear()
        time.sleep(0.5)
        
        b = self.f.deleteTemplate(str(positionNumber))
        if b:
            print('FingerprintThread:Template deleted!')
        
        # continue readImage
        self._continue.set()
        return b

    def run(self):
        try:
            self.f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
            
            if self.f.verifyPassword() == False:
                raise ValueError('The given fingerprint sensor password is wrong!')
        
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
        
        print('Currently used templates: ' + str(self.f.getTemplateCount()) + '/' + str(self.f.getStorageCapacity()))

        # REGISTER sequence
        sequence = 1
        
        while True:
            retry = 0
            while True:
                print('Waiting for finger...')
                retry += 1
                try:
                    while not self.f.readImage():
                        print('looping .readImage()')
                        self._continue.wait()
                        time.sleep(0.5)
                    break
                    
                except Exception as e:
                    print('PyFingerprint:{}, try {} of 3'.format(e, retry))
                    if retry == 3:
                        raise Exception('PyFingerprint: Failed to read image 3 times, exiting.')
                    # delay 2 seconds before next try
                    time.sleep(2)
            # end while retry == 3
            
            if FingerprintThread.MODE == SEARCH:
                self.f.convertImage(1)
                FingerprintThread.template = self.f.searchTemplate()
                self.app.event_generate('<<FINGERPRINT>>', when='tail', state=FingerprintThread.template[0])

            elif FingerprintThread.MODE == REGISTER:
                if sequence == 1:
                    self.f.convertImage(1)
                    FingerprintThread.template = self.f.searchTemplate()
                    sequence += 1
                
                elif sequence == 2:
                    self.f.convertImage(2)
                    if self.f.compareCharacteristics():
                        self.f.createTemplate()
                        # ? characterics = str(self.f.downloadCharacteristics(0x01)).encode('utf-8')
                        position_number = self.f.storeTemplate()
                    else:
                        position_number = -1

                    self.app.event_generate('<<FINGERPRINT>>', when='tail', state = position_number)
                    
                    # Reset MODE
                    sequence = 1
                    FingerprintThread.MODE = SEARCH
            
            # Delay before next finger scan
            time.sleep(2)


if __name__ == "__main__":
    import tkinter as tk
    
    
    def on_fingerprint(event):
        print('on_fingerprint()  positionNumber={}'.format(event.state))
    
    if 0:  # test MODE REGISTER
        print('on_register')
        FingerprintThread.MODE = REGISTER
    
    root = tk.Tk()
    fp = FingerprintThread(root)
    root.bind('<<FINGERPRINT>>', on_fingerprint)

    if 1:  # test delete_template
        fp.delete_template('<position number to delete>')

    root.mainloop()
