# sygnaly

Program analizujący mowę. Wykrywa płeć osoby mówiącej.

Algorytm:
  1. Wczytaj plik.
  2. Wybierz z pliku potrzebne dane.
  3. Wylicz okno, którym będzie wykonywane przeglądanie amplitud sygnału. 
  4. Przekształć sygnał do jednego kanału.
  5. Iteruj po sygnale oknem czasowym:
    5a. Wylicz fft na przedziale
    5b. Wybierz indeks elementu maksymalnego, oblicz częśtotliwość dominującą i odłóż do listy
  6. Posortuj liste rosnąco
  7. Wybierz mediane i przyrównaj do progu.
  8. Zwróć wynik.
  
Okno, którym algorytm iteruje po sygnale jest zależne od parametru dźwięku. 
Kolejne wartości częstotliwości liczone z indeksów listy przekształconej za pomocą fft różnią się o 5 hz.

Próg 165 hx został dobrany metodą prób i błędów na zbiorze plików testowych. 
