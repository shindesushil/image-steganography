import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder


from functools import partial

import numpy as np
from PIL import Image
import os




def Decode(src):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))

    if "$t3g0" in message:
        return("Hidden Message:", message[:-5])
    else:
        return("No Hidden Message Found")


class Stegano:


    def __init__(self):
        print("Inside Stegano")

    
        
    

    # Method to encode
    def Encode(self, src, message, dest): 

        

        self.img = Image.open(src, 'r')
        self.width, self.height = self.img.size
        self.array = np.array(list(self.img.getdata()))

        if self.img.mode == 'RGB':
            n = 3
        elif self.img.mode == 'RGBA':
            n = 4
        self.total_pixels = self.array.size//n

        message += "$t3g0"
        self.b_message = ''.join([format(ord(i), "08b") for i in message])
        self.req_pixels = len(self.b_message)

        if self.req_pixels > self.total_pixels:
            print("Error : Larger File Required")
        else:
            index=0
            for p in range(self.total_pixels):
                for q in range(0, 3):
                    if index < self.req_pixels:
                        self.array[p][q] = int(bin(self.array[p][q])[2:9] + self.b_message[index], 2)
                        index += 1


        self.array=self.array.reshape(self.height, self.width, n)
        self.enc_img = Image.fromarray(self.array.astype('uint8'), self.img.mode)
        self.enc_img.save(dest)

    async def Decode(self, src):

        print(src)
        img = Image.open(src, 'r')
        array = np.array(list(img.getdata()))

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4

        total_pixels = array.size//n

        hidden_bits = ""
        for p in range(total_pixels):
            for q in range(0, 3):
                hidden_bits += (bin(array[p][q])[2:][-1])

                hidden_bits += (bin(array[p][q])[2:][-1])
        hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

        message = ""
        for i in range(len(hidden_bits)):
            if message[-5:] == "$t3g0":
                break
            else:
                message += chr(int(hidden_bits[i], 2))

         
        if "$t3g0" in message:
            return ("Hidden Message:", message[:-5])
        else:
            print(message[:-5])
            return("No Hidden Message Found")
    






class PopupBox:
    def __init__(self, **kwargs):
        super(PopupBox, self).__init__(**kwargs)

    def showMessage(self, msg):
        self.layout = GridLayout(cols = 1, padding = 10, spacing = 5)

        
        self.message = Label(text = msg)
        self.btnClose = Button(text = "Close")
        self.btnClose.size_hint = None, None
        self.btnClose.size = 150,50

        self.btnClose.bind(on_press = self.dismiss)

        self.layout.add_widget(self.message)
        self.layout.add_widget(self.btnClose)


    def dismiss(self):
        self.popup.dismiss()
        




class DataKeeper:
    encodedFile = None
    inFilePath = None
    filePath = None
    messageData = None
    outFilePath = ""

    def __init__(self, **kwargs):
        super(DataKeeper, self).__init__(**kwargs)

        self.layout = GridLayout(cols = 1, padding = 10, spacing = 5)

        self.outFileName = TextInput(hint_text = "File Name", multiline = False)

        self.btnClose = Button(text = "Submit")
        self.btnClose.size_hint = None, None
        self.btnClose.size = 150,50

        self.btnClose.bind(on_press = partial(self.setName, self.outFileName.text))

        self.layout.add_widget(self.outFileName)
        self.layout.add_widget(self.btnClose)

        

        self.popup = Popup(title = "Enter File Name (Without Extension)", content = self.layout)
        self.popup.auto_dismiss = False
        self.popup.size_hint = 0.6, 0.4
        self.popup.pos_hint = {"x": 0.2, "top": 0.9}

    
    def getFileName(self):
        self.popup.open()
    
    def setName(self,instance,fileName):

        DataKeeper.encodedFile = self.outFileName.text
        print("out file name : ",self.outFileName.text)
        print("File path : ", DataKeeper.filePath)
        print("Message Data : ", DataKeeper.messageData)

        delimiter = chr(92)
        DataKeeper.outFilePath = os.path.join(DataKeeper.filePath, DataKeeper.encodedFile+ ".png")

        print("Out File Path : "+DataKeeper.outFilePath)

        # self.popup.dismiss()

        self.dismissPopup()

        Stegano().Encode(DataKeeper.inFilePath, DataKeeper.messageData, DataKeeper.outFilePath)


    
    def dismissPopup(self):
        self.popup.dismiss()

        # Call Encoding method

        # Encode(DataKeeper.inFilePath, DataKeeper.messageData, DataKeeper.messageData)



class HomeWindow(Screen):
    pass

class EncodeWindow(Screen):

    def __init__(self, **kwargs):
        super(EncodeWindow, self).__init__(**kwargs)
        self.inFile = ""
        self.outFile = ""

    def selected(self, filename):
        try:
            self.ids.filechooser._update_files()
            self.inFile = filename[0]
            DataKeeper.inFilePath = filename[0]
            DataKeeper.filePath = self.ids.filechooser.path
            #DataKeeper.messageData = self.ids.msgBox.text
            self.ids.my_image.source = self.inFile

        except:
            pass

    def handlePress(self, msg):

        print("Message : ",msg)
        DataKeeper.messageData = msg

        if DataKeeper.encodedFile is None:
            DataKeeper().getFileName()

        # delimiter = chr(92)
        # self.outFilePath = DataKeeper.filePath + "\\" +DataKeeper.encodedFile + ".png"
        # self.outFilePath = os.path.join(DataKeeper.filePath, DataKeeper.encodedFile + ".png")

        # print(self.outFilePath)
        

        


#decode window code here

class DecodeWindow(Screen):
    def selected(self, filename):
        try:
            self.ids.my_image.source = filename[0]
            self.decodeImage = filename[0]

        except:
            pass

    def decodeFunc(self, image):
        # self.msg = asyncio.run(Stegano().Decode(image))
        msg = Decode(image)
        self.ids.filechooser1._update_files()
        self.ids.msg.text = str(msg[0]+" "+msg[1])

        

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('design.kv')

class MyApp(App):
    def build(self):
        self.title = "Image Steganography"
        return kv


if __name__ == "__main__":
    MyApp().run()


