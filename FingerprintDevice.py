import time
from pyfingerprint.pyfingerprint import PyFingerprint
import pymysql
import threading, time
import tkinter as tk


class FingerprintThread(threading.Thread):
    def __init__(self, parent):
        super().__init__(daemon = True)
        result = None
        self.template = None
        #self.app.bind('<<GRANT_ACCESS>>', callback)
        self.start()

    def run(self):        
        #self.db = pymysql.connect(host = "192.168.1.9",port = 3306, user = "root",passwd = "justin",db= "thesis_main")
        #self.cursor = self.db.cursor()
        #self.db.autocommit(True)
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
                        print('looping .readImage()')
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

            positionNumber = result[0]
            accuracyScore = result[1]

            self.cursor.execute("SELECT * FROM residents_admin WHERE FINGER_TEMPLATE = %s",positionNumber)
            FingerprintThread.result = self.cursor.fetchone()
            print (FingerprintThread.result)
            if FingerprintThread.result:
                self.app.event_generate('<<GRANT_ACCESS>>', state = 1, when='tail')
            else:
                self.cursor.execute("SELECT * FROM residents_db WHERE FINGER_TEMPLATE = %s", positionNumber)
                FingerprintThread.result = self.cursor.fetchone()
                print (FingerprintThread.result)
                if FingerprintThread.result:
                    self.app.event_generate('<<GRANT_ACCESS>>', state = 2, when='tail')
                else:
                    messagebox.showerror("Warning!","Your fingerprint is not yet registered!")

if __name__ == "__main__":
    import tkinter as tk

    def on_grant_access(event):
        print('on_grant_access()  positionNumber={},  accuracyScore={}'
              .format, fp.fingerprint[0], fp.fingerprint[1])

    root = tk.Tk()
    fp = FingerprintThread(root)
    root.bind('<<FINGERPRINT>>', on_grant_access)
    root.mainloop()

