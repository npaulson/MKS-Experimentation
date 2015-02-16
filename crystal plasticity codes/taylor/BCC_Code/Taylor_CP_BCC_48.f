C((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))
	SUBROUTINE CHECK(Q,TH,PHI,OM,ICHK)
	IMPLICIT REAL*8(A-H,O-Z)
	DIMENSION Q(3,3)
	TOL=1.0D-3
	A = DCOS(PHI)*DCOS(OM)-DSIN(PHI)*DSIN(OM)*DCOS(TH)
	B = -DSIN(OM)*DCOS(PHI)-DCOS(OM)*DSIN(PHI)*DCOS(TH)
	C = DCOS(OM)*DSIN(PHI)+DSIN(OM)*DCOS(PHI)*DCOS(TH)
	D = -DSIN(PHI)*DSIN(OM)+DCOS(PHI)*DCOS(OM)*DCOS(TH)
        IF(DABS(A-Q(1,1)).LT.TOL.AND.DABS(B-Q(2,1)).LT.TOL.
     +    AND.DABS(C-Q(1,2)).LT.TOL.AND.DABS(D-Q(2,2)).LT.TOL)ICHK=1
	RETURN
	END
C(((((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))
	SUBROUTINE CHECK1(Q,TH,PHI,OM,ICHK)
	IMPLICIT REAL*8(A-H,O-Z)
	DIMENSION Q(3,3)
	TOL=1.0D-3 
	TH  = 0.0D0
        PHI = 0.0D0
        OM  = 0.0D0
	Q(3,3) = 1.0*Q(3,3)/DABS(Q(3,3))
	TH = DACOS(Q(3,3))
	IF(DABS(Q(1,3)).GT.TOL)RETURN
	IF(DABS(Q(2,3)).GT.TOL)RETURN
	IF(DABS(Q(3,1)).GT.TOL)RETURN
	IF(DABS(Q(3,2)).GT.TOL)RETURN
	IF(Q(3,3).EQ.1.0)THEN
	   IF(DABS(Q(1,1)-Q(2,2)).GT.TOL)RETURN
	   IF(DABS(Q(1,2)+Q(2,1)).GT.TOL)RETURN
	ELSE
	   IF(DABS(Q(1,1)+Q(2,2)).GT.TOL)RETURN
	   IF(DABS(Q(1,2)-Q(2,1)).GT.TOL)RETURN
	ENDIF
	PHI = DATAN2(Q(1,2),Q(1,1))
	ICHK = 1
	RETURN
	END
C*********************************************************************
C    THIS SUBROUTINE DOES THE POLAR DECOMPOSITION F=[R][U]=[V][R] 
C    FOR THE ELASTIC DEF GRAD FSTAU AND EVALUATES THE ROTATION RSTAU
C*********************************************************************
	SUBROUTINE DECOMP(ICRYS)
cvd$r    noconcur
        INCLUDE 'commonsn48.tex'
C
	REAL*8 IC,IIC,IIIC,IU,IIU,IIIU
	DIMENSION C(3,3),CC(3,3),
     .            U(3,3),UINV(3,3)
C
C    TRANSPOSE F MATRIX, OBTAIN [C] = [FT] [F], [CC]= [C][C], FIND 
C    PRINCIPAL INVARIANTS OF MATRIX [C].
C
	      C(1,1) = FSTAU(1,1,ICRYS)*FSTAU(1,1,ICRYS) +
     &                FSTAU(2,1,ICRYS)*FSTAU(2,1,ICRYS) +
     &                FSTAU(3,1,ICRYS)*FSTAU(3,1,ICRYS)
      C(1,2) = FSTAU(1,1,ICRYS)*FSTAU(1,2,ICRYS) +
     &                FSTAU(2,1,ICRYS)*FSTAU(2,2,ICRYS) +
     &                FSTAU(3,1,ICRYS)*FSTAU(3,2,ICRYS)
      C(1,3) = FSTAU(1,1,ICRYS)*FSTAU(1,3,ICRYS) +
     &                FSTAU(2,1,ICRYS)*FSTAU(2,3,ICRYS) +
     &                FSTAU(3,1,ICRYS)*FSTAU(3,3,ICRYS)
      C(2,1) = FSTAU(1,2,ICRYS)*FSTAU(1,1,ICRYS) +
     &                FSTAU(2,2,ICRYS)*FSTAU(2,1,ICRYS) +
     &                FSTAU(3,2,ICRYS)*FSTAU(3,1,ICRYS)
      C(2,2) = FSTAU(1,2,ICRYS)*FSTAU(1,2,ICRYS) +
     &                FSTAU(2,2,ICRYS)*FSTAU(2,2,ICRYS) +
     &                FSTAU(3,2,ICRYS)*FSTAU(3,2,ICRYS)
      C(2,3) = FSTAU(1,2,ICRYS)*FSTAU(1,3,ICRYS) +
     &                FSTAU(2,2,ICRYS)*FSTAU(2,3,ICRYS) +
     &                FSTAU(3,2,ICRYS)*FSTAU(3,3,ICRYS)
      C(3,1) = FSTAU(1,3,ICRYS)*FSTAU(1,1,ICRYS) +
     &                FSTAU(2,3,ICRYS)*FSTAU(2,1,ICRYS) +
     &                FSTAU(3,3,ICRYS)*FSTAU(3,1,ICRYS)
      C(3,2) = FSTAU(1,3,ICRYS)*FSTAU(1,2,ICRYS) +
     &                FSTAU(2,3,ICRYS)*FSTAU(2,2,ICRYS) +
     &                FSTAU(3,3,ICRYS)*FSTAU(3,2,ICRYS)
      C(3,3) = FSTAU(1,3,ICRYS)*FSTAU(1,3,ICRYS) +
     &                FSTAU(2,3,ICRYS)*FSTAU(2,3,ICRYS) +
     &                FSTAU(3,3,ICRYS)*FSTAU(3,3,ICRYS)


	      CC(1,1) = C(1,1)*C(1,1) +
     &                C(1,2)*C(2,1) +
     &                C(1,3)*C(3,1)
      CC(1,2) = C(1,1)*C(1,2) +
     &                C(1,2)*C(2,2) +
     &                C(1,3)*C(3,2)
      CC(1,3) = C(1,1)*C(1,3) +
     &                C(1,2)*C(2,3) +
     &                C(1,3)*C(3,3)
      CC(2,1) = C(2,1)*C(1,1) +
     &                C(2,2)*C(2,1) +
     &                C(2,3)*C(3,1)
      CC(2,2) = C(2,1)*C(1,2) +
     &                C(2,2)*C(2,2) +
     &                C(2,3)*C(3,2)
      CC(2,3) = C(2,1)*C(1,3) +
     &                C(2,2)*C(2,3) +
     &                C(2,3)*C(3,3)
      CC(3,1) = C(3,1)*C(1,1) +
     &                C(3,2)*C(2,1) +
     &                C(3,3)*C(3,1)
      CC(3,2) = C(3,1)*C(1,2) +
     &                C(3,2)*C(2,2) +
     &                C(3,3)*C(3,2)
      CC(3,3) = C(3,1)*C(1,3) +
     &                C(3,2)*C(2,3) +
     &                C(3,3)*C(3,3)


C
	CALL INVARIANTS(C,IC,IIC,IIIC)
	CALL INVEIGEN(IC,IIC,IIIC,E1,E2,E3)
C
C    EIGEN VALUES AND INVARIANTS OF U
C
	UE1=DSQRT(E1)
	UE2=DSQRT(E2)
	UE3=DSQRT(E3)
	CALL EIGENINV(UE1,UE2,UE3,IU,IIU,IIIU)
C
C    EVALUATE COMPONENTS OF U
C
	PHI1=1.0/(IIU*(IIU*(IIU+IC)+IIC)+IIIC)
	ALP1=-(IU*IIU-IIIU)
	BETA1=(IU*IIU-IIIU)*(IIU+IC)
	GAM1=(IU*IIIC+IIIU*(IIU*(IIU+IC)+IIC))
	DO 10 J=1,3
	DO 10 I=1,3
10       U(I,J)=PHI1*(ALP1*CC(I,J)+BETA1*C(I,J)+GAM1*ONET(I,J))
C
C    EVALUATE COMPONENTS OF U INVERSE
C
	PHI2=1.0/(IIIU*IIIU*(IIIU+IU*IC)+IU*IU*(IU*IIIC+IIIU*IIC))
	ALP2=IU*(IU*IIU-IIIU)
	BETA2=-(IU*IIU-IIIU)*(IIIU+IU*IC)
	GAM2=IIU*IIIU*(IIIU+IU*IC)+IU*IU*(IIU*IIC+IIIC)
	DO 20 J=1,3
	DO 20 I=1,3
20	 UINV(I,J)=PHI2*(ALP2*CC(I,J)+BETA2*C(I,J)+GAM2*ONET(I,J))
C
C    EVALUATE [RSTAU]=[FSTAU][UINV]
C
              RSTAU(1,1,ICRYS) = FSTAU(1,1,ICRYS)*UINV(1,1) +
     &                FSTAU(1,2,ICRYS)*UINV(2,1) +
     &                FSTAU(1,3,ICRYS)*UINV(3,1)
      RSTAU(1,2,ICRYS) = FSTAU(1,1,ICRYS)*UINV(1,2) +
     &                FSTAU(1,2,ICRYS)*UINV(2,2) +
     &                FSTAU(1,3,ICRYS)*UINV(3,2)
      RSTAU(1,3,ICRYS) = FSTAU(1,1,ICRYS)*UINV(1,3) +
     &                FSTAU(1,2,ICRYS)*UINV(2,3) +
     &                FSTAU(1,3,ICRYS)*UINV(3,3)
      RSTAU(2,1,ICRYS) = FSTAU(2,1,ICRYS)*UINV(1,1) +
     &                FSTAU(2,2,ICRYS)*UINV(2,1) +
     &                FSTAU(2,3,ICRYS)*UINV(3,1)
      RSTAU(2,2,ICRYS) = FSTAU(2,1,ICRYS)*UINV(1,2) +
     &                FSTAU(2,2,ICRYS)*UINV(2,2) +
     &                FSTAU(2,3,ICRYS)*UINV(3,2)
      RSTAU(2,3,ICRYS) = FSTAU(2,1,ICRYS)*UINV(1,3) +
     &                FSTAU(2,2,ICRYS)*UINV(2,3) +
     &                FSTAU(2,3,ICRYS)*UINV(3,3)
      RSTAU(3,1,ICRYS) = FSTAU(3,1,ICRYS)*UINV(1,1) +
     &                FSTAU(3,2,ICRYS)*UINV(2,1) +
     &                FSTAU(3,3,ICRYS)*UINV(3,1)
      RSTAU(3,2,ICRYS) = FSTAU(3,1,ICRYS)*UINV(1,2) +
     &                FSTAU(3,2,ICRYS)*UINV(2,2) +
     &                FSTAU(3,3,ICRYS)*UINV(3,2)
      RSTAU(3,3,ICRYS) = FSTAU(3,1,ICRYS)*UINV(1,3) +
     &                FSTAU(3,2,ICRYS)*UINV(2,3) +
     &                FSTAU(3,3,ICRYS)*UINV(3,3)


C
	RETURN
	END
C**************************************************************
C  THIS SUBROUTINE CALCULATES THE INVARIANTS OF A 3X3 MATRIX
C**************************************************************
	SUBROUTINE INVARIANTS(C,IC,IIC,IIIC)
cvd$r   noconcur
	IMPLICIT REAL*8(A-H,O-Z)
	REAL*8 IC,IIC,IIIC
	DIMENSION C(3,3)
C
C   FOR 3 X 3 MATRICES ONLY
C
        IC=C(1,1)+C(2,2)+C(3,3)
	IIC=0.0
	DO 20 J=1,3
	DO 20 K=1,3
20	 IIC=IIC+C(J,K)*C(K,J)
	IIC=0.5*(IC**2-IIC)
	IIIC=C(1,1)*(C(2,2)*C(3,3)-C(2,3)*C(3,2))-
     .	     C(1,2)*(C(2,1)*C(3,3)-C(2,3)*C(3,1))+
     .	     C(1,3)*(C(2,1)*C(3,2)-C(2,2)*C(3,1))
	RETURN
	END
C*************************************************************
C  THIS SUBROUTINE CALCULATES THE EIGENVALUES, GIVEN THE 
C  INVARIANTS OF A 3X3 SYMMETRIC MATRIX WHOSE EIGEN VALUES ARE 
C  ALL POSITIVE. THE METHOD USED IS SOLVING THE CUBIC
C  CHARACTERISTIC EQUATION OF THE MATRIX. PAGE 157 OF NUMERICAL
C  RECIPES.
C*************************************************************
	SUBROUTINE INVEIGEN(IC,IIC,IIIC,E1,E2,E3)
	IMPLICIT REAL*8(A-H,O-Z)
	REAL*8 IC,IIC,IIIC
	IF(IC.EQ.3.0D0.AND.IIC.EQ.3.0D0.AND.IIIC.EQ.1.0D0)THEN
	  E1=1.0D0
	  E2=1.0D0
	  E3=1.0D0
	  RETURN
	ENDIF
C
C  REFORMULATE THE EQUATION INTERMS OF (E-1) AS UNKNOWN
C
	A1=-(3.0-IC)
 	A2=-(3.0-2.0*IC+IIC)
	A3=-(1.0-IC+IIC-IIIC)
	CALL CUBIC(A1,A2,A3,E1,E2,E3)
	E1=1.0+E1
	E2=1.0+E2
	E3=1.0+E3
	RETURN
	END
C******************************************************************
C   THIS SUBROUTINE SOLVES A CUBIC EQUATION:
C   X^3 = A1*X^2 +A2*X + A3
C******************************************************************
	SUBROUTINE CUBIC(A1,A2,A3,X1,X2,X3)
	IMPLICIT REAL*8(A-H,O-Z)
	Q = (A1*A1)/3.0+A2
	R = (2.0*A1*A1*A1+9.0*A1*A2+27.0*A3)/27.0
	S=2.0*DSQRT(Q/3.0)
	IF(S.EQ.0.0)THEN
	  X1=0.0
	  X2=0.0
	  X3=0.0
	ELSE
	  XARG=4.0*R/(S*S*S)
	  IF(ABS(XARG).GT.1.0D0)XARG=1.0D0
	  THETA=(1./3.)*DACOS(XARG)
	  PI=DACOS(-1.0D0)
	  X1=S*DCOS(THETA)
	  X2=S*DCOS(THETA-2.*PI/3.)
	  X3=S*DCOS(THETA+2.*PI/3.)
	ENDIF
	AA=A1/3.0
	X1=X1+AA
	X2=X2+AA
	X3=X3+AA
	RETURN
	END
C*******************************************************************
C   THIS SUBROUTINE FINDS THE INVARIANTS GIVEN THE EIGEN VALUES
C*******************************************************************
	SUBROUTINE EIGENINV(E1,E2,E3,IU,IIU,IIIU)
	IMPLICIT REAL*8(A-H,O-Z)
	REAL*8 IU,IIU,IIIU
	IU = E1 + E2 + E3
	IIU = E1*E2 + E2*E3 + E3*E1
	IIIU = E1*E2*E3
	RETURN
	END
C((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))
	SUBROUTINE DEFGRAD(ICRYS)
C
C  THIS SUBROUTINE PROVIDES THE DEFORMATION GRADIENT TENSOR FTAU AT
C  THE END THE CURRENT TIME STEP
C 
	INCLUDE 'commonsn48.tex'
        DIMENSION FSB(3,3),FSB1(3,3),TMP1(3,3),ROT(3,3)
  	FTTAU(1,1) = ONET(1,1)
	FTTAU(1,2) = ONET(1,2)
	FTTAU(1,3) = ONET(1,3)
	FTTAU(2,1) = ONET(2,1)
	FTTAU(2,2) = ONET(2,2)
	FTTAU(2,3) = ONET(2,3)
	FTTAU(3,1) = ONET(3,1)
	FTTAU(3,2) = ONET(3,2)
	FTTAU(3,3) = ONET(3,3)
C
C  SIMPLE SHEAR
C
        IF(LFLAG.EQ.1)THEN
          FTTAU(1,3) = EDOT*TAU
C
C ISOCHORIC UNIAXIAL TENSION OR COMPRESSION
C
	ELSE IF(LFLAG.EQ.2)THEN
	  FTTAU(2,2) = DEXP(-EDOT*TAU/2.0)
          FTTAU(3,3) = DEXP(EDOT*TAU)
          FTTAU(1,1) = FTTAU(2,2)
C
CC MODIFIED DIPEN PATEL

	ELSE IF(LFLAG.EQ.555)THEN
	  FTTAU(1,1) = DEXP(-EDOT*TAU)
          FTTAU(3,3) = DEXP(EDOT*TAU)


CC END DIPEN PATEL
C ISOCHORIC PLANE STRAIN TENSION OR COMPRESSION
C 
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
cc	ELSE IF(LFLAG.EQ.3)THEN
cc		DFACT=DSQRT(2+DSIN(2*FTHETA))
cc
cc        FTTAU(1,1) = DEXP((DCOS(FTHETA))*(-EDOT*TAU)/DFACT)
cc		FTTAU(2,2) = DEXP((DSIN(FTHETA))*(-EDOT*TAU)/DFACT)
cc	    FTTAU(3,3) = DEXP((DCOS(FTHETA)+DSIN(FTHETA))*(EDOT*TAU)/DFACT)
	
	ELSE IF(LFLAG.EQ.3)THEN

c	Loading in 1	 
	FTTAU(1,1) = DEXP(DSQRT(TWO/THREE)*DCOS(FTHETA-PI/3)*(-EDOT*TAU))
	FTTAU(2,2) = DEXP(DSQRT(TWO/THREE)*DCOS(FTHETA+PI/3)*(-EDOT*TAU))
	FTTAU(3,3) = DEXP(DSQRT(TWO/THREE)*(DCOS(FTHETA)*(EDOT*TAU)))

c	Loading in 3
c	FTTAU(3,3) = DEXP(DSQRT(TWO/THREE)*DCOS(FTHETA-PI/3)*(-EDOT*TAU))
c	FTTAU(1,1) = DEXP(DSQRT(TWO/THREE)*DCOS(FTHETA+PI/3)*(-EDOT*TAU))
c	FTTAU(2,2) = DEXP(DSQRT(TWO/THREE)*(DCOS(FTHETA)*(EDOT*TAU)))

c	Loading in 2
c	FTTAU(2,2) = DEXP(DSQRT(TWO/THREE)*DCOS(FTHETA-PI/3)*(-EDOT*TAU))
c	FTTAU(3,3) = DEXP(DSQRT(TWO/THREE)*DCOS(FTHETA+PI/3)*(-EDOT*TAU))
c	FTTAU(1,1) = DEXP(DSQRT(TWO/THREE)*(DCOS(FTHETA)*(EDOT*TAU)))

CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

c       WRITE(*,*) FTTAU(1,1), FTTAU(2,2), FTTAU(3,3)
	ELSE IF(LFLAG.EQ.4)THEN
          FTTAU(3,3) = DEXP(-(1-QFAC)*EDOT*TAU)
          FTTAU(2,2) = DEXP(-QFAC*EDOT*TAU)
          FTTAU(1,1) = DEXP(EDOT*TAU)
	ELSE IF(LFLAG.EQ.55)THEN
		FTTAU(1,1) =0.5*(DEXP(EDOT*TAU)+DEXP(-EDOT*TAU))
          FTTAU(1,3) =0.5*(DEXP(EDOT*TAU)-DEXP(-EDOT*TAU))
		FTTAU(3,1) =FTTAU(1,3)
		FTTAU(3,3) = FTTAU(1,1)
		FTTAU(2,2) = 1.0
		FTTAU(1,2) = 0.0
		FTTAU(2,1)=  0.0
		FTTAU(2,3)=  0.0
		FTTAU(3,2)=  0.0
C  ROTATIONS
	ELSE IF(LFLAG.EQ.66)THEN
		FTTAU(1,1) = COS(EDOT*TAU)
		FTTAU(1,2) = 0
		FTTAU(1,3) = -SIN(EDOT*TAU)
		FTTAU(2,1) = 0
		FTTAU(2,2) = 1
		FTTAU(2,3) = 0
		FTTAU(3,1) = -FTTAU(1,3)
		FTTAU(3,2) = 0
		FTTAU(3,3) = FTTAU(1,1)
	ELSE IF(LFLAG.EQ.77)THEN
		FTTAU(2,2) = COS(EDOT*TAU)
          FTTAU(2,3) = -SIN(EDOT*TAU)
		FTTAU(3,2) = -FTTAU(1,3)
		FTTAU(3,3) = FTTAU(1,1)
	ELSE IF(LFLAG.EQ.15)THEN
	  FTTAU(2,2) = DEXP(-EDOT*TAU/4.0)
        FTTAU(3,3) = DEXP(EDOT*TAU)
        FTTAU(1,1) = DEXP(-3*EDOT*TAU/4)
	ENDIF
C  ASSYMETRIC SHEAR
C
        IF(LFLAG.EQ.5)THEN
          FTTAU(1,3) = EDOT*TAU
	ENDIF
       ALPHAR = ALPHA*PI/180.0
       ROT(1,1) = DCOS(ALPHAR)
       ROT(1,2) = DSIN(ALPHAR)
       ROT(1,3) = 0.0
       ROT(2,1) = -ROT(1,2)
       ROT(2,2) = ROT(1,1)
       ROT(2,3) = 0.0
       ROT(3,1) = 0.0
       ROT(3,2) = 0.0
       ROT(3,3) = 1.0
       DO 10 I=1,3
       DO 10 J=1,3
        TMP1(I,J)=0.0
        DO 10 K = 1,3
10      TMP1(I,J)=TMP1(I,J)+ROT(I,K)*FTTAU(K,J)
       DO 20 I=1,3
       DO 20 J=1,3
        FTTAU(I,J)=0.0
        DO 20 K=1,3
20      FTTAU(I,J)=FTTAU(I,J)+TMP1(I,K)*ROT(J,K)
C        WRITE(*,*)'fttau'
C        WRITE(*,*)((fttau(i,j),j=1,3),i=1,3)
      
C
C
      FTAU(1,1) = FTTAU(1,1)*FT(1,1) +
     &                FTTAU(1,2)*FT(2,1) +
     &                FTTAU(1,3)*FT(3,1)
      FTAU(1,2) = FTTAU(1,1)*FT(1,2) +
     &                FTTAU(1,2)*FT(2,2) +
     &                FTTAU(1,3)*FT(3,2)
      FTAU(1,3) = FTTAU(1,1)*FT(1,3) +
     &                FTTAU(1,2)*FT(2,3) +
     &                FTTAU(1,3)*FT(3,3)
      FTAU(2,1) = FTTAU(2,1)*FT(1,1) +
     &                FTTAU(2,2)*FT(2,1) +
     &                FTTAU(2,3)*FT(3,1)
      FTAU(2,2) = FTTAU(2,1)*FT(1,2) +
     &                FTTAU(2,2)*FT(2,2) +
     &                FTTAU(2,3)*FT(3,2)
      FTAU(2,3) = FTTAU(2,1)*FT(1,3) +
     &                FTTAU(2,2)*FT(2,3) +
     &                FTTAU(2,3)*FT(3,3)
      FTAU(3,1) = FTTAU(3,1)*FT(1,1) +
     &                FTTAU(3,2)*FT(2,1) +
     &                FTTAU(3,3)*FT(3,1)
      FTAU(3,2) = FTTAU(3,1)*FT(1,2) +
     &                FTTAU(3,2)*FT(2,2) +
     &                FTTAU(3,3)*FT(3,2)
      FTAU(3,3) = FTTAU(3,1)*FT(1,3) +
     &                FTTAU(3,2)*FT(2,3) +
     &                FTTAU(3,3)*FT(3,3)


	RETURN
	END	  
C(((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))
        SUBROUTINE EULANG(ICRYS)
cvd$r   noconcur
        INCLUDE 'commonsn48.tex'
        DIMENSION Q(3,3)
C 
	SMALL=1.0D-6
C
              Q(1,1) = RSTAU(1,1,ICRYS)*QMAT(1,1,ICRYS) +
     &                RSTAU(1,2,ICRYS)*QMAT(2,1,ICRYS) +
     &                RSTAU(1,3,ICRYS)*QMAT(3,1,ICRYS)
      Q(1,2) = RSTAU(1,1,ICRYS)*QMAT(1,2,ICRYS) +
     &                RSTAU(1,2,ICRYS)*QMAT(2,2,ICRYS) +
     &                RSTAU(1,3,ICRYS)*QMAT(3,2,ICRYS)
      Q(1,3) = RSTAU(1,1,ICRYS)*QMAT(1,3,ICRYS) +
     &                RSTAU(1,2,ICRYS)*QMAT(2,3,ICRYS) +
     &                RSTAU(1,3,ICRYS)*QMAT(3,3,ICRYS)
      Q(2,1) = RSTAU(2,1,ICRYS)*QMAT(1,1,ICRYS) +
     &                RSTAU(2,2,ICRYS)*QMAT(2,1,ICRYS) +
     &                RSTAU(2,3,ICRYS)*QMAT(3,1,ICRYS)
      Q(2,2) = RSTAU(2,1,ICRYS)*QMAT(1,2,ICRYS) +
     &                RSTAU(2,2,ICRYS)*QMAT(2,2,ICRYS) +
     &                RSTAU(2,3,ICRYS)*QMAT(3,2,ICRYS)
      Q(2,3) = RSTAU(2,1,ICRYS)*QMAT(1,3,ICRYS) +
     &                RSTAU(2,2,ICRYS)*QMAT(2,3,ICRYS) +
     &                RSTAU(2,3,ICRYS)*QMAT(3,3,ICRYS)
      Q(3,1) = RSTAU(3,1,ICRYS)*QMAT(1,1,ICRYS) +
     &                RSTAU(3,2,ICRYS)*QMAT(2,1,ICRYS) +
     &                RSTAU(3,3,ICRYS)*QMAT(3,1,ICRYS)
      Q(3,2) = RSTAU(3,1,ICRYS)*QMAT(1,2,ICRYS) +
     &                RSTAU(3,2,ICRYS)*QMAT(2,2,ICRYS) +
     &                RSTAU(3,3,ICRYS)*QMAT(3,2,ICRYS)
      Q(3,3) = RSTAU(3,1,ICRYS)*QMAT(1,3,ICRYS) +
     &                RSTAU(3,2,ICRYS)*QMAT(2,3,ICRYS) +
     &                RSTAU(3,3,ICRYS)*QMAT(3,3,ICRYS)


	ICHK=0
	IF(DABS(Q(3,3))-ONE.GT.SMALL)THEN
C           WRITE(9,*)'ICRYS',ICRYS
C           WRITE(9,*)'Q',((Q(I,J),J=1,3),I=1,3)
	   PAUSE 'Q(3,3) > 1.0'
	ENDIF
C
	DO 10 J = 1,3
	DO 10 I = 1,3
 10	  IF(DABS(Q(I,J)).LT.SMALL) Q(I,J)=ZERO
C
	IF(DABS(DABS(Q(3,3))-ONE).LT.SMALL)THEN
           CALL CHECK1(Q,T,P,O,ICHK)
           TH(ICRYS) = T
           PHI(ICRYS)= P
           OM(ICRYS) = O
	   IF(ICHK.NE.1)GO TO 20
	   RETURN
	ENDIF
C
	TH(ICRYS) = DACOS(Q(3,3))
	STH = DSIN(TH(ICRYS))
	OM(ICRYS) = DATAN2(Q(1,3)/STH,Q(2,3)/STH)
	PHI(ICRYS) = DATAN2(Q(3,1)/STH,-Q(3,2)/STH)
C
        T = TH(ICRYS) 
        P = PHI(ICRYS)
        O = OM(ICRYS) 
	CALL CHECK(Q,T,P,O,ICHK)
	IF(ICHK.EQ.1)RETURN
C
	TH(ICRYS) = TWO*PI-TH(ICRYS)
	STH = DSIN(TH(ICRYS))
	OM(ICRYS) = DATAN2(Q(1,3)/STH,Q(2,3)/STH)
	PHI(ICRYS) = DATAN2(Q(3,1)/STH,-Q(3,2)/STH)
C
        T = TH(ICRYS) 
        P = PHI(ICRYS)
        O = OM(ICRYS) 
	CALL CHECK(Q,T,P,O,ICHK)

 20	IF(ICHK.NE.1)THEN
C	    WRITE(9,*)'ICRYS = ',ICRYS
C	    WRITE(9,*)'Q',((Q(J,K),K=1,3),J=1,3)
            PAUSE 'FAILED TO FIND EULER ANGLES'
	ENDIF
	RETURN
	END
C(((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))
C(((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))
	SUBROUTINE FORMSP(ICRYS)
cvd$r  noconcur
	INCLUDE 'commonsn48.tex'
	DIMENSION TMP(3,3)
C
        DO 10 I = 1,48
C
        TMP(1,1) = SMAT(1,1,I)*QT(1,1,ICRYS) +
     &                SMAT(1,2,I)*QT(2,1,ICRYS) +
     &                SMAT(1,3,I)*QT(3,1,ICRYS)
      TMP(1,2) = SMAT(1,1,I)*QT(1,2,ICRYS) +
     &                SMAT(1,2,I)*QT(2,2,ICRYS) +
     &                SMAT(1,3,I)*QT(3,2,ICRYS)
      TMP(1,3) = SMAT(1,1,I)*QT(1,3,ICRYS) +
     &                SMAT(1,2,I)*QT(2,3,ICRYS) +
     &                SMAT(1,3,I)*QT(3,3,ICRYS)
      TMP(2,1) = SMAT(2,1,I)*QT(1,1,ICRYS) +
     &                SMAT(2,2,I)*QT(2,1,ICRYS) +
     &                SMAT(2,3,I)*QT(3,1,ICRYS)
      TMP(2,2) = SMAT(2,1,I)*QT(1,2,ICRYS) +
     &                SMAT(2,2,I)*QT(2,2,ICRYS) +
     &                SMAT(2,3,I)*QT(3,2,ICRYS)
      TMP(2,3) = SMAT(2,1,I)*QT(1,3,ICRYS) +
     &                SMAT(2,2,I)*QT(2,3,ICRYS) +
     &                SMAT(2,3,I)*QT(3,3,ICRYS)
      TMP(3,1) = SMAT(3,1,I)*QT(1,1,ICRYS) +
     &                SMAT(3,2,I)*QT(2,1,ICRYS) +
     &                SMAT(3,3,I)*QT(3,1,ICRYS)
      TMP(3,2) = SMAT(3,1,I)*QT(1,2,ICRYS) +
     &                SMAT(3,2,I)*QT(2,2,ICRYS) +
     &                SMAT(3,3,I)*QT(3,2,ICRYS)
      TMP(3,3) = SMAT(3,1,I)*QT(1,3,ICRYS) +
     &                SMAT(3,2,I)*QT(2,3,ICRYS) +
     &                SMAT(3,3,I)*QT(3,3,ICRYS)


C
        SMATG(1,1,I,ICRYS) = QMAT(1,1,ICRYS)*TMP(1,1) +
     &                QMAT(1,2,ICRYS)*TMP(2,1) +
     &                QMAT(1,3,ICRYS)*TMP(3,1)
      SMATG(1,2,I,ICRYS) = QMAT(1,1,ICRYS)*TMP(1,2) +
     &                QMAT(1,2,ICRYS)*TMP(2,2) +
     &                QMAT(1,3,ICRYS)*TMP(3,2)
      SMATG(1,3,I,ICRYS) = QMAT(1,1,ICRYS)*TMP(1,3) +
     &                QMAT(1,2,ICRYS)*TMP(2,3) +
     &                QMAT(1,3,ICRYS)*TMP(3,3)
      SMATG(2,1,I,ICRYS) = QMAT(2,1,ICRYS)*TMP(1,1) +
     &                QMAT(2,2,ICRYS)*TMP(2,1) +
     &                QMAT(2,3,ICRYS)*TMP(3,1)
      SMATG(2,2,I,ICRYS) = QMAT(2,1,ICRYS)*TMP(1,2) +
     &                QMAT(2,2,ICRYS)*TMP(2,2) +
     &                QMAT(2,3,ICRYS)*TMP(3,2)
      SMATG(2,3,I,ICRYS) = QMAT(2,1,ICRYS)*TMP(1,3) +
     &                QMAT(2,2,ICRYS)*TMP(2,3) +
     &                QMAT(2,3,ICRYS)*TMP(3,3)
      SMATG(3,1,I,ICRYS) = QMAT(3,1,ICRYS)*TMP(1,1) +
     &                QMAT(3,2,ICRYS)*TMP(2,1) +
     &                QMAT(3,3,ICRYS)*TMP(3,1)
      SMATG(3,2,I,ICRYS) = QMAT(3,1,ICRYS)*TMP(1,2) +
     &                QMAT(3,2,ICRYS)*TMP(2,2) +
     &                QMAT(3,3,ICRYS)*TMP(3,2)
      SMATG(3,3,I,ICRYS) = QMAT(3,1,ICRYS)*TMP(1,3) +
     &                QMAT(3,2,ICRYS)*TMP(2,3) +
     &                QMAT(3,3,ICRYS)*TMP(3,3)


C
C    THE  SYMMETRIC PART OF MATRIX SMATG IS STORED AS A VECTOR PMAT. ALSO 
C    PMAT ENTERS THE CALCULATIONS ONLY AS DOT PRODUCT WITH THE STRESS. THE 
C    DOT PRODUCT OF THE MATRICES PMAT AND THE STRESS CAN BE REPLACED BY 
C    THE DOT PRODUCT BETWEEN THEIR VECTOR REPRESENTATIONS, IF THE OFF-
C    DIAGONAL TERMS OF PMAT ARE DOUBLED IN THEIR VECTOR REPRESENTATION.
C 
C
 	   PMAT(1,I,ICRYS) = SMATG (1,1,I,ICRYS) 
	   PMAT(2,I,ICRYS) = SMATG (2,2,I,ICRYS)
	   PMAT(3,I,ICRYS) = SMATG (3,3,I,ICRYS)
	   PMAT(4,I,ICRYS) = SMATG (1,2,I,ICRYS) + SMATG (2,1,I,ICRYS)
	   PMAT(5,I,ICRYS) = SMATG (1,3,I,ICRYS) + SMATG (3,1,I,ICRYS)
	   PMAT(6,I,ICRYS) = SMATG (3,2,I,ICRYS) + SMATG (2,3,I,ICRYS)
C
  10    CONTINUE
	RETURN
	END
C((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))
	SUBROUTINE INITIALIZE(IC)
	INCLUDE 'commonsn48.tex'
	CHARACTER*60 DUMMY
	OPEN(UNIT=2,FILE='euler.inp',STATUS ='OLD')
	OPEN(UNIT=3,FILE='bcc48',STATUS = 'OLD')
C
C   INITIALIZE CONSTANTS AND SCALARS
C
        ZERO = 0.0D0
	TINY = 1.0D-10
	ONE  = 1.0D0
	TWO  = 2.0D0
	THREE= 3.0D0
	FOUR = 4.0D0
	HALF = ONE/TWO
	THIRD= ONE/THREE
        PI = FOUR*DATAN(ONE)
        TIME = 0.0
C
C   initialize identity matrices
C
        DO 10 J=1,3
	   DO 10 I=1,3
 10           ONET(I,J) = ZERO
        DO 20 J=1,6
           DO 20 I=1,6
 20           ONES(I,J) = ZERO
C
 	ONET(1,1) = ONE
	ONET(2,2) = ONE
	ONET(3,3) = ONE
C
 	ONES(1,1) = ONE
	ONES(2,2) = ONE
	ONES(3,3) = ONE
	ONES(4,4) = ONE
	ONES(5,5) = ONE
	ONES(6,6) = ONE
C
       DELTA(1)=ONET(1,1) 
      DELTA(2)=ONET(2,2) 
      DELTA(3)=ONET(3,3)
      DELTA(4)=ONET(1,2) 
      DELTA(5)=ONET(1,3) 
      DELTA(6)=ONET(2,3) 

C
C
C   INITIALIZE FT; EQUAL TO IDENTITY IF THIS IS FRESH RUN OR READ
C   FROM RESTART FILE.
C
        IF(IC.EQ.0)THEN
            FT(1,1) = ONET (1,1)
           FT(1,2) = ONET (1,2)
           FT(1,3) = ONET (1,3)
           FT(2,1) = ONET (2,1)
           FT(2,2) = ONET (2,2)
           FT(2,3) = ONET (2,3)
           FT(3,1) = ONET (3,1)
           FT(3,2) = ONET (3,2)
           FT(3,3) = ONET (3,3)
        ELSE
           READ(16,*)((FT(I,J),J=1,3),I=1,3)
        ENDIF
C 
C  OBTAIN SLIP SYSTEM INFORMATION
C
	READ(3,*)NSLIP
	DO 30 I = 1,NSLIP
 30	READ(3,*)(AN(I,J),J=1,3),(AM(I,J),J=1,3)
C
	DO 40 I = 1,NSLIP
	   AMA = ONE/DSQRT(AM(I,1)**2+AM(I,2)**2+AM(I,3)**2)
	   ANA = ONE/DSQRT(AN(I,1)**2+AN(I,2)**2+AN(I,3)**2)
 	     AM(I,1) = AM(I,1)*AMA
             AN(I,1) = AN(I,1)*ANA
	     AM(I,2) = AM(I,2)*AMA
             AN(I,2) = AN(I,2)*ANA
	     AM(I,3) = AM(I,3)*AMA
             AN(I,3) = AN(I,3)*ANA
C
C            COMPUTE MATRIX SMAT IN LOCAL COORDINATES
C
 	     SMAT(1,1,I) = AM(I,1)*AN(I,1)
	     SMAT(1,2,I) = AM(I,1)*AN(I,2)
	     SMAT(1,3,I) = AM(I,1)*AN(I,3)
	     SMAT(2,1,I) = AM(I,2)*AN(I,1)
	     SMAT(2,2,I) = AM(I,2)*AN(I,2)
	     SMAT(2,3,I) = AM(I,2)*AN(I,3)
	     SMAT(3,1,I) = AM(I,3)*AN(I,1)
	     SMAT(3,2,I) = AM(I,3)*AN(I,2)
	     SMAT(3,3,I) = AM(I,3)*AN(I,3)
 40    CONTINUE
C
C  OBTAIN CRYSTAL INFORMATION
C
C  (HACKED TO READ IN SINGLE ANGLE)
	RADDEG = PI/180.0D0
C	READ(2,*)NCRYS
C	WRITE(*,*)'Bunge Angle (phi1, PHI, Phi2), 1
C     &
C     & Using Canova Angles (Theta, Phi, Omega), 2'
C	WRITE(*,*)'Output angles are in Bunge angles - regardless'
C	Read(*,*)iangtype
c41
CCCCCCCCCCCCCCCCModified
	RADDEG = PI/180.0D0
	READ(2,*)NCRYS
C	Write(*,*)'Bunge Angle (phi1, PHI, Phi2), 1
C     &
C     & Using Canova Angles (Theta, Phi, Omega), 2'
C	write(*,*)'Output angles are in Bunge angles - regardless'
	iangtype=1
c41
	DO 50 ICRYS = 1,NCRYS
	If(iangtype.EQ.1)THEN
	  	READ(2,*)phi1b,phib,phi2b
	    TH(ICRYS) = phib*RADDEG
		PHI(ICRYS) = (180.-phi2b)*RADDEG
		OM(ICRYS) = (180.-phi1b)*RADDEG
	 else
		read(2,*)TH(ICRYS),PHI(ICRYS),OM(ICRYS)
		TH(ICRYS) = TH(ICRYS)*RADDEG
		PHI(ICRYS) = PHI(ICRYS)*RADDEG
		OM(ICRYS) = OM(ICRYS)*RADDEG
	 ENDIF
	 
	ITHETA=30
	FTHETA = ITHETA*PI/180
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCcccccdipen
		
C	READ(*,*) phi1b, ITHETA
C	NCRYS = ZERO
C	DO phib = 0,90,3
C		DO phi2b = 0,90,3
C			WRITE(*,*) phi1b,phib,phi2b
C			NCRYS = NCRYS + ONE 
C                       ICRYS = NCRYS
C		TH(ICRYS) = phib*RADDEG
C			PHI(ICRYS) = (180.-phi2b)*RADDEG
C			OM(ICRYS) = (180.-phi1b)*RADDEG
C		END DO
C	END DO
C	FTHETA = (ITHETA-1)*2*PI/120
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDipen
C
 50     CONTINUE
C
cvd$    cncall
cvd$    concur
	DO 100 ICRYS = 1,NCRYS  
	     wstar(1,icrys)= 0.0
	     wstar(2,icrys)= 0.0
	     wstar(3,icrys)= 0.0		     
           NSB(ICRYS) = 0
C
C          OBTAIN THE TRANSFORMATION MATRIX AND STORE FOR USE IN FINAL 
C          TEXTURE CALCULATION.
C
	   CALL ROTMAT(ICRYS)
C
C          COMPUTE SALPHA AND PALPHA MATRICES FOR THE CRYSTAL IN GLOBAL
C          COORDINATES. PALPHA IS THE SYMMETRIC COMPONENT OF SALPHA.
C
           CALL FORMSP(ICRYS)
C
C          INITIALIZE THE STRESS, PLASTIC DEFORMATION GRADIENT AND SLIP
C          SYSTEM RESISTANCES AT ZERO, OR READ FRO RESTART FILE.
C
           IF(IC.EQ.0)THEN
cvd$         noconcur
             DO 60 K = 1,3
              DO 60 J = 1,3
                TBTMAT(J,K,ICRYS) = ZERO
 60	        FPTINV(J,K,ICRYS) = ONET(J,K)
cvd$         noconcur
	     DO 70 J = 1,48
                ACCGAM(J,ICRYS) = 0.0
 70             CRSS(J,ICRYS) = SO
           ENDIF
C
 100     CONTINUE
C
         IF(IC.NE.0)THEN
          READ(16,*)(((TBTMAT(J,K,I),K=1,3),J=1,3),I=1,NCRYS)
          READ(16,*)(((FPTINV(J,K,I),K=1,3),J=1,3),I=1,NCRYS)
          READ(16,*)((CRSS(I,ICRYS),I=1,48),ICRYS=1,NCRYS)
         ENDIF
C
C  INITIALISE LATENT HARDENING MATRIX QLAT
C
	DO 150 J = 1,48
         DO 150 I = 1,48
 150         QLAT(I,J) = QL
	DO 200 NBL = 1,4
     	   DO 200 JIND = 1,3
              J = JIND + (NBL-1)*3
              DO 200 IIND = 1,3
                 I = IIND + (NBL-1)*3
		 QLAT(I,J) = ONE
 200    CONTINUE
C
	CLOSE(2)
	CLOSE(3)
C
C  PUT IN THE HEADERS FOR THE STRESS OUTPUT FILES.
C
	DUMMY = 'GAMMA'
	WRITE(10,101)DUMMY
	WRITE(11,101)DUMMY
	WRITE(12,101)DUMMY
	WRITE(13,101)DUMMY
	WRITE(14,101)DUMMY
101     FORMAT(A6)
	DUMMY = 'S11'
	WRITE(10,101)DUMMY
	DUMMY ='S22'
	WRITE(11,101)DUMMY
 	DUMMY = 'S12'
	WRITE(12,101)DUMMY
	DUMMY = 'S33'
	WRITE(13,101)DUMMY
	DUMMY = 'S11P'
	WRITE(14,101)DUMMY
	DUMMY = 'TYPE 3'
	WRITE(10,101)DUMMY
	WRITE(11,101)DUMMY
	WRITE(12,101)DUMMY
	WRITE(13,101)DUMMY
	WRITE(14,101)DUMMY
	DUMMY = 'SYMB 201.'
	WRITE(10,110)DUMMY
	WRITE(11,110)DUMMY
	WRITE(12,110)DUMMY
	WRITE(13,110)DUMMY
	WRITE(14,110)DUMMY
110	FORMAT(A9)
	DUMMY = 'END'
	WRITE(10,120)DUMMY
	WRITE(11,120)DUMMY
	WRITE(12,120)DUMMY
	WRITE(13,120)DUMMY
	WRITE(14,120)DUMMY
120	FORMAT(A3)
	DUMMY = '0.0 0.0'
        IF(IC.EQ.0)THEN
	WRITE(10,110)DUMMY
	WRITE(11,110)DUMMY
	WRITE(12,110)DUMMY
	WRITE(13,110)DUMMY
	WRITE(14,110)DUMMY
        ENDIF
	RETURN
	END
C(((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))
        SUBROUTINE INPUT
        INCLUDE 'commonsn48.tex'
C	CHARACTER DUMMY
C	DIMENSION DUMMY(80)
C
	OPEN(UNIT=1,FILE='temptay_48.inp',STATUS='OLD')
        READ(1,1)DUMMY
1       FORMAT(80A1)
	READ(1,*)C11,C12,C44,LFLAG,EDOT,QFAC
	READ(1,1)DUMMY
	READ(1,*)TTIME,DTIME
	READ(1,1)DUMMY
	READ(1,*)TAUTO,DTMAX
	READ(1,1)DUMMY
	READ(1,*)GDO,XM
	READ(1,1)DUMMY
	READ(1,*)OUT,TEX
	READ(1,1)DUMMY
	READ(1,*)HO,SO,SS,AEXP,QL,SEXP
	CLOSE(1)
	RETURN
	END	
C**************************************************************************
C   THIS PROGRAM IMPLEMENTS A NEW FULLY IMPLICIT TIME INTEGRATION SCHEME
C   FOR A SET OF CONSTITUTIVE LAWS THAT DESCRIBE THE EVOLUTION OF CRYSTAL-
C   LOGRAPHIC TEXTURE WITH LARGE DEFORMATIONS.
C
C   THIS PROGRAM IS LIMITED TO HOMOGENEOUS DEFORMATIONS.
C
C   THE DEFINITIONS OF MOST VARIABLES ARE PROVIDED IN COMMONS.TEX. 
C   THIS IS THE MAIN PROGRAM. THE LOCAL VARIABLES ARE DEFINED AS:
C
C   TEXFLAG   : A TIME FLAG INDICATING WHEN TEXTURE IS TO BE OUTPUT.
C
C   OUTFLAG   : A TIME FLAG INDICATING WHEN STRESSES ARE TO BE WRITTEN
C               TO FILES.
C    
        PROGRAM MAIN
C
        INCLUDE 'commonsn48.tex'
C
	OPEN(UNIT=10,FILE='s11')
	OPEN(UNIT=11,FILE='s22')
	OPEN(UNIT=12,FILE='s12')
	OPEN(UNIT=13,FILE='s33')
	OPEN(UNIT=14,FILE='s13')
	OPEN(UNIT=15,FILE='s23')
	OPEN(UNIT=17,FILE='crystalstresses.txt')
	OPEN(UNIT=8,FILE='texture.out')
	OPEN(UNIT=9,FILE='errorfile')
      OPEN(UNIT=15,FILE='ept.res')
      OPEN(UNIT=16,FILE='ept.res0',STATUS='OLD')
	open(unit=21,file='wstar.txt')
C
        IC=0
        ALPHA=0.0
	TOTALGAM = 0.0
C
        CALL INPUT
C
	CALL INITIALIZE(IC)
C
	TEXFLAG = TEX
	OUTFLAG = TAUTO

C
C   START OF TIME LOOP
C
100     IF(TIME.EQ.TTIME)GO TO 300

C	Marko 2-28-08
	if(time.eq.dtime)THEN
	dtime = 20
	ENDIF
C	Marko 2-28-08

	TAU = TIME + DTIME
	IF(TAU.GT.TTIME)THEN
          TAU = TTIME
          DTIME = TAU - TIME
        ENDIF
C	WRITE(*,*)'TAU=',TAU
C
C   GET THE DEFORMATION GRADIENT AT TAU IN GLOBAL COORDINATES
C
C
C   START OF LOOP OVER CRYSTALS
C
C       concurrent call of sbr's inside the do loop
cvd$    cncall
	DO 200 ICRYS = 1,NCRYS

	     CALL DEFGRAD(ICRYS)
C
C            COMPUTE THE TRIAL STRESS TBTR
C
	     CALL TRSTRESS(ICRYS)
C
C            SOLVE FOR TBTAU; USE TBTMAT AS INITIAL GUESS
C
             TBTAU(1,1,ICRYS) = TBTMAT(1,1,ICRYS)
             TBTAU(1,2,ICRYS) = TBTMAT(1,2,ICRYS)
             TBTAU(1,3,ICRYS) = TBTMAT(1,3,ICRYS)
             TBTAU(2,1,ICRYS) = TBTMAT(2,1,ICRYS)
             TBTAU(2,2,ICRYS) = TBTMAT(2,2,ICRYS)
             TBTAU(2,3,ICRYS) = TBTMAT(2,3,ICRYS)
             TBTAU(3,1,ICRYS) = TBTMAT(3,1,ICRYS)
             TBTAU(3,2,ICRYS) = TBTMAT(3,2,ICRYS)
             TBTAU(3,3,ICRYS) = TBTMAT(3,3,ICRYS)
C
C
	     CALL NEWT(ICRYS)
C
	     CALL UPDATE(ICRYS)
	
C
 200    CONTINUE
C
C       AVERAGING IS DONE ON CAUCHY STRESS (EQUIVALENT TO DOING ON
C       FIRST PK STRESS).
C
c,,,,,,,,,,,,,,, use next instructions on alliant only!,,,,,,,,,,,,,,
C        AVGSTR = sum(TTAU,3)
C        DGMAXG = maxval(DGMAX)
c'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
c,,,,,,,,,alternative instructions for sun stations,,,,,,,,,,,,,,,,,,
C
         AVGSTR(1,1) = ZERO
         AVGSTR(1,2) = ZERO
         AVGSTR(1,3) = ZERO
         AVGSTR(2,1) = ZERO
         AVGSTR(2,2) = ZERO
         AVGSTR(2,3) = ZERO
         AVGSTR(3,1) = ZERO
         AVGSTR(3,2) = ZERO
         AVGSTR(3,3) = ZERO
C
        DO 210 ICRYS = 1,NCRYS
          IF(TAU.EQ.TTIME) THEN
            TOTALGAM = 0.0
            DO 97 J=1,48
97          TOTALGAM = DABS(DGTAU(J,ICRYS))+TOTALGAM
	   hid = (TTAU(1,1,ICRYS)+TTAU(2,2,ICRYS)+TTAU(3,3,ICRYS))/3
            WRITE(17,888)TTAU(1,1,ICRYS)-hid,
     &      TTAU(2,2,ICRYS)-hid,
     &   TTAU(1,2,ICRYS),TTAU(1,3,ICRYS),TTAU(2,3,ICRYS),TOTALGAM/DTIME
          ENDIF
98        FORMAT(3F10.4)
888   format(7f15.9)
          DO 210 K = 1,3
              DO 210 J = 1,3
 210              AVGSTR(J,K) = AVGSTR(J,K) + TTAU(J,K,ICRYS)
C
        DGMAXG = ZERO
        DO 220 ICRYS=1,NCRYS
 220        DGMAXG = DMAX1(DGMAXG,DGMAX(ICRYS))
c'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	DO 230 K = 1,3
        DO 230 J = 1,3
 230		AVGSTR(J,K) = AVGSTR(J,K)/NCRYS
C
C       printing
C
        IF(TAU.GE.TEXFLAG)THEN
                CALL TEXTURE
                TEXFLAG = TEXFLAG+TEX
        ENDIF
C
	IF(TAU.LT.TAUTO.OR.TAU.GE.OUTFLAG) CALL OUTPUT
        IF(TAU.GE.OUTFLAG) OUTFLAG = OUTFLAG+OUT
C
C       update time 
C
	TIME = TAU
C
C
	IF(TAU.GT.TAUTO)THEN
        	DTIME = DTIME*0.01/DGMAXG
	        IF(DTIME.GT.DTMAX)DTIME = DTMAX
	ENDIF
C
	GO TO 100
C
C300  	WRITE(15,*)TIME 
300	DO 301 K=1,NCRYS
	TACCGAM=0.
	do 302 J=1,48		
302	TACCGAM=TACCGAM+ACCGAM(J,K) 
301	 WRITE(15,*)TACCGAM
C        WRITE(15,*)((FTAU(J,K),K=1,3),J=1,3)
C        WRITE(15,*)(((TBTMAT(J,K,I),K=1,3),J=1,3),I=1,NCRYS)
C        WRITE(15,*)(((FPTINV(J,K,I),K=1,3),J=1,3),I=1,NCRYS)
c        WRITE(15,*)((CRSS(J,I),J=1,12),I=1,NCRYS)

c        I played here for...
c         WRITE(17,*) TTAU(1,1,ICRYS),TTAU(2,2,ICRYS),TTAU(3,3,ICRYS),
c     &   TTAU(1,2,ICRYS),TTAU(1,3,ICRYS),TTAU(2,3,ICRYS),TOTALGAM
        
        CLOSE(10)
	CLOSE(11)
	CLOSE(12)
	CLOSE(13)
	CLOSE(14)
	CLOSE(15)
	CLOSE(16)
	CLOSE(8)
	STOP
	END
C((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))))
c ------------ take out keyword recursive to run it on sun!!!!---
C
	SUBROUTINE NEWT(ICRYS)
cvd$r   noconcur
	INCLUDE 'commonsn48.tex'
	DIMENSION CRSSALPHA(48),CONST(6,6,48), DEPI(48),
     &           ERR(6),AJAC(6,6),ABSA(6),D(6),UX(6),INDX(6),DTBV(6),
     &           ABDTBV(6),TRV(6),TBV(6),RSSTAU(48),ABSDG(48),
     &           CRSSNEW(48),HJ(48),TOLD(6)
       LOGICAL LMASK(6)
C
        ITER = 1
        DGDO = GDO*DTIME
        XMINV= ONE/XM
C
        RELAX = ONE
        ICORR = 0
        DMAX = 0.05D0
C
        DO 1 I = 1,48
         CRSSALPHA(I)= CRSS(I,ICRYS)
         DO 1 K = 1,6
          DO 1 J = 1,6
 1           CONST(J,K,I) = CMAT(J,I,ICRYS)*PMAT(K,I,ICRYS)
 
C
        TRV(1)=TBTR(1,1,ICRYS) 
      TRV(2)=TBTR(2,2,ICRYS) 
      TRV(3)=TBTR(3,3,ICRYS)
      TRV(4)=TBTR(1,2,ICRYS) 
      TRV(5)=TBTR(1,3,ICRYS) 
      TRV(6)=TBTR(2,3,ICRYS) 

        TBV(1)=TBTAU(1,1,ICRYS) 
      TBV(2)=TBTAU(2,2,ICRYS) 
      TBV(3)=TBTAU(3,3,ICRYS)
      TBV(4)=TBTAU(1,2,ICRYS) 
      TBV(5)=TBTAU(1,3,ICRYS) 
      TBV(6)=TBTAU(2,3,ICRYS) 

C
C,,,,,,,,,,,,,,,, start double loop ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
 999    CONTINUE
C
C       Evaluate resolved shear stress (ex-sbr RESOLVE)-------------
C
	DO 10 I = 1,48
 10	 RSSTAU(I) = ZERO
C
	DO 20 J = 1,6
         DO 20 I = 1,48
 20	   RSSTAU(I) = RSSTAU(I) + TBV(J)*PMAT(J,I,ICRYS)
C
C       ---------- (end ex-RESOLVE)---------------------------------
C
C       Evaluate delta-gamma on the slip systems (ex-sbr DGAMMAO)-------
C
	DO 30 I = 1,48
	 IF(RSSTAU(I).EQ.ZERO)THEN
           DGTAU(I,ICRYS) = ZERO
	 ELSE
           ABSDG(I) = DGDO*DABS(RSSTAU(I)/CRSSALPHA(I))**XMINV
           DGTAU(I,ICRYS) = SIGN(ABSDG(I),RSSTAU(I))
	 ENDIF
 30     CONTINUE
C
C       -----------------(end ex-DGAMMAO)--------------------------------
C
        DO 34 J=1,6
34         TOLD(J) = TBV(J)
C
	DO 40 J=1,6
 40      ERR(J) =  TBV(J) - TRV(J)
C
        DO 50 I=1,48
           DO 50 J=1,6
 50           ERR(J) = ERR(J)+DGTAU(I,ICRYS)*CMAT(J,I,ICRYS)
C
        DO 60 K=1,6
           DO 60 J=1,6
 60           AJAC(J,K) = ONES(J,K)     
C
C       the loop on I (the slip systems) has to be made explicit
C       so that the '100' loops can be collapsed
c
        I = 0
 99     CONTINUE
           I = I+1
	   IF (DGTAU(I,ICRYS).NE.ZERO) THEN
               DEPI(I) = DGTAU(I,ICRYS)*XMINV/RSSTAU(I)
C
               DO 100 K = 1,6
	       DO 100 J = 1,6
 100	          AJAC(J,K) = AJAC(J,K) +CONST(J,K,I)* DEPI(I)
C
           ENDIF
        IF(I.LT.48) GO TO 99
C
C==================================================================
C      Solution of AJAC*DTBV=ERR using Gauss-Jordan elimination   |
C      with partial (column) pivoting (ex- sbr's LUDCMP & LUBKSB) |
C
       DO 110 J=1,6
 110      LMASK(J) = .TRUE.
C
C      do over the columns
C
       DO 170 J=1,6
C
C        column pivoting : find max coeff. in column J
C
         DO 120 K=1,6
 120        ABSA(K) = DABS(AJAC(K,J))
C
 	  DO 130 K=1,6
  130       IF(LMASK(K)
     &     .AND.( (.NOT.LMASK(1)) .OR. (ABSA(K).GE.ABSA(1)) )
     &     .AND.( (.NOT.LMASK(2)) .OR. (ABSA(K).GE.ABSA(2)) )
     &     .AND.( (.NOT.LMASK(3)) .OR. (ABSA(K).GE.ABSA(3)) )
     &     .AND.( (.NOT.LMASK(4)) .OR. (ABSA(K).GE.ABSA(4)) )
     &     .AND.( (.NOT.LMASK(5)) .OR. (ABSA(K).GE.ABSA(5)) )
     &     .AND.( (.NOT.LMASK(6)) .OR. (ABSA(K).GE.ABSA(6)) )  )
     &                          IPIV = K
C        store pivot and position
         INDX(J)     = IPIV
	  D(IPIV)     = ONE/AJAC (IPIV,J) 
         LMASK(IPIV) = .FALSE.
C
C        compute elimination coefficients for column J
C
         DO 140 K=1,6
 140        AJAC(K,J) = AJAC(K,J)*D(IPIV)
C
C        value zero cause pivot row to remain unchanged
C
         AJAC(IPIV,J) = ZERO
C
C        update all remaining columns
C       
C        no data dependency because AJAC(IPIV,J)=0.0
cvd$     nodepchk
         DO 150 L=J+1,6
cvd$        nodepchk
            DO 150 K=1,6
 150              AJAC(K,L) = AJAC(K,L) - AJAC(K,J)*AJAC(IPIV,L)
C
C        update r.h.s
C       
C        no data dependency because AJAC(IPIV,J)=0.0
cvd$     nodepchk
         DO 160 K=1,6
 160        ERR(K) = ERR(K) - AJAC(K,J)*ERR(IPIV)
C
 170   CONTINUE
C
C      compute solution UX of (1/D)*UX=ERR 
C      (non ordered solution of original system)       
C
       DO 180 J=1,6
 180      UX(J) = ERR(J)*D(J)
C
C      gather solution to build DTBV
C
       DO 190 J=1,6
 190      DTBV(J) = UX(INDX(J))
C
C==================end G-J algorithm=================================
C
	DO 200 J = 1,6
              ABDTBV(J) = DABS(DTBV(J))
              TBV(J)= TBV(J) - DTBV(J)
 200   CONTINUE
C
	ERRMAX = ZERO
	DO 210 J = 1,6
 210	  ERRMAX = DMAX1(ERRMAX,ABDTBV(J))
C
	ITER = ITER + 1
C
	IF(ITER.GT.100)THEN
         WRITE(9,*)'TBV, ERCRSS,ERRMAX',ERCRSS,ERRMAX
	  WRITE(9,*)(TBV(I),I=1,6)
         WRITE(9,*)(CRSSALPHA(I),I=1,48)
	ENDIF
C
        IF(ITER.GT.110)STOP
998     CONTINUE
C
C       Evaluate resolved shear stress (ex-sbr RESOLVE)-------------
C
	DO 310 I = 1,48
 310	 RSSTAU(I) = ZERO
C
	DO 320 J = 1,6
         DO 320 I = 1,48
 320	   RSSTAU(I) = RSSTAU(I) + TBV(J)*PMAT(J,I,ICRYS)
C
C       ---------- (end ex-RESOLVE)---------------------------------
C
C       Evaluate delta-gamma on the slip systems (ex-sbr DGAMMAO)-------
C
        AMAXDG = 0.0D0
	DO 330 I = 1,48
	 IF(RSSTAU(I).EQ.ZERO)THEN
           ABSDG(I) = ZERO
           DGTAU(I,ICRYS) = ZERO
	 ELSE
           ABSDG(I) = DGDO*DABS(RSSTAU(I)/CRSSALPHA(I))**XMINV
           DGTAU(I,ICRYS) = SIGN(ABSDG(I),RSSTAU(I))
	 ENDIF
 330     AMAXDG = DMAX1(AMAXDG,ABSDG(I))
C
C       ---------------------(end ex-DGAMMAO)---------------------------
        IF(ERRMAX.GT.SO/10000.) THEN
         IF(AMAXDG.GT.DMAX*RELAX) THEN
           IF(ICORR.GT.30)GO TO 36
           DO 33 J=1,6
           DTBV(J) = DTBV(J)*0.25
33         TBV(J)=TOLD(J)-DTBV(J) 
           ICORR=ICORR+1
           GO TO 998
         ENDIF
36      CONTINUE
        ICORR = 0
        GO TO 999
        ENDIF
C
C''''''''''''''''''''end inside loop''''''''''''''''''''''''''''''
C
C       Update CRSSALPHA ( ex sbr. UPCRSS)-----------------------------
C
	DO 350 I = 1,48
C
          IF ((ABSDG(I)/DGDO).LT.TINY)THEN
               HJ(I) = ZERO
          ELSE
               SGN = ONE - CRSSALPHA(I)/(SS*(ABSDG(I)/DGDO)**SEXP) 
               IF (SGN.EQ.ZERO)THEN
                       HJ(I) = ZERO
               ELSE
	               HJ(I) = SIGN(HO*(DABS(SGN))**AEXP,SGN)
               ENDIF
          ENDIF
C
          CRSSNEW(I) = CRSS(I,ICRYS)
C
 350   CONTINUE
C
	DO 360 II = 1,48
	 DO 360 I = 1,48
 360       CRSSNEW(I) = CRSSNEW(I)+HJ(II)*QLAT(I,II)*ABSDG(II)
C
	ERCRSS = ZERO
	DO 370 I = 1,48 
	  ERCRSS = DMAX1(DABS(CRSSNEW(I)-CRSSALPHA(I)),ERCRSS)  
	  CRSSALPHA(I) = CRSSNEW(I)
 370   CONTINUE
C-------------- end ex-sbr UPCRSS ------------------------------------

	IF(ERCRSS.GT.SO/100.)GO TO 999
C'''''''''''''''''''''''' end outside loop '''''''''''''''''''''''''''
C
         TBTAU(1,1,ICRYS)=TBV(1) 
      TBTAU(1,2,ICRYS)=TBV(4) 
      TBTAU(1,3,ICRYS)=TBV(5)
      TBTAU(2,1,ICRYS)=TBV(4) 
      TBTAU(2,2,ICRYS)=TBV(2) 
      TBTAU(2,3,ICRYS)=TBV(6)
      TBTAU(3,1,ICRYS)=TBV(5) 
      TBTAU(3,2,ICRYS)=TBV(6) 
      TBTAU(3,3,ICRYS)=TBV(3)

C
C
        DGMAX(ICRYS) = ZERO
        GMAX = ZERO
        NSYS(ICRYS) = 0
C
	DO 500 I = 1,48
        ACCGAM(I,ICRYS)=ACCGAM(I,ICRYS)+ABSDG(I)
        CRSS(I,ICRYS)=CRSSALPHA(I)
        GMAX=DMAX1(GMAX,ACCGAM(I,ICRYS))
        IF(GMAX.EQ.ACCGAM(I,ICRYS))NSYS(ICRYS) = I
500     DGMAX(ICRYS) = DMAX1(DGMAX(ICRYS),ABSDG(I))
C
	RETURN
	END


C(((((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))
	SUBROUTINE OUTPUT
	INCLUDE 'commonsn48.tex'
	IF(LFLAG.EQ.1)THEN
           WRITE(10,*)FTAU(1,3),AVGSTR(1,1)
           WRITE(11,*)FTAU(1,3),AVGSTR(2,2)
           WRITE(14,*)FTAU(1,3),AVGSTR(1,3)
           WRITE(13,*)FTAU(1,3),AVGSTR(3,3)
	ENDIF
	IF(LFLAG.EQ.2)THEN
	   SIGM = (AVGSTR(1,1)+AVGSTR(2,2))/2.0
 	   DDLFT = DABS(DLOG(FTAU(3,3)))
	   WRITE(10,*)DDLFT,AVGSTR(1,1)-SIGM
	   WRITE(11,*)DDLFT,AVGSTR(2,2)-SIGM
	   WRITE(12,*)DDLFT,AVGSTR(1,2)
	   WRITE(13,*)DDLFT,AVGSTR(3,3)-SIGM
           WRITE(14,*)DDLFT,AVGSTR(1,3)
	ENDIF
	IF(LFLAG.EQ.3.OR.LFLAG.EQ.4)THEN
 	   DDLFT = DABS(DLOG(FTAU(3,3)))
C     &	    AVGSTR(1,2), AVGSTR(1,3), AVGSTR(2,3)
           WRITE(11,*)DDLFT,AVGSTR(2,2)

95        FORMAT(7F10.4)
	   WRITE(12,*)DDLFT,AVGSTR(1,2)
	   WRITE(13,*)DDLFT,AVGSTR(3,3)-AVGSTR(1,1)
           WRITE(14,*)DDLFT,AVGSTR(1,3)
	ENDIF
	IF (LFLAG.EQ.55)THEN
		WRITE(10,*)FTAU(1,3),AVGSTR(1,1)
          WRITE(11,*)FTAU(1,3),AVGSTR(2,2)
		WRITE(12,*)FTAU(1,3),AVGSTR(1,2)
          WRITE(14,*)FTAU(1,3),AVGSTR(1,3)
          WRITE(13,*)FTAU(1,3),AVGSTR(3,3),AVGSTR(1,1)-AVGSTR(3,3)
	ENDIF
	RETURN
	END
C((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))
	SUBROUTINE ROTMAT(ICRYS)
C
C     TRANSFORMATION MATRIX, GIVEN THE EULER ANGLES. SEE APPENDIX A OF THE
C     REPORT.
C
	INCLUDE 'commonsn48.tex'
	SOM = DSIN(OM(ICRYS))
        COM = DCOS(OM(ICRYS))
        STH = DSIN(TH(ICRYS))
        CTH = DCOS(TH(ICRYS))
        SPH = DSIN(PHI(ICRYS))
        CPH = DCOS(PHI(ICRYS))
        QMAT(1,1,ICRYS) = CPH*COM-SPH*SOM*CTH
        QMAT(1,2,ICRYS) = SPH*COM+SOM*CPH*CTH
        QMAT(1,3,ICRYS) = STH*SOM
        QMAT(2,1,ICRYS) = -CPH*SOM-SPH*COM*CTH
        QMAT(2,2,ICRYS) = -SPH*SOM+CPH*COM*CTH
        QMAT(2,3,ICRYS) = STH*COM
        QMAT(3,1,ICRYS) = STH*SPH
        QMAT(3,2,ICRYS) = -STH*CPH
        QMAT(3,3,ICRYS) = CTH
C
       QT(1,1,ICRYS)=QMAT(1,1,ICRYS) 
      QT(1,2,ICRYS)=QMAT(2,1,ICRYS) 
      QT(1,3,ICRYS)=QMAT(3,1,ICRYS)
      QT(2,1,ICRYS)=QMAT(1,2,ICRYS) 
      QT(2,2,ICRYS)=QMAT(2,2,ICRYS) 
      QT(2,3,ICRYS)=QMAT(3,2,ICRYS)
      QT(3,1,ICRYS)=QMAT(1,3,ICRYS) 
      QT(3,2,ICRYS)=QMAT(2,3,ICRYS) 
      QT(3,3,ICRYS)=QMAT(3,3,ICRYS)

C
	RETURN
	END
C((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))
	SUBROUTINE TEXTURE
	INCLUDE 'commonsn48.tex'
	dimension wp(3,3), tmp(3,3), tmp1(3,3)
C
        DEGRAD = 180.0D0/PI
C
cvd$    cncall
	DO 100 ICRYS = 1,NCRYS
C 	
	CALL DECOMP(ICRYS)

      wp(1,2)=wstar(1,icrys)/dtime
      wp(1,3)=wstar(2,icrys)/dtime
      wp(2,3)=wstar(3,icrys)/dtime
	wp(2,1)=-wp(1,2)
	wp(3,1)=-wp(1,3)
	wp(3,2)=-wp(2,3)
	wp(1,1)=0.0
	wp(2,2)=0.0
	wp(3,3)=0.0

      do 10 i=1,3
	do 10 j=1,3
	tmp(i,j)=0.0
	do 10 k=1,3
10	tmp(i,j)=tmp(i,j)+rstau(i,k,icrys)*wp(k,j)
      do 11 i=1,3
	do 11 j=1,3
	tmp1(i,j)=0.0
	do 11 k=1,3
11	tmp1(i,j)=tmp1(i,j)+tmp(i,k)*rstau(j,k,icrys)
C    HACK: WRITE WSTAR to console
      WRITE(21,12)tmp1(1,2),tmp1(1,3),tmp1(2,3)
12    format(9f15.9)





C
	CALL EULANG(ICRYS)
        TH(ICRYS) = TH(ICRYS)*DEGRAD
        PHI(ICRYS) = PHI(ICRYS)*DEGRAD
	OM(ICRYS) = OM(ICRYS)*DEGRAD
C
 100	CONTINUE
      
C	HACK: WRITE to console
	WRITE(8,*)NCRYS
        DO 200 ICRYS = 1,NCRYS
200     WRITE(8,*)180.-OM(ICRYS),TH(ICRYS),180.-PHI(ICRYS)
C
	RETURN
	END
C((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))
	SUBROUTINE TRSTRESS(ICRYS)
cvd$r   noconcur
	INCLUDE 'commonsn48.tex'
	DIMENSION BALPHA(3,3,48),CALPHA(3,3,48)
	DIMENSION TMP1(3,3,48),TMP2(3,3),TMP3(3,3),TC(3,3),EC(3,3)
C
C    COMPUTE TENSOR QUANTITY A
C
        TMP3(1,1) = FTAU(1,1)*FTAU(1,1) +
     &                FTAU(2,1)*FTAU(2,1) +
     &                FTAU(3,1)*FTAU(3,1)
      TMP3(1,2) = FTAU(1,1)*FTAU(1,2) +
     &                FTAU(2,1)*FTAU(2,2) +
     &                FTAU(3,1)*FTAU(3,2)
      TMP3(1,3) = FTAU(1,1)*FTAU(1,3) +
     &                FTAU(2,1)*FTAU(2,3) +
     &                FTAU(3,1)*FTAU(3,3)
      TMP3(2,1) = FTAU(1,2)*FTAU(1,1) +
     &                FTAU(2,2)*FTAU(2,1) +
     &                FTAU(3,2)*FTAU(3,1)
      TMP3(2,2) = FTAU(1,2)*FTAU(1,2) +
     &                FTAU(2,2)*FTAU(2,2) +
     &                FTAU(3,2)*FTAU(3,2)
      TMP3(2,3) = FTAU(1,2)*FTAU(1,3) +
     &                FTAU(2,2)*FTAU(2,3) +
     &                FTAU(3,2)*FTAU(3,3)
      TMP3(3,1) = FTAU(1,3)*FTAU(1,1) +
     &                FTAU(2,3)*FTAU(2,1) +
     &                FTAU(3,3)*FTAU(3,1)
      TMP3(3,2) = FTAU(1,3)*FTAU(1,2) +
     &                FTAU(2,3)*FTAU(2,2) +
     &                FTAU(3,3)*FTAU(3,2)
      TMP3(3,3) = FTAU(1,3)*FTAU(1,3) +
     &                FTAU(2,3)*FTAU(2,3) +
     &                FTAU(3,3)*FTAU(3,3)


C
        TMP2(1,1) = TMP3(1,1)*FPTINV(1,1,ICRYS) +
     &                TMP3(1,2)*FPTINV(2,1,ICRYS) +
     &                TMP3(1,3)*FPTINV(3,1,ICRYS)
      TMP2(1,2) = TMP3(1,1)*FPTINV(1,2,ICRYS) +
     &                TMP3(1,2)*FPTINV(2,2,ICRYS) +
     &                TMP3(1,3)*FPTINV(3,2,ICRYS)
      TMP2(1,3) = TMP3(1,1)*FPTINV(1,3,ICRYS) +
     &                TMP3(1,2)*FPTINV(2,3,ICRYS) +
     &                TMP3(1,3)*FPTINV(3,3,ICRYS)
      TMP2(2,1) = TMP3(2,1)*FPTINV(1,1,ICRYS) +
     &                TMP3(2,2)*FPTINV(2,1,ICRYS) +
     &                TMP3(2,3)*FPTINV(3,1,ICRYS)
      TMP2(2,2) = TMP3(2,1)*FPTINV(1,2,ICRYS) +
     &                TMP3(2,2)*FPTINV(2,2,ICRYS) +
     &                TMP3(2,3)*FPTINV(3,2,ICRYS)
      TMP2(2,3) = TMP3(2,1)*FPTINV(1,3,ICRYS) +
     &                TMP3(2,2)*FPTINV(2,3,ICRYS) +
     &                TMP3(2,3)*FPTINV(3,3,ICRYS)
      TMP2(3,1) = TMP3(3,1)*FPTINV(1,1,ICRYS) +
     &                TMP3(3,2)*FPTINV(2,1,ICRYS) +
     &                TMP3(3,3)*FPTINV(3,1,ICRYS)
      TMP2(3,2) = TMP3(3,1)*FPTINV(1,2,ICRYS) +
     &                TMP3(3,2)*FPTINV(2,2,ICRYS) +
     &                TMP3(3,3)*FPTINV(3,2,ICRYS)
      TMP2(3,3) = TMP3(3,1)*FPTINV(1,3,ICRYS) +
     &                TMP3(3,2)*FPTINV(2,3,ICRYS) +
     &                TMP3(3,3)*FPTINV(3,3,ICRYS)


C
        A(1,1,ICRYS) = FPTINV(1,1,ICRYS)*TMP2(1,1) +
     &                FPTINV(2,1,ICRYS)*TMP2(2,1) +
     &                FPTINV(3,1,ICRYS)*TMP2(3,1)
      A(1,2,ICRYS) = FPTINV(1,1,ICRYS)*TMP2(1,2) +
     &                FPTINV(2,1,ICRYS)*TMP2(2,2) +
     &                FPTINV(3,1,ICRYS)*TMP2(3,2)
      A(1,3,ICRYS) = FPTINV(1,1,ICRYS)*TMP2(1,3) +
     &                FPTINV(2,1,ICRYS)*TMP2(2,3) +
     &                FPTINV(3,1,ICRYS)*TMP2(3,3)
      A(2,1,ICRYS) = FPTINV(1,2,ICRYS)*TMP2(1,1) +
     &                FPTINV(2,2,ICRYS)*TMP2(2,1) +
     &                FPTINV(3,2,ICRYS)*TMP2(3,1)
      A(2,2,ICRYS) = FPTINV(1,2,ICRYS)*TMP2(1,2) +
     &                FPTINV(2,2,ICRYS)*TMP2(2,2) +
     &                FPTINV(3,2,ICRYS)*TMP2(3,2)
      A(2,3,ICRYS) = FPTINV(1,2,ICRYS)*TMP2(1,3) +
     &                FPTINV(2,2,ICRYS)*TMP2(2,3) +
     &                FPTINV(3,2,ICRYS)*TMP2(3,3)
      A(3,1,ICRYS) = FPTINV(1,3,ICRYS)*TMP2(1,1) +
     &                FPTINV(2,3,ICRYS)*TMP2(2,1) +
     &                FPTINV(3,3,ICRYS)*TMP2(3,1)
      A(3,2,ICRYS) = FPTINV(1,3,ICRYS)*TMP2(1,2) +
     &                FPTINV(2,3,ICRYS)*TMP2(2,2) +
     &                FPTINV(3,3,ICRYS)*TMP2(3,2)
      A(3,3,ICRYS) = FPTINV(1,3,ICRYS)*TMP2(1,3) +
     &                FPTINV(2,3,ICRYS)*TMP2(2,3) +
     &                FPTINV(3,3,ICRYS)*TMP2(3,3)



C
C    COMPUTE TBTR
C
        DO 10 J=1,3
        DO 10 K=1,3
10       TMP2(J,K)=A(J,K,ICRYS)-ONET(J,K)
        TMP3(1,1) = QT(1,1,ICRYS)*TMP2(1,1) +
     &                QT(1,2,ICRYS)*TMP2(2,1) +
     &                QT(1,3,ICRYS)*TMP2(3,1)
      TMP3(1,2) = QT(1,1,ICRYS)*TMP2(1,2) +
     &                QT(1,2,ICRYS)*TMP2(2,2) +
     &                QT(1,3,ICRYS)*TMP2(3,2)
      TMP3(1,3) = QT(1,1,ICRYS)*TMP2(1,3) +
     &                QT(1,2,ICRYS)*TMP2(2,3) +
     &                QT(1,3,ICRYS)*TMP2(3,3)
      TMP3(2,1) = QT(2,1,ICRYS)*TMP2(1,1) +
     &                QT(2,2,ICRYS)*TMP2(2,1) +
     &                QT(2,3,ICRYS)*TMP2(3,1)
      TMP3(2,2) = QT(2,1,ICRYS)*TMP2(1,2) +
     &                QT(2,2,ICRYS)*TMP2(2,2) +
     &                QT(2,3,ICRYS)*TMP2(3,2)
      TMP3(2,3) = QT(2,1,ICRYS)*TMP2(1,3) +
     &                QT(2,2,ICRYS)*TMP2(2,3) +
     &                QT(2,3,ICRYS)*TMP2(3,3)
      TMP3(3,1) = QT(3,1,ICRYS)*TMP2(1,1) +
     &                QT(3,2,ICRYS)*TMP2(2,1) +
     &                QT(3,3,ICRYS)*TMP2(3,1)
      TMP3(3,2) = QT(3,1,ICRYS)*TMP2(1,2) +
     &                QT(3,2,ICRYS)*TMP2(2,2) +
     &                QT(3,3,ICRYS)*TMP2(3,2)
      TMP3(3,3) = QT(3,1,ICRYS)*TMP2(1,3) +
     &                QT(3,2,ICRYS)*TMP2(2,3) +
     &                QT(3,3,ICRYS)*TMP2(3,3)


        EC(1,1) = TMP3(1,1)*QMAT(1,1,ICRYS) +
     &                TMP3(1,2)*QMAT(2,1,ICRYS) +
     &                TMP3(1,3)*QMAT(3,1,ICRYS)
      EC(1,2) = TMP3(1,1)*QMAT(1,2,ICRYS) +
     &                TMP3(1,2)*QMAT(2,2,ICRYS) +
     &                TMP3(1,3)*QMAT(3,2,ICRYS)
      EC(1,3) = TMP3(1,1)*QMAT(1,3,ICRYS) +
     &                TMP3(1,2)*QMAT(2,3,ICRYS) +
     &                TMP3(1,3)*QMAT(3,3,ICRYS)
      EC(2,1) = TMP3(2,1)*QMAT(1,1,ICRYS) +
     &                TMP3(2,2)*QMAT(2,1,ICRYS) +
     &                TMP3(2,3)*QMAT(3,1,ICRYS)
      EC(2,2) = TMP3(2,1)*QMAT(1,2,ICRYS) +
     &                TMP3(2,2)*QMAT(2,2,ICRYS) +
     &                TMP3(2,3)*QMAT(3,2,ICRYS)
      EC(2,3) = TMP3(2,1)*QMAT(1,3,ICRYS) +
     &                TMP3(2,2)*QMAT(2,3,ICRYS) +
     &                TMP3(2,3)*QMAT(3,3,ICRYS)
      EC(3,1) = TMP3(3,1)*QMAT(1,1,ICRYS) +
     &                TMP3(3,2)*QMAT(2,1,ICRYS) +
     &                TMP3(3,3)*QMAT(3,1,ICRYS)
      EC(3,2) = TMP3(3,1)*QMAT(1,2,ICRYS) +
     &                TMP3(3,2)*QMAT(2,2,ICRYS) +
     &                TMP3(3,3)*QMAT(3,2,ICRYS)
      EC(3,3) = TMP3(3,1)*QMAT(1,3,ICRYS) +
     &                TMP3(3,2)*QMAT(2,3,ICRYS) +
     &                TMP3(3,3)*QMAT(3,3,ICRYS)


        TC(1,1)=0.5*(C11*EC(1,1)+C12*EC(2,2)+C12*EC(3,3))
        TC(2,2)=0.5*(C12*EC(1,1)+C11*EC(2,2)+C12*EC(3,3))
        TC(3,3)=0.5*(C12*EC(1,1)+C12*EC(2,2)+C11*EC(3,3))
        TC(1,2)=0.5*C44*EC(1,2)
        TC(1,3)=0.5*C44*EC(1,3)
        TC(2,3)=0.5*C44*EC(2,3)
        TC(2,1)=TC(1,2)
        TC(3,1)=TC(1,3)
        TC(3,2)=TC(2,3)
        TMP2(1,1) = QMAT(1,1,ICRYS)*TC(1,1) +
     &                QMAT(1,2,ICRYS)*TC(2,1) +
     &                QMAT(1,3,ICRYS)*TC(3,1)
      TMP2(1,2) = QMAT(1,1,ICRYS)*TC(1,2) +
     &                QMAT(1,2,ICRYS)*TC(2,2) +
     &                QMAT(1,3,ICRYS)*TC(3,2)
      TMP2(1,3) = QMAT(1,1,ICRYS)*TC(1,3) +
     &                QMAT(1,2,ICRYS)*TC(2,3) +
     &                QMAT(1,3,ICRYS)*TC(3,3)
      TMP2(2,1) = QMAT(2,1,ICRYS)*TC(1,1) +
     &                QMAT(2,2,ICRYS)*TC(2,1) +
     &                QMAT(2,3,ICRYS)*TC(3,1)
      TMP2(2,2) = QMAT(2,1,ICRYS)*TC(1,2) +
     &                QMAT(2,2,ICRYS)*TC(2,2) +
     &                QMAT(2,3,ICRYS)*TC(3,2)
      TMP2(2,3) = QMAT(2,1,ICRYS)*TC(1,3) +
     &                QMAT(2,2,ICRYS)*TC(2,3) +
     &                QMAT(2,3,ICRYS)*TC(3,3)
      TMP2(3,1) = QMAT(3,1,ICRYS)*TC(1,1) +
     &                QMAT(3,2,ICRYS)*TC(2,1) +
     &                QMAT(3,3,ICRYS)*TC(3,1)
      TMP2(3,2) = QMAT(3,1,ICRYS)*TC(1,2) +
     &                QMAT(3,2,ICRYS)*TC(2,2) +
     &                QMAT(3,3,ICRYS)*TC(3,2)
      TMP2(3,3) = QMAT(3,1,ICRYS)*TC(1,3) +
     &                QMAT(3,2,ICRYS)*TC(2,3) +
     &                QMAT(3,3,ICRYS)*TC(3,3)


        TBTR(1,1,ICRYS) = TMP2(1,1)*QT(1,1,ICRYS) +
     &                TMP2(1,2)*QT(2,1,ICRYS) +
     &                TMP2(1,3)*QT(3,1,ICRYS)
      TBTR(1,2,ICRYS) = TMP2(1,1)*QT(1,2,ICRYS) +
     &                TMP2(1,2)*QT(2,2,ICRYS) +
     &                TMP2(1,3)*QT(3,2,ICRYS)
      TBTR(1,3,ICRYS) = TMP2(1,1)*QT(1,3,ICRYS) +
     &                TMP2(1,2)*QT(2,3,ICRYS) +
     &                TMP2(1,3)*QT(3,3,ICRYS)
      TBTR(2,1,ICRYS) = TMP2(2,1)*QT(1,1,ICRYS) +
     &                TMP2(2,2)*QT(2,1,ICRYS) +
     &                TMP2(2,3)*QT(3,1,ICRYS)
      TBTR(2,2,ICRYS) = TMP2(2,1)*QT(1,2,ICRYS) +
     &                TMP2(2,2)*QT(2,2,ICRYS) +
     &                TMP2(2,3)*QT(3,2,ICRYS)
      TBTR(2,3,ICRYS) = TMP2(2,1)*QT(1,3,ICRYS) +
     &                TMP2(2,2)*QT(2,3,ICRYS) +
     &                TMP2(2,3)*QT(3,3,ICRYS)
      TBTR(3,1,ICRYS) = TMP2(3,1)*QT(1,1,ICRYS) +
     &                TMP2(3,2)*QT(2,1,ICRYS) +
     &                TMP2(3,3)*QT(3,1,ICRYS)
      TBTR(3,2,ICRYS) = TMP2(3,1)*QT(1,2,ICRYS) +
     &                TMP2(3,2)*QT(2,2,ICRYS) +
     &                TMP2(3,3)*QT(3,2,ICRYS)
      TBTR(3,3,ICRYS) = TMP2(3,1)*QT(1,3,ICRYS) +
     &                TMP2(3,2)*QT(2,3,ICRYS) +
     &                TMP2(3,3)*QT(3,3,ICRYS)

  
C
C    COMPUTE CALPHA AND STORE IN CMAT
C
C------------------ex sbr  FORMCMAT -------------------------------
C
	DO 100 I = 1,48
C
      TMP1(1,1,I) = A(1,1,ICRYS)*SMATG(1,1,I,ICRYS) +
     &                A(1,2,ICRYS)*SMATG(2,1,I,ICRYS) +
     &                A(1,3,ICRYS)*SMATG(3,1,I,ICRYS)
      TMP1(1,2,I) = A(1,1,ICRYS)*SMATG(1,2,I,ICRYS) +
     &                A(1,2,ICRYS)*SMATG(2,2,I,ICRYS) +
     &                A(1,3,ICRYS)*SMATG(3,2,I,ICRYS)
      TMP1(1,3,I) = A(1,1,ICRYS)*SMATG(1,3,I,ICRYS) +
     &                A(1,2,ICRYS)*SMATG(2,3,I,ICRYS) +
     &                A(1,3,ICRYS)*SMATG(3,3,I,ICRYS)
      TMP1(2,1,I) = A(2,1,ICRYS)*SMATG(1,1,I,ICRYS) +
     &                A(2,2,ICRYS)*SMATG(2,1,I,ICRYS) +
     &                A(2,3,ICRYS)*SMATG(3,1,I,ICRYS)
      TMP1(2,2,I) = A(2,1,ICRYS)*SMATG(1,2,I,ICRYS) +
     &                A(2,2,ICRYS)*SMATG(2,2,I,ICRYS) +
     &                A(2,3,ICRYS)*SMATG(3,2,I,ICRYS)
      TMP1(2,3,I) = A(2,1,ICRYS)*SMATG(1,3,I,ICRYS) +
     &                A(2,2,ICRYS)*SMATG(2,3,I,ICRYS) +
     &                A(2,3,ICRYS)*SMATG(3,3,I,ICRYS)
      TMP1(3,1,I) = A(3,1,ICRYS)*SMATG(1,1,I,ICRYS) +
     &                A(3,2,ICRYS)*SMATG(2,1,I,ICRYS) +
     &                A(3,3,ICRYS)*SMATG(3,1,I,ICRYS)
      TMP1(3,2,I) = A(3,1,ICRYS)*SMATG(1,2,I,ICRYS) +
     &                A(3,2,ICRYS)*SMATG(2,2,I,ICRYS) +
     &                A(3,3,ICRYS)*SMATG(3,2,I,ICRYS)
      TMP1(3,3,I) = A(3,1,ICRYS)*SMATG(1,3,I,ICRYS) +
     &                A(3,2,ICRYS)*SMATG(2,3,I,ICRYS) +
     &                A(3,3,ICRYS)*SMATG(3,3,I,ICRYS)


C
          BALPHA(1,1,I) = TMP1(1,1,I)+TMP1(1,1,I)
          BALPHA(1,2,I) = TMP1(1,2,I)+TMP1(2,1,I)
          BALPHA(1,3,I) = TMP1(1,3,I)+TMP1(3,1,I)
          BALPHA(2,1,I) = TMP1(2,1,I)+TMP1(1,2,I)
          BALPHA(2,2,I) = TMP1(2,2,I)+TMP1(2,2,I)
          BALPHA(2,3,I) = TMP1(2,3,I)+TMP1(3,2,I)
          BALPHA(3,1,I) = TMP1(3,1,I)+TMP1(1,3,I)
          BALPHA(3,2,I) = TMP1(3,2,I)+TMP1(2,3,I)
          BALPHA(3,3,I) = TMP1(3,3,I)+TMP1(3,3,I)
        TMP2(1,1) = QT(1,1,ICRYS)*BALPHA(1,1,I) +
     &                QT(1,2,ICRYS)*BALPHA(2,1,I) +
     &                QT(1,3,ICRYS)*BALPHA(3,1,I)
      TMP2(1,2) = QT(1,1,ICRYS)*BALPHA(1,2,I) +
     &                QT(1,2,ICRYS)*BALPHA(2,2,I) +
     &                QT(1,3,ICRYS)*BALPHA(3,2,I)
      TMP2(1,3) = QT(1,1,ICRYS)*BALPHA(1,3,I) +
     &                QT(1,2,ICRYS)*BALPHA(2,3,I) +
     &                QT(1,3,ICRYS)*BALPHA(3,3,I)
      TMP2(2,1) = QT(2,1,ICRYS)*BALPHA(1,1,I) +
     &                QT(2,2,ICRYS)*BALPHA(2,1,I) +
     &                QT(2,3,ICRYS)*BALPHA(3,1,I)
      TMP2(2,2) = QT(2,1,ICRYS)*BALPHA(1,2,I) +
     &                QT(2,2,ICRYS)*BALPHA(2,2,I) +
     &                QT(2,3,ICRYS)*BALPHA(3,2,I)
      TMP2(2,3) = QT(2,1,ICRYS)*BALPHA(1,3,I) +
     &                QT(2,2,ICRYS)*BALPHA(2,3,I) +
     &                QT(2,3,ICRYS)*BALPHA(3,3,I)
      TMP2(3,1) = QT(3,1,ICRYS)*BALPHA(1,1,I) +
     &                QT(3,2,ICRYS)*BALPHA(2,1,I) +
     &                QT(3,3,ICRYS)*BALPHA(3,1,I)
      TMP2(3,2) = QT(3,1,ICRYS)*BALPHA(1,2,I) +
     &                QT(3,2,ICRYS)*BALPHA(2,2,I) +
     &                QT(3,3,ICRYS)*BALPHA(3,2,I)
      TMP2(3,3) = QT(3,1,ICRYS)*BALPHA(1,3,I) +
     &                QT(3,2,ICRYS)*BALPHA(2,3,I) +
     &                QT(3,3,ICRYS)*BALPHA(3,3,I)


        EC(1,1) = TMP2(1,1)*QMAT(1,1,ICRYS) +
     &                TMP2(1,2)*QMAT(2,1,ICRYS) +
     &                TMP2(1,3)*QMAT(3,1,ICRYS)
      EC(1,2) = TMP2(1,1)*QMAT(1,2,ICRYS) +
     &                TMP2(1,2)*QMAT(2,2,ICRYS) +
     &                TMP2(1,3)*QMAT(3,2,ICRYS)
      EC(1,3) = TMP2(1,1)*QMAT(1,3,ICRYS) +
     &                TMP2(1,2)*QMAT(2,3,ICRYS) +
     &                TMP2(1,3)*QMAT(3,3,ICRYS)
      EC(2,1) = TMP2(2,1)*QMAT(1,1,ICRYS) +
     &                TMP2(2,2)*QMAT(2,1,ICRYS) +
     &                TMP2(2,3)*QMAT(3,1,ICRYS)
      EC(2,2) = TMP2(2,1)*QMAT(1,2,ICRYS) +
     &                TMP2(2,2)*QMAT(2,2,ICRYS) +
     &                TMP2(2,3)*QMAT(3,2,ICRYS)
      EC(2,3) = TMP2(2,1)*QMAT(1,3,ICRYS) +
     &                TMP2(2,2)*QMAT(2,3,ICRYS) +
     &                TMP2(2,3)*QMAT(3,3,ICRYS)
      EC(3,1) = TMP2(3,1)*QMAT(1,1,ICRYS) +
     &                TMP2(3,2)*QMAT(2,1,ICRYS) +
     &                TMP2(3,3)*QMAT(3,1,ICRYS)
      EC(3,2) = TMP2(3,1)*QMAT(1,2,ICRYS) +
     &                TMP2(3,2)*QMAT(2,2,ICRYS) +
     &                TMP2(3,3)*QMAT(3,2,ICRYS)
      EC(3,3) = TMP2(3,1)*QMAT(1,3,ICRYS) +
     &                TMP2(3,2)*QMAT(2,3,ICRYS) +
     &                TMP2(3,3)*QMAT(3,3,ICRYS)


        TC(1,1)=0.5*(C11*EC(1,1)+C12*EC(2,2)+C12*EC(3,3))
        TC(2,2)=0.5*(C12*EC(1,1)+C11*EC(2,2)+C12*EC(3,3))
        TC(3,3)=0.5*(C12*EC(1,1)+C12*EC(2,2)+C11*EC(3,3))
        TC(1,2)=0.5*C44*EC(1,2)
        TC(1,3)=0.5*C44*EC(1,3)
        TC(2,3)=0.5*C44*EC(2,3)
        TC(2,1)=TC(1,2)
        TC(3,1)=TC(1,3)
        TC(3,2)=TC(2,3)
        TMP2(1,1) = QMAT(1,1,ICRYS)*TC(1,1) +
     &                QMAT(1,2,ICRYS)*TC(2,1) +
     &                QMAT(1,3,ICRYS)*TC(3,1)
      TMP2(1,2) = QMAT(1,1,ICRYS)*TC(1,2) +
     &                QMAT(1,2,ICRYS)*TC(2,2) +
     &                QMAT(1,3,ICRYS)*TC(3,2)
      TMP2(1,3) = QMAT(1,1,ICRYS)*TC(1,3) +
     &                QMAT(1,2,ICRYS)*TC(2,3) +
     &                QMAT(1,3,ICRYS)*TC(3,3)
      TMP2(2,1) = QMAT(2,1,ICRYS)*TC(1,1) +
     &                QMAT(2,2,ICRYS)*TC(2,1) +
     &                QMAT(2,3,ICRYS)*TC(3,1)
      TMP2(2,2) = QMAT(2,1,ICRYS)*TC(1,2) +
     &                QMAT(2,2,ICRYS)*TC(2,2) +
     &                QMAT(2,3,ICRYS)*TC(3,2)
      TMP2(2,3) = QMAT(2,1,ICRYS)*TC(1,3) +
     &                QMAT(2,2,ICRYS)*TC(2,3) +
     &                QMAT(2,3,ICRYS)*TC(3,3)
      TMP2(3,1) = QMAT(3,1,ICRYS)*TC(1,1) +
     &                QMAT(3,2,ICRYS)*TC(2,1) +
     &                QMAT(3,3,ICRYS)*TC(3,1)
      TMP2(3,2) = QMAT(3,1,ICRYS)*TC(1,2) +
     &                QMAT(3,2,ICRYS)*TC(2,2) +
     &                QMAT(3,3,ICRYS)*TC(3,2)
      TMP2(3,3) = QMAT(3,1,ICRYS)*TC(1,3) +
     &                QMAT(3,2,ICRYS)*TC(2,3) +
     &                QMAT(3,3,ICRYS)*TC(3,3)


        CALPHA(1,1,I) = TMP2(1,1)*QT(1,1,ICRYS) +
     &                TMP2(1,2)*QT(2,1,ICRYS) +
     &                TMP2(1,3)*QT(3,1,ICRYS)
      CALPHA(1,2,I) = TMP2(1,1)*QT(1,2,ICRYS) +
     &                TMP2(1,2)*QT(2,2,ICRYS) +
     &                TMP2(1,3)*QT(3,2,ICRYS)
      CALPHA(1,3,I) = TMP2(1,1)*QT(1,3,ICRYS) +
     &                TMP2(1,2)*QT(2,3,ICRYS) +
     &                TMP2(1,3)*QT(3,3,ICRYS)
      CALPHA(2,1,I) = TMP2(2,1)*QT(1,1,ICRYS) +
     &                TMP2(2,2)*QT(2,1,ICRYS) +
     &                TMP2(2,3)*QT(3,1,ICRYS)
      CALPHA(2,2,I) = TMP2(2,1)*QT(1,2,ICRYS) +
     &                TMP2(2,2)*QT(2,2,ICRYS) +
     &                TMP2(2,3)*QT(3,2,ICRYS)
      CALPHA(2,3,I) = TMP2(2,1)*QT(1,3,ICRYS) +
     &                TMP2(2,2)*QT(2,3,ICRYS) +
     &                TMP2(2,3)*QT(3,3,ICRYS)
      CALPHA(3,1,I) = TMP2(3,1)*QT(1,1,ICRYS) +
     &                TMP2(3,2)*QT(2,1,ICRYS) +
     &                TMP2(3,3)*QT(3,1,ICRYS)
      CALPHA(3,2,I) = TMP2(3,1)*QT(1,2,ICRYS) +
     &                TMP2(3,2)*QT(2,2,ICRYS) +
     &                TMP2(3,3)*QT(3,2,ICRYS)
      CALPHA(3,3,I) = TMP2(3,1)*QT(1,3,ICRYS) +
     &                TMP2(3,2)*QT(2,3,ICRYS) +
     &                TMP2(3,3)*QT(3,3,ICRYS)


C
                 CMAT(1,I,ICRYS)=CALPHA(1,1,I) 
      CMAT(2,I,ICRYS)=CALPHA(2,2,I) 
      CMAT(3,I,ICRYS)=CALPHA(3,3,I)
      CMAT(4,I,ICRYS)=CALPHA(1,2,I) 
      CMAT(5,I,ICRYS)=CALPHA(1,3,I) 
      CMAT(6,I,ICRYS)=CALPHA(2,3,I) 

C
 100    CONTINUE
C----------------------end ex -FORMCMAT--------------------------
C
	RETURN
	END
C(((((((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))
        SUBROUTINE UPDATE(ICRYS)
cvd$r   noconcur
	INCLUDE 'commonsn48.tex'
	REAL*8 LPBDT
	DIMENSION LPBDT(3,3),TMP1(3,3),FPITAU(3,3),Q(3,3),
     &        AMS(3),ANS(3)
C
C  COMPUTE FPTAU INVERSE IN GLOBAL COORDINATES
C
	DO 10 M = 1,3
	DO 10 K = 1,3
          LPBDT(K,M) = DGTAU(1,ICRYS)*SMATG(K,M,1,ICRYS)+
     &                 DGTAU(2,ICRYS)*SMATG(K,M,2,ICRYS)+
     &                 DGTAU(3,ICRYS)*SMATG(K,M,3,ICRYS)+
     &                 DGTAU(4,ICRYS)*SMATG(K,M,4,ICRYS)+
     &                 DGTAU(5,ICRYS)*SMATG(K,M,5,ICRYS)+
     &                 DGTAU(6,ICRYS)*SMATG(K,M,6,ICRYS)+
     &                 DGTAU(7,ICRYS)*SMATG(K,M,7,ICRYS)+
     &                 DGTAU(8,ICRYS)*SMATG(K,M,8,ICRYS)+
     &                 DGTAU(9,ICRYS)*SMATG(K,M,9,ICRYS)+
     &                 DGTAU(10,ICRYS)*SMATG(K,M,10,ICRYS)+
     &                 DGTAU(11,ICRYS)*SMATG(K,M,11,ICRYS)+
     &                 DGTAU(12,ICRYS)*SMATG(K,M,12,ICRYS)+
     &		       DGTAU(13,ICRYS)*SMATG(K,M,13,ICRYS)+
     &                 DGTAU(14,ICRYS)*SMATG(K,M,14,ICRYS)+
     &                 DGTAU(15,ICRYS)*SMATG(K,M,15,ICRYS)+
     &                 DGTAU(16,ICRYS)*SMATG(K,M,16,ICRYS)+
     &                 DGTAU(17,ICRYS)*SMATG(K,M,17,ICRYS)+
     &                 DGTAU(18,ICRYS)*SMATG(K,M,18,ICRYS)+
     &                 DGTAU(19,ICRYS)*SMATG(K,M,19,ICRYS)+
     &                 DGTAU(20,ICRYS)*SMATG(K,M,20,ICRYS)+
     &                 DGTAU(21,ICRYS)*SMATG(K,M,21,ICRYS)+
     &                 DGTAU(22,ICRYS)*SMATG(K,M,22,ICRYS)+
     &                 DGTAU(23,ICRYS)*SMATG(K,M,23,ICRYS)+
     &                 DGTAU(24,ICRYS)*SMATG(K,M,24,ICRYS)+
     &		       DGTAU(25,ICRYS)*SMATG(K,M,25,ICRYS)+
     &                 DGTAU(26,ICRYS)*SMATG(K,M,26,ICRYS)+
     &                 DGTAU(27,ICRYS)*SMATG(K,M,27,ICRYS)+
     &                 DGTAU(28,ICRYS)*SMATG(K,M,28,ICRYS)+
     &                 DGTAU(29,ICRYS)*SMATG(K,M,29,ICRYS)+
     &                 DGTAU(30,ICRYS)*SMATG(K,M,30,ICRYS)+
     &                 DGTAU(31,ICRYS)*SMATG(K,M,31,ICRYS)+
     &                 DGTAU(32,ICRYS)*SMATG(K,M,32,ICRYS)+
     &                 DGTAU(33,ICRYS)*SMATG(K,M,33,ICRYS)+
     &                 DGTAU(34,ICRYS)*SMATG(K,M,34,ICRYS)+
     &                 DGTAU(35,ICRYS)*SMATG(K,M,35,ICRYS)+
     &                 DGTAU(36,ICRYS)*SMATG(K,M,36,ICRYS)+
     &		       DGTAU(37,ICRYS)*SMATG(K,M,37,ICRYS)+
     &                 DGTAU(38,ICRYS)*SMATG(K,M,38,ICRYS)+
     &                 DGTAU(39,ICRYS)*SMATG(K,M,39,ICRYS)+
     &                 DGTAU(40,ICRYS)*SMATG(K,M,40,ICRYS)+
     &                 DGTAU(41,ICRYS)*SMATG(K,M,41,ICRYS)+
     &                 DGTAU(42,ICRYS)*SMATG(K,M,42,ICRYS)+
     &                 DGTAU(43,ICRYS)*SMATG(K,M,43,ICRYS)+
     &                 DGTAU(44,ICRYS)*SMATG(K,M,44,ICRYS)+
     &                 DGTAU(45,ICRYS)*SMATG(K,M,45,ICRYS)+
     &                 DGTAU(46,ICRYS)*SMATG(K,M,46,ICRYS)+
     &                 DGTAU(47,ICRYS)*SMATG(K,M,47,ICRYS)+
     &                 DGTAU(48,ICRYS)*SMATG(K,M,48,ICRYS)
	 
	 
 10        TMP1(K,M)  = ONET(K,M)-LPBDT(K,M)

 	IF(TAU.EQ.TTIME) THEN
      wstar(1,icrys) = 0.5*(lpbdt(1,2)-lpbdt(2,1))
      wstar(2,icrys) = 0.5*(lpbdt(1,3)-lpbdt(3,1))
      wstar(3,icrys) = 0.5*(lpbdt(2,3)-lpbdt(3,2))
	endif
C
              FPITAU(1,1) = FPTINV(1,1,ICRYS)*TMP1(1,1) +
     &                FPTINV(1,2,ICRYS)*TMP1(2,1) +
     &                FPTINV(1,3,ICRYS)*TMP1(3,1)
      FPITAU(1,2) = FPTINV(1,1,ICRYS)*TMP1(1,2) +
     &                FPTINV(1,2,ICRYS)*TMP1(2,2) +
     &                FPTINV(1,3,ICRYS)*TMP1(3,2)
      FPITAU(1,3) = FPTINV(1,1,ICRYS)*TMP1(1,3) +
     &                FPTINV(1,2,ICRYS)*TMP1(2,3) +
     &                FPTINV(1,3,ICRYS)*TMP1(3,3)
      FPITAU(2,1) = FPTINV(2,1,ICRYS)*TMP1(1,1) +
     &                FPTINV(2,2,ICRYS)*TMP1(2,1) +
     &                FPTINV(2,3,ICRYS)*TMP1(3,1)
      FPITAU(2,2) = FPTINV(2,1,ICRYS)*TMP1(1,2) +
     &                FPTINV(2,2,ICRYS)*TMP1(2,2) +
     &                FPTINV(2,3,ICRYS)*TMP1(3,2)
      FPITAU(2,3) = FPTINV(2,1,ICRYS)*TMP1(1,3) +
     &                FPTINV(2,2,ICRYS)*TMP1(2,3) +
     &                FPTINV(2,3,ICRYS)*TMP1(3,3)
      FPITAU(3,1) = FPTINV(3,1,ICRYS)*TMP1(1,1) +
     &                FPTINV(3,2,ICRYS)*TMP1(2,1) +
     &                FPTINV(3,3,ICRYS)*TMP1(3,1)
      FPITAU(3,2) = FPTINV(3,1,ICRYS)*TMP1(1,2) +
     &                FPTINV(3,2,ICRYS)*TMP1(2,2) +
     &                FPTINV(3,3,ICRYS)*TMP1(3,2)
      FPITAU(3,3) = FPTINV(3,1,ICRYS)*TMP1(1,3) +
     &                FPTINV(3,2,ICRYS)*TMP1(2,3) +
     &                FPTINV(3,3,ICRYS)*TMP1(3,3)


C
              DET = FPITAU(1,1)*(FPITAU(2,2)*FPITAU(3,3)-
     &                  FPITAU(2,3)*FPITAU(3,2))-
     &       FPITAU(1,2)*(FPITAU(2,1)*FPITAU(3,3)-
     &                  FPITAU(3,1)*FPITAU(2,3))+
     &       FPITAU(1,3)*(FPITAU(2,1)*FPITAU(3,2)-
     &                  FPITAU(3,1)*FPITAU(2,2))

C
	IF(DABS(DET-ONE).GT.1.0D-3)THEN
          WRITE(9,*)'ICRYS = ',ICRYS
          WRITE(9,*)'DETERMINANT OF FPITAU = ',DET
          WRITE(9,*)'FPI'
          WRITE(9,*)((FPTINV(J,K,ICRYS),K=1,3),J=1,3)
          WRITE(9,*)'LPBDT'
          WRITE(9,*)((LPBDT(J,K),K=1,3),J=1,3)
          WRITE(9,*)'FPITAU'
          WRITE(9,*)((FPITAU(J,K),K=1,3),J=1,3)
          WRITE(9,*)'FT'
          WRITE(9,*)((FT(J,K),K=1,3),J=1,3)
          WRITE(9,*)'FTTAU'
          WRITE(9,*)((FTTAU(J,K),K=1,3),J=1,3)
          WRITE(9,*)'FTAU'
          WRITE(9,*)((FTAU(J,K),K=1,3),J=1,3)
          PAUSE
	ENDIF
C
C  NORMALIZE FPITAU SO THAT DETERMINANT IS 1.0
C
	CDET = ONE/(DET**(THIRD))
	DO 20 K = 1,3
        DO 20 J = 1,3
 20        FPITAU(J,K) = FPITAU(J,K)*CDET
C
C  COMPUTE FSTAU IN GLOBAL COORDINATES.
C
              FSTAU(1,1,ICRYS) = FTAU(1,1)*FPITAU(1,1) +
     &                FTAU(1,2)*FPITAU(2,1) +
     &                FTAU(1,3)*FPITAU(3,1)
      FSTAU(1,2,ICRYS) = FTAU(1,1)*FPITAU(1,2) +
     &                FTAU(1,2)*FPITAU(2,2) +
     &                FTAU(1,3)*FPITAU(3,2)
      FSTAU(1,3,ICRYS) = FTAU(1,1)*FPITAU(1,3) +
     &                FTAU(1,2)*FPITAU(2,3) +
     &                FTAU(1,3)*FPITAU(3,3)
      FSTAU(2,1,ICRYS) = FTAU(2,1)*FPITAU(1,1) +
     &                FTAU(2,2)*FPITAU(2,1) +
     &                FTAU(2,3)*FPITAU(3,1)
      FSTAU(2,2,ICRYS) = FTAU(2,1)*FPITAU(1,2) +
     &                FTAU(2,2)*FPITAU(2,2) +
     &                FTAU(2,3)*FPITAU(3,2)
      FSTAU(2,3,ICRYS) = FTAU(2,1)*FPITAU(1,3) +
     &                FTAU(2,2)*FPITAU(2,3) +
     &                FTAU(2,3)*FPITAU(3,3)
      FSTAU(3,1,ICRYS) = FTAU(3,1)*FPITAU(1,1) +
     &                FTAU(3,2)*FPITAU(2,1) +
     &                FTAU(3,3)*FPITAU(3,1)
      FSTAU(3,2,ICRYS) = FTAU(3,1)*FPITAU(1,2) +
     &                FTAU(3,2)*FPITAU(2,2) +
     &                FTAU(3,3)*FPITAU(3,2)
      FSTAU(3,3,ICRYS) = FTAU(3,1)*FPITAU(1,3) +
     &                FTAU(3,2)*FPITAU(2,3) +
     &                FTAU(3,3)*FPITAU(3,3)


C
C  COMPUTE CAUCHY STRESS IN GLOBAL COORDINATES AND UPDATE TBMAT,FPTINV
C

              TMP1(1,1) = FSTAU(1,1,ICRYS)*TBTAU(1,1,ICRYS) +
     &                FSTAU(1,2,ICRYS)*TBTAU(2,1,ICRYS) +
     &                FSTAU(1,3,ICRYS)*TBTAU(3,1,ICRYS)
      TMP1(1,2) = FSTAU(1,1,ICRYS)*TBTAU(1,2,ICRYS) +
     &                FSTAU(1,2,ICRYS)*TBTAU(2,2,ICRYS) +
     &                FSTAU(1,3,ICRYS)*TBTAU(3,2,ICRYS)
      TMP1(1,3) = FSTAU(1,1,ICRYS)*TBTAU(1,3,ICRYS) +
     &                FSTAU(1,2,ICRYS)*TBTAU(2,3,ICRYS) +
     &                FSTAU(1,3,ICRYS)*TBTAU(3,3,ICRYS)
      TMP1(2,1) = FSTAU(2,1,ICRYS)*TBTAU(1,1,ICRYS) +
     &                FSTAU(2,2,ICRYS)*TBTAU(2,1,ICRYS) +
     &                FSTAU(2,3,ICRYS)*TBTAU(3,1,ICRYS)
      TMP1(2,2) = FSTAU(2,1,ICRYS)*TBTAU(1,2,ICRYS) +
     &                FSTAU(2,2,ICRYS)*TBTAU(2,2,ICRYS) +
     &                FSTAU(2,3,ICRYS)*TBTAU(3,2,ICRYS)
      TMP1(2,3) = FSTAU(2,1,ICRYS)*TBTAU(1,3,ICRYS) +
     &                FSTAU(2,2,ICRYS)*TBTAU(2,3,ICRYS) +
     &                FSTAU(2,3,ICRYS)*TBTAU(3,3,ICRYS)
      TMP1(3,1) = FSTAU(3,1,ICRYS)*TBTAU(1,1,ICRYS) +
     &                FSTAU(3,2,ICRYS)*TBTAU(2,1,ICRYS) +
     &                FSTAU(3,3,ICRYS)*TBTAU(3,1,ICRYS)
      TMP1(3,2) = FSTAU(3,1,ICRYS)*TBTAU(1,2,ICRYS) +
     &                FSTAU(3,2,ICRYS)*TBTAU(2,2,ICRYS) +
     &                FSTAU(3,3,ICRYS)*TBTAU(3,2,ICRYS)
      TMP1(3,3) = FSTAU(3,1,ICRYS)*TBTAU(1,3,ICRYS) +
     &                FSTAU(3,2,ICRYS)*TBTAU(2,3,ICRYS) +
     &                FSTAU(3,3,ICRYS)*TBTAU(3,3,ICRYS)


              TTAU(1,1,ICRYS) = TMP1(1,1)*FSTAU(1,1,ICRYS) +
     &                TMP1(1,2)*FSTAU(1,2,ICRYS) +
     &                TMP1(1,3)*FSTAU(1,3,ICRYS)
      TTAU(1,2,ICRYS) = TMP1(1,1)*FSTAU(2,1,ICRYS) +
     &                TMP1(1,2)*FSTAU(2,2,ICRYS) +
     &                TMP1(1,3)*FSTAU(2,3,ICRYS)
      TTAU(1,3,ICRYS) = TMP1(1,1)*FSTAU(3,1,ICRYS) +
     &                TMP1(1,2)*FSTAU(3,2,ICRYS) +
     &                TMP1(1,3)*FSTAU(3,3,ICRYS)
      TTAU(2,1,ICRYS) = TMP1(2,1)*FSTAU(1,1,ICRYS) +
     &                TMP1(2,2)*FSTAU(1,2,ICRYS) +
     &                TMP1(2,3)*FSTAU(1,3,ICRYS)
      TTAU(2,2,ICRYS) = TMP1(2,1)*FSTAU(2,1,ICRYS) +
     &                TMP1(2,2)*FSTAU(2,2,ICRYS) +
     &                TMP1(2,3)*FSTAU(2,3,ICRYS)
      TTAU(2,3,ICRYS) = TMP1(2,1)*FSTAU(3,1,ICRYS) +
     &                TMP1(2,2)*FSTAU(3,2,ICRYS) +
     &                TMP1(2,3)*FSTAU(3,3,ICRYS)
      TTAU(3,1,ICRYS) = TMP1(3,1)*FSTAU(1,1,ICRYS) +
     &                TMP1(3,2)*FSTAU(1,2,ICRYS) +
     &                TMP1(3,3)*FSTAU(1,3,ICRYS)
      TTAU(3,2,ICRYS) = TMP1(3,1)*FSTAU(2,1,ICRYS) +
     &                TMP1(3,2)*FSTAU(2,2,ICRYS) +
     &                TMP1(3,3)*FSTAU(2,3,ICRYS)
      TTAU(3,3,ICRYS) = TMP1(3,1)*FSTAU(3,1,ICRYS) +
     &                TMP1(3,2)*FSTAU(3,2,ICRYS) +
     &                TMP1(3,3)*FSTAU(3,3,ICRYS)


	      DET = FSTAU(1,1,ICRYS)*(FSTAU(2,2,ICRYS)*FSTAU(3,3,ICRYS)-
     &                  FSTAU(2,3,ICRYS)*FSTAU(3,2,ICRYS))-
     &       FSTAU(1,2,ICRYS)*(FSTAU(2,1,ICRYS)*FSTAU(3,3,ICRYS)-
     &                  FSTAU(3,1,ICRYS)*FSTAU(2,3,ICRYS))+
     &       FSTAU(1,3,ICRYS)*(FSTAU(2,1,ICRYS)*FSTAU(3,2,ICRYS)-
     &                  FSTAU(3,1,ICRYS)*FSTAU(2,2,ICRYS))

C
	DETINV = ONE/DET
	DO 30 J = 1,3
	DO 30 K = 1,3
	    TTAU(J,K,ICRYS) = TTAU(J,K,ICRYS)*DETINV
            TBTMAT(J,K,ICRYS) = TBTAU(J,K,ICRYS)
 30         FPTINV(J,K,ICRYS) = FPITAU(J,K)
C
        IF(LFLAG.EQ.4.AND.NSB(ICRYS).EQ.0)THEN
        GAMAX = ACCGAM(NSYS(ICRYS),ICRYS)
        IF(GAMAX.LT.0.3)GO TO 100
C       
        CALL DECOMP(ICRYS)

              Q(1,1) = RSTAU(1,1,ICRYS)*QMAT(1,1,ICRYS) +
     &                RSTAU(1,2,ICRYS)*QMAT(2,1,ICRYS) +
     &                RSTAU(1,3,ICRYS)*QMAT(3,1,ICRYS)
      Q(1,2) = RSTAU(1,1,ICRYS)*QMAT(1,2,ICRYS) +
     &                RSTAU(1,2,ICRYS)*QMAT(2,2,ICRYS) +
     &                RSTAU(1,3,ICRYS)*QMAT(3,2,ICRYS)
      Q(1,3) = RSTAU(1,1,ICRYS)*QMAT(1,3,ICRYS) +
     &                RSTAU(1,2,ICRYS)*QMAT(2,3,ICRYS) +
     &                RSTAU(1,3,ICRYS)*QMAT(3,3,ICRYS)
      Q(2,1) = RSTAU(2,1,ICRYS)*QMAT(1,1,ICRYS) +
     &                RSTAU(2,2,ICRYS)*QMAT(2,1,ICRYS) +
     &                RSTAU(2,3,ICRYS)*QMAT(3,1,ICRYS)
      Q(2,2) = RSTAU(2,1,ICRYS)*QMAT(1,2,ICRYS) +
     &                RSTAU(2,2,ICRYS)*QMAT(2,2,ICRYS) +
     &                RSTAU(2,3,ICRYS)*QMAT(3,2,ICRYS)
      Q(2,3) = RSTAU(2,1,ICRYS)*QMAT(1,3,ICRYS) +
     &                RSTAU(2,2,ICRYS)*QMAT(2,3,ICRYS) +
     &                RSTAU(2,3,ICRYS)*QMAT(3,3,ICRYS)
      Q(3,1) = RSTAU(3,1,ICRYS)*QMAT(1,1,ICRYS) +
     &                RSTAU(3,2,ICRYS)*QMAT(2,1,ICRYS) +
     &                RSTAU(3,3,ICRYS)*QMAT(3,1,ICRYS)
      Q(3,2) = RSTAU(3,1,ICRYS)*QMAT(1,2,ICRYS) +
     &                RSTAU(3,2,ICRYS)*QMAT(2,2,ICRYS) +
     &                RSTAU(3,3,ICRYS)*QMAT(3,2,ICRYS)
      Q(3,3) = RSTAU(3,1,ICRYS)*QMAT(1,3,ICRYS) +
     &                RSTAU(3,2,ICRYS)*QMAT(2,3,ICRYS) +
     &                RSTAU(3,3,ICRYS)*QMAT(3,3,ICRYS)

	  
        DO 35 I=1,48
        IF(ACCGAM(I,ICRYS).LT.GAMAX)GO TO 35
        DO 40 J=1,3
        AMS(J) = 0.0
        ANS(J) = 0.0
        DO 40 K = 1,3
        AMS(J) = AMS(J)+Q(J,K)*AM(I,K)
40      ANS(J) = ANS(J)+Q(J,K)*AN(I,K)
        
        ANG1 = 35.0*PI/180.0
        CANG1 = DCOS(ANG1)
        SANG1 = DSIN(ANG1)
        SBD1 = DABS(AMS(1)*CANG1+AMS(3)*SANG1) 
        SBD2 = DABS(-AMS(1)*CANG1+AMS(3)*SANG1) 
        SBP1 = DABS(-ANS(1)*SANG1+ANS(3)*CANG1)
        SBP2 = DABS( ANS(1)*SANG1+ANS(3)*CANG1)
        IF(SBD1.GT.1.0.OR.SBD2.GT.1.0.OR.SBP1.GT.1.0.OR.SBP2.GT.1.0)
     &    WRITE(9,*)'SBD. OR. SBP. GT. 1.0'
        IF((1.0-SBD1).LE.0.1.AND.(1.0-SBP1).LE.0.1)THEN
          IF(NSB(ICRYS).NE.0)WRITE(9,*)'TWO SHEAR BANDS!!!'
          NSB(ICRYS)=1
          SBTIME(ICRYS) = TAU
        ENDIF
        IF((1.0-SBD2).LE.0.1.AND.(1.0-SBP2).LE.0.1)THEN
          IF(NSB(ICRYS).NE.0)WRITE(9,*)'TWO SHEAR BANDS!!!'
          NSB(ICRYS)=-1
          SBTIME(ICRYS) = TAU
        ENDIF
35      CONTINUE
        ENDIF
100     CONTINUE
             
	RETURN
	END
