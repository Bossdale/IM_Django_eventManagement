from django.db import models


class Event(models.Model):
    # String reference 'Room' is perfect here because class Room is defined below
    room = models.ForeignKey('Room', on_delete=models.CASCADE)

    # Correct references to the account app
    teacher = models.ManyToManyField('account.Teacher')
    attendees = models.ManyToManyField('account.Student', through="AttendEvent")

    # Fields
    EventId = models.AutoField(primary_key=True)
    EventTitle = models.CharField(max_length=120)
    DateOfEvent = models.DateField()
    MaxParticipants = models.IntegerField()

    # IMPROVEMENT 1: Add __str__ so the Admin panel shows "Python Workshop" instead of "Event object (1)"
    def __str__(self):
        return self.EventTitle


class Room(models.Model):
    RoomId = models.AutoField(primary_key=True)
    RoomName = models.CharField(max_length=120)

    def __str__(self):
        return self.RoomName


class AttendEvent(models.Model):
    # IMPROVEMENT 2: 'NOT JOINED' is exactly 10 chars.
    # Increased max_length to 20 to prevent "Data too long" errors if you change status text later.
    status_type = (('JOINED', 'ATTENDING'), ('NOT JOINED', 'NOT ATTENDING'))

    student = models.ForeignKey('account.Student', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=status_type, default='JOINED')

    def __str__(self):
        return f"{self.student} - {self.event}"