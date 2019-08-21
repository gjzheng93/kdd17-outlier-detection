function [X] = rescale(X)
%function [X] = rescale(X)
% rescales data to be within [0,1]
%
%
X=bsxfun(@times,bsxfun(@minus,X,min(X,[],2)),1./max(X,[],2));

