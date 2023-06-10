# **Biblioteka do wyszukiwania wyrażeń regularnych**

Program udostępnia zbiór narzędzi do wyszukiwania 
wzorca zapisanego w postaci wyrażenia regularnego.

## Składnia języka
Jedynymi dozwolonymi elementami wyrażenia regularnego są symbole ASCII
### Podstawy
- W celu połączenia dwóch wyrażeń w jedno zapisujemy je obok siebie (np. `AB`
akceptuje wyrażenie `A` po którym następuje `B`) 
- symbol `|` oznacza alternatywe pomiędzy dwoma wyrażeniami
(np. `A|B` akceptuje wyrażenie `A` lub `B`)
- konkatenacja ma priorytet nad operatorem `|` więc wyrażanie można grupować za 
pomocą `()` (np. aby napisać wyrażenie rozpoczynające się od litery `a` i 
kończące na `b` lub `c` zapisujemy `a(b|c)`)
- ciąg alternatyw `a|b|c|d` można zapisać jako `[abcd]`, do `[]` można również
wpisywać zakres symboli (wcześniejszy przykład jest równoważny `[a-d]`). W `[]`
może znajdować się kilka zakresów (np. `[A-Z0-9]`)
### Operatory
- symbol `*` następujący po wyrażeniu oznacza 0 lub więcej wystąpień tego 
wyrażenia (np `a*` akceptuje `aaaaaa` oraz ` `)
- symbol `+` następujący po wyrażeniu oznacza 1 lub więcej wystąpień tego 
wyrażenia (np `a+` akceptuje `aaaaaa`, ale **nie** akceptuje ` `) 
- symbol `?` następujący po wyrażeniu oznacza dokładnie 0 lub 1
wystąpienie wyrażenia (np `a?` akceptuje `a` lub ` `) 
- zapis `A{x}`, gdzie `x` jest liczbą naturalną, oznacza dokładnie `x` 
wysąpień wyrażenia `A`
- zapis `A{x,y}`, gdzie `x,y` są liczbami naturalnymi, oznacza że liczba
wysąpień `A` zawiera się w przedziale od `x` do `y` włącznie
### Symbole specjalne
- symbol `.` zastępuje wszystkie symbole
- symbol `\w` zastępuje `[a-zA-Z0-9_]`
- symbol `\d` zastępuje `[0-9]`
- symbol `\s` zastępuje `[\n\t ]`
- duże wersje poprzednich symboli zastępują dopełnienie ich małych 
odpowiedników
- specjalny symbol `\ ` postawiony przed **symbolem specjalnym** , **operatorem**
lub innym znakiem o szczególnym znaczeniu, niweluje jego specjalne zadanie
(wliczając w to samego siebie) 

## Obsługa paczki
W celu użycia biblioteki w programie należy zaimportować klasę `CompiledRegex`
z pliku `compile.py` za pomocą ```from regex.compiled import CompiledRegex```.
Następnie zainicjalizować klasę podając za argument wyrażenie regularne.
Metody tej klasy zapewniają narzędzia do wyszukiwania instancji w tekście:
- `full_match(str)` spawdza czy `str` jest akceptowany przez wyrażenie
- `find_all(str)` wyszukuje wszystkie wystapienia słów należących do języka 
wyrażenia regularnego w `str`
-  `match(str)` zwraca początek `str` pasujący do wyrażenia reguralnego, w 
przeciwnym razie zwraca None
- `search(str)` zwraca pierwsze słowo należące do języka wyrażenia reguralnego
w tekście
- `pack()` zwraca skompilowaną wersje regex'a która może zostać zapisana
do pliku
- `unpack()` pozwala wczytać skompilowaną wersje regex'a
```python
from regex.compile import CompiledRegex

# Kompilowanie wyrażenia rozpoznającego adres e-mail
foo = CompiledRegex(r"([a-z0-9_\.]+)@([-\da-z\.]+)\.([a-z\.]{2,6})")
foo.full_match("abc@gmail.com")  # returns <Match: 'abc@gmail.com', span: (0, 13)>
foo.full_match("abcgmail.com")   # returns None

txt = "abc@gmail.com, abcgmail.com"
foo.find_all(txt)  # returns [<Match: 'abc@gmail.com', span: (0, 13)>]
foo.search("abc@gmail.com, abcgmail.com") # returns <Match: 'abc@gmail.com', span: (0, 13)>
```
