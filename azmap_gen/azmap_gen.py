#! /usr/bin/env python3
"""Amateur Radio azimuthal map generation script by EU1KY

   Install prerequisites before use:
       pip install scipy numpy matplotlib basemap basemap-data-hires

   Usage:
       python azmap_gen.py your_qth_locator

   Example:
       python azmap.py KO33jn
"""

import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
from PIL import Image

def toLoc(locator):
    if not isinstance(locator, str):
        raise TypeError('QTH locator must be a string')
    locator = locator.strip().upper()
    N = len(locator)
    assert 8 >= N >= 2 and N % 2 == 0, 'Maidenhead locator requires 2-8 characters, even number of characters'
    Oa = ord('A')
    lon = -180.
    lat = -90.
    lon += (ord(locator[0])-Oa)*20
    lat += (ord(locator[1])-Oa)*10
    if N >= 4:
        lon += int(locator[2])*2
        lat += int(locator[3])*1
    if N >= 6:
        lon += (ord(locator[4])-Oa) * 5./60
        lat += (ord(locator[5])-Oa) * 2.5/60
    if N >= 8:
        lon += int(locator[6]) * 5./600
        lat += int(locator[7]) * 2.5/600
    return lat, lon


def shoot(lon, lat, azimuth, maxdist=20000):
    """Shooter Function
    Original javascript on http://williams.best.vwh.net/gccalc.htm
    Translated to python by Thomas Lecocq
    """
    glat1 = lat * np.pi / 180.
    glon1 = lon * np.pi / 180.
    s = maxdist
    faz = azimuth * np.pi / 180.
 
    EPS= 0.00000000005
    if ((np.abs(np.cos(glat1))<EPS) and not (np.abs(np.sin(faz))<EPS)):
        alert("Only N-S courses are meaningful, starting at a pole!")
 
    a=6378.13
    f=1/298.257223563
    r = 1 - f
    tu = r * np.tan(glat1)
    sf = np.sin(faz)
    cf = np.cos(faz)
    if (cf==0):
        b=0.
    else:
        b=2. * np.arctan2 (tu, cf)
 
    cu = 1. / np.sqrt(1 + tu * tu)
    su = tu * cu
    sa = cu * sf
    c2a = 1 - sa * sa
    x = 1. + np.sqrt(1. + c2a * (1. / (r * r) - 1.))
    x = (x - 2.) / x
    c = 1. - x
    c = (x * x / 4. + 1.) / c
    d = (0.375 * x * x - 1.) * x
    tu = s / (r * a * c)
    y = tu
    c = y + 1

    while (np.abs (y - c) > EPS):
        sy = np.sin(y)
        cy = np.cos(y)
        cz = np.cos(b + y)
        e = 2. * cz * cz - 1.
        c = y
        x = e * cy
        y = e + e - 1.
        y = (((sy * sy * 4. - 3.) * y * cz * d / 6. + x) *
              d / 4. - cz) * sy * d + tu
 
    b = cu * cy * cf - su * sy
    c = r * np.sqrt(sa * sa + b * b)
    d = su * cy + cu * sy * cf
    glat2 = (np.arctan2(d, c) + np.pi) % (2*np.pi) - np.pi
    c = cu * cy - su * sy * cf
    x = np.arctan2(sy * sf, c)
    c = ((-3. * c2a + 4.) * f + 4.) * c2a * f / 16.
    d = ((e * cy * c + cz) * sy * c + y) * sa
    glon2 = ((glon1 + x - (1. - c) * d * f + np.pi) % (2*np.pi)) - np.pi    
 
    baz = (np.arctan2(sa, b) + np.pi) % (2 * np.pi)
 
    glon2 *= 180./np.pi
    glat2 *= 180./np.pi
    baz *= 180./np.pi
 
    return (glon2, glat2, baz)


def createmap(locator):
    lat_0, lon_0 = toLoc(locator) 
    file_to_save = "%s.png" % locator
    print("Generating map file %s, this may take some time to download a basemap image from the Internet..." % file_to_save)

    m = Basemap( projection='aeqd',
                 lat_0=lat_0,
                 lon_0=lon_0,
                 resolution='h')

    m.drawcountries(linewidth=0.1, color='#202020')

    # Fill the map with texture taken from internet
    m.shadedrelief(scale=0.2)

    # draw a dot at the center.
    xpt, ypt = m(lon_0, lat_0)
    m.plot([xpt], [ypt],'yo')

    #draw azimuths
    effects = [PathEffects.withStroke(linewidth=0.5, alpha = 0.7, foreground='y')]
    for az in range(10, 361, 10):
        lont, latt, baz = shoot(lon_0, lat_0, az, 1000)
        lon2, lat2, baz = shoot(lon_0, lat_0, az, 19000)
        xpt, ypt = m(lon2, lat2)
        m.drawgreatcircle(lont, latt, lon2, lat2, linewidth=0.2, color='red', alpha=0.7)
        #add azimuth annotations
        txt = plt.text(xpt, ypt, "%d" % az, verticalalignment = 'center', horizontalalignment='center',
                 fontsize = 7, color ='blue', alpha = 1.0, fontweight = 'bold')
        txt.set_path_effects(effects)

    plt.savefig(file_to_save, dpi=300)

    print("Generating a small map file azmap_s.jpg...")
    img = Image.open(file_to_save)
    newimg = img.crop(box=(428, 171, 428+1112, 171+1112)) # Ugly hardcode, todo: fix it
    newimg = newimg.resize((400, 400), resample = Image.LANCZOS)
    newimg = newimg.convert('RGB')
    newimg.save('azmap_s.jpg')
    print("Done")



if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python azmap.py your_qth_locator")
        sys.exit(1)
    loc = sys.argv[1]
    try:
        createmap(loc)
    except:
        import traceback
        traceback.print_exc()
