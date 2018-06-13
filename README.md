Projekt 1

Program sprowadzający wyrażenie do najprostszej postaci (alternatywa koniunkcji).
Wyrażenie może zawierać:
- alfanumeryczne zmienne logiczne
- operatory: koniunkcji (&), alternatywy (|), alternatywy wykluczającej (^), negacji (!), implikacji (>) i równoważności (=)
- stałe logiczne (0 lub 1)
- spacje

Ważne:
W algorytmie ewaluacyjnym operatory: negacji i koniunkcji mają wyższy priorytet - jest to spowodowane wygodą.
Wtedy nie trzeba wpisywać wyrażenia, np. ((!a)&b)|c, wystarczy !a&b|c.
W razie wątpliwości co do kolejności wykonywania działań, proszę użyć nawiasowania - wszystkie inne operatory mają ten sam
priorytet, co przy ewaluowaniu spowoduje wykonywanie ich od prawej do lewej w obrębie pojedynczej pary nawiasów.

Projekt 2

Program wczytujący plik w formacie JSON z opisem grafiki, wyświetlający grafikę na ekranie i zapisujący ją do pliku PNG.

Przykładowy plik JSON został zawarty w projekcie.

Wywołanie:
-o / --output - argument po fladze to nazwa pliku, do którego zostanie zapisana grafika. Flaga opcjonalna. Jej brak spowoduje tylko wyświetlnie grafiki.

Argument bez flagi to nazwa pliku z wejściowym JSON-em.

W przypadku wielu nazw plików wejściowych/wyjściowych, zostanie wybrana pierwsza napotkana nazwa pliku danego typu.
Dla pliku wyjściowego nie trzeba podawać rozszerzenia '.png'.

np.
```
python paint.py input.json
python paint.py input.json --output output.png
```

Do uruchomienia wymagany jest pakiet Pillow

Projekt 3

Symulator gry na giełdzie.
```
python manage.py runserver
```
```
localhost:8000
```
Do uruchomienia wymagany jest pakiet quandl.

W razie dalszych problemów, potrzebne mogą okazać się pakiety pandas i pandas_datareader.
