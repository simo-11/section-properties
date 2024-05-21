function f=tps_plot(f,file,t)
% plots tpaps f using file to get nodes
% highly coupled with used data factories
    tfn=replace(file.name,"warping","triangles");
    fn=sprintf("%s/%s",file.folder,tfn);
    t2=readtable(fn);
    T=[t2.f, t2.s, t2.t]+1; % +1 to get proper indexes to coordinates in t
    TO=triangulation(T,t.x,t.y,t.w);
    trisurf(TO)
end