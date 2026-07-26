'''
from django.http import HttpResponse

# Create your views here.
def application_list(request):
    return HttpResponse("This is my applications page, built by me!")

#A view is just a function that takes a request and returns a response
'''


#Updating the view to fetch data

from django.shortcuts import render, get_object_or_404, redirect
from .models import Application, ALLOWED_TRANSITIONS
from .forms import PostingForm

def application_list(request):
    applications = Application.objects.all()  #this means give me all the rows in the Application table.
    return render(request, "tracker/application_list.html", {"applications": applications}) #render this template and pass this data

def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk) #fetch the one application with that id. If no such application exists, it automatically shows a clean "404 Not Found" page instead of crashing.

    if request.method == "POST":  #updating application_detail and putting the concept of POST in there to make buttons for legal next moves. Cuz buttons will POST. (reading = GET, changing = POST)
        new_status = request.POST.get("new_status")
        application.transition_to(new_status)
        return redirect(request.path)
    
    allowed = ALLOWED_TRANSITIONS[application.status]
    return render(request, "tracker/application_detail.html", {"application" : application, "allowed" : allowed,
    })

def add_application(request):
        if request.method == "POST":
            form = PostingForm(request.POST)
            if form.is_valid():
                posting = form.save()
                application = Application.objects.create(posting = posting)
                return redirect (f"/applications/{application.pk}/")
        else:
             form = PostingForm()
        return render(request, "tracker/add_application.html", {"form": form})
