from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cars, Bookings, Additions, Customers
from django.templatetags.static import static
from datetime import datetime,timedelta
from django.utils import timezone
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def homepage(request):
    return render(request, 'rentals/homepage.html')


def fleet(request):
    return render(request, 'rentals/fleet.html')


def menubookings(request):
    return render(request, 'rentals/menubookings.html')


def terms(request):
    return render(request, 'rentals/terms.html')


def contact(request):
    return render(request, 'rentals/contact.html')


def about(request):
    return render(request, 'rentals/about.html')


def faq(request):
    return render(request, 'rentals/faq.html')


# Search Available Cars
def search_available_cars(request):
    if request.method == "GET":
        start_da = request.GET.get('start_da')
        end_da = request.GET.get('end_da')

        if start_da and end_da:
            start_da = datetime.strptime(start_da, "%Y-%m-%d").date()
            end_da = datetime.strptime(end_da, "%Y-%m-%d").date()

            # Get all booked cars in the selected date range
            booked_cars = Bookings.objects.filter(
                start_da__lte=end_da,
                end_da__gte=start_da
            ).values_list('car_id', flat=True)

            # Get cars that are NOT booked
            available_cars = Cars.objects.exclude(
                id__in=booked_cars).order_by('-year')
            paginator = Paginator(available_cars, 8)  # 8 cars per page
            page_number = request.GET.get('page')
            cars = paginator.get_page(page_number)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                data = {
                    'cars': list(cars.object_list.values('id', 'reg_no', 'make', 'model', 'year', 'price_day', 'car_status', 'car_photo')),
                    'has_next': cars.has_next(),
                    'has_previous': cars.has_previous(),
                    'next_page': cars.next_page_number() if cars.has_next() else None,
                    'previous_page': cars.previous_page_number() if cars.has_previous() else None,
                }
                return JsonResponse(data)

            return render(request, 'rentals/search_results.html', {'cars': cars})

    return render(request, 'rentals/search_results.html')


# Fleet Page Car Display
def fleet_list(request):
    cars_list = Cars.objects.all().order_by('-id')  # Get all cars
    paginator = Paginator(cars_list, 24)  # 8 cars per page
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'cars': [
                {
                    "id": car.id,
                    "reg_no": car.reg_no,
                    "make": car.make,
                    "model": car.model,
                    "year": car.year,
                    # Ensure JSON serializable
                    "price_day": float(car.price_day),
                    "car_status": car.car_status,
                    "car_photo": request.build_absolute_uri(car.car_photo.url) if car.car_photo else None,
                }
                for car in cars
            ],
            'has_next': cars.has_next(),
            'has_previous': cars.has_previous(),
            'next_page': cars.next_page_number() if cars.has_next() else None,
            'previous_page': cars.previous_page_number() if cars.has_previous() else None,
        }
        return JsonResponse(data)

    return render(request, 'rentals/fleet.html', {'cars': cars})


# Homepage Car Display
def homepage_cars(request):
    cars_list = Cars.objects.all().order_by('-year')  # Get all cars
    paginator = Paginator(cars_list, 3)  # 3 cars per page
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'cars': [
                {
                    "id": car.id,
                    "reg_no": car.reg_no,
                    "make": car.make,
                    "model": car.model,
                    "year": car.year,
                    # Ensure JSON serializable
                    "price_day": float(car.price_day),
                    "car_status": car.car_status,
                    "car_photo": request.build_absolute_uri(car.car_photo.url) if car.car_photo else None,
                }
                for car in cars
            ],
            'has_next': cars.has_next(),
            'has_previous': cars.has_previous(),
            'next_page': cars.next_page_number() if cars.has_next() else None,
            'previous_page': cars.previous_page_number() if cars.has_previous() else None,
        }
        return JsonResponse(data)

    return render(request, 'rentals/homepage.html', {'cars': cars})

#Booking page and information
def booking(request, car_id):
    car = get_object_or_404(Cars, id=car_id)  # Get the car by its ID
    additions = Additions.objects.all()  # Fetch all add-ons

    if request.method == "POST":
        #Hold customer info in a session
        request.session['customer_data'] = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "contact": request.POST.get("contact"),
            "email": request.POST.get("email"),
        }
       
        pickup_date = request.POST.get("pickup_date")
        dropoff_date = request.POST.get("dropoff_date")
        pickup_time = request.POST.get("pickup_time")
        dropoff_time = request.POST.get("dropoff_time")
        pickup_location = request.POST.get("pickup_location")
        selected_additions = request.POST.getlist("additions")  # List of selected add-ons

        # Calculate rental days
        pickup_date_obj = datetime.strptime(pickup_date, "%Y-%m-%d").date()
        dropoff_date_obj = datetime.strptime(dropoff_date, "%Y-%m-%d").date()
        day_difference = (dropoff_date_obj - pickup_date_obj).days

        # Get car details
        base_price = day_difference * car.price_day

        # Calculate add-on price
        add_on_total = 0
        selected_additions_objects = Additions.objects.filter(id__in=selected_additions)
        for addition in selected_additions_objects:
            add_on_total += addition.price * day_difference

        total_price = float(base_price + add_on_total)
        print("Selected Additions (IDs):", selected_additions)
        print("Selected Additions Objects:", selected_additions_objects)
        
        
        request.session["booking_data"] = {
            "car_id": car.id,
            "customer_id": 0,
            "start_date": str(pickup_date_obj),
            "end_date": str(dropoff_date_obj),
            "start_time": pickup_time,
            "end_time": dropoff_time,
            "pickup_location": pickup_location,
            "selected_additions": selected_additions,
            "total_price": total_price,
        }
       
        # Redirect to the payments page
        return redirect(f"/confirm/")

    return render(request, "rentals/bookings.html", {"car": car, "additions": additions})

