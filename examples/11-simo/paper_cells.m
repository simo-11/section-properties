function paper_cells(ao)
arguments
    ao.models=["poly44","cubicinterp","tps"]
    ao.cubs=["integral2","glaubitz","rbfcub"]
    ao.debugLevel=0
    ao.plot=0
    ao.scat_type='halton'
    ao.cards=[100,400,500]
    ao.rsquareMin=0.9
    ao.n="*"
end
%{
matlab run to reproduce results in paper
%}
add_lib_to_path
r{1}=testRectangle(height=100,width=100,models=ao.models,...
    cubs=ao.cubs,debug=ao.debugLevel,cards=ao.cards);
r{2}=testRectangle(height=10,width=100,models=ao.models,...
    cubs=ao.cubs,debug=ao.debugLevel,cards=ao.cards);
