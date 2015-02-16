C	********************************************************************
      SUBROUTINE UMAT(STRESS,STATEV,DDSDDE,SSE,SPD,SCD,
     1  RPL,DDSDDT,DRPLDE,DRPLDT,
     2  STRAN,DSTRAN,TIM,DTIME,TEMP,DTEMP,PREDEF,DPRED, CMNAME,
     3  NDI,NSHR,NTENS,NSTATV,PROPS,NPROPS,COORDS,DROT,PNEWDT,
     4  CELENT,DFGRD0,DFGRD1,NOEL,NPT,LAYER,KSPT,KSTEP,KINC)      
C
C     INCLUDE 'ABA_PARAM.INC'
      INCLUDE'/nv/hp22/dpatel73/CPFEM/Classical/commonsn.txt'
      CHARACTER*8 CMNAME
      DIMENSION STRESS(NTENS),STATEV(NSTATV),
     1 DDSDDE(NTENS,NTENS),DDSDDT(NTENS),DRPLDE(NTENS),
     2 STRAN(NTENS),DSTRAN(NTENS),TIM(2),PREDEF(1),DPRED(1),
     3 PROPS(NPROPS),COORDS(3),DROT(3,3),DROTTRANS(3,3),
     4 DFGRD0(3,3),DFGRD1(3,3)
C
C	Added by Hamad F. Al-Harbi: June 19, 2012
      DIMENSION TTAUV(6), DGTAU(48),RSSTAU(48),DTDD(6,6),TBTRV(6),
     &FST(3,3),RTTAU(3,3),UTTAU(3,3),TBTAUV(6),
     &TENSP(6,6),CMAT(6,48),TENSPP(3,3,6),
     &CRSS(48),CRSST(48),FPINVT(3,3),FPITAU(3,3),
     &OLDJAC(NTENS,NTENS),AvgStress(6),AvgJAC(6,6)
!	------------------------------------------------------------------
	LHAMADTEST=0	! Just for debugging
	IF (LHAMADTEST ==1) print*,'Beginning of Subrt: UMAT',NOEL,NPT
      TIME = TIM(2)
!	------------------------------------------------------------------
C	Added by Hamad F. Al-Harbi: June 19, 2012
C
!	Read user's inputs from ABAQUS input file:
		C11	   = PROPS(1)	! Elastic constant C11 in the crystal frame
		C12	   = PROPS(2)	! Elastic constant C12 in the crystal frame
		C44	   = PROPS(3)	! Elastic constant C44 in the crystal frame
		XM	   = PROPS(4)	! Rate sensitivity,m (metals ~0.01 at room temp.)
		SO	   = PROPS(5)	! Initial slip resistance
		HO	   = PROPS(6)	! Hardening rate, ho
		SS	   = PROPS(7)	! Saturation value, Ss
		AEXP   = PROPS(8)	! Hardening expondent, a
        NCRYS  = PROPS(9)   ! No. of crystals per integration point
        Nslip  = PROPS(10)  ! No. of slip systems
!	------------------------------------------------------------------
C     Used later to save F(t) at the last time step for texture printing
      TEXTME=099.99   ! change based on total time (e.g. if ttime=1, let textme=0.99)
C     ------------------------------------------------------------------      
        IF (NCRYS > MAXCRYS) THEN
           WRITE (*,*) '***********************************************'
           WRITE (*,*) 'ERROR: NCRYS > MAXCRYS, Pls change MAXCRYS'
           WRITE (*,*) '***********************************************'
           CALL XIT
        ENDIF
C
!	==================================================================      
C       INITIALZE; DONE ONLY IN THE FIRST INCREMENT OF THE FIRST STEP (FOR ALL NPT)		    
C
	IF (KSTEP == 1) THEN
	   IF (KINC == 1) THEN

	      CALL INITIAL(C11,C12,C44,NCRYS)
              TFLAG = TIME  !not used 
!	------------------------------------------------------------------             
C     For the 1st increment: Start Loop over all crystals for each integration point
C     First, initialize the average Jacobian values to zero
      outer0: DO J1 = 1,6    
          inner0: DO K1 = 1,6
                AvgJAC(K1,J1) = 0.0
          END DO inner0
      END DO outer0 
C      
      icount=1 
      InitialCrystalLoop: DO icrys=1,NCRYS
      ind=icount+Nslip
C
        STATEV(icount:ind-1)=SO  ! For 1st increment: CRSST=SO
C
		STATEV(ind)=1.0	             ! FPINVT(1,1)
		STATEV(ind+1)=0.0	     ! FPINVT(1,2)
		STATEV(ind+2)=0.0	     ! FPINVT(1,3)
		STATEV(ind+3)=0.0	     ! FPINVT(2,1)
		STATEV(ind+4)=1.0	     ! FPINVT(2,2)
		STATEV(ind+5)=0.0   	     ! FPINVT(2,3)
		STATEV(ind+6)=0.0   	     ! FPINVT(3,1)
		STATEV(ind+7)=0.0   	     ! FPINVT(3,2)
		STATEV(ind+8)=1.0   	     ! FPINVT(3,3)	
C
C     Compute the sum of the initial Jacobin=sum of Elasticity tensor over all crystals 
        DO 70 K1 = 1,NTENS      !NTENS=6 for 3D problem
            DO 70 K2 = 1,NTENS                
            OLDJAC(K1,K2)=ELAS(K1,K2,icrys) 
            IF(K1.GT.NDI)THEN
                OLDJAC(K1,K2) = OLDJAC(K1,K2)*0.50D0
            ENDIF
70        AvgJAC(K1,K2) = AvgJAC(K1,K2)+OLDJAC(K1,K2)
C
C     >>>>>> Go to the next crystal >>>>
      icount=icount+Nslip+9
      END DO InitialCrystalLoop 
!	--------------------------------------------------------------------
C     Compute the averge values of the Jacobian and Update state variables
      JJ=(Nslip+9)*NCRYS
      outer1: DO J1 = 1,6 
          inner1: DO K1 = 1,6
                JJ=JJ+1
                AvgJAC(K1,J1) = AvgJAC(K1,J1)/NCRYS
                OLDJAC(K1,J1)=  AvgJAC(K1,J1)
                STATEV(JJ)  = OLDJAC(K1,J1) !  where, e.g. if icount=22
                                    	   					    !       STATEV(22:27)=OLDJAC(1:6,1)
										    !		STATEV(28:33)=OLDJAC(1:6,2)
										    !		STATEV(34:39)=OLDJAC(1:6,3)
										    !		STATEV(40:45)=OLDJAC(1:6,4)
										    !		STATEV(46:51)=OLDJAC(1:6,5)
										    !		STATEV(52:57)=OLDJAC(1:6,6)
          END DO inner1
      END DO outer1	
C

!	------------------------------------------------------------------             
C            Check1 by Dipen
            !  WRITE(*,*) 'NOEL, NPT=',NOEL,NPT
            !  WRITE(201,*) 'NOEL, NPT=',NOEL,NPT
            !  WRITE(201,*) ((DFGRD1(J,K),K=1,3),J=1,3)  
            !  WRITE(201,*) '----------------------------------'
            !  WRITE(201,*) (STRAN(J),J=1,NTENS) 
            !  WRITE(205,777)KSTEP, NOEL,NPT,KINC,DTIME,TIM(2)
            !  WRITE(205,666) ((OLDJAC(J,K),K=1,6),J=1,6) 
            !  WRITE(205,*)'%-------------------------------- '


666           format(6f20.6)
777           format (4I16,2f16.9) 

             ! PAUSE   To stop 
             ! CALL XIT to exit  
!	------------------------------------------------------------------ 


	      ENDIF	    !for KINC
        ENDIF       ! for KSTEP
!	==================================================================      
!       IF DUMMY FTAU STEP GO DIRECTLY TO ELASTIC JACOBIAN
        IF (KINC == 1) THEN
		CHK=0
		DO J=1,3
		   DO K=1,3
		   	CHK=CHK+DABS(DFGRD1(K,J)-DFGRD0(K,J))
          	       END DO
		END DO
C
		If (chk <= 1.0D-10) GO TO 500
C		
        ENDIF  !for KINC
!	==================================================================      
!	^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^      
C     If increment > 1
C     Just to print to the screen (FOR A NEW TIME INCREMENT).
	IF(TIME.GT.TFLAG) THEN
C		Write(*,147)'[inc#,  dtime, time]:', KINC, dtime,time
	    TFLAG = TIME
	ENDIF
C
c      Added by Hamad
        DGMaxALL = 0.0
        DGMinALL = 99.9
C     Start Loop over all crystals for each integration point
C     First, initialize the average stress and Jacobian values to zero
      outer2: DO J1 = 1,6
          AvgStress(J1) = 0.0     
          inner2: DO K1 = 1,6
                AvgJAC(K1,J1) = 0.0
          END DO inner2
      END DO outer2
C
C      NCRYS2=0
      icount=1      
      CrystalLoop: DO icrys=1,NCRYS
C
      ind=icount+Nslip
C
	CRSST(1:Nslip)=STATEV(icount:ind-1)
C     
	FPINVT(1,1)=STATEV(ind)
	FPINVT(1,2)=STATEV(ind+1)
	FPINVT(1,3)=STATEV(ind+2)
	FPINVT(2,1)=STATEV(ind+3)
	FPINVT(2,2)=STATEV(ind+4)
	FPINVT(2,3)=STATEV(ind+5)
	FPINVT(3,1)=STATEV(ind+6)
	FPINVT(3,2)=STATEV(ind+7)
	FPINVT(3,3)=STATEV(ind+8)
!	------------------------------------------------------------------
C     CHECK IF THE JACOBIAN MUST BE EVALUATED
	  JAC1 = 1	!Hamad, June 19, 2012: Jacobian to be updated all the time
!	------------------------------------------------------------------
C     if jacobian must be evaluated performe preliminary calculations
	IF(JAC1.EQ.1) CALL PREJAC(RTTAU,UTTAU,DFGRD0,DFGRD1,TENSP,TENSPP)
!	------------------------------------------------------------------
C     COMPUTE THE TB STRESS AT PREVIOUS TIME. SERVES AS INITIAL GUESS
C     AND USED IN COMPUTING UMEROR. DENOTED AS TBTAUV.
      CALL GUESSTB(FST,DFGRD0,TBTAUV,FPINVT,icrys)
!	------------------------------------------------------------------
C     COMPUTE THE TRIAL STRESS TBTR AND CdeltaS OF SLIP SYSTEMS
C     FOR THE CURRENT CRYSTAL.
      CALL TRSTR(DFGRD1,CMAT,FPINVT,TBTRV,icrys)
!	------------------------------------------------------------------
C     TIME INTEGRATION
      ICFLAG=0
      CALL NEWT(XM,SO,HO,SS,AEXP,ICFLAG,DTIME,
     &DGTAU,RSSTAU,TBTAUV,CMAT,CRSS,CRSST,DGMAX,TBTRV,icrys)
C
C     Added by Hamad
      DGMaxALL = DMAX1(DGMAXALL, DGMAX)
      DGMinALL = DMIN1(DGMinALL, DGMAX)
C
C     Check if there have been errors computing stress
      IF(ICFLAG.EQ.1)THEN
c        WRITE(*,*) '***********************************************'
c        WRITE(*,*) 'ERROR IN COMPUTING STRESS, ICFLAG=1'
c        WRITE(*,*) 'NOEL,  NPT, DTIME,  TIME, icrys'
c        WRITE(*,*)  NOEL,NPT,DTIME,TIME,icrys
c
c
c        WRITE(*,*) 'CRSST='
c        WRITE(*,*)  CRSST
c        WRITE(*,*) 'FPINVT='
c        WRITE(*,*) ((FPINVT(J,K),K=1,3),J=1,3)
c        WRITE(*,*) 'Ft='
c        WRITE(*,*) ((DFGRD0(J,K),K=1,3),J=1,3)
c        WRITE(*,*) 'Ftau='
c        WRITE(*,*) ((DFGRD1(J,K),K=1,3),J=1,3)
        PNEWDT = 0.5
C
!       Hamad; Just for test.... DO NOT USE....DO NOT USE
!       Skip this crystal only for which the stress was not correct
C       icount=icount+Nslip+9
C       IF (NCRYS2 < NCRYS/2) GO TO 500   ! If stress cannot be found for many crystals..skip all
C       Cycle CrystalLoop
C
        GO TO 500          ! Hamad: Use this
      ENDIF
!	------------------------------------------------------------------
      CALL UPDATE(XM,SS,AEXP,TTAUV,DGTAU,
     &   RSSTAU,DTDD,FST,RTTAU,UTTAU,DFGRD1,TBTAUV,TENSP,
     &   CMAT,TENSPP,CRSS,CRSST,FPINVT,FPITAU,JAC1,icrys)
!	------------------------------------------------------------------
C	Added by Hamad F. Al-Harbi: June 19, 2012
!	Update slip reistance, CRSS
!	NOTE: This update occurs only when the current iteration is the last one in the current increment
!		  i.e. STATEV doesn't change if the current iteration is not the last one
!	NOTE: STATEV enters the UMAT with 0.0D0 values for the 1st increment even if you give them values for trial iterations 	    
		STATEV(icount:ind-1)=CRSS(1:Nslip)	
C
		STATEV(ind)  =FPITAU(1,1)
		STATEV(ind+1)=FPITAU(1,2)
		STATEV(ind+2)=FPITAU(1,3)
		STATEV(ind+3)=FPITAU(2,1)
		STATEV(ind+4)=FPITAU(2,2)
		STATEV(ind+5)=FPITAU(2,3)
		STATEV(ind+6)=FPITAU(3,1)
		STATEV(ind+7)=FPITAU(3,2)
		STATEV(ind+8)=FPITAU(3,3)
!	------------------------------------------------------------------
C     Compute the sum of the stress and Jacobian over all crystals 
      outer3: DO J1 = 1,6
          AvgStress(J1) = AvgStress(J1)+TTAUV(J1)        
          inner3: DO K1 = 1,6
                AvgJAC(K1,J1) = AvgJAC(K1,J1)+DTDD(K1,J1)
          END DO inner3
      END DO outer3
C
C     >>>>> Go to the next crystal >>>>>>
      icount=icount+Nslip+9
C      NCRYS2=NCRYS2+1
C
      END DO CrystalLoop
C      IF (NCRYS2 > NCRYS) NCRYS2=NCRYS
!	==================================================================
!	^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C     Compute the averge values of the stress and Jacobian
      outer4: DO J1 = 1,6
          AvgStress(J1) = AvgStress(J1)/NCRYS
          inner4: DO K1 = 1,6
                AvgJAC(K1,J1) = AvgJAC(K1,J1)/NCRYS
          END DO inner4
      END DO outer4						
!	------------------------------------------------------------------
C	PLACING STRESS AND JACOBIAN IN CORRECT PLACES FOR ABAQUS
        JJ=(Nslip+9)*NCRYS
        DO 400 J = 1,6
          STRESS(J) = AvgStress(J)
C	      IF(JAC1.EQ.0)GO TO 400    ! Hamad: In this version, JAC1 = 1
          DO 350 K = 1,6
			    JJ=JJ+1 
                OLDJAC(K,J) = AvgJAC(K,J)
                STATEV(JJ)  = OLDJAC(K,J)	!Hamad: MODIFY LATER AND REMOVE OLDJAC
 350      CONTINUE 
 400    CONTINUE
!	------------------------------------------------------------------
C     FILL UP JACOBIAN FOR ABAQUS
C     By default: Stress is passed from the previous increment
C             but Jacobian (DDSDDE) is passed as 0.0
500    CONTINUE
C
        JJ=(Nslip+9)*NCRYS
        DO 600 I = 1,NTENS
        DO 600 J = 1,NTENS
            JJ=JJ+1
600         DDSDDE(J,I) = STATEV(JJ)
!     ------------------------------------------------------------------
C     This is to save F(t) at the last time step..used later for texture printing
CCCCC			      IF(TIME+DTIME .GT. TEXTME) THEN
CCCCC			        STATEV(icount) = DFGRD0(1,1)
CCCCC					STATEV(icount+1)=DFGRD0(1,2)
CCCCC					STATEV(icount+2)=DFGRD0(1,3)
CCCCC					STATEV(icount+3)=DFGRD0(2,1)
CCCCC					STATEV(icount+4)=DFGRD0(2,2)
CCCCC					STATEV(icount+5)=DFGRD0(2,3)
CCCCC					STATEV(icount+6)=DFGRD0(3,1)
CCCCC					STATEV(icount+7)=DFGRD0(3,2)
CCCCC					STATEV(icount+8)=DFGRD0(3,3)
CCCCC			      ENDIF
!	------------------------------------------------------------------	
C     COMPUTE UMEROR FOR USE IN EXECS
        JFLAG=1	!By Hamad..Modify Later JFLAG=Iteration# per increment
c        commented by Hamad: check first with Dr.Kalidindi: DGMaxALL vs DGMinALL
c        IF(PNEWDT.LT.1.0) RETURN
c        RDG = DGMinALL/0.02                ! WHAT SHOULD BE USED: DGMaxALL OR  DGMinALL
c        PNEWDT = 1.0
c        IF(RDG.LE.0.75.AND.JFLAG.LE.4)PNEWDT = 1.25
c        IF(RDG.LE.0.5.AND.JFLAG.LE.3)PNEWDT = 1.5
c        IF(RDG.GT.1.25)PNEWDT = 0.5
!	------------------------------------------------------------------
147    FORMAT(A25,1I4,2f9.4) 				
C
	IF (LHAMADTEST ==1) print*,'End of Subrt: UMAT',NOEL,NPT
      RETURN
      END
!	============================================================================================      
!	============================================================================================ 
        SUBROUTINE GUESSTB(FST,FT,TBTAUV,FPINVT,icrys)
      INCLUDE'/nv/hp22/dpatel73/CPFEM/Classical/commonsn.txt'
      DIMENSION TMP(3,3),ES(3,3),ESV(6),FST(3,3),FT(3,3),TBTAUV(6),
     &FPINVT(3,3)

	DIMENSION ONET(3,3)
	DATA ONET(1,1),ONET(1,2),ONET(1,3),
     &	 ONET(2,1),ONET(2,2),ONET(2,3),
     &     ONET(3,1),ONET(3,2),ONET(3,3)
     & /1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0/
C
	IF (LHAMADTEST ==1) print*,'Begin of Subrt:GUESSTB'
C
       FST(1,1) = FT(1,1)*FPINVT(1,1) +
     &                FT(1,2)*FPINVT(2,1) +
     &                FT(1,3)*FPINVT(3,1)
      FST(1,2) = FT(1,1)*FPINVT(1,2) +
     &                FT(1,2)*FPINVT(2,2) +
     &                FT(1,3)*FPINVT(3,2)
      FST(1,3) = FT(1,1)*FPINVT(1,3) +
     &                FT(1,2)*FPINVT(2,3) +
     &                FT(1,3)*FPINVT(3,3)
      FST(2,1) = FT(2,1)*FPINVT(1,1) +
     &                FT(2,2)*FPINVT(2,1) +
     &                FT(2,3)*FPINVT(3,1)
      FST(2,2) = FT(2,1)*FPINVT(1,2) +
     &                FT(2,2)*FPINVT(2,2) +
     &                FT(2,3)*FPINVT(3,2)
      FST(2,3) = FT(2,1)*FPINVT(1,3) +
     &                FT(2,2)*FPINVT(2,3) +
     &                FT(2,3)*FPINVT(3,3)
      FST(3,1) = FT(3,1)*FPINVT(1,1) +
     &                FT(3,2)*FPINVT(2,1) +
     &                FT(3,3)*FPINVT(3,1)
      FST(3,2) = FT(3,1)*FPINVT(1,2) +
     &                FT(3,2)*FPINVT(2,2) +
     &                FT(3,3)*FPINVT(3,2)
      FST(3,3) = FT(3,1)*FPINVT(1,3) +
     &                FT(3,2)*FPINVT(2,3) +
     &                FT(3,3)*FPINVT(3,3)
C
       TMP(1,1) = FST(1,1)*FST(1,1) +
     &                FST(2,1)*FST(2,1) +
     &                FST(3,1)*FST(3,1)
      TMP(1,2) = FST(1,1)*FST(1,2) +
     &                FST(2,1)*FST(2,2) +
     &                FST(3,1)*FST(3,2)
      TMP(1,3) = FST(1,1)*FST(1,3) +
     &                FST(2,1)*FST(2,3) +
     &                FST(3,1)*FST(3,3)
      TMP(2,1) = FST(1,2)*FST(1,1) +
     &                FST(2,2)*FST(2,1) +
     &                FST(3,2)*FST(3,1)
      TMP(2,2) = FST(1,2)*FST(1,2) +
     &                FST(2,2)*FST(2,2) +
     &                FST(3,2)*FST(3,2)
      TMP(2,3) = FST(1,2)*FST(1,3) +
     &                FST(2,2)*FST(2,3) +
     &                FST(3,2)*FST(3,3)
      TMP(3,1) = FST(1,3)*FST(1,1) +
     &                FST(2,3)*FST(2,1) +
     &                FST(3,3)*FST(3,1)
      TMP(3,2) = FST(1,3)*FST(1,2) +
     &                FST(2,3)*FST(2,2) +
     &                FST(3,3)*FST(3,2)
      TMP(3,3) = FST(1,3)*FST(1,3) +
     &                FST(2,3)*FST(2,3) +
     &                FST(3,3)*FST(3,3)
C
        DO 10 I=1,3
        DO 10 J=1,3
 10        ES(J,I) = 0.50D0*(TMP(J,I)-ONET(J,I))
