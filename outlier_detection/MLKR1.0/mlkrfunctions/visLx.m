function [F,G]=visLx(L,X,Y)

% do vidualization
Lx=L*X;
persistent h;
try,
 if isempty(h), error('not a handle');end;
 set(h,'XDataSource',Lx(1,:),'YDataSource',Lx(2,:));
catch,
  h=scatter(Lx(1,:),Lx(2,:),20,Y,'MarkerFaceColor','flat','MarkerEdgeColor',[0,0,0]);  
end;
colorbar;
drawnow;

