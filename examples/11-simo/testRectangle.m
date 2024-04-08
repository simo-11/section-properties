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
    if ao.debugLevel>0
        fprintf("file=%s\n",fn);
    end
    file=sprintf("%s/%s",list(i).folder,fn);
    t=readtable(file);
    if ao.debugLevel>1
        fprintf("x values: %.3g - %.3g\n",min(t.x),max(t.x));
        fprintf("y values: %.3g - %.3g\n",min(t.y),max(t.y));
        fprintf("w values: %.3g - %.3g\n",min(t.w),max(t.w));
    end
    maxIw=(max(t.x)-min(t.x))*(max(t.y)-min(t.y))*(max(t.w)-min(t.w))^2;
    o.t=t;
    o.file=file;
    for mi=1:ms
        model=ao.models(mi);
        switch model
            otherwise
            ft=model;
        end
        if ao.debugLevel>0
            fprintf("model=%s\n",model);
        end
        [f,gof,output,warnstr,errstr,convmsg]=...
            fit([t.x t.y],t.w,ft); %#ok<ASGLU>
        w=@(x,y)f(x,y).^2;
        Iw=integral2(w,0,ao.width/1000,0,ao.height/1000);
        if ao.debugLevel>1
            disp(f);
            disp(gof);
            fprintf("Iw=%.3g\n",Iw);
        end
        if Iw>maxIw
            fprintf("Model %s for file %s rejected, Iw=%.3g>%.3g\n",...
                model,fn,Iw,maxIw);
            continue;
        end
        es=sprintf("o.%s_Iw=Iw;",model);
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


