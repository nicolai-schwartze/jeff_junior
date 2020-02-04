import tkinter as tk
from PIL import Image, ImageTk
from copy import deepcopy
import cv2


WIDTH, HEIGHT = 640, 570
topx, topy, botx, boty = 0, 0, 0, 0
videoStreamStartStop = True
videoStreamButtonText = "Start/Stop Video"
rect_id = None
frame = None


def get_mouse_posn(event):
    global topy, topx

    topx, topy = event.x, event.y

def update_sel_rect(event):
    global rect_id
    global topy, topx, botx, boty

    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)  # Update selection rect.


if __name__ == "__main__":
    
    leftCameraIndex = 2
    camera = cv2.VideoCapture(leftCameraIndex)

    window = tk.Tk()
    window.title("Configurate Laser Template")
    window.geometry('%sx%s' % (WIDTH, HEIGHT))
    window.configure(background='grey')
    
    # take first image
    img = camera.read()[1]
    img_blue = deepcopy(img[:,:,0])
    img_red = deepcopy(img[:,:,2])
    img[:,:,2] = img_blue
    img[:,:,0] = img_red
    img = Image.fromarray(img)
    
    # write first image to canvas
    img = ImageTk.PhotoImage(img)
    canvas = tk.Canvas(window, width=img.width(), height=img.height(),
                       borderwidth=0, highlightthickness=0)
    canvas.pack(expand=True)
    canvas.img = img  # Keep reference in case this code is put into a function.
    img_on_canvas = canvas.create_image(0, 0, image=img, anchor=tk.NW)
    
    # video stream function
    def videoStream():
        global frame
        frame = camera.read()[1]
        vid = deepcopy(frame)
        vid_blue = deepcopy(vid[:,:,0])
        vid_red = deepcopy(vid[:,:,2])
        vid[:,:,2] = vid_blue
        vid[:,:,0] = vid_red
        vid = Image.fromarray(vid)
        
        img2 = ImageTk.PhotoImage(vid)
        canvas.img = img2
        canvas.itemconfig(img_on_canvas, image = img2)
        
        global videoStreamStartStop
        if videoStreamStartStop:
            window.after(100, videoStream)
    
    
    def start_stop_VideoStream():
        global videoStreamStartStop
        print(videoStreamStartStop)
        if videoStreamStartStop:
            videoStreamStartStop = False
        else:
            videoStreamStartStop = True
            window.after(100, videoStream)

        
    startStopVideoStreamButton = tk.Button(window, text=videoStreamButtonText, command=start_stop_VideoStream)
    startStopVideoStreamButton.pack()
    
    def createRedTemplate():
        global frame
        capture = frame[topy:boty,topx:botx,:]
        cv2.imwrite("./red_template.png", capture)
        print("created red template")
            
    redTemplateButton = tk.Button(window, text="Create Red Template", fg='red', command=createRedTemplate)
    redTemplateButton.pack()
    
    def createGreenTemplate():
        global frame
        capture = frame[topy:boty,topx:botx,:]
        cv2.imwrite("./green_template.png", capture)
        print("created green template")
            
    greenTemplateButton = tk.Button(window, text="Create Green Template", fg='green', command=createGreenTemplate)
    greenTemplateButton.pack()
    
    # Create selection rectangle (invisible since corner points are equal).
    rect_id = canvas.create_rectangle(topx, topy, topx, topy,
                                      dash=(2,2), fill='', outline='black')
    
    canvas.bind('<Button-1>', get_mouse_posn)
    canvas.bind('<B1-Motion>', update_sel_rect)
    
    videoStream()
    window.mainloop()
    print("closing template creation app")