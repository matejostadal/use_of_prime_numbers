Využití prvočísel při šifrování dat
Bakalářská práce
Katedra Informatiky, Přírodovědecká fakulta, Univerzita Palackého v Olomouci
2023
Matěj Ošťádal

------------------------------
Příručka k elektronickým datům	
------------------------------

Obsah elektronických dat:
-------------------------

- doc/	Obsahuje text práce ve formátu PDF, vytvořený s použitím závazného stylu KI PřF UP
	v Olomouci pro závěrečné práce, včetně všech příloh, a všechny soubory potřebné
	pro bezproblémové vygenerování PDF dokumentu textu, tj. zdrojový kód textu, vložené
        obrázky, a podobně.
- docs/	Obsahuje dokumentaci jednotlivých modulů ze složky impl/. Tato dokumentace je přístupná přes soubor index.html.
- impl/ Obsahuje moduly implementující algoritmy probrané v teoretické části,
        modul obsahující uvedené metody kryptosystému RSA, a modul, ve kterém je několik příkladů použití
        implementovaných algoritmů a jejich základní testy.

- README.txt tento soubor


Požadavky pro spuštění:
-----------------------

Pro fungování programů je nutné mít nainstalovaný programovací jazyk Python verze 3.10. (nebo vyšší).
Návod ke stažení jazyku Python a konkrétní soubory k instalaci lze nalézt na webu https://www.python.org/downloads/.


Testování a použití algoritmů:
------------------------------

Pro testování algoritmů implementovaných v jednotlivých modulech doporučujeme projít modul examples.py, ve kterém jsou
všechny implementované algoritmy použity.
Nejjednodušším způsobem jejich testování je pak odkomentování jeho jednotlivých sekcí (případně jejich úprava) a spuštění tohoto modulu přes příkazovou řádku.

Libovolný modul jazyka Python lze spustit z příkazové řádky pomocí příkazu: python <modul>.py (za <modul> stačí doplnit konkrétní název).

Alternativně můžeme algoritmy z modulů (případně kompletní moduly) ze složky impl/ importovat do libovolného vlastního modulu, ve kterém je potom můžeme využívat.
Návod k importování v jazyce Python lze nalézt na webu https://docs.python.org/3/reference/import.html.
