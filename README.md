# Automation_Fel — Instrucțiuni de utilizare

Scurt: acest proiect conține două scripturi Python:
- `Import.py` — generează un fișier text cu onomastici dintr-un fișier Excel (foaie lună).
- `RenameImages.py` — redenumește imaginile dintr-o arhivă .zip pe baza fișierului text și creează o arhivă *_RENAMED.zip*.
- `run_windows.bat` — rulează automat pas cu pas cele două scripturi și șterge fișierul text rezultat.

Urmează pașii de mai jos pentru utilizare pe Windows.

Cerinte minime
- Asigură-te că ai instalat Python versiunea 3.8 sau mai recentă și că executabilul Python este recunoscut de sistem, adică poate fi rulat din linia de comandă/terminal folosind comanda python.

1) Clonare repository
- Deschide Command Prompt sau PowerShell.
- Rulează:
```powershell
cd /d C:\
git clone <URL_REPOSITORY>
cd /d d:\ATGAR\Fel\Automation_Fel
```
Înlocuiește `<URL_REPOSITORY>` cu URL-ul git al proiectului.

2) Configurare mediu virtual (.venv) și instalare dependințe
- Creare mediu virtual (în folderul proiectului):
```powershell
python -m venv .venv
```
- Activare:
  - PowerShell:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  - Command Prompt:
  ```bat
  .venv\Scripts\activate.bat
  ```
- Instalare dependințe:
```powershell
pip install -r requirements.txt
```
## Pentru utilizatorii fără experiență
### run_windows.bat 
Rulează automat totul.
(Notă: dacă folosiți doar această metodă scriptul doar va redenumi toate felicitarile din arhiva)
- Pas I) Asigurațivă că ați realizat ABDOLUT toate felicitările din luna respectivă.
- Pas II) Descarcați arhiva din Canva.
IMPORTANT: arhiva de tip `.zip` trebuie să conțină exact tot atâtea felicitări cât și oameni în pagina din excel și sa se afle exact în aceeași ordine cum sunt găsiți în document.
- Deschideți `PowerShell` sau `Command Prompt` și schimbați directorul în proiect:
```powershell
cd /d d:\ATGAR\Fel\Automation_Fel
```
- Rulați batch-ul (folosiți ghilimele pentru căi cu spații).
Mai simplu este să dați click dreapta pe fisier sau folder și să copiați calea absolută(aveți buton special `copy as a path`) 
Parametri: fișier Excel, luna (nume în română), arhiva .zip:
```powershell
& .\run_windows.bat "D:\cale\lista.xlsx" "noiembrie" "D:\cale\poze.zip"
```
Ce face:
- Apelează `Import.py` pentru a crea `onomastici_<LUNA>_<AN>.txt` în folderul în care se află arhiva (parametrul 3).
- Apelează `RenameImages.py` cu arhiva și fișierul text găsit; creează `*_RENAMED.zip` în același folder.
- Șterge fișierul text generat.

## Pentru utilizatori mai experimentați:
### A) Import.py

- Acesta va citi toți onomasticii din pagina specificată și îi va pune într-un fișier text in formatul: `"Nume Prenume - data nașterii - fpuncție"`
(functia poate lipsi).

- Puteți utiliza acest script separat pentru a vă crea un fișier text de unde puteți extrage prin Ctrl+C numele si prenumele în ordinea în care trebuie inserate în felicitare (se poate utiliza Ctrl+V), deasemenea puteți proceda la fel pentru a gasi mai usor persoana.
 
  - Utilizare:
  ```powershell
  python Import.py "<cale_catre_excel>" <luna> "<folder_output>"
  ```
  - Exemple:
  ```powershell
  python Import.py "D:\Documents\lista.xlsx" "noiembrie" "D:\Documents\"
  python Import.py ".\lista.xlsx" "11" ".\"
  ```
  - Observații:
    - `<luna>` poate fi nume în română (ex: `noiembrie`, `ian`) sau număr (`11`).
    - Dacă nu furnizezi anul, scriptul alege anul astfel încât luna să nu fie în trecut relativ la data curentă (dacă luna < luna curentă -> folosește anul următor).
    - Output: `onomastici_<LUNA>_<AN>.txt` în folderul specificat.

### B) RenameImages.py
- Acest script pentru a redenumi toate fișierele salvate într-o arhiva de tip `.zip` (Redenumirea este utilă pentru persoana ce programează felicitările).
- ATENȚIE!!!: Felicitările în arhivă trebuie să se regăsească exact în aceeași ordine ca și numele corespunzătoare în fișierul text de unde sunt extrase, în caz contrar datele și numele fiecărei felicitări va fi eronat.   
  - Utilizare:
  ```powershell
  python RenameImages.py "<cale_catre_arhiva.zip>" "<cale_catre_fisier_text>"
  ```
  (Fisierul text este cel creat la paul anterior)
  - Exemplu:
  ```powershell
  python RenameImages.py "D:\Date\poze.zip" "D:\Date\onomastici_noiembrie_2025.txt"
  ```
  - Observații:
    - Arhiva trebuie să conțină imaginile; scriptul parcurge recursiv conținutul zip și ia fișiere cu extensiile `.jpg`, `.jpeg`, `.png`.
    - Dacă numărul imaginilor diferă de numărul intrărilor din fișierul text, scriptul se oprește și afișează eroare.
    - Output: `poze_RENAMED.zip` (nume identic cu arhiva inițială + `_RENAMED.zip`) în același folder.

##### Probleme comune și soluții rapide
- "python" nu este recunoscut -> Python nu este în PATH. Reinstalează Python și bifează opțiunea "Add to PATH" sau folosește calea completă către python.exe.
- Eroare la deschiderea fișierului Excel -> verifică calea și dacă fișierul este închis (nu deschis în Excel).
- Nu se găsește foaia -> verifică numele foilor din Excel.
- Număr imagini != intrări în fișier text -> verifică conținutul zip și formatul fișierului text (fiecare linie trebuie să conțină date corecte).
- Probleme cu spații în căi -> folosește întotdeauna ghilimele în jurul parametrilor.
