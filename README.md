## Analysis of Buddha Images Around the Phra Pathom Chedi Using Feature Matching

A computer vision project for identifying Buddha statues at Phra Pathom Chedi using image feature matching techniques.

--- 

## 🎯 **Project Overview**

This project focuses on the recognition of Buddha statues around **Phra Pathom Chedi** by detecting and matching image features. A dataset was created from real-world photos taken around the site, and green screen techniques were applied to standardize backgrounds and improve detection performance.

--- 

## ⚙️ **Workflow**

1. **Data Collection**  
   - Photographs of Buddha statues were taken from various locations around Phra Pathom Chedi.

2. **Image Preprocessing**  
   - Backgrounds were manually turned into green screen using **Paint**, **Photoshop**, or similar tools.

3. **Metadata Annotation**  
   - A `buddha_names.txt` file maps image filenames to their corresponding Buddha statue names.

4. **Feature Detection & Matching**  
   - Uses the following algorithms:
     - ORB
     - AKAZE
     - KAZE
     - SIFT  
   - Input images are compared against the dataset to find the most similar match.

5. **Similarity Scoring**  
   - Outputs the matched image, the statue name, and a similarity score.

6. **GUI Interface**  
   - Built with **Tkinter**:
     - Upload an image
     - Run matching
     - See the result with matched name and score

--- 

## 🔧 **Tech Stack**

- **OpenCV**
- **Pillow**
- **Tkinter**
- **JSON**
