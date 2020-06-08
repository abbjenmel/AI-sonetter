#Ai-Sonetter
Det här projektet har två versioner som båda genererar sonetter som liknar William Shakespeare's sonetter.

##Version 1
Version 1 använder en GP2- text genererande modul som körs i google colab för att generera sonetter. Sonnetterna som genereras 
blir ganska dåliga då de är en halv till en och en halv sonett och de inte rimmar.
För att generera en sonett gå in på länken för att komma till [google colaben](https://colab.research.google.com/drive/188je9qaKHiynj-y5lMlMVm4BMNgJV67A)
Ladda upp filen som heter sonnets.txt som ligger i mappen sonnets till colaben. Efter det måste du köra cell nr 1, 5, 6, 8, 10, 11, 12.
Efter att cellerna är körda är modellen tränad och då kan man gå ner till sektionen som heter Generate Text From the Trained Model,
där kan man välja att köra den första cellen om man vill ha många sonetter eller den andra cellen om man vill ha en sonett.

##Version 2
Version 2 är baserad på ett projek av [LuxMiranda](https://github.com/LuxMiranda/will-ai-shakespeare). Koden genererar en sonett som rimmar
och består av 14 rader, det vill säga att den har rätt struktur för en sonett. För att använda AI'n ladda ner mappen som heter Sonnetter AI. Öppna en command
prompt i mappen som du laddant ned. Kolla vilken version av python du använder då AI'n kräver python 2.7. Om du inte använder python 2.7
ladda ner det innan du kör scriptet. När du har python 2.7 kör skriv in commandot shakespeare.py och då genereras det en sonett. Programmet 
kräver ganska många bibliotek så om du får felmeddelanden om att du inte har de program som krävs ladda ner dem och försök igen.
