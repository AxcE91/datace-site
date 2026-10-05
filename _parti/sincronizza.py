"""
Copia il footer unico (_parti/footer.html) in tutte le pagine del sito.

Il footer era ricopiato a mano in ogni pagina: aggiungere o togliere uno
strumento voleva dire toccare 15 file, ed era facile dimenticarne uno.
Ora si modifica SOLO _parti/footer.html e si lancia, dalla radice del sito:

    py _parti/sincronizza.py            # aggiorna le pagine
    py _parti/sincronizza.py --controlla # non scrive: dice quali pagine sono diverse

Lo script sostituisce solo ciò che sta fra i marcatori
<!-- DATACE FOOTER START --> e <!-- DATACE FOOTER END -->: il resto della
pagina non lo tocca, e rispetta gli a-capo di ogni file.
Le cartelle che iniziano con "_" non vengono pubblicate da GitHub Pages.
"""
import pathlib
import re
import sys

SITO = pathlib.Path(__file__).resolve().parent.parent
# utf-8-sig: se footer.html viene salvato con un BOM (lo fa PowerShell, alcuni
# editor), il BOM NON deve finire nelle pagine: si accumulerebbe a ogni giro.
FOOTER = (SITO / "_parti" / "footer.html").read_text(encoding="utf-8-sig").strip()
BLOCCO = re.compile(r"<!-- DATACE FOOTER START -->.*?<!-- DATACE FOOTER END -->", re.S)


def pagine():
    for p in sorted(SITO.rglob("*.html")):
        rel = p.relative_to(SITO).parts
        if rel[0].startswith(("_", ".")) or rel[0] == "docs":
            continue
        yield p


def main(controlla: bool) -> int:
    diverse = []
    for p in pagine():
        testo = p.read_bytes().decode("utf-8")
        trovato = BLOCCO.search(testo)
        if not trovato:
            continue  # pagine senza footer standard (404, pagine vecchie, bozze)
        # Gli a-capo del BLOCCO, non del file: alcune pagine li hanno misti, e
        # cambiarli farebbe risultare modificate righe identiche.
        nl = "\r\n" if "\r\n" in trovato.group(0) else "\n"
        nuovo = BLOCCO.sub(lambda _: FOOTER.replace("\n", nl), testo, count=1)
        if nuovo != testo:
            diverse.append(p.relative_to(SITO))
            if not controlla:
                p.write_bytes(nuovo.encode("utf-8"))
    azione = "da aggiornare" if controlla else "aggiornate"
    print(f"{len(diverse)} pagine {azione}", *diverse, sep="\n  ")
    return 1 if (controlla and diverse) else 0


if __name__ == "__main__":
    sys.exit(main("--controlla" in sys.argv))
