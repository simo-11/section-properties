
function [t,dbox,area_domain]=define_scattered_pointset(card,...
    domain_struct,scat_type,area_domain)

if nargin < 1, card=800; end
if nargin < 2,  domain_struct=define_domain('polygon'); end
if nargin < 3, scat_type='halton'; end
if nargin < 4
    xyw=define_cub_rule(domain_struct,1,0); area_domain=sum(xyw(:,3));
end


switch scat_type
    case 'halton'
        P = haltonset(2);
    otherwise
        P = sobolset(2);
end

% bounding box
dbox=domain_struct.dbox;
xLimit=dbox(1,:);
yLimit=dbox(2,:);
area_boundingbox=diff(xLimit)*diff(yLimit);

% ratio: area(bounding box)/area(domain)
ratio=area_boundingbox/area_domain;

% computing sufficiently large pointset on [0,1] x [0,1]
card_bbox=ceil(4*ratio*card);
t0_ref = net(P,card_bbox);

% mapping sufficiently large pointset on domain bounding box
t0=[xLimit(1)+(t0_ref(:,1))*diff(xLimit) ...
    yLimit(1)+(t0_ref(:,2))*diff(yLimit)];

% extracting points on domain
in0=indomain_routine(domain_struct,t0);
in=find(in0 == 1);

% problem with cardinality: warning of failure
if length(in) < card
    fprintf('\n \t Number of points provided: %6.0f, asked for: %6.0f',...
       length(in),card )
end

t=t0(in(1:card),:);
