function [c]=testRectangle(ao)
arguments
    ao.height=100
    ao.width=100
    ao.models=["poly44","cubicinterp","tps"]
    ao.debugLevel=0
    ao.plot=0
    ao.rsquareMin=0.9
    ao.n="*"
end
%{
Test warping function fit using csv files in gen directory
%}
fp=sprintf("gen/warping-rectangle-%g-%g-%s.csv",...
    ao.height,ao.width,ao.n);
list=dir(fp);
n=size(list,1);
c=cell(n,1);
ms=size(ao.models,2);
H=ao.height/1000;
W=ao.width/1000;
for i=1:n
    fn=list(i).name;
    fprintf("file=%s\n",fn);
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
        fitMethod='fit';
        if startsWith(model,"sinhs")
            n=str2double(extract(model,digitsPattern));
            ft=fittype(@(x0,y0,x,y) ...
                rect_psi(x,y,x0,y0,n,W/2,H/2),...
                coefficients={'x0','y0'},...
                independent={'x','y'},...
                dependent='w');
        elseif startsWith(model,"tps")
            fitMethod='tpaps';
        else  
            ft=model;
        end
        switch fitMethod
            case 'fit'
                [f,gof,output,warnstr,errstr,convmsg]=...
                    fit([t.x t.y],t.w,ft); %#ok<ASGLU>
                if (gof.rsquare<ao.rsquareMin)
                    fprintf(['Model %s for file %s rejected,'...
                    ' rsquare=%.3g, min=%.3g\n'],...
                    model,fn,...
                    gof.rsquare,ao.rsquareMin);
                    continue;
                end                
                w=@(x,y)f(x,y).^2;
            case 'tpaps'
                if strlength(model)>3
                    pin=str2double(extractAfter(model,3));
                else
                    pin=1;
                end
                f=tpaps([t.x t.y]',t.w',pin);
                w=@(x,y)reshape(fnval(f,[x(:)';y(:)']).^2,...
                    size(x,1),[]);
        end
        Iw=integral2(w,0,W,0,H);
        fprintf("model=%s, Iw=%.3g\n",model,Iw);
        if ao.debugLevel>1
            disp(f);
            switch fitMethod
                case 'fit'
                disp(gof);
            end
        end
        if ao.plot
            s=sprintf("%s for %s",model,fn);
            figure('Name',s);
            switch fitMethod
                case 'fit'
                plot(f,[t.x t.y],t.w);
                s=sprintf("Iw=%.3g, rsquare=%.4g",Iw,gof.rsquare);
                title(s);
                case 'tpaps'
                tps_plot(f,list(i),t);
                s=sprintf("Iw=%.3g",Iw);
                title(s);
            end
            axis equal;
            ax=gca;
            dz=(max(t.w)-min(t.w))/min([max(t.x) max(t.y)]);
            ax.DataAspectRatio=[1 1 dz];
        end
        if (Iw>maxIw)
            fprintf(['Model %s for file %s rejected,'...
            ' Iw=%.3g, max=%.3g'],...
            model,fn,...
            Iw,maxIw);
            continue;
        end
        es=sprintf("o.%s_Iw=Iw;",model);
        eval(es);
        es=sprintf("o.%s_fit=f;",model);
        eval(es);
        switch fitMethod
            case 'fit'
            es=sprintf("o.%s_gof=gof;",model);
            eval(es);
            es=sprintf("o.%s_output=output;",model);
            eval(es);
        end
    end
    c{i}=o;
end


