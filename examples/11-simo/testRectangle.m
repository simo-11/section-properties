function [c]=testRectangle(ao)
arguments
    ao.height=100
    ao.width=100
    ao.debugLevel=0
end
%{
Test warping function fit using csv files in gen directory
%}
fp=sprintf("gen/warping-rectangle-%g-%g-*.csv",ao.height,ao.width);
list=dir(fp);
n=size(list,1);
c=cell(n,1);
models=["cubicinterp","poly44"];
ms=size(models,2);
for i=1:n
    file=sprintf("%s/%s",list(i).folder,list(i).name);
    t=readtable(file);
    o.t=t;
    o.file=file;
    for mi=1:ms
        model=models(mi);
        f=fit([t.x t.y],t.w,model);
        w=@(x,y)f(x,y).^2;
        Iw=integral2(w,0,ao.width/1000,0,ao.height/1000); %#ok<NASGU>
        es=sprintf("o.%s=Iw;",model);
        eval(es);
        es=sprintf("o.%s_fit=f;",model);
        eval(es);
    end
    c{i}=o;
end


