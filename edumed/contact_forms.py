# -*- coding: utf-8 -*-
import re

from django import forms
from django.forms.formsets import BaseFormSet
from django.utils.safestring import mark_safe
from markdown2 import Markdown

from contact.fields import HeaderField
from contact.forms import ContactForm
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from edumed.contact_forms_test import TestForm

LINK_PATTERNS = [
    (re.compile(r'((http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,;@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)'),
     r'\1')
]

markdown = Markdown(extras=["link-patterns", 'code-friendly'], link_patterns=LINK_PATTERNS)

WOJEWODZTWA = (
    u'dolnośląskie',
    u'kujawsko-pomorskie',
    u'lubelskie',
    u'lubuskie',
    u'łódzkie',
    u'małopolskie',
    u'mazowieckie',
    u'opolskie',
    u'podkarpackie',
    u'podlaskie',
    u'pomorskie',
    u'śląskie',
    u'świętokrzyskie',
    u'warmińsko-mazurskie',
    u'wielkopolskie',
    u'zachodniopomorskie',
)

WOJEWODZTWO_CHOICES = [(u'', u'(wybierz)')] + [(w, w) for w in WOJEWODZTWA]


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
    instytucja = forms.CharField(
        label=u'Instytucja (nazwa, adres)', widget=forms.Textarea, max_length=1000, required=False)
    uwagi = forms.CharField(label=u'Uwagi', widget=forms.Textarea, max_length=1800, required=False)
        
    zajecia_przedszkole = forms.BooleanField(label=u'Prowadzę zajęcia z dziećmi w wieku przedszkolnym', required=False)
    zajecia_sp13 = forms.BooleanField(label=u'Prowadzę zajęcia z dziećmi z SP kl. 1-3', required=False)
    zajecia_sp46 = forms.BooleanField(label=u'Prowadzę zajęcia z dziećmi z SP kl. 4-6', required=False)
    zajecia_gimnazjum = forms.BooleanField(label=u'Prowadzę zajęcia z młodzieżą w wieku gimnazjalnym', required=False)
    zajecia_ponadgimnazjalne = forms.BooleanField(
        label=u'Prowadzę zajęcia z młodzieżą ze szkół ponadgimnazjalnych', required=False)
    zajecia_wyzsze = forms.BooleanField(label=u'Prowadzę zajęcia w szkole wyższej', required=False)
    zajecia_dorosli = forms.BooleanField(label=u'Prowadzę zajęcia dla dorosłych', required=False)
    zajecia_seniorzy = forms.BooleanField(label=u'Prowadzę zajęcia dla seniorów', required=False)
    zgoda_dane = forms.BooleanField(
        label=u'Oświadczam, że wyrażam zgodę na przetwarzanie moich danych osobowych zawartych '
              u'w niniejszym formularzu zgłoszeniowym przez Fundację Nowoczesna Polska '
              u'(administratora danych) z siedzibą w Warszawie (00-514) przy ul. Marszałkowskiej 84/92 '
              u'lok. 125 w celu otrzymywania newslettera Edukacja medialna. Jednocześnie oświadczam, '
              u'że zostałam/em poinformowana/y o tym, że mam prawo wglądu w treść swoich danych '
              u'i możliwość ich poprawiania oraz że ich podanie jest dobrowolne, ale niezbędne '
              u'do dokonania zgłoszenia.')


class ContestForm(ContactForm):
    form_tag = 'konkurs'
    form_title = u"Zgłoś się do konkursu"
    admin_list = ['nazwisko', 'instytucja', 'tytul']

    nazwisko = forms.CharField(label=u'Imię i nazwisko', max_length=128)
    contact = forms.EmailField(label=u'Adres e-mail', max_length=128)
    instytucja = forms.CharField(label=u'Instytucja (nazwa, adres)', widget=forms.Textarea, max_length=1000)
    tytul = forms.CharField(
        label=u'Tytuł przeprowadzonej lekcji',
        help_text=u'proszę wymienić wszystkie, jeśli zostały przeprowadzone więcej niż jedne zajęcia',
        widget=forms.Textarea, max_length=1000)
    uczestnicy = forms.CharField(label=u'Liczba uczestników', max_length=64)
    trudnosci = forms.CharField(
        label=u'Czy w trakcie zajęć pojawiły się jakieś trudności? Jeśli tak, to jakie?',
        widget=forms.Textarea, max_length=2000)
    pomocne = forms.CharField(
        label=u'Co w materiałach okazało się najbardziej pomocne w przygotowaniu i prowadzeniu lekcji?',
        widget=forms.Textarea, max_length=2000)
    nieprzydatne = forms.CharField(
        label=u'Co w materiałach okazało się nieprzydatne w przygotowaniu i prowadzeniu lekcji?',
        widget=forms.Textarea, max_length=2000)
    poprawic = forms.CharField(
        label=u'Jak możemy poprawić serwis edukacjamedialna.edu.pl?',
        widget=forms.Textarea, max_length=2000, required=False)
    inne = forms.CharField(label=u'Inne uwagi i komentarze', widget=forms.Textarea, max_length=2000, required=False)
    zgoda_regulamin = forms.BooleanField(
        label=u'Znam i akceptuję regulamin konkursu Medialog.',
        help_text=u'Zobacz <a href="/media/chunks/attachment/Regulamin_konkursu_MediaLog_1.pdf">'
                  u'regulamin konkursu MediaLog</a>.')
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


