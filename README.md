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
