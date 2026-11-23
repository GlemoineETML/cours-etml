# -*- coding: utf-8 -*-
"""Source unique des résultats numériques du cours triphasé (présentation, fiche, corrigé, vérification)."""
import math
r3 = math.sqrt(3)
U, UPH, F = 400.0, 400 / math.sqrt(3), 50.0
W = 2 * math.pi * F
RHO = 0.0175                     # cuivre, Ω·mm²/m


def fr(x, nd=2):
    return f"{x:,.{nd}f}".replace(",", " ").replace(".", ",")


R = {}
# --- exemple guidé (diapo 5) : moteur 2,8 kW, Y, cos 0,85
R["g_I"] = 2800 / (r3 * U * 0.85)
R["g_Q"] = r3 * U * R["g_I"] * math.sin(math.acos(0.85))
# --- question de départ : borne 11 kW vs prise 16 A
R["borne_I11"] = 11000 / (r3 * U)
R["borne_I22"] = 22000 / (r3 * U)
R["prise_P"] = 230 * 16
# --- N°1 plaque moteur 4 kW 230Δ/400Y cos 0,82 η 0,86
R["m_Pabs"] = 4000 / 0.86
R["m_I"] = R["m_Pabs"] / (r3 * U * 0.82)
R["m_S"] = r3 * U * R["m_I"]
R["m_Q"] = R["m_S"] * math.sin(math.acos(0.82))
R["m_Iph_D230"] = R["m_I"] * r3          # courant ligne si réseau 3×230 V en Δ (plaque 14,2 A)
R["m_I_D230"] = R["m_Pabs"] / (r3 * 230 * 0.82)
# --- N°2 tensions
R["t_U"] = 232 * r3
R["t_Uph"] = 386 / r3
# --- N°3 borne VE
R["ve_I11"] = R["borne_I11"]; R["ve_I22"] = R["borne_I22"]
R["ve_Pmono"] = 230 * 16
R["ve_E"] = 60 * 0.6
R["ve_tmono"] = R["ve_E"] / (R["ve_Pmono"] / 1000)
R["ve_ttri"] = R["ve_E"] / 11
# --- N°4 chauffe-eau 9 kW Δ, dépannage
R["c_I"] = 9000 / (r3 * U)
R["c_Iph"] = R["c_I"] / r3
R["c_R"] = U ** 2 / 3000
R["c_Rmes"] = 2 * R["c_R"] / 3
R["c_Rdef"] = 2 * R["c_R"]
R["c_Pdef"] = 2 * U ** 2 / R["c_R"]
# --- N°5 charges monophasées (2300 / 1380 / 920 W sous 230 V)
I5 = [2300 / 230, 1380 / 230, 920 / 230]
R["n_I"] = I5
R["n_IN"] = math.sqrt(sum(i * i for i in I5) - (I5[0] * I5[1] + I5[0] * I5[2] + I5[1] * I5[2]))
z = sum(i * complex(math.cos(math.radians(a)), math.sin(math.radians(a))) for i, a in zip(I5, (90, -30, 210)))
assert abs(abs(z) - R["n_IN"]) < 1e-9
R["n_P"] = 2300 + 1380 + 920
# --- N°6 neutre coupé : radiateur 2000 W (L1), lampe 100 W (L2)
Ra, Rb = 230 ** 2 / 2000, 230 ** 2 / 100
R["nc_Ra"], R["nc_Rb"] = Ra, Rb
R["nc_I"] = U / (Ra + Rb)
R["nc_Ua"], R["nc_Ub"] = Ra * R["nc_I"], Rb * R["nc_I"]
# --- diapo neutre (exemple du fascicule) : plaque 800 W, radiateur 3000 W
Rp, Rr = 230 ** 2 / 800, 230 ** 2 / 3000
Ie = U / (Rp + Rr)
R["ex_Up"], R["ex_Ur"] = Rp * Ie, Rr * Ie
# --- N°7 chauffe-eau Δ 120 Ω, fusible fondu ; même R en Y
R["f_PD"] = 3 * U ** 2 / 120
R["f_PDcut"] = U ** 2 / 120 + U ** 2 / 240
R["f_PY"] = U ** 2 / 120
R["f_PYcut"] = U ** 2 / 240
R["f_ID"] = r3 * U / 120
R["f_IDcut"] = U / 120 + U / 240
# --- N°8 compensation menuiserie 48 kW cos 0,72 → 0,95
P8, c1, c2 = 48000, 0.72, 0.95
R["k_I1"] = P8 / (r3 * U * c1)
R["k_t1"], R["k_t2"] = math.tan(math.acos(c1)), math.tan(math.acos(c2))
R["k_QL"] = P8 * R["k_t1"]; R["k_Q2"] = P8 * R["k_t2"]
R["k_QC"] = R["k_QL"] - R["k_Q2"]
R["k_QC1"] = R["k_QC"] / 3
R["k_C"] = R["k_QC1"] / (U ** 2 * W)
R["k_I2"] = P8 / (r3 * U * c2)
# --- N°9 chute de tension : pompe 7,5 kW, η 0,88, cos 0,85, 60 m, 4 mm²
R["d_Rc"] = RHO * 60 / 4
R["d_P1"] = 7500 / 0.88
R["d_I"] = R["d_P1"] / (r3 * U * 0.85)
R["d_dU"] = r3 * R["d_Rc"] * R["d_I"]
R["d_pc"] = R["d_dU"] / U * 100
R["d_Pl"] = 3 * R["d_Rc"] * R["d_I"] ** 2
R["d_U1"] = U + R["d_dU"]
# --- N°10 mélange : four 3 × 40 Ω
R["x_IY"] = UPH / 40; R["x_PY"] = 3 * UPH ** 2 / 40
R["x_Iph"] = U / 40; R["x_ID"] = r3 * U / 40; R["x_PD"] = 3 * U ** 2 / 40
# --- ticket de sortie
R["tk_Iph"] = 17.3 / r3

if __name__ == "__main__":
    for k, v in R.items():
        print(f"{k:12s}", [round(x, 3) for x in v] if isinstance(v, list) else round(v, 4))
