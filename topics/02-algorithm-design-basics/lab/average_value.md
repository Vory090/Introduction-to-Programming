# Výpočet průměrné hodnoty

Navrhněte vývojový diagram algoritmu, který načte právě **pět čísel**,
průběžně je sčítá a po načtení posledního čísla vypočítá a vypíše jejich
aritmetický průměr. Diagram musí zachytit inicializaci součtu, opakované
načítání pěti hodnot, aktualizaci součtu i závěrečný výpočet.


## Pseudokód

```
NASTAV N = 5
NASTAV total = 0

VYPIŠ "Zadej N čísel"

PRO i od 1 do N
NAČTI x
total = total + x
KONEC PRO

average = total / N
VYPIŠ average
```

## Ukázková implementace v Pythonu

```python
# number of values (constant)
N = 5

total = 0

print(f"Enter {N} numbers:")

for i in range(1, N + 1):
    x = float(input(f"Value #{i}: "))
    total = total + x

average = total / N
print("Average value:", average)
```

<details>
<summary>Řešení – vývojový diagram</summary>

```mermaid
flowchart TD
    start([Start]) --> init["N = 5<br/>total = 0"]
    init --> prompt["Vypiš výzvu k zadání N čísel"]
    prompt --> setI["i = 1"]
    setI --> loop{"i <= N?"}
    loop -- ano --> read["Načti x"]
    read --> add["total = total + x"]
    add --> increment["i = i + 1"]
    increment --> loop
    loop -- ne --> average["average = total / N"]
    average --> output["Vypiš average"]
    output --> stop([Konec])
```

</details>
