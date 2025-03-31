from django import forms
from .models import Customers, Bookings, Additions

class customerform (forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['first_name', "last_name", "contact", "email"]


class availabilityform (forms.Form):
    start_da = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Start Date"
    )
    end_da = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="End Date"
    )                            


class bookingform(forms.ModelForm):
    start_da = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_da = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    pickup_loc = forms.CharField(max_length=255)
    baby_seat = forms.BooleanField(required=False)
    insurance = forms.BooleanField(required=False)

    class Meta:
        model = Bookings
        fields = ['start_da', 'end_da', 'start_time', 'end_time', 'pickup_loc', 'baby_seat', 'insurance']