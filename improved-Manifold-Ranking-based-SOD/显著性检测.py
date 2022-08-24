# coding=utf-8
import cv2
import numpy as np
import math
import time


np.set_printoptions(threshold=np.inf)
t0 = time.time()
#导入一张图片,将图片压缩为300*300
img = cv2.imread("../origin_pic/sample1.jpg")

# cv2.imshow("img",img)
print("原始尺寸:",img.shape)



size=(300,300)
img = cv2.resize(img,(300,300))
cv2.imshow("img2",img)
print("压缩后尺寸:",img.shape)



#对压缩后的图片进行一次高斯平滑
kernel_size=(3,3)
sigma=1.5
IS=cv2.GaussianBlur(img,kernel_size,sigma)
print("IS尺寸:",IS.shape)
cv2.imshow("gaussian",IS)



'''对原始图片进行超像素分割'''
#初始化slic项,超像素平均尺寸20（默认为10),平滑因子20
slic = cv2.ximgproc.createSuperpixelSLIC(img,region_size=20,ruler = 20.0)
slic.iterate(10)     #迭代次数，越大效果越好
mask_slic = slic.getLabelContourMask() #获取Mask，超像素边缘Mask==1
label = slic.getLabels()        #获取超像素标签
number_slic = slic.getNumberOfSuperpixels()  #获取超像素数目
(m,n)=label.shape
print("m=",m)
print("n=",n)
print("超像素标签尺寸:",label.shape)
print("超像素数目:",number_slic)

'''在原图上绘制超像素边界'''
mask_inv_slic = cv2.bitwise_not(mask_slic)
img_slic = cv2.bitwise_and(img,img,mask =  mask_inv_slic)
cv2.imshow("img_slic",img_slic)


'''建立一个n*5维的矩阵'''
supmean= np.zeros((number_slic,5),dtype=np.uint64)
minx=np.zeros((number_slic,2),dtype=np.uint64)
print("超像素矩阵的类型:",supmean.dtype)
print("超像素矩阵的尺寸:",supmean.shape)

labelnum=np.zeros(number_slic)

for i in range(0,m):
    for j in range(0,n):
        supmean[label[i][j],0]=supmean[label[i][j],0]+i
        supmean[label[i][j],1]=supmean[label[i][j],1]+j
        #后面为颜色信息
        supmean[label[i][j],2]=(supmean[label[i][j],2]+np.uint64(IS[i][j][0]))
        supmean[label[i][j],3]=(supmean[label[i][j],3]+np.uint64(IS[i][j][1]))
        supmean[label[i][j],4]=(supmean[label[i][j],4]+np.uint64(IS[i][j][2]))
        labelnum[label[i][j]]=labelnum[label[i][j]]+1

for i in range(0,number_slic):
    supmean[i][0]=np.uint16(supmean[i][0]/labelnum[i])
    supmean[i][1]=np.uint16(supmean[i][1]/labelnum[i])
    supmean[i][2]=np.uint16(supmean[i][2]/labelnum[i])
    supmean[i][3]=np.uint16(supmean[i][3]/labelnum[i])
    supmean[i][4]=np.uint16(supmean[i][4]/labelnum[i])

IM=np.zeros((3,300,300), dtype=np.uint8)
#3*300*300
for i in range(0,m):
    for j in range(0,n):
        IM[0][i][j]=np.uint8(supmean[label[i][j],2])
        IM[1][i][j]=np.uint8(supmean[label[i][j], 3])
        IM[2][i][j]=np.uint8(supmean[label[i][j], 4])

print(supmean[0][1])

#supim=uint8(cat(3,IM(:,:,1),IM(:,:,2),IM(:,:,3)));
#print(IM)


