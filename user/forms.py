from django import forms


from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="Select Image")


class regdata(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}), required=True,max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password','placeholder':'Password'}),required=True,max_length=200)
    teamname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Team Name'}),required=True,max_length=80)
    itype = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Institution Type'}),required=True,max_length=100)
    iname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Institution Name'}),required=True,max_length=200)
    irec = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Institution Recognized By'}),required=True,max_length=100)
    tcap = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Team Captain'}),required=True,max_length=100)
    phn = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Contact Number'}),required=True,max_length=10)
    altphn = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Alternate Contact Number'}),required=True,max_length=10)
    coach = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Team Coach'}),required=True,max_length=100)
    size = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Team Size','max':'30'}),required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Address','rows':'3'}),required=True,max_length=500)



class otp(forms.Form):
    mname = forms.CharField(widget=forms.TextInput(attrs={'id':'team_name'}))