C
      ESV(1)=ES(1,1) 
      ESV(2)=ES(2,2) 
      ESV(3)=ES(3,3)
      ESV(4)=ES(1,2) 
      ESV(5)=ES(1,3) 
      ESV(6)=ES(2,3) 

      TBTAUV(1)  =    ELAS(1,1,icrys)*ESV(1) +
     &                ELAS(1,2,icrys)*ESV(2) +
     &                ELAS(1,3,icrys)*ESV(3) +
     &                ELAS(1,4,icrys)*ESV(4) +
     &                ELAS(1,5,icrys)*ESV(5) +
     &                ELAS(1,6,icrys)*ESV(6)
        TBTAUV(2) = ELAS(2,1,icrys)*ESV(1) +
     &                ELAS(2,2,icrys)*ESV(2) +
     &                ELAS(2,3,icrys)*ESV(3) +
     &                ELAS(2,4,icrys)*ESV(4) +
     &                ELAS(2,5,icrys)*ESV(5) +
     &                ELAS(2,6,icrys)*ESV(6)
        TBTAUV(3) = ELAS(3,1,icrys)*ESV(1) +
     &                ELAS(3,2,icrys)*ESV(2) +
     &                ELAS(3,3,icrys)*ESV(3) +
     &                ELAS(3,4,icrys)*ESV(4) +
     &                ELAS(3,5,icrys)*ESV(5) +
     &                ELAS(3,6,icrys)*ESV(6)
        TBTAUV(4) = ELAS(4,1,icrys)*ESV(1) +
     &                ELAS(4,2,icrys)*ESV(2) +
     &                ELAS(4,3,icrys)*ESV(3) +
     &                ELAS(4,4,icrys)*ESV(4) +
     &                ELAS(4,5,icrys)*ESV(5) +
     &                ELAS(4,6,icrys)*ESV(6)
        TBTAUV(5) = ELAS(5,1,icrys)*ESV(1) +
     &                ELAS(5,2,icrys)*ESV(2) +
     &                ELAS(5,3,icrys)*ESV(3) +
     &                ELAS(5,4,icrys)*ESV(4) +
     &                ELAS(5,5,icrys)*ESV(5) +
     &                ELAS(5,6,icrys)*ESV(6)
        TBTAUV(6) = ELAS(6,1,icrys)*ESV(1) +
     &                ELAS(6,2,icrys)*ESV(2) +
     &                ELAS(6,3,icrys)*ESV(3) +
     &                ELAS(6,4,icrys)*ESV(4) +
     &                ELAS(6,5,icrys)*ESV(5) +
     &                ELAS(6,6,icrys)*ESV(6)

	IF (LHAMADTEST ==1) print*,'End of Subrt:GUESSTB'
C
        RETURN
        END
C((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))
      SUBROUTINE INITIAL(C11,C12,C44,NCRYS)
C
      INCLUDE'/nv/hp22/dpatel73/CPFEM/Classical/commonsn.txt'
      DIMENSION AM(48,3),AN(48,3),SLOCAL(3,3,48),
     &Q(3,3),QT(3,3),TMP(3,3),g(3,MAXCRYS)
C
	IF (LHAMADTEST ==1) print*,'Beginning of Subrt: INITIAL'
!	--------------------------------------------------------------
C     Enter the initial texture here (Run the MATLAB code and paste the output here)
C
         g(1:3,1) = [83.2, 125.4, 30.4] 
        !	--------------------------------------------------------------
C       Define Slip System for BCC   (48 slip systems)
C	AM=Slip direction & AN=Slip plane normal							
           AN(1,1:3)=[1,1,0]
           AM(1,1:3)=[-1,1,1]
           AN(2,1:3)=[1,1,0]
           AM(2,1:3)=[1,-1,1]
           AN(3,1:3)=[-1,1,0]
           AM(3,1:3)=[1,1,1]
           AN(4,1:3)=[-1,1,0]
           AM(4,1:3)=[1,1,-1]
           AN(5,1:3)=[1,0,1]
           AM(5,1:3)=[1,-1,-1]
           AN(6,1:3)=[1,0,1]
           AM(6,1:3)=[1,1,-1]
           AN(7,1:3)=[-1,0,1]
           AM(7,1:3)=[1,1,1]
           AN(8,1:3)=[-1,0,1]
           AM(8,1:3)=[-1,1,-1]
           AN(9,1:3)=[0,1,1]
           AM(9,1:3)=[-1,-1,1]
           AN(10,1:3)=[0,1,1]
           AM(10,1:3)=[1,-1,1]
           AN(11,1:3)=[0,-1,1]
           AM(11,1:3)=[1,1,1]
           AN(12,1:3)=[0,-1,1]
           AM(12,1:3)=[-1,1,1]
           AN(13,1:3)=[1,1,2]
           AM(13,1:3)=[-1,-1,1]
           AN(14,1:3)=[1,-1,2]
           AM(14,1:3)=[-1,1,1]
           AN(15,1:3)=[-1,-1,2]
           AM(15,1:3)=[1,1,1]
           AN(16,1:3)=[-1,1,2]
           AM(16,1:3)=[1,-1,1]
           AN(17,1:3)=[-1,2,-1]
           AM(17,1:3)=[1,1,1]
           AN(18,1:3)=[1,2,-1]
           AM(18,1:3)=[-1,1,1]
           AN(19,1:3)=[1,2,1]
           AM(19,1:3)=[-1,1,-1]
           AN(20,1:3)=[-1,2,1]
           AM(20,1:3)=[1,1,-1]
           AN(21,1:3)=[2,1,1]
           AM(21,1:3)=[-1,1,1]
           AN(22,1:3)=[2,1,-1]
           AM(22,1:3)=[1,-1,1]
           AN(23,1:3)=[2,-1,-1]
           AM(23,1:3)=[1,1,1]
           AN(24,1:3)=[2,-1,1]
           AM(24,1:3)=[1,1,-1]
           AN(25,1:3)=[1,2,3]
           AM(25,1:3)=[-1,-1,1]
           AN(26,1:3)=[1,-2,3]
           AM(26,1:3)=[-1,1,1]
           AN(27,1:3)=[-1,-2,3]
           AM(27,1:3)=[1,1,1]
           AN(28,1:3)=[-1,2,3]
           AM(28,1:3)=[1,-1,1]
           AN(29,1:3)=[2,1,3]
           AM(29,1:3)=[-1,-1,1]
           AN(30,1:3)=[2,-1,3]
           AM(30,1:3)=[-1,1,1]
           AN(31,1:3)=[-2,-1,3]
           AM(31,1:3)=[1,1,1]
           AN(32,1:3)=[-2,1,3]
           AM(32,1:3)=[1,-1,1]
           AN(33,1:3)=[2,3,1]
           AM(33,1:3)=[-1,1,-1]
           AN(34,1:3)=[-2,3,1]
           AM(34,1:3)=[1,1,-1]
           AN(35,1:3)=[-2,3,-1]
           AM(35,1:3)=[1,1,1]
           AN(36,1:3)=[2,3,-1]
           AM(36,1:3)=[-1,1,1]
           AN(37,1:3)=[1,3,2]
           AM(37,1:3)=[-1,1,-1]
           AN(38,1:3)=[-1,3,2]
           AM(38,1:3)=[1,1,-1]
           AN(39,1:3)=[-1,3,-2]
           AM(39,1:3)=[1,1,1]
           AN(40,1:3)=[1,3,-2]
           AM(40,1:3)=[-1,1,1]
           AN(41,1:3)=[3,2,1]
           AM(41,1:3)=[1,-1,-1]
           AN(42,1:3)=[3,2,-1]
           AM(42,1:3)=[1,-1,1]
           AN(43,1:3)=[3,-2,-1]
           AM(43,1:3)=[1,1,1]
           AN(44,1:3)=[3,-2,1]
           AM(44,1:3)=[1,1,-1]
           AN(45,1:3)=[3,1,2]
           AM(45,1:3)=[1,-1,-1]
           AN(46,1:3)=[3,1,-2]
           AM(46,1:3)=[1,-1,1]
           AN(47,1:3)=[3,-1,-2]
           AM(47,1:3)=[1,1,1]
           AN(48,1:3)=[3,-1,2]
           AM(48,1:3)=[1,1,-1]
!	--------------------------------------------------------------
	IF (LHAMADTEST ==1) print*,'Location-3 Subrt: INITIAL'

        DO 40 I = 1,48
             AMA = 1.0D0/DSQRT(AM(I,1)**2+AM(I,2)**2+AM(I,3)**2)
             ANA = 1.0D0/DSQRT(AN(I,1)**2+AN(I,2)**2+AN(I,3)**2)
             AM(I,1) = AM(I,1)*AMA
             AN(I,1) = AN(I,1)*ANA
             AM(I,2) = AM(I,2)*AMA
             AN(I,2) = AN(I,2)*ANA
             AM(I,3) = AM(I,3)*AMA
             AN(I,3) = AN(I,3)*ANA
C
C     COMPUTE MATRIX SLOCAL IN LOCAL COORDINATES
C
             SLOCAL(1,1,I) = AM(I,1)*AN(I,1)
             SLOCAL(1,2,I) = AM(I,1)*AN(I,2)
             SLOCAL(1,3,I) = AM(I,1)*AN(I,3)
             SLOCAL(2,1,I) = AM(I,2)*AN(I,1)
             SLOCAL(2,2,I) = AM(I,2)*AN(I,2)
             SLOCAL(2,3,I) = AM(I,2)*AN(I,3)
             SLOCAL(3,1,I) = AM(I,3)*AN(I,1)
             SLOCAL(3,2,I) = AM(I,3)*AN(I,2)
             SLOCAL(3,3,I) = AM(I,3)*AN(I,3)
 40    CONTINUE
C
	IF (LHAMADTEST ==1) print*,'Location-4 Subrt: INITIAL'
C  COMPUTE TRANSFORMATIONS MATRICES FOR EACH CRYSTAL AND Sdelta
C  AND Pdelta (VECTORIZED) IN GLOBAL COORDINATES
C
C
C       OBTAIN CRYSTAL INFORMATION
C
        RADDEG = 4.0D0*DATAN(1.0D0)/180.0D0
C		phib1= 0.0	!in degree
C		phib = 0.0
C		phib2= 0.0
C
        InitialLoop: DO icrys=1,NCRYS
            phib1 = g(1,icrys)
            phib  = g(2,icrys)
            phib2 = g(3,icrys)
C            
            TH = phib*RADDEG
            PHI = (180-phib2)*RADDEG
            OM = (180-phib1)*RADDEG
C
C            OBTAIN TRANSFORMATION MATRICES
             CALL ROTMAT(TH,PHI,OM,Q,QT)
!	--------------------------------------------------------------
C     COMPUTE ELAS MATRICES FOR THE CRYSTAL
C	Added by Hamad F. Al-Harbi: June 19, 2012
!	Below is used instead of subroutine: ELAST
C
        HC44 = 0.50D0*C44
        TC11 = 2.0D0*C11
        TC12 = 2.0D0*C12
C        
      ELAS(1,1,icrys) = C11*( Q(1,1)*Q(1,1)*Q(1,1)*Q(1,1)+
     &         Q(1,2)*Q(1,2)*Q(1,2)*Q(1,2)+
     &         Q(1,3)*Q(1,3)*Q(1,3)*Q(1,3))+
     &  C12*( Q(1,1)*Q(1,1)*(Q(1,2)*Q(1,2)+Q(1,3)*Q(1,3))+
     &         Q(1,2)*Q(1,2)*(Q(1,1)*Q(1,1)+Q(1,3)*Q(1,3))+
     &         Q(1,3)*Q(1,3)*(Q(1,1)*Q(1,1)+Q(1,2)*Q(1,2)))+
     &  HC44*( Q(1,1)*Q(1,2)*(Q(1,1)*Q(1,2)+Q(1,2)*Q(1,1))+
     &         Q(1,1)*Q(1,3)*(Q(1,1)*Q(1,3)+Q(1,3)*Q(1,1))+
     &         Q(1,2)*Q(1,1)*(Q(1,2)*Q(1,1)+Q(1,1)*Q(1,2))+
     &         Q(1,2)*Q(1,3)*(Q(1,2)*Q(1,3)+Q(1,3)*Q(1,2))+
     &         Q(1,3)*Q(1,1)*(Q(1,3)*Q(1,1)+Q(1,1)*Q(1,3))+
     &         Q(1,3)*Q(1,2)*(Q(1,3)*Q(1,2)+Q(1,2)*Q(1,3)))
