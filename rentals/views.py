from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cars, Bookings, Additions, Customers, Payments
from django.templatetags.static import static
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail


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

    return render(request, 'rentals/fleet.html', {'cars': cars})


def booking(request, car_id):
    car = get_object_or_404(Cars, id=car_id)  # Get the car by its ID
    additions = Additions.objects.all()  # Fetch all add-ons

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        pickup_date = request.POST.get("pickup_date")
        dropoff_date = request.POST.get("dropoff_date")
        pickup_time = request.POST.get("pickup_time")
        dropoff_time = request.POST.get("dropoff_time")
        pickup_location = request.POST.get("pickup_location")
        selected_additions = request.POST.getlist(
            "additions")  # List of selected add-ons

        # Calculate rental days
        pickup_date_obj = datetime.strptime(pickup_date, "%Y-%m-%d").date()
        dropoff_date_obj = datetime.strptime(dropoff_date, "%Y-%m-%d").date()
        day_difference = (dropoff_date_obj - pickup_date_obj).days

        # Get car details
        base_price = day_difference * car.price_day

        # Calculate add-on price
        add_on_total = 0
        selected_additions_objects = Additions.objects.filter(
            id__in=selected_additions)
        for addition in selected_additions_objects:
            add_on_total += addition.price * day_difference

        total_price = base_price + add_on_total
        print("Selected Additions (IDs):", selected_additions)
        print("Selected Additions Objects:", selected_additions_objects)

        # Save customer (if new)
        customer, created = Customers.objects.get_or_create(email=email, defaults={
            "first_name": first_name,
            "last_name": last_name,
            "contact": contact
        })

        # Save booking
        booking = Bookings.objects.create(
            car=car,
            customer=customer,
            start_da=pickup_date_obj,
            start_time=pickup_time,
            end_da=dropoff_date_obj,
            end_time=dropoff_time,
            pickup_loc=pickup_location,
            total=total_price
        )

        # Associate selected add-ons with the booking
        if selected_additions_objects.exists():
            booking.additions.set(selected_additions_objects)

        # Redirect to the payments page
        return redirect(f"/confirm/{booking.id}")

    return render(request, "rentals/bookings.html", {"car": car, "additions": additions})


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


def confirm(request, booking_id):
    # Fetch the booking using the booking_id
    booking = get_object_or_404(Bookings, id=booking_id)

    # Retrieve related car, customer, and additions data
    car = booking.car
    customer = booking.customer
    additions = booking.additions.all()
    total_price = booking.total

    if request.method == "POST":
        # Check if terms agreement checkbox was checked
        terms_agreement = request.POST.get("terms_agreement")

        if terms_agreement:
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
            [Your Rental Company Name]
            """

            send_mail(user_subject, user_message, admin_email, [user_email])

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
            [Your Rental Company Name]
            """

            send_mail(admin_subject, admin_message, admin_email, [admin_email])

            # Redirect to success page
            return redirect('fleet')

        else:
            # Redirect to an error page if terms were not agreed to
            return redirect('faq')

    # Render the payment page
    return render(request, "rentals/confirm.html", {
        "booking": booking,
        "car": car,
        "customer": customer,
        "additions": additions,
        "total_price": total_price
    })


def payment_success(request):
    return render(request, "rentals/paymentsuccess.html")


def payment_error(request):
    return render(request, "rentals/paymenterror.html")
