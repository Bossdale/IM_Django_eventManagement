from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection, DatabaseError
from django.contrib.auth.decorators import login_required
from .models import Event, AttendEvent
from account.models import Student  # Import Student to query relationship


# 1. The Index View (Dashboard)
def index(request):
    all_events = Event.objects.all().order_by('DateOfEvent')

    # List to store IDs of events the student has already joined
    joined_event_ids = []

    # Only check for joined events if the user is actually logged in
    if request.user.is_authenticated:
        try:
            # Get the Student instance corresponding to the logged-in user
            # We use the username because your Student model inherits PK from User
            student = Student.objects.get(username=request.user.username)

            # Fetch IDs of events where this student has a 'JOINED' status
            joined_event_ids = AttendEvent.objects.filter(
                student=student,
                status='JOINED'
            ).values_list('event_id', flat=True)

        except Student.DoesNotExist:
            # If logged in as Admin or a user not in the Student table
            pass

    context = {
        'events': all_events,
        'joined_event_ids': list(joined_event_ids)  # Pass the list of IDs to template
    }

    return render(request, 'CreateEvent/index.html', context)


# 2. The Register View (Keeps your Stored Procedure logic)
@login_required
def register_student(request, event_id):
    student_username = request.user.username

    try:
        with connection.cursor() as cursor:
            # Calls your MySQL Stored Procedure
            cursor.callproc('RegisterStudentForEvent', [student_username, event_id])

        messages.success(request, f"Success! You are registered for Event #{event_id}.")

    except DatabaseError as e:
        error_str = str(e)
        if "maximum capacity" in error_str:
            messages.error(request, "Registration Failed: This event is fully booked.")
        elif "already registered" in error_str:
            messages.warning(request, "You are already registered for this event.")
        elif "does not exist" in error_str:
            messages.error(request, "Registration Failed: Student record not found.")
        else:
            messages.error(request, f"Database Error: {error_str}")

    return redirect('CreateEvent:index')