# Kompilace kódu a verzování

## Prerekvizity

- Připravte si vlastní účet na Github (nebo ekvivalentní službě)
kam se dokážete během cvičení připojit.
- Pokud chcete používat vlastní počítač (doporučeno),
  nainstalujte si vhodné IDE - Visual Studio Code

## Cíle

- Vysvětlit rozdíl mezi kompilací a interpretací.
- Nakonfigurovat IDE pro editaci, sestavení a spouštění malých programů.
- Online běhová prostředí – notebooky, Colab apod.
- Používat Git pro základní workflow verzování (init, commit, branch).

## Přednáška

- [Slajdy: Kompilace kódu a verzování](lecture/presentation.pdf)
- [Komentované příklady: základní Git workflow](seminar/README.md)

Komentované příklady ukazují, jak se zdrojový kód stává spustitelným
softwarem, jak tento proces podporuje IDE a jak při vývoji používat Git.
Společně se prochází [stejné zadání jako v domácí
přípravě](prework/assignment.md), doplněné vysvětlením příkazů a řešením
obvyklých problémů.

## Domácí příprava

[Zadání domácí přípravy: základní Git workflow](prework/assignment.md)

## Cvičení

Cvičení je věnováno rozsáhlejšímu Git workflow, které propojuje práci s
větvemi, vzdáleným repozitářem, konflikty a úpravy historie.

[Zadání cvičení: pokročilé Git workflow](lab/advanced_git_workflow.md)

### Ukázkový kód (Python)

Spusťte následující kód ve vašem IDE a ukažte cvičícímu.
```python
# hello.py
def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
```
Pokud vám zbude čas, věnujte ho pochopení a vylepšení programu výše.

## Dodatečné materiály

- [Shrnutí cvičení](additional_materials/summary.md)

## Zdroje

- [Pro Git, 2nd Edition](https://git-scm.com/book/en/v2)
- [Dokumentace jazyka Python](https://docs.python.org/3/)
- [Python Developer's Guide – compiler](https://devguide.python.org/internals/compiler/)
- [GNU Compiler Collection – dokumentace](https://gcc.gnu.org/onlinedocs/)
