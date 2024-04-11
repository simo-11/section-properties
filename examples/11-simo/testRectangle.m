function [c]=testRectangle(ao)
arguments
    ao.height=100
    ao.width=100
    ao.models=["cubicinterp","poly44","sinhs"]
    ao.debugLevel=0
    ao.plot=1
    ao.rsquareMin=0.9
end
%{
Test warping function fit using csv files in gen directory
%}
fp=sprintf("gen/warping-rectangle-%g-%g-*.csv",ao.height,ao.width);
list=dir(fp);
n=size(list,1);
c=cell(n,1);
ms=size(ao.models,2);
H=ao.height/1000;
W=ao.width/1000;
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
            case "t1"
                ft=fittype(@(x0,y0,c1,c3,c5,x,y) ...
(x-x0).*(y-y0)+c1*x+c3*y+c5*x,...
                    coefficients={'x0','y0','c1','c3','c5'},...
                    independent={'x','y'},...
                    dependent='w');
            case "sinhs"
            if ao.debugLevel>1
                fprintf("Expected coefficient values for sinhs:\n");
                fprintf("x0=%.3g, y0=%.3g\n",...
                    W/2,H/2);
                fprintf("c1=%.3g, c3=%.3g, c5=%.3g\n",...
                    rwcn(1,H,W),rwcn(3,H,W),rwcn(5,H,W));
            end
                ft=fittype(@(x0,y0,c1,c3,c5,x,y) ...
(x-x0).*(y-y0)+...
c1*sin(pi*(y-y0)/H).*sinh(pi*(x-x0)/H)+...
c3*sin(3*pi*(y-y0)/H).*sinh(3*pi*(x-x0)/H)+...
c5*sin(5*pi*(y-y0)/H).*sinh(5*pi*(x-x0)/H),...
                    coefficients={'x0','y0','c1','c3','c5'},...
                    independent={'x','y'},...
                    dependent='w');
            otherwise
            ft=model;
        end
        if ao.debugLevel>0
            fprintf("model=%s\n",model);
        end
        [f,gof,output,warnstr,errstr,convmsg]=...
            fit([t.x t.y],t.w,ft); %#ok<ASGLU>
        w=@(x,y)f(x,y).^2;
        Iw=integral2(w,0,W,0,H);
        if ao.debugLevel>1
            disp(f);
            disp(gof);
            fprintf("Iw=%.3g\n",Iw);
        end
        if ao.plot
            s=sprintf("%s for %s",model,fn);
            figure('Name',s);
            plot(f,[t.x t.y],t.w);
            axis equal;
            ax=gca;
            dz=(max(t.w)-min(t.w))/min([max(t.x) max(t.y)]);
            ax.DataAspectRatio=[1 1 dz];
            s=sprintf("Iw=%.3g, rsquare=%.4g",Iw,gof.rsquare);
            title(s);
        end
        if (Iw>maxIw)  || (gof.rsquare<ao.rsquareMin)
            fprintf(['Model %s for file %s rejected,'...
                ' Iw=%.3g, max=%.3g'...
                ' rsquare=%.3g, min=%.3g\n'],...
                model,fn,...
                Iw,maxIw,...
                gof.rsquare,ao.rsquareMin);
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
    end
    c{i}=o;
end


