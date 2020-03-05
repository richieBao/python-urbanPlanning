# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 22:08:15 2020

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

mpl.rcParams['font.sans-serif']=['SimHei'] #设置图表文字样式 'SimSun'

#读取第1组数据。读取已经处理，保存为.pkl的数据，读取后为pandas的DataFrame格式
pData=pd.read_pickle(r"F:\data_02_Chicago\parkNetwork\dataOutput\parks_fieldsExtracted.pkl")

#计算频数。（弃）
park_classFrequency=pData.park_class.value_counts()
park_classFrequencyDf=pd.DataFrame.from_dict(data=park_classFrequency.to_dict(),orient='index',columns=['parkClassFre'])  
park_classFrequencyDf['parkClass']=park_classFrequencyDf.index

#读取第2组数据
pFacilityData=pd.read_pickle(r"F:\data_02_Chicago\parkNetwork\dataOutput\parksInfo_linkFacility.pkl")

#print(park_classFrequency.values)
parkClass=[i[:-5] for i in list(park_classFrequency.index)]
parkClassFre=park_classFrequency.values.tolist()

# print(pData.head())
# print(pData.columns)
data=parkClassFre
ingredients=parkClass

#图表pie_A
def pie_a(data,ingredients):
    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute) #"{:.1f}%\n({:d} g)"
    fig, ax = plt.subplots(figsize=(30, 30), subplot_kw=dict(aspect="equal"))
    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),textprops=dict(color="w"))
    ax.legend(wedges, ingredients,
              title="公园类别",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=60, weight="bold")
    # ax.set_title("Matplotlib bakery: A pie")
    plt.show()

#图表pie_B
def pie_b(df):
    # df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
    fig = px.pie(df, values='parkClassFre', names='parkClass', title=' ',color_discrete_sequence=px.colors.sequential.RdBu)
    
    # Spectral11 = ("#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598", "#ffffbf", "#fee08b", "#fdae61", "#f46d43", "#d53e4f", "#9e0142","#fc8d59")
    # fig.update_traces(textfont_size=15,textinfo='label+percent',) #textposition='inside', textinfo='percent+label'
    fig.update_layout(
        # width=200,height=200,
        # title="Plot Title",
        # xaxis_title="x Axis Title",
        # yaxis_title="y Axis Title",
        font=dict(
            family='SimHei', #'Times New Roman'
            size=15,
            # color="#7f7f7f"
        ),
       )
    fig.show()

#计算百分比_地表覆盖
#'classi_count','cla_treeCanopy', 'cla_grassShrub','cla_bareSoil', 'cla_buildings', 'cla_roadsRailraods', 'cla_otherPavedSurfaces','cla_water',
def classificationPercent(df,classi_columns,classi_count):
    for column in classi_columns:
        df[column+"_perc"]=df[column]/df[classi_count]*100
    return df

#箱型图_A
def boxPlot_a(df):
    x_data = ['cla_treeCanopy_perc', 'cla_grassShrub_perc','cla_bareSoil_perc', 'cla_buildings_perc', 'cla_roadsRailraods_perc','cla_water_perc', 'cla_otherPavedSurfaces_perc',]
    y_data = df[x_data].values.T    
    colors = ['rgba(44, 160, 101, 0.5)', 'rgba(255, 144, 14, 0.5)','rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)','rgba(93, 164, 214, 0.5)','rgba(189, 189, 189, 0.5)']
    fig = go.Figure()    
    x_data_label=["树冠覆盖层","草地/灌木层","裸地","建筑","道路/铁路","水体","其它铺设面"]
    for xd, yd, cls in zip(x_data_label, y_data, colors):
            fig.add_trace(go.Box(
                y=yd,
                name=xd,
                boxpoints='all',
                jitter=0.5,
                whiskerwidth=0.2,
                fillcolor=cls,
                marker_size=2,
                line_width=1)
            )    
    fig.update_layout(
        title='',
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(243, 243, 243)',
            gridwidth=1,
            zerolinecolor='rgb(243, 243, 243)',
            zerolinewidth=2,
            tickfont=dict(
                family='SimHei',
                size=10,
                color='black'
                ),
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(255, 255, 255)', #paper_bgcolor='rgb(243, 243, 243)'
        plot_bgcolor='rgb(255, 255, 255)',
        showlegend=False,
        
        font=dict(
            family='SimHei', #'Times New Roman'
            size=12,
            # color="#7f7f7f"
        ),
    )    
    fig.show()

