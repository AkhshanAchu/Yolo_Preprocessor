import xml.etree.ElementTree as ET
import glob
import os
import shutil
import yaml

class xml_txt:
    def __init__(self,input_dir,output_dir,image_dir,format,classes=[],yolo=5,train_ratio=0.7):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.image_dir = image_dir
        self.format = format
        self.classes=classes
        self.train_ratio = train_ratio

        if yolo == 7:
            print("MODEL : Yolov7")
            shutil.copytree("models/yolov7","yolov7")
            self.base = "yolov7"
        if yolo == 5:
            print("MODEL : Yolov5")
            shutil.copytree("models/yolov5","yolov5")
            self.base = "yolov5"
              
        self.image_train = os.path.join(self.base,"custom_dataset","images","train")
        self.image_test = os.path.join(self.base,"custom_dataset","images","test")
        self.label_train = os.path.join(self.base,"custom_dataset","labels","train")
        self.label_test = os.path.join(self.base,"custom_dataset","labels","test")
        self.y_image_train = os.path.join("custom_dataset","images","train")
        self.y_image_test = os.path.join("custom_dataset","images","test")
        self.y_label_train = os.path.join("custom_dataset","labels","train")
        self.y_label_test = os.path.join("custom_dataset","labels","test")

        self.file_creaters()
        

        
    def file_creaters(self):

        print("\nCreating Directories")
        if not os.path.exists(self.image_train):
            os.mkdir(os.path.join(self.base,"custom_dataset"))
            os.mkdir(os.path.join(self.base,"custom_dataset","images"))
            os.mkdir(self.image_train)
        if not os.path.exists(self.image_test):
            os.mkdir(self.image_test)
        if not os.path.exists(self.label_train):
            os.mkdir(os.path.join(self.base,"custom_dataset","labels"))
            os.mkdir(self.label_train)
        if not os.path.exists(self.label_test):
            os.mkdir(self.label_test)
        print("Done...")
        self.iter()
    
    def xml_to_yolo_bbox(self,bbox, w, h):
        # xmin, ymin, xmax, ymax
        x_center = ((bbox[2] + bbox[0]) / 2) / w
        y_center = ((bbox[3] + bbox[1]) / 2) / h
        width = (bbox[2] - bbox[0]) / w
        height = (bbox[3] - bbox[1]) / h
        return [x_center, y_center, width, height]

    def iter(self):
        if self.format:
            files = glob.glob(os.path.join(self.input_dir, '*.txt'))
            self.in_yolo(files)
        else:
            files = glob.glob(os.path.join(self.input_dir, '*.xml'))
            self.in_other(files)
        self.class_file() 

    def in_other(self,files):
        print("\nConverting .xml and Train test Split")
        cutter = 0
        l = len(files)
        self.classes=[]
        trainer = open(os.path.join(self.base,"custom_dataset","train.txt"))
        tester = open(os.path.join(self.base,"custom_dataset","test.txt"))
        for fil in files:
            basename = os.path.basename(fil)
            filename = os.path.splitext(basename)[0]
            # check if the label contains the corresponding image file
            if not os.path.exists(os.path.join(self.image_dir, f"{filename}.jpg")):
                print(f"{filename} image does not exist!")
                continue

            result = []
            cutter+=1
            # parse the content of the xml file
            tree = ET.parse(fil)
            root = tree.getroot()
            width = int(root.find("size").find("width").text)
            height = int(root.find("size").find("height").text)

            for obj in root.findall('object'):
                label = obj.find("name").text
                # check for new classes and append to list
                if label not in self.classes:
                    self.classes.append(label)
                index = self.classes.index(label)
                pil_bbox = [int(x.text) for x in obj.find("bndbox")]
                yolo_bbox = self.xml_to_yolo_bbox(pil_bbox, width, height)
                # convert data to string
                bbox_string = " ".join([str(x) for x in yolo_bbox])
                result.append(f"{index} {bbox_string}")

            if result:
                if cutter < self.train_ratio*l:
                # generate a YOLO format text file for each xml file
                    with open(os.path.join(self.label_train, f"{filename}.txt"), "w", encoding="utf-8") as f:
                        f.write("\n".join(result))
                    shutil.copy2(os.path.join(self.image_dir, f"{filename}.jpg"),os.path.join(self.image_train, f"{filename}.jpg"))
                    trainer.write("\n")
                    trainer.write(os.path.join(self.y_image_train, f"{filename}.jpg"))

                else:
                # generate a YOLO format text file for each xml file
                    with open(os.path.join(self.label_test, f"{filename}.txt"), "w", encoding="utf-8") as f:
                        f.write("\n".join(result))
                    shutil.copy2(os.path.join(self.image_dir, f"{filename}.jpg"),os.path.join(self.image_test, f"{filename}.jpg"))
                    tester.write("\n")
                    tester.write(os.path.join(self.y_image_test, f"{filename}.jpg"))
        trainer.close()
        tester.close()
        print("Done....")
    

    def in_yolo(self,files):
        print("\nCreating Train Test Split...")
        cutter=0
        l=len(files)
        trainer = open(os.path.join(self.base,"custom_dataset","train.txt"),"a")
        tester = open(os.path.join(self.base,"custom_dataset","test.txt"),"a")
        for fil in files:
            basename = os.path.basename(fil)
            filename = os.path.splitext(basename)[0]
            # check if the label contains the corresponding image file
            if not os.path.exists(os.path.join(self.image_dir, f"{filename}.jpg")):
                print(f"{filename} image does not exist!")
                continue

            result = []
            cutter+=1


            if cutter < self.train_ratio*l:
                f = open(fil, "r")
                with open(os.path.join(self.label_train, f"{filename}.txt"), "w", encoding="utf-8") as z:
                        z.write(f.read())
                shutil.copy2(os.path.join(self.image_dir, f"{filename}.jpg"),os.path.join(self.image_train, f"{filename}.jpg")) 
                trainer.write("\n")
                trainer.write(os.path.join(self.y_image_train, f"{filename}.jpg"))
                
            else:
                f = open(fil, "r")
                with open(os.path.join(self.label_test, f"{filename}.txt"), "w", encoding="utf-8") as z:
                        z.write(f.read())
                shutil.copy2(os.path.join(self.image_dir, f"{filename}.jpg"),os.path.join(self.image_test, f"{filename}.jpg"))
                tester.write("\n")
                tester.write(os.path.join(self.y_image_test, f"{filename}.jpg"))
        trainer.close()
        tester.close()
        print("Done....")
    
    def class_file(self):
        print("\nCreating Class Files...")
        if self.base == "yolov5":
            d = {'path':".\custom_dataset","train":"images\\train","val":"images\\test",'names':{}}
            for i,j in enumerate(self.classes):
                d["names"][i] = j           
            with open(os.path.join(self.base,"custom_dataset","data.yaml"), 'w') as yaml_file:
                yaml.dump(d, yaml_file, default_flow_style=False)
        
        if self.base == "yolov7":
            another = open(os.path.join(self.base,"custom_dataset","classes.names"),"w")
            yml = open(os.path.join(self.base,"custom_dataset","data.yaml"),"w")
            for i in self.classes:
                another.write(i)
                another.write("\n")
            another.close()

            # d = {"train":".\custom_dataset\\train.txt","val":".\custom_dataset\\test.txt","nc":len(self.classes),'classes':str(self.classes)}
            # with open(os.path.join(self.base,"custom_dataset","data.yaml"), 'w') as yaml_file:
            #     yaml.dump(d, yaml_file, default_flow_style=False)
            data_yml = "train : {} \nval : {}\n\nnc : {}\n\nnames : {}".format(".\custom_dataset\\train.txt",".\custom_dataset\\test.txt",str(len(self.classes)),str(self.classes))
            yml.write(data_yml)
            yml.close()
        print("Done.....\n\nThe Files are created...")


        

        

                

