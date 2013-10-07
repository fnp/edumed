# -*- coding: utf-8 -*-
from django import forms
from contact.forms import ContactForm


class RegistrationForm(ContactForm):
    form_tag = 'sugestie'
    form_title = u"Zgłoś sugestię"
    admin_list = ['podpis', 'contact', 'temat']

    contact = forms.EmailField(label=u'E-mail', max_length=128, required=False)
    podpis = forms.CharField(label=u'Podpis', max_length=128, required=False)
    temat = forms.CharField(label=u'Temat zgłoszenia', max_length=255)
    tresc = forms.CharField(label=u'Treść', widget=forms.Textarea, max_length=1800)


class CooperateForm(ContactForm):
    form_tag = 'wspolpraca'
    form_title = u"Bądź z nami w kontakcie"
    admin_list = ['podpis', 'contact']

    podpis = forms.CharField(label=u'Imię i nazwisko', max_length=128)
    contact = forms.EmailField(label=u'E-mail', max_length=128)
    instytucja = forms.CharField(label=u'Instytucja (nazwa, adres)', 
            widget=forms.Textarea, max_length=1000, required=False)
    uwagi = forms.CharField(label=u'Uwagi', widget=forms.Textarea, max_length=1800, required=False)
        
    zajecia_przedszkole = forms.BooleanField(label=u'Prowadzę zajęcia z dziećmi w wieku przedszkolnym', required=False)
    zajecia_sp13 = forms.BooleanField(label=u'Prowadzę zajęcia z dziećmi z SP kl. 1-3', required=False)
    zajecia_sp46 = forms.BooleanField(label=u'Prowadzę zajęcia z dziećmi z SP kl. 4-6', required=False)
    zajecia_gimnazjum = forms.BooleanField(label=u'Prowadzę zajęcia z młodzieżą w wieku gimnazjalnym', required=False)
    zajecia_ponadgimnazjalne = forms.BooleanField(label=u'Prowadzę zajęcia z młodzieżą ze szkół ponadgimnazjalnych', required=False)
    zajecia_wyzsze = forms.BooleanField(label=u'Prowadzę zajęcia w szkole wyższej', required=False)
    zajecia_dorosli = forms.BooleanField(label=u'Prowadzę zajęcia dla dorosłych', required=False)
    zajecia_seniorzy = forms.BooleanField(label=u'Prowadzę zajęcia dla seniorów', required=False)


class ContestForm(ContactForm):
    form_tag = 'konkurs'
    form_title = u"Zgłoś się do konkursu"
    admin_list = ['nazwisko', 'instytucja', 'tytul']

    nazwisko = forms.CharField(label=u'Imię i nazwisko', max_length=128)
    contact = forms.EmailField(label=u'Adres e-mail', max_length=128)
    instytucja = forms.CharField(label=u'Instytucja (nazwa, adres)', 
            widget=forms.Textarea, max_length=1000)
    tytul = forms.CharField(label=u'Tytuł przeprowadzonej lekcji',
            help_text=u'proszę wymienić wszystkie, jeśli zostały przeprowadzone więcej niż jedne zajęcia', 
            widget=forms.Textarea, max_length=1000)
    uczestnicy = forms.CharField(label=u'Liczba uczestników', max_length=64)
    trudnosci = forms.CharField(label=u'Czy w trakcie zajęć pojawiły się jakieś trudności? Jeśli tak, to jakie?', 
            widget=forms.Textarea, max_length=2000)
    pomocne = forms.CharField(label=u'Co w materiałach okazało się najbardziej pomocne w przygotowaniu i prowadzeniu lekcji?', 
            widget=forms.Textarea, max_length=2000)
    nieprzydatne = forms.CharField(label=u'Co w materiałach okazało się nieprzydatne w przygotowaniu i prowadzeniu lekcji?', 
            widget=forms.Textarea, max_length=2000)
    poprawic = forms.CharField(label=u'Jak możemy poprawić serwis edukacjamedialna.edu.pl?', 
            widget=forms.Textarea, max_length=2000,
            required=False)
    inne = forms.CharField(label=u'Inne uwagi i komentarze', 
            widget=forms.Textarea, max_length=2000,
            required=False)
    zgoda_regulamin = forms.BooleanField(
        label=u'Znam i akceptuję regulamin konkursu Medialog.',
        help_text=u'Zobacz <a href="/media/chunks/attachment/Regulamin_konkursu_MediaLog_1.pdf">regulamin konkursu MediaLog</a>.'
    )
    zgoda_informacje = forms.BooleanField(
        label=u'Wyrażam zgodę na otrzymywanie informacji od Fundacji Nowoczesna Polska związanych z edukacją medialną.',
        required=False
    )


