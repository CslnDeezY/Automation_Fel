# Import.py

## Descriere
`Import.py` este un script Python care citește date dintr-un fișier Excel cu mai multe pagini (fiecare pagină reprezentând o lună a anului) și generează un fișier text cu informațiile despre persoane.  

- Fiecare foaie din Excel trebuie să aibă următoarea structură:
  - Coloana 1: **Nume Prenume**
  - Coloana 2: **Data nașterii**
  - Coloana 3: **Funcție** (poate fi goală)  

- Scriptul va genera un fișier text în format: prenume - nume - data nașterii - funcție
- Dacă coloana **Funcție** este goală, va fi înlocuită cu un string gol.

--

## Utilizare
1.Asigurați-vă că aveți instalata Python si ca ati instalat corect repositoriul Automation_Fel.
2. Rulați scriptul folosind comanda:
   ```bash
   python Import.py <fisier_excel> <luna> <an> <folder_output>
   ```
    - `<fisier_excel>`: Calea către fișierul Excel de importat.
    - `<luna>`: Luna pentru care se generează fișierul (Luna o scrieti exact cum este in fisierul excel (Incepe cu litera mare si restul mici)).
    - `<an>`: Anul pentru care se generează fișierul.
    - `<folder_output>`: Calea către folderul unde va fi salvat fișierul text generat.

## Exemplu de rulare:
```bash
py Import.py "D:\ATRAG\Felicitari\2025-2026 Zile de naștere.xlsx" Decembrie 2025 "D:\ATRAG\Felicitari\.done"
```

## Note
- Asigurați-vă că fișierul Excel are foile denumite corect (de exemplu: Ianuarie, Februarie, etc.).
- Asigurativa ca aveti instalate extensiile specificate in fisierul `requirements.txt`