class NonEmptyBaseFormSet(BaseFormSet):
    """
    Won't allow formset_factory to be submitted with no forms
    """
    def clean(self):
        for form in self.forms:
            if form.cleaned_data:
                return
        forms.ValidationError(u"Proszę podać dane przynajmniej jednej osoby.")


class WTEMForm(ContactForm):
    disabled = True
    disabled_template = 'wtem/disabled_contact_form.html'
    form_tag = "wtem"
    form_title = u"WTEM - rejestracja uczestników"
    submit_label = u"Wyślij zgłoszenie"
    admin_list = ['imie', 'nazwisko', 'institution']
    form_formsets = {
        'student': forms.formsets.formset_factory(
            WTEMStudentForm, formset=NonEmptyBaseFormSet, max_num=5, validate_max=True, extra=5),
    }

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
        help_text=u'Zobacz <a href="/media/chunks/attachment/regulamin_III_edycja.pdf">'
                  u'regulamin Wielkiego Turnieju Edukacji Medialnej</a>.'
    )
    zgoda_dane = forms.BooleanField(
        label=u'Wyrażam zgodę na przetwarzanie moich danych osobowych oraz danych osobowych moich podopiecznych.',
        # help_text=u'Zobacz <a href="/media/chunks/attachment/Oswiadczenie_o_danych_osobowych.pdf">'
        # 'pełną treść oświadczenia</a>.'
    )

    potw_uczniowie = forms.BooleanField(
        label=u'Potwierdzam, że zgłoszeni Uczestnicy/Uczestniczki w chwili rejestracji są '
              u'uczniami/uczennicami szkoły ponadgimnazjalnej.',
    )
    zgoda_informacje = forms.BooleanField(
        label=u'Wyrażam zgodę na otrzymywanie informacji od Fundacji Nowoczesna Polska '
              u'związanych z edukacją medialną.',
        required=False
    )

    extract_types = (dict(slug='extended', label=_('extended')),)

    @staticmethod
    def get_extract_fields(contact, extract_type_slug):
        fields = contact.body.keys()
        fields.pop(fields.index('student'))
        fields.extend(['contact', 'student_first_name', 'student_last_name', 'student_email'])
        return fields

    @staticmethod
    def get_extract_records(keys, contact, extract_type_slug):
        toret = [dict()]
        for field_name in keys:
            if field_name.startswith('student_'):
                continue
            if field_name == 'contact':
                val = contact.contact
            else:
                val = contact.body[field_name]
            toret[0][field_name] = val
        
        current = toret[0]
        for student in contact.body['student']:
            for attr in ('first_name', 'last_name', 'email'):
                current['student_' + attr] = student[attr]
            if current not in toret:
                toret.append(current)
            current = dict()
        return toret

    def save(self, request, formsets=None):
        contact = super(WTEMForm, self).save(request, formsets)

        mail_subject = render_to_string('contact/wtem/student_mail_subject.html').strip()
        mail_body = render_to_string('contact/wtem/student_mail_body.html')
        for formset in formsets or []:
            for f in formset.forms:
                email = f.cleaned_data.get('email', None)
                try:
                    validate_email(email)
                except ValidationError:
                    pass
                else:
                    send_mail(mail_subject, mail_body, 'edukacjamedialna@nowoczesnapolska.org.pl', [email],
                              fail_silently=True)

        return contact


class CommissionForm(forms.Form):
    name = forms.CharField(label=u'Imię i nazwisko Członka Komisji', max_length=128)
    form_tag = "commission"


