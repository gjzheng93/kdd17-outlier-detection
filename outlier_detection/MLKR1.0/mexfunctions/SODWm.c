/*
 * =============================================================
 * SODW.c
  
 * input: x,a,b,w
 *    x : matrix DxN
 *    W : weight matrix NxN
 *
 * output: for i=1:N; for j=1:N; res=res+W(i,j)*(x(:,i)-x(:,j))*(x(:,i)-x(:,j))';end;
 * 
 * =============================================================
 */

/* $Revision: 1.2 $ */

#include "mex.h"
#include <string.h>

/* If you are using a compiler that equates NaN to zero, you must
 * compile this example using the flag -DNAN_EQUALS_ZERO. For 
 * example:
 *
 *     mex -DNAN_EQUALS_ZERO findnz.c  
 *
 * This will correctly define the IsNonZero macro for your
   compiler. */

#if NAN_EQUALS_ZERO
#define IsNonZero(d) ((d) != 0.0 || mxIsNaN(d))
#else
#define IsNonZero(d) ((d) != 0.0)
#endif


double square(double x) { return(x*x);}

void mexFunction(int nlhs, mxArray *plhs[],
                 int nrhs, const mxArray *prhs[])
{
  /* Declare variables. */ 

  double *X, *dummy, *v1,*v2, *C;
  int m,p,n;
  int j,i,r,c,k;
  double w;
  double * weights;  


  /* Check for proper number of input and output arguments. */    
  if (nrhs != 2) {
    mexErrMsgTxt("Exactly two input arguments required.");
  } 

  if (nlhs > 1) {
    mexErrMsgTxt("Too many output arguments.");
  }

  /* Check data type of input argument. */
  if (!(mxIsDouble(prhs[0]))) {
   mexErrMsgTxt("First argument must be of type double.");
  }
  /* Check data type of input argument. */
  if (!(mxIsDouble(prhs[1]))) {
   mexErrMsgTxt("Second argument must be of type double.");
  }

  n = mxGetN(prhs[0]);
  m = mxGetM(prhs[0]);

  /* Get the number of elements in the input argument. */
  if(n != mxGetN(prhs[1]))
    mexErrMsgTxt("Second matrix must be nxn\n");
  if(n != mxGetM(prhs[1]))
    mexErrMsgTxt("Second matrix must be nxn\n");


  /* Get the data. */
  X  = mxGetPr(prhs[0]);
  weights  = mxGetPr(prhs[1]);
	

  /* Create output matrix */
  plhs[0]=mxCreateDoubleMatrix(m,m,mxREAL);
  C=mxGetPr(plhs[0]);
  memset(C,0,sizeof(double)*m*m);
/*  dummy=new double[m];*/
  dummy=malloc(m*sizeof(double));

 /* compute outer products and sum them up */
  for(i=0;i<n;i++){
   v1=&X[(int) i*m];
   for(j=i+1;j<n;j++){
   /* Assign cols addresses */
   v2=&X[(int) j*m];
   w=2*weights[i*n+j]; /* The 2x allows us to only iterate over the upper triangular part of the matrix */
   if (w==0) continue;
   
   for(r=0;r<m;r++) dummy[r]=v1[r]-v2[r];

  k=0;	
   for(r=0;r<m;r++){
	 for(c=0;c<=r;c++) {C[k]+=dummy[r]*dummy[c]*w;k++;};
	 k+=m-r-1;
   }
  }
  }

  /* fill in lower triangular part of C */
   for(r=0;r<m;r++)
	 for(c=r+1;c<m;c++) C[c+r*m]=C[r+c*m]; 
 free(dummy);
}