C
      ELAS(2,2,icrys) = C11*( Q(2,1)*Q(2,1)*Q(2,1)*Q(2,1)+
     &         Q(2,2)*Q(2,2)*Q(2,2)*Q(2,2)+
     &         Q(2,3)*Q(2,3)*Q(2,3)*Q(2,3))+
     &  C12*( Q(2,1)*Q(2,1)*(Q(2,2)*Q(2,2)+Q(2,3)*Q(2,3))+
     &         Q(2,2)*Q(2,2)*(Q(2,1)*Q(2,1)+Q(2,3)*Q(2,3))+
     &         Q(2,3)*Q(2,3)*(Q(2,1)*Q(2,1)+Q(2,2)*Q(2,2)))+
     &  HC44*( Q(2,1)*Q(2,2)*(Q(2,1)*Q(2,2)+Q(2,2)*Q(2,1))+
     &         Q(2,1)*Q(2,3)*(Q(2,1)*Q(2,3)+Q(2,3)*Q(2,1))+
     &         Q(2,2)*Q(2,1)*(Q(2,2)*Q(2,1)+Q(2,1)*Q(2,2))+
     &         Q(2,2)*Q(2,3)*(Q(2,2)*Q(2,3)+Q(2,3)*Q(2,2))+
     &         Q(2,3)*Q(2,1)*(Q(2,3)*Q(2,1)+Q(2,1)*Q(2,3))+
     &         Q(2,3)*Q(2,2)*(Q(2,3)*Q(2,2)+Q(2,2)*Q(2,3)))



            ELAS(3,3,icrys) = C11*( Q(3,1)*Q(3,1)*Q(3,1)*Q(3,1)+
     &         Q(3,2)*Q(3,2)*Q(3,2)*Q(3,2)+
     &         Q(3,3)*Q(3,3)*Q(3,3)*Q(3,3))+
     &  C12*( Q(3,1)*Q(3,1)*(Q(3,2)*Q(3,2)+Q(3,3)*Q(3,3))+
     &         Q(3,2)*Q(3,2)*(Q(3,1)*Q(3,1)+Q(3,3)*Q(3,3))+
     &         Q(3,3)*Q(3,3)*(Q(3,1)*Q(3,1)+Q(3,2)*Q(3,2)))+
     &  HC44*( Q(3,1)*Q(3,2)*(Q(3,1)*Q(3,2)+Q(3,2)*Q(3,1))+
     &         Q(3,1)*Q(3,3)*(Q(3,1)*Q(3,3)+Q(3,3)*Q(3,1))+
     &         Q(3,2)*Q(3,1)*(Q(3,2)*Q(3,1)+Q(3,1)*Q(3,2))+
     &         Q(3,2)*Q(3,3)*(Q(3,2)*Q(3,3)+Q(3,3)*Q(3,2))+
     &         Q(3,3)*Q(3,1)*(Q(3,3)*Q(3,1)+Q(3,1)*Q(3,3))+
     &         Q(3,3)*Q(3,2)*(Q(3,3)*Q(3,2)+Q(3,2)*Q(3,3)))



            ELAS(1,2,icrys) = C11*( Q(1,1)*Q(1,1)*Q(2,1)*Q(2,1)+
     &         Q(1,2)*Q(1,2)*Q(2,2)*Q(2,2)+       
     &		 Q(1,3)*Q(1,3)*Q(2,3)*Q(2,3))+
     &  C12*( Q(1,1)*Q(1,1)*(Q(2,2)*Q(2,2)+Q(2,3)*Q(2,3))+
     &         Q(1,2)*Q(1,2)*(Q(2,1)*Q(2,1)+Q(2,3)*Q(2,3))+
     &	     Q(1,3)*Q(1,3)*(Q(2,1)*Q(2,1)+Q(2,2)*Q(2,2)))+
     &  HC44*( Q(1,1)*Q(1,2)*(Q(2,1)*Q(2,2)+Q(2,2)*Q(2,1))+
     &         Q(1,1)*Q(1,3)*(Q(2,1)*Q(2,3)+Q(2,3)*Q(2,1))+
     &         Q(1,2)*Q(1,1)*(Q(2,2)*Q(2,1)+Q(2,1)*Q(2,2))+
     &         Q(1,2)*Q(1,3)*(Q(2,2)*Q(2,3)+Q(2,3)*Q(2,2))+
     &         Q(1,3)*Q(1,1)*(Q(2,3)*Q(2,1)+Q(2,1)*Q(2,3))+
     &         Q(1,3)*Q(1,2)*(Q(2,3)*Q(2,2)+Q(2,2)*Q(2,3)))



            ELAS(1,3,icrys) = C11*( Q(1,1)*Q(1,1)*Q(3,1)*Q(3,1)+
     &         Q(1,2)*Q(1,2)*Q(3,2)*Q(3,2)+
     &         Q(1,3)*Q(1,3)*Q(3,3)*Q(3,3))+
     &  C12*( Q(1,1)*Q(1,1)*(Q(3,2)*Q(3,2)+Q(3,3)*Q(3,3))+
     &         Q(1,2)*Q(1,2)*(Q(3,1)*Q(3,1)+Q(3,3)*Q(3,3))+
     &         Q(1,3)*Q(1,3)*(Q(3,1)*Q(3,1)+Q(3,2)*Q(3,2)))+
     &  HC44*( Q(1,1)*Q(1,2)*(Q(3,1)*Q(3,2)+Q(3,2)*Q(3,1))+
     &         Q(1,1)*Q(1,3)*(Q(3,1)*Q(3,3)+Q(3,3)*Q(3,1))+
     &         Q(1,2)*Q(1,1)*(Q(3,2)*Q(3,1)+Q(3,1)*Q(3,2))+
     &         Q(1,2)*Q(1,3)*(Q(3,2)*Q(3,3)+Q(3,3)*Q(3,2))+
     &         Q(1,3)*Q(1,1)*(Q(3,3)*Q(3,1)+Q(3,1)*Q(3,3))+
     &         Q(1,3)*Q(1,2)*(Q(3,3)*Q(3,2)+Q(3,2)*Q(3,3)))



            ELAS(2,3,icrys) = C11*( Q(2,1)*Q(2,1)*Q(3,1)*Q(3,1)+
     &         Q(2,2)*Q(2,2)*Q(3,2)*Q(3,2)+
     &         Q(2,3)*Q(2,3)*Q(3,3)*Q(3,3))+
     &  C12*( Q(2,1)*Q(2,1)*(Q(3,2)*Q(3,2)+Q(3,3)*Q(3,3))+
     &         Q(2,2)*Q(2,2)*(Q(3,1)*Q(3,1)+Q(3,3)*Q(3,3))+
     &         Q(2,3)*Q(2,3)*(Q(3,1)*Q(3,1)+Q(3,2)*Q(3,2)))+
     &  HC44*( Q(2,1)*Q(2,2)*(Q(3,1)*Q(3,2)+Q(3,2)*Q(3,1))+
     &         Q(2,1)*Q(2,3)*(Q(3,1)*Q(3,3)+Q(3,3)*Q(3,1))+
     &         Q(2,2)*Q(2,1)*(Q(3,2)*Q(3,1)+Q(3,1)*Q(3,2))+
     &         Q(2,2)*Q(2,3)*(Q(3,2)*Q(3,3)+Q(3,3)*Q(3,2))+
     &         Q(2,3)*Q(2,1)*(Q(3,3)*Q(3,1)+Q(3,1)*Q(3,3))+
     &         Q(2,3)*Q(2,2)*(Q(3,3)*Q(3,2)+Q(3,2)*Q(3,3)))



        ELAS(2,1,icrys)=ELAS(1,2,icrys)
        ELAS(3,1,icrys)=ELAS(1,3,icrys)
        ELAS(3,2,icrys)=ELAS(2,3,icrys)
            ELAS(4,4,icrys) = TC11*( Q(1,1)*Q(2,1)*Q(1,1)*Q(2,1)+
     &         Q(1,2)*Q(2,2)*Q(1,2)*Q(2,2)+
     &         Q(1,3)*Q(2,3)*Q(1,3)*Q(2,3))+
     &  TC12*( Q(1,1)*Q(2,1)*(Q(1,2)*Q(2,2)+Q(1,3)*Q(2,3))+
     &         Q(1,2)*Q(2,2)*(Q(1,1)*Q(2,1)+Q(1,3)*Q(2,3))+
     &         Q(1,3)*Q(2,3)*(Q(1,1)*Q(2,1)+Q(1,2)*Q(2,2)))+
     &  C44*( Q(1,1)*Q(2,2)*(Q(1,1)*Q(2,2)+Q(1,2)*Q(2,1))+
     &         Q(1,1)*Q(2,3)*(Q(1,1)*Q(2,3)+Q(1,3)*Q(2,1))+
     &         Q(1,2)*Q(2,1)*(Q(1,2)*Q(2,1)+Q(1,1)*Q(2,2))+
     &         Q(1,2)*Q(2,3)*(Q(1,2)*Q(2,3)+Q(1,3)*Q(2,2))+
     &         Q(1,3)*Q(2,1)*(Q(1,3)*Q(2,1)+Q(1,1)*Q(2,3))+
     &         Q(1,3)*Q(2,2)*(Q(1,3)*Q(2,2)+Q(1,2)*Q(2,3)))



            ELAS(5,5,icrys) = TC11*( Q(1,1)*Q(3,1)*Q(1,1)*Q(3,1)+
     &         Q(1,2)*Q(3,2)*Q(1,2)*Q(3,2)+
     &         Q(1,3)*Q(3,3)*Q(1,3)*Q(3,3))+
     &  TC12*( Q(1,1)*Q(3,1)*(Q(1,2)*Q(3,2)+Q(1,3)*Q(3,3))+
     &         Q(1,2)*Q(3,2)*(Q(1,1)*Q(3,1)+Q(1,3)*Q(3,3))+
     &         Q(1,3)*Q(3,3)*(Q(1,1)*Q(3,1)+Q(1,2)*Q(3,2)))+
     &  C44*( Q(1,1)*Q(3,2)*(Q(1,1)*Q(3,2)+Q(1,2)*Q(3,1))+
     &         Q(1,1)*Q(3,3)*(Q(1,1)*Q(3,3)+Q(1,3)*Q(3,1))+
     &         Q(1,2)*Q(3,1)*(Q(1,2)*Q(3,1)+Q(1,1)*Q(3,2))+
     &         Q(1,2)*Q(3,3)*(Q(1,2)*Q(3,3)+Q(1,3)*Q(3,2))+
     &         Q(1,3)*Q(3,1)*(Q(1,3)*Q(3,1)+Q(1,1)*Q(3,3))+
     &         Q(1,3)*Q(3,2)*(Q(1,3)*Q(3,2)+Q(1,2)*Q(3,3)))



            ELAS(6,6,icrys) = TC11*( Q(2,1)*Q(3,1)*Q(2,1)*Q(3,1)+
     &         Q(2,2)*Q(3,2)*Q(2,2)*Q(3,2)+
     &         Q(2,3)*Q(3,3)*Q(2,3)*Q(3,3))+
     &  TC12*( Q(2,1)*Q(3,1)*(Q(2,2)*Q(3,2)+Q(2,3)*Q(3,3))+
     &         Q(2,2)*Q(3,2)*(Q(2,1)*Q(3,1)+Q(2,3)*Q(3,3))+
     &         Q(2,3)*Q(3,3)*(Q(2,1)*Q(3,1)+Q(2,2)*Q(3,2)))+
     &  C44*( Q(2,1)*Q(3,2)*(Q(2,1)*Q(3,2)+Q(2,2)*Q(3,1))+
     &         Q(2,1)*Q(3,3)*(Q(2,1)*Q(3,3)+Q(2,3)*Q(3,1))+
     &         Q(2,2)*Q(3,1)*(Q(2,2)*Q(3,1)+Q(2,1)*Q(3,2))+
     &         Q(2,2)*Q(3,3)*(Q(2,2)*Q(3,3)+Q(2,3)*Q(3,2))+
     &         Q(2,3)*Q(3,1)*(Q(2,3)*Q(3,1)+Q(2,1)*Q(3,3))+
     &         Q(2,3)*Q(3,2)*(Q(2,3)*Q(3,2)+Q(2,2)*Q(3,3)))



            ELAS(4,5,icrys) = TC11*( Q(1,1)*Q(2,1)*Q(1,1)*Q(3,1)+
     &         Q(1,2)*Q(2,2)*Q(1,2)*Q(3,2)+
     &         Q(1,3)*Q(2,3)*Q(1,3)*Q(3,3))+
     &  TC12*( Q(1,1)*Q(2,1)*(Q(1,2)*Q(3,2)+Q(1,3)*Q(3,3))+
     &         Q(1,2)*Q(2,2)*(Q(1,1)*Q(3,1)+Q(1,3)*Q(3,3))+
     &         Q(1,3)*Q(2,3)*(Q(1,1)*Q(3,1)+Q(1,2)*Q(3,2)))+
     &  C44*( Q(1,1)*Q(2,2)*(Q(1,1)*Q(3,2)+Q(1,2)*Q(3,1))+
     &         Q(1,1)*Q(2,3)*(Q(1,1)*Q(3,3)+Q(1,3)*Q(3,1))+
     &         Q(1,2)*Q(2,1)*(Q(1,2)*Q(3,1)+Q(1,1)*Q(3,2))+
     &         Q(1,2)*Q(2,3)*(Q(1,2)*Q(3,3)+Q(1,3)*Q(3,2))+
     &         Q(1,3)*Q(2,1)*(Q(1,3)*Q(3,1)+Q(1,1)*Q(3,3))+
     &         Q(1,3)*Q(2,2)*(Q(1,3)*Q(3,2)+Q(1,2)*Q(3,3)))



            ELAS(4,6,icrys) = TC11*( Q(1,1)*Q(2,1)*Q(2,1)*Q(3,1)+
     &         Q(1,2)*Q(2,2)*Q(2,2)*Q(3,2)+
     &         Q(1,3)*Q(2,3)*Q(2,3)*Q(3,3))+
     &  TC12*( Q(1,1)*Q(2,1)*(Q(2,2)*Q(3,2)+Q(2,3)*Q(3,3))+
     &         Q(1,2)*Q(2,2)*(Q(2,1)*Q(3,1)+Q(2,3)*Q(3,3))+
     &         Q(1,3)*Q(2,3)*(Q(2,1)*Q(3,1)+Q(2,2)*Q(3,2)))+
     &  C44*( Q(1,1)*Q(2,2)*(Q(2,1)*Q(3,2)+Q(2,2)*Q(3,1))+
     &         Q(1,1)*Q(2,3)*(Q(2,1)*Q(3,3)+Q(2,3)*Q(3,1))+
     &         Q(1,2)*Q(2,1)*(Q(2,2)*Q(3,1)+Q(2,1)*Q(3,2))+
     &         Q(1,2)*Q(2,3)*(Q(2,2)*Q(3,3)+Q(2,3)*Q(3,2))+
     &         Q(1,3)*Q(2,1)*(Q(2,3)*Q(3,1)+Q(2,1)*Q(3,3))+
     &         Q(1,3)*Q(2,2)*(Q(2,3)*Q(3,2)+Q(2,2)*Q(3,3)))



            ELAS(5,6,icrys) = TC11*( Q(1,1)*Q(3,1)*Q(2,1)*Q(3,1)+
     &         Q(1,2)*Q(3,2)*Q(2,2)*Q(3,2)+
     &         Q(1,3)*Q(3,3)*Q(2,3)*Q(3,3))+
     &  TC12*( Q(1,1)*Q(3,1)*(Q(2,2)*Q(3,2)+Q(2,3)*Q(3,3))+
     &         Q(1,2)*Q(3,2)*(Q(2,1)*Q(3,1)+Q(2,3)*Q(3,3))+
     &         Q(1,3)*Q(3,3)*(Q(2,1)*Q(3,1)+Q(2,2)*Q(3,2)))+
     &  C44*( Q(1,1)*Q(3,2)*(Q(2,1)*Q(3,2)+Q(2,2)*Q(3,1))+
     &         Q(1,1)*Q(3,3)*(Q(2,1)*Q(3,3)+Q(2,3)*Q(3,1))+
     &         Q(1,2)*Q(3,1)*(Q(2,2)*Q(3,1)+Q(2,1)*Q(3,2))+
     &         Q(1,2)*Q(3,3)*(Q(2,2)*Q(3,3)+Q(2,3)*Q(3,2))+
     &         Q(1,3)*Q(3,1)*(Q(2,3)*Q(3,1)+Q(2,1)*Q(3,3))+
     &         Q(1,3)*Q(3,2)*(Q(2,3)*Q(3,2)+Q(2,2)*Q(3,3)))



        ELAS(5,4,icrys)=ELAS(4,5,icrys)
        ELAS(6,4,icrys)=ELAS(4,6,icrys)
        ELAS(6,5,icrys)=ELAS(5,6,icrys)
            ELAS(1,4,icrys) = TC11*( Q(1,1)*Q(1,1)*Q(1,1)*Q(2,1)+
     &         Q(1,2)*Q(1,2)*Q(1,2)*Q(2,2)+
     &         Q(1,3)*Q(1,3)*Q(1,3)*Q(2,3))+
     &  TC12*( Q(1,1)*Q(1,1)*(Q(1,2)*Q(2,2)+Q(1,3)*Q(2,3))+
     &         Q(1,2)*Q(1,2)*(Q(1,1)*Q(2,1)+Q(1,3)*Q(2,3))+
     &         Q(1,3)*Q(1,3)*(Q(1,1)*Q(2,1)+Q(1,2)*Q(2,2)))+
     &  C44*( Q(1,1)*Q(1,2)*(Q(1,1)*Q(2,2)+Q(1,2)*Q(2,1))+
     &         Q(1,1)*Q(1,3)*(Q(1,1)*Q(2,3)+Q(1,3)*Q(2,1))+
     &         Q(1,2)*Q(1,1)*(Q(1,2)*Q(2,1)+Q(1,1)*Q(2,2))+
     &         Q(1,2)*Q(1,3)*(Q(1,2)*Q(2,3)+Q(1,3)*Q(2,2))+
     &         Q(1,3)*Q(1,1)*(Q(1,3)*Q(2,1)+Q(1,1)*Q(2,3))+
     &         Q(1,3)*Q(1,2)*(Q(1,3)*Q(2,2)+Q(1,2)*Q(2,3)))



            ELAS(1,5,icrys) = TC11*( Q(1,1)*Q(1,1)*Q(1,1)*Q(3,1)+
     &         Q(1,2)*Q(1,2)*Q(1,2)*Q(3,2)+
     &         Q(1,3)*Q(1,3)*Q(1,3)*Q(3,3))+
     &  TC12*( Q(1,1)*Q(1,1)*(Q(1,2)*Q(3,2)+Q(1,3)*Q(3,3))+
     &         Q(1,2)*Q(1,2)*(Q(1,1)*Q(3,1)+Q(1,3)*Q(3,3))+
     &         Q(1,3)*Q(1,3)*(Q(1,1)*Q(3,1)+Q(1,2)*Q(3,2)))+
     &  C44*( Q(1,1)*Q(1,2)*(Q(1,1)*Q(3,2)+Q(1,2)*Q(3,1))+
     &         Q(1,1)*Q(1,3)*(Q(1,1)*Q(3,3)+Q(1,3)*Q(3,1))+
     &         Q(1,2)*Q(1,1)*(Q(1,2)*Q(3,1)+Q(1,1)*Q(3,2))+
     &         Q(1,2)*Q(1,3)*(Q(1,2)*Q(3,3)+Q(1,3)*Q(3,2))+
     &         Q(1,3)*Q(1,1)*(Q(1,3)*Q(3,1)+Q(1,1)*Q(3,3))+
     &         Q(1,3)*Q(1,2)*(Q(1,3)*Q(3,2)+Q(1,2)*Q(3,3)))



            ELAS(1,6,icrys) = TC11*( Q(1,1)*Q(1,1)*Q(2,1)*Q(3,1)+
     &         Q(1,2)*Q(1,2)*Q(2,2)*Q(3,2)+
     &         Q(1,3)*Q(1,3)*Q(2,3)*Q(3,3))+
     &  TC12*( Q(1,1)*Q(1,1)*(Q(2,2)*Q(3,2)+Q(2,3)*Q(3,3))+
     &         Q(1,2)*Q(1,2)*(Q(2,1)*Q(3,1)+Q(2,3)*Q(3,3))+
     &         Q(1,3)*Q(1,3)*(Q(2,1)*Q(3,1)+Q(2,2)*Q(3,2)))+
     &  C44*( Q(1,1)*Q(1,2)*(Q(2,1)*Q(3,2)+Q(2,2)*Q(3,1))+
     &         Q(1,1)*Q(1,3)*(Q(2,1)*Q(3,3)+Q(2,3)*Q(3,1))+
     &         Q(1,2)*Q(1,1)*(Q(2,2)*Q(3,1)+Q(2,1)*Q(3,2))+
     &         Q(1,2)*Q(1,3)*(Q(2,2)*Q(3,3)+Q(2,3)*Q(3,2))+
     &         Q(1,3)*Q(1,1)*(Q(2,3)*Q(3,1)+Q(2,1)*Q(3,3))+
     &         Q(1,3)*Q(1,2)*(Q(2,3)*Q(3,2)+Q(2,2)*Q(3,3)))



            ELAS(2,4,icrys) = TC11*( Q(2,1)*Q(2,1)*Q(1,1)*Q(2,1)+
     &         Q(2,2)*Q(2,2)*Q(1,2)*Q(2,2)+
     &         Q(2,3)*Q(2,3)*Q(1,3)*Q(2,3))+
     &  TC12*( Q(2,1)*Q(2,1)*(Q(1,2)*Q(2,2)+Q(1,3)*Q(2,3))+
     &         Q(2,2)*Q(2,2)*(Q(1,1)*Q(2,1)+Q(1,3)*Q(2,3))+
     &         Q(2,3)*Q(2,3)*(Q(1,1)*Q(2,1)+Q(1,2)*Q(2,2)))+
     &  C44*( Q(2,1)*Q(2,2)*(Q(1,1)*Q(2,2)+Q(1,2)*Q(2,1))+
     &         Q(2,1)*Q(2,3)*(Q(1,1)*Q(2,3)+Q(1,3)*Q(2,1))+
     &         Q(2,2)*Q(2,1)*(Q(1,2)*Q(2,1)+Q(1,1)*Q(2,2))+
     &         Q(2,2)*Q(2,3)*(Q(1,2)*Q(2,3)+Q(1,3)*Q(2,2))+
     &         Q(2,3)*Q(2,1)*(Q(1,3)*Q(2,1)+Q(1,1)*Q(2,3))+
     &         Q(2,3)*Q(2,2)*(Q(1,3)*Q(2,2)+Q(1,2)*Q(2,3)))



            ELAS(2,5,icrys) = TC11*( Q(2,1)*Q(2,1)*Q(1,1)*Q(3,1)+
     &         Q(2,2)*Q(2,2)*Q(1,2)*Q(3,2)+
     &         Q(2,3)*Q(2,3)*Q(1,3)*Q(3,3))+
     &  TC12*( Q(2,1)*Q(2,1)*(Q(1,2)*Q(3,2)+Q(1,3)*Q(3,3))+
     &         Q(2,2)*Q(2,2)*(Q(1,1)*Q(3,1)+Q(1,3)*Q(3,3))+
     &         Q(2,3)*Q(2,3)*(Q(1,1)*Q(3,1)+Q(1,2)*Q(3,2)))+
     &  C44*( Q(2,1)*Q(2,2)*(Q(1,1)*Q(3,2)+Q(1,2)*Q(3,1))+
     &         Q(2,1)*Q(2,3)*(Q(1,1)*Q(3,3)+Q(1,3)*Q(3,1))+
     &         Q(2,2)*Q(2,1)*(Q(1,2)*Q(3,1)+Q(1,1)*Q(3,2))+
     &         Q(2,2)*Q(2,3)*(Q(1,2)*Q(3,3)+Q(1,3)*Q(3,2))+
     &         Q(2,3)*Q(2,1)*(Q(1,3)*Q(3,1)+Q(1,1)*Q(3,3))+
     &         Q(2,3)*Q(2,2)*(Q(1,3)*Q(3,2)+Q(1,2)*Q(3,3)))



            ELAS(2,6,icrys) = TC11*( Q(2,1)*Q(2,1)*Q(2,1)*Q(3,1)+
     &         Q(2,2)*Q(2,2)*Q(2,2)*Q(3,2)+
     &         Q(2,3)*Q(2,3)*Q(2,3)*Q(3,3))+
     &  TC12*( Q(2,1)*Q(2,1)*(Q(2,2)*Q(3,2)+Q(2,3)*Q(3,3))+
     &         Q(2,2)*Q(2,2)*(Q(2,1)*Q(3,1)+Q(2,3)*Q(3,3))+
     &         Q(2,3)*Q(2,3)*(Q(2,1)*Q(3,1)+Q(2,2)*Q(3,2)))+
     &  C44*( Q(2,1)*Q(2,2)*(Q(2,1)*Q(3,2)+Q(2,2)*Q(3,1))+
     &         Q(2,1)*Q(2,3)*(Q(2,1)*Q(3,3)+Q(2,3)*Q(3,1))+
     &         Q(2,2)*Q(2,1)*(Q(2,2)*Q(3,1)+Q(2,1)*Q(3,2))+
     &         Q(2,2)*Q(2,3)*(Q(2,2)*Q(3,3)+Q(2,3)*Q(3,2))+
     &         Q(2,3)*Q(2,1)*(Q(2,3)*Q(3,1)+Q(2,1)*Q(3,3))+
     &         Q(2,3)*Q(2,2)*(Q(2,3)*Q(3,2)+Q(2,2)*Q(3,3)))



            ELAS(3,4,icrys) = TC11*( Q(3,1)*Q(3,1)*Q(1,1)*Q(2,1)+
     &         Q(3,2)*Q(3,2)*Q(1,2)*Q(2,2)+
     &         Q(3,3)*Q(3,3)*Q(1,3)*Q(2,3))+
     &  TC12*( Q(3,1)*Q(3,1)*(Q(1,2)*Q(2,2)+Q(1,3)*Q(2,3))+
     &         Q(3,2)*Q(3,2)*(Q(1,1)*Q(2,1)+Q(1,3)*Q(2,3))+
     &         Q(3,3)*Q(3,3)*(Q(1,1)*Q(2,1)+Q(1,2)*Q(2,2)))+
     &  C44*( Q(3,1)*Q(3,2)*(Q(1,1)*Q(2,2)+Q(1,2)*Q(2,1))+
     &         Q(3,1)*Q(3,3)*(Q(1,1)*Q(2,3)+Q(1,3)*Q(2,1))+
     &         Q(3,2)*Q(3,1)*(Q(1,2)*Q(2,1)+Q(1,1)*Q(2,2))+
     &         Q(3,2)*Q(3,3)*(Q(1,2)*Q(2,3)+Q(1,3)*Q(2,2))+
     &         Q(3,3)*Q(3,1)*(Q(1,3)*Q(2,1)+Q(1,1)*Q(2,3))+
     &         Q(3,3)*Q(3,2)*(Q(1,3)*Q(2,2)+Q(1,2)*Q(2,3)))



            ELAS(3,5,icrys) = TC11*( Q(3,1)*Q(3,1)*Q(1,1)*Q(3,1)+
     &         Q(3,2)*Q(3,2)*Q(1,2)*Q(3,2)+
     &         Q(3,3)*Q(3,3)*Q(1,3)*Q(3,3))+
     &  TC12*( Q(3,1)*Q(3,1)*(Q(1,2)*Q(3,2)+Q(1,3)*Q(3,3))+
     &         Q(3,2)*Q(3,2)*(Q(1,1)*Q(3,1)+Q(1,3)*Q(3,3))+
     &         Q(3,3)*Q(3,3)*(Q(1,1)*Q(3,1)+Q(1,2)*Q(3,2)))+
     &  C44*( Q(3,1)*Q(3,2)*(Q(1,1)*Q(3,2)+Q(1,2)*Q(3,1))+
     &         Q(3,1)*Q(3,3)*(Q(1,1)*Q(3,3)+Q(1,3)*Q(3,1))+
     &         Q(3,2)*Q(3,1)*(Q(1,2)*Q(3,1)+Q(1,1)*Q(3,2))+
     &         Q(3,2)*Q(3,3)*(Q(1,2)*Q(3,3)+Q(1,3)*Q(3,2))+
     &         Q(3,3)*Q(3,1)*(Q(1,3)*Q(3,1)+Q(1,1)*Q(3,3))+
     &         Q(3,3)*Q(3,2)*(Q(1,3)*Q(3,2)+Q(1,2)*Q(3,3)))



            ELAS(3,6,icrys) = TC11*( Q(3,1)*Q(3,1)*Q(2,1)*Q(3,1)+
     &         Q(3,2)*Q(3,2)*Q(2,2)*Q(3,2)+
     &         Q(3,3)*Q(3,3)*Q(2,3)*Q(3,3))+
     &  TC12*( Q(3,1)*Q(3,1)*(Q(2,2)*Q(3,2)+Q(2,3)*Q(3,3))+
     &         Q(3,2)*Q(3,2)*(Q(2,1)*Q(3,1)+Q(2,3)*Q(3,3))+
     &         Q(3,3)*Q(3,3)*(Q(2,1)*Q(3,1)+Q(2,2)*Q(3,2)))+
     &  C44*( Q(3,1)*Q(3,2)*(Q(2,1)*Q(3,2)+Q(2,2)*Q(3,1))+
     &         Q(3,1)*Q(3,3)*(Q(2,1)*Q(3,3)+Q(2,3)*Q(3,1))+
     &         Q(3,2)*Q(3,1)*(Q(2,2)*Q(3,1)+Q(2,1)*Q(3,2))+
     &         Q(3,2)*Q(3,3)*(Q(2,2)*Q(3,3)+Q(2,3)*Q(3,2))+
     &         Q(3,3)*Q(3,1)*(Q(2,3)*Q(3,1)+Q(2,1)*Q(3,3))+
     &         Q(3,3)*Q(3,2)*(Q(2,3)*Q(3,2)+Q(2,2)*Q(3,3)))



        ELAS(4,1,icrys)=0.50D0*ELAS(1,4,icrys)
        ELAS(4,2,icrys)=0.50D0*ELAS(2,4,icrys)
        ELAS(4,3,icrys)=0.50D0*ELAS(3,4,icrys)
        ELAS(5,1,icrys)=0.50D0*ELAS(1,5,icrys)
        ELAS(5,2,icrys)=0.50D0*ELAS(2,5,icrys)
        ELAS(5,3,icrys)=0.50D0*ELAS(3,5,icrys)
        ELAS(6,1,icrys)=0.50D0*ELAS(1,6,icrys)
        ELAS(6,2,icrys)=0.50D0*ELAS(2,6,icrys)
        ELAS(6,3,icrys)=0.50D0*ELAS(3,6,icrys)
!	--------------------------------------------------------------
	IF (LHAMADTEST ==1) print*,'Location-5 Subrt: INITIAL'
C
C     COMPUTE Sdelta AND Pdelta MATRICES FOR THE CRYSTAL IN GLOBAL
C     COORDINATES. Pdelta IS THE SYMMETRIC COMPONENT OF Sdelta.
C
C	Added by Hamad F. Al-Harbi: June 19, 2012
!       Below is instead of Subroutine FORMSP(SLOCAL,Q,QT)
	
	DO 10 M = 1,48
!		COMPUTE [TMP]=[SLOCAL] X [QT]
	 	DO 110 I=1,3
		DO 110 J=1,3
		TMP(I,J) = 0.0
		DO 110 K=1,3