class OlimpiadaForm(ContactForm):
    disabled = True
    disabled_template = 'wtem/disabled_contact_form.html'
    form_tag = "olimpiada"
    form_title = u"Olimpiada Cyfrowa - Elektroniczny System Zgłoszeń"
    submit_label = u"Wyślij zgłoszenie"
    admin_list = ['nazwisko', 'school']
    form_formsets = {
        'student': forms.formsets.formset_factory(WTEMStudentForm, formset=NonEmptyBaseFormSet),
        'commission': forms.formsets.formset_factory(CommissionForm, formset=BaseFormSet),
    }

    contact = forms.EmailField(label=u'Adres e-mail Przewodniczącego/Przewodniczącej', max_length=128)
    przewodniczacy = forms.CharField(label=u'Imię i nazwisko Przewodniczącego/Przewodniczącej', max_length=128)
    school = forms.CharField(label=u'Nazwa szkoły', max_length=255)
    school_address = forms.CharField(label=u'Adres szkoły', widget=forms.Textarea, max_length=1000)
    school_email = forms.EmailField(label=u'Adres e-mail szkoły', max_length=128)
    school_phone = forms.CharField(label=u'Numer telefonu szkoły', max_length=32)
    school_www = forms.URLField(label=u'Strona WWW szkoły', max_length=255, required=False)

    zgoda_regulamin = forms.BooleanField(
        label=u'Znam i akceptuję Regulamin Olimpiady Cyfrowej.',
        help_text=u'Zobacz <a href="https://olimpiadacyfrowa.pl/regulamin/" target="_blank">'
                  u'regulamin Olimpiady Cyfrowej</a>.'
    )
    zgoda_dane = forms.BooleanField(
        label=u'Oświadczam, że wyrażam zgodę na przetwarzanie danych osobowych zawartych w niniejszym formularzu '
              u'zgłoszeniowym przez Fundację Nowoczesna Polska (administratora danych) z siedzibą w Warszawie (00-514) '
              u'przy ul. Marszałkowskiej 84/92 lok. 125 na potrzeby organizacji Olimpiady Cyfrowej. Jednocześnie '
              u'oświadczam, że zostałam/em poinformowana/y o tym, że mam prawo wglądu w treść swoich danych '
              u'i możliwość ich poprawiania oraz że ich podanie jest dobrowolne, ale niezbędne do dokonania '
              u'zgłoszenia.')

    extract_types = (dict(slug='extended', label=_('extended')),)

    @staticmethod
    def get_extract_fields(contact, extract_type_slug):
        fields = contact.body.keys()
        if 'student' in fields:
            fields.remove('student')
        fields.extend(['contact', 'student_first_name', 'student_last_name', 'student_email'])
        return fields

    @staticmethod
    def get_extract_records(keys, contact, extract_type_slug):
        toret = [{}]
        for field_name in keys:
            if field_name.startswith('student_'):
                continue
            if field_name == 'contact':
                val = contact.contact
            else:
                val = contact.body[field_name]
            toret[0][field_name] = val

        current = toret[0]
        if 'student' in contact.body:
            for student in contact.body['student']:
                for attr in ('first_name', 'last_name', 'email'):
                    current['student_' + attr] = student[attr]
                if current not in toret:
                    toret.append(current)
                current = {}
        return toret

    def save(self, request, formsets=None):
        contact = super(OlimpiadaForm, self).save(request, formsets)

        mail_subject = render_to_string('contact/olimpiada/student_mail_subject.html').strip()
        mail_body = render_to_string('contact/olimpiada/student_mail_body.html')
        for formset in formsets or []:
            if formset.prefix == 'student':
                for f in formset.forms:
                    email = f.cleaned_data.get('email', None)
                    try:
                        validate_email(email)
                    except ValidationError:
                        pass
                    else:
                        send_mail(mail_subject, mail_body, 'edukacjamedialna@nowoczesnapolska.org.pl', [email],
                                  fail_silently=True)

        return contact


class MILForm(ContactForm):
    form_tag = 'mil'
    form_title = _('Share your thoughts on the "Media and information literacy competencies catalogue"')
    submit_label = _('Submit')
    base_template = 'base_mil.html'
    site_name = site_domain = 'katalog.nowoczesnapolska.org.pl'

    name = forms.CharField(label=_('Name and Surname'), max_length=255)
    contact = forms.EmailField(label=_('E-mail'), max_length=255)

    institution = forms.CharField(label=_('Institution'), widget=forms.Textarea, max_length=8192)

    question_stages = forms.CharField(
        label=_('What do you think about the proposed educational stages classification?'),
        widget=forms.Textarea,
        max_length=255,
        required=False)

    question_fields = forms.CharField(
        label=_('What do you think about the proposed thematic fields?'),
        widget=forms.Textarea,
        max_length=255,
        required=False)

    question_left_out = forms.CharField(
        label=_('What important areas of media and information literacy have been left out?'),
        widget=forms.Textarea,
        max_length=255,
        required=False)

    other = forms.CharField(
        label=_('Other suggestions and comments'),
        widget=forms.Textarea,
        max_length=255,
        required=False)


class TEMForm(ContactForm):
    form_tag = 'tem'
    form_title = u"TEM - szkolenie dla trenerów edukacji medialnej"
    admin_list = ['imie', 'nazwisko', 'instytucja', 'contact']

    imie = forms.CharField(label=u'Imię', max_length=128)
    nazwisko = forms.CharField(label=u'Nazwisko', max_length=128)
    contact = forms.EmailField(label=u'E-mail', max_length=128)
    telefon = forms.CharField(label=u'Tel. kontaktowy', max_length=128)
    instytucja = forms.CharField(label=u'Instytucja', max_length=256)
    adres = forms.CharField(label=u'Adres', widget=forms.Textarea, max_length=1000)
    stanowisko = forms.CharField(label=u'Stanowisko', max_length=256)
    doswiadczenie = forms.CharField(
        label=u'Jakie jest Pani/Pana doświadczenie w zakresie edukacji medialnej?',
        widget=forms.Textarea, max_length=500, help_text=u'(max 500 znaków)')
    dlaczego = forms.CharField(
        label=u'Dlaczego chce Pani/Pan wziąć udział w szkoleniu?',
        widget=forms.Textarea, max_length=500, help_text=u'(max 500 znaków)')
    jak_wykorzystac = forms.CharField(
        label=u'Jak zamierza Pan/Pani wykorzystać wiedzę zdobytą w czasie szkolenia?',
        widget=forms.Textarea, max_length=500, help_text=u'(max 500 znaków)')

    zajecia = forms.BooleanField(
        label=u'W okresie wrzesień-październik 2015 r. przeprowadzę min. 2 godziny zajęć edukacji medialnej '
              u'z wybraną grupą dzieci lub młodzieży.', required=True)
    zgoda_informacje = forms.BooleanField(
        label=u'Wyrażam zgodę na otrzymywanie informacji od Fundacji Nowoczesna Polska '
              u'związanych z edukacją medialną.', required=False)


