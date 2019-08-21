function [F,D] = mlkrLossL2(L,X,Y,outdim,fun)
%function [F,D] = mlkrLoss(L,X,Y,outdim,fun)
% Computes the mlkrLoss and gradient
% Input: 
% L : (dxd)x1 vector of the vectorized transformation matrix
% X : dxn input data
% Y : 1xn input labels
% 
% Optional:
%
% outdim : (default=d) , output dimensionality of L, in case of a rectangular matrix
% fun : a function of matrix L which is executed each iteration (e.g. to compute the validation error)
%
%
% copyright Jake Gardner and Kilian Q. Weinberger, 2012
%

    [d,N] = size(X);  
    if nargin<4,outdim=d;end;
        
    Ln = reshape(L, outdim, d);
    Lx = Ln * X;
    Kij = cmpKij(Lx);
    yhat = cmpYhat(Kij,Y);
    
    F = sum((Y-yhat').^2);
    if nargout > 1
       % Compute gradient
       S = mlkrGrad(X,Y,yhat',Kij);
       D = vec(2*Ln*S);
    end
    
    if nargin==5 && ~isempty(fun), 
        fun(reshape(L,outdim,d));
    end;
end


function M = mlkrGrad(X,Y,yhat,Kij)
    [d,N] = size(X);
     dy=bsxfun(@minus,repmat(yhat',1,N),Y); % dy_{ij} = yhat_i - y_j
    den = 1./(sum(Kij,2) - diag(Kij)); % normalization term for each yhat,  den_i = 1/sum_{j \neq i}K_{ij}
    den(den==Inf)=1/eps;
    dd=(yhat-Y)'; % dd_i = yhat_i - y_i
    W=Kij.*(bsxfun(@times,bsxfun(@times,dy,dd),den)+bsxfun(@times,bsxfun(@times,dy',dd'),den'));
    M=SODWm(X,W);    
end



function [Kij] = cmpKij(LX)
    dist = distance(LX); % get the distance^2 for each pair of instances
    Kij = exp(-dist);
end

function [yhat] = cmpYhat(Kij, Y)
    Kijd = Kij - eye(size(Kij));
    su=sum(Kijd,1);
    su(su==0)=eps;
    yhat = (sum(bsxfun(@times,Kijd,Y'),1) ./ su)';
end
