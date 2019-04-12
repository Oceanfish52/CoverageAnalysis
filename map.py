import pandas as pd
import numpy as np
#from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions, CategoricalColorMapper, HoverTool, BoxSelectTool,LassoSelectTool
from bokeh.plotting import gmap
from bokeh.io import curdoc

clustered_df = pd.read_csv('../files/cluster_df.csv')
# revise the table column name
clustered_df.columns = ['_'.join(col.split()).lower() for col in clustered_df.columns]
clustered_df.rename({'rsrp(all_mrs)_(dbm)':'rsrp_(dbm)'},axis=1,inplace=True)

# define the map center using lat mean and lng mean
lat_c = clustered_df['latitude'].mean()
lng_c = clustered_df['longitude'].mean()
map_options = GMapOptions(lat=lat_c, lng=lng_c, map_type="roadmap", zoom=15)

api_key = 'AIzaSyClOyZoAE2FUhhqpaY0jMH6nX2lcyBOgg4'
p = gmap(api_key, map_options, title="Bangkok",height = 600,width=1200)

source = ColumnDataSource(clustered_df[(lat_c-0.012<clustered_df['latitude'])&\
                          (lat_c+0.012>clustered_df['latitude'])&\
                          (lng_c-0.024<clustered_df['longitude'])&\
                          (lng_c+0.024>clustered_df['longitude'])])

color_mapper = CategoricalColorMapper(factors=['red','blue','green','purple','orange','darkred','darkblue'],
                 palette=['red','blue','green','purple','orange','darkred','darkblue'])

p.circle(x='latitude', y='longitude',source=source, size=1.5,color=dict(field='color', transform=color_mapper),\
        legend='cluster_id')

'''hover = HoverTool(tooltips=[('Cluster id', '@cluster_id'),
                            ('RSRP (dBm)', '@rsrp_(dbm)'),
                            ('MR count', '@mr_count'),
                            ('Number of subscribers','@number_of_subscribers')])'''

box_sel = BoxSelectTool()
lass_sel = LassoSelectTool()

#p.add_tools(hover)
p.add_tools(box_sel)
p.add_tools(lass_sel)

# define the callback function
def callback(attr,old,new):
    print('(',map_options.lat,',',map_options.lng,')')
map_options.on_change('lat',callback)
#show(p)

curdoc().add_root(p)
