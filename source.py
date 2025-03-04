import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, ttk
import tkinter.font as font
from PIL import Image, ImageTk
import os
import cv2
import json
from ttkthemes import ThemedTk


def select_image():
    global file_path, img1
    button2.config(text = 'Check')
    button1.config(text = "Select A Image")
    try:
        file_path = filedialog.askopenfilename(title='Select A File')
        image = Image.open(file_path)
        
        img1 = cv2.imread(file_path)
        w, h, c = img1.shape
        if w > h:
            image = image.rotate(-90)
        image = image.resize((430, 450))
        
        photo = ImageTk.PhotoImage(image)
        img1_label.config(image=photo)
        img1_label.image = photo
        path_label.config(text='Directory : ' + file_path, font = ('Verdana', 9))
        label1.config(text = '')
        label2.config(text = '')
        label3.config(text = '')
        label5.config(text = '')
        textbox1.place(width=0)
        textbox2.place(width=0)
        textbox3.place(width=0)
    except Exception as err:
        print(err)
        button1.config(text = "Cannot read image")


def Process(selected_algorithm):
    global file_path, result_path, img1, main_image_name, image_similarity, image_good_matches, best_match
    button2.config(text = 'Check')
    try:
        # resize image
        scale_percent = 40 # percent of original size
        width = int(img1.shape[1] * scale_percent / 100)
        height = int(img1.shape[0] * scale_percent / 100)
        dim = (width, height)
        img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
        
        # Find Image's key and descriptor
        algos = {'ORB                             *' : cv2.ORB_create(),
                 'KAZE' : cv2.KAZE_create(),
                 'SIFT' : cv2.SIFT_create(),
                 'AKAZE' : cv2.AKAZE_create()}
        
        algorithm = algos[selected_algorithm]
        print(f'Algorithm : {selected_algorithm}')
        kp1, des1 = algorithm.detectAndCompute(img1, None)
        
        # Data Storages
        main_image_name = []
        image_matches = []
        image_good_matches = []
        kps2 = []
        desor2 = []
        good_match_list = []
        image_similarity = []
        ## Read Main Image
        print('\n')
        print(' --------------- Processing --------------- ')
        for main in main_file_list:
            print(f'Reading {main}')
            img2 = cv2.imread(filename = os.path.join(path, main), flags = 0)
            kp2, des2 = algorithm.detectAndCompute(img2, None)
            matcher = cv2.BFMatcher()
            matches = matcher.knnMatch(des1, des2, k=2)
            threshold = 0.75
            good_matches = []
            for m, n in matches:
                if m.distance < threshold*n.distance:
                    good_matches.append([m])
            print(f'Good Matches : {len(good_matches)}')
            
            # Store all Output into Data storages
            try:
                similarity = (len(good_matches) / len(matches)) * 100
                similarity = round(similarity, 2)
                image_similarity.append(similarity)
                print(f'Match Percentages : {similarity:.2f}%')
            except:
                image_similarity.append('0%')
            image_matches.append(len(matches))
            kps2.append(kp2)
            desor2.append(des2)
            main_image_name.append(main)
            image_good_matches.append(len(good_matches))
            good_match_list.append(good_matches)
    
        best_match = image_good_matches.index(max(image_good_matches))
        print('\n')
        print(' --------------- Result --------------- ')
        print(f'Best Match Image : {main_image_name[best_match]} \nMatch Percentage : {image_similarity[best_match]}%\nGood Matches : {image_good_matches[best_match]}')
        
        # Read the best match to show the result

        show_result()
        best_match_image = cv2.imread(os.path.join(path, main_image_name[best_match]), 0)
        matching_result = cv2.drawMatchesKnn(img1, kp1, best_match_image, kps2[best_match], good_match_list[best_match], None, flags = 2)
        
        result_path = 'Matching_Result.jpg'
        cv2.imwrite(result_path, matching_result)
        image = Image.open(result_path)
        image = image.resize((700, 450))
        photo = ImageTk.PhotoImage(image)
        img1_label.config(image=photo)
        img1_label.image = photo
        
    except Exception as err:
        print(err)
        button2.config(text = 'Image not found')
    

