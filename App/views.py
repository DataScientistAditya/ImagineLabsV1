from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from .form import PptForm
from .Apify.Fetchdocs import FetchDocuments
from .Apify.CreateDocs import CreateDocument
from pathlib import Path
from django.core.files import File
from .models import PptData
import os
from django.core.files import File
# Create your views here.


def Home(request):
    context = {}
    try:
        if request.method == "POST":
            PptForms = PptForm(request.POST)
            if PptForms.is_valid():
                #print("form is vaild")
                Learn = PptForms.cleaned_data['Query']
                LaymanTerm = PptForms.cleaned_data['isLayman']
                if LaymanTerm != " ":
                    if LaymanTerm == True:
                        FetchData = FetchDocuments(Learn, "yes")
                        PptTextContent, Title, ImageLists = FetchData.GetCleanedFetchedData()    
                        #print("gets input value")
                    else:
                        FetchData = FetchDocuments(Learn, "no")
                        PptTextContent, Title, ImageLists = FetchData.GetCleanedFetchedData() 
                print("Getting Ppt docs")
                if Title is not None:
                    print("Creating slides")
                    Split = Learn.split()
                    PPtNameSplit = "".join(Split)
                    PptCreateObj = CreateDocument(PptTextContent,ImageLists,Title,PPtNameSplit)
                    PptCreateObj.CreateFirstSlide()
                    Filename = PptCreateObj.CreatePPT()
                    print("File name is {0}".format(Filename))
                    PptForms.save()
                    Pptid = PptData.objects.filter(Query = Learn).values("id").last()["id"]
                    PptObj = PptData.objects.get(id = Pptid)
                    Folderdir = os.getcwd()
                    PdfFilePath = Folderdir + "\\{0}".format(Filename)
                    path = Path(PdfFilePath)
                    with path.open(mode='rb') as f:
                        PptObj.FileLoc = File(f,name=path.name)
                        PptObj.save()
                    #LocData = PptFileLocation(Query = PptObj, FileLoc  =)
                    print("Complete Creating slides")
                    return redirect("/GetAllDocs")
                else:
                    return HttpResponse("Please Use some other tags for your search, we are unable to find any outputs for your search")
            else:
                return HttpResponse("Form is not Valid")
        else:
            PptForms = PptForm()
            context['PptForm'] = PptForms
        return render(request,'Home/Home.html',context=context)
    except:
        return HttpResponse("somthing went wrong, please try with some other keywords")

def GetAllDocs(request):
    try:
        Context ={}
        Data = PptData.objects.all().values("Query","FileLoc").order_by("-id")
        Context["Data"] = Data
        return render(request,"Dash/Dash.html",context=Context)
    except:
        return HttpResponse("somthing went wrong, please try with some other keywords")