#计算百分比_冠层高
def treeHeightPercent(df,treeHeightCount_columns,treeHeightNodata_columns):
    for i in range(len(treeHeightCount_columns)):
        df[treeHeightCount_columns[i]+"_perc"]=df[treeHeightCount_columns[i]]/(df[treeHeightCount_columns[i]]+df[treeHeightNodata_columns[i]])*100
    return df

#箱型图_冠层高_A
def boxPlot_treeHeight(df):
    x_data = ['HVege_count_perc', 'MVege_count_perc', 'LVege_count_perc']
    y_data = df[x_data].values.T    
    colors = ['rgba(44, 160, 101, 0.5)', 'rgba(255, 144, 14, 0.5)','rgba(93, 164, 214, 0.5)'] # ['rgba(44, 160, 101, 0.5)', 'rgba(255, 144, 14, 0.5)','rgba(93, 164, 214, 0.5)']
    fig = go.Figure()    
    x_data_label=["高","中","低",]
    for xd, yd, cls in zip(x_data_label, y_data, colors):
            fig.add_trace(go.Box(
                y=yd,
                name=xd,
                boxpoints='all',
                jitter=0.5,
                whiskerwidth=0.2,
                fillcolor=cls,
                marker_size=2,
                line_width=1)
            )
    
    fig.update_layout(
        title='',
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(243, 243, 243)',
            gridwidth=1,
            zerolinecolor='rgb(243, 243, 243)',
            zerolinewidth=2,
            tickfont=dict(
                family='SimHei',
                size=10,
                color='black'
                ),
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(255, 255, 255)', #paper_bgcolor='rgb(243, 243, 243)'
        plot_bgcolor='rgb(255, 255, 255)',
        showlegend=False,
        
        font=dict(
            family='SimHei', #'Times New Roman'
            size=12,
            # color="#7f7f7f"
        ),
    )
    
    fig.show()

#箱型图_冠层高_B
def boxPlot_treeHeight_b(df):
    import plotly.express as px
    x_data = ['HVege_count_perc', 'MVege_count_perc', 'LVege_count_perc']
    dfStack=df[x_data].stack()
    dfStack["percID"]=x_data
    
    percID=pd.DataFrame(dfStack).index.get_level_values(1).tolist()
    fig = px.box(df, x=percID, y=dfStack, points="all",)
    fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = [0, 1, 2],
        ticktext = ['高-树木', '中-树木', '低-树木',],   
    ),
    font=dict(
            family='SimHei', #'Times New Roman'
            size=12,
           # color="#7f7f7f"
         ),
    paper_bgcolor='rgb(255, 255, 255)', #paper_bgcolor='rgb(243, 243, 243)'
    plot_bgcolor='rgb(255, 255, 255)',
    showlegend=False,
    
    yaxis=dict(
    autorange=True,
    showgrid=True,
    zeroline=True,
    dtick=5,
    gridcolor='rgb(243, 243, 243)',
    gridwidth=1,
    zerolinecolor='rgb(243, 243, 243)',
    zerolinewidth=2,
    tickfont=dict(
        family='SimHei',
        size=10,
        color='black'
        ),),
)
    fig.show()

#小提琴图—_景观指数
def LAMetrics_violin_a(df):
    # scaler = MinMaxScaler() 
    cols_to_norm=['FRAC','shapeIdx']
    df[cols_to_norm] = df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    fig = go.Figure()
    fig.add_trace(go.Violin(x=['FRAC']*len(df['FRAC']),
                            y=df['FRAC'],
                            legendgroup='FRAC', scalegroup='FRAC', name='FRAC',
                            side='negative',
                            pointpos=-1.3, # where to position points
                            line_color='rgb(149, 0, 68)',
                            showlegend=True)
             )
    fig.add_trace(go.Violin(x=['shapeIdx']*len(df['shapeIdx']),
                            y=df['shapeIdx'],
                            legendgroup='shapeIdx', scalegroup='shapeIdx', name='shapeIdx',
                            side='positive',
                            pointpos=1.35,
                            line_color='rgb(115, 116, 0)',
                            showlegend=True)
             )
    
    # update characteristics shared by all traces
    fig.update_traces(meanline_visible=True,
                      points='all', # show all points
                      jitter=0.2,  # add some jitter on points for better visibility
                      scalemode='count') #scale violin plot area with total count
    fig.update_layout(
        title_text=" ",
        violingap=0, violingroupgap=0, violinmode='overlay',
        
        # xaxis = dict(
        #     tickmode = 'array',
        #     tickvals = [0, 1, 2],
        #     # ticktext = ['高-树木', '中-树木'],   
        # ),
        font=dict(
                family='SimHei', #'Times New Roman'
                size=12,
               # color="#7f7f7f"
             ),
        paper_bgcolor='rgb(255, 255, 255)', #paper_bgcolor='rgb(243, 243, 243)'
        plot_bgcolor='rgb(255, 255, 255)',
        showlegend=False,
        
        yaxis=dict(
        autorange=True,
        showgrid=True,
        zeroline=True,
        # dtick=5,
        gridcolor='rgb(243, 243, 243)',
        # gridwidth=1,
        zerolinecolor='rgb(243, 243, 243)',
        # zerolinewidth=2,
        tickfont=dict(
            family='SimHei',
            size=10,
            color='black'
            ),),       

        )
    fig.show() 