#全局
supmean=supmean.astype(np.float)
dist_all=np.zeros(number_slic)
print("dist_all的尺寸:",dist_all.shape)
w0=0.1
for i in range(0,number_slic):
    for j in range(0,number_slic):
        dist_all[i]=dist_all[i]+(w0*(supmean[i][0]-supmean[j][0])**2+
                                 w0*(supmean[i][1]-supmean[j][1])**2+
                                 (supmean[i][2]-supmean[j][2])**2+
                                 (supmean[i][3]-supmean[j][3])**2+
                                 (supmean[i][4]-supmean[j][4])**2)**0.5
#归一化
dist_min=np.min(dist_all)
dist_max=np.max(dist_all)
print("all最小值:",dist_min)
print("all最大值:",dist_max)
for i in range(0,number_slic):
    dist_all[i]=(dist_all[i]-dist_min)*255/(dist_max-dist_min)
dist_all=dist_all.astype(np.uint8)
im_all=np.zeros((300,300))
print("im_allchicun:",im_all.shape)
for i in range(0,m):
    for j in range(0,n):
        im_all[i][j]=dist_all[label[i][j]]
im_all=im_all.astype(np.uint8)

#边缘
dist_edge=np.zeros(number_slic)
w0=0.1
thre=70
for i in range(0,number_slic):
    for j in range(0,number_slic):
        if supmean[j][0]<=thre or supmean[j][0]>=m-thre or supmean[j][1] <=thre or supmean[j][1]>=m-thre:
            dist_edge[i]= dist_edge[i]+(w0*(supmean[i][0]-supmean[j][0])**2+
                                        w0*(supmean[i][1]-supmean[j][1])**2+
                                        (supmean[i][2]-supmean[j][2])**2+
                                        (supmean[i][3]-supmean[j][3])**2+
                                        (supmean[i][4]-supmean[j][4])**2)**0.5

#归一化
dist_min=np.min(dist_edge)
dist_max=np.max(dist_edge)
print("edge最小值:",dist_min)
print("edge最大值:",dist_max)
for i in range(0,number_slic):
    dist_edge[i]=(dist_edge[i]-dist_min)*255/(dist_max-dist_min)
dist_edge=dist_edge.astype(np.uint8)
print(dist_edge.shape)
im_edge=np.zeros((300,300))
for i in range(0,m):
    for j in range(0,n):
        im_edge[i][j]=dist_edge[label[i][j]]
im_edge=(im_edge).astype(np.uint8)


# #===========================局部
# sa=np.ones(number_slic)
# w0=0.12
# w=0.18
# radius=20
# for i in range(0,number_slic):
#     numerator=0
#     denominator=0
#     for j in range(0,number_slic):
#         dist_ij=((supmean[i][0]-supmean[j][0])**2+(supmean[i][1]-supmean[j][1])**2)
#         if i!=j:
#             dist_local=(w0*dist_ij+(supmean[i][2]-supmean[j][2])**2+(supmean[i][3]-supmean[j][4])**2+(
#                         supmean[i][4]-supmean[j][4])**2)**0.5
#             numerator=numerator+math.exp(-w*dist_local)*dist_all[j]
#             denominator=denominator+math.exp(-w*dist_local)
#     sa[i]=numerator/denominator
# sa_max=max(sa)
# sa_min=min(sa)
# for i in range(0,number_slic):
#     sa[i]=(sa[i]-sa_min)*255/(sa_max-sa_min)
# sa=sa.astype(np.uint8)
# im_local=np.zeros((300,300))
# for i in range(0,m):
#     for j in range(0,n):
#         im_local[i][j]=sa[label[i][j]]
# im_local=im_local.astype(np.uint8)
# # =========================
t1 = time.time()
print(t1-t0)
'''对边缘显著性结果进行模糊'''
# kernel_size=(3,3)
# sigma=1.5
# new_edge=cv2.GaussianBlur(im_edge,kernel_size,sigma)
cv2.imshow("im_dege",im_edge)
# cv2.imshow("new_edge",new_edge)
cv2.waitKey(0)
cv2.destroyAllWindows()

