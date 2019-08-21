function L = mlkr(lossType, xTr,yTr,varargin)
%function L = mlkr(xTr,yTr,varargin)
%
% MLKR algorithm
% Input: 
% X : dxn input data
% Y : 1xn input labels
% 
% Optional:
%
% 'outdim' : (default=d) , output dimensionality of L, in case of a rectangular matrix
% 'Linit'  : (default PCA projection matrix), initialization of MLKR
% 'maxiter' : (default=-20), (negative numbers mean line searches, positive numbers mean function evaluations
% 'function' : (defualt []), you can provide a function of L, which is computed each iteration (e.g. to compute the validation error, or to visualize the embedding)
%
%
% copyright Jake Gardner and Kilian Q. Weinberger, 2012
%


[d,n]=size(xTr);

% just in case perform pca
[~,Lu,~]=applypca(xTr);

pars.outdim = d;
pars.Linit=Lu;
pars.maxiter=-20;
pars.function=[];
pars=extractpars(varargin,pars);   

Linit=pars.Linit(1:pars.outdim,:);
if strcmp(lossType, 'L1')
    L = minimize(Linit(:),'mlkrLossL1',pars.maxiter,xTr,yTr,pars.outdim,pars.function);
elseif strcmp(lossType, 'L2')
    L = minimize(Linit(:),'mlkrLossL2',pars.maxiter,xTr,yTr,pars.outdim,pars.function);
end
L=reshape(L,pars.outdim,d);




