# Kompilace kódu a verzování — co jsme dělali na cvičení a jak to dohnat

> Materiál k [tématu 01](https://github.com/CVUT-FS-12110/Introduction-to-Programming/blob/master/topics/01-compilation-versioning-ides/README.md). Cvičení je za námi — tenhle text je pro ty z vás, kteří nestihli všechny kontrolní body, nebo je odklikali, ale nejsou si jistí, co se vlastně stalo. Projděte si sekce k tomu, kde jste se zasekli, a zkuste si dané kroky zopakovat v klidu doma. Nemusíte dělat vše znovu od nuly — stačí ta část, která vám nesedí.
>
> **Poznámka k větvím:** v předmětu se držíme výchozí větve `master`, protože to je výchozí nastavení Gitu po běžné instalaci. GitHub dnes standardně zakládá repozitáře s větví `main` — pokud si to v nastavení účtu nepřenastavíte na `master`, budete mít lokálně `master` a na GitHubu `main`, a začnou vám nesedět příkazy ze zadání. Buď si tedy GitHub přenastavte (*Settings → Repositories → Repository default branch*), nebo všude v zadání důsledně dosazujte název své reálné větve. Princip je v obou případech úplně stejný.

---

## Rychlá sebekontrola — kde vlastně jsem?

Projděte si seznam a zaškrtněte si, co máte reálně hotové. Podle toho poznáte, kam v tomhle textu skočit.

**Domácí příprava (repozitář `progintro`):**
- [ ] repozitář existuje na GitHubu a je naklonovaný u mě v počítači
- [ ] mám v něm commit s `README.md` a zprávou `added readme`
- [ ] existuje větev `dev` s dalším commitem a je odeslaná na GitHub
- [ ] mám commit vytvořený přes webové rozhraní GitHubu (`edited online`)
- [ ] `dev` je sloučená do `master` a existuje release `v0.1`

**Cvičení (fork repozitáře vyučujícího):**
- [ ] **A** — `origin` = můj fork, `upstream` = originál, `app.py` a `CHANGELOG.md` jsou v mém forku
- [ ] **B** — funkce ve větvi `feature/user-name` prošla přes pull request do `master`
- [ ] **C** — vyřešený konflikt mezi `feature/greeting-style` a `feature/formal-greeting`
- [ ] **D** — `git stash` a hotfix, rozpracovaná validace se neztratila
- [ ] **E** — rebase a úklid historie *(rozšiřující)*
- [ ] **F** — cherry-pick a revert *(rozšiřující)*
- [ ] **7** — anotovaný tag `v0.2.0` a release

První nezaškrtnutá položka je místo, kde má smysl začít. Části E a F jsou rozšiřující — pokud jste je nestihli, není to problém; základ jsou body A–D.

---

## 1. Teorie na začátku: kompilace vs. interpretace

Tohle byl teoretický úvod přednášky a často se z něj ve spěchu stane jen dvojice slov bez obsahu. Rozdíl je přitom jednoduchý:

- **Kompilovaný jazyk** (C, C++, Rust) — zdrojový kód se *předem*, celý najednou, přeloží kompilátorem do strojového kódu. Vznikne spustitelný soubor, který pak běží sám o sobě, bez potřeby původního zdrojáku. Syntaktické chyby a velkou část typových chyb odhalí už překlad — program se prostě nezkompiluje.
- **Interpretovaný jazyk** (typicky Python) — kód vykonává za běhu interpret. Není zde samostatný krok "vyrob binárku", takže vývoj je rychlejší, ale chyba na řádku 400 se projeví teprve ve chvíli, kdy program ten řádek skutečně vykoná.

Přesnější obrázek u Pythonu: `.py` soubor se nejdřív přeloží do **bytecode** (mezikód, ty soubory `.pyc` ve složce `__pycache__`) a teprve ten vykonává virtuální stroj Pythonu. Takže i "interpretovaný" jazyk má krok překladu — jen probíhá automaticky při spuštění a cílem není strojový kód procesoru. Hranice kompilovaný/interpretovaný je tedy spíš spektrum než ostrá čára. Detaily najdete v [Python Developer's Guide – compiler](https://devguide.python.org/internals/compiler/), pro srovnání klasický kompilátor v [dokumentaci GCC](https://gcc.gnu.org/onlinedocs/).

**Co jste měli na cvičení ukázat:** spuštění `hello.py` ve svém IDE. Pokud jste se k tomu nedostali, uděláte to za dvě minuty doma:

```python
# hello.py
def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
```

Podmínka `if __name__ == "__main__":` zajistí, že se `main()` zavolá jen při přímém spuštění souboru, ne když ho někdo naimportuje jako modul. Uvidíte ji v Pythonu pořád, tak ať víte, co dělá.

---

## 2. IDE a SSH klíč — nejčastější důvod, proč se někdo na cvičení zdržel

Pokud jste na cvičení strávili půlku času tím, že vám GitHub odmítal `push`, je to skoro jistě tímhle. Doma si to dejte do pořádku, ať vás to už nikdy nezastaví:

1. **VS Code** (nebo jiné IDE, se kterým umíte).
2. **SSH klíč** napojený na GitHub účet:
   - `ssh-keygen -t ed25519 -C "vas@email.cz"` vygeneruje klíčový pár,
   - obsah **veřejné** části (`~/.ssh/id_ed25519.pub`) vložíte na GitHubu do *Settings → SSH and GPG keys → New SSH key*,
   - privátní klíč (bez `.pub`) nikdy nikam nekopírujte a nikomu neposílejte,
   - ověření: `ssh -T git@github.com` — správná odpověď je uvítací hláška s vaším uživatelským jménem (a informace, že shell přístup GitHub neposkytuje; to je v pořádku).
3. Repozitář musí být naklonovaný přes **SSH adresu** (`git@github.com:...`), ne HTTPS — jinak se SSH klíč vůbec nepoužije. Ověřit i změnit se to dá přes `git remote -v` a `git remote set-url origin ...`.

---

## 3. Základní model Gitu — pokud vám příkazy přišly jako magie

Tohle je nejdůležitější část celého materiálu. Jakmile vám sedne tenhle obrázek, přestanou být příkazy náhodná zaklínadla:

```
pracovní adresář  →  staging area (index)  →  lokální repozitář  →  vzdálený repozitář
     (edituju)          (git add)               (git commit)           (git push)
```

- **Pracovní adresář** — soubory tak, jak je vidíte a upravujete.
- **Staging area (index)** — výběr změn, které chcete dát do příštího commitu. `git add` sem věci přidává. Existuje proto, abyste mohli commitnout jen *část* svých úprav.
- **Lokální repozitář** — historie u vás na disku. `git commit` z obsahu staging area vytvoří nový snímek. Celá historie je lokálně, i bez internetu.
- **Vzdálený repozitář** — GitHub. Synchronizujete se s ním jen vědomě, přes `push` a `pull`/`fetch`.

Dva reflexy, které si osvojte hned: **`git status`** (v jakém jsem stavu, co je ve staging area) a **`git diff`** (co přesně jsem změnil). Před každým commitem. Je to nejlevnější pojistka proti tomu, že commitnete něco, co jste nechtěli — a je to pravidlo výslovně uvedené i v zadání cvičení.

Další pojmy, které padly a stojí za ujasnění:
- **Commit** je neměnný snímek celého projektu plus odkaz na předchozí commit. Historie je tím pádem řetěz (přesněji orientovaný graf) commitů.
- **Větev (branch)** je jen **pojmenovaný ukazatel na commit**. Nic se nekopíruje, proto je zakládání větví levné a běžné — klidně jich mějte desítky.
- **HEAD** je ukazatel na to, kde právě stojíte (typicky na aktuální větvi).
- **Tag** je taky ukazatel na commit, ale **nepohyblivý**. Větev se s dalšími commity posouvá, tag zůstává navždy na jednom commitu. Proto se tagy používají na verze.

---

## 4. Domácí příprava — základní workflow, krok za krokem

[Zadání](https://github.com/CVUT-FS-12110/Introduction-to-Programming/blob/master/topics/01-compilation-versioning-ides/prework/assignment.md). Pokud jste ho na cvičení nestihli nebo si nejste jistí, co se v jednotlivých krocích dělo:

**Klon.** `git clone` stáhne celou historii repozitáře včetně informace, odkud pochází — ta se uloží jako vzdálený repozitář jménem `origin`.

**První commit.** `git add README.md` → `git commit -m "added readme"` → `git push`. Zpráva commitu popisuje, *co se stalo* — ne "úkol 1" ani "test". Zvykejte si na to od začátku.

**Větev `dev`.** `git switch -c dev` (moderní varianta) nebo `git checkout -b dev` (starší, funguje pořád) vytvoří větev a rovnou na ni přepne. Přidáte řádek `Under development` do `README.md`, přidáte prázdný textový soubor, oboje commitnete a odešlete: `git push -u origin dev`. Přepínač `-u` nastaví vazbu na vzdálenou větev, takže příště stačí prosté `git push`.

> Pozor na past: Git neumí verzovat prázdné **adresáře**, ale prázdný **soubor** commitnout jde. Musí ale projít přes `git add` — sám se do commitu nedostane.

**Editace online.** Úprava souboru přímo v rozhraní GitHubu vytvoří normální commit, úplně stejný, jako byste ho udělali lokálně. Poučení: Git nežije jen v terminálu. Důsledek, který mnohé překvapí — po téhle úpravě má vzdálená větev commit navíc oproti vaší lokální. Než budete pokračovat lokálně, musíte si ho stáhnout (`git pull`), jinak vám `push` selže.

**Merge na GitHubu.** Sloučení `dev` do `master` přes webové rozhraní je zjednodušená verze toho, co jste pak na cvičení dělali s konflikty ručně.

**Release `v0.1`.** Release je tag obalený hezčím rozhraním (popis vydání, přiložené soubory). Označuje stav, který jste "vydali".

---

## 5. Cvičení — pokročilý workflow, sekce po sekci

[Zadání](https://github.com/CVUT-FS-12110/Introduction-to-Programming/blob/master/topics/01-compilation-versioning-ides/lab/advanced_git_workflow.md). Bylo záměrně navržené tak, aby se celé nedalo stihnout — takže pokud jste ho nedokončili, je to očekávaný stav, ne selhání. Níže je ke každé sekci to podstatné.

| Sekce | Co se procvičuje | Proč to v praxi potřebujete |
|---|---|---|
| 1. Fork + upstream | práce s repozitářem, do kterého nemáte právo zápisu | takhle se přispívá do open-source |
| 2. Feature branch + PR | izolace jedné funkce, review před sloučením | standardní firemní workflow |
| 3. Konflikt | dvě větve mění stejný řádek | nevyhnutelná realita týmové práce |
| 4. `git stash` | odložení rozpracované práce kvůli naléhavé opravě | hotfix uprostřed rozdělané věci |
| 5. Rebase | lineární, čitelná historie | usnadňuje review a hledání chyb |
| 6. Cherry-pick / revert | přenesení a vrácení konkrétního commitu | náprava chyby bez přepisování historie |
| 7. Tag + release | značení verzí | jak se vydává software |

### Sekce 1 — fork a upstream (kontrolní bod A)

Nejčastější zmatek celého cvičení: **fork vs. clone.**
- **Fork** = vaše vlastní kopie celého repozitáře **na GitHubu**. Vlastníte ji, můžete do ní pushovat.
- **Clone** = stažení repozitáře (vašeho forku i cizího) **na váš disk**.

V úloze děláte obojí: forknete repozitář vyučujícího a pak klonujete **svůj fork**. Proto musí `origin` ukazovat na váš fork. Originál přidáte jako druhý vzdálený repozitář:

```
git remote add upstream <adresa repozitáře vyučujícího>
git remote -v
```

Výstup musí ukazovat `origin` = váš fork, `upstream` = originál. Pokud vám `push` hlásí chybějící oprávnění, je to skoro vždycky tím, že máte `origin` nastavený na originál.

Aktualizace vašeho `master` podle originálu pak vypadá takto: `git fetch upstream` stáhne změny (ale nic nemění ve vašich větvích), `git merge upstream/master` je začlení do vaší aktuální větve, `git push origin master` je odešle do vašeho forku.

> `git fetch` jen stahuje, `git pull` = `fetch` + rovnou `merge`. Pro pochopení, co se děje, je na začátku lepší dělat ty dva kroky odděleně.

### Sekce 2 — feature větev a pull request (kontrolní bod B)

Smysl feature větve: rozpracovaná práce nikdy nejde přímo do `master`. Vzniká odděleně, projde kontrolou a teprve pak se sloučí.

Zadání chtělo změnu rozdělit **nejméně do dvou commitů** (načtení vstupu zvlášť, sestavení pozdravu zvlášť). Není to buzerace — commit s jednou logickou změnou se dá později mnohem snáz pochopit, vrátit i najít jako viníka chyby.

Historii si zobrazíte příkazem `git log --oneline --graph --all`. Ten se naučte, je to váš hlavní nástroj na zorientování se v tom, co se ve vašem repozitáři vlastně děje.

Pull request je funkce GitHubu, ne Gitu — je to žádost o sloučení větve, kolem které se dá diskutovat a komentovat. V tomhle cvičení ho otevíráte do `master` **ve svém forku**, ne do repozitáře vyučujícího.

Po sloučení uklidíte: `git switch master`, `git pull`, `git branch -d feature/user-name` (lokálně) a smazání větve na GitHubu (tlačítko v PR).

### Sekce 3 — konflikt (kontrolní bod C)

Konflikt vzniká, když dvě větve změnily **stejné místo stejného souboru** a Git nemá jak rozhodnout, která verze platí. Není to chyba, kterou jste způsobili — je to Git, který korektně říká „tady rozhodni ty, nebudu hádat".

V souboru uvidíte:

```
<<<<<<< HEAD
verze z větve, ve které právě jste
=======
verze z větve, kterou slučujete
>>>>>>> feature/formal-greeting
```

Postup: obsah ručně upravte tak, aby dával smysl (v tomhle zadání měl uživatel mít na výběr mezi neformálním a formálním pozdravem, tedy obě varianty měly zůstat zachované), **odstraňte všechny tři značky**, program spusťte a vyzkoušejte, pak `git add app.py` a `git commit` dokončí merge.

Když si v půlce nejste jistí: **`git merge --abort`** vás bezpečně vrátí do stavu před začátkem merge. Nic se neztratí.

### Sekce 4 — stash (kontrolní bod D)

`git stash` je šuplík na rozdělanou práci: odloží necommitnuté změny, pracovní adresář se vrátí do čistého stavu a vy se můžete bez problémů přepnout jinam.

**Chyták, na který jich narazilo víc:** `git stash` ve výchozím nastavení **neodloží soubory, které Git zatím nesleduje** (nově vytvořené, nikdy nepřidané přes `git add`). Zadání přitom mluvilo o odložení „včetně případných nových souborů" — na to potřebujete `git stash -u` (nebo `--include-untracked`).

Zpátky to dostanete přes `git stash pop` (obnoví a smaže záznam) nebo `git stash apply` (obnoví a záznam ponechá). Seznam odložených věcí zobrazí `git stash list`, úklid zbytečného záznamu `git stash drop`. Pokud jste použili `apply`, záznam vám tam zůstal — to byl poslední krok zadání.

### Sekce 5 — rebase *(rozšiřující, kontrolní bod E)*

Merge i rebase řeší totéž — dostat změny z jedné větve do druhé — ale zásadně jinak:

- **merge** vytvoří nový spojovací commit a **zachová** historii tak, jak se skutečně odehrála (včetně větvení).
- **rebase** vezme commity vaší větve a **přepíše je** tak, jako by od začátku vycházely z nového základu. Výsledkem je rovná, lineární historie — ale commity dostanou **nová ID** (hashe). Staré commity nezmizí hned, ale už na ně neukazuje žádná větev.

Interaktivní rebase (`git rebase -i`) navíc umožní commity slučovat, přejmenovávat a přeskupovat — to je ten "úklid historie", kdy z pěti commitů typu „fix" uděláte jeden smysluplný.

Protože se ID změnila, běžný `git push` už neprojde — vzdálená větev vypadá jako rozcházející se. Proto zadání mluví o bezpečné variantě force push:

```
git push --force-with-lease
```

`--force-with-lease` je bezpečnější než `--force`, protože nejprve ověří, že vzdálená větev je pořád v tom stavu, jaký jste naposledy viděli. Pokud tam někdo mezitím něco přidal, push se odmítne místo toho, aby cizí práci přepsal.

**Zlaté pravidlo:** nepřepisujte historii, kterou už někdo jiný používá. Na vlastní feature větvi je to v pořádku, na sdíleném `master` ne.

A kdyby se rebase nepovedl: **`git reflog`** je záchranná síť. Zaznamenává, kam všude HEAD ukazoval, takže se dá dohledat i commit, na který už nevede žádná větev, a vrátit se k němu.

### Sekce 6 — cherry-pick a revert *(rozšiřující, kontrolní bod F)*

Dvě operace, které se často pletou dohromady:

- **`git cherry-pick <hash>`** = „vezmi *tenhle jeden konkrétní* commit z jiné větve a aplikuj ho sem". V zadání jste nejdřív přenesli jen dokumentační commit — proto program popisovanou funkci ještě neuměl, dokumentace předběhla implementaci. Vzniká **nový commit s novým hashem**, původní zůstává tam, kde byl.
- **`git revert <hash>`** = „vytvoř **nový** commit, který ruší účinek toho starého". Historie zůstává úplná: je v ní vidět jak chyba, tak její náprava. Tím se liší od `git reset`, který by commit z historie odstranil — což je u publikované historie nebezpečné.

Rozdíl si doložíte příkazy `git log`, `git show <hash>` a `git diff`.

### Sekce 7 — vydání verze

```
git tag -a v0.2.0 -m "popis vydání"
git push origin v0.2.0
```

Přepínač `-a` vytvoří **anotovaný** tag — plnohodnotný objekt s autorem, datem a zprávou (to zadání chtělo). Bez něj vznikne jen lehký ukazatel bez metadat. Tagy se navíc **neodesílají automaticky** spolu s `git push`, musíte je poslat výslovně. Z odeslaného tagu pak na GitHubu vytvoříte release.

Finální graf historie: `git log --oneline --graph --decorate --all`.

---

## 6. Chyby, které se na cvičení objevily nejčastěji

- **Nesoulad `master` / `main`.** Lokálně `master`, na GitHubu `main` — a najednou nic nesedí. Viz poznámka na začátku: buď si GitHub přenastavte na `master`, nebo důsledně dosazujte svůj skutečný název větve.
- **„Nothing to commit"** — zapomenutý `git add`. `git status` vám to řekne.
- **Odmítnutý push kvůli oprávnění** — `origin` ukazuje na cizí repozitář místo na váš fork. `git remote -v`.
- **Odmítnutý push kvůli rozcházející se historii** — vzdálená větev má commity, které nemáte (typicky po editaci online). Řešení je `git pull`, ne force push.
- **Jeden obří commit se vším.** Zadání záměrně chce dělení do logických kroků.
- **Panika u konfliktu.** `git merge --abort` a jste zpátky před ním.
- **Ztracené změny po `git stash`** — buď jste hledali netrackované soubory, které se bez `-u` neodložily, nebo jste `pop` provedli na jiné větvi, než čekáte. `git stash list` pomůže.

---

## 7. Kam dál

- [Pro Git, 2nd Edition](https://git-scm.com/book/en/v2) — kompletní kniha o Gitu zdarma, česky i anglicky, výborná jako referenční příručka. Na dohnání látky stačí kapitoly 2 a 3.
- [Dokumentace jazyka Python](https://docs.python.org/3/)
- [Python Developer's Guide – compiler](https://devguide.python.org/internals/compiler/)
- [GNU Compiler Collection – dokumentace](https://gcc.gnu.org/onlinedocs/)

---

### Na závěr

Cílem prvního týdne nebylo naučit se příkazy nazpaměť. Šlo o to získat pocit, že vám Git nic nesebere: že se nebojíte založit větev, že konflikt není katastrofa a že rozumíte, proč se commituje po malých krocích. Pokud jste některé části nestihli, projděte si je doma a poznamenejte si konkrétní místa, kde vám to nesedí — s konkrétní otázkou vám na příštím cvičení pomůžeme mnohem líp než s „nerozumím Gitu".

---

🤖 Co-Authored-By: Claude <noreply@anthropic.com>
