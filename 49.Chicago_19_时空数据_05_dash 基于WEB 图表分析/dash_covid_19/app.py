# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 09:56:06 2020

@author: :Richie Bao-caDesign设计(cadesign.cn).Chicago
ref: dash: https://dash-gallery.plotly.host/Portal/
"""
import pathlib,random
import os

import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

import constants
import GeospatIal_Distribution_DYnamics as gdd
import geopandas as gpd

# some color names is invalid in dash such as sienna, silver  
colors_css=[
            "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure",
            "beige", "bisque", "black", "blanchedalmond", "blue",
            "blueviolet", "brown", "burlywood", "cadetblue",
            "chartreuse", "chocolate", "coral", "cornflowerblue",
            "cornsilk", "crimson", "cyan", "darkblue", "darkcyan",
            "darkgoldenrod", "darkgray", "darkgrey", "darkgreen",
            "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange",
            "darkorchid", "darkred", "darksalmon", "darkseagreen",
            "darkslateblue", "darkslategray", "darkslategrey",
            "darkturquoise", "darkviolet", "deeppink", "deepskyblue",
            "dimgray", "dimgrey", "dodgerblue", "firebrick",
            "floralwhite", "forestgreen", "fuchsia", "gainsboro",
            "ghostwhite", "gold", "goldenrod", "gray", "grey", "green",
            "greenyellow", "honeydew", "hotpink", "indianred", "indigo",
            "ivory", "khaki", "lavender", "lavenderblush", "lawngreen",
            "lemonchiffon", "lightblue", "lightcoral", "lightcyan",
            "lightgoldenrodyellow", "lightgray", "lightgrey",
            "lightgreen", "lightpink", "lightsalmon", "lightseagreen",
            "lightskyblue", "lightslategray", "lightslategrey",
            "lightsteelblue", "lightyellow", "lime", "limegreen",
            "linen", "magenta", "maroon", "mediumaquamarine",
            "mediumblue", "mediumorchid", "mediumpurple",
            "mediumseagreen", "mediumslateblue", "mediumspringgreen",
            "mediumturquoise", "mediumvioletred", "midnightblue",
            "mintcream", "mistyrose", "moccasin", "navajowhite", "navy",
            "oldlace", "olive", "olivedrab", "orange", "orangered",
            "orchid", "palegoldenrod", "palegreen", "paleturquoise",
            "palevioletred", "papayawhip", "peachpuff", "peru", "pink",
            "plum", "powderblue", "purple", "red", "rosybrown",
            "royalblue", "rebeccapurple", "saddlebrown", "salmon",
            "sandybrown", "seagreen", "seashell",
            "skyblue", "slateblue", "slategray", "slategrey", "snow",
            "springgreen", "steelblue", "tan", "teal", "thistle", "tomato",
            "turquoise", "violet", "wheat", "white", "whitesmoke",
            "yellow", "yellowgreen"
    ]
random.shuffle(colors_css)
# app initialize
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server
app.config["suppress_callback_exceptions"] = True

# mapbox  official website https://www.mapbox.com/
mapbox_access_token = "pk.eyJ1IjoicmljaGllYmFvIiwiYSI6ImNrYjB3Y2E1MzBkY3YyenBmNmZjZDZqOTAifQ.w_BzSVgbfiApJHQielaYZg"


# Load data
APP_PATH = str(pathlib.Path("__file__").parent.resolve())
# APP_PATH=os.path.dirname(os.path.abspath("__file__"))
dataFpDic={
        "Covid-19_CasesByZipCode":os.path.join(APP_PATH,os.path.join("data",r"COVID-19_Cases__Tests__and_Deaths_by_ZIP_Code.csv")),
        
        "zip_codes":os.path.join(APP_PATH,os.path.join("data",r"Boundaries - ZIP Codes\geo_export_1a9a53ff-8090-4a1a-85ce-ac92bd036028.shp")),
   
        "populationCensus":os.path.join(APP_PATH,os.path.join("data",r"populationCensus_Project\populationCensus_Project.shp")),
        "populationCensusTif":os.path.join(APP_PATH,os.path.join("data",r"population.tif")),
   }
'''basis'''
covid19_gpd,covid19_df,covid19_zip,covid19_df_byZip=gdd.covid_19_csv2gpd(dataFpDic) 
population_quantile=gdd.populationNeighborhood(dataFpDic["populationCensus"],dataFpDic["zip_codes"],dataFpDic["populationCensusTif"])
crs_4326 = {'init' :'epsg:4326'}
population_quantile_4326=population_quantile.to_crs(crs_4326)
# population_quantile_4326_json=population_quantile_4326.geometry.to_json() 
polyg_55=population_quantile_4326.geometry.to_list()[55]
# population_quantile_4326_json=gpd.GeoSeries([polyg_55]).__geo_interface__


def get_polygon(lons, lats, color='blue'):
    if len(lons) != len(lats):
        raise ValueError('the legth of longitude list  must coincide with that of latitude')
    geojd = {"type": "FeatureCollection"}
    geojd['features'] = []
    coords = []
    for lon, lat in zip(lons, lats): 
        coords.append((lon, lat))   
    coords.append((lons[0], lats[0]))  #close the polygon  
    geojd['features'].append({ "type": "Feature",
                               "geometry": {"type": "Polygon",
                                            "coordinates": [coords] }})
    layer=dict(sourcetype = 'geojson',
             source =geojd,
             below='',  
             type = 'fill',   
             color = color,
             opacity=0.2,
             )
    return layer

# Assign color to legend
colormap = {}
for ind, formation_name in enumerate(population_quantile["idx"].unique().tolist()):
    colormap[formation_name] = constants.colors[ind]




def build_graph_title(title):
    return html.P(className="graph-title", children=title)
    
def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Img(src=app.get_asset_url("logo_programmer_a.png")),
            html.H6("时空数据——时空分布动态"),
        ],
    )    

app.layout = html.Div(
    children=[
        html.Div(
            id="top-row",
            children=[
                html.Div(
                    className="row",
                    id="top-row-header",
                    children=[
                        html.Div(
                            id="header-container",
                            children=[
                                build_banner(),
                                html.P(
                                    id="instructions",
                                    children=" 城市时空数据分析的目的，通常是探查城市区域间某一随时间变化因素之间存在的关系，"
                                    "例如全局相关性变化，LISA变化，从一分位数区域转变到另一分位数区域的概率、 时间，以及方向，亦包括各区域变化因素的稳定性确定等内容。"
                                    "本次分析所使用的python库为giddy，用于探索城市时空分布动态-Covid-19时空变化。"
                                    ,
                                ),
                                build_graph_title("区域选择-absolute dynamics"),
                                dcc.Dropdown(
                                    id="operator-select",
                                    options=[
                                        {"label": str(i), "value": str(i)}
                                        for i in population_quantile["idx"].unique().tolist()
                                    ],
                                    multi=True,
                                    value=[
                                        str(population_quantile["idx"].unique().tolist()[0]),
                                        str(population_quantile["idx"].unique().tolist()[1]),
                                    ],
                                ),
                            
                            ],
                        )
                    ],
                ),
                
                
                html.Div(
                    className="row",
                    id="top-row-graphs",
                    children=[
                        # Well map
                        html.Div(
                            id="well-map-container",
                            children=[
                                build_graph_title("Neighborhood set LIMA"),
                                dcc.RadioItems(
                                    id="mapbox-view-selector",
                                    options=[
                                        {"label": "basic", "value": "basic"},
                                        {"label": "satellite", "value": "satellite"},
                                        {"label": "outdoors", "value": "outdoors"},
                                        {
                                            "label": "satellite-street",
                                            "value": "mapbox://styles/mapbox/satellite-streets-v9",
                                        },
                                    ],
                                    value="basic",
                                ),
                                
                               
                                
                               dcc.Graph(
                                    id="well-map",
                                    figure={
                                        "layout": {
                                            "paper_bgcolor": "#192444", ##192444  #ffffff
                                            "plot_bgcolor": "#192444",  ##192444
                                        }
                                    },
                                    config={"scrollZoom": True, "displayModeBar": True},
                                    style={'height': 600},
                                ),
                            ],
                        ), 
                        ],
                        ),
                ],
                ),
                
                html.Div(
                    className="row",
                    id="bottom-row",
                    children=[
                        # Formation bar plots
                        html.Div(
                            id="global-spatial-autocorrelation",
                            className="gsa",
                            children=[
                                build_graph_title("global spatial autocorrelation for Covid-19-cases"),
                                dcc.Graph(id="global_spatial_autocorrelation"),
                            ],
                        ),
                        
                    html.Div(     
                        className="zipSup",
                        id="zip-sup",
                        style={'color': 'grey', 'fontSize': 20,'align':'left',},
                        ),
                    
                        html.Div(
                            # Selected well productions
                            id="well-production-container",
                            className="wpc",
                            children=[
                                build_graph_title("absolute dynamics"),
                                dcc.Graph(id="production-fig",
                                          style={'height': 600},
                                          ),
                            ],
                        ),
                       
                    ],
                ),          
        
        
        
        ]
            
        
   )

def sig_lnhood():
    data_df=covid19_df[['CasesWeekly','WeekStart','zipBak']]
    zipPolygon=dataFpDic["zip_codes"]
    
    caseWeekly_unstack=data_df['CasesWeekly'].unstack(level=0)
    zip_codes= gpd.read_file(zipPolygon)
    data_df_zipGPD=zip_codes.merge(caseWeekly_unstack,left_on='zip', right_on=caseWeekly_unstack.index)
    data_df_zipGPD["centroid"]=data_df_zipGPD.geometry.centroid
    
    data_df_zipGPD_fill=data_df_zipGPD.fillna(method='bfill',axis=1) 
    weeks=data_df.index.get_level_values('Week Number').unique().to_list()

    sig_lnhood,data_df_zipGPD_bfill=gdd.kendallTau(covid19_df[['CasesWeekly','WeekStart','zipBak']],population_quantile[['zip','idx', 'geometry']])
    sig_lnhood_4326=sig_lnhood.to_crs(crs_4326)
    sig_lnhood_4326["centroid"]=sig_lnhood_4326.geometry.centroid
    random.shuffle(colors_css)
    sig_lnhood_4326["color"]=[colors_css[i] for i in list(range(sig_lnhood_4326.shape[0]))]
    
    return sig_lnhood_4326,data_df_zipGPD_bfill


#significant neighborhood set LIMA for Covid-19
@app.callback(
    Output("well-map", "figure"),
    [
      # Input("operator-select", "value"),
      Input("mapbox-view-selector", "value"),
      ]
)
def generate_well_map(style):
    lons,lats= polyg_55.exterior.coords.xy
    mylayers =[]
    mylayers.append(get_polygon(lons=lons, lats=lats,  color='gold')) 

    layout = go.Layout(
        clickmode="event+select",
        dragmode="lasso",
        showlegend=True,
        autosize=True,
        hovermode="closest",
        margin=dict(l=0, r=0, t=0, b=0),
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(lat= 41.849366, lon=-87.623814),
            pitch=0,
            zoom=9,
            style=style,
        ),
        legend=dict(
            bgcolor="#1f2c56",
            orientation="h",
            font=dict(color="white"),
            x=0,
            y=0,
            yanchor="bottom",
        ),
        # mapbox_layers =mylayers,
    )
    sig_lnhood_4326,_=sig_lnhood()
    
    
    #基于本地LIMA流动性指标/Local indicator of mobility association-LIMA Neighbor set LIMA
    data=[]
    for idx in sig_lnhood_4326.idx.unique():
        df_idx=sig_lnhood_4326[sig_lnhood_4326.idx==idx]
        
        lons=df_idx.centroid.x
        lats=df_idx.centroid.y 
        
        
        new_trace = go.Scattermapbox(
                    lat=lats,
                    lon=lons,
                    mode="markers",
                    marker={"color": df_idx.color, "size": 12},
                    text=["sig_lnhood:"+"%.2f"%row.sig_lnhood+"<br>"+"region:"+str(row.idx) for idx,row in df_idx.iterrows()],
                    name=str(idx),
                    selectedpoints=None,
                    customdata=np.array([81389]),
                )
        data.append(new_trace)          

    mylayers =[]
    i=0
    for p in population_quantile_4326.geometry.to_list():
        # print(p.geom_type=='Polygon') #'MultiPolygon'
        if p.geom_type=='Polygon':
            lons,lats= p.exterior.coords.xy
            mylayers.append(get_polygon(lons=lons, lats=lats, color=colors_css[i])) #"gold"
        elif p.geom_type=='MultiPolygon':
            for mp in p:
                lons,lats= mp.exterior.coords.xy
                mylayers.append(get_polygon(lons=lons, lats=lats,  color='gold'))
        else:
            pass
        i+=1   

    layout.update(mapbox_layers =mylayers,overwrite=True)
        
    # print("_"*50)
    # print(style)
    # print({"data": data, "layout": layout})
    return {"data": data, "layout": layout}


#relative dynamics
@app.callback(
    [Output("production-fig", "figure"),
     Output("global_spatial_autocorrelation","figure"),
     Output("zip-sup","children")
     ],
    [
        # Input("well-map", "selectedData"),
        # Input("ternary-map", "selectedData"),
        # Input("form-by-bar", "selectedData"),
        Input("operator-select", "value"),
    ],
)
def generate_production_plot(op_select):
    weeksUnique,rvalArray,r_first_last=gdd.absoluteRelative_dynamics(covid19_df[['CasesWeekly','WeekStart','zipBak']])  
    _,data_df_zipGPD_bfill=sig_lnhood()
    # rvalArray_df=pd.DataFrame(rvalArray,columns=[str(col) for col in r_first_last[0]])
    rvalArray_df=pd.DataFrame(rvalArray,columns=r_first_last[0])

    ctx = dash.callback_context
    prop_id = ""
    prop_type = ""
    if ctx.triggered:
        splitted = ctx.triggered[0]["prop_id"].split(".")
        prop_id = splitted[0]
        prop_type = splitted[1]
    print("/*"*50)
    print(prop_id,prop_type)
    if prop_id == "operator-select" and prop_type == "value":
        if op_select is not None:
            # op_select_zip=rvalArray_df[["60619","60649"]]
            print("_"*10+"op_select:",op_select)
            # op_select=[(2, 3),(1,2)] #testing
            op_select=[eval(v) for v in op_select]
            op_select_zip=data_df_zipGPD_bfill[data_df_zipGPD_bfill["idx"].isin(op_select)]            
            # print(op_select_zip)
        else:
            op_select_zip=data_df_zipGPD_bfill
    
    op_select_zip_cases=op_select_zip[weeksUnique]
    rvalArray=op_select_zip_cases.to_numpy().T
    zipList=op_select_zip.zip.to_list()

    #A-relative dynamics
    layout_relativeDynamic = dict(
        xaxis=dict(title="week"), 
        yaxis=dict(title="zip code of the city of Chicago", type="log"),
        
    )
    data_relativeDynamics=[]    
    i=0
    for row in list(range(rvalArray.shape[1])):
        rvalArray_row=rvalArray.T[row]
        new_trace = dict(
            x=weeksUnique,
            y=rvalArray_row,
            name=zipList[i],
            mode="lines+markers",
            hoverinfo="x+y+name",
            marker=dict(
                symbol="hexagram-open", line={"width": "0.5"}, color=colors_css[row]
            ),
            # line=dict(shape="spline"),
            showlegend=True,
        )
        data_relativeDynamics.append(new_trace)
        i=+1
    fig_relativeDynamics={"data": data_relativeDynamics, "layout": layout_relativeDynamic}   
    
    #B-quantiles MoranI Plot
    weeks,MoransI,UpperBound,LowerBound=gdd.quantiles_MoranI_Plot(covid19_df[['CasesWeekly','WeekStart','zipBak']],dataFpDic["zip_codes"])  

    figure_GlobalSpatialAutocorrelation=dict(
        data=[
            dict(
                x=weeks,
                y=UpperBound,
                name='UpperBound',
                marker=dict(
                    color='rgb(55, 83, 109)'
                )
            ),
            dict(
                x=weeks,
                y=LowerBound,
                name='LowerBound',
                marker=dict(
                    color='rgb(55, 83, 109)'
                )
            ),
            dict(
                x=weeks,
                y=MoransI,
                name='Moran`s I',
                marker=dict(
                    color='rgb(26, 118, 255)'
                )
            )
        ],
        layout=dict(
            title='Global spatial autocorrelation for Covid-19-cases',
            showlegend=True,
            legend=dict(
                x=0,
                y=1.0
            ),
            margin=dict(l=40, r=0, t=40, b=30)
        )
    )
        
    zip_sup_text=[u'zip_sup index: "{}" corresponding zip:"{}"'.format(sub, op_select_zip[op_select_zip.idx.isin([sub])].zip.to_list()) for sub in op_select]
    
    
    return fig_relativeDynamics,figure_GlobalSpatialAutocorrelation,zip_sup_text

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)

'''
ValueError: Invalid property specified for object of type plotly.graph_objs.layout.mapbox.Layer: 'line_color'

    Valid properties:
        below
            Determines if the layer will be inserted before the
            layer with the specified ID. If omitted or set to '',
            the layer will be inserted above every existing layer.
        circle
            :class:`plotly.graph_objects.layout.mapbox.layer.Circle
            ` instance or dict with compatible properties
        color
            Sets the primary layer color. If `type` is "circle",
            color corresponds to the circle color
            (mapbox.layer.paint.circle-color) If `type` is "line",
            color corresponds to the line color
            (mapbox.layer.paint.line-color) If `type` is "fill",
            color corresponds to the fill color
            (mapbox.layer.paint.fill-color) If `type` is "symbol",
            color corresponds to the icon color
            (mapbox.layer.paint.icon-color)
        coordinates
            Sets the coordinates array contains [longitude,
            latitude] pairs for the image corners listed in
            clockwise order: top left, top right, bottom right,
            bottom left. Only has an effect for "image"
            `sourcetype`.
        fill
            :class:`plotly.graph_objects.layout.mapbox.layer.Fill`
            instance or dict with compatible properties
        line
            :class:`plotly.graph_objects.layout.mapbox.layer.Line`
            instance or dict with compatible properties
        maxzoom
            Sets the maximum zoom level (mapbox.layer.maxzoom). At
            zoom levels equal to or greater than the maxzoom, the
            layer will be hidden.
        minzoom
            Sets the minimum zoom level (mapbox.layer.minzoom). At
            zoom levels less than the minzoom, the layer will be
            hidden.
        name
            When used in a template, named items are created in the
            output figure in addition to any items the figure
            already has in this array. You can modify these items
            in the output figure by making your own item with
            `templateitemname` matching this `name` alongside your
            modifications (including `visible: false` or `enabled:
            false` to hide it). Has no effect outside of a
            template.
        opacity
            Sets the opacity of the layer. If `type` is "circle",
            opacity corresponds to the circle opacity
            (mapbox.layer.paint.circle-opacity) If `type` is
            "line", opacity corresponds to the line opacity
            (mapbox.layer.paint.line-opacity) If `type` is "fill",
            opacity corresponds to the fill opacity
            (mapbox.layer.paint.fill-opacity) If `type` is
            "symbol", opacity corresponds to the icon/text opacity
            (mapbox.layer.paint.text-opacity)
        source
            Sets the source data for this layer
            (mapbox.layer.source). When `sourcetype` is set to
            "geojson", `source` can be a URL to a GeoJSON or a
            GeoJSON object. When `sourcetype` is set to "vector" or
            "raster", `source` can be a URL or an array of tile
            URLs. When `sourcetype` is set to "image", `source` can
            be a URL to an image.
        sourceattribution
            Sets the attribution for this source.
        sourcelayer
            Specifies the layer to use from a vector tile source
            (mapbox.layer.source-layer). Required for "vector"
            source type that supports multiple layers.
        sourcetype
            Sets the source type for this layer, that is the type
            of the layer data.
        symbol
            :class:`plotly.graph_objects.layout.mapbox.layer.Symbol
            ` instance or dict with compatible properties
        templateitemname
            Used to refer to a named item in this array in the
            template. Named items from the template will be created
            even without a matching item in the input figure, but
            you can modify one by making an item with
            `templateitemname` matching its `name`, alongside your
            modifications (including `visible: false` or `enabled:
            false` to hide it). If there is no template or no
            matching item, this item will be hidden unless you
            explicitly show it with `visible: true`.
        type
            Sets the layer type, that is the how the layer data set
            in `source` will be rendered With `sourcetype` set to
            "geojson", the following values are allowed: "circle",
            "line", "fill" and "symbol". but note that "line" and
            "fill" are not compatible with Point GeoJSON
            geometries. With `sourcetype` set to "vector", the
            following values are allowed:  "circle", "line", "fill"
            and "symbol". With `sourcetype` set to "raster" or
            `*image*`, only the "raster" value is allowed.
        visible
            Determines whether this layer is displayed
'''