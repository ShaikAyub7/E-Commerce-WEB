from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    new_username = forms.CharField(max_length=150, required=False, label='New Username')

    class Meta:
        model = Profile
        fields = ['profile_image', 'user', 'location', 'occupation', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].widget.attrs.update({
            'class': 'form-control-file',
            'accept': 'image/*',
        })

        self.fields['user'].widget.attrs.update({
            'class': 'form-control',
            'readonly': True,
        })
        
        self.fields['location'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Location',
        })

        self.fields['occupation'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Occupation',
        })

        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Phone Number',
        })

    def as_custom_bootstrap(self):
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs['placeholder'] = field.label
        return self
