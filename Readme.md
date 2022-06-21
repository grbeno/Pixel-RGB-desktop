## Pixel elemző program

#### Magyar
Válasszon RGB színt az objektum felismeréshez (pl. repce virágzás, növénybetegségek).
<br/>
***(1)*** kepvago.py - előkészíti a képet (baseimage) RGB elemzéshez.
<br/>
***(2)*** pixel_1.1.py - RGB elemzés paraméterek szerint (rész képek/parcellák, R,G,B, euklideszi távolság).
### Hogyan működik?
Töltse le a zip fájlt és másolja egy mappába.

Ha még nincs telepítve virtuális környezet, akkor pl.:

```$ pip install pipenv```

Lépjen be a választott mappába konzolon.

```$ cd <választott-mappa>```

Telepítse a szükséges könyvtárakat az alábbi paranccsal:

```$ pipenv install -r requirements.txt```

Válassza ki a vizsgálati képet, majd jelölje ki az ellentétes sarokpontokat, hogy átlót alkossanak a képen.

```$ python kepvago.py```

Töltse ki az űrlapot a megfelelő paraméterekkel.

```$ python pixel_1.1.py```

#### English
The Pixel-RGB is a python solution for analysing images by their pixels.
Pick an RGB color then find the object (blooming, diseases etc.) on the image.
<br/>
***(1)*** kepvago.py - prepare the image (baseimage) for RGB analysis.
<br/>
***(2)*** pixel_1.1.py - RGB analysis by parameters (part images, R,G,B, euclidean distance).
### How to use
Download the zip file then open your CLI.

If you have not installed virtual environment yet, then you can do:

```$ pip install pipenv```

Select your directory as current on your console.

```$ cd <selected-dir>```

Install the required librarires with the command below:

```$ pipenv install -r requirements.txt```

Select the image and click on the points of the opposite corners of the selected table to constitute a diagonal line.

```$ python kepvago.py```

Fill the form with the appropriate parameters.

```$ python pixel_1.1.py```
<br/>
