from django import forms
from .models import Question, Choice
from django.contrib.auth.models import User


class VoteForm(forms.Form):
    new_option = forms.CharField(max_length=200, required=False)

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(VoteForm, self).__init__(*args, **kwargs)
        CHOICES = [(ch.id, ch.choice_text) for ch in self.question.choice_set.all()]
        CHOICES.append((-1, 'other option (please specify in the box below)'))
        self.fields['your_choice'] = forms.ChoiceField(choices = CHOICES, widget=forms.RadioSelect())

    def clean_your_choice(self):
        your_choice = self.cleaned_data.get('your_choice')
        return int(your_choice)

    def clean(self):
        super(VoteForm, self).clean()
        choice_id = self.cleaned_data.get('your_choice')
        new_option = self.cleaned_data.get('new_option')
        if choice_id < 0:
            if not new_option:
                raise forms.ValidationError(
                    'Please specify a new option (or choose an existing one)!'
                    )
        else:
            if new_option:
                raise forms.ValidationError(
                    'Do not specify a new option with also choosing an existing one!'
                    )

    def save(self):
        choice_id = self.cleaned_data.get('your_choice')
        if choice_id < 0:
            new_option = Choice(
                question=self.question,
                choice_text=self.cleaned_data.get('new_option'),
                votes=0
                )
            new_option.save()
        else:
            selected_choice = Choice.objects.get(pk=choice_id)
            selected_choice.votes += 1
            selected_choice.save()

"""
class VoteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(VoteForm, self).__init__(*args, **kwargs)
        CHOICES = [(ch.id, ch.choice_text) for ch in self.question.choice_set.all()]
        self.fields['your_choice'] = forms.ChoiceField(choices = CHOICES, widget=forms.RadioSelect())

    def save(self):
        choice_id = self.cleaned_data.get('your_choice')
        selected_choice = Choice.objects.get(pk=choice_id)
        selected_choice.votes += 1
        selected_choice.save()
"""

"""
class VoteForm(forms.Form):
    CHOICES = [(ch.id, ch.choice_text) for ch in Choice.objects.all()]
#    your_choice = forms.ChoiceField(choices = CHOICES)
    your_choice = forms.ChoiceField(choices = CHOICES, widget=forms.RadioSelect())

    def save(self):
        choice_id = self.cleaned_data.get('your_choice')
        selected_choice = Choice.objects.get(pk=choice_id)
        selected_choice.votes += 1
        selected_choice.save()
"""


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    enter_password = forms.CharField(widget=forms.PasswordInput)
    retype_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('The username has been already taken.')
        return username

    def clean_enter_password(self):
        password = self.cleaned_data.get('enter_password')
        if len(password) < 5:
            raise forms.ValidationError('Password must contain 5 or more characters.')
        return password

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('enter_password')
        retyped = self.cleaned_data.get('retype_password')
        if password and retyped and (password != retyped):
            self.add_error('retype_password', 'This does not match with the above.')

    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('enter_password')
        new_user = User.objects.create_user(username = username)
        new_user.set_password(password)
        new_user.save()