class SuperwizjaForm(ContactForm):
    form_tag = 'superwizja'
    form_title = u"Informacje o zajęciach"
    admin_list = ['nazwisko', 'contact', 'skype', 'temat']
    submit_label = u'Wyślij'

    nazwisko = forms.CharField(label=u'Imię i nazwisko', max_length=1024)
    contact = forms.CharField(label=u'E-mail kontaktowy', required=False)
    skype = forms.CharField(label=u'Nazwa użytkownika Skype', max_length=255)
    temat = forms.CharField(label=u'Temat zajęć', max_length=1024)
    termin = forms.CharField(label=u'Termin zajęć', max_length=1024)
    czas_trwania = forms.CharField(label=u'Czas trwania zajęć', max_length=1024)
    miejsce = forms.CharField(label=u'Miejsce prowadzenia zajęć', max_length=1024)
    rodzaj = forms.ChoiceField(
        label=u'Rodzaj zajęć', widget=forms.RadioSelect,
        choices=[('jednorazowe', 'jednorazowe'), ('w ramach cyklu', 'w ramach cyklu')])
    cykl = forms.CharField(label=u'Jeśli w ramach cyklu, to podaj jego temat i czas trwania', required=False)
    sposob = forms.ChoiceField(
        label=u'Sposób prowadzenia zajęć', widget=forms.RadioSelect,
        choices=[('samodzielnie', 'samodzielnie'), (u'z drugą osobą', 'z drugą osobą')])
    wrazenia = forms.CharField(
        label=u'Opisz Twoje ogólne wrażenia po warsztacie.', widget=forms.Textarea, max_length=4096)
    opiekun = forms.CharField(
        label=u'Czy opiekun grupy był obecny podczas zajęć? Jeśli tak, opisz krótko jego rolę.',
        widget=forms.Textarea, max_length=4096)
    grupa = forms.CharField(
        label=u'Opisz krótko grupę uczestników zajęć (wiek, liczba osób, czy to pierwszy kontakt z grupą).',
        widget=forms.Textarea, max_length=4096)
    cel = forms.CharField(
        label=u'Jaki był założony cel zajęć? Dlaczego wybrałaś/eś taki cel?', widget=forms.Textarea, max_length=4096)
    ewaluacja = forms.CharField(
        label=u'W jaki sposób sprawdziłeś/aś, czy cel zajęć został zrealizowany? Opisz krótko efekty zajęć.',
        widget=forms.Textarea, max_length=4096)
    # header
    przygotowania = forms.CharField(
        label=u'Opisz w punktach proces przygotowania się do zajęć.', widget=forms.Textarea, max_length=4096)
    przygotowania_trudnosci = forms.CharField(
        label=u'Co na etapie przygotowań sprawiło Ci największą trudność?', widget=forms.Textarea, max_length=4096)
    przygotowania_pomoc = forms.CharField(
        label=u'Co było pomocne w przygotowaniu zajęć? '
              u'(Czy korzystałaś/eś z materiałów z serwisu edukacjamedialna.edu.pl? Jeśli tak, to jakich?)',
        widget=forms.Textarea, max_length=4096)
    narzedzia = forms.CharField(
        label=u'Jakie narzędzie/a planowałaś/eś wykorzystać, a jakie wykorzystałaś/eś?',
        widget=forms.Textarea, max_length=4096)
    struktura = forms.CharField(
        label=u'Opisz w punktach strukturę zajęć. '
              u'Zaznacz ile czasu planowałaś/eś na każdą część, a ile czasu faktycznie Ci to zajęło.',
        widget=forms.Textarea, max_length=4096)
    prowadzenie_trudnosci = forms.CharField(
        label=u'Co sprawiało Ci trudność w prowadzeniu zajęć?', widget=forms.Textarea, max_length=4096)
    prowadzenie_pomoc = forms.CharField(
        label=u'Co było pomocne w prowadzeniu zajęć?', widget=forms.Textarea, max_length=4096)
    kontrakt = forms.CharField(
        label=u'W jakiej formie został zawarty kontrakt z uczestnikami? Jakie zasady zostały przyjęte? '
              u'Czy w trakcie zajęć Ty bądź uczestnicy odwoływaliście się do kontraktu?',
        widget=forms.Textarea, max_length=4096)
    trudne_sytuacje = forms.CharField(
        label=u'Czy podczas zajęć miały miejsce tzw. „trudne sytuacje”. '
              u'Jak na nie zareagowałaś/eś? Czy potrzebowałabyś/łbyś czegoś w związku z nimi?',
        widget=forms.Textarea, max_length=4096)
    informacje_zwrotne = forms.CharField(
        label=u'Czy zbierałaś/eś informacje zwrotne od uczestników? Jeśli tak, na co zwrócili uwagę? '
              u'W jaki sposób zbierałaś/eś informacje zwrotne?', widget=forms.Textarea, max_length=4096)

    mocne_strony = forms.CharField(
        label=u'Opisz w punktach mocne strony przeprowadzonych zajęć.', widget=forms.Textarea, max_length=4096)
    zmiany = forms.CharField(
        label=u'Opisz w punktach, co byś zmienił(a) na przyszłość.', widget=forms.Textarea, max_length=4096)
    potrzeby = forms.CharField(
        label=u'Czy potrzebowałbyś/łbyś czegoś przed następnymi zajęciami?', widget=forms.Textarea, max_length=4096)
    uwagi = forms.CharField(label=u'Inne uwagi', widget=forms.Textarea, max_length=4096, required=False)


