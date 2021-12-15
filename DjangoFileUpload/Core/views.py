from . import models
from django.shortcuts import render
from func.please_be_final import *

def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        document = models.Document(
            title=fileTitle,
            uploadedFile=uploadedFile
            # uploadedFile = uploadedFile + ".mp3"
        )
        document.save()
        a = predict_all_genre("func/xgb_model.model", path="media/Uploaded Files")
        print(a)

    documents = models.Document.objects.all()

    return render(request, "Core/upload-file.html", context={
        "files": documents
    })
