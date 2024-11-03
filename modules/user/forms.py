from django import forms

class AddUserForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(required=True)
    phone = forms.CharField(max_length=11, required=True)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 11:
            raise forms.ValidationError('Phone must be a valid 11-digit number.')
        return phone