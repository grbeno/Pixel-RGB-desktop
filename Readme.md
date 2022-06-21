## Pixel elemző program

#### Magyar
###### Válasszon RGB színt az objektum felismeréshez (pl. repce virágzás, növénybetegségek).
###### 1. kepvago.py - előkészíti a képet (baseimage) RGB elemzéshez.
###### 2. pixel_1.1.py - RGB elemzés paraméterek szerint (rész képek/parcellák, R,G,B, euklideszi távolság)
### Hogyan működik?
```$ pipenv install -r requirements.txt```
###### Válassza ki a vizsgálati képet, majd jelölje ki az ellentétes sarokpontokat, hogy átlót alkossanak a képen.
```$ python kepvago.py```
```$ python pixel_1.1.py```
<br/>
#### English
###### The PixelRGB is a python solution for analysing images by their pixels.
###### Pick an RGB color then find the object (blooming, diseas etc.) on the image.
###### 1. kepvago.py - prepare the image (baseimage) for RGB analysis.
###### 2. pixel_1.1.py - RGB analysis by parameters (part images, R,G,B, euclidean distance)
### How to use
```$ pipenv install -r requirements.txt```
###### Select the image and click the points of opposite sites of a table to constitute diagonal line.
```$ python kepvago.py```
```$ python pixel_1.1.py```
<br/>
