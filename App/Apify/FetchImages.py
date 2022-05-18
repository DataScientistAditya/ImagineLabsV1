from simple_image_download import simple_image_download as smp
import os
from PIL import Image

class FetchImages():
    
    def __init__(self,quary):
        self.quary = quary
        
    def Downlaod_Images(self):    
        lst = []
        spltstr = self.quary.split()
        newstr = "".join(spltstr)
        lst.append(newstr)
        print(lst)
        
        res = smp.Downloader()
        for i in lst:
            res.download(keywords=i,limit=4)
        
        Folderdir = os.getcwd()
        ImageFolder = Folderdir + "\\simple_images\\{0}".format(newstr)
        ListofImages = []
        
        for imgs in os.listdir(ImageFolder):
            ListofImages.append(imgs)
        
        List_of_Image_Loc = []       
        for j in ListofImages:
            Local_Loc = ImageFolder + "\\{0}".format(j)
            image = Image.open(Local_Loc)
            width, height = image.size
            if width >200:
                List_of_Image_Loc.append(Local_Loc)
        return List_of_Image_Loc
                
            
            
        
    
    