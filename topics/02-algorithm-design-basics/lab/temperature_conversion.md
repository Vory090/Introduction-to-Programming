# Převod teploty ze stupňů Celsia

Navrhněte vývojový diagram jednoduchého **sekvenčního algoritmu**. Algoritmus
načte teplotu ve stupních Celsia, vypočítá z ní teplotu ve stupních Fahrenheita
a v kelvinech a obě získané hodnoty vypíše. Použijte vztahy:

```text
fahrenheit = celsius × 9 / 5 + 32
kelvin = celsius + 273,15
```

Program vypíše obě převedené hodnoty. Vyzkoušejte alespoň teploty `0`, `100`
a `-40` °C a před spuštěním odhadněte výsledek.

## Pseudokód

```text
NAČTI celsius
fahrenheit = celsius * 9 / 5 + 32
kelvin = celsius + 273.15
VYPIŠ fahrenheit
VYPIŠ kelvin
```

## Ukázková implementace v Pythonu

```python
celsius = float(input("Temperature in °C: "))

fahrenheit = celsius * 9 / 5 + 32
kelvin = celsius + 273.15

print("Temperature in °F:", fahrenheit)
print("Temperature in K:", kelvin)
```

## Rozšíření

Výstup zaokrouhlete na dvě desetinná místa. Potom doplňte kontrolu, která
upozorní na teplotu nižší než absolutní nula (`-273.15 °C`).

<details>
<summary>Řešení – vývojový diagram</summary>

```mermaid
flowchart TD
    start([Start]) --> read["Načti celsius"]
    read --> fahrenheit["fahrenheit = celsius × 9 / 5 + 32"]
    fahrenheit --> kelvin["kelvin = celsius + 273,15"]
    kelvin --> output["Vypiš fahrenheit a kelvin"]
    output --> stop([Konec])
```

</details>
