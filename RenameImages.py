import sys
import zipfile
import os
import shutil
import re

LUNI = {
    "Ianuarie": "01", "Februarie": "02", "Martie": "03",
    "Aprilie": "04", "Mai": "05", "Iunie": "06",
    "Iulie": "07", "August": "08", "Septembrie": "09",
    "Octombrie": "10", "Noiembrie": "11", "Decembrie": "12"
}

ALLOWED_EXT = {".jpg", ".jpeg", ".png"}


def citeste_date_text(fisier_text):
    """
    Fiecare linie poate avea formate:
      - prenume - nume - DD.MM.YYYY - functie
      - prenume nume - DD.MM.YYYY - functie
    Returnează o listă de tuple (zi, luna_numeric, nume, prenume)
    """
    persoane = []
    with open(fisier_text, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = [p.strip() for p in line.split("-")]
            if len(parts) < 2:
                continue

            # Identificăm partea cu data (cea care conține cifre și . sau /)
            data_part = None
            name_part = None
            prenume = nume = None

            for i, p in enumerate(parts):
                if re.search(r'\d', p) and ('.' in p or '/' in p):
                    data_part = p
                    # numele poate fi partea imediat anterior sau prima parte
                    if i >= 1:
                        name_part = parts[i-1]
                    break

            if data_part is None:
                # fallback: dacă formatul este prenume - nume - data
                if len(parts) >= 3:
                    prenume = parts[0]
                    nume = parts[1]
                    data_part = parts[2]
                else:
                    continue

            if prenume is None or nume is None:
                # name_part poate fi "prenume nume" sau "prenume"
                if name_part:
                    name_tokens = name_part.split()
                    if len(name_tokens) >= 2:
                        prenume = name_tokens[0]
                        nume = " ".join(name_tokens[1:])
                    else:
                        # dacă nu, încercăm să luăm prima două părți din linie
                        tokens = parts[0].split()
                        prenume = tokens[0]
                        nume = " ".join(tokens[1:]) if len(tokens) > 1 else ""
                else:
                    # very defensive fallback
                    tokens = parts[0].split()
                    prenume = tokens[0]
                    nume = " ".join(tokens[1:]) if len(tokens) > 1 else ""

            # Data: acceptăm . sau /
            delimit = "." if "." in data_part else "/"
            date_tokens = [t.strip() for t in data_part.split(delimit)]
            if len(date_tokens) < 2:
                continue
            zi = date_tokens[0].zfill(2)
            luna = date_tokens[1].zfill(2)

            persoane.append((zi, luna, nume, prenume))

    return persoane


def find_images_recursively(folder):
    imgs = []
    for root, _, files in os.walk(folder):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in ALLOWED_EXT:
                imgs.append(os.path.join(root, f))
    # sortăm după nume de fișier pentru a păstra ordinea așteptată
    imgs.sort()
    return imgs


def safe_filename(s):
    # elimină caractere care pot crea probleme în nume de fișier
    return re.sub(r'[\\/:"*?<>|]+', "_", s).strip()


def main():
    if len(sys.argv) != 3:
        print("Utilizare: python RenameImages.py <arhiva.zip> <fisier_text>")
        sys.exit(1)

    arhiva_zip = sys.argv[1]
    fisier_text = sys.argv[2]

    if not os.path.isfile(arhiva_zip):
        print("Eroare: arhiva nu exista!")
        sys.exit(1)

    if not os.path.isfile(fisier_text):
        print("Eroare: fisierul text nu exista!")
        sys.exit(1)

    persoane = citeste_date_text(fisier_text)

    folder_temp = "temp_extract_rename"
    if os.path.exists(folder_temp):
        shutil.rmtree(folder_temp)
    os.makedirs(folder_temp)

    with zipfile.ZipFile(arhiva_zip, 'r') as zip_ref:
        zip_ref.extractall(folder_temp)

    imagini = find_images_recursively(folder_temp)

    if len(imagini) != len(persoane):
        print(f"Eroare: {len(imagini)} imagini găsite, dar {len(persoane)} intrări în fișierul text.")
        print("Verificați că arhiva conține doar imaginile relevante și că ordinea este corectă.")
        shutil.rmtree(folder_temp)
        sys.exit(1)

    folder_arhiva = os.path.dirname(arhiva_zip)
    nume_vechi = os.path.basename(arhiva_zip)
    nume_fara_ext = os.path.splitext(nume_vechi)[0]

    arhiva_noua = os.path.join(folder_arhiva, nume_fara_ext + "_RENAMED.zip")

    with zipfile.ZipFile(arhiva_noua, 'w', zipfile.ZIP_DEFLATED) as new_zip:
        for i, img_path in enumerate(imagini):
            zi, luna, nume, prenume = persoane[i]
            ext = os.path.splitext(img_path)[1].lower()
            nume_scurt = safe_filename(f"{zi}_{luna}_{nume}_{prenume}{ext}")
            new_zip.write(img_path, arcname=nume_scurt)

    shutil.rmtree(folder_temp)
    print(f"Arhivă creată: {arhiva_noua}")


if __name__ == "__main__":
    main()