110		TMP(I,J) = TMP(I,J)+SLOCAL(I,K,M)*QT(K,J)
!
!		COMPUTE [SMATG]=[Q] X [TMP]
	 	DO 120 I=1,3
		DO 120 J=1,3
		SMATG(I,J,M,icrys) = 0.0
		DO 120 K=1,3
120		SMATG(I,J,M,icrys) = SMATG(I,J,M,icrys)+Q(I,K)*TMP(K,J)
!
!	   COMPUTE [PMAT]=Symmetric part of[SMATG]
 	   PMAT(1,M,icrys) = SMATG (1,1,M,icrys) 
	   PMAT(2,M,icrys) = SMATG (2,2,M,icrys)
	   PMAT(3,M,icrys) = SMATG (3,3,M,icrys)
	   PMAT(4,M,icrys) = SMATG (1,2,M,icrys) + SMATG (2,1,M,icrys)
	   PMAT(5,M,icrys) = SMATG (1,3,M,icrys) + SMATG (3,1,M,icrys)
	   PMAT(6,M,icrys) = SMATG (3,2,M,icrys) + SMATG (2,3,M,icrys)
10	CONTINUE
C
      END DO InitialLoop
!	--------------------------------------------------------------
	IF (LHAMADTEST ==1) print*,'End of Subrt: INITIAL'
C
        RETURN
        END
C*********************************************************************
C    THIS SUBROUTINE DOES THE POLAR DECOMPOSITION F=[R][U]=[V][R] 
C*********************************************************************
 	SUBROUTINE DECOMP(F,R,U)
      INCLUDE'/nv/hp22/dpatel73/CPFEM/Classical/commonsn.txt'
	REAL*8 IC,IIC,IIIC,IU,IIU,IIIU
	DIMENSION F(3,3),R(3,3),U(3,3),C(3,3),CC(3,3),UINV(3,3)
C	Added by Hamad F. Al-Harbi: June 19, 2012
	DIMENSION ONET(3,3)
	DATA ONET(1,1),ONET(1,2),ONET(1,3),
     &	 ONET(2,1),ONET(2,2),ONET(2,3),
     &     ONET(3,1),ONET(3,2),ONET(3,3)
     & /1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0/

	IF (LHAMADTEST ==1) print*,'Beginning of Subrt: DECOMP'
C    TRANSPOSE F MATRIX->FT, OBTAIN [C] = [FT] [F], [CC]= [C][C], FIND 
C    PRINCIPAL INVARIANTS OF MATRIX [C].
C
	      C(1,1) = F(1,1)*F(1,1) +
     &                F(2,1)*F(2,1) +
     &                F(3,1)*F(3,1)
      C(1,2) = F(1,1)*F(1,2) +
     &                F(2,1)*F(2,2) +
     &                F(3,1)*F(3,2)
      C(1,3) = F(1,1)*F(1,3) +
     &                F(2,1)*F(2,3) +
     &                F(3,1)*F(3,3)
      C(2,1) = F(1,2)*F(1,1) +
     &                F(2,2)*F(2,1) +
     &                F(3,2)*F(3,1)
      C(2,2) = F(1,2)*F(1,2) +
     &                F(2,2)*F(2,2) +
     &                F(3,2)*F(3,2)
      C(2,3) = F(1,2)*F(1,3) +
     &                F(2,2)*F(2,3) +
     &                F(3,2)*F(3,3)
      C(3,1) = F(1,3)*F(1,1) +
     &                F(2,3)*F(2,1) +
     &                F(3,3)*F(3,1)
      C(3,2) = F(1,3)*F(1,2) +
     &                F(2,3)*F(2,2) +
     &                F(3,3)*F(3,2)
      C(3,3) = F(1,3)*F(1,3) +
     &                F(2,3)*F(2,3) +
     &                F(3,3)*F(3,3)

	IF (LHAMADTEST ==1) print*,'Location-1 of Subrt: DECOMP'

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

	IF (LHAMADTEST ==1) print*,'Location-2 of Subrt: DECOMP'
C
	CALL INVARIANTS(C,IC,IIC,IIIC)
        IF (LHAMADTEST ==1) print*,'Location-2a of Subrt: DECOMP'

	CALL INVEIGEN(IC,IIC,IIIC,E1,E2,E3)

        IF (LHAMADTEST ==1) print*,'Location-2b of Subrt: DECOMP'

C    
C	EIGEN VALUES AND INVARIANTS OF U
	UE1=DSQRT(E1)
	UE2=DSQRT(E2)
	UE3=DSQRT(E3)
	CALL EIGENINV(UE1,UE2,UE3,IU,IIU,IIIU)
C
        IF (LHAMADTEST ==1) print*,'Location-2c of Subrt: DECOMP'

	IF (LHAMADTEST ==1) print*,'Location-3 of Subrt: DECOMP'
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
	IF (LHAMADTEST ==1) print*,'Location-4 of Subrt: DECOMP'
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
C    EVALUATE [R]=[F][UINV]
C
	IF (LHAMADTEST ==1) print*,'Location-5 of Subrt: DECOMP'
C
              R(1,1) = F(1,1)*UINV(1,1) +
     &                F(1,2)*UINV(2,1) +
     &                F(1,3)*UINV(3,1)
      R(1,2) = F(1,1)*UINV(1,2) +
     &                F(1,2)*UINV(2,2) +
     &                F(1,3)*UINV(3,2)
      R(1,3) = F(1,1)*UINV(1,3) +
     &                F(1,2)*UINV(2,3) +
     &                F(1,3)*UINV(3,3)
      R(2,1) = F(2,1)*UINV(1,1) +
     &                F(2,2)*UINV(2,1) +
     &                F(2,3)*UINV(3,1)
      R(2,2) = F(2,1)*UINV(1,2) +
     &                F(2,2)*UINV(2,2) +
     &                F(2,3)*UINV(3,2)
      R(2,3) = F(2,1)*UINV(1,3) +
     &                F(2,2)*UINV(2,3) +
     &                F(2,3)*UINV(3,3)
      R(3,1) = F(3,1)*UINV(1,1) +
     &                F(3,2)*UINV(2,1) +
     &                F(3,3)*UINV(3,1)
      R(3,2) = F(3,1)*UINV(1,2) +
     &                F(3,2)*UINV(2,2) +
     &                F(3,3)*UINV(3,2)
      R(3,3) = F(3,1)*UINV(1,3) +
     &                F(3,2)*UINV(2,3) +
     &                F(3,3)*UINV(3,3)


	IF (LHAMADTEST ==1) print*,'End of Subrt: DECOMP'
	RETURN
	END
C**************************************************************
C  THIS SUBROUTINE CALCULATES THE INVARIANTS OF A 3X3 MATRIX
C**************************************************************
	SUBROUTINE INVARIANTS(C,IC,IIC,IIIC)
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
C
c        print*,'Location-1 of Subrt: INVEIGEN',IC,IIC, IIIC

C	Added by Hamad F. Al-Harbi: June 19, 2012
C	If C is an identity matrix:
	IF( DABS(IC-3.0D0)   .LT. 1.0D-6  .AND.
     &	DABS(IIC-3.0D0)  .LT. 1.0D-6  .AND.
     &	DABS(IIIC-1.0D0) .LT. 1.0D-6)  THEN

c   IF( (IC-3.0D0)   .LT. 1.0D-8  .AND.
c    &	(IIC-3.0D0)  .LT. 1.0D-8  .AND.
c   &	(IIIC-3.0D0) .LT. 1.0D-8)  THEN

C
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
c         print*,'Location-2 of Subrt: INVEIGEN'
	CALL CUBIC(A1,A2,A3,E1,E2,E3)
	E1=1.0+E1
	E2=1.0+E2
	E3=1.0+E3
c        print*,'Location-3 of Subrt: INVEIGEN'
	RETURN
	END
C******************************************************************
C   THIS SUBROUTINE SOLVES A CUBIC EQUATION:
C   X^3 = A1*X^2 +A2*X + A3
C******************************************************************
	SUBROUTINE CUBIC(A1,A2,A3,X1,X2,X3)
	IMPLICIT REAL*8(A-H,O-Z)
c        print*,'Location-1 of Subrt: CUBIC'
	Q = (A1*A1)/3.0+A2
	R = (2.0*A1*A1*A1+9.0*A1*A2+27.0*A3)/27.0
        IF (Q .LT. 0.0) THEN   !BY Hamad
C            Print*, 'Error in Subrt. Cubic, Q < 0.0'
C            print*,'In Subrt CUBIC: Q, A1, A2, A3',Q,A1,A2,A3
            Q=0.0
        ENDIF
	S=2.0*DSQRT(Q/3.0)
c        print*,'Location-3 of Subrt: CUBIC'
	IF(S.EQ.0.0)THEN
	  X1=0.0
	  X2=0.0
	  X3=0.0
	ELSE
c       print*,'Location-4 of Subrt: CUBIC'
	  XARG=4.0*R/(S*S*S)
	  IF(ABS(XARG).GT.1.0D0)XARG=1.0D0
	  PI=DACOS(-1.0D0)
	  THETA=(1./3.)*DACOS(XARG)
	  X1=S*DCOS(THETA)
	  X2=S*DCOS(THETA-2.*PI/3.)
	  X3=S*DCOS(THETA+2.*PI/3.)
	ENDIF