#Confirmation and call email functions
def confirm(request):
    booking = None
    customer = None

    #Session Holders
    customer_data = request.session.get("customer_data")
    booking_data = request.session.get("booking_data")
    
    if not customer_data or not booking_data:
        return redirect ('fleet')

    # Retrieve related car, customer, and additions data
    car = get_object_or_404(Cars, id=booking_data["car_id"])
    additions = Additions.objects.filter(id__in=booking_data["selected_additions"])
    total_price = booking_data["total_price"]

    if request.method == "POST":
        # Check if terms agreement checkbox was checked
        terms_agreement = "terms_agreement" in request.POST

        if terms_agreement:
            customer, created = Customers.objects.update_or_create(
                email = customer_data["email"], defaults={
                "first_name": customer_data["first_name"],
                "last_name": customer_data["last_name"],
                "contact": customer_data["contact"],
            })
            booking_data["customer_id"] = customer.id
            request.session["booking_data"] = booking_data
            
            booking = Bookings.objects.create(
                car = car,
                customer = customer,
                start_da = booking_data["start_date"],
                start_time  =booking_data["start_time"],
                end_da = booking_data["end_date"],
                end_time = booking_data["end_time"],
                pickup_loc = booking_data["pickup_location"],
                total = total_price
            )
            
            #Associate selected add-ons with the booking
            if additions.exists():
               booking.additions.set(additions)
            
            #Clear Sessions
            del request.session["booking_data"]
            del request.session["customer_data"]
            
            #Send Emails
            send_booking_email(customer, car, additions, total_price)
            
            # Redirect to success page
            return redirect('fleet')#change to tahank you page

        else:
            # Redirect to an error page if terms were not agreed to
            return redirect('faq')

    # Render the confrimation page
    return render(request, "rentals/confirm.html", {
        "car": car,
        "customer": customer_data,
        "additions": additions,
        "total_price": total_price
    })

#Email Information
def send_booking_email(customer, car, additions, total_price):
    admin_email = settings.DEFAULT_FROM_EMAIL
    user_email = customer.email
    
    # User confirmation email
    user_subject = "Your Car Rental Booking Confirmation"
    user_message = f"""
    Dear {customer.first_name},
    Thank you for booking with us! Here is your rental summary:

    Car: {car.model}
    Price per Day: ${car.price_day}
    Add-ons: 
    {', '.join([f"{add.name} (+${add.price}/day)" for add in additions]) if additions else 'None'}
    
    Total Price: ${total_price}

    We look forward to serving you! If you have any questions, feel free to contact us.

    Best Regards,  
    BT Car Rentals
    """

    send_email(user_subject, user_message, admin_email, [user_email])

    # Admin notification email
    admin_subject = "New Car Rental Booking Received"
    admin_message = f"""
    A new booking has been made.

    Customer: {customer.first_name} {customer.last_name}
    Email: {customer.email}
    Contact: {customer.contact}
    
    Car: {car.model}
    Price per Day: ${car.price_day}
    Add-ons: 
    {', '.join([f"{add.name} (+${add.price}/day)" for add in additions]) if additions else 'None'}

    Total Price: ${total_price}

    Please log in to your admin panel to view the full details.

    Regards,  
    BT Car Rentals
    """

    send_email(admin_subject, admin_message, admin_email, [admin_email])

#Email Settings
def send_email(subject, message, sender_email, recipient_list):
    smtp_server = "smtp.sendgrid.net"
    smtp_port = 587
    smtp_username = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD

    for recipient_email in recipient_list:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            

        except Exception as e:
            print(f"❌Failed to send email to {recipient_email}: {e}")



#Block Dates
def get_booked_dates(request, car_id):
    """Return a list of booked dates for a given car ID."""
    booked_dates = []
    
    # Fetch all bookings for the selected car
    bookings = Bookings.objects.filter(car_id=car_id)

    for booking in bookings:
        start_da = booking.start_da
        end_da = booking.end_da
        current_date = start_da
        
        # Add all booked dates to the list
        while current_date <= end_da:
            booked_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)

    return JsonResponse({"booked_dates": booked_dates})