def show_result():
    global size1, size2, size3, word1, word2, word3, w1, w2, w3, count1, count2, count3, scriptpath
    
        # Reading text file
    with open(scriptpath + r'\buddha_names.txt', 'r', encoding='utf-8') as names:
        data = json.load(names)
    
    picture_name = []
    thai_name = []
    
    for i in data['buddha']:
        picture_name.append(i['picture_name'])
        thai_name.append(i['thai_name'])
    
    result = thai_name[picture_name.index(main_image_name[best_match])]

    label5.config(text = 'Matcing Result')
    
    #Animation Box
    if size1 < 160:
        size1 += 20
        textbox1.place(x = 750, y = 210, width = size1, height = 30)
        window.after(1, show_result)
    elif size2 < 160:
        size2 += 20
        textbox2.place(x = 750, y = 310, width = size2, height = 30)
        window.after(1, show_result)
    elif size3 < 160:    
        size3 += 20
        textbox3.place(x = 750, y = 410, width = size3, height = 30)
        window.after(1, show_result)
    
    
    #Animation Text
    if  size1 == 160 and len(word1) != len(w1):
        w1.append(word1[count1])
        label1.config(text = w1)
        count1 += 1
        window.after(500, show_result)
        
    elif  size2 == 160 and len(word2) != len(w2):
        w2.append(word2[count2])
        label2.config(text = w2)
        count2 += 1
        window.after(500, show_result)
        
    elif  size3 == 160 and len(word3) != len(w3):
        w3.append(word3[count3])
        label3.config(text = w3)
        count3 += 1
        window.after(500, show_result)

    entryText1.set(result)
    entryText2.set(image_similarity[best_match])
    entryText3.set(image_good_matches[best_match])
    
#Starting program
#Uploading green_screen images (main_image)
scriptpath = os.getcwd() + r'\data'
picpath = r'\ImgGreen'
path = scriptpath + picpath
main_file_list = []
for main_img in os.listdir(path):
    if main_img.endswith('.jpg') or main_img.endswith('.jpeg') or main_img.endswith('.png'):
        main_file_list.append(main_img)


size1 = 0
size2 = 0
size3 = 0
word1 = list('Thai_name')
word2 = list('Similarity')
word3 = list('Similar_points')
w1 = []
w2 = []
w3 = []
count1 = 0
count2 = 0
count3 = 0


# GUI
window = ThemedTk(theme = "adapta")
window.iconbitmap(scriptpath + r'\icon.ico')
window.title('pip install')
window.geometry('1000x600')
window.resizable(False, False)

#Seleting button
button1 = ttk.Button(window, text="Select A Image", command=select_image)
button1.place(width=200, height=60, x=50,y=40)

#Combo box
combox = ttk.Combobox(window, values = ['ORB                             *', 'KAZE', 'SIFT', 'AKAZE'])
combox.current(0)
combox.place(width= 125, height = 25, x = 825, y = 10)

#Process button
button2 = ttk.Button(window, text="Check", command=lambda : Process(combox.get()))
button2.place(width = 200, height = 60, x = 750, y = 40)

#Image label
img1_label = ttk.Label(window, text = '')
img1_label.place(x=30,y=115)

#Path label
path_label = ttk.Label(window, text = '')
path_label.place(x = 30, y = 570)

#'Thai_name' label
label1 = tk.Label(window, text = '', font = ('Verdana', 10))
label1.place(x = 755, y = 190)

#Thai_name box
entryText1 = tk.StringVar()
textbox1 = ttk.Entry(window, textvariable = entryText1, font = ('Verdana', 9))
textbox1.place(x = 750, y = 210, width = size1, height = 35)

#'Similarity' label
label2 = tk.Label(window, text = '', font = ('Verdana', 10))
label2.place(x = 755, y = 290)

#Similarity box
entryText2 = tk.StringVar()
textbox2 = ttk.Entry(window, textvariable=entryText2, font = ('Verdana', 9))
textbox2.place(x = 750, y = 310, width = size2, height = 35)

#'Match Points' label
label3 = tk.Label(window, text = '', font = ('Verdana', 10))
label3.place(x = 755, y = 390)

#Match Points box
entryText3 = tk.StringVar()
textbox3 = ttk.Entry(window, textvariable=entryText3, font = ('Verdana', 9))
textbox3.place(x = 750, y = 410, width = size3, height = 35)

#Combo label
label4 = tk.Label(window, text = 'Algorithm : ', font = ('Verdana', 9))
label4.place(x = 750, y = 12)

#'Matching Result' label
label5 = tk.Label(window, text = '', font = ('Verdana', 15, 'underline'))
label5.place(x = 754, y = 150)

window.mainloop()

try:
    os.remove(result_path)
except:
    pass