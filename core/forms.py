from django import forms


class ReviewForm(forms.Form):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)], widget=forms.RadioSelect
    )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 4, "placeholder": "Write your feedback..."}
        ),
        label="Your Comment",
    )
