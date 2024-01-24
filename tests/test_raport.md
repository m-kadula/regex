# Raport z testów

### Wstęp

Biblioteka regex została poddana szczegółowym testom, aby zapewnić jej poprawne działanie i zgodność z oczekiwaniami.
Testy zostały przeprowadzone z wykorzystaniem różnych technik, w tym testów biało- i czarnoskrzynkowych.

### Testy białoskrzynkowe

Testy białoskrzynkowe, znane również jako testy strukturalne, skupiają się na wewnętrznej strukturze kodu.
W naszym przypadku, testy te obejmowały analizę funkcji i metod wewnątrz biblioteki regex.

Na przykład, w pliku `tests/test_automata.py`, przeprowadziliśmy testy jednostkowe na klasach
`ENFA` i `NFA`, które testują wewnętrzne funkcje konwersji automatu. Testy te sprawdzają,
czy funkcje te poprawnie przekształcają wyrażenia regularne na odpowiednie automaty.

Podobnie, w pliku `tests/test_parser.py`, przeprowadziliśmy testy jednostkowe na klasach `Lexer` i `Parser`,
które testują funkcje analizatora leksykalnego i syntaktycznego. Te testy sprawdzają, czy analizatory poprawnie
przetwarzają wyrażenia regularne na tokeny i drzewa składniowe.

### Testy czarnoskrzynkowe

Testy czarnoskrzynkowe, znane również jako testy funkcjonalne, skupiają się na funkcjonalności kodu bez względu na jego
wewnętrzną strukturę. W naszym przypadku, testy te obejmowały sprawdzanie, czy biblioteka regex poprawnie interpretuje i
przetwarza wyrażenia regularne.

Na przykład, w pliku `tests/test_compile.py`, przeprowadziliśmy testy jednostkowe na klasie `CompiledRegex`, która
testuje funkcje kompilacji wyrażeń regularnych. Testy te sprawdzają, czy biblioteka poprawnie interpretuje wyrażenia
regularne i zwraca oczekiwane wyniki dopasowań.

### Podsumowanie

Przeprowadzone testy biało- i czarnoskrzynkowe zapewniają kompleksową ocenę funkcjonalności biblioteki regex. Dzięki nim
możemy mieć pewność, że biblioteka działa zgodnie z oczekiwaniami i spełnia swoje zadania.
