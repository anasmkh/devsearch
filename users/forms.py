from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile, Skill


class customUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','username','password1','password2']



    def __init__(self, *args,**kwargs):
        super(customUserForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class updateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','email','username','location','headline','bio','profile_image','social_website']

    def __init__(self, *args, **kwargs):
        super(updateProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class skillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(skillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})