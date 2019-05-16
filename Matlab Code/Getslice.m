function s=Getslice(varargin)
t = cut_sqw(varargin{:});
g=xye(t);
s.s = g.y;
s.e = g.e;
s.p = g.x;