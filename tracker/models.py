from django.db import models
from django.utils import timezone
from datetime import timedelta

#list of valid states
class Status(models.TextChoices):
    SAVED = "saved", "Saved"
    APPLIED = "applied", "Applied"
    OA = "oa", "Online Assessment"
    INTERVIEW = "interview", "Interview",
    OFFER = "offer", "Offer"
    REJECTED = "rejected", "Rejected"

#Transition rules. each value is a list of states you are allowed to move to
ALLOWED_TRANSITIONS = {
    Status.SAVED: [Status.APPLIED],
    Status.APPLIED: [Status.OA, Status.INTERVIEW, Status.REJECTED],
    Status.OA: [Status.REJECTED, Status.INTERVIEW],
    Status.INTERVIEW: [Status.REJECTED, Status.OFFER],
    Status.OFFER: [],
    Status.REJECTED: []
}    

class Posting(models.Model): # defiines a table called Posting
    company = models.CharField(max_length = 200)
    title = models.CharField(max_length = 200)
    location = models.CharField(max_length = 200, blank = True) #blank = True makes the field optional; allows the field to be empty. Text fields use blank. #null = True means the database can store "nothing". Date fields use null.
    term = models.CharField(max_length = 50, blank = True)
    url = models.URLField(blank = True)
    closes_at = models.DateField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True) #a timestamp django fills automatically, the moment when a row is created.
    content_hash = models.CharField(max_length = 64, blank = True, default = "", db_index = True)

    def __str__(self):
        return f"{self.title} at {self.company}" #Tells django how to label a posting in plain english.

class Application(models.Model):
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE) #ForeignKey is a one-to-many relationship. One posting can have many applications. on_delete=models.CASCADE means if the posting is deleted, all applications for that posting will be deleted too.
    
    status = models.CharField(max_length = 50, choices = Status.choices, default=Status.SAVED) #updated default to Status.SAVED, to always begin a new application at "saved"
    #added 'choices = Status.choices' to obtain a proper dropdown, in the admin, with 6 valid values which are saved, applied, oa, interview, offer, rejected.
    notes = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Application for {self.posting.title} at {self.posting.company}"

    def transition_to(self, new_status):
        if new_status not in ALLOWED_TRANSITIONS[self.status]:
            raise ValueError("status is seen to be moving to an illegal destination, thus blocked")
        
        else:
            StatusEvent.objects.create(application = self, from_status = self.status, to_status = new_status)
            self.status = new_status
            self.save()
    @property
    def is_new(self):
        return timezone.now() - self.created_at < timedelta(hours = 24)
    
        


class StatusEvent(models.Model):
    application = models.ForeignKey(Application, on_delete = models.CASCADE)

    from_status = models.CharField(max_length = 50, choices = Status.choices)

    to_status = models.CharField(max_length = 50, choices= Status.choices)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"This application went from {self.from_status} to {self.to_status} at {self.created_at}"