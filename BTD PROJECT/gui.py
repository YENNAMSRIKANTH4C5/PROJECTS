import tkinter
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2 as cv
from frames import Frames
from displayTumor import DisplayTumor
from predictTumor import predictTumor


class Gui:
    def __init__(self):
        self.MainWindow = tkinter.Tk()
        self.MainWindow.geometry('1200x720')
        self.MainWindow.resizable(width=False, height=False)
        self.MainWindow.title("Brain Tumor Detection System")

        self.DT = DisplayTumor()
        self.fileName = tkinter.StringVar()
        self.listOfWinFrame = []
        self.mriImage = None

        self.wHeight = 700
        self.wWidth = 1180

        self.FirstFrame = Frames(self, self.MainWindow, self.wWidth, self.wHeight, 0, 0)
        self.FirstFrame.btnView['state'] = 'disable'
        self.listOfWinFrame.append(self.FirstFrame)

        # Title Label
        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Brain Tumor Detection", height=1, width=40)
        WindowLabel.place(x=320, y=30)
        WindowLabel.configure(background="red", font=("Comic Sans MS", 16, "bold"))

        self.val = tkinter.IntVar()
        RB1 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="Detect Tumor", variable=self.val,
                                  value=1, command=self.check)
        RB1.place(x=250, y=200)
        RB2 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="View Tumor Region",
                                  variable=self.val, value=2, command=self.check)
        RB2.place(x=250, y=250)

        browseBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Browse", width=8, command=self.browseWindow)
        browseBtn.place(x=800, y=550)

        self.MainWindow.mainloop()

    def browseWindow(self):
        FILEOPENOPTIONS = dict(defaultextension='*.*',
                               filetypes=[('JPG Files', '*.jpg'), ('PNG Files', '*.png'), ('JPEG Files', '*.jpeg'), ('All Files', '*.*')])
        file_path = filedialog.askopenfilename(**FILEOPENOPTIONS)
        if file_path:
            self.fileName.set(file_path)
            image = Image.open(file_path)
            self.mriImage = cv.imread(file_path, 1)
            self.listOfWinFrame[0].readImage(image)
            self.listOfWinFrame[0].displayImage()
            self.DT.readImage(image)

    def check(self):
        if self.mriImage is None:
            print("Please select an image first.")
            return

        if self.val.get() == 1:
            self.listOfWinFrame = [self.FirstFrame]
            self.listOfWinFrame[0].setCallObject(self.DT)
            pred = 0.0
            res = predictTumor(self.mriImage)
            res = float(res) if isinstance(res, (int, float)) else float(res[0][0])  # Ensure float value
            accuracy = round(res * 100, 2)  # Convert to percentage and round of
            pred = accuracy 
            if pred > 98:
                tumor_status = "Tumor Detected"
                color = "red"
            else:
                tumor_status = "No Tumor"
                color = "green"

            # Label to show tumor detection status
            resLabel = tkinter.Label(self.FirstFrame.getFrames(), text=tumor_status, height=1, width=20)
            resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg=color)
            resLabel.place(x=700, y=450)

            # Label to show accuracy percentage
            accuracyLabel = tkinter.Label(self.FirstFrame.getFrames(), text=f"Accuracy: {accuracy}%", height=1, width=20)
            accuracyLabel.configure(background="White", font=("Comic Sans MS", 14, "bold"), fg="blue")
            accuracyLabel.place(x=700, y=500)

        elif self.val.get() == 2:
            self.listOfWinFrame = [self.FirstFrame]
            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)

            secFrame = Frames(self, self.MainWindow, self.wWidth, self.wHeight, self.DT.displayTumor, self.DT)
            self.listOfWinFrame.append(secFrame)

            for i in range(len(self.listOfWinFrame)):
                if i != 0:
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()

            if len(self.listOfWinFrame) > 1:
                self.listOfWinFrame[0].btnView['state'] = 'active'

        else:
            print("Not Working")


# Run the GUI
if __name__ == "__main__":
    mainObj = Gui()
