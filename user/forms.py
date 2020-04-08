from django.forms import ModelForm
from django.forms import ValidationError

from user.models import Profile


class ProfileModelForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_max_distance(self):
        data = self.clean()
        min_distance = data['min_distance']
        max_distance = data['max_distance']
        if min_distance >= max_distance:
            raise ValidationError('min distance is greater than max distance')
        return max_distance

    def clean_max_dating_age(self):
        data = self.clean()
        max_dating_age = data['max_dating_age']
        min_dating_age = data['min_dating_age']
        if min_dating_age >= max_dating_age:
            raise ValidationError('min dating age is greater than max dating age')
        return max_dating_age
