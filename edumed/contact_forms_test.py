# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

from contact.forms import ContactForm


def quiz_question(label, choices):
    return forms.TypedMultipleChoiceField(label=label, choices=choices, coerce=int, widget=forms.CheckboxSelectMultiple)


def make_link(text, url):
    return u'<a href="%s">%s</a>' % (url, text)


class TestForm(ContactForm):
    form_tag = '_____'
    pyt1 = quiz_question(
        label=u'1. Crowdfunding to inaczej:',
        choices=[
            (01, u'finansowanie społecznościowe'),
            (10, u'finansowanie wydawnicze'),
            (20, u'finansowanie przez wielkie wytwórnie'),
            (30, u'finansowanie wielkich sponsorów')])
    pyt2 = quiz_question(
        label=u'2. Powracające problemy z dostępem do internetu u danego usługodawcy to materiał '
              u'na reklamację telekomunikacyjną składaną do:',
        choices=[
            (01, u'Urzędu Komunikacji Elektronicznej'),
            (10, u'Urzędu Kontroli Skarbowej'),
            (20, u'Urzędu Marszałkowskiego'),
            (30, u'Urzędu Ochrony Państwa')])
    pyt3 = quiz_question(
        label=u'3. Śledzone przez firmę zachowanie internauty w internecie:',
        choices=[
            (01, u'zdradzać może preferencje internauty'),
            (11, u'zdradzać może cechy osobowości internauty'),
            (21, u'możliwe jest dzięki programom komputerowym'),
            (31, u'pozwala emitować wstępnie dopasowane oferty na ekranie komputera internauty'),
            (41, u'pozwala badać reakcję na reklamy'),
            (50, u'żadna z powyższych odpowiedzi nie jest prawdziwa')])
    pyt4 = quiz_question(
        label=u'4. Profilowanie nie wiąże się z:',
        choices=[
            (00, u'kategoryzowaniem ludzi według cech i zachowań'),
            (10, u'doborem reklam do użytkownika pod kątem wieku i płci'),
            (20, u'doborem reklam do użytkownika pod kątem wykonanych przez niego polubień i kliknięć'),
            (31, u'żadna z powyższych odpowiedzi nie jest prawidłowa')])
    pyt5 = quiz_question(
        label=u'5. Dobór reklam do użytkownika nie jest w internecie możliwy na podstawie:',
        choices=[
            (00, u'produktów oglądanych w sklepach internetowych'),
            (10, u'słów wyszukiwanych w wyszukiwarkach'),
            (20, u'treści e-maili w usługach poczty elektronicznej'),
            (31, u'żadna z powyższych odpowiedzi nie jest prawidłowa')])
    pyt6 = quiz_question(
        label=u'6. Jeżeli sąd odmówi osobie poniżej 16 roku życia prawa dostępu do informacji publicznej, '
              u'a informacja ta jest dla zainteresowanej osoby subiektywnie ważna, to jaki kolejny krok warto wykonać?',
        choices=[
            (00, u'zrezygnować z uzyskania dostępu do informacji publicznej'),
            (10, u'odłożyć wniosek o dostęp do informacji publicznej do ukończenia 18 roku życia'),
            (21, u'udać się po pomoc do Rzecznika Praw Obywatelskich'),
            (30, u'żadne z powyższych')])
    pyt7 = quiz_question(
        label=u'7. W przypadku, gdy informacje o sprzęcie w sklepie internetowym są niepełne, a sprzedawca '
              u'konsekwentnie wprowadza klientów indywidualnych w błąd, gdzie warto kierować się po pomoc?',
        choices=[
            (01, u'Urząd Ochrony Konkurencji i Konsumentów'),
            (10, u'Urząd Kontroli Skarbowej'),
            (20, u'Urząd do Spraw Cudzoziemców'),
            (30, u'Urząd Ochrony Państwa')])
    pyt8 = quiz_question(
        label=u'8. W ramach dozwolonego użytku wolno nam bez zgody twórcy przygotować spektakl teatralny '
              u'i wystawić go w szkole oraz:',
        choices=[
            (00, u'Sprzedawać widzom bilety, a zysk przeznaczyć na zakup sprzętu uczniowskiego koła naukowego'),
            (10, u'Sprzedawać widzom bilety, a zysk podzielić pomiędzy występujących artystów'),
            (20, u'Nagrać spektakl i udostępnić go wszystkim za darmo w internecie'),
            (30, u'Nagrać spektakl i udostępniać go odpłatnie w internecie'),
            (41, u'Żadna z odpowiedzi nie jest prawidłowa')])
    pyt9 = quiz_question(
        label=u'9. Osoby niepełnosprawne często korzystają z nietypowych narzędzi. Osoby niewidome w internecie '
              u'surfują posługując się specjalnymi “gadającymi” przeglądarkami. Osoby nie mogące korzystać z rąk '
              u'mają specjalne urządzenia umożliwiające nawigację po stronach lub systemy rozpoznawania głosu. '
              u'Zestaw norm dzięki którym strony internetowe są przyjazne dla osób niepełnosprawnych to:',
        choices=[
            (00, u'IDPD – Internet for Disabled People Directive'),
            (11, u'WCAG – Web Content Accessibility Guidelines'),
            (20, u'HTTP – HyperText Markup Language'),
            (30, u'EAA – European Accessibility Act')])
    pyt10 = quiz_question(
        label=u'10. Dane osobowe są chronione mocą prawa, ale niektóre z nich uznaje się za dane wrażliwe i poddaje '
              u'dodatkowym rygorom, m.in. nie wolno ich przetwarzać bez naszej pisemnej zgody lub w celu innym '
              u'niż szczegółowo określony. Do danych wrażliwych zaliczamy:',
        choices=[
            (01, u'pochodzenie rasowe lub etniczne'),
            (11, u'przynależność partyjną'),
            (21, u'dane o stanie zdrowia'),
            (30, u'numer PESEL')])
    pyt11 = quiz_question(
        label=u'11. Majątkowe prawa autorskie są ograniczone w czasie. Kiedy wygasną utwór przechodzi '
              u'do domeny publicznej i staje się własnością wspólną. Dzieje się to:',
        choices=[
            (00, u'50 lat po śmierci twórcy (ze skutkiem na koniec roku kalendarzowego)'),
            (10, u' 50 lat po pierwszym rozpowszechnieniu dzieła, jeśli twórca był anonimowy'),
            (21, u'70 lat po śmierci twórcy (ze skutkiem na koniec roku kalendarzowego)'),
            (31, u'70 lat po pierwszym rozpowszechnieniu dzieła, jeśli miało ono miejsce po śmierci twórcy')])
    pyt12 = quiz_question(
        label=u'12. Wszystkim twórcom przysługują autorskie prawa osobiste, które są – w przeciwieństwie '
              u'do praw majątkowych – są wieczne i niezbywalne. Zaliczamy do nich:',
        choices=[
            (01, u'Prawo do rozpoznania autorstwa'),
            (11, u'Prawo do decyzji o pierwszym rozpowszechnieniu dzieła'),
            (21, u'Prawo do zachowania integralności utworu'),
            (30, u'Prawo do wycofania utworu z obiegu')])
    pyt13 = quiz_question(
        label=u'13. Telewizje utrzymują się przede wszystkim z reklam emitowanych w trakcie trwania programów. '
              u'Przepisy prawa:',
        choices=[
            (00, u'nie regulują sposobu w jaki sposób reklamy te są wyświetlane, decyduje o tym nadawca '
                u'kierując się rachunkiem ekonomicznym, tj. wybiera takie formy wyświetlania reklam, '
                u'które są najbardziej zyskowne'),
            (11, u'ograniczają typ reklam które można emitować ze względu na ich treść lub reklamowane produkty – '
                u'np. nie wolno przedstawiać w pozytywnym świetle ludzi niszczących środowisko naturalne '
                u'lub reklamować gry w kości'),
            (20, u'zabraniają reklamowania produktów w treści filmów'),
            (31, u'uniemożliwiają telewizji publicznej przerywanie filmów reklamami')])
    pyt14 = quiz_question(
        label=u'14. Urzędy które zajmują się ochroną praw obywateli w mediach cyfrowych to:',
        choices=[
            (01, u'Rzecznik Praw Obywatelskich'),
            (10, u'Minister Cyfryzacji'),
            (21, u'Rzecznik Praw Dziecka'),
            (31, u'Generalny Inspektor Ochrony Danych Osobowych')])
    pyt15 = quiz_question(
        label=u'15. W odniesieniu do internetu tak zwane prawo do zapomnienia to:',
        choices=[
            (00, u'Prawo niewysłania w Unii Europejskiej e-maila z potwierdzeniem udziału bez podania przyczyny'),
            (10, u'Prawo niewysłania w Unii Europejskiej e-maila z potwierdzeniem udziału z podaniem zapomnienia '
                u'jako przyczyny'),
            (21, u'Prawo każdego obywatela Unii Europejskiej do zażądania usunięcia jego imienia i nazwiska '
                u'z wyszukiwarki internetowej'),
            (30, u'Prawo każdego obywatela Unii Europejskiej do założenia konta w serwisie społecznościowym'),
            (40, u'Prawo każdego obywatela Unii Europejskiej do zapomnienia adresu wyszukiwarki internetowej '
                u'albo serwisu społecznościowego')])
    pyt16 = quiz_question(
        label=u'16. Autorskie prawa osobiste chronią twórców utworów bezterminowo i bezwarunkowo. Zaliczamy do nich:',
        choices=[
            (01, u'prawo do oznaczania utworu imieniem i nazwiskiem twórcy'),
            (10, u'zakaz parodiowania utworu bez zgody twórcy'),
            (21, u'prawo do zachowania integralności utworu (czyli np. obowiązek wiernego cytowania)'),
            (30, u'prawo do wycofania utworu z obiegu'),
            (41, u'prawo do decyzji o pierwszym rozpowszechnieniu utworu'),
            (50, u'zakaz kopiowania utworu bez zgody twórcy')])
    pyt17 = quiz_question(
        label=u'17. Wykonałeś/wykonałaś remiks cudzych utworów. W jakich sytuacjach możesz rozpowszechnić swój utwór?',
        choices=[
            (01, u'mam zgodę autora/autorki oryginalnego utworu'),
            (10, u'materiały do remiksu zostały ściągnięte z serwisu do przechowywania plików'),
            (20, u'wykorzystane piosenki przesłała mi na Facebooku koleżanka'),
            (31, u'zezwala na to licencja, na której są opublikowane wykorzystane utwory'),
            (41, u'wykorzystane w remiksie utwory są dostępne w domenie publicznej (minęło 70 lat od śmierci autora)'),
            (50, u'utwory użyte w remiksie były udostępnione do odsłuchania na stronach twórców w formie plików mp3')])
    pyt18 = quiz_question(
        label=u'18. Chcesz dowiedzieć się, co sklep internetowy robi z twoimi danymi osobowymi. '
              u'Gdzie szukasz tej informacji?',
        choices=[
            (00, u'w zakładce „O nas”'),
            (10, u'w zakładce „Twój profil”'),
            (21, u'w „Polityce prywatności”'),
            (30, u'w „Regulaminie zakupów”')])
    pyt19 = quiz_question(
        label=u'19. Czy możesz opublikować niekomercyjnie remiks wierszy dostępnych w bibliotece internetowej '
              u'Wolne Lektury?',
        choices=[
            (00, u'nie mogę'),
            (10, u'mogę, ale dopiero kiedy uzyskam zgodę autorów/autorek lub ich spadkobierców'),
            (20, u'mogę, uiściłem/-am opłaty na rzecz Funduszu Promocji Twórczości'),
            (31, u'mogę, wiersze z biblioteki Wolne Lektury znajdują się w domenie publicznej '
                u'albo publikowane są na licencji CC BY-SA 3.0, która umożliwia taką publikację')])
    pyt20 = quiz_question(
        label=u'20. Na co NIE pozwala ci dozwolony użytek?',
        choices=[
            (01, u'na sprzedawanie kopii płyt z muzyką twojego ulubionego zespołu'),
            (10, u'na oglądanie filmu pobranego z internetu'),
            (20, u'na nagranie serialu na płytę i obejrzenie go z rodziną'),
            (30, u'żadna z odpowiedzi nie jest prawidłowa')])

    ANSWER_COMMENTS = [
        (
            u'Początków crowfoundingu można szukać już XVIII wieku, jednak jego największy rozwój przypada na czasy kiedy funkcjonował już internet. Dzięki powstającym internetowym społecznościom możliwe było stworzenie modelu płatności opartego na niewielkich wpłatach od dużej liczby osób. Finansowanie społecznościowe pomaga zapaleńcom, niszowym twórcom czy organizacjom pozarządowym w zbieraniu pieniędzy na cele, które znajdują poparcie w oczach pewnej społeczności. W ramach crowdfoundingu osoby angażujące się finansowo w dany projekt otrzymują coś w zamian. Może to być np. dostęp do wersji testowej wynalazku czy przedpremierowy pokaz filmu, na powstanie których wpłaciło się pieniądze. Zasada nagradzania osób wpłacających w ramach crowdfoundingu zwykle opiera się na tym, że im więcej ktoś wpłaci pieniędzy na dany projekt tym bardziej atrakcyjną formę wynagrodzenia otrzymuje.',
            u'Jeśli chcesz wydać np. książkę możesz to zrobić podpisując umowę z wydawnictwem, które płaci za druk, skład, korektę i inne czynności niezbędne do pojawienia się książki na rynku. Wydawnictwo autorowi płaci wynagrodzenie w postaci ustalonego umownie procentu od ceny książki. Jednak to nie jedyny sposób na wydanie książki. Coraz popularniejszy jest trend selfpublishingu (tj. samodzielne wydanie książki) oraz crowdfoundingu, w ramach którego społeczność przekazuje na pewien cel finanse. Finansowanie społecznościowe pomaga m.in. twórcom w zbieraniu pieniędzy na cele, które znajdują poparcie w oczach pewnej społeczności. W ramach crowdfoundingu osoby angażujące się finansowo w dany projekt otrzymują coś w zamian. Zasada nagradzania osób wpłacających w ramach crowdfoundingu zwykle opiera się na tym, że im więcej ktoś wpłaci pieniędzy na dany projekt tym bardziej atrakcyjną formę wynagrodzenia otrzymuje np. podziękowania we wstępie do książki czy też zniżkę na zakup książki po jej wydaniu.',
            u'Chcąc wydać swoją własną płytę albo wyprodukować film możesz wejść we współpracę z dużą wytwórnią – płytową czy filmową. Ona pokryje wszelkie koszty związane z powstaniem, dystrybucja i sprzedażą Twojego dzieła. Jednak to nie jedyny sposób na wydanie własnej płyty czy stworzenie swojego filmu. Coraz popularniejszy jest trend zwany crowdfoundingiem, w ramach którego społeczność przekazuje na pewien cel finanse. Finansowanie społecznościowe pomaga m.in. twórcom w zbieraniu pieniędzy na cele, które znajdują poparcie w oczach pewnej społeczności. W ramach crowdfoundingu osoby angażujące się finansowo w dany projekt otrzymują coś w zamian. Zasada nagradzania osób wpłacających w ramach crowdfoundingu zwykle opiera się na tym, że im więcej ktoś wpłaci pieniędzy na dany projekt tym bardziej atrakcyjną formę wynagrodzenia otrzymuje np. ekskluzywny materiał z nagrania płyty płyty czy też zaproszenie na przedpremierowy pokaz filmu.',
            u'Sponsoring to jeden z bardziej popularnych sposobów zdobywania pieniędzy na prowadzenie działań z zakresu sportu czy kultury. Pozyskiwanie sponsorów w postaci dużych marek, które wykładają pieniądze na dany cel w zamian za promocję ich firmy np. podczas wydarzenia nie jest jednak zadaniem łatwym. Nie tylko dotarcie do sponsorów jest trudne, ale również cały proces pozyskania finansowania ze względu na wewnętrzną politykę firmy, strategię czy wizerunek marki. Dlatego też na znaczeniu nabiera trend crowdfoundingu, w ramach którego społeczność przekazuje na pewien cel finanse. Finansowanie społecznościowe pomaga m.in. twórcom czy organizatorom eventów w zbieraniu pieniędzy na cele, które znajdują poparcie w oczach pewnej społeczności. W ramach crowdfoundingu osoby angażujące się finansowo w dany projekt otrzymują coś w zamian. Zasada nagradzania osób wpłacających w ramach crowdfoundingu zwykle opiera się na tym, że im więcej ktoś wpłaci pieniędzy na dany projekt tym bardziej atrakcyjną formę wynagrodzenia otrzymuje np. podziękowanie ustne w trakcie wydarzenia czy możliwość wystąpienia podczas wydarzenia.',
        ),
        (
            u'Urząd Komunikacji Elektronicznej, w skrócie UKE, to organ regulujący działalność telekomunikacyjną, pocztową, gospodarkę zasobami częstotliwości oraz kontrolny spełniania wymagań dotyczących kompatybilności elektromagnetycznej. Dlatego też w sytuacji problemów z dostępem do internetu u danego dostawcy, która związana jest bezpośrednio z usługami telekomunikacyjnymi to właśnie ten Urząd będzie właściwym do złożenia reklamacji.',
            u'Urząd Kontroli Skarbowej chroni interesy i prawa majątkowe Skarbu Państwa. Prowadząc kontrole dba o zapewnienie skuteczności wykonywania zobowiązań podatkowych i innych należności stanowiących dochód do budżetu państwa. Bada także czy gospodarowanie mieniem państwowym jest zgodne z prawem, przeciwdziała i zwalcza naruszeniom prawa w tym zakresie. Jak widać więc Urząd ten nie ma wiele wspólnego z reklamacjami telekomunikacyjnymi. W celu złożenia takiej reklamacji należy się udać do UKE – Urzędu Komunikacji Elektronicznej.',
            u'Urząd Marszałkowski jest organem pomocniczym marszałka województwa. Dzięki niemu możliwa jest obsługa kadrowa, prawna, techniczna, organizacyjna i ekspercka komisji organów wykonawczych w województwie tj. zarządu i marszałka oraz uchwałodawczych - sejmiku województwa. Urząd Marszałkowski nie rozpatruje skarg ani reklamacji telekomunikacyjnych. W celu złożenia takiej reklamacji należy udać się do UKE – Urzędu Komunikacji Elektronicznej.',
            u'Jest to organizacja będąca częścią służb specjalnych RP. Jej pracownicy są odpowiedzialni za zapewnienie bezpieczeństwa i obronności kraju, czy też zapobieganie różnorodnym przestępstwom, które mogą mieć konsekwencje w skali całego kraju. UOP nie rozpatruje skarg telekomunikacyjnych. Dlatego chcąc złożyć reklamację należy udać się do UKE, czyli Urzędu Komunikacji Elektronicznej.'
        ),
        (
            u'Śledząc IP danego komputera można odczytywać preferencje czy też poznawać osobowość internauty. Wiadomo bowiem jakie strony odwiedza, w co klika, co kupuje, jakie posty lajkuje na Facebooku. Internet to kopalnia wiedzy o użytkownikach sieci. Gromadzone online dane nazywane są Big Data, a ich analizę umożliwia rozwój specjalnego oprogramowania i sztucznej inteligencji. Maszyny analizują dane, a następnie wysnuwają wnioski i dopasowują np. przekaz marketingowy i reklamowy do preferencji internauty. Pozwalają także na badanie reakcji odbiorcy na prezentowany przekaz. Wszystko to odbywa się za pomocą maszyn, dlatego też nie musisz martwić się, że jesteś pod stałą obserwacją.',
            u'Śledząc IP danego komputera można odczytywać preferencje czy też poznawać osobowość internauty. Wiadomo bowiem jakie strony odwiedza, w co klika, co kupuje, jakie posty lajkuje na Facebooku. Internet to kopalnia wiedzy o użytkownikach sieci. Gromadzone online dane nazywane są Big Data, a ich analizę umożliwia rozwój specjalnego oprogramowania i sztucznej inteligencji. Maszyny analizują dane, a następnie wysnuwają wnioski i dopasowują np. przekaz marketingowy i reklamowy do preferencji internauty. Pozwalają także na badanie reakcji odbiorcy na prezentowany przekaz. Wszystko to odbywa się za pomocą maszyn, dlatego też nie musisz martwić się, że jesteś pod stałą obserwacją.',
            u'Śledząc IP danego komputera można odczytywać preferencje czy też poznawać osobowość internauty. Wiadomo bowiem jakie strony odwiedza, w co klika, co kupuje, jakie posty lajkuje na Facebooku. Internet to kopalnia wiedzy o użytkownikach sieci. Gromadzone online dane nazywane są Big Data, a ich analizę umożliwia rozwój specjalnego oprogramowania i sztucznej inteligencji. Maszyny analizują dane, a następnie wysnuwają wnioski i dopasowują np. przekaz marketingowy i reklamowy do preferencji internauty. Pozwalają także na badanie reakcji odbiorcy na prezentowany przekaz. Wszystko to odbywa się za pomocą maszyn, dlatego też nie musisz martwić się, że jesteś pod stałą obserwacją.',
            u'Śledząc IP danego komputera można odczytywać preferencje czy też poznawać osobowość internauty. Wiadomo bowiem jakie strony odwiedza, w co klika, co kupuje, jakie posty lajkuje na Facebooku. Internet to kopalnia wiedzy o użytkownikach sieci. Gromadzone online dane nazywane są Big Data, a ich analizę umożliwia rozwój specjalnego oprogramowania i sztucznej inteligencji. Maszyny analizują dane, a następnie wysnuwają wnioski i dopasowują np. przekaz marketingowy i reklamowy do preferencji internauty. Pozwalają także na badanie reakcji odbiorcy na prezentowany przekaz. Wszystko to odbywa się za pomocą maszyn, dlatego też nie musisz martwić się, że jesteś pod stałą obserwacją.',
            u'Śledząc IP danego komputera można odczytywać preferencje czy też poznawać osobowość internauty. Wiadomo bowiem jakie strony odwiedza, w co klika, co kupuje, jakie posty lajkuje na Facebooku. Internet to kopalnia wiedzy o użytkownikach sieci. Gromadzone online dane nazywane są Big Data, a ich analizę umożliwia rozwój specjalnego oprogramowania i sztucznej inteligencji. Maszyny analizują dane, a następnie wysnuwają wnioski i dopasowują np. przekaz marketingowy i reklamowy do preferencji internauty. Pozwalają także na badanie reakcji odbiorcy na prezentowany przekaz. Wszystko to odbywa się za pomocą maszyn, dlatego też nie musisz martwić się, że jesteś pod stałą obserwacją.',
            u'Śledząc IP danego komputera można odczytywać preferencje czy też poznawać osobowość internauty. Wiadomo bowiem jakie strony odwiedza, w co klika, co kupuje, jakie posty lajkuje na Facebooku. Internet to kopalnia wiedzy o użytkownikach sieci. Gromadzone online dane nazywane są Big Data, a ich analizę umożliwia rozwój specjalnego oprogramowania i sztucznej inteligencji. Maszyny analizują dane, a następnie wysnuwają wnioski i dopasowują np. przekaz marketingowy i reklamowy do preferencji internauty. Pozwalają także na badanie reakcji odbiorcy na prezentowany przekaz. Wszystko to odbywa się za pomocą maszyn, dlatego też nie musisz martwić się, że jesteś pod stałą obserwacją.',
        ),
        (
            u'Profilowanie w internecie jest stosowane w większości procesów marketingowych. Dzięki czemu można poprzez kategoryzowanie ludzi według cech i zachowań, danych demograficznych i wielu innych czynników dopasować do niego spersonalizowany komunikat reklamowy. Jest to proces, który nie wymaga zgody użytkownika internetu. Zgodnie z rozporządzeniem RODO, które wchodzi w życie wraz z początkiem 2018 roku zabronione jest profilowanie prowadzące do dyskryminacji np. ze względu na rasę.',
            u'Profilowanie w internecie jest stosowane w większości procesów marketingowych. Dzięki czemu można poprzez kategoryzowanie ludzi według cech i zachowań, danych demograficznych i wielu innych czynników dopasować do niego spersonalizowany komunikat reklamowy. Jest to proces, który nie wymaga zgody użytkownika internetu. Zgodnie z rozporządzeniem RODO, które wchodzi w życie wraz z początkiem 2018 roku zabronione jest profilowanie prowadzące do dyskryminacji np. ze względu na rasę.',
            u'Profilowanie w internecie jest stosowane w większości procesów marketingowych. Dzięki czemu można poprzez kategoryzowanie ludzi według cech i zachowań, danych demograficznych i wielu innych czynników dopasować do niego spersonalizowany komunikat reklamowy. Jest to proces, który nie wymaga zgody użytkownika internetu. Zgodnie z rozporządzeniem RODO, które wchodzi w życie wraz z początkiem 2018 roku zabronione jest profilowanie prowadzące do dyskryminacji np. ze względu na rasę.',
            u'Profilowanie w internecie jest stosowane w większości procesów marketingowych. Dzięki czemu można poprzez kategoryzowanie ludzi według cech i zachowań, danych demograficznych i wielu innych czynników dopasować do niego spersonalizowany komunikat reklamowy. Jest to proces, który nie wymaga zgody użytkownika internetu. Zgodnie z rozporządzeniem RODO, które wchodzi w życie wraz z początkiem 2018 roku zabronione jest profilowanie prowadzące do dyskryminacji np. ze względu na rasę. To sprawia, że wszystkie powyższe odpowiedzi są związane z profilowaniem. Odpowiadając na pytanie, które nie są związane z tematem należało więc zaznaczyć odpowiedź żadna z powyższych odpowiedzi nie jest prawdziwa.',
        ),
        (
            u'Personalizacja i dobór reklam do indywidualnego użytkownika w internecie odbywa się na podstawie jego zachowań w sieci – stron internetowych, które odwiedzał, słów wyszukiwanych w wyszukiwarkach, treści e-mail w usługach poczty elektronicznych, produktów oglądanych w sklepach. Dane te są przetwarzane, a następnie analizowane tak aby dobrać przekaz komunikatu reklamowego do potrzeb internauty.',
            u'Personalizacja i dobór reklam do indywidualnego użytkownika w internecie odbywa się na podstawie jego zachowań w sieci – stron internetowych, które odwiedzał, słów wyszukiwanych w wyszukiwarkach, treści e-mail w usługach poczty elektronicznych, produktów oglądanych w sklepach. Dane te są przetwarzane, a następnie analizowane tak aby dobrać przekaz komunikatu reklamowego do potrzeb internauty.',
            u'Personalizacja i dobór reklam do indywidualnego użytkownika w internecie odbywa się na podstawie jego zachowań w sieci – stron internetowych, które odwiedzał, słów wyszukiwanych w wyszukiwarkach, treści e-mail w usługach poczty elektronicznych, produktów oglądanych w sklepach. Dane te są przetwarzane, a następnie analizowane tak aby dobrać przekaz komunikatu reklamowego do potrzeb internauty.',
            u'Personalizacja i dobór reklam do indywidualnego użytkownika w internecie odbywa się na podstawie jego zachowań w sieci – stron internetowych, które odwiedzał, słów wyszukiwanych w wyszukiwarkach, treści e-mail w usługach poczty elektronicznych, produktów oglądanych w sklepach. Dane te są przetwarzane, a następnie analizowane tak aby dobrać przekaz komunikatu reklamowego do potrzeb internauty. Dlatego też dobór reklam jest możliwy na podstawie wszystkich wymienionych działań użytkownika sieci. Odpowiadając na to pytanie należy więc zaznaczyć odpowiedź: żadna z powyższych odpowiedzi nie jest prawidłowa.',
        ),
        (
            u'Prawo dostępu do informacji publicznej jest prawem człowieka i przysługuje każdemu. W prawodawstwie polskim regulacje dotyczące dostępu do informacji publicznej zawarte są w Konstytucji RP (art. 61) wg której prawo dostępu do informacji publicznej posiada każdy. Również osoby nieletnie. Dlatego jeśli osobie poniżej 16 roku życia został odmówiony dostęp do informacji publicznej należy zgłosić się do Rzecznika Praw Obywatelskich z prośbą o pomoc.',
            u'Prawo dostępu do informacji publicznej jest prawem człowieka i przysługuje każdemu. W prawodawstwie polskim regulacje dotyczące dostępu do informacji publicznej zawarte są w Konstytucji RP (art. 61) wg której prawo dostępu do informacji publicznej posiada każdy. Również osoby nieletnie. Dlatego jeśli osobie poniżej 16 roku życia został odmówiony dostęp do informacji publicznej należy zgłosić się do Rzecznika Praw Obywatelskich z prośbą o pomoc.',
            u'Prawo dostępu do informacji publicznej jest prawem człowieka i przysługuje każdemu. W prawodawstwie polskim regulacje dotyczące dostępu do informacji publicznej zawarte są w Konstytucji RP (art. 61) wg której prawo dostępu do informacji publicznej posiada każdy. Również osoby nieletnie. Dlatego jeśli osobie poniżej 16 roku życia został odmówiony dostęp do informacji publicznej należy zgłosić się do Rzecznika Praw Obywatelskich z prośbą o pomoc.',
            u'Prawo dostępu do informacji publicznej jest prawem człowieka i przysługuje każdemu. W prawodawstwie polskim regulacje dotyczące dostępu do informacji publicznej zawarte są w Konstytucji RP (art. 61) wg której prawo dostępu do informacji publicznej posiada każdy. Również osoby nieletnie. Dlatego jeśli osobie poniżej 16 roku życia został odmówiony dostęp do informacji publicznej należy zgłosić się do Rzecznika Praw Obywatelskich z prośbą o pomoc.',
        ),
        (
            u'Jak sama nazwa wskazuje UOKiK za zadanie ma ochronę konsumentów przed niewłaściwymi praktykami ze strony producentów i sprzedawców. Celowe wprowadzanie w błąd jest działaniem na szkodę konsumenta, dlatego też każdy kto jest ofiarą niewłaściwych praktyk, szkodliwych dla interesu konsumenta może skierować się do UOKiK z prośbą o pomoc.',
            u'Urząd Kontroli Skarbowej chroni interesy i prawa majątkowe Skarbu Państwa. Prowadząc kontrole dba o zapewnienie skuteczności wykonywania zobowiązań podatkowych i innych należności stanowiących dochód do budżetu państwa. Bada także czy gospodarowanie mieniem państwowym jest zgodne z prawem, przeciwdziała i zwalcza naruszeniom prawa w tym zakresie. Urząd ten nie zajmuje się sprawami konsumenckimi. W celu rozwiązania opisanego w pytaniu problemu należy udać się do Urzędu Ochrony Konkurencji i Konsumentów.',
            u'Jak można przeczytać na stronie Urzędu do Spraw Cudzoziemców powstał on „by zapewnić kompleksową i profesjonalną obsługę w zakresie legalizacji pobytu i udzielenia ochrony cudzoziemców przebywających na terytorium Rzeczpospolitej Polskiej.” Kwestie związane z ochroną praw konsumenckich nie leżą w kompetencjach urzędu. Aby uzyskać właściwą pomoc należy zgłosić się do Urzędu Ochrony Konkurencji i Konsumentów.',
            u'Jest to organizacja będąca częścią służb specjalnych RP. Jej pracownicy są odpowiedzialni za zapewnienie bezpieczeństwa i obronności kraju, czy też zapobieganie różnorodnym przestępstwom, które mogą mieć konsekwencje w skali całego kraju. UOP nie rozpatruje skarg konsumenckich. Aby uzyskać pomoc w opisanym w pytaniu przykładzie należy zgłosić się do UOKiK – Urzędu Ochrony Konkurencji i Konsumentów.',
        ),
        (
            u'Zgodnie z art. 31 ust. 2 prawa autorskiego "Wolno nieodpłatnie publicznie wykonywać lub odtwarzać przy pomocy urządzeń lub nośników znajdujących się w tym samym miejscu co publiczność rozpowszechnione utwory podczas imprez szkolnych oraz akademickich, jeżeli nie łączy się z tym osiąganie pośrednio lub bezpośrednio korzyści majątkowej i artyści wykonawcy oraz osoby odtwarzające utwory nie otrzymują wynagrodzenia." Przygotowanie spektaklu teatralnego i jego wystawienie w szkole będzie w rozumieniu prawa autorskiego "wykonaniem utworu", zatem nie można w tej sytuacji osiągać żadnych korzyści majątkowych, niezależnie od tego na co miałyby być przeznaczone zdobyte środki.',
            u'Zgodnie z art. 31 ust. 2 prawa autorskiego "Wolno nieodpłatnie publicznie wykonywać lub odtwarzać przy pomocy urządzeń lub nośników znajdujących się w tym samym miejscu co publiczność rozpowszechnione utwory podczas imprez szkolnych oraz akademickich, jeżeli nie łączy się z tym osiąganie pośrednio lub bezpośrednio korzyści majątkowej i artyści wykonawcy oraz osoby odtwarzające utwory nie otrzymują wynagrodzenia." Przygotowanie spektaklu teatralnego i jego wystawienie w szkole będzie w rozumieniu prawa autorskiego "wykonaniem utworu", zatem nie można w tej sytuacji osiągać żadnych korzyści majątkowych, niezależnie od tego na co miałyby być przeznaczone zdobyte środki.',
            u'Udostępnianie w internecie spektaklu wykracza poza ramy prawne publicznego wykonywania utworu, zatem odpowiedź ta jest błędna.',
            u'Udostępnianie w internecie spektaklu wykracza poza ramy prawne publicznego wykonywania utworu, zatem odpowiedź ta jest błędna.',
            u'Zgodnie z art. 31 ust. 2 prawa autorskiego "Wolno nieodpłatnie publicznie wykonywać lub odtwarzać przy pomocy urządzeń lub nośników znajdujących się w tym samym miejscu co publiczność rozpowszechnione utwory podczas imprez szkolnych oraz akademickich, jeżeli nie łączy się z tym osiąganie pośrednio lub bezpośrednio korzyści majątkowej i artyści wykonawcy oraz osoby odtwarzające utwory nie otrzymują wynagrodzenia." Przygotowanie spektaklu teatralnego i jego wystawienie w szkole będzie w rozumieniu prawa autorskiego "wykonaniem utworu", zatem nie można w tej sytuacji osiągać żadnych korzyści majątkowych, niezależnie od tego na co miałyby być przeznaczone zdobyte środki. Z kolei udostępnianie w internecie spektaklu wykracza poza ramy prawne publicznego wykonywania utworu, zatem żadna z odpowiedzi nie jest poprawna.',
        ),
        (
            u'Ta dyrektywa unijna dotyczy dostępności stron internetowych i aplikacji dla osób niepełnosprawnych. Jednak dotyczy tylko stron z sektora poublicznego. Opisane w pytaniu mechanizmy normuje Web Content Accessibillity Guidelines.',
            u'Dokument będący wytycznymi dotyczącymi ułatwień w dostępie do treści publikowanych w internecie normuje zasady tworzenia stron internetowych na potrzeby osób niepełnosprawnych, tak aby treści online były dostępne dla wszystkich. Wśród zasad pojawiających się w WCAG i dokumentach rozszerzających jego zapisy pojawiają się m.in. takie zalecenia: wszystkie pliki dźwiękowe powinny być uzupełnione o transkrypcję dźwiękową czy też wszystkie pliki wideo powinny być uzupełnione o napisy dla osób niesłyszących. To właśnie w WCAG można znaleźć zestaw norm dzięki, którym strony internetowe są przyjazne dla osób niepełnosprawnych.',
            u'Protokół ten odpowiedzialny jest za przesyłanie dokumentów hipertekstowych w sieci WWW. Nie jest to ani zestaw norm, ani tym bardziej norm określających zasady tworzenia stron internetowych tak aby były przyjazne niepełnosprawnym. Wspomniane zasady znajdują się w dokumencie o nazwie WCAG – Web Content Accessibillity Guidelines.',
            u'Europejski Akt o Dostępności to kolejny krok do ułatwienia życia osobom niepełnosprawnym. Dzięki tym normom uniijnym sprzęty elektroniczne – komputery, smartfony czy nawet bankomaty ale też chociażby proces zakupów przez internet ma być dostosowany do potrzeb osób niepełnosprawnych. To bardzo ważny dokument jednak nie określa on zasad tworzenia stron internetowych tak aby były one dopasowane do potrzeb osób niepełnosprawnych. Normy te zawarte są w WCAG – Web Content Accessibillity Guidelines.',
        ),
        (
            u'Ustawa o ochronie danych osobowych z dnia 29 sierpnia 1997 roku szczegółowo określa jakie dane zalicza się do danych wrażliwych. Są to informacje dotyczące pochodzenia rasowego lub etnicznego, poglądów politycznych, przekonań religijnych lub filozoficznych, przynależności wyznaniowej, partyjnej lub związkowej, stanu zdrowia, kodu genetycznego, nałogów lub życia seksualnego, skazań, orzeczeń o ukaraniu i mandatów karnych, orzeczeń wydanych w postępowaniu sądowych lub administracyjnym. Co ważne od maja 2018 definicja danych wrażliwych ulegnie zmianie!',
            u'Ustawa o ochronie danych osobowych z dnia 29 sierpnia 1997 roku szczegółowo określa jakie dane zalicza się do danych wrażliwych. Są to informacje dotyczące pochodzenia rasowego lub etnicznego, poglądów politycznych, przekonań religijnych lub filozoficznych, przynależności wyznaniowej, partyjnej lub związkowej, stanu zdrowia, kodu genetycznego, nałogów lub życia seksualnego, skazań, orzeczeń o ukaraniu i mandatów karnych, orzeczeń wydanych w postępowaniu sądowych lub administracyjnym. Co ważne od maja 2018 definicja danych wrażliwych ulegnie zmianie!',
            u'Ustawa o ochronie danych osobowych z dnia 29 sierpnia 1997 roku szczegółowo określa jakie dane zalicza się do danych wrażliwych. Są to informacje dotyczące pochodzenia rasowego lub etnicznego, poglądów politycznych, przekonań religijnych lub filozoficznych, przynależności wyznaniowej, partyjnej lub związkowej, stanu zdrowia, kodu genetycznego, nałogów lub życia seksualnego, skazań, orzeczeń o ukaraniu i mandatów karnych, orzeczeń wydanych w postępowaniu sądowych lub administracyjnym. Co ważne od maja 2018 definicja danych wrażliwych ulegnie zmianie!',
            u'Ustawa o ochronie danych osobowych z dnia 29 sierpnia 1997 roku szczegółowo określa jakie dane zalicza się do danych wrażliwych. Są to informacje dotyczące pochodzenia rasowego lub etnicznego, poglądów politycznych, przekonań religijnych lub filozoficznych, przynależności wyznaniowej, partyjnej lub związkowej, stanu zdrowia, kodu genetycznego, nałogów lub życia seksualnego, skazań, orzeczeń o ukaraniu i mandatów karnych, orzeczeń wydanych w postępowaniu sądowych lub administracyjnym. Co ważne od maja 2018 definicja danych wrażliwych ulegnie zmianie! Jednak numer PESEL nie należy, ani nie będzie należał do kategorii danych wrażliwych.',
        ),
        (
            u'Zgodnie z treścią art. 36 Ustawy o prawie autorskim i prawach pokrewnych majątkowe prawa autorskie wygasają z upływem lat siedemdziesięciu od: od śmierci twórcy, a do utworów współautorskich - od śmierci współtwórcy, który przeżył pozostałych; w odniesieniu do utworu, którego twórca nie jest znany - od daty pierwszego rozpowszechnienia, chyba że pseudonim nie pozostawia wątpliwości co do tożsamości autora lub jeżeli autor ujawnił swoją tożsamość; w odniesieniu do utworu, do którego autorskie prawa majątkowe przysługują z mocy ustawy innej osobie niż twórca - od daty rozpowszechnienia utworu, a gdy utwór nie został rozpowszechniony - od daty jego ustalenia; w odniesieniu do utworu audiowizualnego - od śmierci najpóźniej zmarłej z wymienionych osób: głównego reżysera, autora scenariusza, autora dialogów, kompozytora muzyki skomponowanej do utworu audiowizualnego; w odniesieniu do utworu słowno-muzycznego, jeżeli utwór słowny i utwór muzyczny zostały stworzone specjalnie dla danego utworu słowno-muzycznego - od śmierci później zmarłej z wymienionych osób: autora utworu słownego albo kompozytora utworu muzycznego.',
            u'Zgodnie z treścią art. 36 Ustawy o prawie autorskim i prawach pokrewnych majątkowe prawa autorskie  wygasają z upływem lat siedemdziesięciu od: od śmierci twórcy, a do utworów współautorskich - od śmierci współtwórcy, który przeżył pozostałych; w odniesieniu do utworu, którego twórca nie jest znany - od daty pierwszego rozpowszechnienia, chyba że pseudonim nie pozostawia wątpliwości co do tożsamości autora lub jeżeli autor ujawnił swoją tożsamość; w odniesieniu do utworu, do którego autorskie prawa majątkowe przysługują z mocy ustawy innej osobie niż twórca - od daty rozpowszechnienia utworu, a gdy utwór nie został rozpowszechniony - od daty jego ustalenia; w odniesieniu do utworu audiowizualnego - od śmierci najpóźniej zmarłej z wymienionych osób: głównego reżysera, autora scenariusza, autora dialogów, kompozytora muzyki skomponowanej do utworu audiowizualnego; w odniesieniu do utworu słowno-muzycznego, jeżeli utwór słowny i utwór muzyczny zostały stworzone specjalnie dla danego utworu słowno-muzycznego - od śmierci później zmarłej z wymienionych osób: autora utworu słownego albo kompozytora utworu muzycznego.',
            u'Zgodnie z treścią art. 36 Ustawy o prawie autorskim i prawach pokrewnych majątkowe prawa autorskie  wygasają z upływem lat siedemdziesięciu od: od śmierci twórcy, a do utworów współautorskich - od śmierci współtwórcy, który przeżył pozostałych; w odniesieniu do utworu, którego twórca nie jest znany - od daty pierwszego rozpowszechnienia, chyba że pseudonim nie pozostawia wątpliwości co do tożsamości autora lub jeżeli autor ujawnił swoją tożsamość; w odniesieniu do utworu, do którego autorskie prawa majątkowe przysługują z mocy ustawy innej osobie niż twórca - od daty rozpowszechnienia utworu, a gdy utwór nie został rozpowszechniony - od daty jego ustalenia; w odniesieniu do utworu audiowizualnego - od śmierci najpóźniej zmarłej z wymienionych osób: głównego reżysera, autora scenariusza, autora dialogów, kompozytora muzyki skomponowanej do utworu audiowizualnego; w odniesieniu do utworu słowno-muzycznego, jeżeli utwór słowny i utwór muzyczny zostały stworzone specjalnie dla danego utworu słowno-muzycznego - od śmierci później zmarłej z wymienionych osób: autora utworu słownego albo kompozytora utworu muzycznego.',
            u'Zgodnie z treścią art. 36 Ustawy o prawie autorskim i prawach pokrewnych majątkowe prawa autorskie  wygasają z upływem lat siedemdziesięciu od: od śmierci twórcy, a do utworów współautorskich - od śmierci współtwórcy, który przeżył pozostałych; w odniesieniu do utworu, którego twórca nie jest znany - od daty pierwszego rozpowszechnienia, chyba że pseudonim nie pozostawia wątpliwości co do tożsamości autora lub jeżeli autor ujawnił swoją tożsamość; w odniesieniu do utworu, do którego autorskie prawa majątkowe przysługują z mocy ustawy innej osobie niż twórca - od daty rozpowszechnienia utworu, a gdy utwór nie został rozpowszechniony - od daty jego ustalenia; w odniesieniu do utworu audiowizualnego - od śmierci najpóźniej zmarłej z wymienionych osób: głównego reżysera, autora scenariusza, autora dialogów, kompozytora muzyki skomponowanej do utworu audiowizualnego; w odniesieniu do utworu słowno-muzycznego, jeżeli utwór słowny i utwór muzyczny zostały stworzone specjalnie dla danego utworu słowno-muzycznego - od śmierci później zmarłej z wymienionych osób: autora utworu słownego albo kompozytora utworu muzycznego.',
        ),
        (
            u'Zgodnie z treścią artykułu 16 ustawy o prawie autorskim i prawach pokrewnych katalog autorskich praw to między innymi uprawnienia do autorstwa utworu, oznaczenia go swoim imieniem i nazwiskiem, pod pseudonimem lub anonimowo, nienaruszalności treści utworu, integralności, decyzji o pierwszym udostępnieniu utworu publiczności czy też nadzoru nad sposobem korzystania z utworu.',
            u'Zgodnie z treścią artykułu 16 ustawy o prawie autorskim i prawach pokrewnych katalog autorskich praw to między innymi uprawnienia do autorstwa utworu, oznaczenia go swoim imieniem i nazwiskiem, pod pseudonimem lub anonimowo, nienaruszalności treści utworu, integralności, decyzji o pierwszym udostępnieniu utworu publiczności czy też nadzoru nad sposobem korzystania z utworu.',
            u'Zgodnie z treścią artykułu 16 ustawy o prawie autorskim i prawach pokrewnych katalog autorskich praw to między innymi uprawnienia do autorstwa utworu, oznaczenia go swoim imieniem i nazwiskiem, pod pseudonimem lub anonimowo, nienaruszalności treści utworu, integralności, decyzji o pierwszym udostępnieniu utworu publiczności czy też nadzoru nad sposobem korzystania z utworu.',
            u'Zgodnie z treścią artykułu 16 ustawy o prawie autorskim i prawach pokrewnych katalog autorskich praw to między innymi uprawnienia do autorstwa utworu, oznaczenia go swoim imieniem i nazwiskiem, pod pseudonimem lub anonimowo, nienaruszalności treści utworu, integralności, decyzji o pierwszym udostępnieniu utworu publiczności czy też nadzoru nad sposobem korzystania z utworu. Do katalogu praw nie przynależy jednak prawo do wycofania utworu z obiegu.',
        ),
        (
            u'Regulacje dotyczące zasad wyświetlania reklam w Polsce, zawarte zostały w Ustawie o Radiofonii  i Telewizji. Ustawa określa m.in. to jak powinny być wyświetlane reklamy, jakie reklamy są zakazane, czy też określają jakie zasady wyświetlania reklam obowiązują w telewizji publicznej.',
            u'Regulacje dotyczące zasad wyświetlania  reklam w Polsce, zawarte zostały w Ustawie o Radiofonii  I Telewizji. Ustawa określa m.in. to jak powinny być wyświetlane reklamy, jakie reklamy są zakazane m.in. te które ukazują ludzi niszczących środowisko w pozytywnym świetle, czy też określają jakie zasady wyświetlania reklam obowiązują w telewizji publicznej. ',

            u'Regulacje dotyczące zasad wyświetlania reklam w Polsce, zawarte zostały w Ustawie o Radiofonii  I Telewizji. Ustawa określa m.in. to jak powinny być wyświetlane reklamy, jakie reklamy są zakazane, czy też określają jakie zasady wyświetlania reklam obowiązują w telewizji publicznej. Działania takie jak reklamowanie produktów w treści filmów, zwane potocznie lokowaniem produktu jest dozwolone prawnie. Jednak program powinien zawierać stosowną adnotację, która informuje widza o tym, że audycja zawierała lokowanie produktu. ',

            u'Regulacje dotyczące zasad wyświetlania reklam w Polsce, zawarte zostały w Ustawie o Radiofonii  I Telewizji. Ustawa określa m.in. to jak powinny być wyświetlane reklamy, jakie reklamy są zakazane, czy też określają jakie zasady wyświetlania reklam obowiązują w telewizji publicznej. Regulacje prawne uniemożliwiają telewizji publicznej np. przerywanie filmów reklamami. ',
        ),
        (
            u'Rzecznik Praw Obywatelskich stoi na straży wolności, praw człowieka i obywatela, niezależnie od tego do jakiego obszaru życia odnoszą się wspomniane prawa i wolności. Zatem również jeśli w mediach cyfrowych łamane są zagwarantowane w Konstytucji i innych aktach prawnych prawa i wolności Rzecznik Praw Obywatelskich powinien zareagować.',
            u'Minister Cyfryzacji i podlegające mu ministerstwo wprowadzają zmiany, które za zadanie mają pogłębiać rozwój cyfryzacji w Polsce. Choć wprowadzane przez Ministerstwo rozwiązania powinny być zgodne z Konstytucją i powinny chronić praw obywateli to Minister nie jest organem, przed którym można dociekać swoich praw w mediach cyfrowych.',
            u'Rzecznik stoi na straży praw dziecka. Ponieważ osoby niepełnoletnie są ogromną grupą użytkowników internetu, również w mediach cyfrowych ich gwarantowane w Konstytucji i innych aktach prawnych prawa powinny być respektowane. O co dba Rzecznik Praw Dziecka.',
            u'GIODO bardzo szczegółowo określa zasady związane z ochroną danych osobowych w ramach mediów cyfrowych. Dbając w ten sposób o prawa obywateli w określonym zakresie.',
        ),
        (
            u'Mówi się, że internet nie zapomina. A jednak w ramach ochrony danych osobowych, w prawodawstwie funkcjonuje pojęcie takie jak Prawo do zapomnienia. Pozwala ono na zażądanie usunięcia imienia i nazwiska konkretnej osoby z wyszukiwarki internetowej. W maju 2016 roku Europejski Trybunał Praw Człowieka zmusił Google do respektowania tego prawa. Jednak nie każdy z wniosków, które wpływają do Google jest rozpatrywany pozytywnie, ponieważ samo Google kieruje się prawem do informacji i wolności słowa. Przez co prawo do zapomnienia, choć jest rozpatrywane, nie zawsze musi zakończyć się po myśli osoby składającej żądanie.',
            u'Mówi się, że internet nie zapomina. A jednak w ramach ochrony danych osobowych, w prawodawstwie funkcjonuje pojęcie takie jak Prawo do zapomnienia. Pozwala ono na zażądanie usunięcia imienia i nazwiska konkretnej osoby z wyszukiwarki internetowej. W maju 2016 roku Europejski Trybunał Praw Człowieka zmusił Google do respektowania tego prawa. Jednak nie każdy z wniosków, które wpływają do Google jest rozpatrywany pozytywnie, ponieważ samo Google kieruje się prawem do informacji i wolności słowa. Przez co prawo do zapomnienia, choć jest rozpatrywane, nie zawsze musi zakończyć się po myśli osoby składającej żądanie.',
            u'Mówi się, że internet nie zapomina. A jednak w ramach ochrony danych osobowych, w prawodawstwie funkcjonuje pojęcie takie jak Prawo do zapomnienia. Pozwala ono na zażądanie usunięcia imienia i nazwiska konkretnej osoby z wyszukiwarki internetowej. W maju 2016 roku Europejski Trybunał Praw Człowieka zmusił Google do respektowania tego prawa. Jednak nie każdy z wniosków, które wpływają do Google jest rozpatrywany pozytywnie, ponieważ samo Google kieruje się prawem do informacji i wolności słowa. Przez co prawo do zapomnienia, choć jest rozpatrywane, nie zawsze musi zakończyć się po myśli osoby składającej żądanie.',
            u'Mówi się, że internet nie zapomina. A jednak w ramach ochrony danych osobowych, w prawodawstwie funkcjonuje pojęcie takie jak Prawo do zapomnienia. Pozwala ono na zażądanie usunięcia imienia i nazwiska konkretnej osoby z wyszukiwarki internetowej. W maju 2016 roku Europejski Trybunał Praw Człowieka zmusił Google do respektowania tego prawa. Jednak nie każdy z wniosków, które wpływają do Google jest rozpatrywany pozytywnie, ponieważ samo Google kieruje się prawem do informacji i wolności słowa. Przez co prawo do zapomnienia, choć jest rozpatrywane, nie zawsze musi zakończyć się po myśli osoby składającej żądanie.',
            u'Mówi się, że internet nie zapomina. A jednak w ramach ochrony danych osobowych, w prawodawstwie funkcjonuje pojęcie takie jak Prawo do zapomnienia. Pozwala ono na zażądanie usunięcia imienia i nazwiska konkretnej osoby z wyszukiwarki internetowej. W maju 2016 roku Europejski Trybunał Praw Człowieka zmusił Google do respektowania tego prawa. Jednak nie każdy z wniosków, które wpływają do Google jest rozpatrywany pozytywnie, ponieważ samo Google kieruje się prawem do informacji i wolności słowa. Przez co prawo do zapomnienia, choć jest rozpatrywane nie zawsze musi zakończyć się po myśli osoby składającej żądanie.',
        ),
        (
            u'Zgodnie z treścią artykułu 16 ustawy o prawie autorskim i prawach pokrewnych katalog autorskich praw to między innymi uprawnienia do autorstwa utworu, oznaczenia go swoim imieniem i nazwiskiem, pod pseudonimem lub anonimowo, nienaruszalności treści utworu, integralności, decyzji o pierwszym udostępnieniu utworu publiczności czy też nadzoru nad sposobem korzystania z utworu.',
            u'Artykuł 29 ustawy o prawie autorskim mówi, że wolno korzystać z utworów na potrzeby parodii, pastiszu lub karykatury, w zakresie uzasadnionym prawami tych gatunków twórczości. Zatem prawo nie chroni autorów przed parodiowaniem ich dzieł.',
            u'Zgodnie z treścią artykułu 16 ustawy o prawie autorskim i prawach pokrewnych katalog autorskich praw to między innymi uprawnienia do autorstwa utworu, oznaczenia go swoim imieniem i nazwiskiem, pod pseudonimem lub anonimowo, nienaruszalności treści utworu, integralności, decyzji o pierwszym udostępnieniu utworu publiczności czy też nadzoru nad sposobem korzystania z utworu. ',
            u'Zgodnie z treścią artykułu 16 ustawy o prawie autorskim i prawach pokrewnych katalog autorskich praw to między innymi uprawnienia do autorstwa utworu, oznaczenia go swoim imieniem i nazwiskiem, pod pseudonimem lub anonimowo, nienaruszalności treści utworu, integralności, decyzji o pierwszym udostępnieniu utworu publiczności czy też nadzoru nad sposobem korzystania z utworu. Do katalogu praw nie przynależy jednak prawo do wycofania utworu z obiegu. ',
            u'Zgodnie z treścią artykułu 16 ustawy o prawie autorskim i prawach pokrewnych katalog autorskich praw to między innymi uprawnienia do autorstwa utworu, oznaczenia go swoim imieniem i nazwiskiem, pod pseudonimem lub anonimowo, nienaruszalności treści utworu, integralności, decyzji o pierwszym udostępnieniu utworu publiczności czy też nadzoru nad sposobem korzystania z utworu. ',
            u'Autorskie prawa osobiste nie obejmują zakazu kopiowania utworu bez zgody twórcy. Dlatego też ta odpowiedź jest błędna. Zgodnie z treścią artykułu 16 ustawy o prawie autorskim i prawach pokrewnych katalog autorskich praw to między innymi uprawnienia do autorstwa utworu, oznaczenia go swoim imieniem i nazwiskiem, pod pseudonimem lub anonimowo, nienaruszalności treści utworu, integralności, decyzji o pierwszym udostępnieniu utworu publiczności czy też nadzoru nad sposobem korzystania z utworu. ',
        ),
        (
            u'Remiks to stworzenie nowego utworu wykorzystując przy tym już istniejące dzieła. Poprzez zestawienie wybranych elementów, tworzeniu kolaży czy zmienianie uporządkowanych części.  Fragmenty innych utworów wykorzystywać można, a następnie rozpowszechniać pod wieloma warunkami m.in. wówczas gdy posiada się zgodę autora/autorki oryginalnego utworu, zezwala na to licencja, wygasły majątkowe prawa autorskie, czyli minęło 70 lat od śmierci autora, przez co utwory są dostępne w domenie publicznej.',
            u'Remiks to stworzenie nowego utworu wykorzystując przy tym już istniejące dzieła. Poprzez zestawienie wybranych elementów, tworzeniu kolaży czy zmienianie uporządkowanych części.  Fragmenty innych utworów wykorzystywać można, a następnie rozpowszechniać pod wieloma warunkami m.in. wówczas gdy posiada się zgodę autora/autorki oryginalnego utworu, zezwala na to licencja, wygasły majątkowe prawa autorskie, czyli minęło 70 lat od śmierci autora, przez co utwory są dostępne w domenie publicznej. Ściągnięcie materiałów z serwisu do przechowywania plików nie daje prawa do ich rozpowszechniania. ',
            u'Remiks to stworzenie nowego utworu wykorzystując przy tym już istniejące dzieła. Poprzez zestawienie wybranych elementów, tworzeniu kolaży czy zmienianie uporządkowanych części.  Fragmenty innych utworów wykorzystywać można, a następnie rozpowszechniać pod wieloma warunkami m.in. wówczas gdy posiada się zgodę autora/autorki oryginalnego utworu, zezwala na to licencja, wygasły majątkowe prawa autorskie, czyli minęło 70 lat od śmierci autora, przez co utwory są dostępne w domenie publicznej. Dostęp do utworu poprzez media społecznościowe nie daje gwarancji, że można z niego korzystać i go rozpowszechniać.',
            u'Remiks to stworzenie nowego utworu wykorzystując przy tym już istniejące dzieła. Poprzez zestawienie wybranych elementów, tworzeniu kolaży czy zmienianie uporządkowanych części.  Fragmenty innych utworów wykorzystywać można, a następnie rozpowszechniać pod wieloma warunkami m.in. wówczas gdy posiada się zgodę autora/autorki oryginalnego utworu, zezwala na to licencja, wygasły majątkowe prawa autorskie, czyli minęło 70 lat od śmierci autora, przez co utwory są dostępne w domenie publicznej.',
            u'Remiks to stworzenie nowego utworu wykorzystując przy tym już istniejące dzieła. Poprzez zestawienie wybranych elementów, tworzeniu kolaży czy zmienianie uporządkowanych części.  Fragmenty innych utworów wykorzystywać można, a następnie rozpowszechniać pod wieloma warunkami m.in. wówczas gdy posiada się zgodę autora/autorki oryginalnego utworu, zezwala na to licencja, wygasły majątkowe prawa autorskie, czyli minęło 70 lat od śmierci autora, przez co utwory są dostępne w domenie publicznej.',
            u'Remiks to stworzenie nowego utworu wykorzystując przy tym już istniejące dzieła. Poprzez zestawienie wybranych elementów, tworzeniu kolaży czy zmienianie uporządkowanych części.  Fragmenty innych utworów wykorzystywać można, a następnie rozpowszechniać pod wieloma warunkami m.in. wówczas gdy posiada się zgodę autora/autorki oryginalnego utworu, zezwala na to licencja, wygasły majątkowe prawa autorskie, czyli minęło 70 lat od śmierci autora, przez co utwory są dostępne w domenie publicznej. Udostępnienie plików MP3, nawet przez twórców nie uprawnia do rozpowszechniania zremiksowanego utworu.',
        ),
        (
            u'Dane osobowe są chronione i istnieją specjalne przepisy normujące to w jakim zakresie można pobierać i przetwarzać dane osobowe. Ze względu na to każdy sklep internetowy musi udostępniać  informacje o tym co robi z danymi swoich użytkowników. Takie informacje znajdują się w ramach tzw. polityki prywatności. ',
            u'Dane osobowe są chronione i istnieją specjalne przepisy normujące to w jakim zakresie można pobierać i przetwarzać dane osobowe. Ze względu na to każdy sklep internetowy musi udostępniać  informacje o tym co robi z danymi swoich użytkowników. Takie informacje znajdują się w ramach tzw. polityki prywatności. ',
            u'Dane osobowe są chronione i istnieją specjalne przepisy normujące to w jakim zakresie można pobierać i przetwarzać dane osobowe. Ze względu na to każdy sklep internetowy musi udostępniać  informacje o tym co robi z danymi swoich użytkowników. Takie informacje znajdują się w ramach tzw. polityki prywatności. ',
            u'Dane osobowe są chronione i istnieją specjalne przepisy normujące to w jakim zakresie można pobierać i przetwarzać dane osobowe. Ze względu na to każdy sklep internetowy musi udostępniać  informacje o tym co robi z danymi swoich użytkowników. Takie informacje znajdują się w ramach tzw. polityki prywatności. Nie każdy sklep musi natomiast posiadać regulamin. Choć jest to pożądane przez klientów i zwiększa wiarygodność e-sklepu.',
        ),
        (
            u'Wiersze z biblioteki Wolne Lektury znajdują się w domenie publicznej albo publikowane są na licencji CC BY-SA 3.0, która umożliwia taką publikację. Wspomniana licencja Creative Commons zezwala na dzielenie się, tj. kopiowanie i rozpowszechnianie utworów na tej licencji w dowolnym medium i formacie oraz adaptacje, czyli remiksy na bazie utworu dla dowolnego celu, także komercyjnego. W domenie publicznej znajdują się zaś utwory, co do których majątkowe prawa autorskie albo wygasły albo nie były nigdy objęte prawem autorskim. Z tego też względu bez problemu można publikować niekomercyjnie remiks wspomnianych w pytaniu wierszy.',
            u'Wiersze z biblioteki Wolne Lektury znajdują się w domenie publicznej albo publikowane są na licencji CC BY-SA 3.0, która umożliwia taką publikację. Wspomniana licencja Creative Commons zezwala na dzielenie się, tj. kopiowanie i rozpowszechnianie utworów na tej licencji w dowolnym medium i formacie oraz adaptacje, czyli remiksy na bazie utworu dla dowolnego celu, także komercyjnego. W domenie publicznej znajdują się zaś utwory, co do których majątkowe prawa autorskie albo wygasły albo nie były nigdy objęte prawem autorskim. Z tego też względu bez problemu można publikować niekomercyjnie remiks wspomnianych w pytaniu wierszy. ',
            u'Wiersze z biblioteki Wolne Lektury znajdują się w domenie publicznej albo publikowane są na licencji CC BY-SA 3.0, która umożliwia taką publikację. Wspomniana licencja Creative Commons zezwala na dzielenie się, tj. kopiowanie i rozpowszechnianie utworów na tej licencji w dowolnym medium i formacie oraz adaptacje, czyli remiksy na bazie utworu dla dowolnego celu, także komercyjnego. W domenie publicznej znajdują się zaś utwory, co do których majątkowe prawa autorskie albo wygasły albo nie były nigdy objęte prawem autorskim. Z tego też względu bez problemu można publikować niekomercyjnie remiks wspomnianych w pytaniu wierszy. Nie jest do tego potrzebne wnoszenie żadnych dodatkowych opłat.',
            u'Wiersze z biblioteki Wolne Lektury znajdują się w domenie publicznej albo publikowane są na licencji CC BY-SA 3.0, która umożliwia taką publikację. Wspomniana licencja Creative Commons zezwala na dzielenie się, tj. kopiowanie i rozpowszechnianie utworów na tej licencji w dowolnym medium i formacie oraz adaptacje, czyli remiksy na bazie utworu dla dowolnego celu, także komercyjnego. W domenie publicznej znajdują się zaś utwory, co do których majątkowe prawa autorskie albo wygasły albo nie były nigdy objęte prawem autorskim. Z tego też względu bez problemu można publikować niekomercyjnie remiks wspomnianych w pytaniu wierszy.',
        ),
        (
            u'Dozwolony użytek to określenie w polskim prawie autorskim na ustawowe ograniczenie treści wyłącznych praw autorskich, które to określa ustawa o prawie autorskim i prawach pokrewnych. Prawo rozgranicza dozwolony użytek na ten realizowany w zakresie prywatnym oraz publicznym. W ramach dozwolonego użytku prywatnego w większości przypadków nie można wnosić roszczeń finansowych związanych z majątkowym prawem autorskim. Użytkownik może bez zgody twórcy nieodpłatnie korzystać z już rozpowszechnionego utworu, a także udostępniać go nieodpłatnie określonej grupie osób. Zatem sprzedaż kopii płyt z muzyką jest według prawa związanego z dozwolonym użytkiem zabronione. ',
            u'Dozwolony użytek to określenie w polskim prawie autorskim na ustawowe ograniczenie treści wyłącznych praw autorskich, które to określa ustawa o prawie autorskim i prawach pokrewnych. Prawo rozgranicza dozwolony użytek na ten realizowany w zakresie prywatnym oraz publicznym. W ramach dozwolonego użytku prywatnego w większości przypadków nie można wnosić roszczeń finansowych związanych z majątkowym prawem autorskim. Użytkownik może bez zgody twórcy nieodpłatnie korzystać z już rozpowszechnionego utworu, a także udostępniać go nieodpłatnie określonej grupie osób. Nawet w sytuacji gdy film został pobrany z nielegalnego internetowego źródła, oglądanie go nie jest zabronione właśnie ze względu na dozwolony użytek prywatny.',
            u'Dozwolony użytek to określenie w polskim prawie autorskim na ustawowe ograniczenie treści wyłącznych praw autorskich, które to określa ustawa o prawie autorskim i prawach pokrewnych. Prawo rozgranicza dozwolony użytek na ten realizowany w zakresie prywatnym oraz publicznym. W ramach dozwolonego użytku prywatnego w większości przypadków nie można wnosić roszczeń finansowych związanych z majątkowym prawem autorskim. Użytkownik może bez zgody twórcy nieodpłatnie korzystać z już rozpowszechnionego utworu, a także udostępniać go nieodpłatnie określonej grupie osób – w tym także rodzinie.',
            u'Dozwolony użytek to określenie w polskim prawie autorskim na ustawowe ograniczenie treści wyłącznych praw autorskich, które to określa ustawa o prawie autorskim i prawach pokrewnych. Prawo rozgranicza dozwolony użytek na ten realizowany w zakresie prywatnym oraz publicznym. W ramach dozwolonego użytku prywatnego w większości przypadków nie można wnosić roszczeń finansowych związanych z majątkowym prawem autorskim. Użytkownik może bez zgody twórcy nieodpłatnie korzystać z już rozpowszechnionego utworu, a także udostępniać go nieodpłatnie określonej grupie osób.',
        )
    ]
