from django import forms


class RequestForm(forms.Form):
    url = forms.URLField(label='URLを入力してください．')
    CHOICE = [
        (1, '☆1'),
        (2, '☆2'),
        (3, '☆3'),
        (4, '☆4'),
        (5, '☆5')
    ]

    stars = forms.MultipleChoiceField(
        label='取得したいレビューを選択してください．',
        choices=CHOICE,
        widget=forms.CheckboxSelectMultiple
    )