class UdzialForm(ContactForm):
    form_tag = 'udzial'
    form_title = u"Udział"
    admin_list = ['nazwisko', 'miejscowosc', 'instytucja']

    nazwisko = forms.CharField(label=u'Imię i nazwisko', max_length=128)
    miejscowosc = forms.CharField(label=u'Miejscowość', max_length=128)
    instytucja = forms.CharField(label=u'Nazwa organizacji/instytucji', max_length=128)
    contact = forms.EmailField(label=u'Adres e-mail', max_length=128)
    telefon = forms.CharField(label=u'Telefon', max_length=32)
    uczestnicy = forms.IntegerField(label=u'Przewidywana liczba uczestników zajęć')


class WTEMStudentForm(forms.Form):
    first_name = forms.CharField(label=u'Imię', max_length=128)
    last_name = forms.CharField(label=u'Nazwisko', max_length=128)
    email = forms.EmailField(label=u'Adres e-mail', max_length=128)
    form_tag = "student"

class NoEmptyFormsAllowedBaseFormSet(forms.formsets.BaseFormSet):
    """
    Won't allow formset_factory to be submitted with no forms
    """
    def clean(self):
        for form in self.forms:
            if form.cleaned_data:
                return
        raise forms.ValidationError(u"Proszę podać dane przynajmniej jednego ucznia.")

class WTEMForm(ContactForm):
    form_tag = "wtem"
    form_title = u"WTEM - rejestracja uczestników"
    submit_label = u"Wyślij zgłoszenie"
    form_formsets = (forms.formsets.formset_factory(WTEMStudentForm, formset=NoEmptyFormsAllowedBaseFormSet),)

    contact = forms.EmailField(label=u'Adres e-mail opiekuna/opiekunki', max_length=128)
    imie = forms.CharField(label=u'Imię', max_length=128)
    nazwisko = forms.CharField(label=u'Nazwisko', max_length=128)
    function = forms.CharField(label=u'Pełniona funkcja', max_length=255)
    institution = forms.CharField(label=u'Nazwa instytucji', max_length=255)
    institution_address = forms.CharField(label=u'Adres instytucji', widget=forms.Textarea, max_length=1000)
    institution_email = forms.EmailField(label=u'Adres e-mail instytucji', max_length=128)
    institution_phone = forms.CharField(label=u'Telefon do instytucji', max_length=32)
    institution_www = forms.URLField(label=u'Strona WWW instytucji', max_length=255, required=False)

    zgoda_regulamin = forms.BooleanField(
        label=u'Znam i akceptuję regulamin Wielkiego Turnieju Edukacji Medialnej.',
        help_text=u'Zobacz <a href="/media/chunks/attachment/.pdf">regulamin Wielkiego Turnieju Edukacji Medialnej</a>.'
    )
    potw_uczniowie = forms.BooleanField(
        label=u'Potwierdzam, że zgłoszeni Uczestnicy/Uczestniczki w chwili rejestracji są uczniami/uczennicami szkoły ponadgimnazjalnej.',
        #help_text=u'Zobacz <a href="/media/chunks/attachment/.pdf">regulamin Wielkiego Turnieju Edukacji Medialnej</a>.'
    )
    zgoda_informacje = forms.BooleanField(
        label=u'Wyrażam zgodę na otrzymywanie informacji od Fundacji Nowoczesna Polska związanych z edukacją medialną.',
        required=False
    )

