from bing_image_downloader import downloader
import os
from PIL import Image

class FetchImages():
    
    def __init__(self,quary):
        self.quary = quary
        
    def Downlaod_Images(self):    
        lst = []
        try:
            spltstr = self.quary.split()
            newstr = "".join(spltstr)
            lst.append(newstr)
            print(lst)
        except:
            newstr = self.quary
        
        downloader.download(newstr,limit=2,adult_filter_off=True, force_replace=False, timeout=60)
        
        Folderdir = os.getcwd()
        ImageFolder = Folderdir + "\\dataset\\{0}".format(newstr)
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
                
            
            
        
    
    