# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 09:41:15 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project)
reference:https://inventwithpython.com/pygame/
"""
import torch,torchvision
import random, pygame, sys,math
from pygame.locals import *
import toOnehotEncoder as ohe
import numpy as np
import phmiData2rasterBunch as phmiBunch 
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(torch.__version__)
print(torchvision.__version__)
print(device)

#栅格的高，宽等于Pytorch深度学习模型训练数据特征值shape形状
phmiRasterWidth=51
phmiRasterHeight=51
featureCellSize=1 #此处为1m，单位m。具体情况根据特征值调整

FPS = 15 #frames per second setting
CELLSIZE=15 #配置每一个单元的大小
#计算游戏窗口的大小（pixel）
WINDOWWIDTH = phmiRasterWidth*CELLSIZE 
WINDOWHEIGHT = phmiRasterHeight*CELLSIZE

#配置方法有所调整，因此下述断言assert依据可以忽略但是仍旧保留，用于相关项目的额参考
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size." # can be ignored
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size." # can be ignored

#变量名的规范化，方便程序迁移
CELLWIDTH = phmiRasterWidth
CELLHEIGHT = phmiRasterHeight

#             R    G    B   预先设置些颜色，备用。同时具有可读性
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)

BGCOLOR = BLACK

#按键操作，此次未使用
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# Amount of space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels.
# XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
# YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)
#未设置margin,但是保留语句，以备相关参考
XMARGIN=0
YMARGIN=0

#主调用程序，配置基本变量和初始化
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('phmi-interactive manipulation')
    # showStartScreen()
    while True:
        runPhmi()
        # showStoppingScreen()
    
#game循环部分    
def runPhmi():    
    # features,labels=readData(dataFpDic)
    # print(features.shape,labels.shape)
    X,pred_labels,model=readData(dataFpDic) #读取训练数据，分类输出类别和训练好的模型
    np.set_printoptions(threshold=sys.maxsize)
    # print(X[0].cpu().numpy())
    # print(X.shape,pred_labels.shape)
    # print(np.unique(X[0].cpu().numpy()))
    # print([math.floor(round(i/2)) for i in X[0].shape])
    centerCarPositionX,centerCarPositionY=[math.floor(round(i/2))-1 for i in X[0].shape] #配置car position无人车位置。此次位于栅格中心
    centerCarPostion={"x":centerCarPositionX,"y":centerCarPositionY} 
    # print(centerCarPostion)
    # landamarksPosition=
    # singleArrayTemp=X[0].cpu().numpy()
    X_np=X.cpu().numpy() #存储的值为pytorch的tensor并且位于gpu中，因此将其转换为numpy的array，并调回到cpu中
    landMarksIdx={} #存储landmarks在栅格中的位置索引，用于game的title索引。多个epoch
    # print(X_np.shape)
    for singArray_idx in range(X_np.shape[0]):        
        relativeCellCoords=np.concatenate([v.reshape(-1,1) for v in np.where(X_np[singArray_idx])],axis=1) #返回数组值索引（2 维度），作为坐标位置
        # print(relativeCellCoords)
        rCellCoordsMatrix=relativeCellCoords.reshape(X_np[singArray_idx].shape+(2,))
        # print(rCellCoordsMatrix)
        extractCoords=rCellCoordsMatrix[X_np[singArray_idx]!=-1] #仅保留待计算的类别索引值
        # print(extractCoords)
        landMarksIdx[singArray_idx]=extractCoords
    # print(landMarksIdx)
    
    #此次仅互动操作一组，可以调整索引值0为其它的值
    LM_epoch=landMarksIdx[0].tolist()
    # print(LM_epoch)    
    phmiValue=pred_labels[0] #一组特征值，对应的分类输出
    
    landMarksIdxCoords_start=[{"x":coordi[0],"y":coordi[1]} for coordi in LM_epoch] #转换成pygame操作数据格式
    
    DISPLAYSURF.fill(BGCOLOR) #配置游戏窗口背景
    drawLandmarks(landMarksIdxCoords_start) #初始化landmarks位置
    drawValue(phmiValue) #初始化phmi预测值
    LM_epoch_distances=[math.sqrt(pow(coordi[0]-centerCarPositionX,2)+pow(coordi[1]-centerCarPositionY,2)) for coordi in LM_epoch] #计算landmarks到car位置的距离。栅格单元为1m
    drawDistance(LM_epoch_distances,LM_epoch) #初始化landmarks到car位置距离显示
    #循环
    while True: # main game loop    
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT: #键盘ESC退出游戏
                terminate()    
            #键盘key部分未使用
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()    
            #鼠标点击操作
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos #获取鼠标点击的位置值
                # print(mousex,mousey)        
                clickedxy = getSpaceClicked(mousex, mousey) #返回点击像素所在的tile位置

                if clickedxy != None:
                    newLM_epoch=landmarksUpdata(LM_epoch,clickedxy) #栅格模式更新
                    # print(newLM_epoch)
                    landMarksIdxCoords=[{"x":coordi[0],"y":coordi[1]} for coordi in newLM_epoch] #转换为pygame操作格式
                    # print(landMarksIdxCoords)
                    pred_label,LMdistances=cal_X(newLM_epoch,(centerCarPositionX,centerCarPositionY),X_np,featureCellSize,model) #模式变换后的预测值，及新距离值
                    print("_"*50)
                    print("landmark changed:",clickedxy)
                    print("new prediction of Phmi:",pred_label)
                    DISPLAYSURF.fill(BGCOLOR) #更新背景，叠加显示变换后的数值
                    drawLandmarks(landMarksIdxCoords) #更新landmarks的位置
                    drawValue(pred_label) #更新预测值
                    drawDistance(LMdistances,newLM_epoch) #更新距离值
      
        drawGrid() #绘制栅格线，方便查看tile位置
        drawCar(centerCarPostion) #绘制car的位置   
        pygame.display.update() #显示更新
        FPSCLOCK.tick(FPS)

#显示landmarks到car位置的距离
def drawDistance(distances,coordis):
    for i in range(len(distances)):
        scoreSurf = BASICFONT.render('%.2f' % (distances[i]), True, WHITE)
        scoreRect = scoreSurf.get_rect()
        adj=0
        scoreRect.topleft = getLeftTopOfTile(coordis[i][0]-adj,coordis[i][1]-adj)
        DISPLAYSURF.blit(scoreSurf, scoreRect)
        
#获取tile的左上角位置像素级        
def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * CELLSIZE) + (tileX - 1)
    top = YMARGIN + (tileY * CELLSIZE) + (tileY - 1)
    return (left, top)
         
#用训练好的模型，预测调整后的pattern模式分类输出
def cal_X(newLM_epoch,centerCarPosition,X_np,featureCellSize,model):
    LMdistances=[math.sqrt(pow(coordi[0]-centerCarPosition[0],2)+pow(coordi[1]-centerCarPosition[1],2)) for coordi in newLM_epoch]
    newFeatureArray=np.full(X_np[0].shape,-1)
    # print(newFeatureArray.shape)
    for i in range(len(newLM_epoch)):
        newFeatureArray[newLM_epoch[i][0]][newLM_epoch[i][1]]=LMdistances[i]
    
    # print(newFeatureArray)
    newFeatureArray=torch.tensor(newFeatureArray,dtype=torch.float).to(device).reshape(1,newFeatureArray.shape[0],newFeatureArray.shape[1])    
    pred_label = model(newFeatureArray).argmax(dim=1).cpu().detach().numpy()
    
    return pred_label,LMdistances
        
#更新landmarks坐标        
def landmarksUpdata(LM_epoch,clickedxy):
        if list(clickedxy) in LM_epoch:
            LM_epoch.remove(list(clickedxy))
        else:
            LM_epoch.append(list(clickedxy))
            
        return LM_epoch
 
#读取训练数据，以及已经训练好的模型
def readData(dataFpDic):
    featureDicFn=dataFpDic["featureDicFn"]
    phmi_labelFn=dataFpDic["phmi_labelFn"]
    ptsVectorsFn=dataFpDic["ptsVectorsFn"]
    PATHModel=dataFpDic["PATHModelFn"]
    featureBool,targetVal=ohe.featureBoolDic(featureDicFn,phmi_labelFn,ptsVectorsFn)
    # featureBoolArray=np.array([featureBool[key]["featureBool"].astype(int) for key in featureBool.keys()])
    featureValueArray=np.array([featureBool[key]["featureDistance"].astype(int) for key in featureBool.keys()])

    features=torch.tensor(featureValueArray,dtype=torch.float) #特征值
    
    '''不同方式的分类连续数值用作输出类别'''
    # labels=torch.tensor(phmiBunch.labelsPercentile(targetVal),dtype=torch.long)
    # labels=torch.tensor(phmiBunch.labelsPercentile_extent(targetVal),dtype=torch.long)
    # labels=torch.tensor(phmiBunch.labelsPercentile_upgrade(targetVal),dtype=torch.long)
    labels=torch.tensor(phmiBunch.labels2Values(np.array(targetVal)),dtype=torch.long) #输出类别
    
    (unique, counts) = np.unique(labels, return_counts=True)
    # print((unique, counts))
    
    #因为样本输出分类数量悬殊，为了避免影响，随机调整类别数量比例至均衡，因此样本量会大量减少，需要获取更多样本。remove some values 1, reduce the impact of it.
    labelBool=labels.numpy()==0
    randomBool=np.random.choice([True, False], size=len(labels), p=[0.1, 0.9])
    labelMask=np.logical_or(labelBool,randomBool,dtype=bool)
    
    features=features[labelMask]
    labels=labels[labelMask]
    
    (unique, counts) = np.unique(labels, return_counts=True)
    # print((unique, counts))
    # print("amount:",len(labels))
    
    # print(np.unique(labels),"amount:",len(np.unique(labels)))
    
    (unique, counts) = np.unique(labels, return_counts=True)
    # print((unique, counts))
    # return features,labels

    #部分结果图像
    batch_size = 20 #20  100
    trainVStest=350 #1500   1800 #根据小批量样本量，调整训练数据集和测试数据集的划分点
    
    test_iter=ohe.data_iter(batch_size, features[trainVStest:], labels[trainVStest:])
    X,y= next(test_iter)
    
    # PATHModel=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\modelsSave\PhmiAlexNet_model.pt"    
    model = torch.load(PATHModel)   
    model.state_dict()

    X=X.to(device)    
    pred_labels = model(X).argmax(dim=1).cpu().detach().numpy()
    titles = ["True "+str(true) + '\n' + "pred"+str(pred) for true, pred in zip(y.numpy(), pred_labels)]    
    return X,pred_labels,model
    
#定义展平层，子类，继承torch.nn.Module
class FlattenLayer(torch.nn.Module):
    def __init__(self):
        super(FlattenLayer, self).__init__()
    def forward(self, x): # x shape: (batch, *, *, ...)
        return x.view(x.shape[0], -1)

#检查键盘操作，此次未使用。相关备用
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

#推出游戏
def terminate():
    pygame.quit()
    sys.exit()

#绘制网格线
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

#绘制landmarks坐标
def drawLandmarks(landmarksCoords):
    for coord in landmarksCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        LMRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, LMRect)
        LMInnerSegmentRect = pygame.Rect(x + 3, y + 3, CELLSIZE - 6, CELLSIZE - 6)
        pygame.draw.rect(DISPLAYSURF, GREEN, LMInnerSegmentRect)

#绘制无人车位置
def drawCar(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    carRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, carRect)

#绘制值
def drawValue(score):
    scoreSurf = BASICFONT.render('PHmi_reclassify: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 200, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

#pixel和tile之间的转换
def getSpaceClicked(mousex, mousey):
    # Return a tuple of two integers of the board space coordinates where
    # the mouse was clicked. (Or returns None not in any space.)
    for x in range(CELLWIDTH):
        for y in range(CELLHEIGHT):
            if mousex > x * CELLSIZE + XMARGIN and \
               mousex < (x + 1) * CELLSIZE + XMARGIN and \
               mousey > y * CELLSIZE + YMARGIN and \
               mousey < (y + 1) * CELLSIZE + YMARGIN:
                return (x, y)
    return None


if __name__ == "__main__":   
    dataFpDic={
            "featureDicFn":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\data\phmiFeature.pkl",
            "phmi_labelFn":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\data\phmi_label.pkl",
            "ptsVectorsFn":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\data\ptsVectors.pkl",
            
            "PATHModelFn":r"C:/Users/richi/omen-richiebao/omen-code/Chicago_code/modelsSave/PhmiAlexNet_model.pt",
        }
    main()