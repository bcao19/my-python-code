;
; Create_Kinetic_H_Mesh.pro
;
pro Create_Kinetic_H_Mesh,nv,mu,x,Ti,Te,n,PipeDia,xH,TiH,TeH,neH,PipeDiaH,vx,vr,Tnorm,E0=E0,ixE0=ixE0,irE0=irE0,fctr=fctr
                                ; JH=JH,Use_Collrad_Ionization=Use_Collrad_Ionization

;add these lines to improve velocity space resolution (use with care):
  nV=20
  ;E0=[.1]

   ; FS: extra flags for ionization coefficients:
   ;key_default,JH,0
   ;key_default,Use_Collrad_Ionization,1 ; true by default

  ; FS: fix choice of ionization coefficients here:
  JH=0
  Use_Collrad_Ionization=1


  mH=1.6726231e-27		
  q=1.602177e-19				
  key_default,fctr,1.0
  nx=n_elements(x)
;
;  Estimate interaction rate with side walls
;
   gamma_wall=dblarr(nx)
;   for k=0,nx-1 do begin
;      if PipeDia(k) gt 0 then gamma_wall(k)=2*sqrt(2*Ti(k)*q/(2*mH))/PipeDia(k)
;   endfor
;
;  Estimate total reaction rate for destruction of hydrogen atoms and for interation with side walls
;
;   RR=n*sigmav_ion_H0(Te)+gamma_wall
   RR=n*sigmav_ion_H0(Te)
;
; Set v0 to thermal speed of 10 eV neutral
;
  v0=sqrt(2*10*q/(mu*mH))
;
; Determine x range for atoms by finding distance into plasma where density persists.
;
;  dGamma/dx=-nH*RR = v0 dnH/dx = -nH*RR
;  d ln(nH)/dx = -RR/v0 = dY/dx
;
;  Compute Y from RR and v0
;
   Y=dblarr(nx)
   for k=1,nx-1 do Y(k)=Y(k-1)-(x(k)-x(k-1))*0.5*(RR(k)+RR(k-1))/v0
;
; Find x location where Y = -5, i.e., where nH should be down by exp(-5)
;
   xmaxH=interpol(x,Y,-5.0) < max(x)
   xminH=x(0)
;
; Interpolate Ti and Te onto a fine mesh between xminH and xmaxH
;
   xfine=xminH+(xmaxH-xminH)*findgen(1001)/1000
   Tifine=interpol(Ti,x,xfine)
   Tefine=interpol(Te,x,xfine)
   nfine=interpol(n,x,xfine)
   PipeDiafine=interpol(PipeDia,x,xfine)
;
; Setup a vx,vr mesh based on raw data to get typical vx, vr values
;
   Create_VrVxMesh,nv,Tifine,vx,vr,Tnorm,E0=E0,ixE0=ixE0,irE0=irE0
   Vth=sqrt(2*q*Tnorm/(mu*mH))
   minVr=vth*min(vr)
   minE0=0.5*mH*minVr*minVr/q
;
;  Estimate interaction rate with side walls
;
   nxfine=n_elements(xfine)
   gamma_wall=dblarr(nxfine)
   for k=0,nxfine-1 do begin
      if PipeDiaFine(k) gt 0 then gamma_wall(k)=2*max(vr)*vth/PipeDiaFine(k)
   endfor
;
; Estimate total reaction rate, including charge exchange and elastic scattering, and interaction with side walls
;
   if Use_Collrad_Ionization then begin
      ioniz_rate=collrad_sigmav_ion_h0(nfine,Tefine) ; from COLLRAD code (DEGAS-2)
   endif else begin
      if JH then begin
         ioniz_rate=JHS_Coef(nfine,Tefine,/no_null) ; Johnson-Hinnov, limited Te range
      endif else begin
         ioniz_rate=sigmav_ion_h0(Tefine) ; from Janev et al., up to 20keV
      endelse
   endelse
   RR=nfine*ioniz_rate+nfine*sigmav_cx_H0(Tifine,replicate(minE0,n_elements(xfine))) +gamma_wall
;
; Compute local maximum grid spacing from dx_max = 2 min(vr) / RR
;
   big_dx=0.02*fctr
   dx_max=fctr*0.8*(2*vth*min(vr)/RR) < big_dx
;
; Construct xH axis 
;
   xpt=xmaxH
   xH=[xpt]
   while xpt gt xminH do begin
      xH=[xpt,xH]
      dxpt1=interpol(dx_max,xfine,xpt)
      dxpt2=dxpt1
      xpt_test=xpt-dxpt1
      if xpt_test gt xminH then dxpt2=interpol(dx_max,xfine,xpt_test)
      ;dxpt=min([dxpt1,dxpt2]) ; *0.5  ; FS: reduce spacing 
      ; FS: force a preset maximum grid spacing
      ;dxpt=max([min([dxpt1,dxpt2]),0.005]) ; FS
      ; force a preset maximum grid spacing
      dxh_max=0.0005     ; JWH: 0.0015 should be sufficient for D3D because scale lengths are 2.5x larger
      dxpt=min([dxpt1,dxpt2,dxh_max])
      xpt=xpt-dxpt
   endwhile
   xH=[xminH,xH(0:n_elements(xH)-2)]
;   if xH(1)-xH(0) > 0.5*big_dx then xH=[xH(0),xH(2:*)]

   TiH=interpol(Tifine,xfine,xH)
   TeH=interpol(Tefine,xfine,xH)
   neH=interpol(nfine,xfine,xH)
   PipeDiaH=interpol(PipeDiaFine,xfine,xH)
   Create_VrVxMesh,nv,TiH,vx,vr,Tnorm,E0=E0,ixE0=ixE0,irE0=irE0
   return
   end
