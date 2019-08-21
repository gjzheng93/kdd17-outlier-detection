

function [success] = demo(data_source, path_to_data, file_name, metric_type, data_range, list_feature, target);

success = 0;

pwd
setpaths;
install;

% load data

fid = fopen(strcat(path_to_data, file_name));
tline = fgets(fid);
tline = tline(1:end-1);
data_head = strsplit(tline, ',');
data = dlmread(strcat(path_to_data, file_name), ',', 1, 0);

list_feature_index = [];
for i = 1:length(list_feature)
    feature = list_feature(i);
    list_feature_index = [list_feature_index find(strcmp(data_head, feature));];
end

X = data(:,list_feature_index)';
Y = data(:,find(strcmp(data_head, target)))';

% Rescale data: (IMPORTANT!)
X=rescale(X);

% downsampling if needed

while size(X, 2) > 5000
    X = X(:,1:2:end);
    Y = Y(:,1:2:end);
end

% split in train / test

if strcmp(data_range, 'noOutlier')
    index_label = find(strcmp(data_head, 'label'));
    array_label = data(:,index_label);
    non_outlier = find(array_label == 0);

    xTr=X(:,non_outlier);
    yTr=Y(non_outlier);
    xTe=X(:,non_outlier);
    yTe=Y(non_outlier);
    
elseif strcmp(data_range, 'full')
    xTr=X(:,1:end);
    yTr=Y(1:end);
    xTe=X(:,1:end);
    yTe=Y(1:end);
    
end

if strcmp(metric_type, 'euclidean')
    L = eye(size(X, 1));
    metric_M = eye(size(X, 1));
    
else

    %% run MLKR (and visualize the embedding of the test data)
    
    if strcmp(metric_type, 'metricRobust')
        lossType = 'L1';
    elseif strcmp(metric_type, 'metric')
        lossType = 'L2';
    end

    fprintf('Running minimize...\n');
    tic;
    L=mlkr(lossType, xTr,yTr,'maxiter',-100,'outdim', size(X,1),'function',@(L) visLx(L,xTe,yTe));
    t=toc;
    fprintf('Training time: %2.2fs\n',t);

    metric_M =  L'*L;

end  

csvwrite(strcat('../python/pkg/', data_source, '.M.', metric_type, '.', data_range,'.conf'), metric_M);
csvwrite(strcat('../python/pkg/', data_source, '.L.', metric_type, '.', data_range,'.conf'), L);

success = 1;

%% Evaluation
% yhat=kregcl(eye(size(L)),xTe,xTr,yTr);
% rmse=sqrt(mean((yhat-yTe).^2));
% fprintf('TEST: Euclidean-RMSE: %2.2e\n',rmse);
% 
% yhat=kregcl(L,xTe,xTr,yTr);
% rmse=sqrt(mean((yhat-yTe).^2));
% fprintf('TEST: MLKR-RMSE: %2.2e\n',rmse);






