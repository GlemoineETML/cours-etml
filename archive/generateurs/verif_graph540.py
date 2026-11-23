# Contrôle indépendant des courbes du corrigé : simulation pas à pas des circuits
# (sans aucune formule exponentielle) comparée aux courbes tracées dans make_fig540.py
import numpy as np
def sim_rc(U, tp, R, C, tend, dt=1e-7):
    uc, out, t = 0.0, [], 0.0
    while t <= tend:
        ue = U if t < tp else 0.0
        out.append((t, ue - uc)); uc += (ue - uc)/(R*C)*dt; t += dt
    return np.array(out)
def sim_rl(U, tp, L, R, tend, dt=1e-7):
    i, out, t = 0.0, [], 0.0
    while t <= tend:
        ue = U if t < tp else 0.0
        out.append((t, R*i)); i += (ue - R*i)/L*dt; t += dt
    return np.array(out)
# ----- courbes TRACÉES (mêmes expressions que make_fig540.py), temps en ms
tau1 = 3.3; v1 = 15*np.exp(-7.999/tau1); v2 = v1 - 15
f1 = lambda t: np.where(t < 8, 15*np.exp(-t/tau1), v2*np.exp(-(t-8)/tau1))
tau2 = 150/56; vm = 20*(1-np.exp(-6/tau2))
f2 = lambda t: np.where(t < 6, 20*(1-np.exp(-t/tau2)), vm*np.exp(-(t-6)/tau2))
s1 = sim_rc(15, 8e-3, 1.5e3, 2.2e-6, 32e-3); s2 = sim_rl(20, 6e-3, 0.15, 56, 21e-3)
for nom, s, f, ex in (("N°1 RC", s1, f1, (7.999, 8.0)), ("N°2 RL", s2, f2, ())):
    t = s[::50, 0]*1e3; m = s[::50, 1]
    keep = np.all([np.abs(t-e) > 0.01 for e in ex], axis=0) if ex else np.ones_like(t, bool)
    err = np.max(np.abs(f(t[keep]) - m[keep]))
    print(f"{nom}: écart max courbe tracée / simulation = {err*1e3:.2f} mV")
def at(s, tms): return s[np.argmin(np.abs(s[:, 0]-tms*1e-3)), 1]
print("N°1 points : 0+ %.3f | τ %.3f | t1 %.4f | t2 %.3f | t2+τ %.3f" %
      (at(s1, 0.0001), at(s1, 3.3), at(s1, 7.999), at(s1, 8.001), at(s1, 11.3)))
i3 = np.argmax((s1[:, 0] > 8e-3) & (s1[:, 1] > -0.2)); print("N°1 t3 (−200 mV) = %.3f ms" % (s1[i3, 0]*1e3))
print("N°2 points : τ %.3f | 6 ms %.3f | 6+τ %.3f | 6+5τ %.3f" %
      (at(s2, tau2), at(s2, 6.0), at(s2, 6+tau2), at(s2, 6+5*tau2)))
print("N°2 continuité à 6 ms : avant %.3f / après %.3f" % (at(s2, 5.999), at(s2, 6.001)))
