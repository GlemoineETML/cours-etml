# Recalcul indépendant — test 540 (régime impulsionnel RC / RL)
import math
from math import exp, log
print("=== Ex1 RC différentiateur ===")
U, tp, R, C = 15.0, 8e-3, 1.5e3, 2.2e-6
tau = R*C; print("tau", tau)
v0 = U; print("Vsor(0+)", v0)
t1 = 7.999e-3; v1 = U*exp(-t1/tau); print("Vsor(t1)", v1)
v2a = v1 - U; print("Vsor(t2) approx", v2a)
v2 = (U*exp(-tp/tau) - U)*exp(-(8.001e-3-tp)/tau); print("Vsor(t2) exact", v2)
dt = tau*log(abs(v2a)/0.2); print("dt", dt, "t3", tp+dt)
# simulation numérique indépendante (Euler) : uC' = (Ven-uC)/RC
dtn=1e-7; uc=0; t=0; tt=None; vmin=0
while t<40e-3:
    ven = U if t<tp else 0
    vs = ven-uc
    if t>tp and vs>-0.2 and tt is None: tt=t
    if t>t1-dtn/2 and abs(t-t1)<dtn/2: print("sim Vsor(t1)",vs)
    vmin=min(vmin,vs)
    uc += (ven-uc)/tau*dtn; t+=dtn
print("sim vmin", vmin, "sim t3", tt)
print("5tau",5*tau)
print("=== Ex2 RL ===")
U, tp, L, R = 20.0, 6e-3, 150e-3, 56.0
tau = L/R; I = U/R
print("tau",tau,"I",I)
i = I*(1-exp(-tp/tau)); print("i(tp)",i,"Vsor",R*i, "%", 1-exp(-tp/tau))
# simulation
dtn=1e-7; il=0; t=0
while t<tp-dtn/2: il += (U-R*il)/L*dtn; t+=dtn
print("sim i", il, "Vsor", R*il)
tau2 = tp/5; R2 = L/tau2; print("tau2",tau2,"R2",R2, "Vsor", U*(1-exp(-5)))
print("5tau a)",5*tau)
for Rn in (120,150):
    t5 = 5*L/Rn; print("E12",Rn,"tau",L/Rn,"5tau",t5,"Vsor(tp)",U*(1-exp(-tp*Rn/L)), "pct", 1-exp(-tp*Rn/L))
# valeurs arrondies comme l'élève
tau_r=2.679e-3; I_r=357.1e-3
print("eleve i", I_r*(1-exp(-6/2.679)), "Vsor", 56*I_r*(1-exp(-6/2.679)))
print("eleve dt", 3.3*log(13.67/0.2))
