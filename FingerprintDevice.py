from pyfingerprint.pyfingerprint import PyFingerprint
import threading, time

SEARCH = 1
REGISTER = 2


class FingerprintThread(threading.Thread):
    template = None
    
    def __init__(self, app):
        super().__init__(daemon=True)
        
        self.app = app
        self.f = None
        self._mode = None
        self._bind_funcid = None
        self._continue = threading.Event()
        
        # Default mode SEARCH
        self._set_mode(SEARCH)
        
        self.start()
    
    def bind(self, mode, callback):
        mode = {'SEARCH': SEARCH, 'REGISTER': REGISTER}.get(mode, None)
        self._set_mode(mode)
        self._bind_funcid = self.app.bind('<<FINGERPRINT>>', callback)
        
    def unbind(self):
        self.app.unbind('<<FINGERPRINT>>', self._bind_funcid)
        self._bind_funcid = None
        self._mode = SEARCH

    def _set_mode(self, mode):
        self._mode = mode
        self._continue.set()
    
    def delete_template(self, positionNumber):
        # wait readImage
        self._continue.clear()
        time.sleep(0.5)
        
        b = self.f.deleteTemplate(int(positionNumber))
        if b:
            print('FingerprintThread:Template deleted!')
        
        # continue readImage
        self._continue.set()
        return b
    
    def run(self):
        try:
            self.f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
            
            if not self.f.verifyPassword():
                raise ValueError('The given fingerprint sensor password is wrong!')
        
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
        
        print('Currently used templates: ' + str(self.f.getTemplateCount()) + '/' + str(self.f.getStorageCapacity()))
        
        # REGISTER sequence
        sequence = 1
        
        while True:  # mainloop forever
            retry = 0
            while True:  # retry
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
            
            position_number = None
            
            if self._mode == SEARCH:
                self.f.convertImage(1)
                FingerprintThread.template = self.f.searchTemplate()
                position_number = FingerprintThread.template[0]
            
            elif self._mode == REGISTER:
                if sequence == 1:
                    self.f.convertImage(1)
                    FingerprintThread.template = self.f.searchTemplate()
                    
                    # Checks if finger is already enrolled
                    positionNumber = FingerprintThread.template[0]
                    if positionNumber < 0:
                        # OK, no event, continue with sequence 2
                        position_number = None
                        sequence += 1
                    else:
                        # event state=-1 - finger allready enrolled
                        position_number = -1
                
                elif sequence == 2:
                    self.f.convertImage(2)
                    if self.f.compareCharacteristics():
                        self.f.createTemplate()
                        position_number = self.f.storeTemplate()
                    else:
                        # event state=-2 - .compareCharacteristics failed
                        position_number = -2
                    
                    # Reset MODE
                    sequence = 1
            
            if position_number is not None:
                self.app.event_generate('<<FINGERPRINT>>', when='tail', state=position_number)
                
                if self._mode == REGISTER:
                    # wait until set_mode(...) is called
                    self._continue.clear()
                    self._continue.wait()
            
            # Delay before next finger scan
            time.sleep(2)


if __name__ == "__main__":
    import tkinter as tk
    
    template_id = None
    
    
    def on_fingerprint(event):
        print('on_fingerprint()  positionNumber={}'.format(event.state))
        
        if event.state >= 0:
            global template_id
            template_id = event.state
            btn2.configure(text=btn2._text.format(template_id))
    
    
    def on_register():  # test MODE REGISTER
        global template_id
        template_id = None
        print('bind REGISTER')
        fp.bind('REGISTER', on_fingerprint)
    
    
    def on_delete():  # test delete_template
        if template_id is not None:
            print('delete_template({})'.format(template_id))
            fp.delete_template(template_id)
    
    
    root = tk.Tk()
    tk.Button(root, text='bind(REGISTER)', command=on_register).pack()
    btn2 = tk.Button(root, text='', command=on_delete)
    btn2._text = 'delete_template({})'
    btn2.configure(text=btn2._text.format(template_id))
    btn2.pack()
    
    fp = FingerprintThread(root)
    fp.bind('SEARCH', on_fingerprint)
    
    root.mainloop()
