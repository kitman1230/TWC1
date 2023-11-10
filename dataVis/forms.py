from django import forms
from .models import ENERGY


class TypeForm(forms.ModelForm):
    class Meta:
        model = ENERGY
        fields = ["energy_Type"]

    energy_Type = forms.ModelChoiceField(
        queryset=ENERGY.objects.values_list("energyType", flat=True).distinct(),
        empty_label="(Choose Energy Type)",
        label="Energy Type",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["energy_Type"].widget.attrs.update({"onchange": "submit()"})
        self.fields["energy_Type"].choices = [
            (x, x) for x in set(self.fields["energy_Type"].queryset)
        ]


chart_Type = [("1", "Bar"), ("2", "Scatter"), ("3", "Line")]


class ChartForm(forms.Form):
    chart_Type = forms.ChoiceField(
        choices=chart_Type,
        label="Chart Type",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["chart_Type"].widget.attrs.update({"onchange": "submit()"})
