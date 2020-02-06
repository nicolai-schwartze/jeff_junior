import tkinter as tk
from PIL import Image, ImageTk
from copy import deepcopy
import cv2



class TemplateCalibrationApp:

    def __init__(self, window, templatePath):
        self.leftCameraIndex = 2
        self.camera = cv2.VideoCapture(self.leftCameraIndex)
        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        self.videoStreamStartStop = True
        self.videoStreamButtonText = "Start/Stop Video"
        self.rect_id = None
        self.frame = None
        self.window = window
        self.templatePath = templatePath
        
        # take first image
        self.img = self.camera.read()[1]
        self.img_blue = deepcopy(self.img[:,:,0])
        self.img_red = deepcopy(self.img[:,:,2])
        self.img[:,:,2] = self.img_blue
        self.img[:,:,0] = self.img_red
        self.img = Image.fromarray(self.img)
        
        # write first image to canvas
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas = tk.Canvas(self.window, width=self.img.width(), height=self.img.height(), borderwidth=0, highlightthickness=0)
        self.canvas.pack(expand=True)
        self.canvas.img = self.img  # Keep reference in case this code is put into a function.
        self.img_on_canvas = self.canvas.create_image(0, 0, image=self.img, anchor=tk.NW)
        
        # create, attach and pack buttons
        self.startStopVideoStreamButton = tk.Button(self.window, text=self.videoStreamButtonText, command=self.start_stop_VideoStream)
        self.startStopVideoStreamButton.pack()
        self.redTemplateButton = tk.Button(self.window, text="Create Red Template", fg='red', command=self.createRedTemplate)
        self.redTemplateButton.pack()
        self.greenTemplateButton = tk.Button(self.window, text="Create Green Template", fg='green', command=self.createGreenTemplate)
        self.greenTemplateButton.pack()
    
        # Create selection rectangle (invisible since corner points are equal).
        self.rect_id = self.canvas.create_rectangle(self.topx, self.topy, self.topx, self.topy, dash=(2,2), fill='', outline='black')
        
        self.canvas.bind('<Button-1>', self.get_mouse_posn)
        self.canvas.bind('<B1-Motion>', self.update_sel_rect)

    def get_mouse_posn(self, event):
        self.topx, self.topy = event.x, event.y
    
    def update_sel_rect(self, event):
        self.rect_id
        self.topy, self.topx, self.botx, self.boty
    
        self.botx, self.boty = event.x, event.y
        self.canvas.coords(self.rect_id, self.topx, self.topy, self.botx, self.boty)  # Update selection rect.
        
    # video stream function
    def videoStream(self):
        self.frame = self.camera.read()[1]
        self.vid = deepcopy(self.frame)
        self.vid_blue = deepcopy(self.vid[:,:,0])
        self.vid_red = deepcopy(self.vid[:,:,2])
        self.vid[:,:,2] = self.vid_blue
        self.vid[:,:,0] = self.vid_red
        self.vid = Image.fromarray(self.vid)
        
        self.img2 = ImageTk.PhotoImage(self.vid)
        self.canvas.img = self.img2
        self.canvas.itemconfig(self.img_on_canvas, image = self.img2)
        
        if self.videoStreamStartStop:
            self.window.after(100, self.videoStream)
    
    
    def start_stop_VideoStream(self):
        if self.videoStreamStartStop:
            self.videoStreamStartStop = False
        else:
            self.videoStreamStartStop = True
            self.window.after(100, self.videoStream)
            
            
    def createRedTemplate(self):
        capture = self.frame[self.topy:self.boty,self.topx:self.botx,:]
        cv2.imwrite(self.templatePath + "red_template.png", capture)
        print("created red template")
        
    def createGreenTemplate(self):
        capture = self.frame[self.topy:self.boty,self.topx:self.botx,:]
        cv2.imwrite(self.templatePath + "green_template.png", capture)
        print("created green template")


if __name__ == "__main__":
    
    WIDTH, HEIGHT = 640, 570
    templatePath = "./"
    window = tk.Tk()
    window.title("Configurate Laser Template")
    window.geometry('%sx%s' % (WIDTH, HEIGHT))
    window.configure(background='grey')
    
    appWindow = TemplateCalibrationApp(window, templatePath)
    
    appWindow.videoStream()
    window.mainloop()
    print("closing template creation app")