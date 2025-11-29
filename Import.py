import os
import sys
from openpyxl import load_workbook

def main():
    # verificare argumente linie de comanda
    if len(sys.argv) != 5:
        print("Utilizare: python Import.py <fisier_excel> <luna> <an> <folder_output>")
        sys.exit(1)

    fisier_excel = sys.argv[1]  # poate fi cale absoluta
    luna = sys.argv[2]
    an = sys.argv[3]
    folder_output = sys.argv[4]  # poate fi cale absoluta

    # verificare existenta folder output
    if not os.path.exists(folder_output):
        os.makedirs(folder_output)

    # constuire cale completa pentru fisierul de output
    nume_fisier_output = f"onomastici_{luna}_{an}.txt"
    cale_fisier_output = os.path.join(folder_output, nume_fisier_output)

    # deschidere fisier excel
    try:
        wb = load_workbook(filename=fisier_excel)
    except Exception as e:
        print(f"Eroare la deschiderea fisierului Excel: {e}")
        sys.exit(1)

    # verificare daca pagina exista
    if luna not in wb.sheetnames:
        print(f"Eroare: nu exista pagina '{luna}' în fișier.")
        print(f"Pagini disponibile: {wb.sheetnames}")
        sys.exit(1)

    ws = wb[luna]

    # citire date si scriere in fisier text
    try:    
        with open(cale_fisier_output, 'w', encoding='utf-8') as f_out:
            for row in ws.iter_rows(min_row=2, values_only=True):  # ignoram header
                nume_prenume = row[0]
                data_nastere = row[1]
                functie = row[2] if row[2] else ""  # daca lipseste, folosim string gol

                if nume_prenume and data_nastere:
                    # spargem "Nume Prenume" -> prenume si nume
                    parti = nume_prenume.split(' ', 1)
                    prenume = parti[1] if len(parti) > 1 else ""
                    nume = parti[0]
                    linie_output = f"{prenume} - {nume} - {data_nastere} - {functie}\n"
                    f_out.write(linie_output)
    except Exception as e:
        print(f"Eroare la scrierea în fișierul de output: {e}")
        sys.exit(1)

    print(f"Datele au fost scrise cu succes în '{cale_fisier_output}'")


if __name__ == "__main__":
    main()
