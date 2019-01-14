# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 17:20:42 2018

@author: richieBao-caDesign设计(cadesign.cn)
"""
from plyfile import PlyData, PlyElement
import vtk
from numpy import random
import numpy as np

'''使用VTK库的点云可视化。关于VTK详细的阐述将在pythonKSystem之后给出。可以先直接查看其官网https://www.vtk.org/获取手册、案例等信息。VTK关系较为复杂，直接通过案例代码不宜看明白之间的关系，结合作者的理论框架，可以通过图表的形式捋清楚。'''
class VtkPointCloud:
    def __init__(self, zMin=-10.0, zMax=10.0, maxNumPoints=1e10):
        self.maxNumPoints = maxNumPoints
        self.vtkPolyData = vtk.vtkPolyData()
        self.clearPoints()
        mapper = vtk.vtkPolyDataMapper() #vtkMapper映射。vtkMapper指定渲染数据和图形库中基本图元之间的联系。vtkMapper一些派生类通过LookupTable映射数据并控制图形库中相应的Actor图元的生成。一个或者多个Actor可以使用相同的Mapper。Mapper有多个参数对其控制。
        mapper.SetInputData(self.vtkPolyData)
        #mapper.SetColorModeToDefault()
        mapper.SetScalarRange(zMin, zMax) 
        mapper.SetScalarVisibility(1) #ScalarVisibility标志可以设置scalar(标量)的数据是否影响相关的Actor颜色。
        self.vtkActor = vtk.vtkActor() #Actor角色，代表渲染场景中绘制对象实体，通过参数的调节可以设置角色的位置方向、渲染特性(Property)、引用(reference)和纹理映射(Texture)等属性，并可对Actor进行缩放。
        self.vtkActor.SetMapper(mapper)  
     
    def addPoint(self, point,color):
        if self.vtkPoints.GetNumberOfPoints() < self.maxNumPoints:
            pointId = self.vtkPoints.InsertNextPoint(point[:])
            self.vtkDepth.InsertNextValue(point[2])
            self.vtkCells.InsertNextCell(1)
            self.vtkCells.InsertCellPoint(pointId)            
            
        else:
            r = random.randint(0, self.maxNumPoints)
            self.vtkPoints.SetPoint(r, point[:])
        
        self.Colors.InsertNextTuple3(color[0],color[1],color[2]) #设置每一增加点的颜色。
        self.vtkPolyData.GetPointData().SetScalars(self.Colors)
        self.vtkPolyData.Modified()
        
        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtkDepth.Modified()
        
    def clearPoints(self):
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkDepth = vtk.vtkDoubleArray()
        self.vtkDepth.SetName('DepthArray')
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepth)
        self.vtkPolyData.GetPointData().SetActiveScalars('DepthArray')

        self.Colors = vtk.vtkUnsignedCharArray()
        self.Colors.SetNumberOfComponents(3) 
        self.Colors.SetName("Colors")
        
'''读取.ply格式点云数据，作为VTK处理的数据源(Source)。关于python-plyfile库读取点云数据后内容的提取方法参考https://github.com/dranjan/python-plyfile，给出了详细的解释。'''   
def dataSource(fn):
    with open(fn, 'rb') as f:
            plydata=PlyData.read(f)
        #print(plydata,'\n',plydata['vertex'][0],'\n',plydata.elements[0].properties)        
    print(plydata) #可以通过打印，查看读取的点云数据格式，从而进一步提取所需数据。
    pointsX=plydata['vertex']['x']  #等同于plydata['vertex'][0]
    pointsY=plydata['vertex']['y']
    pointsZ=plydata['vertex']['z']
    pointsR=plydata['vertex']['red']
    pointsG=plydata['vertex']['green']
    pointsB=plydata['vertex']['blue']
    pointsXYZ=np.array([pointsX,pointsY,pointsZ])
    pointsRGB=np.array([pointsR,pointsG,pointsB])
    #[:,:1000]
    print(pointsRGB.shape,pointsXYZ.shape)
    print(pointsRGB.transpose())  
    return pointsXYZ,pointsRGB
    
if __name__ == "__main__":          
    cloudFN=r'E:\MUBENAcademy\pythonSystem\robotLab\cloudPoints\A_cloud02.ply'
    pointsXYZ,pointsRGB=dataSource(cloudFN)
    pointCloud = VtkPointCloud()
    for point,color in zip(pointsXYZ.transpose().tolist(),pointsRGB.transpose().tolist()):
        pointCloud.addPoint(point,color)
    
    pointCloud.vtkActor.GetProperty().SetPointSize(2)
    
    # Renderer 渲染器，管理光源light、照相机camera和绘制对象等位置、属性。提供世界坐标系、观察坐标系及显示坐标系之间的转换。建立玩完renderer之后，将其加入renderWindow中。
    renderer = vtk.vtkRenderer()
    renderer.AddActor(pointCloud.vtkActor) #将Actor对象添加到绘制器中。
    renderer.SetBackground(.2, .3, .4)
    renderer.ResetCamera()
    
    # Render Window 渲染窗口，管理显示设备上的窗口，为用户图形界面，可以设置渲染窗口大小，立体显示等。基类(超类/父类)为vtkRenderWindow。
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1280,720)
    renderWindow.AddRenderer(renderer)    
    
    # Interactor #创建交互器
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    
    # Begin Interaction
    renderWindow.Render()
    renderWindowInteractor.Start()