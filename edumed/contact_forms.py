# -*- coding: utf-8 -*-
from django import forms
from django.forms.formsets import BaseFormSet
from django.utils.safestring import mark_safe

from contact.forms import ContactForm
from django.utils.translation import ugettext_lazy as _

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


def make_data_processing(middle_text):
    return mark_safe(u'''\
Administratorem danych osobowych jest Fundacja Nowoczesna Polska (ul. Marszałkowska 84/92 lok. 125, 00-514 Warszawa). \
Podanie danych osobowych jest dobrowolne. %s Osobom, których dane są zbierane, przysługuje prawo dostępu do treści \
swoich danych oraz ich poprawiania. Więcej informacji w <a href="https://nowoczesnapolska.org.pl/prywatnosc/">\
polityce prywatności</a>.''' % middle_text)


class ReminderForm(ContactForm):
    form_tag = 'nie-przegap-2018'
    form_title = u'Rejestracja. Nie przegap terminu!'
    contact = forms.EmailField(label=u'Adres e-mail', max_length=128)
    data_processing = make_data_processing(
        u'Dane są przetwarzane w zakresie niezbędnym do wysłania powiadomienia odbiorcom.')
    submit_label = u'Wyślij'


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


class CommissionForm(forms.Form):
    name = forms.CharField(label=u'Imię i nazwisko Członka Komisji', max_length=128)
    form_tag = "commission"


class OlimpiadaForm(ContactForm):
    ends_on = (2017, 11, 17, 0, 5)
    disabled_template = 'wtem/disabled_contact_form.html'
    form_tag = "olimpiada"
    old_form_tags = ["olimpiada-2016"]
    form_title = u"Olimpiada Cyfrowa - Elektroniczny System Zgłoszeń"
    submit_label = u"Wyślij zgłoszenie"
    admin_list = ['nazwisko', 'school']
    form_formsets = {
        'student': forms.formsets.formset_factory(WTEMStudentForm, formset=NonEmptyBaseFormSet),
        'commission': forms.formsets.formset_factory(CommissionForm),
    }
    mailing_field = 'zgoda_newsletter'

    contact = forms.EmailField(label=u'Adres e-mail Przewodniczącego/Przewodniczącej', max_length=128)
    przewodniczacy = forms.CharField(label=u'Imię i nazwisko Przewodniczącego/Przewodniczącej', max_length=128)
    school = forms.CharField(label=u'Nazwa szkoły', max_length=255)
    school_address = forms.CharField(label=u'Adres szkoły', widget=forms.Textarea, max_length=1000)
    school_wojewodztwo = forms.ChoiceField(label=u'Województwo', choices=WOJEWODZTWO_CHOICES)
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
    zgoda_newsletter = forms.BooleanField(
        label=u'Chcę otrzymywać newsletter: Edukacja medialna', required=False)

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
        from wtem.models import Confirmation
        contact = super(OlimpiadaForm, self).save(request, formsets)

        for formset in formsets or []:
            if formset.prefix == 'student':
                for f in formset.forms:
                    email = f.cleaned_data.get('email', None)
                    if email:
                        try:
                            Confirmation.objects.get(email=email)
                        except Confirmation.DoesNotExist:
                            first_name = f.cleaned_data.get('first_name', None)
                            last_name = f.cleaned_data.get('last_name', None)
                            if first_name and last_name:
                                confirmation = Confirmation.create(
                                    first_name=first_name, last_name=last_name, email=email, contact=contact)
                                confirmation.send_mail()
        return contact
