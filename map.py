import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex
import numpy as np
import pandas as pd

plt.figure(figsize=(12, 8), dpi=200)

china_m = Basemap(llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51,
                  projection='lcc', lat_1=33, lat_2=45, lon_0=100)

china_m.readshapefile('gadm36_CHN_shp/gadm36_CHN_1', 'state', drawbounds=True)
china_m.readshapefile('gadm36_TWN_shp/gadm36_TWN_0', 'taiwan', drawbounds=True)
places = china_m.state_info

df = pd.read_csv('A0101a.CSV',encoding='GBK')
new_index_list = []

for place in df['地    区']:
    place = place.replace(' ', '')
    new_index_list.append(place)
new_index = {'region': new_index_list}
new_index = pd.DataFrame(new_index)
df = df.drop(['地    区'], axis=1)
df = pd.concat([new_index, df], axis=1)
df.set_index('region', inplace=True)

df.to_csv('te.csv', index=1)

provinces = china_m.state_info
statenames = []
colors = {}
cmap = plt.cm.YlOrRd
vmax = 100000000
vmin = 3000000

for each_province in provinces:
    province_name = each_province['NL_NAME_1']
    p = province_name.split('|')
    if len(p) > 1:
        s = p[1]
    else:
        s = p[0]
    # 截取前两个字
    s = s[:2]
    # 恢复三字地名
    if s == '黑龍':
        s = '黑龙江'
    elif s == '内蒙':
        s = '内蒙古'

    statenames.append(s)
    pop = df['合计'][s]
    colors[s] = cmap(np.sqrt((pop - vmin) / (vmax - vmin)))[:3]


ax = plt.gca()
for nshape, seg in enumerate(china_m.state):
    color = rgb2hex(colors[statenames[nshape]])
    poly = Polygon(seg, facecolor=color, edgecolor=color)
    ax.add_patch(poly)

plt.show()