#折线图_设施
def LinePlot_facility(df):
    # print(df.columns)
    '''
    Index(['park_no_left', 'label', 'park_class', 'location', 'acres',
       'shape_area', 'shape_leng', 'perimeter', 'geometry', 'index_right',
       'facility_n', 'facility_t', 'park', 'park_no_right', 'x_coord',
       'y_coord'],
      dtype='object')
    '''
    facilityLabelFre=df.facility_n.value_counts()
    print(facilityLabelFre.index)
    print(len(facilityLabelFre.index))
    
    #Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=facilityLabelFre.index, y=facilityLabelFre, mode='lines+markers',name='lines+markers',
                             line=dict(color='firebrick', width=1),marker_size=7
                             ))   
    fig.update_layout(
    title_text=" ",
    font=dict(
            family='SimHei', #'Times New Roman'
            size=12,
           # color="#7f7f7f"
         ),
    plot_bgcolor='rgb(240, 240, 240)',
    )    
    fig.show()

#散点分布图_地表覆盖
def categorical_scatter_jitter_SVF(df):
    from bokeh.io import show, output_file,export_svgs
    from bokeh.models import ColumnDataSource
    from bokeh.plotting import figure
    from bokeh.sampledata.commits import data
    from bokeh.transform import jitter
    from bokeh.io import output_notebook, show
    output_notebook()
    output_file("categorical_scatter_jitter_SVF.html")    
    
    # 'SVFep_min', 'SVFep_max', 'SVFep_mean','SVFep_count', 'SVFep_sum', 'SVFep_std', 'SVFep_median',
    # 'SVFep_majority', 'SVFep_minority', 'SVFep_unique', 'SVFep_range','SVFep_nodata',    
    
    # SVFFields=['SVF_mean','SVF_std', 'SVF_min', 'SVF_25%', 'SVF_50%', 'SVF_75%', 'SVF_max']
    SVFFields=['SVFep_min', 'SVFep_max', 'SVFep_mean','SVFep_std', 'SVFep_median','SVFep_majority', 'SVFep_minority', 'SVFep_range',]
    # SVFFields=['SVF_max']
    # DAYS = ['Sun', 'Sat', 'Fri', 'Thu', 'Wed', 'Tue', 'Mon']
    
    data_SVFFields=df[SVFFields]
    print(data_SVFFields.columns)
    
    dfStack=df[SVFFields].stack()
    dfStackDf=pd.DataFrame(dfStack).reset_index()
    dfStackDfAdj=dfStackDf[["level_1",0]].rename(columns={"level_1":"label",0:"value"})

    source=ColumnDataSource(dfStackDfAdj)
    
    p = figure(plot_width=2000, plot_height=500, y_range=SVFFields, x_axis_type='linear',title=" ") #Enum('linear', 'log', 'datetime', 'mercator') plot_width=2000, plot_height=500,1000/200

    p.circle(x='value', y=jitter('label', width=0.6, range=p.y_range),  source=source, alpha=0.3)        
    
    # p.xaxis.formatter.days = ['%Hh']
    p.x_range.range_padding = 0
    p.ygrid.grid_line_color = None
    
    # p.xaxis.axis_label="xaxis_name"
    # p.xaxis.axis_label_text_font_size = "25pt"
    # p.xaxis.axis_label_text_font = "SimHei"
    # p.xaxis.axis_label_text_color = "black"
    # p.axis.minor_tick_in = -3
    # p.axis.minor_tick_out = 6
    p.xaxis.major_tick_line_width = 3
    p.xaxis.major_label_text_font_size='26pt'
    p.yaxis.major_label_text_font_size='26pt'
        
    show(p)
    p.output_backend = "svg"
    export_svgs(p, filename=r"C:\Users\richi\omen-richiebao\omen_sf_paper_2020\01_ spatial structure of parks of the city of Chicago\fig\svfPlot_.svg")

    return dfStackDfAdj

