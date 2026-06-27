from django.db import models

# Create your models here.
class Contact(models.Model):
    SUBJECT_CHOICES = [
        ('General Inquiry', 'General Inquiry'),
        ('Reservation Assistance', 'Reservation Assistance'),
        ('Private Event Enquiry', 'Private Event Enquiry'),
        ('Feedback / Review', 'Feedback / Review'),
        ('Catering Request', 'Catering Request'),
        ('Press & Media', 'Press & Media'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name