def textarea_field(label, max_length=500):
    return forms.CharField(
        label=label, widget=forms.Textarea, max_length=max_length, help_text=u'(do %s znaków)' % max_length)


class CybernauciForm(ContactForm):
    disabled = True
    disabled_template = 'contact/disabled_contact_form.html'
    form_tag = 'trenerzy-cybernauci2017'
    form_title = u"Cybernauci – szkolenie dla trenerów"
    admin_list = ['nazwisko', 'instytucja', 'contact']
    submit_label = u'Wyślij'

    nazwisko = forms.CharField(label=u'Imię i nazwisko', max_length=1024)
    adres = forms.CharField(label=u'Adres zamieszkania')
    wojewodztwo = forms.ChoiceField(label=u'Województwo', choices=WOJEWODZTWO_CHOICES)
    contact = forms.CharField(label=u'Adres e-mail')
    telefon = forms.CharField(label=u'Telefon kontaktowy', max_length=32)
    dlaczego = textarea_field(
        label=u'Proszę opisać, dlaczego chce Pan/Pani zostać Emisariuszem Bezpiecznego Internetu.')
    grupy = forms.MultipleChoiceField(
        label=u'Proszę wskazać, dla których grup realizował Pan/realizowała Pani zajęcia warsztatowe',
        widget=forms.CheckboxSelectMultiple,
        choices=[
            ('Uczniowie klas 1-3', 'Uczniowie klas 1-3'),
            ('Uczniowie klas 4-6', 'Uczniowie klas 4-6'),
            ('Uczniowie szkół gimnazjalnych', 'Uczniowie szkół gimnazjalnych'),
            ('Uczniowie szkół ponadgimnazjalnych', 'Uczniowie szkół ponadgimnazjalnych'),
            ('Nauczyciele', 'Nauczyciele'),
            ('Rodzice', 'Rodzice'),
        ])
    doswiadczenie_grupy = textarea_field(
        label=u'Proszę opisać swoje doświadczenie w pracy warsztatowej z grupami docelowymi Projektu '
              u'(dziećmi, młodzieżą, osobami dorosłymi: nauczycielami, rodzicami).',
        max_length=750)
    doswiadczenie_edumed = textarea_field(
        label=u'Jakie jest Pana/Pani doświadczenie w zakresie edukacji medialnej, '
              u'zwłaszcza w zakresie bezpieczeństwa w Internecie i korzystania z TIK? '
              u'Skąd czerpie Pan/Pani wiedzę w tym zakresie? W jakich projektach brał '
              u'Pan/brała Pani udział dotychczas?',
        max_length=750)
    szkolenia = textarea_field(
        label=u'Proszę wymienić studia, szkolenia albo kursy (maks. 5 najważniejszych) '
              u'powiązane z tematyką Projektu, w których Pan/Pani uczestniczył/ła, '
              u'w tym dane na temat instytucji czy osoby prowadzącej (z JEDNOZDANIOWYM '
              u'omówieniem i terminami, w których się odbyły).')
    realizacje = textarea_field(
        label=u'Proszę opisać swoje doświadczenie w zakresie realizacji działań w lokalnym środowisku '
              u'szkolnym (np. na terenie gminy/powiatu/województwa).')
    cel = textarea_field(
        label=u'Proszę opisać, jaką wiedzę i umiejętności chce Pan/Pani zdobyć '
              u'lub doskonalić poprzez uczestnictwo w Szkoleniu trenerskim.')
    skad = forms.CharField(label=u'Skąd dowiedział/dowiedziała się Pan/Pani o projekcie „Cybernauci”?')
    zgoda_regulamin = forms.BooleanField(
        label=u'Oświadczam, że zapoznałem/zapoznałam się z Regulaminem Rekrutacji '
              u'i Uczestnictwa w Projekcie „Cybernauci – kompleksowy projekt '
              u'kształtowania bezpiecznych zachowań w sieci” i akceptuję jego warunki.',
        help_text=u'Zobacz <a href="https://cybernauci.edu.pl/wp-content/uploads/2017/04/'
                  u'regulamin_Cybernauci_szkolenie_trenerskie_2017.pdf">regulamin</a>.')
    zgoda_dane = forms.BooleanField(
        label=u'Wyrażam zgodę na przetwarzanie moich danych osobowych zawartych '
              u'w niniejszym dokumencie dla potrzeb niezbędnych do realizacji Projektu '
              u'„Cybernauci – kompleksowy projekt kształtowania bezpiecznych zachowań '
              u'w sieci”  zgodnie z ustawą z dnia 29.08.1997 roku o Ochronie Danych '
              u'Osobowych (Dz. U. z 2002 r. Nr 101, poz. 926 z późniejszymi zmianami).')
    zgoda_niekaralnosc = forms.BooleanField(
        label=u'W przypadku zakwalifikowania się na kurs zobowiązuję się '
              u'do dostarczenia świadectwa o niekaralności – najpóźniej w dniu rozpoczęcia Szkolenia.')
    zgoda_newsletter = forms.BooleanField(
        required=False,
        label=u'Chcę otrzymywać newsletter Edukacja Medialna.')
    cv = forms.FileField(
        label=u'Wgraj plik CV.',
        help_text=u'Prosimy o nazwanie pliku swoim imieniem i nazwiskiem. Preferowany format: PDF.')


