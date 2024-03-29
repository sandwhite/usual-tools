% Demo for paper "Saliency Detection via Graph-Based Manifold Ranking" 
% by Chuan Yang, Lihe Zhang, Huchuan Lu, Ming-Hsuan Yang, and Xiang Ruan
% To appear in Proceedings of IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2013), Portland, June, 2013.
function result = demo()
clear;
addpath('./others/');
%%------------------------set parameters---------------------%%
theta=10; % control the edge weight 10 15
alpha=0.99;% control the balance of two items in manifold ranking cost function 0.99
spnumber=300;% superpixel number 200  300
imgRoot='./test/';% test image path
saldir='./saliencymap/';% the output path of the saliency map
supdir='./superpixels/';% the superpixel label file path
mkdir(supdir);
mkdir(saldir);
imnames=dir([imgRoot '*' 'jpg']);

for ii=1:length(imnames)   
    tic;
    
    disp(ii);
    imname=[imgRoot imnames(ii).name];
    origin_img=imread(imname);
    [O_m,O_n,k] = size(origin_img);

    [input_im,w]=removeframe(imname);% run a pre-processing to remove the image frame
    [m,n,k] = size(input_im); 
    
    %disp([m,n]);
    
%%----------------------generate superpixels--------------------%%      
    imname=[imname(1:end-4) '.bmp'];% the slic software support only the '.bmp' image
    
    %指令为‘文件名 20 200 超像素文件地址（用于指定输出位置）’，weight:20, superpixelnumber:200;
    comm=['SLICSuperpixelSegmentation' ' ' imname ' ' int2str(20) ' ' int2str(spnumber) ' ' supdir]; 
    system(comm);    
    spname=[supdir imnames(ii).name(1:end-4)  '.dat'];
    superpixels=ReadDAT([m,n],spname); % superpixel label matrix
    spnum=max(superpixels(:));% the actual superpixel number

%%----------------------design the graph model--------------------------%%
% compute the feature (mean color in lab color space) 
% for each node (superpixels)
    input_vals=reshape(input_im, m*n, k);
    rgb_vals=zeros(spnum,1,3);
    inds=cell(spnum,1);
    for i=1:spnum
        inds{i}=find(superpixels==i);
        rgb_vals(i,1,:)=mean(input_vals(inds{i},:),1);
    end
    lab_vals = colorspace('Lab<-', rgb_vals); 
    seg_vals=reshape(lab_vals,spnum,3);% feature for each superpixel
 
 % get edges
    adjloop=AdjcProcloop(superpixels,spnum);
    edges=[];
    for i=1:spnum
        indext=[];
        ind=find(adjloop(i,:)==1);
        for j=1:length(ind)
            indj=find(adjloop(ind(j),:)==1);
            indext=[indext,indj];
        end
        indext=[indext,ind];
        indext=indext((indext>i));
        indext=unique(indext);
        if(~isempty(indext))
            ed=ones(length(indext),2);
            ed(:,2)=i*ed(:,2);
            ed(:,1)=indext;
            edges=[edges;ed];
        end
    end

% compute affinity matrix
    weights = makeweights(edges,seg_vals,theta);
    W = adjacency(edges,weights,spnum);

% learn the optimal affinity matrix (eq. 3 in paper)
    dd = sum(W); D = sparse(1:spnum,1:spnum,dd); clear dd;
    optAff =(D-alpha*W)\eye(spnum); 
    mz=diag(ones(spnum,1));
    mz=~mz;
    optAff=optAff.*mz;
  
%%-----------------------------stage 1--------------------------%%
% compute the saliency value for each superpixel 
% with the top boundary as the query
    Yt=zeros(spnum,1);
    bst=unique(superpixels(1,1:n));
    Yt(bst)=1;
    bsalt=optAff*Yt;
    bsalt=(bsalt-min(bsalt(:)))/(max(bsalt(:))-min(bsalt(:)));
    bsalt=1-bsalt;
    %figure;imshow(bsalt,[]);title('bsalt');
    

% down
    Yd=zeros(spnum,1);
    bsd=unique(superpixels(m,1:n));
    Yd(bsd)=1;
    bsald=optAff*Yd;
    bsald=(bsald-min(bsald(:)))/(max(bsald(:))-min(bsald(:)));
    bsald=1-bsald;

   
% right
    Yr=zeros(spnum,1);
    bsr=unique(superpixels(1:m,1));
    Yr(bsr)=1;
    bsalr=optAff*Yr;
    bsalr=(bsalr-min(bsalr(:)))/(max(bsalr(:))-min(bsalr(:)));
    bsalr=1-bsalr;
    
    
% left
    Yl=zeros(spnum,1);
    bsl=unique(superpixels(1:m,n));
    Yl(bsl)=1;
    bsall=optAff*Yl;
    bsall=(bsall-min(bsall(:)))/(max(bsall(:))-min(bsall(:)));
    bsall=1-bsall;
   
% combine
    bsalc=(bsalt.*bsald.*bsall.*bsalr);
   
    bsalc=(bsalc-min(bsalc(:)))/(max(bsalc(:))-min(bsalc(:)));
    
    
% assign the saliency value to each pixel
     tmapstage1=zeros(m,n);
     for i=1:spnum
        tmapstage1(inds{i})=bsalc(i);
     end
     tmapstage1=(tmapstage1-min(tmapstage1(:)))/(max(tmapstage1(:))-min(tmapstage1(:)));
     %figure;imshow(tmapstage1,[]);title('test');
     
     
     mapstage1=zeros(w(1),w(2));
     mapstage1(w(3):w(4),w(5):w(6))=tmapstage1;
     
     %mapstage1 = imresize(mapstage1,[700,700],'nearest');
     
     mapstage1=uint8(mapstage1*255);  
     %outname=[saldir imnames(ii).name(1:end-4) '_stage1' '.png'];
     
     
     %imwrite(mapstage1,outname);
     %figure;imshow(mapstage1,[]);title('output_stage1 image');
%%----------------------stage2-------------------------%%
% binary with an adaptive threhold (i.e. mean of the saliency map)
    th=mean(bsalc);
    bsalc(bsalc<th)=0;
    bsalc(bsalc>=th)=1;
    
    
% compute the saliency value for each superpixel
    fsal=optAff*bsalc;    
    
% assign the saliency value to each pixel
    tmapstage2=zeros(m,n);
    for i=1:spnum
        tmapstage2(inds{i})=fsal(i);    
    end
    
    tmapstage2=(tmapstage2-min(tmapstage2(:)))/(max(tmapstage2(:))-min(tmapstage2(:)));
    
    mapstage2=zeros(w(1),w(2));
    mapstage2(w(3):w(4),w(5):w(6))=tmapstage2;
    mapstage2=uint8(tmapstage2*255);

    
    outname=[saldir imnames(ii).name(1:end-4) '_stage2' '.jpg'];   
    
    
    %[m,n,k] = size(tmapstage2); 
    %disp([m,n]);
    
    mapstage2 = imresize(mapstage2,[O_m,O_n],'nearest');
    
    imwrite(mapstage2,outname);
    %figure;imshow(mapstage2,[]);title('output_stage2 image');
    result = 1;
    toc;
end



