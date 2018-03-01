# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

from contact.forms import ContactForm


def quiz_question(label, choices):
    return forms.TypedChoiceField(label=label, choices=choices, coerce=int, widget=forms.RadioSelect)


def make_link(text, url):
    return u'<a href="%s">%s</a>' % (url, text)


class TestForm(ContactForm):
    form_tag = '_____'
    pyt1 = quiz_question(
        label=u'1. Na stronie portalu internetowego pod jednym z artykułów opublikowano komentarz o treści '
              u'„Nie wszyscy muzułmanie to terroryści, ale wszyscy terroryści to muzułmanie”. '
              u'Komentarz podlega moderacji i powinien:',
        choices=[
            (1, u'zostać zachowany, ponieważ jest prywatną opinią korzystającą z wolności słowa,'),
            (0, u'zostać zachowany, ponieważ informuje o fakcie,'),
            (2, u'zostać usunięty, ponieważ jest wprowadzającą w błąd interpretacją faktów.'),
        ])
    pyt2 = quiz_question(
        label=u'2. Aby przygotować podcast, należy posiadać przynajmniej:',
        choices=[
            (0, u'półprofesjonalny mikrofon radiowy, z wbudowanym interfejsem dźwiękowym, '
                u'komercyjne oprogramowanie typu DAW, średnio-zaawansowane umiejętności cyfrowej obróbki dźwięku,'),
            (1, u'urządzenie do nagrywania dźwięku, laptop, oprogramowanie dedykowane do tworzenia podcastów,'),
            (2, u'urządzenie do nagrywania dźwięku, podstawowe oprogramowanie do edycji dźwięku, '
                u'podstawowe umiejętności cyfrowej obróbki dźwięku.')])
    pyt3 = quiz_question(
        label=u'3. Muzeum cyfrowe chce udostępnić skan XIV-wiecznego kodeksu. '
              u'Zgodnym z ideą domeny publicznej sposobem jego udostępnienia będzie:',
        choices=[
            (0, u'udostępnienie go na licencji Creative Commons,'),
            (2, u'udostępnienie go bez licencji z czytelnym wskazaniem praw do dowolnego wykorzystania,'),
            (1, u'udostępnienie go w pliku jakości produkcyjnej.')])
    pyt4 = quiz_question(
        label=u'4. Aby uniknąć możliwości podejrzenia przez niepowołane osoby, jakie strony internetowe '
              u'odwiedzałaś/eś ostatnio, powinieneś/powinnaś:',
        choices=[
            (0, u'ustawić opcję otwierania nowej sesji przeglądarki bez wyświetlania ostatnio używanych kart '
                u'oraz regularnie czyścić historię wyszukiwania,'),
            (2, u'wylogowywać się lub blokować ekran za każdym razem, kiedy odchodzisz od komputera, tabletu '
                u'lub odkładasz gdzieś telefon, regularnie czyścić dane zgromadzone przez przeglądarkę internetową,'),
            (1, u'wylogowywać się lub blokować ekran za każdym razem, kiedy odchodzisz od komputera, tabletu '
                u'lub odkładasz gdzieś telefon, regularnie czyścić historię przeglądanych stron.')])
    pyt5 = quiz_question(
        label=u'5. Komentarz opublikowany w Internecie ma taką samą wartość bez względu na to, '
              u'czy jest anonimowy czy podpisany imieniem i nazwiskiem:',
        choices=[
            (0, u'tak, ze względu na zasadę wolności słowa,'),
            (2, u'to zależy od jego treści i kontekstu, w którym go opublikowano,'),
            (1, u'tak, z punktu widzenia odpowiedzialności prawnej.')])
    pyt6 = quiz_question(
        label=u'6. Wraz z grupą osób zamierzasz przygotować cyfrową opowieść (narrację) na temat współczesnych '
              u'nastolatków i ich stosunku do szkoły. Żeby praca była efektywna, a jej rezultat efektowny, warto '
              u'zorganizować wspólną pracę w następujących krokach:',
        choices=[
            (2, u'przeprowadzić wspólną dyskusję odnośnie możliwych tematów opowieści, wybrać jeden, ustalić, '
                u'co należy zrobić, podzielić zadania w grupie i przygotować scenariusz narracji '
                u'(opisać poszczególne sceny, co się w nich znajdzie, co będzie potrzebne do ich przygotowania),'),
            (0, u'zgromadzić jak najwięcej materiałów wideo i zdjęć, wybrać oprogramowanie do obróbki wideo i wspólnie '
                u'decydować o kolejności scen i zawartości opowieści,'),
            (1, u'wybrać temat opowieści, zgromadzić jak najwięcej filmików i zdjęć, podzielić się zadaniami w grupie, '
                u'zmontować narrację z części przygotowanych przez uczestników zespołu.')])
    pyt7 = quiz_question(
        label=u'7. Firma telekomunikacyjna wykorzystuje boty do automatycznego odpowiadania na pytania klientów '
              u'zadawane w serwisie społecznościowym. Boty zwracają się do wszystkich po imieniu. Kiedy użytkownik, '
              u'który sobie tego nie życzy, wyraża swoje niezadowolenie z takiej formy rozmowy, firma powinna:',
        choices=[
            (2, u'przeprosić użytkownika, szanując preferowane przez niego reguły komunikacji,'),
            (0, u'zignorować użytkownika odwołując się do zasad netykiety,'),
            (1, u'zareagować zgodnie z wypracowanymi wewnętrznie zasadami komunikacji.')])
    pyt8 = quiz_question(
        label=u'8. Jesteś członkiem/członkinią grupy, która przygotowuje aplikację mającą ułatwić osobom '
              u'z niepełnosprawnościami poruszanie się po Twojej miejscowości. Oprogramowanie będzie m.in. informować, '
              u'czy przy określonej instytucji, firmie, sklepie, znajdują się miejsca parkingowe dla osób '
              u'z niepełnosprawnościami i ile ich jest. Aby aplikacja działała prawidłowo, powinieneś/powinnaś:',
        choices=[
            (1, u'przygotować listę najważniejszych obiektów w Twoim mieście i skontaktować się z ich administracją, '
                u'pytając o liczbę miejsc parkingowych,'),
            (0, u'poszukać informacji o dostępnych miejscach parkingowych na stronach instytucji, firm i sklepów,'),
            (2, u'skontaktować się z administracją obiektów, o których będzie informować aplikacja, udać się również '
                u'do tych obiektów, aby potwierdzić ilość dostępnych miejsc, spróbować zgromadzić informacje o tym, '
                u'jak często miejsca parkingowe są zajmowane przez ludzi pełnosprawnych.')])
    pyt9 = quiz_question(
        label=u'9. Pojęcie „niewidzialnej pracy” może dotyczyć:',
        choices=[
            (2, u'moderatorów mediów społecznościowych zatrudnianych w krajach o niskich kosztach pracy,'),
            (1, u'użytkowników serwisów społecznościowych publikujących codziennie i bez wynagrodzenia własne '
                u'materiały w tym serwisie,'),
            (0, u'informatyków budujących rozwiązania IT dla firm.')])

    pyt10 = quiz_question(
        label=u'10. Możesz uważać, że informacje, do których docierasz, są wiarygodne, ponieważ:',
        choices=[
            (1, u'pojawiają się w wielu telewizyjnych serwisach informacyjnych, na profilach społecznościowych '
                u'moich znajomych i w różnorodnych internetowych serwisach informacyjnych, wszędzie przedstawiane '
                u'są w podobny sposób,'),
            (2, u'pojawiają się w wielu serwisach informacyjnych, na profilach moich znajomych, zawierają odnośniki '
                u'do oryginalnych źródeł, do których można dotrzeć,'),
            (0, u'pojawiają się na profilach wielu moich znajomych w serwisach społecznościowych i '
                u'w kilku internetowych serwisach informacyjnych.')])
    pyt11 = quiz_question(
        label=u'11. W pewnym mieście prokuratura bada umowy z wykonawcami projektów budżetu obywatelskiego. '
              u'Nikomu, jak dotąd, nie postawiono zarzutów. Która postać tytułu newsa opublikowanego '
              u'na lokalnym portalu internetowym będzie najbardziej zgodna z zasadami etyki dziennikarskiej?',
        choices=[
            (1, u'„Budżet obywatelski: niejasne umowy z wykonawcami?”,'),
            (2, u'„Prokuratura zbada umowy z wykonawcami projektów budżetu obywatelskiego.”,'),
            (0, u'„Zobacz, które firmy mogły obłowić się na projektach budżetu obywatelskiego!”.')])
    pyt12 = quiz_question(
        label=u'12. Dołączyłeś/aś do grupy, która zbiera informacje o problemach dotyczących młodych ludzi '
              u'w Twojej okolicy. Zamierzacie zaprezentować zgromadzone informacje w interesujący sposób, '
              u'tak by zainteresować lokalne media, służby miejskie, zwykłych obywateli i Waszych rówieśników. '
              u'Grupa nie ma możliwości regularnego spotykania się, dlatego wybraliście pracę wyłącznie '
              u'przez Internet. Który zestaw narzędzi pozwoli Wam na jak najlepszą, wspólną pracę?',
        choices=[
            (0, u'mail grupowy, komunikator tekstowy (np. Messenger), oprogramowanie do tworzenia podcastów, '
                u'stacjonarne narzędzie do tworzenia prezentacji (np. Power Point),'),
            (1, u'mail grupowy, komunikator tekstowy zespołu (np. Slack), narzędzie do kolektywnego tworzenia '
                u'map myśli (np. Coggle), blog redagowany przez wszystkich uczestników projektu, aplikacja do '
                u'synchronizowania plików w chmurze (np. Dropbox), narzędzie do grupowej komunikacji za pomocą wideo '
                u'(np. Skype),'),
            (2, u'aplikacja do zarządzania zadaniami zespołu i terminami do wykonania (np. Wunderlist), '
                u'narzędzie do tworzenia kolektywnych notatek (np. OneNote) lub wspólnej pracy z tekstem '
                u'(np. EtherPad, Google Dokumenty), grupa w serwisie społecznościowym lub tekstowy komunikator '
                u'zespołu (np. Messenger lub Slack), narzędzia do gromadzenia lub prezentowania materiałów '
                u'(np. wspólny blog, kanał w serwisie społecznościowym).')])
    pyt13 = quiz_question(
        label=u'13. Poniżej podano wybrane cechy hasła opublikowanego w Wikipedii. '
              u'Która z nich jest najbardziej pomocna przy analizie jakości hasła?',
        choices=[
            (0, u'liczba edycji hasła,'),
            (1, u'długość i struktura hasła,'),
            (2, u'obecność i jakość przypisów.')])
    pyt14 = quiz_question(
        label=u'14. Na przeglądanej stronie internetowej znalazłeś/aś interesującą grafikę, którą chciał(a)byś '
              u'wykorzystać w przygotowywanej cyfrowej narracji. Nie jest ona jednak podpisana. Co robisz?',
        choices=[
            (0, u'podpisuję grafikę adresem strony, na której ją znalazłem/am,'),
            (1, u'korzystam z opcji wyszukiwania obrazem w wyszukiwarce grafiki, chcąc znaleźć inne strony, '
                u'gdzie pojawiła się grafika,'),
            (2, u'korzystam z opcji wyszukiwania obrazem, a jeśli to się nie powiedzie, skontaktuję się '
                u'z administratorem strony, na której znalazłem/am grafikę, pytając o autora; przeglądam także '
                u'informacje o stronie, szukając ewentualnych informacji o zasadach publikacji treści; być może '
                u'autor informuje, że wszystkie grafiki są jego autorstwa.')])
    pyt15 = quiz_question(
        label=mark_safe(
            u'15. W nieistniejącym języku programowania TEST dana jest funkcja zapisana w następujący sposób:'
            u'<p><code>funkcja f(a) { wyświetl a + b;<br>'
            u'}</code></p>'
            u'<strong>Przeczytaj uważnie kod i zastanów się, jak działa ta funkcja.'
            u'Główną wadą tego kodu jest przetwarzanie brakującego argumentu:</strong>'),
        choices=[
            (2, u'b,'),
            (1, u'b będącego dowolną liczbą,'),
            (0, u'f.')])
    pyt16 = quiz_question(
        label=u'16. Przygotowujesz teledysk do utworu nagranego przez Twój zespół. Efekt swojej pracy opublikujesz '
              u'na kanale zespołu na YouTube. Teledysk nie może łamać praw autorskich, w przeciwnym razie zostanie '
              u'usunięty z serwisu. W teledysku możesz wykorzystać zdjęcia, ikony, fragmenty filmów:',
        choices=[
            (1, mark_safe(
                u'znalezionych w wyszukiwarce serwisu Flickr na licencji %s, przygotowanych przez Ciebie, '
                u'ściągniętych z serwisu %s,' % (
                    make_link(u'CC BY-SA', 'https://www.flickr.com/creativecommons/by-sa-2.0/'),
                    make_link(u'The Noun Project', 'https://thenounproject.com')))),
            (2, mark_safe(
                u'znalezionych w wyszukiwarce serwisu Flickr na licencji %s, przygotowanych przez Ciebie, '
                u'ściągniętych z %s,' % (
                    make_link(u'CC-BY', 'https://www.flickr.com/creativecommons/by-2.0/'),
                    make_link(u'serwisu ze zdjęciami NASA',
                              'https://www.nasa.gov/multimedia/imagegallery/index.html')))),
            (0, mark_safe(
                u'znalezionych w wyszukiwarce serwisu Flickr na licencji %s, przygotowanych przez Ciebie, '
                u'ściągniętych z wyszukiwarki grafiki Google.' %
                make_link('CC-BY-NC', 'https://www.flickr.com/creativecommons/by-nc-2.0/')))])
    pyt17 = quiz_question(
        label=mark_safe(
            u'17. Muzeum cyfrowe udostępniło skan druku propagandowego z pierwszej połowy XVII w. '
            u'w humorystyczny sposób przedstawiający strony angielskiej wojny domowej (trwającej z przerwami '
            u'między 1642 a 1651 rokiem):'
            u'<p><a href="https://commons.wikimedia.org/wiki/File:Engl-Bürgerkrieg.JPG">'
            u'<img src="https://upload.wikimedia.org/wikipedia/commons/c/c6/Engl-B%C3%BCrgerkrieg.JPG"></a></p>'
            u'<p><a href="https://commons.wikimedia.org/wiki/File:Engl-Bürgerkrieg.JPG">'
            u'https://commons.wikimedia.org/wiki/File:Engl-Bürgerkrieg.JPG</a></p>'
            u'<strong>Najlepszym zestawem tagów dla osoby katalogującej pliki cyfrowe w muzeum, '
            u'a równocześnie najbardziej użytecznym dla użytkowników przeszukujących stronę '
            u'zestawem słów kluczowych opisujących ten obiekt będzie:</strong>'),
        choices=[
            (2, u'Anglia, wojna domowa, karykatura, propaganda,'),
            (0, u'komiks, śmiech, Anglicy, Wielka Brytania, psy,'),
            (1, u'Angielska Wojna Domowa 1642-1651, propaganda.')])
    pyt18 = quiz_question(
        label=u'18. Podczas wycieczki szkolnej zrobiłaś/eś sporo zdjęć znajomym, w różnych sytuacjach. '
              u'Masz również dostęp do wielu fotografii, które przygotowali Twoi koledzy i koleżanki. '
              u'Zamierzasz niektóre z nich zamieścić na swoim kanale w serwisie społecznościowym. Możesz opublikować:',
        choices=[
            (0, u'zdjęcia prezentujące selfie (o ile nie przedstawiają więcej niż dwóch osób), '
                u'zdjęcia grupy podczas zwiedzania, zdjęcia, które ktoś zrobił Tobie na tle zwiedzanych obiektów, '
                u'zdjęcia, na których ludzie się uśmiechają i cieszą, że robisz im zdjęcie,'),
            (1, u'zdjęcia prezentujące selfie (ale tylko Twoje), zdjęcia pokazujące w oddali grupę na tle '
                u'zwiedzanych obiektów, zdjęcia, zdjęcia na których widać tylko Ciebie, na tle zwiedzanych obiektów,'),
            (2, u'zdjęcia prezentujące selfie (na których jesteś Ty, ale również inne osoby, które potwierdziły, '
                u'że możesz opublikować fotografie), zdjęcia na których widać tylko Ciebie '
                u'i masz zgodę na ich publikację od osoby, która wykonała fotografię, '
                u'wykonane przez Ciebie zdjęcia zwiedzanych obiektów.')])
    pyt19 = quiz_question(
        label=u'19. Korzystając z sieci, natrafiamy na różne interesujące informacje. '
              u'Pojawiają się w wielu serwisach informacyjnych, społecznościowych, w postaci reklam '
              u'dołączanych do materiałów wideo, reklam zamieszczonych w tekstach itp. '
              u'Na co warto zwracać uwagę, podczas codziennego korzystania z mediów, '
              u'żeby efektywnie wykorzystać czas spędzony w Internecie?',
        choices=[
            (1, u'zaplanować czas spędzany na korzystaniu z mediów i starać się trzymać swojego planu, '
                u'nie unikasz jednak nagłych rozmów przez komunikator, oglądania postów, '
                u'zdjęć i filmików dodawanych przez znajomych,'),
            (0, u'zaplanować, co będziesz robił(a), ale traktujesz to jako ramę działania, wiesz, '
                u'że po drodze pojawi się wiele interesujących informacji, z których skorzystasz,'),
            (2, u'zaplanować czas spędzany na korzystaniu z mediów i rejestrować, co, '
                u'kiedy i przez ile czasu robisz, np. instalując aplikację do mierzenia czasu spędzanego w sieci. '
                u'Następnie analizujesz zebrane informacje i starasz się określić, co robisz zbyt często '
                u'i jakie rzeczy odciągają Twoją uwagę od tych zaplanowanych.')])
    pyt20 = quiz_question(
        label=u'20. Blokująca reklamy wtyczka do przeglądarki działa w następujący sposób:',
        choices=[
            (0, u'analizuje treść tekstów oraz obrazków i blokuje te, które zawierają reklamy,'),
            (1, u'blokuje wyświetlanie plików reklam zanim wyświetli je przeglądarka,'),
            (2, u'blokuje komunikację przeglądarki z serwerami publikującymi reklamy.')])

    ANSWER_COMMENTS = [
        (
            u"Stwierdzenie „Nie wszyscy muzułmanie to terroryści, ale wszyscy terroryści to muzułmanie” nie "
            u"odzwierciedla faktów. O ile prawdą jest, że „Nie wszyscy muzułmanie to terroryści”, to błędnym "
            u"założeniem jest, że „wszyscy terroryści są muzułmanami”. Terroryzm jako akt agresji fizycznej wymierzony"
            u" przeciwko innym osobom nie jest domeną tej, czy innej religii. Wynika on często z fundamentalistycznych "
            u"postaw i może pojawić się w różnych kontekstach politycznych i społecznych, a nie tylko religijnych. "
            u"Z drugiej strony, każdemu użytkownikowi Internetu przysługuje wolność słowa, która oznacza prawo "
            u"do publicznego wyrażania własnych poglądów w przestrzenie publicznej. Zachęca do tego zwłaszcza możliwość"
            u" zostawiania komentarzy pod różnego rodzaju artykułami. Należy liczyć się z tym, że część z nich może "
            u"wprowadzać w błąd. Jeśli przyjmiemy interpretację, zgodnie z którą wpis użytkownika na portalu "
            u"internetowym jest opinią, to mamy prawo do jego zachowania.\n"
            u"Jeśli chcesz pogłębić swoją wiedzę na temat „terroryzmu” możesz przeczytać artykuł "
            u"pt. „Zjawisko terroryzmu”: "
            u"http://www.ies.krakow.pl/wydawnictwo/prokuratura/pdf/2012/07-08/11resztak.pdf.\n"
            u"\n"
            u"O prawie do wolności wypowiedzi w Internecie i zagrożeniach związanych z jego ograniczeniem możesz "
            u"przeczytać w komentarzu prawnika pt. „Masz prawo swobodnie wypowiadać się w Internecie, tak samo jak "
            u"wyjść z domu i chodzić po ulicach!”: "
            u"http://prawokultury.pl/newsy/masz-prawo-swobodnie-wypowiadac-sie-w-internecie-t/.",

            u"Stwierdzenie „Nie wszyscy muzułmanie to terroryści, ale wszyscy terroryści to muzułmanie” nie "
            u"odzwierciedla faktów. W tym przypadku należy odróżnić fakt, czyli coś co naprawdę się wydarzyło, "
            u"od opinii, która określa nasz sąd na temat wybranych przez nas kwestii. O ile prawdą jest, że "
            u"„Nie wszyscy muzułmanie to terroryści”, to błędnym założeniem jest, że „wszyscy terroryści są "
            u"muzułmanami”. Terroryzm jako akt agresji fizycznej wymierzony przeciwko innym osobom nie jest domeną "
            u"tej, czy innej religii. Wynika on często z fundamentalistycznych postaw i może pojawić się w różnych "
            u"kontekstach politycznych i społecznych, a nie tylko religijnych. Zachowanie wpisu zawierającego powyższą "
            u"treść może wprowadzać w błąd jego czytelników ponieważ nie odnosi się do faktów, dlatego najlepszą opcją "
            u"jest jego usunięcie.\n"
            u"\n"
            u"Jeśli chcesz pogłębić swoją wiedzę na temat „terroryzmu” możesz przeczytać artykuł "
            u"pt. „Zjawisko terroryzmu”: "
            u"http://www.ies.krakow.pl/wydawnictwo/prokuratura/pdf/2012/07-08/11resztak.pdf.",

            u"Stwierdzenie „Nie wszyscy muzułmanie to terroryści, ale wszyscy terroryści to muzułmanie” "
            u"nie odzwierciedla faktów i jest błędną ich interpretacją W tym przypadku należy odróżnić fakt, "
            u"czyli coś, co naprawdę się wydarzyło, od opinii, która określa nasz sąd na temat wybranych przez nas "
            u"kwestii. O ile prawdą jest, że „Nie wszyscy muzułmanie to terroryści”, to błędnym założeniem jest, że "
            u"„wszyscy terroryści są muzułmanami”. Terroryzm jako akt agresji fizycznej wymierzony przeciwko innym "
            u"osobom nie jest domeną tej, czy innej religii. Wynika on często z fundamentalistycznych postaw i może "
            u"pojawić się w różnych kontekstach politycznych i społecznych, a nie tylko religijnych. Zachowanie wpisu "
            u"zawierającego powyższą treść może wprowadzać w błąd jego czytelników, dlatego najlepszą opcją jest jego "
            u"usunięcie.\n"
            u"\n"
            u"Jeśli chcesz pogłębić swoją wiedzę na temat „terroryzmu” możesz przeczytać artykuł "
            u"pt. „Zjawisko terroryzmu”: "
            u"http://www.ies.krakow.pl/wydawnictwo/prokuratura/pdf/2012/07-08/11resztak.pdf."),
        (
            u"Wymienione narzędzia i umiejętności brzmią bardzo profesjonalnie, a ich wartość wydaje się być "
            u"bardzo wysoka. Jeśli każdy zakładałby, że wszystkie one są potrzebne do rozpoczęcia nagrywania audycji, "
            u"nigdy by tego nie zrobił.\n"
            u"\n"
            u"Tak jak nie od razu Rzym zbudowano, tak nie od razu trzeba nagrywać w profesjonalnym studio. Nawet "
            u"zawodowi podcasterzy od czegoś musieli zacząć – w większości od mikrofonu wbudowanego w komputer. Prawie "
            u"każdy młody człowiek ma w ręku znacznie doskonalsze narzędzie, jakim jest smartfon. W Internecie można "
            u"łatwo znaleźć darmowe oprogramowanie do obróbki dźwięku i tutoriale, które pomogą w tworzeniu podcastu.\n"
            u"\n"
            u"O tym, jak zacząć tworzyć podcast, nie wydając nawet złotówki przeczytasz tu: "
            u"https://malawielkafirma.pl/wlasny-podcast-za-darmo/.",

            u"Wymienione narzędzia i umiejętności brzmią profesjonalnie, nie wszyscy mogą pozwolić sobie na taki "
            u"zakup. Ale czy faktycznie jest to konieczne? Jeśli każdy zakładałby, że wszystkie one są potrzebne do "
            u"rozpoczęcia nagrywania audycji, nigdy by tego nie zrobił. Do przygotowania podcastu nie trzeba "
            u"wykorzystywać komputera. Potrzebne jest urządzenie, które pozwoli na nagrywanie dźwięku i jego "
            u"podstawową obróbkę (może to być zatem także smartfon).\n"
            u"\n"
            u"O tym, jak zacząć tworzyć podcast nie wydając nawet złotówki przeczytasz tu: "
            u"https://malawielkafirma.pl/wlasny-podcast-za-darmo/.",

            u"Urządzenie do nagrywania dźwięku i możliwość jego podstawowej edycji (zarówno jeśli chodzi o dostępne "
            u"oprogramowanie, jak i posiadane umiejętności), to wystarczający początek. Z czasem, jeśli tworzenie "
            u"podcastu okaże się pasją, można zdecydować się na poszerzenie wachlarza narzędzi, którymi będzie się "
            u"posługiwać.\n"
            u"\n"
            u"O tym, jak zacząć tworzyć podcast nie wydając nawet złotówki przeczytasz tu: "
            u"https://malawielkafirma.pl/wlasny-podcast-za-darmo/."),
        (
            u"Utwory powstałe w czasach kiedy nie obowiązywały prawa autorskie należą do tak zwanej domeny publicznej. "
            u"Domeną publiczną oznaczany tę twórczość i te utwory, do których wygasły majątkowe prawa autorskie, "
            u"więc żadna licencja nie ma w tym przypadku zastosowania. Poprzez publikowanie utworu na licencjach "
            u"Creative Commons przekazujemy informację o tym, że chcemy dzielić się swoimi utworami (w szerszym bądź "
            u"węższym zakresie). Zasada ta nie dotyczy wszystkich licencji CC. Tą, która dają największą dowolność "
            u"korzystania z utworu, jest licencja CC BY (Creative Commons Uznanie Autorstwa).\n"
            u"Mówiąc inaczej, łatwiej nam jest wykorzystywać zdjęcia, obrazy, czy też muzykę na licencji CC "
            u"do własnych celów (np. w prezentacji lub na swojej stronie internetowej), ponieważ nie musimy prosić "
            u"autora o pozwolenie na ich użytkowanie – wszystko oczywiście zależy od rodzaju licencji CC, a tych jest "
            u"kilka. Warto wcześniej się z nimi zapoznać na stronie: https://creativecommons.pl.\n"
            u"\n"
            u"Z definicją domeny publicznej można zapoznać się na stronie: "
            u"http://domenapubliczna.org/co-to-jest-domena-publiczna/.\n"
            u"\n"
            u"Więcej o prawach autorskich można przeczytać w Ustawie z dnia 4 lutego 1994 r. o prawie autorskich "
            u"i prawach pokrewnych: "
            u"http://isap.sejm.gov.pl/Download?id=WDU19940240083&type=3 "
            u"oraz na stronie http://prawokultury.pl.",

            u"XIV-wieczny kodeks powstał w czasach, w których nie obowiązywały tak zwane prawa autorskie. "
            u"Z tego względu jego udostępnienie i rozpowszechnianie w jakikolwiek sposób jest dozwolone bez podawania "
            u"licencji, ponieważ kodeks ten należy już do domeny publicznej. Prawa autorskie to zbiór reguł "
            u"dotyczących praw osobistych i majątkowych, jakie nam przysługują przy utworach (np. zdjęciach, muzyce), "
            u"który stworzyliśmy osobiście. Z kolei domeną publiczną określamy tę twórczość i te utwory, z których "
            u"możemy korzystać w dowolny sposób, ponieważ prawa autorskie wygasły (minęło 70 lat od śmierci ich "
            u"twórców) lub utwory powstały wtedy, kiedy prawa autorskie nie istniały.\n"
            u"\n"
            u"O idei udostępniania utworów na zasadach licencji Creative Commons można przeczytać na stronie: "
            u"https://creativecommons.pl.\n"
            u"\n"
            u"Z definicją domeny publicznej można zapoznać się na stronie: "
            u"http://domenapubliczna.org/co-to-jest-domena-publiczna/.\n"
            u"\n"
            u"Więcej o prawa autorskich można przeczytać w Ustawie z dnia 4 lutego 1994 r. o prawie autorskich "
            u"i prawach pokrewnych: http://isap.sejm.gov.pl/Download?id=WDU19940240083&type=3 oraz na stronie "
            u"http://prawokultury.pl.",

            u"Ważne jest, aby wszystkie dokumenty o znaczeniu historycznym udostępnianie były odbiorcom w jak "
            u"najlepszej jakości produkcyjnej. W przypadku XIV-wiecznego kodeksu oznacza to, że muzeum cyfrowe powinno "
            u"postarać się o zeskanowanie dokumenty w wysokiej rozdzielczości, która umożliwi dokładne zaznajomienie "
            u"się z jego treścią szerokim rzeszom odbiorców. Jednak idea domeny publicznej zakłada przede wszystkim "
            u"możliwość korzystania z udostępnianego utworu bez ograniczeń wynikających z praw autorskich. Domeną "
            u"publiczną określamy tę twórczość i te utwory, z których możemy korzystać w dowolny sposób, ponieważ "
            u"prawa autorskie dawno wygasły lub powstały wtedy, kiedy prawa autorskie nie istniały. Prawa autorskie to "
            u"zbiór reguł dotyczących praw jakie nam przysługują przy utworach (np. zdjęciach, muzyce), które "
            u"stworzyliśmy osobiście. Na przykład jedną z ważniejszych kwestii dotyczących praw autorskich jest "
            u"pobieranie opłat za każdorazowe użycie skomponowanego przez nas utworu.\n"
            u"\n"
            u"O idei udostępniania utworów na zasadach licencji Creative Commons można przeczytać na stronie: "
            u"https://creativecommons.pl.\n"
            u"\n"
            u"Z definicją domeny publicznej można zapoznać się na stronie: "
            u"http://domenapubliczna.org/co-to-jest-domena-publiczna/.\n"
            u"\n"
            u"Więcej o prawa autorskich można przeczytać w Ustawie z dnia 4 lutego 1994 r. o prawie autorskich "
            u"i prawach pokrewnych: http://isap.sejm.gov.pl/Download?id=WDU19940240083&type=3 oraz na stronie "
            u"http://prawokultury.pl."),
        (
            u"Zastosowanie takich metod ochrony swojej prywatności nie gwarantuje skutecznego działania. "
            u"Komputer odnotowuje nasze działania na różne sposoby – historia odwiedzanych stron to tylko jeden "
            u"z nich. Dane zapisane w formularzach, „ciasteczka” (niewielkie informacje, wysyłane przez serwis "
            u"internetowy, który odwiedzamy i zapisywane na urządzeniu końcowym – komputerze, laptopie, smartfonie – "
            u"z którego korzystamy podczas przeglądania stron internetowych: http://wszystkoociasteczkach.pl/) "
            u"pozwolą zainteresowanej osobie ustalić, co robiłeś. Ważne jest także chronienie swoich kont i ich danych,"
            u" zawsze pamiętaj o wylogowaniu się i zablokowaniu komputera, jeśli odchodzisz od niego na chwilę.\n"
            u"\n"
            u"Pamiętaj także, że jeśli korzystasz ze swojego konta Google na wielu urządzeniach, sam serwis tworzy "
            u"synchronizowaną historię aktywności. Jak ją usunąć, dowiesz się tu:\n"
            u"https://support.google.com/websearch/answer/54068?hl=pl&ref_topic=1638123.\n"
            u"\n"
            u"Więcej o ochronie prywatności w Internecie dowiesz się tu: https://panoptykon.org/ i tu: "
            u"http://www.saferinternet.pl/pl/ochrona-prywatnosci.",

            u"Kompleksowe stosowanie różnych metod ochrony swojej prywatności pozwala nam na zachowanie prywatności w "
            u"Internecie. Pamiętanie o tym, że komputer odnotowuje nasze działania na różne sposoby – historia "
            u"odwiedzanych stron to tylko jeden z nich – to istotny element skutecznej ochrony. Dane zapisane w "
            u"formularzach, „ciasteczka” (niewielkie informacje, wysyłane przez serwis internetowy, który odwiedzamy i "
            u"zapisywane na urządzeniu końcowym – komputerze, laptopie, smartfonie – z którego korzystamy podczas "
            u"przeglądania stron internetowych: http://wszystkoociasteczkach.pl/) pozwolą zainteresowanej osobie "
            u"ustalić, co robiłeś, dlatego usuwanie historii i wszystkich pozostałych danych gromadzonych przez "
            u"przeglądarkę to czynności, które są niezbędne. Ważne jest także chronienie swoich kont i ich danych, "
            u"zawsze pamiętaj o wylogowaniu się i zablokowaniu komputera, jeśli odchodzisz od niego na chwilę.\n"
            u"\n"
            u"Pamiętaj także, że jeśli korzystasz ze swojego konta Google na wielu urządzeniach, sam serwis Google "
            u"tworzy synchronizowaną historię aktywności. Jak ją usunąć, dowiesz się tu:\n"
            u"https://support.google.com/websearch/answer/54068?hl=pl&ref_topic=1638123.\n"
            u"\n"
            u"\n"
            u"Więcej o ochronie prywatności w Internecie dowiesz się tu:\n"
            u"http://www.saferinternet.pl/pl/ochrona-prywatnosci.",

            u"Kompleksowe stosowanie różnych metod ochrony swojej prywatności pozwala nam na zachowanie prywatności "
            u"w Internecie. Pamiętanie o tym, że komputer odnotowuje nasze działania na różne sposoby – historia "
            u"odwiedzanych stron to tylko jeden z nich – to istotny element skutecznej ochrony. Dane zapisane "
            u"w formularzach, „ciasteczka” (niewielkie informacje, wysyłane przez serwis internetowy, który odwiedzamy "
            u"i zapisywane na urządzeniu końcowym – komputerze, laptopie, smartfonie – z którego korzystamy podczas "
            u"przeglądania stron internetowych: http://wszystkoociasteczkach.pl/) pozwolą zainteresowanej osobie "
            u"ustalić, co robiłeś. Dlatego usuwanie historii nie wystarczy, konieczne jest kasowanie wszystkich "
            u"pozostałych danych gromadzonych przez przeglądarkę. Ważne jest także chronienie swoich kont i ich "
            u"danych, zawsze pamiętaj o wylogowaniu się i zablokowaniu komputera, jeśli odchodzisz od niego na chwilę."
            u"\n"
            u"\n"
            u"Pamiętaj także, że jeśli korzystasz ze swojego konta Google na wielu urządzeniach, sam serwis Google "
            u"tworzy synchronizowaną historię aktywności. Jak ją usunąć, dowiesz się tu:\n"
            u"https://support.google.com/websearch/answer/54068?hl=pl&ref_topic=1638123.\n"
            u"\n"
            u"Więcej o ochronie prywatności w Internecie dowiesz się tu:\n"
            u"http://www.saferinternet.pl/pl/ochrona-prywatnosci."),
        (
            u"Wolność słowa oznacza przede wszystkim nasze prawo do wyrażania swoich własnych poglądów i w przypadku "
            u"skorzystania z tej wolności nie ma większego znaczenia czy swoje poglądy wyrażamy anonimowo, "
            u"czy też podpisujemy się pod nimi imieniem i nazwiskiem. Wolność słowa nie ma związku z wartością "
            u"komentarzy w Internecie. Z drugiej strony jednak należy pamiętać, że korzystanie z wolności słowa "
            u"nie oznacza, że nie możemy czuć się odpowiedzialni za swoje opinie wyrażane w Internecie i publikować "
            u"na przykład obraźliwe komentarze. Poza tym pełna anonimowość w sieci nie istnieje – jeśli zrobimy coś "
            u"złego w Internecie, to łatwo będzie można nas namierzyć.\n"
            u"\n"
            u"Z tematem problematyki wolności w Internecie można zapoznać się w artykule "
            u"pt. „Problem wolności w Internecie”: "
            u"http://www.ujk.edu.pl/infotezy/ojs/index.php/infotezy/about/submissions#authorGuidelines.",

            u"To, czy wartość komentarza opublikowanego w Internecie zależy od jego podpisania przez autora, wynika "
            u"z kontekstu, treści i często miejsca, w którym się ten komentarz znajduje. Wartość komentarza możemy "
            u"na przykład łatwo ocenić wtedy, kiedy jesteśmy w stanie zidentyfikować osobę, która go umieszcza w "
            u"Internecie. Ma to szczególne znaczenie, jeśli dana osoba jest uznanym ekspertem w dziedzinie, w której "
            u"się wypowiada. Bywają jednak sytuacje, w których anonimowe komentarze bywają również wartościowe. "
            u"Można to zaobserwować w sytuacjach, w których anonimowy komentarz dostarcza nam informacji, które "
            u"nie mogłyby zostać rozpowszechnione w inny sposób, jak tylko właśnie anonimowo – na przykład "
            u"udostępnienie informacji w Internecie o trudnych warunkach pracy w pewnej firmie pod imieniem "
            u"i nazwiskiem mogłoby zaszkodzić autorowi, który prawdopodobnie straciłby pracę. Pamiętajmy jednak "
            u"o tym, aby każdy komentarz w Internecie weryfikować we własnym zakresie i że nigdy nie istnieje pełna "
            u"anonimowość w sieci.\n"
            u"\n"
            u"Z tematem problematyki wolności w Internecie można zapoznać się w artykule "
            u"pt. „Problem wolności w Internecie”: "
            u"http://www.ujk.edu.pl/infotezy/ojs/index.php/infotezy/about/submissions#authorGuidelines.",

            u"Odpowiedzialność prawna to konsekwencje, jakie możemy ponieść w wyniku złamania prawa. Z punktu widzenia "
            u"odpowiedzialności prawnej nie ma znaczenia czy komentarz w Internecie jest anonimowy, czy też podpisany "
            u"imieniem i nazwiskiem. Na przykład za pomówienie kogoś w Internecie kodeks karny przewiduje różnego "
            u"rodzaju kary, w tym więzienie. Jeśli osoba pomawiająca dokonała tego czynu używając anonimowych danych, "
            u"to i tak na wniosek prokuratury prowadzącej śledztwo administrator strony, na której doszło do "
            u"pomówienia ma obowiązek udostępnić adres IP użytkownika (numer służący identyfikacji komputerów i innych "
            u"urządzeń w sieci). A stąd już prosta droga do uzyskania dokładnych danych adresowych osoby pomawiającej."
            u"\n"
            u"\n"
            u"Na temat odpowiedzialności prawnej za komentarze umieszczane w Internecie można przeczytać w artykule "
            u"pt. „Ten komentarz mnie obraża. Co mam zrobić?” "
            u"https://panoptykon.org/wiadomosc/ten-komentarz-mnie-obraza-co-mam-zrobic."),
        (
            u"Oryginalny pomysł i scenariusz – oparte na własnych odczuciach, czyli „twórcze, a nie odtwórcze” to "
            u"najważniejszy etap opowiadania historii. Im więcej własnych idei i koncepcji włożycie w opowiadaną "
            u"historię, tym będzie Wam bliższa, i tym lepiej będzie przemawiała do jej odbiorców. I, co także bardzo "
            u"ważne, historia, którą wymyślicie sami, na pewno nie będzie naruszać niczyich praw autorskich…\n"
            u"\n"
            u"Ważne są także kolejne kroki, które podejmiecie. Po wyborze tematu musicie podzielić się zadaniami, "
            u"aby każdy element zadania był wykonany. Jeśli tego nie zrobicie, w grupie szybko zapanuje chaos – "
            u"jednymi sprawami zajmie się kilka osób, a innymi – nikt. Warto też opracować harmonogram, aby ze "
            u"wszystkim zdążyć na czas. Podczas realizacji zadania bądźcie w stałym kontakcie, żeby na bieżąco "
            u"wymieniać się uwagami na temat wspólnej pracy.\n"
            u"\n"
            u"Więcej o tym, jak zorganizować wspólną pracę, znaleźć można tutaj: "
            u"https://edukacjamedialna.edu.pl/lekcje/sieciowa-wspolpraca/ i tutaj: "
            u"https://edukacjamedialna.edu.pl/lekcje/dokumentacja-i-narracje-cyfrowe/.",

            u"Jeśli nie zaczniecie pracy od zastanowienia się nad tym, jaką historię chcecie opowiedzieć, nie dacie "
            u"sobie szansy, aby opowiadała ona o rzeczach ważnych dla Was. Stworzycie – zamiast własnej historii – "
            u"zbitek cudzych opowieści. Oryginalny pomysł i scenariusz – oparte na własnych odczuciach, czyli "
            u"„twórcze, a nie odtwórcze” to najważniejszy etap opowiadania historii. Im więcej własnych idei "
            u"i koncepcji włożycie w opowiadaną historię, tym będzie Wam bliższa, i tym lepiej będzie przemawiała "
            u"do jej odbiorców. I, co także bardzo ważne, historia, którą wymyślicie sami, na pewno nie będzie "
            u"naruszać niczyich praw autorskich…\n"
            u"\n"
            u"Ważne są także kolejne kroki, które podejmiecie. Po wyborze tematu musicie podzielić się zadaniami, "
            u"aby każdy element zadania był wykonany. Jeśli tego nie zrobicie, w grupie szybko zapanuje chaos – "
            u"jednymi sprawami zajmie się kilka osób, a innymi – nikt. Warto też opracować harmonogram, aby ze "
            u"wszystkim zdążyć na czas. Podczas realizacji zadania bądźcie w stałym kontakcie, aby na bieżąco "
            u"wymieniać się uwagami na temat wspólnej pracy.\n"
            u"\n"
            u"Więcej o tym, jak zorganizować wspólną pracę, znaleźć można tutaj: "
            u"https://edukacjamedialna.edu.pl/lekcje/sieciowa-wspolpraca/ i tutaj: "
            u"https://edukacjamedialna.edu.pl/lekcje/dokumentacja-i-narracje-cyfrowe/.",

            u"Temat opowieści, który wybieracie razem, jest jednocześnie jej początkiem. Jeśli zrodzi się w dyskusji "
            u"między Wami, to dacie sobie możliwość opowiedzenia własnej historii. Jeśli jednak na tym "
            u"poprzestaniecie, wykorzystując cudze filmiki i zdjęcia, nie będzie ona wyłącznie Wasza, bowiem będziecie "
            u"opowiadać cudzymi słowami i obrazami. Oryginalny pomysł i scenariusz – oparte na własnych pomysłach, "
            u"czyli „twórcze, a nie odtwórcze” to najważniejszy etap opowiadania historii. Im więcej własnych idei "
            u"i koncepcji włożycie w opowiadaną historię, tym będzie Wam bliższa, i tym lepiej będzie przemawiała "
            u"do jej odbiorców. I, co także bardzo ważne, historia, którą wymyślicie sami, na pewno nie będzie "
            u"naruszać niczyich praw autorskich…\n"
            u"\n"
            u"Ważne są także kolejne kroki, które podejmiecie. Po wyborze tematu musicie podzielić się zadaniami, "
            u"aby każdy element zadania był wykonany. Jeśli tego nie zrobicie, w grupie szybko zapanuje chaos – "
            u"jednymi sprawami zajmie się kilka osób, a innymi – nikt. Warto też opracować harmonogram, aby ze "
            u"wszystkim zdążyć na czas. Podczas realizacji zadania bądźcie w stałym kontakcie, aby na bieżąco "
            u"wymieniać się uwagami na temat wspólnej pracy.\n"
            u"\n"
            u"Więcej o tym, jak zorganizować wspólną pracę, znaleźć można tutaj: "
            u"https://edukacjamedialna.edu.pl/lekcje/sieciowa-wspolpraca/ i tutaj: "
            u"https://edukacjamedialna.edu.pl/lekcje/dokumentacja-i-narracje-cyfrowe/."),
        (
            u"Korzystając z Internetu i komunikując się z innymi użytkownikami możemy odnieść wrażenie, że użytkownicy "
            u"zwracają się do siebie w bardzo bezpośredni sposób. Nie można jednak nikogo zmuszać do zaakceptowania "
            u"powszechnych reguł komunikacji w Internecie, jeśli w rzeczywistości na co dzień dana osoba nie stosuje "
            u"nieformalnej komunikacji w kontaktach z nieznajomymi, w tym również przedstawicielami różnych firm "
            u"i organizacji. Trudno nam sobie w rzeczywistości niewirtualnej wyobrazić pracownika jakiejś firmy, "
            u"który po imieniu odpowiada nam na zadane przez nas pytania. Najlepszą reakcja firmy na zaistniały "
            u"problem jest więc przeproszenie użytkownika za bezpośredni i nieformalny zwrot po imieniu.\n"
            u"\n"
            u"Prof. Jerzy Bralczyk o netykiecie: https://www.youtube.com/watch?v=thwUHPXbBoo.\n"
            u"\n"
            u"O zwracaniu się w Internecie do innych użytkowników per „pani” / „pan” można posłuchać na kanale "
            u"„Czas Gentelmanów”: https://www.youtube.com/watch?v=A8qznS7LjQY.",

            u"Korzystając z Internetu i komunikując się z innymi użytkownikami możemy odnieść wrażenie, że użytkownicy "
            u"zwracają się do siebie w bardzo bezpośredni sposób. Nie można jednak nikogo zmuszać do zaakceptowania "
            u"powszechnych reguł komunikacji w Internecie, zwłaszcza, jeśli w rzeczywistości na co dzień dana osoba "
            u"nie stosuje nieformalnej komunikacji w kontaktach z nieznajomymi, w tym również przedstawicielami "
            u"różnych firm i organizacji. Trudno nam w rzeczywistości niewirtualnej wyobrazić sobie pracownika "
            u"jakiejś firmy, który po imieniu odpowiada nam na zadane przez nas pytania. Najlepszą reakcją firmy "
            u"na zaistniały problem jest więc przeproszenie użytkownika za bezpośredni formalny zwrot po imieniu. "
            u"Pod żadnym pozorem nie powinna ignorować użytkownika odwołując się do zasady netykiety, czyli zbioru "
            u"zasad porozumiewania się w Internecie. Chociaż zgodnie z jej zasadami, przyjęte jest zwracanie się "
            u"do siebie po imieniu, to nie możemy innym narzucać własnych reguł komunikacji. Dotyczy to przede "
            u"wszystkim firm, które komunikują się w Internecie ze swoimi klientami.\n"
            u"\n"
            u"Prof. Jerzy Bralczyk o netykiecie: https://www.youtube.com/watch?v=thwUHPXbBoo.\n"
            u"\n"
            u"O zwracaniu się w Internecie do innych użytkowników per „pani” / „pan” można posłuchać na kanale "
            u"„Czas Gentelmanów”: https://www.youtube.com/watch?v=A8qznS7LjQY.",

            u"Korzystając z Internetu i komunikując się z innymi użytkownikami możemy odnieść wrażenie, że użytkownicy "
            u"zwracają się do siebie w bardzo bezpośredni sposób. Nie można jednak nikogo zmuszać do zaakceptowania "
            u"powszechnych reguł komunikacji w Internecie, jeśli w rzeczywistości na co dzień dana osoba stosuje "
            u"formalna komunikację w kontaktach z osobami nieznajomymi, w tym również przedstawicielami różnych firm "
            u"i organizacji. Trudno nam sobie w rzeczywistości niewirtualnej wyobrazić pracownika jakiejś firmy, "
            u"który po imieniu odpowiada nam na zadane przez nas pytania. Poprawną reakcją firmy na zaistniały problem "
            u"w komunikacji internetowej jest działanie zgodne z wypracowanymi wewnętrznie zasadami komunikacji. "
            u"Stanowią one coś na wzór kodeksu opracowanego przez daną firmę, który mówi pracownikom firmy, "
            u"jak należy zachowywać się w kontaktach z klientami. Niezależnie od zasad obowiązujących w firmie, "
            u"najlepszym rozwiązaniem będzie przeproszenie urażonego użytkownika.\n"
            u"\n"
            u"Prof. Jerzy Bralczyk o netykiecie: https://www.youtube.com/watch?v=thwUHPXbBoo.\n"
            u"\n"
            u"O zwracaniu się w Internecie do innych użytkowników per „pani” / „pan” można posłuchać na kanale "
            u"„Czas Gentelmanów”: https://www.youtube.com/watch?v=A8qznS7LjQY."),
        (
            u"Krytyczne podejście do informacji to jedna z najważniejszych umiejętności we współczesnym świecie, "
            u"w którym informacja otacza nas i dociera zewsząd. Przy tworzeniu aplikacji warto skontaktować się "
            u"z administracją, aby ustalić liczbę dostępnych miejsc. Pamiętaj jednak, że osoba udzielająca informacji "
            u"może nie mieć pełnej wiedzy – lub popełnić błąd. Dobrze byłoby zweryfikować otrzymane informacje "
            u"osobiście (aby Twoje dane pochodziły z więcej niż jednego źródła).\n"
            u"\n"
            u"Więcej o tym, dlaczego warto weryfikować informacje, dowiesz się tu:\n"
            u"https://www.youtube.com/watch?v=ZHHmEi9VAbY.\n"
            u"\n"
            u"Więcej o weryfikacji informacji w Internecie dowiesz się stąd:\n"
            u"http://www.heuristic.pl/blog/internet/Wiarygodnosc-informacji-zamieszczanych-w-Internecie;204.html.",

            u"Krytyczne podejście do informacji to jedna z najważniejszych umiejętności we współczesnym świecie, "
            u"w którym informacja otacza nas i dociera zewsząd. Ważne jest, aby uzyskana przez Ciebie informacja była "
            u"aktualna i najlepiej, aby pochodziła z więcej niż jednego źródła. Dlatego optymalnym rozwiązaniem byłoby "
            u"sprawdzenie danych ze strony (która mogła dawno nie być aktualizowana), na przykład poprzez kontakt "
            u"z administracją oraz osobiste udanie się na miejsce i sprawdzenie uzyskanych odpowiedzi.\n"
            u"\n"
            u"Więcej o tym, dlaczego warto weryfikować informacje dowiesz się tu:\n"
            u"https://www.youtube.com/watch?v=ZHHmEi9VAbY.\n"
            u"\n"
            u"Więcej o weryfikacji informacji w Internecie dowiesz się stąd:\n"
            u"http://www.heuristic.pl/blog/internet/Wiarygodnosc-informacji-zamieszczanych-w-Internecie;204.html.",

            u"Krytyczne podejście do informacji to jedna z najważniejszych umiejętności we współczesnym świecie, "
            u"w którym informacja otacza nas i dociera zewsząd. Ważne jest, aby uzyskana przez Ciebie informacja była "
            u"aktualna, wiarygodna i wyczerpująca. Dlatego optymalnym rozwiązaniem jest właśnie kontakt "
            u"z administracją oraz osobiste udanie się na miejsce i sprawdzenie uzyskanych odpowiedzi. Ważne jest "
            u"także sprawdzenie, jakie okoliczności mogą wpływać na stan „formalny” badanej rzeczywistości – "
            u"częstotliwość łamania przepisów przez pełnosprawnych kierowców stanowi taką incydentalną okoliczność, "
            u"której częste występowanie może całkowicie zniweczyć sens używania aplikacji, jeśli nie zostanie "
            u"uwzględnione w jej działaniu.\n"
            u"\n"
            u"Więcej o tym, dlaczego warto weryfikować informacje dowiesz się tu:\n"
            u"https://www.youtube.com/watch?v=ZHHmEi9VAbY.\n"
            u"\n"
            u"Więcej o weryfikacji informacji w Internecie dowiesz się tu:\n"
            u"http://www.heuristic.pl/blog/internet/Wiarygodnosc-informacji-zamieszczanych-w-Internecie;204.html."),
        (
            u"Niewidzialna praca to między innymi praca wykonywana na rzecz swojej rodziny / wolontariat. Chociaż "
            u"zazwyczaj kojarzona jest z pracą w domu (na przykład kobiety opiekujące się dziećmi), to odnosi się też "
            u"do „szarych pracowników” wielkich korporacji, którzy stoją za sukcesem tych przedsiębiorstw, w tym "
            u"moderatorów mediów społecznościowych, których rola jest niezastąpiona i niezbędna dla sprawnego "
            u"funkcjonowania biznesu.\n"
            u"„Niewidzialną pracą” można nazwać również aktywność użytkowników mediów społecznościowych, którzy "
            u"poprzez komentarze pod wpisami i newsami podtrzymują zainteresowanie innych użytkowników, a co za tym "
            u"idzie zwiększają zainteresowanie potencjalnych reklamodawców.\n"
            u"\n"
            u"O niewidzialnej pracy można przeczytać w artykule pt. „Niewidzialna praca o wielkiej mocy”: "
            u"http://www.praca.pl/poradniki/rynek-pracy/niewidzialna-praca-o-wielkiej-mocy_pr-1711.html.",

            u"Niewidzialna praca to między innymi praca wykonywana na rzecz swojej rodziny / wolontariat. Chociaż "
            u"zazwyczaj kojarzona jest z pracą w domu (na przykład kobiety opiekujące się dziećmi), to odnosi się też "
            u"do „szarych pracowników” wielkich korporacji, którzy stoją za sukcesem tych przedsiębiorstw, w tym "
            u"moderatorów mediów społecznościowych, których rola jest niezastąpiona i niezastąpiona i niezbędna dla "
            u"sprawnego funkcjonowania biznesu.\n"
            u"„Niewidzialną pracą” można nazwać również aktywność użytkowników mediów społecznościowych, którzy "
            u"poprzez komentarze pod wpisami i newsami oraz udostępnianie różnego rodzaju treści podtrzymują "
            u"zainteresowanie innych użytkowników, a co za tym idzie zwiększają zainteresowanie potencjalnych "
            u"reklamodawców.\n"
            u"\n"
            u"O niewidzialnej pracy można przeczytać w artykule pt. „Niewidzialna praca o wielkiej mocy”: "
            u"http://www.praca.pl/poradniki/rynek-pracy/niewidzialna-praca-o-wielkiej-mocy_pr-1711.html.",

            u"Niewidzialna praca to między innymi praca wykonywana na rzecz swojej rodziny / wolontariat. Chociaż "
            u"zazwyczaj kojarzona jest z pracą w domu (na przykład kobiety opiekujące się dziećmi), to odnosi się "
            u"też do „szarych pracowników” wielkich korporacji, którzy stoją za sukcesem tych przedsiębiorstw, "
            u"w tym moderatorów mediów społecznościowych, których rola jest niezastąpiona i niezbędna dla sprawnego "
            u"funkcjonowania biznesu.\n"
            u"„Niewidzialną pracą” można nazwać również aktywność użytkowników mediów społecznościowych, którzy "
            u"poprzez komentarze pod wpisami i newsami podtrzymują zainteresowanie innych użytkowników, a co za tym "
            u"idzie zwiększają zainteresowanie potencjalnych reklamodawców.\n"
            u"Z całą pewnością informatycy budujący rozwiązania IT dla firm nie są osobami wykonującymi „niewidzialną "
            u"pracę”, chociażby z tego względu, że swoją pracę wykonują najczęściej poza domem, jej efekty są "
            u"dostrzegane i doceniane oraz pobierają za nią wysokie wynagrodzenia (pracownicy IT są jedną z najlepiej "
            u"opłacanych grup zawodowych na całym świecie).\n"
            u"\n"
            u"O niewidzialnej pracy można przeczytać w artykule pt. „Niewidzialna praca o wielkiej mocy”: "
            u"http://www.praca.pl/poradniki/rynek-pracy/niewidzialna-praca-o-wielkiej-mocy_pr-1711.html."),
        (
            u"Informacja nazywana jest we współczesnym świecie „zasobem strategicznym”. Pozwala działać, planować, "
            u"podejmować decyzje w świadomy sposób – i z prawdopodobieństwem osiągnięcia dobrych skutków. Jednak, "
            u"aby informacja spełniała takie funkcje, musi być wiarygodna, aktualna, kompletna. Jej wiarygodność "
            u"należy zatem sprawdzać i weryfikować. Jeśli pojawia się w więcej niż jednym źródle, rośnie "
            u"prawdopodobieństwo, że nie jest manipulacją ani dezinformacją. Czasami zdarza się, że kolejne media "
            u"bezmyślnie powtarzają informację za tym, kto podał ją jako pierwszy, i trafia ona do wielu odbiorców, "
            u"ostatecznie okazuje się nieprawdziwa. Bez dotarcia do jej właściwego, oryginalnego źródła, trudno mieć "
            u"100-procentową pewność, że mamy do czynienia z wartościową informacją.",

            u"Informacja nazywana jest we współczesnym świecie „zasobem strategicznym”. Pozwala działać, planować, "
            u"podejmować decyzje w świadomy sposób – i z prawdopodobieństwem osiągnięcia dobrych skutków. Jednak, aby "
            u"informacja spełnia takie funkcje, musi być wiarygodna, aktualna, kompletna. Jej wiarygodność należy "
            u"zatem sprawdzać i weryfikować. Jeśli pojawia się w więcej niż jednym źródle, rośnie prawdopodobieństwo, "
            u"że nie jest manipulacją ani dezinformacją. Jeśli dodatkowo informacja potwierdzona jest możliwością "
            u"dotarcia do oryginalnego jej źródła, zamiast opracowania lub interpretacji, można z wysokim "
            u"prawdopodobieństwem zakładać, że jest prawdziwa.",

            u"Informacja nazywana jest we współczesnym świecie „zasobem strategicznym”. Pozwala działać, planować, "
            u"podejmować decyzje w świadomy sposób – i z prawdopodobieństwem osiągnięcia dobrych skutków. Jednak, aby "
            u"informacja spełnia takie funkcje, musi być wiarygodna, aktualna, kompletna. Informacja pochodząca "
            u"jedynie z serwisów społecznościowych i nielicznych portali informacyjnych, a także nie można ustalić jej "
            u"oryginalnego źródła, nie wolno zakładać, że jest prawdziwa. Możemy pozwolić wprowadzić się w błąd – "
            u"a nasi znajomi, na których profilach społecznościowych będziemy się opierać, mogą nawet nie mieć "
            u"świadomości, że rozprzestrzeniają nieprawdziwe informacje.\n"
            u"\n"
            u"O potencjalnych konsekwencjach fałszywych informacji w prawdziwym świecie przeczytasz tu:\n"
            u"https://www.wprost.pl/swiat/10030588/"
            u"Facebook-wplynal-na-wynik-amerykanskich-wyborow-Zuckerberg-komentuje.html."),
        (
            u"Samo podjęcie czynności kontrolnych przez prokuraturę nie musi oznaczać, że umowy podpisywane "
            u"z wykonawcami budżetu obywatelskiego odbyły się z naruszeniem prawa. Każdy z nas może paść ofiarą "
            u"niesłusznych oskarżeń, dlatego powinno unikać się ocen dotyczących ewentualnej winy. Dopóki zarzuty "
            u"postawione przez prokuraturę (jeśli w ogóle zostaną postawione) nie zostaną uprawomocnione wyrokiem "
            u"sądowym, obowiązuje tzw. domniemanie niewinności. Tytuł zastosowanego newsa jest akceptowalny, ponieważ "
            u"nie rozstrzyga ewentualnej winy wykonawców budżetu obywatelskiego. Niestety, z drugiej strony "
            u"sformułowanie „niejasne umowy” sugeruje pewnego rodzaju nieprawidłowości. Dziennikarze tworzący newsy "
            u"powinni działać zgodnie z etyką zawodową. Są oni zobowiązani do rzetelnego informowania o faktach "
            u"i unikaniu prasowych przekłamań, nie tylko w treści newsów, ale również w ich tytułach. Bywa jednak tak, "
            u"że dziennikarze tworzący tytuły wiadomości manipulują nami, aby podstępnie zmusić nas do zaznajomienia "
            u"się z ich treścią. Robią to najczęściej w celu wygenerowania dodatkowych zysków z reklam, które "
            u"pojawiają się obok treści wiadomości. To zjawisko nosi nazwę „clickbait”.\n"
            u"\n"
            u"Jeśli chcesz dowiedzieć się czym jest dokładnie „clickbait” posłuchaj audycji pt. „Clickbait w sieci, "
            u"czyli kto chce cię oszukać”: "
            u"http://www.polskieradio.pl/9/3850/Artykul/1665036,Clickbait-w-sieci-czyli-kto-chce-cie-oszukac.\n"
            u"\n"
            u"W celu zapoznania się ze standardami pracy dziennikarskiej warto przeczytać:\n"
            u"Kartę Etyczną Mediów: http://www.dziennikarzerp.pl/wp-content/uploads/2010/06/karta_dziennikarzy.pdf.\n"
            u"Kodeks etyki dziennikarskiej Stowarzyszenia Dziennikarzy Polskich: "
            u"http://sdp.pl/s/kodeks-etyki-dziennikarskiej-sdp.\n"
            u"Dziennikarski kodeks obyczajowy Stowarzyszenia Dziennikarzy RP: "
            u"http://www.dziennikarzerp.pl/wp-content/uploads/2010/06/kodeks.pdf.",

            u"Zastosowanie takiego tytułu jest najlepsze, ponieważ stwierdza tylko pewien fakt, a jednocześnie "
            u"nie przesądza o rezultatach działań kontrolnych prokuratury. Samo podjęcie czynności kontrolnych "
            u"przez prokuraturę nie musi oznaczać, że umowy podpisywane z wykonawcami budżetu obywatelskiego odbyły "
            u"się z naruszeniem prawa. Każdy z nas może paść ofiarą niesłusznych oskarżeń, dlatego powinno unikać się "
            u"skrajnych ocen dotyczących ewentualnej winy. Dopóki zarzuty postawione przez prokuraturę (jeśli w ogóle "
            u"zostaną postawione) nie zostaną uprawomocnione wyrokiem sądowym obowiązuje tzw. domniemanie niewinności. "
            u"Tytuł zastosowanego newsa jest poprawny i zgodny z etyką zawodową dziennikarza. Pamiętajmy, "
            u"że dziennikarze zobowiązani są do rzetelnego informowania o faktach i unikaniu prasowych przekłamań, "
            u"nie tylko w treści newsów, ale również w ich tytułach.\n"
            u"\n"
            u"W celu zapoznania się ze standardami pracy dziennikarskiej warto przeczytać:\n"
            u"Kartę Etyczną Mediów: http://www.dziennikarzerp.pl/wp-content/uploads/2010/06/karta_dziennikarzy.pdf.\n"
            u"Kodeks etyki dziennikarskiej Stowarzyszenia Dziennikarzy Polskich: "
            u"http://sdp.pl/s/kodeks-etyki-dziennikarskiej-sdp.\n"
            u"Dziennikarski kodeks obyczajowy Stowarzyszenia Dziennikarzy RP: "
            u"http://www.dziennikarzerp.pl/wp-content/uploads/2010/06/kodeks.pdf.",

            u"Zastosowanie takiego tytułu wprowadza tylko niepotrzebny zamęt i nosi znamiona manipulacji skierowanej "
            u"wobec czytelników. Taki tytuł może być krzywdzący dla wykonawców, ponieważ wprost sugeruje ich winę. "
            u"Samo podjęcie czynności kontrolnych przez prokuraturę nie musi oznaczać, że umowy podpisywane "
            u"z wykonawcami budżetu obywatelskiego odbyły się z naruszeniem prawa. Każdy z nas może paść ofiarą "
            u"niesłusznych oskarżeń, dlatego powinno unikać się skrajnych ocen dotyczących ewentualnej winy. "
            u"Dopóki zarzuty postawione przez prokuraturę (jeśli w ogóle zostaną postawione) nie zostaną "
            u"uprawomocnione wyrokiem sądowym obowiązuje tzw. domniemanie niewinności. Tytuł zastosowanego newsa jest "
            u"nieakceptowalny, ponieważ zakłada winę, której nie udowodniono. Dziennikarze tworzący newsy powinni "
            u"działać zgodnie z etyką zawodową. Są oni zobowiązani do rzetelnego informowania o faktach i unikaniu "
            u"prasowych przekłamań, nie tylko w treści newsów, ale również w ich tytułach. Bywa jednak tak, że "
            u"dziennikarze tworzący tytuły wiadomości manipulują nami, aby podstępnie zmusić nas do zaznajomienia się "
            u"z ich treścią. Robią to najczęściej w celu wygenerowania dodatkowych zysków z reklam, które pojawiają "
            u"się obok treści wiadomości. To zjawisko nosi nazwę „clickbait”.\n"
            u"\n"
            u"Jeśli chcesz dowiedzieć się czym jest dokładnie „clickbait” posłuchaj audycji pt. „Clickbait w sieci, "
            u"czyli kto chce cię oszukać”: "
            u"http://www.polskieradio.pl/9/3850/Artykul/1665036,Clickbait-w-sieci-czyli-kto-chce-cie-oszukac.\n"
            u"\n"
            u"W celu zapoznania się ze standardami pracy dziennikarskiej warto przeczytać:\n"
            u"Kartę Etyczną Mediów: http://www.dziennikarzerp.pl/wp-content/uploads/2010/06/karta_dziennikarzy.pdf.\n"
            u"Kodeks etyki dziennikarskiej Stowarzyszenia Dziennikarzy Polskich: "
            u"http://sdp.pl/s/kodeks-etyki-dziennikarskiej-sdp.\n"
            u"Dziennikarski kodeks obyczajowy Stowarzyszenia Dziennikarzy RP: "
            u"http://www.dziennikarzerp.pl/wp-content/uploads/2010/06/kodeks.pdf."),
        (
            u"Wymienione w odpowiedzi narzędzia służą raczej dystrybucji informacji i prezentowaniu własnych wniosków "
            u"/ przemyśleń (Power Point lub podcast), a nie pracy w grupie. Stosowane przy realizacji projektu "
            u"narzędzia muszą pozwalać na komunikację zwrotną, wymianę myśli i ustalenia – a także wprowadzanie "
            u"zmian w tworzonych treściach (muszą zatem pozwalać na tworzenie treści w formie wspólnie realizowanego "
            u"procesu, a nie prezentować je statycznie).\n"
            u"\n"
            u"Informacje o komunikacji w projektach znajdziesz tu:\n"
            u"http://www.ptzp.org.pl/files/konferencje/kzz/artyk_pdf_2017/T1/t1_200.pdf.",

            u"Wymienione w odpowiedzi narzędzia służą wspólnej pracy nad projektem, mogą jednak nie pozwalać "
            u"na przykład na pełne śledzenie chronologii wypowiedzi i ustaleń (Coggle) lub też odnotowanie efektów "
            u"i ustaleń (Skype). Stosowane przy realizacji Waszego projektu narzędzia muszą pozwalać na komunikację "
            u"zwrotną, wymianę myśli i ustalenia – a także wprowadzanie zmian w tworzonych treściach (muszą zatem "
            u"pozwalać na tworzenie treści w formie wspólnie realizowanego procesu, a nie prezentować je statycznie) "
            u"i umożliwiać śledzenie historii dokonywanych ustaleń i wprowadzanych zmian.\n"
            u"\n"
            u"Informacje o komunikacji w projektach znajdziesz tu:\n"
            u"http://www.ptzp.org.pl/files/konferencje/kzz/artyk_pdf_2017/T1/t1_200.pdf.",

            u"Wybrane narzędzia powinny doskonale odpowiedzieć na potrzeby współpracy przy realizacji projektu. "
            u"Pozwalają zarówno na zarządzanie wewnątrz projektu (Wunderlist), jak i wspólne tworzenie koncepcji "
            u"opracowywanego dzieła (OneNote, Google Docs). Szybka, grupowa komunikacja, uwzględniająca wszystkich "
            u"uczestników projektu, zachowująca historię konwersacji, pozwala nie tylko na dokonywanie ustaleń, "
            u"ale i odnoszenie się do nich w przyszłości.\n"
            u"\n"
            u"Informacje o komunikacji w projektach znajdziesz tu:\n"
            u"http://www.ptzp.org.pl/files/konferencje/kzz/artyk_pdf_2017/T1/t1_200.pdf."),
        (
            u"Liczba edycji hasła na Wikipedii nie jest wskaźnikiem jego jakości. Przy niektórych hasłach, szczególnie "
            u"społecznie drażliwych i kontrowersyjnych, liczba edycji może wynikać z braku zgody społeczności "
            u"wikipedystów co do jednej neutralnej definicji. Przyczyną dużej liczby edycji bywa również zamierzone "
            u"i złośliwe działanie internautów, którzy stosując tzw. trolling zmieniają znaczenie danego hasła, "
            u"obniżając jego wartość merytoryczną lub przedstawiając skrajny punkt widzenia. Liczba edycji może "
            u"wynikać też ze zmieniającej się stale wiedzy na temat danego zjawiska.\n"
            u"\n"
            u"Na temat oceny jakości haseł tworzonych na Wikipedii można przeczytać tutaj: "
            u"https://pl.wikipedia.org/wiki/Wikipedia:Ocena_jakości.",

            u"Długość hasła na Wikipedii może być dobry miernikiem jego jakości, ale też niewystarczającym. "
            u"Podobnie z jego strukturą. Nawet jeśli hasło zawiera odpowiedni wstęp definicyjny oraz dalsze "
            u"skonkretyzowanie omawianej problematyki, nie oznacza to automatycznie, że mamy do czynienia z hasłem "
            u"wysokiej jakości. Długość i odpowiednia struktura nie będą niosły ze sobą wartości, jeśli hasło "
            u"nie będzie zawierało odpowiednich przypisów i odnośników do innych rzetelnych źródeł, w których "
            u"potwierdzone są tezy i informacje zawarte w opisie hasła. Po zapoznaniu się z interesującym hasłem "
            u"warto zawsze sprawdzić źródła, do których się ono odnosi. Sama obecność odnośników nie oznacza, że są "
            u"one aktualne i rzetelne.\n"
            u"\n"
            u"Na temat oceny jakości haseł tworzonych na Wikipedii można przeczytać tutaj: "
            u"https://pl.wikipedia.org/wiki/Wikipedia:Ocena_jakości.",

            u"Ani liczba edycji hasła, ani jego długość i struktura nie ma znaczenia dla jego jakości, jeśli w opisie "
            u"hasła nie znajdziemy odpowiednich przypisów. To źródła, do których odnosi się opis hasła, stanowią "
            u"przede wszystkim o jego wartości merytorycznej. Należy jednak pamiętać, że sama obecność odnośników "
            u"jeszcze nic nie znaczy, warto samemu sprawdzić, czy są one aktualne i odnoszą do rzetelnej wiedzy.\n"
            u"Na temat oceny jakości haseł tworzonych na Wikipedii można przeczytać tutaj: "
            u"https://pl.wikipedia.org/wiki/Wikipedia:Ocena_jakości."),
        (
            u"Ochrona praw autorskich oraz przestrzeganie przepisów i norm związanych z tymi prawami jest szczególnie "
            u"istotna w cyfrowym świecie, w którym skopiowanie cudzego pomysłu wymaga często jedynie zastosowanie "
            u"funkcji „Kopiuj – Wklej”. Wykorzystanie podpisanej grafiki z podaniem jedynie adresu strony nie "
            u"gwarantuje ochrony praw jej autora – grafika mogła znaleźć się na stronie w sposób niezgodny z prawem, "
            u"z naruszeniem praw jej autora, poza tym autor interesującej nas grafiki ma prawo do bycia docenionym "
            u"poprzez podanie imienia i nazwiska lub pseudonimu. Dlatego, jeśli masz wątpliwości, zrób co możesz, "
            u"aby ustalić jej pierwotne źródło i autora i sprawdzić, czy pozwolił on na jej wykorzystywanie przez inne "
            u"osoby.\n"
            u"\n"
            u"O tym, że nawet wielkie firmy popełniają plagiaty przeczytasz tu:\n"
            u"http://noizz.pl/lifestyle/"
            u"zara-kopiuje-grafiki-artystki-my-jestesmy-znani-a-ty-nie-odpowiadaja-prawnicy-firmy/p9y17wp.\n"
            u"\n"
            u"O ochronie praw autorskich więcej dowiesz się tu: http://prawokultury.pl.",

            u"Ochrona praw autorskich oraz przestrzeganie przepisów i norm związanych z tymi prawami jest szczególnie "
            u"istotna w cyfrowym świecie, w którym skopiowanie cudzego pomysłu wymaga często jedynie zastosowanie "
            u"funkcji „Kopiuj – Wklej”. Wykorzystanie podpisanej grafiki z podaniem jedynie adresu strony "
            u"nie gwarantuje ochrony praw jej autora – grafika mogła znaleźć się na stronie w sposób niezgodny "
            u"z prawem, z naruszeniem praw jej autora. Z takiego jednego naruszenia mogą rodzić się kolejne – "
            u"grafika może być zamieszczana przez administratorów kolejnych stron. Dlatego, jeśli masz wątpliwości, "
            u"zrób co możesz, aby ustalić jej pierwotne źródło i autora i sprawdzić, czy pozwolił on na jej "
            u"wykorzystywanie przez inne osoby.\n"
            u"\n"
            u"O ochronie praw autorskich więcej dowiesz się tu: http://prawokultury.pl.",

            u"Ochrona praw autorskich oraz przestrzeganie przepisów i norm związanych z tymi prawami jest szczególnie "
            u"istotna w cyfrowym świecie, w którym skopiowanie cudzego pomysłu wymaga często jedynie zastosowanie "
            u"funkcji „Kopiuj – Wklej”. Wykorzystanie podpisanej grafiki z podaniem jedynie adresu strony "
            u"nie gwarantuje ochrony praw jej autora – grafika mogła znaleźć się na stronie w sposób niezgodny "
            u"z prawem, z naruszeniem praw jej autora. Zrobienie wszystkiego, co możliwe, aby ustalić jej pierwotne "
            u"źródło i autora i sprawdzić, czy pozwolił on na jej wykorzystywanie przez inne osoby, sprawia, "
            u"że zachowujemy się nie tylko fair w stosunku do autora, ale także przestrzegamy obowiązujących w tym "
            u"zakresie przepisów.\n"
            u"\n"
            u"O ochronie praw autorskich więcej dowiesz się tu: http://prawokultury.pl."),
        (
            u"Przedstawiona w kodzie funkcja zawiera niepełną listę argumentów. Zadaniem funkcji f(a) jest "
            u"wyświetlenie sumy argumentu „a” oraz argumentu „b”. Niestety, sama funkcja pozwala określić wyłącznie "
            u"argument „a” – z tego względu jej zapis jest niezgodny z zadaniem, które ma zrealizować. Główną wadą "
            u"tego kodu jest więc przetwarzanie brakującego argumentu „b”.",

            u"Przedstawiona w kodzie funkcja zawiera niepełną listę argumentów. Zadaniem funkcji f(a) jest "
            u"wyświetlenie sumy argumentu „a” oraz argumentu „b”. Niestety, sama funkcja pozwala określić wyłącznie "
            u"argument „a” – z tego względu jej zapis jest niezgodny z zadaniem, które ma zrealizować. Odpowiedź ta "
            u"jest niepoprawna, ponieważ funkcja nie określa, czy argument zarówno „a” jak i „b” muszą mieć charakter "
            u"liczbowy. Mogą mieć również charakter łańcuchowy (tj. tekstowy).",

            u"Jest to błędna odpowiedź, ponieważ litera „f” w podanym kodzie nie oznacza argumentów funkcji. Argument "
            u"funkcji oznaczony jest literą „a” i znajduje się w nawiasie. Litera „f” oznacza funkcje, która w tym "
            u"przypadku przetwarza argument „a”. Ponadto przedstawiona w kodzie funkcja zawiera niepełną listę "
            u"argumentów. Zadaniem przedstawione funkcji f(a) jest wyświetlenie sumy argumentu „a” oraz argumentu „b”. "
            u"Niestety, sama funkcja pozwala określić wyłącznie argument „a” – z tego względu jej zapis jest niezgodny "
            u"z zadaniem, które ma zrealizować.\n"
            u"\n"
            u"O definicji funkcji na przykładzie języka programowania C można przeczytać tutaj: "
            u"https://pl.wikibooks.org/wiki/C/Funkcje#cite_note-1."),
        (
            u"Licencje Creative Commons pozwalają zastąpić tradycyjny model ochrony praw autorskich „Wszystkie prawa "
            u"zastrzeżone” zasadą „Pewne prawa zastrzeżone” – przy jednoczesnym poszanowaniu zasad prawa autorskiego "
            u"(http://creativecommons.pl/poznaj-licencje-creative-commons/). Licencja CC-BY-SA pozwala na kopiowanie, "
            u"zmienianie, rozprowadzanie, przedstawianie i wykonywanie utworu oraz utworów zależnych, które muszą być "
            u"opublikowane na tej samej licencji. Musisz jednak zwrócić uwagę na to, jaka licencja obowiązuje "
            u"dla materiałów ściągniętych z serwisu The Noun Project, aby nie naruszyć praw ich autorów.",

            u"Licencje Creative Commons pozwalają zastąpić tradycyjny model ochrony praw autorskich „Wszystkie prawa "
            u"zastrzeżone” zasadą „Pewne prawa zastrzeżone” – przy jednoczesnym poszanowaniu zasad prawa autorskiego "
            u"(http://creativecommons.pl/poznaj-licencje-creative-commons/). Licencja CC-BY pozwala na kopiowanie, "
            u"zmienianie, rozprowadzanie, przedstawianie i wykonywanie utworu jedynie pod warunkiem oznaczenia "
            u"autorstwa i gwarantuje najszersze swobody licencjobiorcy. Materiały z serwisu NASA należą natomiast – "
            u"jak wszystkie dzieła stworzone przez rząd federalny USA – do domeny publicznej, która daje wszystkim "
            u"nieograniczone prawo do dzieł, których wykorzystanie nie podlega restrykcjom i ograniczeniom, ponieważ "
            u"prawa majątkowe do twórczości wygasły lub twórczość ta nigdy nie była lub nie jest przedmiotem prawa "
            u"autorskiego (http://domenapubliczna.org/co-to-jest-domena-publiczna/).",

            u"Wykorzystanie materiałów ściągniętych z wyszukiwarki grafiki Google, bez sprawdzenia ich pochodzenia, "
            u"udzielonej przez twórcę licencji oraz bez znajomości praw, jakie przysługują przy ich użyciu, w znacznej "
            u"większości mogą narazić Cię na zarzut nieuprawnionego wykorzystania cudzej twórczości, a zatem "
            u"naruszenia praw autorskich. Wyszukiwarka Google umożliwia filtrowanie wyników m.in. na podstawie "
            u"licencji, na jakiej zostały udostępnione materiały. Opcję tę znajdziesz w zakładce Narzędzia – Prawa do "
            u"użytkowania."),
        (
            u"Podczas wyszukiwaniu w Internecie obiektów takich jak zdjęcia lub grafiki istotna jest nie tyle liczba "
            u"słów kluczowych, co ich trafność. Wybrane przez Ciebie słowa kluczowe zawierają odniesienie do "
            u"wydarzenia historycznego, miejsca, formy przekazu – są więc one wyczerpujące i pozwolą otrzymać "
            u"najlepsze rezultaty odnoszące się do poszukiwanego przez nas obiektu.",

            u"Podczas wyszukiwaniu w Internecie obiektów takich jak zdjęcia lub grafiki istotna jest nie tyle liczba "
            u"słów kluczowych, co ich trafność. Wybrane przez Ciebie słowa kluczowe zawierają odniesienia wyłącznie "
            u"do miejsca związanego z wydarzeniem oraz jego zawartości wizualnej – są więc one niewyczerpujące i "
            u"nie pozwolą uzyskać najlepszych rezultatów odnoszących się do poszukiwanego przez nas obiektu. Brakuje "
            u"przede wszystkim odniesienia do samego wydarzenia, czyli angielskiej wojny domowej w latach 1642-1651.",

            u"Podczas wyszukiwaniu w Internecie obiektów takich jak zdjęcia lub grafiki istotna jest nie tyle liczba "
            u"słów kluczowych, co ich trafność. Wybrane przez Ciebie słowa kluczowe zawierają odniesienia do miejsca "
            u"związanego z wydarzeniem, okresu oraz jego formy – są one trafne, a co za tym idzie powinniśmy uzyskać "
            u"rezultat odnoszący się do poszukiwanego przez nas obiektu. Warto jednak poszerzyć zakres słów kluczowych "
            u"o dodatkowe informacje, na przykład użyć hasła „karykatura”. Dodatkowe słowa mogą zwiększyć skuteczność "
            u"naszych poszukiwań."),
        (
            u"Ochrona praw jednostki w Internecie dotyczy różnych aspektów naszego funkcjonowania w przestrzeni "
            u"cyfrowej. Jedną z nich jest ochrona naszych praw do stworzonego dzieła, a zatem naszych praw autorskich. "
            u"Nie można zatem wykorzystywać bez pozwolenia niczyich zdjęć do tworzenia własnej relacji z wydarzeń, "
            u"nawet organizowanych i przeżytych wspólnie.\n"
            u"\n"
            u"Co więcej, ludzie mają prawo do samodzielnego decydowania o tym, w jaki sposób ich wizerunek będzie "
            u"upubliczniony. Dlatego zanim zamieścisz zdjęcie innej osoby, nawet wspólne selfie, upewnij się, "
            u"że sfotografowana osoba wyraża zgodę na zamieszczenie zdjęcia w Internecie.\n"
            u"\n"
            u"Więcej o ochronie wizerunku dowiesz się tu:\n"
            u"https://portal.uw.edu.pl/web/ado/ochrona-wizerunku.",

            u"Ochrona praw jednostki w Internecie dotyczy różnych aspektów naszego funkcjonowania w przestrzeni "
            u"cyfrowej. Jedną z nich jest ochrona naszych praw do stworzonego dzieła, a zatem naszych praw autorskich. "
            u"Nie można zatem wykorzystywać bez pozwolenia niczyich zdjęć do tworzenia własnej relacji z wydarzeń, "
            u"nawet organizowanych i przeżytych wspólnie. Zanim wykorzystasz czyjeś zdjęcie – nawet takie, na którym "
            u"jesteś – zapytaj o zgodę jego autorkę / autora o możliwość jego wykorzystania.",

            u"Ochrona praw jednostki w Internecie dotyczy różnych aspektów naszego funkcjonowania w przestrzeni "
            u"cyfrowej. Jedną z nich jest ochrona naszych praw do stworzonego dzieła, a zatem naszych praw autorskich. "
            u"Nie można zatem wykorzystywać bez pozwolenia niczyich zdjęć do tworzenia własnej relacji z wydarzeń, "
            u"nawet organizowanych i przeżytych wspólnie. Jeśli jednak uzyskałeś zgodę autorki / autora na "
            u"publikowanie zdjęć, możesz to bez wahania zrobić. Co więcej, ludzie mają prawo do samodzielnego "
            u"decydowania o tym, w jaki sposób ich wizerunek będzie upubliczniony. Jeśli jednak przed publikacją "
            u"zdjęcia upewniłeś się, że sfotografowana osoba wyraża na zamieszczenie zdjęcia w Internecie zgodę, "
            u"również możesz bez wątpliwości zamieścić zdjęcie.\n"
            u"\n"
            u"Więcej o ochronie wizerunku dowiesz się tu:\n"
            u"https://portal.uw.edu.pl/web/ado/ochrona-wizerunku."),
        (
            u"Internet to niemal nieskończone źródło informacji, edukacji, rozrywki. Często trudno jest zapanować nad "
            u"otwieraniem kolejnych, coraz bardziej interesujących (jak się może zdawać), stron. Zachowanie dyscypliny "
            u"i świadomości własnych działań – oraz świadomości upływającego czasu – pozwala na zarządzanie własnym "
            u"czasem i efektywne wykorzystanie narzędzia, jakim jest światowa sieć. Warto pamiętać, że taka dyscyplina "
            u"bywa trudna, szczególnie jeśli bez żadnego zastanowienia będziesz pozwalać na to, aby kolejne bodźce "
            u"odrywały Cię od realizowania zaplanowanych działań.\n"
            u"\n"
            u"Więcej o zarządzaniu czasem dowiesz się tu:\n"
            u"http://michalpasterski.pl/2012/06/zarzadzanie-czasem-w-5-cwiczeniach/.\n"
            u"\n"
            u"Co nas denerwuje i rozprasza i jak sobie z tym radzić? Zajrzyj tu:\n"
            u"http://gazetapraca.pl/gazetapraca/1,95288,13425980,Co_nas_denerwuje__co_nas_rozprasza.html.\n"
            u"\n"
            u"Pomidor pomoże? Prosty sposób na zarządzanie czasem znajdziesz tu:\n"
            u"http://projektantczasu.pl/technika-pomodoro-pommodoro-pomidora/.",

            u"Internet to niemal nieskończone źródło informacji, edukacji, rozrywki. Często trudno jest zapanować nad "
            u"otwieraniem kolejnych, coraz bardziej interesujących (jak się może zdawać), stron. Zachowanie dyscypliny "
            u"i świadomości własnych działań – oraz świadomości upływającego czasu – pozwala na zarządzanie własnym "
            u"czasem i efektywne wykorzystanie narzędzia, jakim jest światowa sieć. Jeśli nie narzucisz sam sobie "
            u"granic i nie będziesz świadomie panował nad podejmowanymi działaniami, Twój plan nigdy się nie ziści.\n"
            u"\n"
            u"Więcej o zarządzaniu czasem dowiesz się tu:\n"
            u"http://michalpasterski.pl/2012/06/zarzadzanie-czasem-w-5-cwiczeniach/.\n"
            u"\n"
            u"Co nas denerwuje i rozprasza i jak sobie z tym radzić? Zajrzyj tu:\n"
            u"http://gazetapraca.pl/gazetapraca/1,95288,13425980,Co_nas_denerwuje__co_nas_rozprasza.html.\n"
            u"\n"
            u"Pomidor pomoże? Prosty sposób na zarządzanie czasem znajdziesz tu:\n"
            u"http://projektantczasu.pl/technika-pomodoro-pommodoro-pomidora/.",

            u"Internet to niemal nieskończone źródło informacji, edukacji, rozrywki. Często trudno jest zapanować nad "
            u"otwieraniem kolejnych, coraz bardziej interesujących (jak się może zdawać), stron. Zachowanie dyscypliny "
            u"i świadomości własnych działań – oraz świadomości upływającego czasu – pozwala na zarządzanie własnym "
            u"czasem i efektywne wykorzystanie narzędzia, jakim jest światowa sieć. Wykorzystanie zewnętrznych "
            u"narzędzi, które pozwalają nam obiektywnie oceniać własne zachowania i dokonywać ich stosownej korekty – "
            u"jeśli to niezbędne – to sposób nie tylko na efektywne działanie, ale i na zwiększenie prawdopodobieństwa "
            u"osiągnięcia sukcesu w podejmowanych przedsięwzięciach.\n"
            u"\n"
            u"Więcej o zarządzaniu czasem dowiesz się tu:\n"
            u"http://michalpasterski.pl/2012/06/zarzadzanie-czasem-w-5-cwiczeniach/.\n"
            u"\n"
            u"Co nas denerwuje i rozprasza i jak sobie z tym radzić? Zajrzyj tu:\n"
            u"http://gazetapraca.pl/gazetapraca/1,95288,13425980,Co_nas_denerwuje__co_nas_rozprasza.html.\n"
            u"\n"
            u"Pomidor pomoże? Prosty sposób na zarządzanie czasem znajdziesz tu:\n"
            u"http://projektantczasu.pl/technika-pomodoro-pommodoro-pomidora/."),
        (
            u"Wtyczki do przeglądarek, których zadaniem jest blokowanie reklam, nie analizują treści zawartych "
            u"na stronach internetowych. Jeśli posiadałyby taką funkcjonalność, to zapewne odczulibyśmy spowolnienie "
            u"w działaniu przeglądarki internetowej. Wtyczki blokujące reklamy działają w oparciu o listę plików "
            u"graficznych, animacji i wyskakujących okien. To przede wszystkim sam użytkownik decyduje, jakie elementy "
            u"strony mają podlegać zablokowaniu w oparciu o zdefiniowane obiekty.\n"
            u"\n"
            u"O mechanizmie blokowania reklam można przeczytać na stronie producenta najpopularniejszej wtyczki "
            u"Adblock Plus: https://adblockplus.org/en/about.",

            u"Faktycznie, korzystając z wtyczki blokującej reklamy zauważymy, że reklamy te nie wyświetlają się nam "
            u"podczas użytkowania przeglądarki. Co więcej nasza przeglądarka nie tylko nie wyświetla nam zablokowanych "
            u"reklam, ale wcześniej przerywa komunikację z serwerami, które odpowiadają za ich publikacje. Za to, jaki "
            u"serwer powinien być niedopuszczony do komunikacji z przeglądarką, odpowiada sam użytkownik. Wtyczki "
            u"blokujące reklamy działają bowiem w oparciu o listę plików graficznych, animacji i wyskakujących okien. "
            u"To przede wszystkim sam użytkownik decyduje, jakie elementy strony mają znaleźć się na stronie i "
            u"podlegać zablokowaniu.\n"
            u"\n"
            u"O mechanizmie blokowania reklam można przeczytać na stronie producenta najpopularniejszej wtyczki "
            u"Adblock Plus: https://adblockplus.org/en/about.",

            u"Przeglądarka internetowa z zainstalowaną wtyczką nie tylko nie wyświetla nam zablokowane reklamy, "
            u"ale przede wszystkim blokuję komunikację z serwerami, które odpowiadają za ich publikacje. Za to, "
            u"jaki serwer powinien być niedopuszczony do komunikacji z przeglądarką, odpowiada sam użytkownik. Wtyczki "
            u"blokujące reklamy działają bowiem w oparciu o listę plików graficznych, animacji i wyskakujących okien. "
            u"To przede wszystkim sam użytkownik decyduje, jakie elementy strony mają znaleźć się na stronie "
            u"i podlegać zablokowaniu. Wtyczka nie tylko zablokuje te elementy, ale również nie dopuści do komunikacji "
            u"z serwerami odpowiedzialnymi za ich treść.\n"
            u"\n"
            u"O mechanizmie blokowania reklam można przeczytać na stronie producenta najpopularniejszej wtyczki "
            u"Adblock Plus: https://adblockplus.org/en/about."),
    ]