class WLEMForm(ContactForm):
    disabled = True
    form_tag = 'wlem'
    form_title = u"WLEM - szkolenie dla warszawskich liderów edukacji medialnej"
    admin_list = ['nazwisko', 'instytucja', 'contact']
    submit_label = u'Wyślij'

    nazwisko = forms.CharField(label=u'Imię i nazwisko', max_length=128)
    contact = forms.CharField(label=u'Adres e-mail')
    telefon = forms.CharField(label=u'Tel. kontaktowy', max_length=32)
    instytucja = forms.CharField(label=u'Instytucja', max_length=128)
    instytucja_adres = forms.CharField(label=u'Adres (instytucji)', max_length=1024)
    stanowisko = forms.CharField(label=u'Stanowisko', max_length=256)
    doswiadczenie = forms.CharField(
        label=u'Jakie jest Pani/Pana doświadczenie w zakresie edukacji medialnej?',
        widget=forms.Textarea, max_length=4096)
    dlaczego = forms.CharField(
        label=u'Dlaczego chce Pani/Pan wziąć udział w szkoleniu?',
        widget=forms.Textarea, max_length=4096)
    cel = forms.CharField(
        label=u'Jaką wiedzę i umiejętności chce Pan/Pani zdobyć lub doskonalić poprzez uczestnictwo w szkoleniu?',
        widget=forms.Textarea, max_length=4096)
    jak_wykorzystac = forms.CharField(
        label=u'Jak zamierza Pan/Pani wykorzystać wiedzę i umiejętności zdobyte w czasie szkolenia?',
        widget=forms.Textarea, max_length=4096)
    zgoda_zajecia = forms.BooleanField(
        label=u'W okresie lipiec-październik 2016 r. przeprowadzę min. 2 godziny zajęć '
              u'edukacji medialnej z grupą warszawiaków.')
    zgoda_dane = forms.BooleanField(
        label=u'Wyrażam zgodę na przetwarzanie moich danych osobowych zawartych '
              u'w niniejszym dokumencie dla potrzeb niezbędnych do realizacji Projektu '
              u'„Warszawscy Liderzy Edukacji Medialnej” zgodnie z ustawą z dnia 29.08.1997 '
              u'roku o Ochronie Danych Osobowych (Dz. U. z 2002 r. Nr 101, poz. 926 '
              u'z późniejszymi zmianami).')
    zgoda_newsletter = forms.BooleanField(
        required=False,
        label=u'Wyrażam zgodę na otrzymywanie informacji od Fundacji Nowoczesna Polska '
              u'związanych z edukacją medialną.')


def ordered_textarea_field(start, pre_label=u'', label=u'', max_length=500):
    return textarea_field(
        mark_safe(u'%s<ol type="a" start="%s"><li>%s</li></ol>' % (pre_label, start, label)),
        max_length=max_length)


def simple_choices(*choices):
    return tuple((choice, choice) for choice in choices)


