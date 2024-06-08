function I=do_cub(f,domain,cub,ao)
%
%{
f=function to evaluate
domain=struct with fields
 polyshape
 dbox
 vertices
cub cubature method
ao=argument object struct with fields
 debugLevel int 
%}
arguments
    f
    domain
    cub
    ao
end
if ao.debugLevel>3
    fprintf("cub=%s",cub);
end
switch cub
    case 'integral2'
        I=integral2(f,domain.dbox(1,1),domain.dbox(1,2),...
            domain.dbox(2,1),domain.dbox(2,2));
        return
    case 'glaubitz'
    case 'rbfcub'
        [w, cpus, Vcond , moms , res2 ,phi_str]=...
            RBF_cub_polygon_OPT(domain.polyshape,t);%#ok<ASGLU>
        if ao.debugLevel>3
            for i=1:4
                if i==4
                    sep="\n";
                else
                    sep=", ";
                end
                fprintf("cpus(%d)=%.3G%s",i,cpus(i),sep);
            end
        end    
    otherwise
        error("cub value %s is not supported\n",cub)
end
I=w'*ft;
end