function [c]=testRectangle(ao)
arguments
    ao.height=100
    ao.width=100
    ao.models=["cubicinterp","poly44"]
    ao.debugLevel=0
    ao.plot=1
end
%{
Test warping function fit using csv files in gen directory
%}
fp=sprintf("gen/warping-rectangle-%g-%g-*.csv",ao.height,ao.width);
list=dir(fp);
n=size(list,1);
c=cell(n,1);
ms=size(ao.models,2);
for i=1:n
    fn=list(i).name;
    file=sprintf("%s/%s",list(i).folder,fn);
    t=readtable(file);
    o.t=t;
    o.file=file;
    for mi=1:ms
        model=ao.models(mi);
        switch model
            otherwise
            ft=model;
        end
        [f,gof,output,warnstr,errstr,convmsg]=...
            fit([t.x t.y],t.w,ft); %#ok<ASGLU>
        w=@(x,y)f(x,y).^2;
        Iw=integral2(w,0,ao.width/1000,0,ao.height/1000);
        es=sprintf("o.%s=Iw;",model);
        eval(es);
        es=sprintf("o.%s_fit=f;",model);
        eval(es);
        es=sprintf("o.%s_gof=gof;",model);
        eval(es);
        es=sprintf("o.%s_output=output;",model);
        eval(es);
        if ao.plot
            s=sprintf("%s for %s",model,fn);
            figure('Name',s);
            plot(f,[t.x t.y],t.w);
            axis equal;
            ax=gca;
            dz=max(t.w)/min([max(t.x) max(t.y)]);
            ax.DataAspectRatio=[1 1 dz];
            s=sprintf("Iw=%.3g, rsquare=%.4g",Iw,gof.rsquare);
            title(s);
        end
    end
    c{i}=o;
end


