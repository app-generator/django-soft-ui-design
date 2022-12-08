import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget

from apps.home.models import Worker, Task, TaskType, Position


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
            "profile_image",
        )


class TaskCreationForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    deadline = forms.DateField(
        widget=SelectDateWidget(empty_label=("year", "month", "day")), required=False
    )

    class Meta:
        model = Task
        fields = "__all__"

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < datetime.date.today():
            raise forms.ValidationError("The date of deadline cannot be in the past!")
        return deadline


class TaskUpdateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    deadline = forms.DateField(
        widget=SelectDateWidget(empty_label=("year", "month", "day")), required=False
    )

    class Meta:
        model = Task
        fields = "__all__"


class TaskSearchForm(forms.Form):
    task_type = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by task type..."}),
    )


class TaskTypeCreationForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = "__all__"


class TaskTypeUpdateForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = "__all__"


class PositionCreationForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"


class PositionUpdateForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ("first_name", "last_name", "position", "profile_image")