class CybernauciAnkietaForm(ContactForm):
    def __init__(self, *args, **kwargs):
        super(CybernauciAnkietaForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    form_tag = 'cybernauci-ankieta-trenera-2017'
    form_title = u"Cybernauci – ankieta trenerska"
    nazwisko = forms.CharField(label=u'Imię i nazwisko', max_length=128)
    contact = forms.CharField(label=u'Adres e-mail')
    pyt1a = ordered_textarea_field(
        1, pre_label=u'1. W kontekście planowanego szkolenia jakie są Twoje oczekiwania w zakresie:',
        label=u'przekazywanej wiedzy')
    pyt1b = ordered_textarea_field(2, label=u'tematyki szkoleń z bezpieczeństwa w sieci')
    pyt1c = ordered_textarea_field(3, label=u'materiałów dydaktycznych')
    pyt1d = ordered_textarea_field(4, label=u'organizacji  i prowadzenia szkoleń w projekcie')
    pyt1e = ordered_textarea_field(5, label=u'umiejętności trenerskich')
    pyt1f = ordered_textarea_field(6, label=u'inne, jakie?')
    pyt2 = textarea_field(u'2. W których tematach z obszaru bezpieczeństwa w sieci czujesz się najpewniej? '
                          u'Dlaczego?')
    pyt3 = textarea_field(u'3. Które z tematów znasz słabej lub których nie znasz zupełnie?')
    pyt4 = textarea_field(u'4. Jakie są Twoje mocne strony jako osoby prowadzącej warsztaty?')
    pyt5 = textarea_field(u'5. Nad jakimi elementami pracy trenerskiej chciałbyś/chciałabyś popracować?')
    pyt6 = textarea_field(u'6. Co jest dla Ciebie najważniejsze w pracy z grupą? '
                          u'Na co zwracasz uwagę w tym obszarze jako osoba prowadząca warsztaty?')
    pyt7 = textarea_field(
        u'7. Jakie są Twoje największe obawy wobec realizacji szkoleń w placówkach oświatowych?')
    pyt8a = ordered_textarea_field(
        1, pre_label=u'8. Opisz szczegółowo doświadczenie z różnymi grupami:', label=u'rodzice')
    pyt8b = ordered_textarea_field(2, label=u'nauczyciele')
    pyt8c = ordered_textarea_field(3, label=u'młodzież ponadgimnazjalna')
    pyt8d = ordered_textarea_field(4, label=u'młodzież gimnazjalna')
    pyt8e = ordered_textarea_field(5, label=u'dzieci i młodzież szkół podstawowych')
    pyt9 = textarea_field(
        u'9. Z jakimi grupami wiekowymi najlepiej Ci się współpracuje? '
        u'Umiejętności w zakresie pracy z którą grupą najbardziej chciałabyś/chciałbyś zdobyć/doskonalić?')
    pyt10 = textarea_field(
        u'10. W jaki sposób na co dzień dbasz o swój rozwój jako trenera/trenerki, '
        u'osoby prowadzącej warsztaty czy inne formy szkoleniowe?')
    pyt11 = textarea_field(u'11. Jakie są Twoje potrzeby żywieniowe?')
    pyt12 = forms.ChoiceField(
        label=u'12. Jak przyjedziesz do Wilgi?',
        widget=forms.RadioSelect,
        choices=simple_choices(
            u'publiczna komunikacja do/z Warszawy (i wesoły bus do/z Wilgi)',
            u'publiczna komunikacja do/z Wilgi',
            u'samochód prywatny'))


class SciezkiKopernikaForm(ContactForm):
    form_tag = 'sciezki-kopernika'
    form_title = u'Formularz zgłoszeniowy na warsztaty'
    disabled = True

    nazwisko = forms.CharField(label=u'Imię i nazwisko uczestnika/uczestniczki', max_length=128)
    rok_urodzenia = forms.IntegerField(label=u'Rok urodzenia')
    adres_dom = forms.CharField(label=u'Adres zamieszkania – ulica i numer', max_length=128)
    adres_poczta = forms.CharField(label=u'Adres zamieszkania – kod pocztowy i miejscowość', max_length=128)
    contact = forms.EmailField(label=u'Adres e-mail')
    szkola = forms.CharField(label=u'Nazwa szkoły', max_length=128)
    adres_szkola = forms.CharField(label=u'Adres szkoły – ulica i numer', max_length=128)
    poczta_szkola = forms.CharField(label=u'Adres szkoły – kod pocztowy i miejscowość', max_length=128)
    opiekun = forms.CharField(label=u'Imię i nazwisko rodzica/opiekuna', max_length=128)
    adres_opiekun = forms.CharField(label=u'Adres zamieszkania rodzica/opiekuna – ulica i numer', max_length=128)
    poczta_opiekun = forms.CharField(
        label=u'Adres zamieszkania rodzica/opiekuna – kod pocztowy i miejscowość', max_length=128)
    telefon_opiekun = forms.CharField(label=u'Numer telefonu rodzica/opiekuna', max_length=32)
    email_opiekun = forms.EmailField(label=u'Adres e-mail rodzica/opiekuna', max_length=32)
    specjalne_potrzeby = forms.ChoiceField(
        label=u'Czy uczestnik/uczestniczka ma specjalne potrzeby wynikające z niepełnosprawności', required=True,
        choices=[('tak', 'tak'), ('nie', 'nie')], widget=forms.RadioSelect)
    zgoda_regulamin = forms.BooleanField(
        label=mark_safe(
            u'Oświadczam, że zapoznałem/am się z <a href="/media/chunks/attachment/Regulamin.pdf" target="_blank">'
            u'Regulaminem udziału w projekcie</a> '
            u'i spełniam kryteria kwalifikowalności do udziału w projekcie.'))


ODMOWA_CHOICES = [
    ('nie', u'Nie'),
    ('tak', u'Tak'),
    ('odmowa', u'Odmowa odpowiedzi'),
]

YESNO_CHOICES = [
    ('nie', u'Nie'),
    ('tak', u'Tak'),
]


class SciezkiKopernikaTestForm(TestForm):
    def __init__(self, *args, **kwargs):
        super(SciezkiKopernikaTestForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    result_page = True
    form_tag = 'sciezki-kopernika-test'
    form_title = u'Test wiedzy w zakresie edukacji medialnej i cyfrowej'
    submit_label = u'Wyślij'

    contact = forms.EmailField(label=u'Adres e-mail, na który przyślemy informację o wynikach')
    head1 = HeaderField(
        label=u'Test powstał w ramach projektu "Collegium Młodych - media i technologie" realizowany w ramach '
              u'III Osi priorytetowej: Szkolnictwo wyższe dla gospodarki i rozwoju, Działanie 3.1 Kompetencje '
              u'w szkolnictwie wyższym Programu Operacyjnego Wiedza Edukacja Rozwój, współfinansowanego przez '
              u'Unię Europejską w ramach Europejskiego Funduszu Społecznego. Nr umowy POWR.03.01.00-00-C078/16-00.')
    head2 = HeaderField(
        label=u'Dane zbierane są wyłącznie na potrzeby realizacji projektu „Collegium Młodych – media i technologie”,'
              u' w szczególności potwierdzenia kwalifikowalności wydatków, udzielenia wsparcia, monitoringu, '
              u'ewaluacji, kontroli, audytu i sprawozdawczości oraz działań informacyjno-promocyjnych w ramach '
              u'PO WER.')
    imie = forms.CharField(label=u'Imię')
    nazwisko = forms.CharField(label=u'Nazwisko')
    PESEL = forms.CharField(label=u'PESEL', required=False, help_text=u'zostawić pusty w przypadku braku')
    plec = forms.ChoiceField(
        label=u'Płeć', widget=forms.RadioSelect,
        choices=[('k', u'kobieta'), ('m', u'mężczyzna')])
    wiek = forms.IntegerField(label='Wiek')
    wyksztalcenie = forms.ChoiceField(
        label=u'Wykształcenie',
        choices=[
            (u'Niższe niż podstawowe', u'Niższe niż podstawowe'),
            (u'Podstawowe', u'Podstawowe'),
            (u'Gimnazjalne', u'Gimnazjalne'),
            (u'Ponadgimnazjalne', u'Ponadgimnazjalne'),
            (u'Policealne', u'Policealne'),
            (u'Wyższe', u'Wyższe'),
        ])
    wojewodztwo = forms.ChoiceField(label=u'Województwo', choices=WOJEWODZTWO_CHOICES)
    powiat = forms.CharField(label=u'Powiat')
    gmina = forms.CharField(label=u'Gmina')
    miejscowosc = forms.CharField(label=u'Miejscowość')
    ulica = forms.CharField(label=u'Ulica', required=False)
    numer = forms.CharField(label=u'Nr budynku')
    lokal = forms.CharField(label=u'Nr lokalu', required=False)
    kod = forms.CharField(label=u'Kod pocztowy')
    telefon = forms.CharField(label=u'Telefon kontaktowy')
    status = forms.ChoiceField(
        label=u'Status na rynku pracy',
        choices=[
            (u'uczeń', u'osoba bierna zawodowo ucząca się'),
            (u'nieuczeń', u'osoba bierna zawodowo nieuczestnicząca w kształceniu'),
            (u'bezrobotna-up', u'Osoba bezrobotna zarejestrowana w ewidencji UP'),
            (u'bezrobotna-nie-up', u'Osoba bezrobotna nie zarejestrowana w ewidencji UP'),
            (u'pracująca', u'Osoba pracująca'),
            (u'inne', u'inne'),
        ])
    typ_szkoly = forms.CharField(label=u'Typ szkoły (ponadgimnazjalna; inna, jaka?)', required=False)
    mniejszosc = forms.ChoiceField(
        label=u'Osoba należąca do mniejszości narodowej lub etnicznej, migrant, osoba obcego pochodzenia',
        choices=ODMOWA_CHOICES)
    bezdomna = forms.ChoiceField(
        label=u'Osoba bezdomna lub dotknięta wykluczeniem z dostępu do mieszkań', choices=YESNO_CHOICES)
    niepelnosprawna = forms.ChoiceField(
        label=u'Osoba z niepełnosprawnościami',
        choices=ODMOWA_CHOICES)
    pytanie4 = forms.ChoiceField(
        label=u'Osoba przebywająca w gospodarstwie domowym bez osób pracujących',
        choices=YESNO_CHOICES)
    pytanie5 = forms.ChoiceField(
        label=u'Osoba przebywająca w gospodarstwie domowym z dziećmi pozostającymi na utrzymaniu',
        choices=YESNO_CHOICES)
    pytanie6 = forms.ChoiceField(
        label=u'Osoba żyjąca w gospodarstwie składającym się z jednej osoby dorosłej i dzieci '
              u'pozostających na utrzymaniu',
        choices=YESNO_CHOICES)
    pytanie7 = forms.ChoiceField(
        label=u'Osoba żyjąca w innej niekorzystnej sytuacji społecznej (inne niż wymienione powyżej)',
        choices=ODMOWA_CHOICES)

    @classmethod
    def results(cls, contact):
        fields = cls().fields

        def get_idx(choices, answer):
            return dict((score, i) for i, (score, text) in enumerate(choices))[answer]

        def question_data(i):
            field = 'pyt%s' % i
            choices = fields[field].choices
            score = contact.body[field]
            chosen_idx = get_idx(choices, score)
            correct_idx = get_idx(choices, 2)
            return {
                'score': score,
                'chosen_idx': chosen_idx,
                'correct_idx': correct_idx,
                'chosen': 'abc'[chosen_idx],
                'correct': 'abc'[correct_idx],
                'label': fields[field].label,
                'comment': mark_safe(markdown.convert(cls.ANSWER_COMMENTS[i-1][chosen_idx])),
                'answers': [(text, a_score == score, a_score == 2) for a_score, text in choices],
            }
        question_count = 20
        questions = [question_data(i) for i in xrange(1, question_count + 1)]
        points = sum(question['score'] for question in questions)
        return {'questions': questions, 'points': points/2., 'total': question_count}
