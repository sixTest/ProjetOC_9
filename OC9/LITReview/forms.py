from django import forms


class ConnectionForm(forms.Form):
    username = forms.CharField(
        label='Nom',
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom utilisateur'}),
    )

    password = forms.CharField(
        label='Mot de passe',
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Mot de passe'}),
    )


class InscriptionForm(forms.Form):
    username = forms.CharField(
        label='Nom',
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom utilisateur'})
    )
    password = forms.CharField(
        label='Mot de passe',
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Mot de passe'})
    )
    confirm_password = forms.CharField(
        label='Confirmer le mot de passe',
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password',
                                      'placeholder': 'Confirmer le mot de passe'})
    )


class CreationTicketForm(forms.Form):
    title_ticket = forms.CharField(
        label='Titre',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre'}),
    )

    description = forms.CharField(
        label='Description',
        max_length=1000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})
    )

    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )


class CreationReviewForm(forms.Form):
    title_review = forms.CharField(
        label='Titre',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre'}),
    )

    comment = forms.CharField(
        label='Commentaire',
        max_length=1000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
    )
