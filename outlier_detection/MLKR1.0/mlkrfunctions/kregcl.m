function [yhat] = kregcl(L,xTe,xTr,yTr)
%function [yhat] = kregcl(L,xTe,xTr,yTr)
%
% performs kernel regression
% Input:
% L : Transformation matrix (learned with MLKR)
% xTe: Test data (dxm)
% xTr: Training data (dxn)
% yTr: Training labels (1xn)
%
% Output:
% yhat: predictions (1xm
%
% copyright Kilian Q. Weinberger and Jake Gardner, 2012
% 

    N = size(xTr,2);
    n = size(xTe,2);
    d = size(xTr,1);
    
    Lxe = L * xTe;
    Lxr = L * xTr;
    
    % compute kernel
    dist = distance(Lxr,Lxe);
    Kij=exp(-dist);
    
    % normalize K
    s=1./sum(Kij,1);
    s(s==Inf)=1.0; % in case some points are too far from everything
    Kij=bsxfun(@times,Kij,s);
    
    % compute label
    yhat=yTr*Kij;
    
    
%     for i = 1:n
%         for j = 1:N
%             Kij(i,j) = exp(-dist(i,j));
%         end
%     end
%     
%     yhat = zeros(n,1);
%     for i = 1:n
%         for j = 1:N
%             yhat(i) = yhat(i) + Kij(i,j) * yTr(j);
%         end
%         yhat(i) = yhat(i) / sum(Kij(i,:));
%     end
%end

