## Pixel elemző program

### Magyar
Válasszon RGB színt az objektum felismeréshez (pl. repce virágzás, növénybetegségek).
<br/><br/>
***(1)*** kepvago.py - előkészíti a képet (baseimage) RGB elemzéshez.
<br/>
***(2)*** pixel_1.1.py - RGB elemzés paraméterek szerint (rész képek/parcellák, R,G,B, euklideszi távolság).
### Hogyan működik?
Töltse le a zip fájlt és csomagolja ki egy mappába.

Ha még nincs telepítve virtuális környezet, akkor pl.:

```$ pip install pipenv```

Lépjen be a választott mappába konzolon:

```$ cd <választott-mappa>```

Aktiválja a virtuális környezetet:

```$ pipenv shell```

Telepítse a szükséges könyvtárakat az alábbi paranccsal:

```$ pipenv install -r requirements.txt```

Válassza ki a vizsgálati képet, majd jelölje ki az ellentétes sarokpontokat, hogy átlót alkossanak a képen:

```$ python kepvago.py```

Töltse ki az űrlapot a megfelelő paraméterekkel:

```$ python pixel.py```
##
### English
The Pixel-RGB is a python solution for analysing images by their pixels.
Pick an RGB color then the algorithm finds the object (blooming, diseases etc.) on the image.
<br/><br/>
***(1)*** kepvago.py - prepare the image (baseimage) for RGB analysis.
<br/>
***(2)*** pixel_1.1.py - RGB analysis by parameters (part images, R,G,B, euclidean distance).
### How to use?
Download and unzip the zip file then open your CLI.

If you have not installed virtual environment yet, then you can do:

```$ pip install pipenv```

Select your directory as current on your console:

```$ cd <selected-dir>```

Activate virtual environment:

```$ pipenv shell```

Install the required librarires with the command below:

```$ pipenv install -r requirements.txt```

Select the image, then mark the opposite corners to form a diagonal on the image.:

```$ python kepvago.py```

Fill the form with the appropriate parameters:

```$ python pixel.py```
<br/>
