#  YOLO Preprocessor

>  **Transform your dataset into YOLO-ready format with just a few clicks!**

A powerful web-based preprocessing application that streamlines data preparation for YOLOv5 and YOLOv7 training. Say goodbye to manual annotation conversion! 

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-green.svg)](https://flask.palletsprojects.com/)
[![YOLO](https://img.shields.io/badge/YOLO-v5%20%7C%20v7-orange.svg)](https://github.com/ultralytics/yolov5)

---

## Features

| Feature | Description | Status |
|---------|-------------|---------|
| **Format Conversion** | XML → YOLO format conversion | ✅ |
| **Train-Test Split** | Automatic dataset splitting | ✅ |
| **Batch Processing** | Handle multiple files at once | ✅ |
| **Ready-to-Train** | YOLOv5 & YOLOv7 compatible output | ✅ |
| **Web Interface** | User-friendly drag & drop | ✅ |
| **Chunked Upload** | Large file support | ✅ |

---

### The Process

1. ** Upload** your ZIP file containing images + XML annotations
2. ** Configure** your YOLO version, classes, and split ratio  
3. ** Convert** XML annotations to YOLO format automatically
4. ** Split** dataset into training and testing sets
5. ** Organize** files into proper directory structure
6. ** Download** your ready-to-train dataset!

---

## Installation & Setup

### Prerequisites

```bash
# Required: Python 3.x
python --version  # Should be 3.x+
```

###  Quick Start

```bash
#  Clone the repository
git clone https://github.com/AkhshanAchu/Yolo_Preprocessor.git
cd Yolo_Preprocessor

# Install dependencies
pip install flask pathlib

# Run the application
python app.py
```

### Access the App
Open your browser and navigate to: **http://localhost:5000** 🎉

---

## How to Use

### 📂 Step 1: Prepare Your Data
Create a ZIP file with this structure:
```
📦 your_dataset.zip
├── 📁 images/
│   ├──  image1.jpg
│   ├──  image2.jpg
│   └── ...
└── 📁 labels/
    ├──  image1.xml
    ├──  image2.xml
    └──  ...
```

### Step 2: Configure & Process

1. ** Upload**: Drag & drop your ZIP file
2. ** Target**: Choose YOLOv5 (5) or YOLOv7 (7)
3. ** Classes**: Enter class names: `person,car,bicycle,dog`
4. ** Split Ratio**: Set training ratio: `0.8` (80% train, 20% test)
5. ** Process**: Hit submit and watch the magic happen! 

### Step 3: Download Results

Get your perfectly formatted dataset ready for training!

---

## 📁 Output Structure

### For YOLOv5:
```
 yolov5/
├── 📁 images/
│   ├── 📁 train/ 
│   └── 📁 val/ 
├── 📁 labels/
│   ├── 📁 train/ 
│   └── 📁 val/ 
└── 📄 data.yaml 
```

###  For YOLOv7:
```
 yolov7/
├── 📁 images/
│   ├── 📁 train/ 
│   └── 📁 val/ 
├── 📁 labels/
│   ├── 📁 train/ 
│   └── 📁 val/ 
└──  data.yaml 
```

---

## Configuration Options

| Parameter | Description | Example |
|-----------|-------------|---------|
| **YOLO Version** | Target YOLO model | `5` or `7` | 
| **Classes** | Object classes | `person,car,bicycle` |
| **Train Ratio** | Training split | `0.8` (80% train) |

---

## Ready to Get Started?

**Transform your dataset today and start training amazing YOLO models!** 

[![Get Started](https://img.shields.io/badge/Get%20Started-Now!-brightgreen.svg?style=for-the-badge)](https://github.com/AkhshanAchu/Yolo_Preprocessor)

---
