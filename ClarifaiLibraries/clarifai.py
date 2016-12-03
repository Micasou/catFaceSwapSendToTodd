from clarifai.rest import ClarifaiApp
import Tkinter
import requests
words = []
subDict = None
class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"https://samples.clarifai.com/metro-north.jpg")

        button = Tkinter.Button(self,text=u"Generate Labels",
                                command=self.OnButtonClick)
        button.grid(column=1,row=0)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.labelVariable.set(u" ".join(words))

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnButtonClick(self):
        labels = self.labelImage(self.entryVariable.get())
        self.labelVariable.set(" ".join(words))
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnPressEnter(self,event):
        labels = self.labelImage(self.entryVariable.get())
        self.labelVariable.set(" \n".join(words))
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def labelImage(self, imageURL):
        app = ClarifaiApp()
        d = app.tag_urls([imageURL])  
        #output list, value
        count = 0

        for key, value in d.iteritems():
            if key == 'outputs':
                subDict = value
                break

        for i in subDict:
            for key, value in i.iteritems(): 
                if key == 'data':
                    subDict = value
                    break

        for key, value in subDict.iteritems(): 
            if key == 'concepts':
                subDict = value
                break

        for i in subDict:
            for key, value in i.iteritems():
                if key == 'name':
                    words.append(value)
                    if(len(words) % 4 == 0):
                        words.append('\n')
                    break
        return words

if __name__ == "__main__":

    raw = requests.get('http://www.facebook.com').text

    print raw

    app = simpleapp_tk(None)
    app.title('my application')
    app.mainloop()