c        print*,'Location-5 of Subrt: CUBIC'
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
C(((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))
C  THIS SUBROUTINE INVERTS A 3X3 MATRIX. METHOD FOLLOWED IS ON PAGE 83 
C  OF NUMERICAL RECIPES
C((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
	SUBROUTINE MAT3INV(A,B)
cvd$r  noconcurr
	IMPLICIT REAL*8(A-H,O-Z)
	DIMENSION A(3,3),B(3,3)
	DIMENSION A11(2,2),A12(2),A21(2),
     &           B11(2,2),B12(2),B21(2),
     &           R1(2,2),R2(2),R3(2)
C
C
C           A11 (2X2)    A12 (2x1)
C     A = 
C           A21 (1X2)    A22 (1X1)
C
C
C           B11 (2X2)    B12 (2x1)
C     B = 
C           B21 (1X2)    B22 (1X1)
C
        A11(1,1)=A(1,1)
        A11(1,2)=A(1,2)
        A11(2,1)=A(2,1)
        A11(2,2)=A(2,2)
        A12(1)  =A(1,3)
        A12(2)  =A(2,3)
        A21(1)  =A(3,1)
        A21(2)  =A(3,2)
        A22     =A(3,3)
C
C      R1 = INV (A11)
C
	DET = A11(1,1)*A11(2,2)-A11(1,2)*A11(2,1)
C
	R1(1,1) = A11(2,2)/DET
	R1(2,2) = A11(1,1)/DET
	R1(1,2) = -A11(1,2)/DET
	R1(2,1) = -A11(2,1)/DET
C
C      R2 = A21 R1
C
       R2(1) = A21(1)*R1(1,1) + A21(2)*R1(2,1)
       R2(2) = A21(1)*R1(1,2) + A21(2)*R1(2,2)
C
C      R3 = R1 A12
C
       R3(1) = R1(1,1)*A12(1) + R1(1,2)*A12(2)
       R3(2) = R1(2,1)*A12(1) + R1(2,2)*A12(2)
C
C      R4 = A21 R3
C
       R4 = A21(1)*R3(1) + A21(2)*R3(2)
C
C      R5 = R4 - A22
C
       R5 = R4 - A22
C
C      R6 = INV(R5)
C
       R6 =1.0D0/R5
C
C      B12 = R3  R6
C
       B12(1) = R3(1)*R6
       B12(2) = R3(2)*R6
C
C      B21 = R6  R2
C
       B21(1) = R6*R2(1)
       B21(2) = R6*R2(2)
C
C      R7 = R3[tensprod]B21
C      B11 = R1 - R7
C
       B11(1,1) = R1(1,1) - R3(1)*B21(1)
       B11(1,2) = R1(1,2) - R3(1)*B21(2)
       B11(2,1) = R1(2,1) - R3(2)*B21(1)
       B11(2,2) = R1(2,2) - R3(2)*B21(2)
C
C      B22 = -R6
C
       B22 = -R6
C
C      REASSEMBLE INTO B MATRIX
C
       B(1,1) = B11(1,1)
       B(1,2) = B11(1,2)
       B(2,1) = B11(2,1)
       B(2,2) = B11(2,2)
       B(1,3) = B12(1)
       B(2,3) = B12(2)
       B(3,1) = B21(1)
       B(3,2) = B21(2)
	B(3,3) = B22
C
	RETURN
	END
C(((((((((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))
      SUBROUTINE NEWT(XM,SO,HO,SS,AEXP,ICFLAG,DTIME,
     &			DGTAU,RSSTAU,TBTAUV,CMAT,CRSS,CRSST,DGMAX,TBTRV,icrys)
C
      INCLUDE'/nv/hp22/dpatel73/CPFEM/Classical/commonsn.txt'
	REAL*8, PARAMETER :: GDO = 0.001
	LOGICAL LMASK(6)

      DIMENSION CRSSdelta(48),CONST(6,6,48), DEPI(48),
     &ERR(6),AJAC(6,6),ABSA(6),D(6),DTBV(6),TBTRV(6),
     &ABDTBV(6),ABSDG(48),SLIPSIGN(48),CRSSNEW(48),HJ(48),TOLD(6)
C
C	Added by Hamad F. Al-Harbi: June 19, 2012
      DIMENSION DGTAU(48),RSSTAU(48),TBTAUV(6),
     &CMAT(6,48),CRSS(48),CRSST(48)
C
	IF (LHAMADTEST ==1) print*,'Begin of Subrt: NEWT'
        ITER = 0 
        DGDO = GDO*DTIME 
        XMINV= 1.0D0/XM 
C
 	RELAX = 1.0D0
 	ncut = 0
 	ncor = 0
 	DMAX = .2
 	ITERINT = 0
C 
      DO 1 I = 1,48
	   CRSSdelta(I)= CRSST(I)
			DO 1 K = 1,6 
			DO 1 J = 1,6 
1				CONST(J,K,I) = CMAT(J,I)*PMAT(K,I,icrys)
C
C,,,,,,,,,,,,,,,, start double loop ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
 999    CONTINUE 
C
	IF (LHAMADTEST ==1) print*,'Loc-1 of Subrt: NEWT' 
C       Evaluate resolved shear stress (ex-sbr RESOLVE)-------------
C
        DO 10 I = 1,48
 10      RSSTAU(I) = 0.0D0 
C
        DO 20 J = 1,6
         DO 20 I = 1,48
           RSSTAU(I) = RSSTAU(I)+TBTAUV(J)*PMAT(J,I,icrys)	!h2b
  20       SLIPSIGN(I) = sign(1.0D0,RSSTAU(I))
C 
C       ---------- (end ex-RESOLVE)---------------------------------
C       Evaluate deltaa-gamma on the slip systems (ex-sbr DGAMMAO)-------
        AMAXDG = 0.0D0
        DO 30 I = 1,48 
         IF(RSSTAU(I).EQ.0.0D0)THEN
           ABSDG(I) = 0.0D0
           DGTAU(I) = 0.0D0
         ELSE
	IF (LHAMADTEST ==1) print*,'Loc-1b of Subrt: NEWT'
C
            ABSDG(I) = DGDO*DABS(RSSTAU(I)/CRSSdelta(I))**XMINV	!hhh        
            DGTAU(I) =ABSDG(I)*SLIPSIGN(I)          
            AMAXDG = DMAX1(AMAXDG,ABSDG(I))
C         
         ENDIF        
 30     CONTINUE 

	IF (LHAMADTEST ==1) print*,'Loc-2 of Subrt: NEWT' 
C
 	IF (AMAXDG.GT.DMAX*RELAX.AND.ITER.NE.0)THEN
 	   IF(ICORR.GT.30)GO TO 33
 	   DO 32 J=1,6
            DTBV(J) = DTBV(J)*0.25
 32         TBTAUV(J) = TOLD(J)-DTBV(J)
 	   ICORR = ICORR + 1
 	   ncut = ncut+1
 	   GO TO 999
          ENDIF
      
 33	CONTINUE
 	DO 34 J=1,6 
 34	  TOLD(J) = TBTAUV(J)
C
	IF(ICORR.NE.0)NCOR=NCOR+1
	ICORR = 0
	ITERINT = ITERINT +1
      IF (LHAMADTEST ==1) print*,'Loc-3 of Subrt: NEWT' 

 	IF (ITERINT.GT.100)RELAX = RELAX*0.8D0
C       -----------------(end ex-DGAMMAO)--------------------------------
C
        DO 40 J=1,6
 40      ERR(J) =  TBTAUV(J) - TBTRV(J)
C
        DO 50 I=1,48
           DO 50 J=1,6
 50           ERR(J) = ERR(J)+DGTAU(I)*CMAT(J,I)
C
c
c
	  DO 60 K=1,6
           DO 60 J=1,6
 60           AJAC(J,K) = 0.0D0

        AJAC(1,1) = 1.0D0
        AJAC(2,2) = 1.0D0
        AJAC(3,3) = 1.0D0
        AJAC(4,4) = 1.0D0
        AJAC(5,5) = 1.0D0
        AJAC(6,6) = 1.0D0
c
C
	IF (LHAMADTEST ==1) print*,'Loc-4 of Subrt: NEWT' 
C

        I = 0
 99     CONTINUE
           I = I+1
           IF (DGTAU(I).NE.0.0D0) THEN
               DEPI(I) = DGTAU(I)*XMINV/RSSTAU(I)
C
               DO 100 K = 1,6
               DO 100 J = 1,6
 100              AJAC(J,K) = AJAC(J,K) +CONST(J,K,I)* DEPI(I)
C
           ENDIF
        IF(I.LT.48) GO TO 99
C
CC==================================================================
C      Solution of AJAC*DTBV=ERR using Gauss elimination          |
C      with partial (column) pivoting (ex- sbr's LUDCMP & LUBKSB) |
C
       DO 110 J=1,6
 110      LMASK(J) = .TRUE.
C
	IF (LHAMADTEST ==1) print*,'Loc-5 of Subrt: NEWT' 
C      do over the columns
C
       DO 170 J=1,5
C
C        column pivoting : find max coeff. in column J
C
         DO 120 K=J,6
 120        ABSA(K) = DABS(AJAC(K,J))
C
          DO 130 K=J,6
 130       IF(  ( (.NOT.LMASK(1)) .OR. (ABSA(K).GE.ABSA(1)) )
     &     .AND.( (.NOT.LMASK(2)) .OR. (ABSA(K).GE.ABSA(2)) )
     &     .AND.( (.NOT.LMASK(3)) .OR. (ABSA(K).GE.ABSA(3)) )
     &     .AND.( (.NOT.LMASK(4)) .OR. (ABSA(K).GE.ABSA(4)) )
     &     .AND.( (.NOT.LMASK(5)) .OR. (ABSA(K).GE.ABSA(5)) )
     &     .AND.( (.NOT.LMASK(6)) .OR. (ABSA(K).GE.ABSA(6)) )  )
     &                          IPIV = K
C
C        switch row IPIV and row J of matrix AJAC.......
         DO 135 JJ=J,6
            D(JJ)         = AJAC(J,JJ)
            AJAC(J,JJ)    = AJAC(IPIV,JJ)
 135        AJAC(IPIV,JJ) = D(JJ)
C
C        .....and r.h.s. ERR
C
         D(1)      = ERR(J)
         ERR(J)    = ERR(IPIV)
         ERR(IPIV) = D(1)
C
         R = 1.0D0/AJAC(J,J)
         LMASK(J) = .FALSE.
C
C
C        compute elimination coefficients for column J
C
         DO 140 K=J+1,6
 140        AJAC(K,J) = AJAC(K,J)*R
C
C        update all remaining columns
C
C        no data dependency because doloop starts at J+1
cvd$     nodepchk
         DO 150 L=J+1,6
cvd$        nodepchk
            DO 150 K=J+1,6
 150              AJAC(K,L) = AJAC(K,L) - AJAC(K,J)*AJAC(J,L)
C
C        update r.h.s
C
C        no data dependency because doloop starts at J+1
cvd$     nodepchk
         DO 160 K=J+1,6
 160        ERR(K) = ERR(K) - AJAC(K,J)*ERR(J)
C
 170   CONTINUE
	IF (LHAMADTEST ==1) print*,'Loc-6 of Subrt: NEWT' 

C      compute solution
C
       DTBV(6) = ERR(6)/AJAC(6,6)
       DO 190 J= 6,2,-1
           DO 180 K=1,J-1
 180           ERR(K) = ERR(K)-AJAC(K,J)*DTBV(J)
 190       DTBV(J-1) = ERR(J-1)/AJAC(J-1,J-1)
C
C==================end G algorithm=================================
C      
        DO 200 J = 1,6
         ABDTBV(J) = DABS(DTBV(J))
         TBTAUV(J)= TBTAUV(J) - DTBV(J)
 200   CONTINUE
C
        ERRMAX = 0.0D0
         DO 210 J = 1,6
 210      ERRMAX = DMAX1(ERRMAX,ABDTBV(J))
C
        ITER = ITER + 1
        IF(ITER.EQ.100) THEN
            ICFLAG=1
c            WRITE(*,*) 'ERRmax=', ERRMAX
c            WRITE(*,*) 'TBTAUV=', TBTAUV
        ENDIF
        IF(ITER.EQ.101)RETURN
        TOL=SO/10000.0          !Original Tolerance
        IF(ERRMAX .GT. TOL)GO TO 999
        IF(ITER.LE.3)GO TO 999
C''''''''''''''''''''end inside loop''''''''''''''''''''''''''''''
C       Evaluate resolved shear stress (ex-sbr RESOLVE)-------------
	IF (LHAMADTEST ==1) print*,'Loc-7 of Subrt: NEWT' 

        DO 310 I = 1,48
 310     RSSTAU(I) = 0.0D0
C
        DO 320 J = 1,6
         DO 320 I = 1,48
 320       RSSTAU(I) = RSSTAU(I)+TBTAUV(J)*PMAT(J,I,icrys)	!h2a
C
C       ---------- (end ex-RESOLVE)---------------------------------
C
C       Evaluate deltaa-gamma on the slip systems (ex-sbr DGAMMAO)-------
C
        DO 330 I = 1,48
         IF(RSSTAU(I).EQ.0.0D0)THEN
           ABSDG(I) = 0.0D0
           DGTAU(I) = 0.0D0
         ELSE
          ABSDG(I) = DGDO*DABS(RSSTAU(I)/CRSSdelta(I))**XMINV
          DGTAU(I) =sign(ABSDG(I),RSSTAU(I))
         ENDIF
 330     CONTINUE
C
C       ---------------------(end ex-DGAMMAO)---------------------------

	IF (LHAMADTEST ==1) print*,'Loc-8 of Subrt: NEWT'
!		print*,HO,1.0D0,CRSSdelta(1:48),SS,AEXP,CRSST(1:48)	
C       Update CRSSdelta ( ex sbr. UPCRSS)-----------------------------
       DO 350 I = 1, 48
         IF (CRSSdelta(I).GT.SS)THEN
!		IF (LHAMADTEST ==1) print*,'Loc-8a of Subrt: NEWT' 
	               HJ(I) = 0.0D0
         ELSE
!	IF (LHAMADTEST ==1) print*,'Loc-8b of Subrt: NEWT' 	
!	print*,HO,1.0D0,CRSSdelta(I),SS,AEXP
               HJ(I) = HO*(1.0D0 - CRSSdelta(I)/SS)**AEXP             
         ENDIF
		IF (LHAMADTEST ==1) print*,'Loc-8c of Subrt: NEWT' 
        CRSSNEW(I) = CRSST(I)
 350  CONTINUE

	IF (LHAMADTEST ==1) print*,'Loc-9 of Subrt: NEWT'
C

        DO 360 II = 1,48
         DO 360 I = 1,48
C	Added by Hamad F. Al-Harbi: June 19, 2012
 !360       CRSSNEW(I) = CRSSNEW(I)+HJ(II)*QLAT(I,II)*ABSDG(II) 
 360       CRSSNEW(I) = CRSSNEW(I)+HJ(II)*ABSDG(II)   !for no latent hard QLAT=1



	IF (LHAMADTEST ==1) print*,'Loc-10 of Subrt: NEWT' 
C

        ERCRSS = 0.0D0
        DO 370 I = 1,48
          ERCRSS = DMAX1(DABS(CRSSNEW(I)-CRSSdelta(I)),ERCRSS)
          CRSSdelta(I) = CRSSNEW(I)
 370   CONTINUE
C-------------- end ex-sbr UPCRSS ------------------------------------
C 
	IF (LHAMADTEST ==1) print*,'Loc-11 of Subrt: NEWT' 
	     
        IF(ERCRSS.GT.SO/1000.0)GO TO 999
C'''''''''''''''''''''''' end outside loop '''''''''''''''''''''''''''
       DGMAX = 0.0D0	!1
C
        DO 500 I = 1,48
        CRSS(I)=CRSSdelta(I)
500     DGMAX = DMAX1(DGMAX,ABSDG(I))	!2
C
 	RELAX = 1.0D0
 	ITERINT = 0
	IF (LHAMADTEST ==1) print*,'End of Subrt: NEWT' 
C

      RETURN
      END				
C((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))
        SUBROUTINE PREJAC(RTTAU,UTTAU,FT,FTAU,TENSP,TENSPP)
      INCLUDE'/nv/hp22/dpatel73/CPFEM/Classical/commonsn.txt'
      DIMENSION FTINV(3,3),FTTAU(3,3),RTTAU(3,3),UTTAU(3,3),
     &		  FT(3,3),FTAU(3,3),TENSP(6,6),TENSPP(3,3,6)
C
C  COMPUTE FT INVERSE
	IF (LHAMADTEST ==1) print*,'Beginning of Subrt: PREJAC'
C
	CALL MAT3INV(FT,FTINV)
C
C  COMPUTR FTTAU
C
             FTTAU(1,1) = FTAU(1,1)*FTINV(1,1) +
     &                FTAU(1,2)*FTINV(2,1) +
     &                FTAU(1,3)*FTINV(3,1)
      FTTAU(1,2) = FTAU(1,1)*FTINV(1,2) +
     &                FTAU(1,2)*FTINV(2,2) +
     &                FTAU(1,3)*FTINV(3,2)
      FTTAU(1,3) = FTAU(1,1)*FTINV(1,3) +
     &                FTAU(1,2)*FTINV(2,3) +
     &                FTAU(1,3)*FTINV(3,3)
      FTTAU(2,1) = FTAU(2,1)*FTINV(1,1) +
     &                FTAU(2,2)*FTINV(2,1) +
     &                FTAU(2,3)*FTINV(3,1)
      FTTAU(2,2) = FTAU(2,1)*FTINV(1,2) +
     &                FTAU(2,2)*FTINV(2,2) +
     &                FTAU(2,3)*FTINV(3,2)
      FTTAU(2,3) = FTAU(2,1)*FTINV(1,3) +
     &                FTAU(2,2)*FTINV(2,3) +
     &                FTAU(2,3)*FTINV(3,3)
      FTTAU(3,1) = FTAU(3,1)*FTINV(1,1) +
     &                FTAU(3,2)*FTINV(2,1) +
     &                FTAU(3,3)*FTINV(3,1)
      FTTAU(3,2) = FTAU(3,1)*FTINV(1,2) +
     &                FTAU(3,2)*FTINV(2,2) +
     &                FTAU(3,3)*FTINV(3,2)
      FTTAU(3,3) = FTAU(3,1)*FTINV(1,3) +
     &                FTAU(3,2)*FTINV(2,3) +
     &                FTAU(3,3)*FTINV(3,3)


C
C  POLAR DECOMPOSITION TO FIND U & R
C
	CALL DECOMP(FTTAU,RTTAU,UTTAU)	!This call is inside subrt. PREJAC
C
C  DEFINE TENSOR P
C
 	DO 100 K=1,6
	DO 100 J=1,6
 100      TENSP(J,K) =0.0D0
C
     	TENSP(1,1)  = UTTAU(1,1)
     	TENSP(2,2)  = UTTAU(2,2)
     	TENSP(3,3)  = UTTAU(3,3)
     	TENSP(1,4)  = 0.50D0*UTTAU(1,2)
     	TENSP(1,5)  = 0.50D0*UTTAU(1,3)
     	TENSP(2,4)  = 0.50D0*UTTAU(1,2)
     	TENSP(2,6)  = 0.50D0*UTTAU(2,3)
     	TENSP(3,5)  = 0.50D0*UTTAU(1,3)
     	TENSP(3,6)  = 0.50D0*UTTAU(2,3)
     	TENSP(4,1)  = 0.50D0*0.50D0*UTTAU(1,2)
     	TENSP(4,2)  = 0.50D0*0.50D0*UTTAU(1,2)
     	TENSP(4,5)  = 0.50D0*0.50D0*UTTAU(2,3)
     	TENSP(4,6)  = 0.50D0*0.50D0*UTTAU(1,3)
     	TENSP(5,1)  = 0.50D0*0.50D0*UTTAU(1,3)
     	TENSP(5,3)  = 0.50D0*0.50D0*UTTAU(1,3)
     	TENSP(5,4)  = 0.50D0*0.50D0*UTTAU(2,3)
     	TENSP(5,6)  = 0.50D0*0.50D0*UTTAU(1,2)
     	TENSP(6,2)  = 0.50D0*0.50D0*UTTAU(2,3)
     	TENSP(6,3)  = 0.50D0*0.50D0*UTTAU(2,3)
     	TENSP(6,4)  = 0.50D0*0.50D0*UTTAU(1,3)
     	TENSP(6,5)  = 0.50D0*0.50D0*UTTAU(1,2)
     	TENSP(4,4)  = 0.50D0*(UTTAU(1,1)+UTTAU(2,2))
     	TENSP(5,5)  = 0.50D0*(UTTAU(1,1)+UTTAU(3,3))
     	TENSP(6,6)  = 0.50D0*(UTTAU(2,2)+UTTAU(3,3))
C
    
	DO LLLL=1,6
C
        TENSPP(1,1,LLLL)=TENSP(1,LLLL) 
        TENSPP(2,2,LLLL)=TENSP(2,LLLL) 
        TENSPP(3,3,LLLL)=TENSP(3,LLLL) 
        TENSPP(1,2,LLLL)=TENSP(4,LLLL)*0.50D0 
        TENSPP(2,1,LLLL)=TENSP(4,LLLL)*0.50D0 
        TENSPP(1,3,LLLL)=TENSP(5,LLLL)*0.50D0 
        TENSPP(3,1,LLLL)=TENSP(5,LLLL)*0.50D0 
        TENSPP(2,3,LLLL)=TENSP(6,LLLL)*0.50D0 
        TENSPP(3,2,LLLL)=TENSP(6,LLLL)*0.50D0 
C
	END DO
C
	IF (LHAMADTEST ==1) print*,'End of Subrt: PREJAC'
C
        RETURN
        END
C((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))
        SUBROUTINE ROTMAT(TH,PHI,OM,Q,QT)
        IMPLICIT REAL*8(A-H,O-Z)
        DIMENSION Q(3,3),QT(3,3)
        SOM = DSIN(OM)
        COM = DCOS(OM)
        STH = DSIN(TH)
        CTH = DCOS(TH)
        SPH = DSIN(PHI)
        CPH = DCOS(PHI)
c
c        Q(2,1) = CPH*COM-SPH*SOM*CTH
c        Q(2,2) = SPH*COM+SOM*CPH*CTH
c        Q(2,3) = STH*SOM
c        Q(3,1) = -CPH*SOM-SPH*COM*CTH
c        Q(3,2) = -SPH*SOM+CPH*COM*CTH
c        Q(3,3) = STH*COM
c        Q(1,1) = STH*SPH
c        Q(1,2) = -STH*CPH
c        Q(1,3) = CTH
c		changes made from the above to the following (18 April BRD)
C	
	  Q(1,1) = CPH*COM-SPH*SOM*CTH
        Q(1,2) = SPH*COM+SOM*CPH*CTH
        Q(1,3) = STH*SOM
        Q(2,1) = -CPH*SOM-SPH*COM*CTH
        Q(2,2) = -SPH*SOM+CPH*COM*CTH
        Q(2,3) = STH*COM
        Q(3,1) = STH*SPH
        Q(3,2) = -STH*CPH
        Q(3,3) = CTH	


	
	QT(1,1)=Q(1,1) 
      QT(1,2)=Q(2,1) 
      QT(1,3)=Q(3,1)
      QT(2,1)=Q(1,2) 
      QT(2,2)=Q(2,2) 
      QT(2,3)=Q(3,2)
      QT(3,1)=Q(1,3) 
      QT(3,2)=Q(2,3) 
      QT(3,3)=Q(3,3)

C
        RETURN
        END
C((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))
	SUBROUTINE TRSTR(FTAU,CMAT,FPINVT,TBTRV,icrys)
      INCLUDE'/nv/hp22/dpatel73/CPFEM/Classical/commonsn.txt'
	DIMENSION Bdelta(3,3,48)
	DIMENSION TMP1(3,3,48),TMP2(3,3),TMP3(3,3),A(3,3),EV(6),TBTRV(6),
     &		  FTAU(3,3),CMAT(6,48),FPINVT(3,3)
C
	IF (LHAMADTEST ==1) print*,'Begin of Subrt: TRSTR'
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
        TMP2(1,1) = TMP3(1,1)*FPINVT(1,1) +
     &                TMP3(1,2)*FPINVT(2,1) +
     &                TMP3(1,3)*FPINVT(3,1)
      TMP2(1,2) = TMP3(1,1)*FPINVT(1,2) +
     &                TMP3(1,2)*FPINVT(2,2) +
     &                TMP3(1,3)*FPINVT(3,2)
      TMP2(1,3) = TMP3(1,1)*FPINVT(1,3) +
     &                TMP3(1,2)*FPINVT(2,3) +
     &                TMP3(1,3)*FPINVT(3,3)
      TMP2(2,1) = TMP3(2,1)*FPINVT(1,1) +
     &                TMP3(2,2)*FPINVT(2,1) +
     &                TMP3(2,3)*FPINVT(3,1)
      TMP2(2,2) = TMP3(2,1)*FPINVT(1,2) +
     &                TMP3(2,2)*FPINVT(2,2) +
     &                TMP3(2,3)*FPINVT(3,2)
      TMP2(2,3) = TMP3(2,1)*FPINVT(1,3) +
     &                TMP3(2,2)*FPINVT(2,3) +
     &                TMP3(2,3)*FPINVT(3,3)
      TMP2(3,1) = TMP3(3,1)*FPINVT(1,1) +
     &                TMP3(3,2)*FPINVT(2,1) +
     &                TMP3(3,3)*FPINVT(3,1)
      TMP2(3,2) = TMP3(3,1)*FPINVT(1,2) +
     &                TMP3(3,2)*FPINVT(2,2) +
     &                TMP3(3,3)*FPINVT(3,2)
      TMP2(3,3) = TMP3(3,1)*FPINVT(1,3) +
     &                TMP3(3,2)*FPINVT(2,3) +
     &                TMP3(3,3)*FPINVT(3,3)


C
        A(1,1) = FPINVT(1,1)*TMP2(1,1) +
     &                FPINVT(2,1)*TMP2(2,1) +
     &                FPINVT(3,1)*TMP2(3,1)
      A(1,2) = FPINVT(1,1)*TMP2(1,2) +
     &                FPINVT(2,1)*TMP2(2,2) +
     &                FPINVT(3,1)*TMP2(3,2)
      A(1,3) = FPINVT(1,1)*TMP2(1,3) +
     &                FPINVT(2,1)*TMP2(2,3) +
     &                FPINVT(3,1)*TMP2(3,3)
      A(2,1) = FPINVT(1,2)*TMP2(1,1) +
     &                FPINVT(2,2)*TMP2(2,1) +
     &                FPINVT(3,2)*TMP2(3,1)
      A(2,2) = FPINVT(1,2)*TMP2(1,2) +
     &                FPINVT(2,2)*TMP2(2,2) +
     &                FPINVT(3,2)*TMP2(3,2)
      A(2,3) = FPINVT(1,2)*TMP2(1,3) +
     &                FPINVT(2,2)*TMP2(2,3) +
     &                FPINVT(3,2)*TMP2(3,3)
      A(3,1) = FPINVT(1,3)*TMP2(1,1) +
     &                FPINVT(2,3)*TMP2(2,1) +
     &                FPINVT(3,3)*TMP2(3,1)
      A(3,2) = FPINVT(1,3)*TMP2(1,2) +
     &                FPINVT(2,3)*TMP2(2,2) +
     &                FPINVT(3,3)*TMP2(3,2)
      A(3,3) = FPINVT(1,3)*TMP2(1,3) +
     &                FPINVT(2,3)*TMP2(2,3) +
     &                FPINVT(3,3)*TMP2(3,3)

	IF(LHAMADTEST==1)print*,'Location-1 on Subrt:TRSTR'


      EV(1)=A(1,1) 
      EV(2)=A(2,2) 
      EV(3)=A(3,3)
      EV(4)=A(1,2) 
      EV(5)=A(1,3) 
      EV(6)=A(2,3) 

          DO 10 I=1,3
10         EV(I)= EV(I)-1.0D0
	IF(LHAMADTEST==1)print*,'Location-2 on Subrt:TRSTR'
C
          TBTRV(1) = ELAS(1,1,icrys)*EV(1) +
     &                ELAS(1,2,icrys)*EV(2) +
     &                ELAS(1,3,icrys)*EV(3) +
     &                ELAS(1,4,icrys)*EV(4) +
     &                ELAS(1,5,icrys)*EV(5) +
     &                ELAS(1,6,icrys)*EV(6)
        TBTRV(2) = ELAS(2,1,icrys)*EV(1) +
     &                ELAS(2,2,icrys)*EV(2) +
     &                ELAS(2,3,icrys)*EV(3) +
     &                ELAS(2,4,icrys)*EV(4) +
     &                ELAS(2,5,icrys)*EV(5) +
     &                ELAS(2,6,icrys)*EV(6)
        TBTRV(3) = ELAS(3,1,icrys)*EV(1) +
     &                ELAS(3,2,icrys)*EV(2) +
     &                ELAS(3,3,icrys)*EV(3) +
     &                ELAS(3,4,icrys)*EV(4) +
     &                ELAS(3,5,icrys)*EV(5) +
     &                ELAS(3,6,icrys)*EV(6)
        TBTRV(4) = ELAS(4,1,icrys)*EV(1) +
     &                ELAS(4,2,icrys)*EV(2) +
     &                ELAS(4,3,icrys)*EV(3) +
     &                ELAS(4,4,icrys)*EV(4) +
     &                ELAS(4,5,icrys)*EV(5) +
     &                ELAS(4,6,icrys)*EV(6)
        TBTRV(5) = ELAS(5,1,icrys)*EV(1) +
     &                ELAS(5,2,icrys)*EV(2) +
     &                ELAS(5,3,icrys)*EV(3) +
     &                ELAS(5,4,icrys)*EV(4) +
     &                ELAS(5,5,icrys)*EV(5) +
     &                ELAS(5,6,icrys)*EV(6)
        TBTRV(6) = ELAS(6,1,icrys)*EV(1) +
     &                ELAS(6,2,icrys)*EV(2) +
     &                ELAS(6,3,icrys)*EV(3) +
     &                ELAS(6,4,icrys)*EV(4) +
     &                ELAS(6,5,icrys)*EV(5) +
     &                ELAS(6,6,icrys)*EV(6)

	IF (LHAMADTEST ==1) print*,'Location-3 on Subrt: TRSTR'


          DO 20 I=1,6
20         TBTRV(I)= 0.50D0*TBTRV(I)
C
C    COMPUTE Cdelta AND STORE IN CMAT
C
C------------------ex sbr  FORMC -------------------------------
C
	DO 100 I = 1,48
C
       TMP1(1,1,I) = A(1,1)*SMATG(1,1,I,ICRYS) +
     &                A(1,2)*SMATG(2,1,I,ICRYS) +
     &                A(1,3)*SMATG(3,1,I,ICRYS)
      TMP1(1,2,I) = A(1,1)*SMATG(1,2,I,ICRYS) +
     &                A(1,2)*SMATG(2,2,I,ICRYS) +
     &                A(1,3)*SMATG(3,2,I,ICRYS)
      TMP1(1,3,I) = A(1,1)*SMATG(1,3,I,ICRYS) +
     &                A(1,2)*SMATG(2,3,I,ICRYS) +
     &                A(1,3)*SMATG(3,3,I,ICRYS)
      TMP1(2,1,I) = A(2,1)*SMATG(1,1,I,ICRYS) +
     &                A(2,2)*SMATG(2,1,I,ICRYS) +
     &                A(2,3)*SMATG(3,1,I,ICRYS)
      TMP1(2,2,I) = A(2,1)*SMATG(1,2,I,ICRYS) +
     &                A(2,2)*SMATG(2,2,I,ICRYS) +
     &                A(2,3)*SMATG(3,2,I,ICRYS)
      TMP1(2,3,I) = A(2,1)*SMATG(1,3,I,ICRYS) +
     &                A(2,2)*SMATG(2,3,I,ICRYS) +
     &                A(2,3)*SMATG(3,3,I,ICRYS)
      TMP1(3,1,I) = A(3,1)*SMATG(1,1,I,ICRYS) +
     &                A(3,2)*SMATG(2,1,I,ICRYS) +
     &                A(3,3)*SMATG(3,1,I,ICRYS)
      TMP1(3,2,I) = A(3,1)*SMATG(1,2,I,ICRYS) +
     &                A(3,2)*SMATG(2,2,I,ICRYS) +
     &                A(3,3)*SMATG(3,2,I,ICRYS)
      TMP1(3,3,I) = A(3,1)*SMATG(1,3,I,ICRYS) +
     &                A(3,2)*SMATG(2,3,I,ICRYS) +
     &                A(3,3)*SMATG(3,3,I,ICRYS)


C
          Bdelta(1,1,I) = TMP1(1,1,I)+TMP1(1,1,I)
          Bdelta(1,2,I) = TMP1(1,2,I)+TMP1(2,1,I)
          Bdelta(1,3,I) = TMP1(1,3,I)+TMP1(3,1,I)
          Bdelta(2,1,I) = TMP1(2,1,I)+TMP1(1,2,I)
          Bdelta(2,2,I) = TMP1(2,2,I)+TMP1(2,2,I)
          Bdelta(2,3,I) = TMP1(2,3,I)+TMP1(3,2,I)
          Bdelta(3,1,I) = TMP1(3,1,I)+TMP1(1,3,I)
          Bdelta(3,2,I) = TMP1(3,2,I)+TMP1(2,3,I)
          Bdelta(3,3,I) = TMP1(3,3,I)+TMP1(3,3,I)
        EV(1)=Bdelta(1,1,I) 
      EV(2)=Bdelta(2,2,I) 
      EV(3)=Bdelta(3,3,I)
      EV(4)=Bdelta(1,2,I) 
      EV(5)=Bdelta(1,3,I) 
      EV(6)=Bdelta(2,3,I) 

          CMAT(1,I) = ELAS(1,1,icrys)*EV(1) +
     &                ELAS(1,2,icrys)*EV(2) +
     &                ELAS(1,3,icrys)*EV(3) +
     &                ELAS(1,4,icrys)*EV(4) +
     &                ELAS(1,5,icrys)*EV(5) +
     &                ELAS(1,6,icrys)*EV(6)
        CMAT(2,I) = ELAS(2,1,icrys)*EV(1) +
     &                ELAS(2,2,icrys)*EV(2) +
     &                ELAS(2,3,icrys)*EV(3) +
     &                ELAS(2,4,icrys)*EV(4) +
     &                ELAS(2,5,icrys)*EV(5) +
     &                ELAS(2,6,icrys)*EV(6)
        CMAT(3,I) = ELAS(3,1,icrys)*EV(1) +
     &                ELAS(3,2,icrys)*EV(2) +
     &                ELAS(3,3,icrys)*EV(3) +
     &                ELAS(3,4,icrys)*EV(4) +
     &                ELAS(3,5,icrys)*EV(5) +
     &                ELAS(3,6,icrys)*EV(6)
        CMAT(4,I) = ELAS(4,1,icrys)*EV(1) +
     &                ELAS(4,2,icrys)*EV(2) +
     &                ELAS(4,3,icrys)*EV(3) +
     &                ELAS(4,4,icrys)*EV(4) +
     &                ELAS(4,5,icrys)*EV(5) +
     &                ELAS(4,6,icrys)*EV(6)
        CMAT(5,I) = ELAS(5,1,icrys)*EV(1) +
     &                ELAS(5,2,icrys)*EV(2) +
     &                ELAS(5,3,icrys)*EV(3) +
     &                ELAS(5,4,icrys)*EV(4) +
     &                ELAS(5,5,icrys)*EV(5) +
     &                ELAS(5,6,icrys)*EV(6)
        CMAT(6,I) = ELAS(6,1,icrys)*EV(1) +
     &                ELAS(6,2,icrys)*EV(2) +
     &                ELAS(6,3,icrys)*EV(3) +
     &                ELAS(6,4,icrys)*EV(4) +
     &                ELAS(6,5,icrys)*EV(5) +
     &                ELAS(6,6,icrys)*EV(6)


        DO 110 J=1,6
110       CMAT(J,I)=0.50D0*CMAT(J,I)
100    CONTINUE
C
	IF (LHAMADTEST ==1) print*,'End of Subrt: TRSTR'
	RETURN
	END
C((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))
      SUBROUTINE UPDATE(XM,SS,AEXP,TTAUV,DGTAU,
     &				    RSSTAU,DTDD,FST,RTTAU,UTTAU,FTAU,TBTAUV,
     &					TENSP,CMAT,TENSPP,CRSS,CRSST,
     &					FPINVT,FPITAU,JAC1,icrys)
C
      INCLUDE'/nv/hp22/dpatel73/CPFEM/Classical/commonsn.txt'
        REAL*8 LPBDT
        DIMENSION LPBDT(3,3),FPITAU(3,3),FSTAU(3,3),
     &            TBTAU(3,3),TTAU(3,3),FSINV(3,3)
	DIMENSION TMP1(3,3),TMP2(3,3),TMP3(3,3,3,3,48),
     &	          TMP4(3,3,3,3,48),TMPS1(3,3,6),TMPS2(3,3,6),
     &           TMPS5(3,3,6),TMPS6(3,3),TMPS7(3,3),TMPS8(3,3,6),
     &		   TMPS9(3,3,6),TMPW1(3,3),TMPW2(3,3,6),TMPW3(3,3,6),
     &           TMPW4(3,3,6),TMPW5(6)
	DIMENSION TENSCC(3,3,3,3),TENSC(6,6),TENSD(6,6),
     & TENSGG(3,3,3,3,48),TENSG(6,6,48),TENSJ(6,6,48),
     & TENSL(6,6),TENSB(48),TENSK(6,6),TKINV(6,6),
     & TENSM(6,6),TENSQ(6,6),TENSQQ(3,3,6),TENSR(6,48),
     & TENSS(3,3,6),TENSW(3,3,6)
	DIMENSION DELS(48),DIFS(48),DEPI(48),
     &           DEPA(48)
	DIMENSION UMX(6,6),RHS(6,6),ABSA(6),D(6),INDX(6)
       LOGICAL LMASK(6)
C	Added by Hamad F. Al-Harbi: June 19, 2012
      DIMENSION TTAUV(6),DGTAU(48),RSSTAU(48),DTDD(6,6),FPINVT(3,3),
     &		  FST(3,3),RTTAU(3,3),UTTAU(3,3),FTAU(3,3),TBTAUV(6),
     &		  TENSP(6,6),CMAT(6,48),TENSPP(3,3,6),CRSS(48),CRSST(48)

	DIMENSION ONET(3,3)
	DATA ONET(1,1),ONET(1,2),ONET(1,3),
     &	 ONET(2,1),ONET(2,2),ONET(2,3),
     &     ONET(3,1),ONET(3,2),ONET(3,3)
     & /1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0/
c     
	IF (LHAMADTEST ==1) print*,'Beginning of Subrt: UPDATE'
C  COMPUTE FPTAU INVERSE IN GLOBAL COORDINATES
C
        DO 10 M = 1,3
        DO 10 K = 1,3
        LPBDT(K,M)=0.0D0
        DO 11 KK = 1,48
 11       LPBDT(K,M) = LPBDT(K,M)+DGTAU(KK)*SMATG(K,M,KK,icrys)
 10     TMP1(K,M)  = ONET(K,M)-LPBDT(K,M)
C
          FPITAU(1,1) = FPINVT(1,1)*TMP1(1,1) +
     &                FPINVT(1,2)*TMP1(2,1) +
     &                FPINVT(1,3)*TMP1(3,1)
      FPITAU(1,2) = FPINVT(1,1)*TMP1(1,2) +
     &                FPINVT(1,2)*TMP1(2,2) +
     &                FPINVT(1,3)*TMP1(3,2)
      FPITAU(1,3) = FPINVT(1,1)*TMP1(1,3) +
     &                FPINVT(1,2)*TMP1(2,3) +
     &                FPINVT(1,3)*TMP1(3,3)
      FPITAU(2,1) = FPINVT(2,1)*TMP1(1,1) +
     &                FPINVT(2,2)*TMP1(2,1) +
     &                FPINVT(2,3)*TMP1(3,1)
      FPITAU(2,2) = FPINVT(2,1)*TMP1(1,2) +
     &                FPINVT(2,2)*TMP1(2,2) +
     &                FPINVT(2,3)*TMP1(3,2)
      FPITAU(2,3) = FPINVT(2,1)*TMP1(1,3) +
     &                FPINVT(2,2)*TMP1(2,3) +
     &                FPINVT(2,3)*TMP1(3,3)
      FPITAU(3,1) = FPINVT(3,1)*TMP1(1,1) +
     &                FPINVT(3,2)*TMP1(2,1) +
     &                FPINVT(3,3)*TMP1(3,1)
      FPITAU(3,2) = FPINVT(3,1)*TMP1(1,2) +
     &                FPINVT(3,2)*TMP1(2,2) +
     &                FPINVT(3,3)*TMP1(3,2)
      FPITAU(3,3) = FPINVT(3,1)*TMP1(1,3) +
     &                FPINVT(3,2)*TMP1(2,3) +
     &                FPINVT(3,3)*TMP1(3,3)

C
              DET = FPITAU(1,1)*(FPITAU(2,2)*FPITAU(3,3)-
     &                  FPITAU(2,3)*FPITAU(3,2))-
     &       FPITAU(1,2)*(FPITAU(2,1)*FPITAU(3,3)-
     &                  FPITAU(3,1)*FPITAU(2,3))+
     &       FPITAU(1,3)*(FPITAU(2,1)*FPITAU(3,2)-
     &                  FPITAU(3,1)*FPITAU(2,2))


C
        IF(DABS(DET-1.0D0).GT.1.0D-2)THEN
          WRITE(*,*)'DETERMINANT OF FPITAU = ',DET
        ENDIF
C
C  NORMALIZE FPITAU soo THAT DETERMINANT IS 1.0
C
        IF (DET.GT.0.0D0) THEN
C
          CDET = 1.0D0/(DET**(1.0D0/3.0D0))
          DO 20 K = 1,3
          DO 20 J = 1,3
 20        FPITAU(J,K) = FPITAU(J,K)*CDET
C
         ENDIF
        IF (LHAMADTEST ==1) print*,'Location-1 Subrt: UPDATE'
CC
C  COMPUTE FSTAU IN GLOBAL COORDINATES.
C
      FSTAU(1,1) = FTAU(1,1)*FPITAU(1,1) +
     &                FTAU(1,2)*FPITAU(2,1) +
     &                FTAU(1,3)*FPITAU(3,1)
      FSTAU(1,2) = FTAU(1,1)*FPITAU(1,2) +
     &                FTAU(1,2)*FPITAU(2,2) +
     &                FTAU(1,3)*FPITAU(3,2)
      FSTAU(1,3) = FTAU(1,1)*FPITAU(1,3) +
     &                FTAU(1,2)*FPITAU(2,3) +
     &                FTAU(1,3)*FPITAU(3,3)
      FSTAU(2,1) = FTAU(2,1)*FPITAU(1,1) +
     &                FTAU(2,2)*FPITAU(2,1) +
     &                FTAU(2,3)*FPITAU(3,1)
      FSTAU(2,2) = FTAU(2,1)*FPITAU(1,2) +
     &                FTAU(2,2)*FPITAU(2,2) +
     &                FTAU(2,3)*FPITAU(3,2)
      FSTAU(2,3) = FTAU(2,1)*FPITAU(1,3) +
     &                FTAU(2,2)*FPITAU(2,3) +
     &                FTAU(2,3)*FPITAU(3,3)
      FSTAU(3,1) = FTAU(3,1)*FPITAU(1,1) +
     &                FTAU(3,2)*FPITAU(2,1) +
     &                FTAU(3,3)*FPITAU(3,1)
      FSTAU(3,2) = FTAU(3,1)*FPITAU(1,2) +
     &                FTAU(3,2)*FPITAU(2,2) +
     &                FTAU(3,3)*FPITAU(3,2)
      FSTAU(3,3) = FTAU(3,1)*FPITAU(1,3) +
     &                FTAU(3,2)*FPITAU(2,3) +
     &                FTAU(3,3)*FPITAU(3,3)


C
C  COMPUTE CAUCHY STRESS IN GLOBAL COORDINATES 
C
      TBTAU(1,1)=TBTAUV(1) 
      TBTAU(1,2)=TBTAUV(4) 
      TBTAU(1,3)=TBTAUV(5)
      TBTAU(2,1)=TBTAUV(4) 
      TBTAU(2,2)=TBTAUV(2) 
      TBTAU(2,3)=TBTAUV(6)
      TBTAU(3,1)=TBTAUV(5) 
      TBTAU(3,2)=TBTAUV(6) 
      TBTAU(3,3)=TBTAUV(3)

C
      TMPW1(1,1) = TBTAU(1,1)*FSTAU(1,1) +
     &                TBTAU(1,2)*FSTAU(1,2) +
     &                TBTAU(1,3)*FSTAU(1,3)
      TMPW1(1,2) = TBTAU(1,1)*FSTAU(2,1) +
     &                TBTAU(1,2)*FSTAU(2,2) +
     &                TBTAU(1,3)*FSTAU(2,3)
      TMPW1(1,3) = TBTAU(1,1)*FSTAU(3,1) +
     &                TBTAU(1,2)*FSTAU(3,2) +
     &                TBTAU(1,3)*FSTAU(3,3)
      TMPW1(2,1) = TBTAU(2,1)*FSTAU(1,1) +
     &                TBTAU(2,2)*FSTAU(1,2) +
     &                TBTAU(2,3)*FSTAU(1,3)
      TMPW1(2,2) = TBTAU(2,1)*FSTAU(2,1) +
     &                TBTAU(2,2)*FSTAU(2,2) +
     &                TBTAU(2,3)*FSTAU(2,3)
      TMPW1(2,3) = TBTAU(2,1)*FSTAU(3,1) +
     &                TBTAU(2,2)*FSTAU(3,2) +
     &                TBTAU(2,3)*FSTAU(3,3)
      TMPW1(3,1) = TBTAU(3,1)*FSTAU(1,1) +
     &                TBTAU(3,2)*FSTAU(1,2) +
     &                TBTAU(3,3)*FSTAU(1,3)
      TMPW1(3,2) = TBTAU(3,1)*FSTAU(2,1) +
     &                TBTAU(3,2)*FSTAU(2,2) +
     &                TBTAU(3,3)*FSTAU(2,3)
      TMPW1(3,3) = TBTAU(3,1)*FSTAU(3,1) +
     &                TBTAU(3,2)*FSTAU(3,2) +
     &                TBTAU(3,3)*FSTAU(3,3)

        IF (LHAMADTEST ==1) print*,'Location-2 Subrt: UPDATE'

          TTAU(1,1) = FSTAU(1,1)*TMPW1(1,1) +
     &                FSTAU(1,2)*TMPW1(2,1) +
     &                FSTAU(1,3)*TMPW1(3,1)
      TTAU(1,2) = FSTAU(1,1)*TMPW1(1,2) +
     &                FSTAU(1,2)*TMPW1(2,2) +
     &                FSTAU(1,3)*TMPW1(3,2)
      TTAU(1,3) = FSTAU(1,1)*TMPW1(1,3) +
     &                FSTAU(1,2)*TMPW1(2,3) +
     &                FSTAU(1,3)*TMPW1(3,3)
      TTAU(2,1) = FSTAU(2,1)*TMPW1(1,1) +
     &                FSTAU(2,2)*TMPW1(2,1) +
     &                FSTAU(2,3)*TMPW1(3,1)
      TTAU(2,2) = FSTAU(2,1)*TMPW1(1,2) +
     &                FSTAU(2,2)*TMPW1(2,2) +
     &                FSTAU(2,3)*TMPW1(3,2)
      TTAU(2,3) = FSTAU(2,1)*TMPW1(1,3) +
     &                FSTAU(2,2)*TMPW1(2,3) +
     &                FSTAU(2,3)*TMPW1(3,3)
      TTAU(3,1) = FSTAU(3,1)*TMPW1(1,1) +
     &                FSTAU(3,2)*TMPW1(2,1) +
     &                FSTAU(3,3)*TMPW1(3,1)
      TTAU(3,2) = FSTAU(3,1)*TMPW1(1,2) +
     &                FSTAU(3,2)*TMPW1(2,2) +
     &                FSTAU(3,3)*TMPW1(3,2)
      TTAU(3,3) = FSTAU(3,1)*TMPW1(1,3) +
     &                FSTAU(3,2)*TMPW1(2,3) +
     &                FSTAU(3,3)*TMPW1(3,3)


              DET = FSTAU(1,1)*(FSTAU(2,2)*FSTAU(3,3)-
     &                  FSTAU(2,3)*FSTAU(3,2))-
     &       FSTAU(1,2)*(FSTAU(2,1)*FSTAU(3,3)-
     &                  FSTAU(3,1)*FSTAU(2,3))+
     &       FSTAU(1,3)*(FSTAU(2,1)*FSTAU(3,2)-
     &                  FSTAU(3,1)*FSTAU(2,2))

C
        DETINV = 1.0D0/DET
        DO 30 J = 1,3
        DO 30 K = 1,3
 30           TTAU(J,K) = TTAU(J,K)*DETINV
 !30         FPINV(J,K,NPT,NOEL) = FPITAU(J,K)
C
      TTAUV(1)=TTAU(1,1) 
      TTAUV(2)=TTAU(2,2) 
      TTAUV(3)=TTAU(3,3)
      TTAUV(4)=TTAU(1,2) 
      TTAUV(5)=TTAU(1,3) 
      TTAUV(6)=TTAU(2,3) 

        IF (LHAMADTEST ==1) print*,'Location-3 Subrt: UPDATE'

C
C	update the jacobian if required
      IF (JAC1.NE.1) GO TO 400	!JAC=1>>Jacobian to be updated all the time
C
C========================================================
C	EVALUATE THE NEW JACOBIAN FOR THE CRYSTAL
C========================================================
C
C   1) Evaluate TENSCC
C
        TMP1(1,1) = UTTAU(1,1)*FST(1,1) +
     &                UTTAU(1,2)*FST(2,1) +
     &                UTTAU(1,3)*FST(3,1)
      TMP1(1,2) = UTTAU(1,1)*FST(1,2) +
     &                UTTAU(1,2)*FST(2,2) +
     &                UTTAU(1,3)*FST(3,2)
      TMP1(1,3) = UTTAU(1,1)*FST(1,3) +
     &                UTTAU(1,2)*FST(2,3) +
     &                UTTAU(1,3)*FST(3,3)
      TMP1(2,1) = UTTAU(2,1)*FST(1,1) +
     &                UTTAU(2,2)*FST(2,1) +
     &                UTTAU(2,3)*FST(3,1)
      TMP1(2,2) = UTTAU(2,1)*FST(1,2) +
     &                UTTAU(2,2)*FST(2,2) +
     &                UTTAU(2,3)*FST(3,2)
      TMP1(2,3) = UTTAU(2,1)*FST(1,3) +
     &                UTTAU(2,2)*FST(2,3) +
     &                UTTAU(2,3)*FST(3,3)
      TMP1(3,1) = UTTAU(3,1)*FST(1,1) +
     &                UTTAU(3,2)*FST(2,1) +
     &                UTTAU(3,3)*FST(3,1)
      TMP1(3,2) = UTTAU(3,1)*FST(1,2) +
     &                UTTAU(3,2)*FST(2,2) +
     &                UTTAU(3,3)*FST(3,2)
      TMP1(3,3) = UTTAU(3,1)*FST(1,3) +
     &                UTTAU(3,2)*FST(2,3) +
     &                UTTAU(3,3)*FST(3,3)


        TMP2(1,1) = FST(1,1)*UTTAU(1,1) +
     &                FST(2,1)*UTTAU(2,1) +
     &                FST(3,1)*UTTAU(3,1)
      TMP2(1,2) = FST(1,1)*UTTAU(1,2) +
     &                FST(2,1)*UTTAU(2,2) +
     &                FST(3,1)*UTTAU(3,2)
      TMP2(1,3) = FST(1,1)*UTTAU(1,3) +
     &                FST(2,1)*UTTAU(2,3) +
     &                FST(3,1)*UTTAU(3,3)
      TMP2(2,1) = FST(1,2)*UTTAU(1,1) +
     &                FST(2,2)*UTTAU(2,1) +
     &                FST(3,2)*UTTAU(3,1)
      TMP2(2,2) = FST(1,2)*UTTAU(1,2) +
     &                FST(2,2)*UTTAU(2,2) +
     &                FST(3,2)*UTTAU(3,2)
      TMP2(2,3) = FST(1,2)*UTTAU(1,3) +
     &                FST(2,2)*UTTAU(2,3) +
     &                FST(3,2)*UTTAU(3,3)
      TMP2(3,1) = FST(1,3)*UTTAU(1,1) +
     &                FST(2,3)*UTTAU(2,1) +
     &                FST(3,3)*UTTAU(3,1)
      TMP2(3,2) = FST(1,3)*UTTAU(1,2) +
     &                FST(2,3)*UTTAU(2,2) +
     &                FST(3,3)*UTTAU(3,2)
      TMP2(3,3) = FST(1,3)*UTTAU(1,3) +
     &                FST(2,3)*UTTAU(2,3) +
     &                FST(3,3)*UTTAU(3,3)

        IF (LHAMADTEST ==1) print*,'Location-4 Subrt: UPDATE'

C
	DO 35 L=1,3
	 DO 35 K=1,3
	  DO 35 J=1,3
           DO 35 M=1,3
 35    	TENSCC(M,J,K,L)= FST(K,M)*TMP1(L,J)+FST(L,J)*TMP2(M,K)
C
C   2) Evaluate TENSGG
C
	DO 40 I=1,48
	 DO 40 L=1,3
	  DO 40 K=1,3
            TMP3(1,1,K,L,I) = TENSCC(1,1,K,L)*SMATG(1,1,I,ICRYS) +
     &                TENSCC(1,2,K,L)*SMATG(2,1,I,ICRYS) +
     &                TENSCC(1,3,K,L)*SMATG(3,1,I,ICRYS)
      TMP3(1,2,K,L,I) = TENSCC(1,1,K,L)*SMATG(1,2,I,ICRYS) +
     &                TENSCC(1,2,K,L)*SMATG(2,2,I,ICRYS) +
     &                TENSCC(1,3,K,L)*SMATG(3,2,I,ICRYS)
      TMP3(1,3,K,L,I) = TENSCC(1,1,K,L)*SMATG(1,3,I,ICRYS) +
     &                TENSCC(1,2,K,L)*SMATG(2,3,I,ICRYS) +
     &                TENSCC(1,3,K,L)*SMATG(3,3,I,ICRYS)
      TMP3(2,1,K,L,I) = TENSCC(2,1,K,L)*SMATG(1,1,I,ICRYS) +
     &                TENSCC(2,2,K,L)*SMATG(2,1,I,ICRYS) +
     &                TENSCC(2,3,K,L)*SMATG(3,1,I,ICRYS)
      TMP3(2,2,K,L,I) = TENSCC(2,1,K,L)*SMATG(1,2,I,ICRYS) +
     &                TENSCC(2,2,K,L)*SMATG(2,2,I,ICRYS) +
     &                TENSCC(2,3,K,L)*SMATG(3,2,I,ICRYS)
      TMP3(2,3,K,L,I) = TENSCC(2,1,K,L)*SMATG(1,3,I,ICRYS) +
     &                TENSCC(2,2,K,L)*SMATG(2,3,I,ICRYS) +
     &                TENSCC(2,3,K,L)*SMATG(3,3,I,ICRYS)
      TMP3(3,1,K,L,I) = TENSCC(3,1,K,L)*SMATG(1,1,I,ICRYS) +
     &                TENSCC(3,2,K,L)*SMATG(2,1,I,ICRYS) +
     &                TENSCC(3,3,K,L)*SMATG(3,1,I,ICRYS)
      TMP3(3,2,K,L,I) = TENSCC(3,1,K,L)*SMATG(1,2,I,ICRYS) +
     &                TENSCC(3,2,K,L)*SMATG(2,2,I,ICRYS) +
     &                TENSCC(3,3,K,L)*SMATG(3,2,I,ICRYS)
      TMP3(3,3,K,L,I) = TENSCC(3,1,K,L)*SMATG(1,3,I,ICRYS) +
     &                TENSCC(3,2,K,L)*SMATG(2,3,I,ICRYS) +
     &                TENSCC(3,3,K,L)*SMATG(3,3,I,ICRYS)


         TMP4(1,1,K,L,I) = SMATG(1,1,I,ICRYS)*TENSCC(1,1,K,L) +
     &                SMATG(2,1,I,ICRYS)*TENSCC(2,1,K,L) +
     &                SMATG(3,1,I,ICRYS)*TENSCC(3,1,K,L)
      TMP4(1,2,K,L,I) = SMATG(1,1,I,ICRYS)*TENSCC(1,2,K,L) +
     &                SMATG(2,1,I,ICRYS)*TENSCC(2,2,K,L) +
     &                SMATG(3,1,I,ICRYS)*TENSCC(3,2,K,L)
      TMP4(1,3,K,L,I) = SMATG(1,1,I,ICRYS)*TENSCC(1,3,K,L) +
     &                SMATG(2,1,I,ICRYS)*TENSCC(2,3,K,L) +
     &                SMATG(3,1,I,ICRYS)*TENSCC(3,3,K,L)
      TMP4(2,1,K,L,I) = SMATG(1,2,I,ICRYS)*TENSCC(1,1,K,L) +
     &                SMATG(2,2,I,ICRYS)*TENSCC(2,1,K,L) +
     &                SMATG(3,2,I,ICRYS)*TENSCC(3,1,K,L)
      TMP4(2,2,K,L,I) = SMATG(1,2,I,ICRYS)*TENSCC(1,2,K,L) +
     &                SMATG(2,2,I,ICRYS)*TENSCC(2,2,K,L) +
     &                SMATG(3,2,I,ICRYS)*TENSCC(3,2,K,L)
      TMP4(2,3,K,L,I) = SMATG(1,2,I,ICRYS)*TENSCC(1,3,K,L) +
     &                SMATG(2,2,I,ICRYS)*TENSCC(2,3,K,L) +
     &                SMATG(3,2,I,ICRYS)*TENSCC(3,3,K,L)
      TMP4(3,1,K,L,I) = SMATG(1,3,I,ICRYS)*TENSCC(1,1,K,L) +
     &                SMATG(2,3,I,ICRYS)*TENSCC(2,1,K,L) +
     &                SMATG(3,3,I,ICRYS)*TENSCC(3,1,K,L)
      TMP4(3,2,K,L,I) = SMATG(1,3,I,ICRYS)*TENSCC(1,2,K,L) +
     &                SMATG(2,3,I,ICRYS)*TENSCC(2,2,K,L) +
     &                SMATG(3,3,I,ICRYS)*TENSCC(3,2,K,L)
      TMP4(3,3,K,L,I) = SMATG(1,3,I,ICRYS)*TENSCC(1,3,K,L) +
     &                SMATG(2,3,I,ICRYS)*TENSCC(2,3,K,L) +
     &                SMATG(3,3,I,ICRYS)*TENSCC(3,3,K,L)


             TENSGG(1,1,K,L,I)=TMP3(1,1,K,L,I)+TMP4(1,1,K,L,I)
             TENSGG(1,2,K,L,I)=TMP3(1,2,K,L,I)+TMP4(1,2,K,L,I)
             TENSGG(1,3,K,L,I)=TMP3(1,3,K,L,I)+TMP4(1,3,K,L,I)
             TENSGG(2,1,K,L,I)=TMP3(2,1,K,L,I)+TMP4(2,1,K,L,I)
             TENSGG(2,2,K,L,I)=TMP3(2,2,K,L,I)+TMP4(2,2,K,L,I)
             TENSGG(2,3,K,L,I)=TMP3(2,3,K,L,I)+TMP4(2,3,K,L,I)
             TENSGG(3,1,K,L,I)=TMP3(3,1,K,L,I)+TMP4(3,1,K,L,I)
             TENSGG(3,2,K,L,I)=TMP3(3,2,K,L,I)+TMP4(3,2,K,L,I)
             TENSGG(3,3,K,L,I)=TMP3(3,3,K,L,I)+TMP4(3,3,K,L,I)
C
C
 40	CONTINUE
C
        IF (LHAMADTEST ==1) print*,'Location-5 Subrt: UPDATE'
C   3) Evaluate TENSC,TENSG
C
	      TENSC(1,1)=TENSCC(1,1,1,1) 
      TENSC(1,2)=TENSCC(1,1,2,2) 
      TENSC(1,3)=TENSCC(1,1,3,3) 
      TENSC(1,4)=(TENSCC(1,1,1,2)+TENSCC(1,1,2,1))*0.50D0
      TENSC(1,5)=(TENSCC(1,1,1,3)+TENSCC(1,1,3,1))*0.50D0
      TENSC(1,6)=(TENSCC(1,1,2,3)+TENSCC(1,1,3,2))*0.50D0
      TENSC(2,1)=TENSCC(2,2,1,1) 
      TENSC(2,2)=TENSCC(2,2,2,2) 
      TENSC(2,3)=TENSCC(2,2,3,3) 
      TENSC(2,4)=(TENSCC(2,2,1,2)+TENSCC(2,2,2,1))*0.50D0
      TENSC(2,5)=(TENSCC(2,2,1,3)+TENSCC(2,2,3,1))*0.50D0
      TENSC(2,6)=(TENSCC(2,2,2,3)+TENSCC(2,2,3,2))*0.50D0
      TENSC(3,1)=TENSCC(3,3,1,1) 
      TENSC(3,2)=TENSCC(3,3,2,2) 
      TENSC(3,3)=TENSCC(3,3,3,3) 
      TENSC(3,4)=(TENSCC(3,3,1,2)+TENSCC(3,3,2,1))*0.50D0
      TENSC(3,5)=(TENSCC(3,3,1,3)+TENSCC(3,3,3,1))*0.50D0
      TENSC(3,6)=(TENSCC(3,3,2,3)+TENSCC(3,3,3,2))*0.50D0
      TENSC(4,1)=TENSCC(1,2,1,1) 
      TENSC(4,2)=TENSCC(1,2,2,2) 
      TENSC(4,3)=TENSCC(1,2,3,3) 
      TENSC(4,4)=(TENSCC(1,2,1,2)+TENSCC(1,2,2,1))*0.50D0
      TENSC(4,5)=(TENSCC(1,2,1,3)+TENSCC(1,2,3,1))*0.50D0
      TENSC(4,6)=(TENSCC(1,2,2,3)+TENSCC(1,2,3,2))*0.50D0
      TENSC(5,1)=TENSCC(1,3,1,1) 
      TENSC(5,2)=TENSCC(1,3,2,2) 
      TENSC(5,3)=TENSCC(1,3,3,3) 
      TENSC(5,4)=(TENSCC(1,3,1,2)+TENSCC(1,3,2,1))*0.50D0
      TENSC(5,5)=(TENSCC(1,3,1,3)+TENSCC(1,3,3,1))*0.50D0
      TENSC(5,6)=(TENSCC(1,3,2,3)+TENSCC(1,3,3,2))*0.50D0
      TENSC(6,1)=TENSCC(2,3,1,1) 
      TENSC(6,2)=TENSCC(2,3,2,2) 
      TENSC(6,3)=TENSCC(2,3,3,3) 
      TENSC(6,4)=(TENSCC(2,3,1,2)+TENSCC(2,3,2,1))*0.50D0
      TENSC(6,5)=(TENSCC(2,3,1,3)+TENSCC(2,3,3,1))*0.50D0
      TENSC(6,6)=(TENSCC(2,3,2,3)+TENSCC(2,3,3,2))*0.50D0

C
	DO 50 I=1,48
 	       TENSG(1,1,I)=TENSGG(1,1,1,1,I) 
      TENSG(1,2,I)=TENSGG(1,1,2,2,I) 
      TENSG(1,3,I)=TENSGG(1,1,3,3,I) 
      TENSG(1,4,I)=(TENSGG(1,1,1,2,I)+TENSGG(1,1,2,1,I))*0.50D0
      TENSG(1,5,I)=(TENSGG(1,1,1,3,I)+TENSGG(1,1,3,1,I))*0.50D0
      TENSG(1,6,I)=(TENSGG(1,1,2,3,I)+TENSGG(1,1,3,2,I))*0.50D0
      TENSG(2,1,I)=TENSGG(2,2,1,1,I) 
      TENSG(2,2,I)=TENSGG(2,2,2,2,I) 
      TENSG(2,3,I)=TENSGG(2,2,3,3,I) 
      TENSG(2,4,I)=(TENSGG(2,2,1,2,I)+TENSGG(2,2,2,1,I))*0.50D0
      TENSG(2,5,I)=(TENSGG(2,2,1,3,I)+TENSGG(2,2,3,1,I))*0.50D0
      TENSG(2,6,I)=(TENSGG(2,2,2,3,I)+TENSGG(2,2,3,2,I))*0.50D0
      TENSG(3,1,I)=TENSGG(3,3,1,1,I) 
      TENSG(3,2,I)=TENSGG(3,3,2,2,I) 
      TENSG(3,3,I)=TENSGG(3,3,3,3,I) 
      TENSG(3,4,I)=(TENSGG(3,3,1,2,I)+TENSGG(3,3,2,1,I))*0.50D0
      TENSG(3,5,I)=(TENSGG(3,3,1,3,I)+TENSGG(3,3,3,1,I))*0.50D0
      TENSG(3,6,I)=(TENSGG(3,3,2,3,I)+TENSGG(3,3,3,2,I))*0.50D0
      TENSG(4,1,I)=TENSGG(1,2,1,1,I) 
      TENSG(4,2,I)=TENSGG(1,2,2,2,I) 
      TENSG(4,3,I)=TENSGG(1,2,3,3,I) 
      TENSG(4,4,I)=(TENSGG(1,2,1,2,I)+TENSGG(1,2,2,1,I))*0.50D0
      TENSG(4,5,I)=(TENSGG(1,2,1,3,I)+TENSGG(1,2,3,1,I))*0.50D0
      TENSG(4,6,I)=(TENSGG(1,2,2,3,I)+TENSGG(1,2,3,2,I))*0.50D0
      TENSG(5,1,I)=TENSGG(1,3,1,1,I) 
      TENSG(5,2,I)=TENSGG(1,3,2,2,I) 
      TENSG(5,3,I)=TENSGG(1,3,3,3,I) 
      TENSG(5,4,I)=(TENSGG(1,3,1,2,I)+TENSGG(1,3,2,1,I))*0.50D0
      TENSG(5,5,I)=(TENSGG(1,3,1,3,I)+TENSGG(1,3,3,1,I))*0.50D0
      TENSG(5,6,I)=(TENSGG(1,3,2,3,I)+TENSGG(1,3,3,2,I))*0.50D0
      TENSG(6,1,I)=TENSGG(2,3,1,1,I) 
      TENSG(6,2,I)=TENSGG(2,3,2,2,I) 
      TENSG(6,3,I)=TENSGG(2,3,3,3,I) 
      TENSG(6,4,I)=(TENSGG(2,3,1,2,I)+TENSGG(2,3,2,1,I))*0.50D0
      TENSG(6,5,I)=(TENSGG(2,3,1,3,I)+TENSGG(2,3,3,1,I))*0.50D0
      TENSG(6,6,I)=(TENSGG(2,3,2,3,I)+TENSGG(2,3,3,2,I))*0.50D0

 50	CONTINUE
        IF (LHAMADTEST ==1) print*,'Location-6 Subrt: UPDATE'

C   4) Evaluate TENSD ,TENSJ
C
	DO 60 J=1,6
        DO 60 M=1,6
         TENSD(M,J)= 0.0D0
         DO 65 K=1,6
65       TENSD(M,J)=TENSD(M,J)+ELAS(M,K,icrys)*TENSC(K,J)
60  	 TENSD(M,J)=TENSD(M,J)*0.50D0 
        DO 70 I=1,48
	DO 70 J=1,6
        DO 70 M=1,6
         TENSJ(M,J,I)=0.0D0
         DO 75 K=1,6
75       TENSJ(M,J,I)=TENSJ(M,J,I)+ELAS(M,K,icrys)*TENSG(K,J,I)
70       TENSJ(M,J,I) = 0.50D0*TENSJ(M,J,I) 
C
C   5) Evaluate TENSL
C
	DO 120 J=1,6
	DO 120 M=1,6
         TENSL(M,J) = TENSD(M,J)
         DO 120 KK = 1,48
 120	 TENSL(M,J) = TENSL(M,J)-DGTAU(KK)*TENSJ(M,J,KK)
C
C
C   6) Evaluate TENSB
C
	DO 130 I=1,48
        DELS(I) = CRSS(I)-CRSST(I)
        DIFS(I) = SS -CRSS(I)
        IF((DGTAU(I).EQ.0.0D0).OR.(DELS(I).LE.0.0D0).OR.
     &    (RSSTAU(I).EQ.0.0D0).OR.(DIFS(I).LE.0.0D0))THEN
          TENSB(I) = 0.0D0
        ELSE
	   DEPI(I) = DGTAU(I)/(RSSTAU(I)*XM)
	   DEPA(I) = 1.0D0+DELS(I)*DIFS(I)/(CRSST(I)*
     &	             XM*(DIFS(I)+DELS(I)*AEXP))
	   TENSB(I) = DEPI(I)/DEPA(I)
	 ENDIF
 130	CONTINUE
C
C   7) Evaluate TENSK
C	
	DO 140 J=1,6
	DO 140 M=1,6
		IF (M .EQ. J) THEN
			TENSK(M,J)=1.0D0
		ELSE
		    TENSK(M,J)=0.0D0
		ENDIF
c
         DO 140 KK=1,48
 140	 TENSK(M,J)=TENSK(M,J)+CMAT(M,KK)*PMAT(J,KK,icrys)*TENSB(KK)
C
        IF (LHAMADTEST ==1) print*,'Location-7 Subrt: UPDATE'
C       error: illegal memory reference
C   7) Evaluate TKINV using gauss-jordan
C==================================================================
C      Solution of TENSK*TKINV=ONES using Gauss-Jordan elimination 
C      with partial (column) pivoting
C==================================================================
C
       DO 210 J=1,6
          LMASK(J) = .TRUE.
          DO 210 K=1,6
 210           RHS(K,J) = 0.0D0
        RHS(1,1) = 1.0D0
        RHS(2,2) = 1.0D0
        RHS(3,3) = 1.0D0
        RHS(4,4) = 1.0D0
        RHS(5,5) = 1.0D0
        RHS(6,6) = 1.0D0		
c
c        IF (LHAMADTEST ==1) print*,'Location-7a Subrt: UPDATE'
C      do over the columns
C
       DO 270 J=1,6
C
C        column pivoting : find max coeff. in column J
C
         DO 220 K=1,6
 220        ABSA(K) = DABS(TENSK(K,J))
C
c        IF (LHAMADTEST ==1) print*,'Location-7b Subrt: UPDATE'
 	  DO 230 K=1,6
  230       IF(LMASK(K)
     &     .AND.( (.NOT.LMASK(1)) .OR. (ABSA(K).GE.ABSA(1)) )
     &     .AND.( (.NOT.LMASK(2)) .OR. (ABSA(K).GE.ABSA(2)) )
     &     .AND.( (.NOT.LMASK(3)) .OR. (ABSA(K).GE.ABSA(3)) )
     &     .AND.( (.NOT.LMASK(4)) .OR. (ABSA(K).GE.ABSA(4)) )
     &     .AND.( (.NOT.LMASK(5)) .OR. (ABSA(K).GE.ABSA(5)) )
     &     .AND.( (.NOT.LMASK(6)) .OR. (ABSA(K).GE.ABSA(6)) )  )
     &                          IPIV = K
C        store pivot and position
         INDX(J)     = IPIV
	  D(IPIV)     = 1.0D0/TENSK (IPIV,J) 
         LMASK(IPIV) = .FALSE.
C
c        IF (LHAMADTEST ==1) print*,'Location-7c Subrt: UPDATE'
C        compute elimination coefficients for column J
C
         DO 240 K=1,6
 240        TENSK(K,J) = TENSK(K,J)*D(IPIV)
C
C        value 0.0D0 cause pivot row to remain unchanged
C        IF (LHAMADTEST ==1) print*,'Location-7d Subrt: UPDATE'
C
         TENSK(IPIV,J) = 0.0D0
C
C        update all remaining columns
C       
C        no data dependency because TENSK(IPIV,J)=0.0
cvd$     nodepchk
         DO 250 L=J+1,6
cvd$        nodepchk
            DO 250 K=1,6
 250              TENSK(K,L) = TENSK(K,L) - TENSK(K,J)*TENSK(IPIV,L)
C
C        update r.h.s
C        IF (LHAMADTEST ==1) print*,'Location-7e Subrt: UPDATE'
C
C        no data dependency because TENSK(IPIV,J)=0.0
cvd$     nodepchk
         DO 260 L=1,6
cvd$        nodepchk
            DO 260 K=1,6

 260        RHS(K,L) = RHS(K,L) - TENSK(K,J)*RHS(IPIV,L)
C
C        IF (LHAMADTEST ==1) print*,'Location-7f Subrt: UPDATE'
 270   CONTINUE
C
C      compute all columns L of the solution UMX(L) of
C              (1/D)*UMX(L)=RHS(L) 
C      (non ordered solution of original system)       
C
       DO 280 L=1,6
       DO 280 J=1,6
 280      UMX(J,L) = RHS(J,L)*D(J)
C
C      gather solution to build TKINV
C        IF (LHAMADTEST ==1) print*,'Location-7g Subrt: UPDATE'
C
       DO 290 L=1,6
       DO 290 J=1,6
 290      TKINV(J,L) = UMX(INDX(J),L)
C
C==================end G-J algorithm=================================
C
        IF (LHAMADTEST ==1) print*,'Location-8 Subrt: UPDATE'

C   8) Evaluate TENSM,TENSQ,TENSQQ,TENSR
C
	DO 300 J=1,6
	 DO 300 M=1,6
 300	   TENSM(M,J) = TKINV(M,1)*TENSL(1,J)+
     &                 TKINV(M,2)*TENSL(2,J)+
     &                 TKINV(M,3)*TENSL(3,J)+
     &                 TKINV(M,4)*TENSL(4,J)+
     &                 TKINV(M,5)*TENSL(5,J)+
     &                 TKINV(M,6)*TENSL(6,J)
C
	DO 310 J=1,6
	 DO 310 M=1,6
 310	   TENSQ(M,J) = TENSM(M,1)*TENSP(1,J)+
     &                 TENSM(M,2)*TENSP(2,J)+
     &                 TENSM(M,3)*TENSP(3,J)+
     &                 TENSM(M,4)*TENSP(4,J)+
     &                 TENSM(M,5)*TENSP(5,J)+
     &                 TENSM(M,6)*TENSP(6,J)
C
   
	DO LLLL=1,6
C
        TENSQQ(1,1,LLLL)=TENSQ(1,LLLL) 
        TENSQQ(2,2,LLLL)=TENSQ(2,LLLL) 
        TENSQQ(3,3,LLLL)=TENSQ(3,LLLL) 
        TENSQQ(1,2,LLLL)=TENSQ(4,LLLL) 
        TENSQQ(2,1,LLLL)=TENSQ(4,LLLL) 
        TENSQQ(1,3,LLLL)=TENSQ(5,LLLL) 
        TENSQQ(3,1,LLLL)=TENSQ(5,LLLL) 
        TENSQQ(2,3,LLLL)=TENSQ(6,LLLL) 
        TENSQQ(3,2,LLLL)=TENSQ(6,LLLL) 
C
	END DO
C
C        IF (LHAMADTEST ==1) print*,'Location-8a1 Subrt: UPDATE'
	DO 320 I=1,48
	 DO 320 J=1,6
C        IF (LHAMADTEST ==1) print*,'Location-8a2 Subrt: UPDATE',I,J
 320	   TENSR(J,I) = TENSB(I)*(PMAT(1,I,icrys)*TENSQ(1,J)+
     &                           PMAT(2,I,icrys)*TENSQ(2,J)+
     &                           PMAT(3,I,icrys)*TENSQ(3,J)+
     &                           PMAT(4,I,icrys)*TENSQ(4,J)+
     &                           PMAT(5,I,icrys)*TENSQ(5,J)+
     &                           PMAT(6,I,icrys)*TENSQ(6,J))
C
c        IF (LHAMADTEST ==1) print*,'Location-8a3 Subrt: UPDATE'

C   9) Evaluate TENSS
C
        TMPS6(1,1) = UTTAU(1,1)*FST(1,1) +
     &                UTTAU(1,2)*FST(2,1) +
     &                UTTAU(1,3)*FST(3,1)
      TMPS6(1,2) = UTTAU(1,1)*FST(1,2) +
     &                UTTAU(1,2)*FST(2,2) +
     &                UTTAU(1,3)*FST(3,2)
      TMPS6(1,3) = UTTAU(1,1)*FST(1,3) +
     &                UTTAU(1,2)*FST(2,3) +
     &                UTTAU(1,3)*FST(3,3)
      TMPS6(2,1) = UTTAU(2,1)*FST(1,1) +
     &                UTTAU(2,2)*FST(2,1) +
     &                UTTAU(2,3)*FST(3,1)
      TMPS6(2,2) = UTTAU(2,1)*FST(1,2) +
     &                UTTAU(2,2)*FST(2,2) +
     &                UTTAU(2,3)*FST(3,2)
      TMPS6(2,3) = UTTAU(2,1)*FST(1,3) +
     &                UTTAU(2,2)*FST(2,3) +
     &                UTTAU(2,3)*FST(3,3)
      TMPS6(3,1) = UTTAU(3,1)*FST(1,1) +
     &                UTTAU(3,2)*FST(2,1) +
     &                UTTAU(3,3)*FST(3,1)
      TMPS6(3,2) = UTTAU(3,1)*FST(1,2) +
     &                UTTAU(3,2)*FST(2,2) +
     &                UTTAU(3,3)*FST(3,2)
      TMPS6(3,3) = UTTAU(3,1)*FST(1,3) +
     &                UTTAU(3,2)*FST(2,3) +
     &                UTTAU(3,3)*FST(3,3)

c        IF (LHAMADTEST ==1) print*,'Location-8a4 Subrt: UPDATE'

        TMPS7(1,1) = RTTAU(1,1)*TMPS6(1,1) +
     &                RTTAU(1,2)*TMPS6(2,1) +
     &                RTTAU(1,3)*TMPS6(3,1)
      TMPS7(1,2) = RTTAU(1,1)*TMPS6(1,2) +
     &                RTTAU(1,2)*TMPS6(2,2) +
     &                RTTAU(1,3)*TMPS6(3,2)
      TMPS7(1,3) = RTTAU(1,1)*TMPS6(1,3) +
     &                RTTAU(1,2)*TMPS6(2,3) +
     &                RTTAU(1,3)*TMPS6(3,3)
      TMPS7(2,1) = RTTAU(2,1)*TMPS6(1,1) +
     &                RTTAU(2,2)*TMPS6(2,1) +
     &                RTTAU(2,3)*TMPS6(3,1)
      TMPS7(2,2) = RTTAU(2,1)*TMPS6(1,2) +
     &                RTTAU(2,2)*TMPS6(2,2) +
     &                RTTAU(2,3)*TMPS6(3,2)
      TMPS7(2,3) = RTTAU(2,1)*TMPS6(1,3) +
     &                RTTAU(2,2)*TMPS6(2,3) +
     &                RTTAU(2,3)*TMPS6(3,3)
      TMPS7(3,1) = RTTAU(3,1)*TMPS6(1,1) +
     &                RTTAU(3,2)*TMPS6(2,1) +
     &                RTTAU(3,3)*TMPS6(3,1)
      TMPS7(3,2) = RTTAU(3,1)*TMPS6(1,2) +
     &                RTTAU(3,2)*TMPS6(2,2) +
     &                RTTAU(3,3)*TMPS6(3,2)
      TMPS7(3,3) = RTTAU(3,1)*TMPS6(1,3) +
     &                RTTAU(3,2)*TMPS6(2,3) +
     &                RTTAU(3,3)*TMPS6(3,3)
C
c        IF (LHAMADTEST ==1) print*,'Location-8b Subrt: UPDATE'

C
	DO 330 L=1,6
C
           TMPS1(1,1,L) = TENSPP(1,1,L)*FST(1,1) +
     &                TENSPP(1,2,L)*FST(2,1) +
     &                TENSPP(1,3,L)*FST(3,1)
      TMPS1(1,2,L) = TENSPP(1,1,L)*FST(1,2) +
     &                TENSPP(1,2,L)*FST(2,2) +
     &                TENSPP(1,3,L)*FST(3,2)
      TMPS1(1,3,L) = TENSPP(1,1,L)*FST(1,3) +
     &                TENSPP(1,2,L)*FST(2,3) +
     &                TENSPP(1,3,L)*FST(3,3)
      TMPS1(2,1,L) = TENSPP(2,1,L)*FST(1,1) +
     &                TENSPP(2,2,L)*FST(2,1) +
     &                TENSPP(2,3,L)*FST(3,1)
      TMPS1(2,2,L) = TENSPP(2,1,L)*FST(1,2) +
     &                TENSPP(2,2,L)*FST(2,2) +
     &                TENSPP(2,3,L)*FST(3,2)
      TMPS1(2,3,L) = TENSPP(2,1,L)*FST(1,3) +
     &                TENSPP(2,2,L)*FST(2,3) +
     &                TENSPP(2,3,L)*FST(3,3)
      TMPS1(3,1,L) = TENSPP(3,1,L)*FST(1,1) +
     &                TENSPP(3,2,L)*FST(2,1) +
     &                TENSPP(3,3,L)*FST(3,1)
      TMPS1(3,2,L) = TENSPP(3,1,L)*FST(1,2) +
     &                TENSPP(3,2,L)*FST(2,2) +
     &                TENSPP(3,3,L)*FST(3,2)
      TMPS1(3,3,L) = TENSPP(3,1,L)*FST(1,3) +
     &                TENSPP(3,2,L)*FST(2,3) +
     &                TENSPP(3,3,L)*FST(3,3)

c        IF (LHAMADTEST ==1) print*,'Location-8c Subrt: UPDATE'
C
           TMPS2(1,1,L) = RTTAU(1,1)*TMPS1(1,1,L) +
     &                RTTAU(1,2)*TMPS1(2,1,L) +
     &                RTTAU(1,3)*TMPS1(3,1,L)
      TMPS2(1,2,L) = RTTAU(1,1)*TMPS1(1,2,L) +
     &                RTTAU(1,2)*TMPS1(2,2,L) +
     &                RTTAU(1,3)*TMPS1(3,2,L)
      TMPS2(1,3,L) = RTTAU(1,1)*TMPS1(1,3,L) +
     &                RTTAU(1,2)*TMPS1(2,3,L) +
     &                RTTAU(1,3)*TMPS1(3,3,L)
      TMPS2(2,1,L) = RTTAU(2,1)*TMPS1(1,1,L) +
     &                RTTAU(2,2)*TMPS1(2,1,L) +
     &                RTTAU(2,3)*TMPS1(3,1,L)
      TMPS2(2,2,L) = RTTAU(2,1)*TMPS1(1,2,L) +
     &                RTTAU(2,2)*TMPS1(2,2,L) +
     &                RTTAU(2,3)*TMPS1(3,2,L)
      TMPS2(2,3,L) = RTTAU(2,1)*TMPS1(1,3,L) +
     &                RTTAU(2,2)*TMPS1(2,3,L) +
     &                RTTAU(2,3)*TMPS1(3,3,L)
      TMPS2(3,1,L) = RTTAU(3,1)*TMPS1(1,1,L) +
     &                RTTAU(3,2)*TMPS1(2,1,L) +
     &                RTTAU(3,3)*TMPS1(3,1,L)
      TMPS2(3,2,L) = RTTAU(3,1)*TMPS1(1,2,L) +
     &                RTTAU(3,2)*TMPS1(2,2,L) +
     &                RTTAU(3,3)*TMPS1(3,2,L)
      TMPS2(3,3,L) = RTTAU(3,1)*TMPS1(1,3,L) +
     &                RTTAU(3,2)*TMPS1(2,3,L) +
     &                RTTAU(3,3)*TMPS1(3,3,L)

        IF (LHAMADTEST ==1) print*,'Location-9 Subrt: UPDATE'

C
           TMPS5(1,1,L) = TMPS2(1,1,L)*LPBDT(1,1) +
     &                TMPS2(1,2,L)*LPBDT(2,1) +
     &                TMPS2(1,3,L)*LPBDT(3,1)
      TMPS5(1,2,L) = TMPS2(1,1,L)*LPBDT(1,2) +
     &                TMPS2(1,2,L)*LPBDT(2,2) +
     &                TMPS2(1,3,L)*LPBDT(3,2)
      TMPS5(1,3,L) = TMPS2(1,1,L)*LPBDT(1,3) +
     &                TMPS2(1,2,L)*LPBDT(2,3) +
     &                TMPS2(1,3,L)*LPBDT(3,3)
      TMPS5(2,1,L) = TMPS2(2,1,L)*LPBDT(1,1) +
     &                TMPS2(2,2,L)*LPBDT(2,1) +
     &                TMPS2(2,3,L)*LPBDT(3,1)
      TMPS5(2,2,L) = TMPS2(2,1,L)*LPBDT(1,2) +
     &                TMPS2(2,2,L)*LPBDT(2,2) +
     &                TMPS2(2,3,L)*LPBDT(3,2)
      TMPS5(2,3,L) = TMPS2(2,1,L)*LPBDT(1,3) +
     &                TMPS2(2,2,L)*LPBDT(2,3) +
     &                TMPS2(2,3,L)*LPBDT(3,3)
      TMPS5(3,1,L) = TMPS2(3,1,L)*LPBDT(1,1) +
     &                TMPS2(3,2,L)*LPBDT(2,1) +
     &                TMPS2(3,3,L)*LPBDT(3,1)
      TMPS5(3,2,L) = TMPS2(3,1,L)*LPBDT(1,2) +
     &                TMPS2(3,2,L)*LPBDT(2,2) +
     &                TMPS2(3,3,L)*LPBDT(3,2)
      TMPS5(3,3,L) = TMPS2(3,1,L)*LPBDT(1,3) +
     &                TMPS2(3,2,L)*LPBDT(2,3) +
     &                TMPS2(3,3,L)*LPBDT(3,3)


C
 330	CONTINUE
C
	DO 340 L=1,6
	DO 340 J=1,3
	DO 340 M=1,3
         TMPS8(M,J,L) = 0.0D0 
         DO 340 KK=1,48  
 340	 TMPS8(M,J,L) = TMPS8(M,J,L)+SMATG(M,J,KK,icrys)*TENSR(L,KK)
C
	DO 350 L=1,6
C
         TMPS9(1,1,L) = TMPS7(1,1)*TMPS8(1,1,L) +
     &                TMPS7(1,2)*TMPS8(2,1,L) +
     &                TMPS7(1,3)*TMPS8(3,1,L)
      TMPS9(1,2,L) = TMPS7(1,1)*TMPS8(1,2,L) +
     &                TMPS7(1,2)*TMPS8(2,2,L) +
     &                TMPS7(1,3)*TMPS8(3,2,L)
      TMPS9(1,3,L) = TMPS7(1,1)*TMPS8(1,3,L) +
     &                TMPS7(1,2)*TMPS8(2,3,L) +
     &                TMPS7(1,3)*TMPS8(3,3,L)
      TMPS9(2,1,L) = TMPS7(2,1)*TMPS8(1,1,L) +
     &                TMPS7(2,2)*TMPS8(2,1,L) +
     &                TMPS7(2,3)*TMPS8(3,1,L)
      TMPS9(2,2,L) = TMPS7(2,1)*TMPS8(1,2,L) +
     &                TMPS7(2,2)*TMPS8(2,2,L) +
     &                TMPS7(2,3)*TMPS8(3,2,L)
      TMPS9(2,3,L) = TMPS7(2,1)*TMPS8(1,3,L) +
     &                TMPS7(2,2)*TMPS8(2,3,L) +
     &                TMPS7(2,3)*TMPS8(3,3,L)
      TMPS9(3,1,L) = TMPS7(3,1)*TMPS8(1,1,L) +
     &                TMPS7(3,2)*TMPS8(2,1,L) +
     &                TMPS7(3,3)*TMPS8(3,1,L)
      TMPS9(3,2,L) = TMPS7(3,1)*TMPS8(1,2,L) +
     &                TMPS7(3,2)*TMPS8(2,2,L) +
     &                TMPS7(3,3)*TMPS8(3,2,L)
      TMPS9(3,3,L) = TMPS7(3,1)*TMPS8(1,3,L) +
     &                TMPS7(3,2)*TMPS8(2,3,L) +
     &                TMPS7(3,3)*TMPS8(3,3,L)


C
 350	CONTINUE
C
	DO 360 L=1,6
	 DO 360 J=1,3
	  DO 360 M=1,3
 360      TENSS(M,J,L) = TMPS2(M,J,L)-TMPS5(M,J,L)-TMPS9(M,J,L)
C
C   10) Evaluate TENSW
C
	CALL MAT3INV(FSTAU,FSINV)
C
        IF (LHAMADTEST ==1) print*,'Location-10 Subrt: UPDATE'

	DO 370 L=1,6
C
        TMPW2(1,1,L) = TENSS(1,1,L)*TMPW1(1,1) +
     &                TENSS(1,2,L)*TMPW1(2,1) +
     &                TENSS(1,3,L)*TMPW1(3,1)
      TMPW2(1,2,L) = TENSS(1,1,L)*TMPW1(1,2) +
     &                TENSS(1,2,L)*TMPW1(2,2) +
     &                TENSS(1,3,L)*TMPW1(3,2)
      TMPW2(1,3,L) = TENSS(1,1,L)*TMPW1(1,3) +
     &                TENSS(1,2,L)*TMPW1(2,3) +
     &                TENSS(1,3,L)*TMPW1(3,3)
      TMPW2(2,1,L) = TENSS(2,1,L)*TMPW1(1,1) +
     &                TENSS(2,2,L)*TMPW1(2,1) +
     &                TENSS(2,3,L)*TMPW1(3,1)
      TMPW2(2,2,L) = TENSS(2,1,L)*TMPW1(1,2) +
     &                TENSS(2,2,L)*TMPW1(2,2) +
     &                TENSS(2,3,L)*TMPW1(3,2)
      TMPW2(2,3,L) = TENSS(2,1,L)*TMPW1(1,3) +
     &                TENSS(2,2,L)*TMPW1(2,3) +
     &                TENSS(2,3,L)*TMPW1(3,3)
      TMPW2(3,1,L) = TENSS(3,1,L)*TMPW1(1,1) +
     &                TENSS(3,2,L)*TMPW1(2,1) +
     &                TENSS(3,3,L)*TMPW1(3,1)
      TMPW2(3,2,L) = TENSS(3,1,L)*TMPW1(1,2) +
     &                TENSS(3,2,L)*TMPW1(2,2) +
     &                TENSS(3,3,L)*TMPW1(3,2)
      TMPW2(3,3,L) = TENSS(3,1,L)*TMPW1(1,3) +
     &                TENSS(3,2,L)*TMPW1(2,3) +
     &                TENSS(3,3,L)*TMPW1(3,3)


C
        TMPW3(1,1,L) = TENSQQ(1,1,L)*FSTAU(1,1) +
     &                TENSQQ(1,2,L)*FSTAU(1,2) +
     &                TENSQQ(1,3,L)*FSTAU(1,3)
      TMPW3(1,2,L) = TENSQQ(1,1,L)*FSTAU(2,1) +
     &                TENSQQ(1,2,L)*FSTAU(2,2) +
     &                TENSQQ(1,3,L)*FSTAU(2,3)
      TMPW3(1,3,L) = TENSQQ(1,1,L)*FSTAU(3,1) +
     &                TENSQQ(1,2,L)*FSTAU(3,2) +
     &                TENSQQ(1,3,L)*FSTAU(3,3)
      TMPW3(2,1,L) = TENSQQ(2,1,L)*FSTAU(1,1) +
     &                TENSQQ(2,2,L)*FSTAU(1,2) +
     &                TENSQQ(2,3,L)*FSTAU(1,3)
      TMPW3(2,2,L) = TENSQQ(2,1,L)*FSTAU(2,1) +
     &                TENSQQ(2,2,L)*FSTAU(2,2) +
     &                TENSQQ(2,3,L)*FSTAU(2,3)
      TMPW3(2,3,L) = TENSQQ(2,1,L)*FSTAU(3,1) +
     &                TENSQQ(2,2,L)*FSTAU(3,2) +
     &                TENSQQ(2,3,L)*FSTAU(3,3)
      TMPW3(3,1,L) = TENSQQ(3,1,L)*FSTAU(1,1) +
     &                TENSQQ(3,2,L)*FSTAU(1,2) +
     &                TENSQQ(3,3,L)*FSTAU(1,3)
      TMPW3(3,2,L) = TENSQQ(3,1,L)*FSTAU(2,1) +
     &                TENSQQ(3,2,L)*FSTAU(2,2) +
     &                TENSQQ(3,3,L)*FSTAU(2,3)
      TMPW3(3,3,L) = TENSQQ(3,1,L)*FSTAU(3,1) +
     &                TENSQQ(3,2,L)*FSTAU(3,2) +
     &                TENSQQ(3,3,L)*FSTAU(3,3)


C
        TMPW4(1,1,L) = FSTAU(1,1)*TMPW3(1,1,L) +
     &                FSTAU(1,2)*TMPW3(2,1,L) +
     &                FSTAU(1,3)*TMPW3(3,1,L)
      TMPW4(1,2,L) = FSTAU(1,1)*TMPW3(1,2,L) +
     &                FSTAU(1,2)*TMPW3(2,2,L) +
     &                FSTAU(1,3)*TMPW3(3,2,L)
      TMPW4(1,3,L) = FSTAU(1,1)*TMPW3(1,3,L) +
     &                FSTAU(1,2)*TMPW3(2,3,L) +
     &                FSTAU(1,3)*TMPW3(3,3,L)
      TMPW4(2,1,L) = FSTAU(2,1)*TMPW3(1,1,L) +
     &                FSTAU(2,2)*TMPW3(2,1,L) +
     &                FSTAU(2,3)*TMPW3(3,1,L)
      TMPW4(2,2,L) = FSTAU(2,1)*TMPW3(1,2,L) +
     &                FSTAU(2,2)*TMPW3(2,2,L) +
     &                FSTAU(2,3)*TMPW3(3,2,L)
      TMPW4(2,3,L) = FSTAU(2,1)*TMPW3(1,3,L) +
     &                FSTAU(2,2)*TMPW3(2,3,L) +
     &                FSTAU(2,3)*TMPW3(3,3,L)
      TMPW4(3,1,L) = FSTAU(3,1)*TMPW3(1,1,L) +
     &                FSTAU(3,2)*TMPW3(2,1,L) +
     &                FSTAU(3,3)*TMPW3(3,1,L)
      TMPW4(3,2,L) = FSTAU(3,1)*TMPW3(1,2,L) +
     &                FSTAU(3,2)*TMPW3(2,2,L) +
     &                FSTAU(3,3)*TMPW3(3,2,L)
      TMPW4(3,3,L) = FSTAU(3,1)*TMPW3(1,3,L) +
     &                FSTAU(3,2)*TMPW3(2,3,L) +
     &                FSTAU(3,3)*TMPW3(3,3,L)


C
	 TMPW5(L) = TENSS(1,1,L)*FSINV(1,1)+
     &             TENSS(2,2,L)*FSINV(2,2)+
     &             TENSS(3,3,L)*FSINV(3,3)+
     &             TENSS(1,2,L)*FSINV(1,2)+
     &             TENSS(2,1,L)*FSINV(2,1)+
     &             TENSS(1,3,L)*FSINV(1,3)+
     &             TENSS(3,1,L)*FSINV(3,1)+
     &             TENSS(2,3,L)*FSINV(2,3)+
     &             TENSS(3,2,L)*FSINV(3,2)
C
 370	CONTINUE
C
	DO 380 L=1,6
	 DO 380 J=1,3
	  DO 380 M=1,3
 380	    TENSW(M,J,L) = DETINV*(TMPW2(M,J,L)+TMPW2(J,M,L)+
     &                    TMPW4(M,J,L))+TTAU(M,J)*TMPW5(L)
C
C	STORE JACOBIAN FOR THE CRYSTAL
C
	DO 390 L=1,6
C
	  DTDD(1,L) = TENSW (1,1,L)
	  DTDD(2,L) = TENSW (2,2,L)
	  DTDD(3,L) = TENSW (3,3,L)
	  DTDD(4,L) = 0.50D0*(TENSW (1,2,L) + TENSW (2,1,L))
	  DTDD(5,L) = 0.50D0*(TENSW (1,3,L) + TENSW (3,1,L))
	  DTDD(6,L) = 0.50D0*(TENSW (2,3,L) + TENSW (3,2,L))
C
 390 	CONTINUE
C
C=================== END JACOBIAN ========================
C
 400  CONTINUE
	IF (LHAMADTEST ==1) print*,'End of Subrt: UPDATE'
C
      RETURN
      END
C((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC     
C  UEXTERNALDB subroutine: to manage user-defined external databases and calculate model-independent history information
C  ACCESSED: LOP=0   BEGINNING OF THE ANALYSIS 
C            LOP=1,2 BEGINNING AND END OF EACH INCREMENT
C            LOP=3   END OF THE ANALYSIS
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC     
      SUBROUTINE UEXTERNALDB(LOP,LRESTART,TIME,DTIME,KSTEP,KINC,STRAN)
C     ----------------------------------------------------------------
      IMPLICIT NONE
      INTEGER                        :: LOP, LRESTART,KSTEP,KINC,J 
      REAL*8                         :: DTIME
      REAL*8                         :: STRAN
      REAL*8, DIMENSION(2)           :: TIME
C     ----------------------------------------------------------------
C
C     AT THE END OF EACH INCREMENT, PRINT TO THE SCREEN AND INITIALIZE JFLAG
      IF (LOP .EQ. 2) THEN
          Write(*,147)'[inc,   dtime,  time  ]:',KINC,  dtime,  TIME(2)
C          WRITE(201,*) (STRAN(J),J=1,NTENS)
      ENDIF
C
147   FORMAT(A40,1I4,2f9.4)    
C     ----------------------------------------------------------------
      IF(LOP.EQ.0)THEN
!          OPEN Checking files
           OPEN(UNIT=201,FILE='/nv/hp22/dpatel73/CPFEM/Classical
     .Check_Unit201.txt',
     .STATUS ='REPLACE')
           OPEN(UNIT=202,FILE='/nv/hp22/dpatel73/CPFEM/Classical
     .Check_Unit202.txt',
     .STATUS ='REPLACE')
           OPEN(UNIT=203,FILE='/nv/hp22/dpatel73/CPFEM/Classical
     .Check_Unit203.txt',
     .STATUS ='REPLACE')
           OPEN(UNIT=204,FILE='/nv/hp22/dpatel73/CPFEM/Classical
     .Check_Unit204.txt',
     .STATUS ='REPLACE')
           OPEN(UNIT=205,FILE='/nv/hp22/dpatel73/CPFEM/Classical
     .Check_Unit205.txt',
     .STATUS ='REPLACE')
      ENDIF
C    CLOSE CHECKING FILES AT THE END OF ANALYSIS
      IF (LOP .EQ. 3) THEN
         CLOSE(201)
         CLOSE(202)
         CLOSE(203)
         CLOSE(204)
         CLOSE(205)
      ENDIF
C     ----------------------------------------------------------------
      RETURN
      END