'''
attributes are axis_label, axis_label_standoff, axis_label_text_align, axis_label_text_alpha, axis_label_text_baseline, axis_label_text_color, axis_label_text_font, axis_label_text_font_size, axis_label_text_font_style, axis_label_text_line_height, axis_line_alpha, axis_line_cap, axis_line_color, axis_line_dash, axis_line_dash_offset, axis_line_join, axis_line_width, bounds, fixed_location, formatter, js_event_callbacks, js_property_callbacks, level, major_label_orientation, major_label_overrides, major_label_standoff, major_label_text_align, major_label_text_alpha, major_label_text_baseline, major_label_text_color, major_label_text_font, major_label_text_font_size, major_label_text_font_style, major_label_text_line_height, major_tick_in, major_tick_line_alpha, major_tick_line_cap, major_tick_line_color, major_tick_line_dash, major_tick_line_dash_offset, major_tick_line_join, major_tick_line_width, major_tick_out, minor_tick_in, minor_tick_line_alpha, minor_tick_line_cap, minor_tick_line_color, minor_tick_line_dash, minor_tick_line_dash_offset, minor_tick_line_join, minor_tick_line_width, minor_tick_out, name, subscribed_events, tags, ticker, visible, x_range_name or y_range_name
'''

#相关热力图_结构
def heatmap_pData(df):
    import pandas as pd
    import seaborn as sns
    sns.set()
    
    # Load the brain networks example dataset
    # df = sns.load_dataset("brain_networks", header=[0, 1, 2], index_col=0)
    
    # Select a subset of the networks
    used_networks = [1, 5, 6, 7, 8, 12, 13, 17]
    # used_columns = [True,]*len(df.columns)
    
    # print(len(used_columns))
    # print(used_columns)
    # df = df.loc[:, used_columns]
    columnsList=['shapelyArea', 'shapelyLength','shapeIdx', 'FRAC', 
                 'popu_mean', 'popu_std','SVFW_mean', 'SVFW_std',
                 'SVFep_std', 'SVFep_median','SVFep_majority', 'SVFep_minority',
                 'facilityFre',
                 'HVege_mean','HVege_count','MVege_mean', 'MVege_count','LVege_mean', 'LVege_count',
                 'cla_treeCanopy', 'cla_grassShrub', 'cla_bareSoil','cla_buildings', 'cla_roadsRailraods', 'cla_otherPavedSurfaces','cla_water',
                 ]
    df=df[columnsList]
    
    # Create a categorical palette to identify the networks
    network_pal = sns.husl_palette(8, s=.45)
    network_lut = dict(zip(map(str, used_networks), network_pal))
    
    # Convert the palette to vectors that will be drawn on the side of the matrix
    networks = df.columns
    network_colors = pd.Series(networks, index=df.columns).map(network_lut)
    
    # Draw the full plot
    sns.clustermap(df.corr(), center=0, cmap="vlag",
                    row_colors=network_colors, col_colors=network_colors,
                    linewidths=.75, figsize=(13, 13))
    

if __name__=="__main__": 
    pass
    # pie_a(data,ingredients)
    # pie_b(park_classFrequencyDf)7

    '''
    classi_columns=['cla_treeCanopy', 'cla_grassShrub','cla_bareSoil', 'cla_buildings', 'cla_roadsRailraods', 'cla_otherPavedSurfaces','cla_water']
    classi_count='classi_count'
    pData_perc=classificationPercent(pData,classi_columns,classi_count)
    boxPlot_a(pData_perc)
    '''
    
    '''
    treeHeightCount_columns=['HVege_count','MVege_count','LVege_count']
    treeHeightNodata_columns=['HVege_nodata','MVege_nodata','LVege_nodata']
    treeHeightPerc=treeHeightPercent(pData,treeHeightCount_columns,treeHeightNodata_columns)
    boxPlot_treeHeight(treeHeightPerc)
    
    boxPlot_treeHeight_b(treeHeightPerc)
    '''
    
    # LAMetrics_violin_a(pData)
    
    # LinePlot_facility(pFacilityData)    
    
    # x=categorical_scatter_jitter_SVF(pData)
    
    # heatmap_pData(pData)
    