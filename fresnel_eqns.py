# <filename>.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: <date>

# <description>

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import numpy as np
import matplotlib.pyplot as plt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

pi = np.pi

csv_save_path = 'T:/Device Components/Grating Coupler/20250228_gc_study'
csv_file_name = 'bigStack_350LN_hmm'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def rte(th1_deg, th2_deg, n1, n2):
    # reflection coeff, TE
    
    th1_rad = pi/180 * th1_deg
    th2_rad = pi/180 * th2_deg
    
    rte_top = n1 * np.cos(th1_rad) - n2 * np.cos(th2_rad)
    rte_bot = n1 * np.cos(th1_rad) + n2 * np.cos(th2_rad)
    
    return rte_top / rte_bot

def rtm(th1_deg, th2_deg, n1, n2):
    # reflection coeff, TM
    
    th1_rad = pi/180 * th1_deg
    th2_rad = pi/180 * th2_deg
    
    rtm_top = n1 * np.sec(th1_rad) - n2 * np.sec(th2_rad)
    rtm_bot = n1 * np.sec(th1_rad) + n2 * np.sec(th2_rad)
    
    return rtm_top / rtm_bot


def tte(th1_deg, th2_deg, n1, n2):
    # transmission coeff, TE
    
    th1_rad = pi/180 * th1_deg
    th2_rad = pi/180 * th2_deg
    
    return 1 + rte(th1_deg, th2_rad, n1, n2)

def ttm(th1_deg, th2_deg, n1, n2):
    # transmission coeff, TM
    
    th1_rad = pi/180 * th1_deg
    th2_rad = pi/180 * th2_deg
    
    return (1 + rtm(th1_rad, th2_rad, n1, n2)) * np.cos(th1_rad) / np.cos(th2_rad)


def switch_ms(M_in):
    # the same conversion applies going S to M
    
    a = M_in[0][0]
    b = M_in[0][1]
    c = M_in[1][0]
    d = M_in[1][1]
    
    t12 = a - b*c/d
    r21 = b/d
    r12 = -c/d
    t21 = 1/d
    
    S = np.array([[t12, r21], [r12, t21]])
    return S

def switch_ms_svl(svl_in):
    # the same conversion applies going S to M
    
    svl_out = 0j + np.zeros(np.shape(svl_in))
    
    a = svl_in[:, 1]
    b = svl_in[:, 2]
    c = svl_in[:, 3]
    d = svl_in[:, 4]
    
    t12 = a - b*c/d
    r21 = b/d
    r12 = -c/d
    t21 = 1/d
    
    svl_out[:, 0] = svl_in[:, 0]
    svl_out[:, 1] = t12
    svl_out[:, 2] = r21
    svl_out[:, 3] = r12
    svl_out[:, 4] = t21
    
    return svl_out


def m_prop(d, wl0, n, th_deg = 0):
    # propagation of a wave with
    # free space wavelength wl0
    # propagation angle th_deg
    # thru homogenous medium of
    # thickness d
    # index n
    
    th_rad = pi/180 * th_deg
    phi = n * 2*pi/wl0 * d * np.cos(th_rad)
    
    M = np.array([
        [np.exp(-1j * phi), 0],
        [0, np.exp(1j * phi)]
    ])
    
    return M


def m_sb(th1_deg, th2_deg, n1, n2, pol):
    # single boundary
    
    th1_rad = pi/180 * th1_deg
    th2_rad = pi/180 * th2_deg
    
    if pol.lower() == 'te':
        n_bar_1 = n1 * np.cos(th1_rad)
        n_bar_2 = n2 * np.cos(th2_rad)
        a21 = 1
    elif pol.lower() == 'tm':
        n_bar_1 = n1 * np.sec(th1_rad)
        n_bar_2 = n2 * np.sec(th2_rad)
        a21 = np.cos(th1_rad) / np.cos(th2_rad)
    
    M = 1/(2 * a21 * n_bar_2) * np.array([
        [n_bar_1 + n_bar_2, n_bar_2 - n_bar_1],
        [n_bar_2 - n_bar_1, n_bar_1 + n_bar_2]
    ])
    
    return M

def airy_3lyr(s0, s2, wl_array, d1, n1, th1_deg, pol):
    
    th1_rad = pi/180 * th1_deg
    
    if pol.lower() == 'te':
        n_bar_1 = n1 * np.cos(th1_rad)
    elif pol.lower() == 'tm':
        n_bar_1 = n1 * np.sec(th1_rad)
    
    phi_arr = n1 * 2*pi/wl_array * d1 * np.cos(th1_rad)
    
    t13_up = s0[0][0] * s2[0][0] * np.exp(-1j * phi_arr)
    t13_dn = (1 - s0[0][1] * s2[1][0] * np.exp(-2j * phi_arr))
    
    r13_up = s0[0][0] * s2[0][0] * s2[1][0] * np.exp(-2j * phi_arr)
    r13_dn = t13_dn
    
    r31_up = s0[0][1] * s2[0][0]
    r31_dn = s2[1][1] * (1 - s0[0][1] * s2[1][0] * np.exp(-2j * phi_arr))
    
    t31_up = r31_dn
    t31_dn = s0[1][1] * np.exp(1j * phi_arr)
    
    
    s_out = np.array([
        wl_array,
        t13_up/t13_dn,
        s2[0][1] + r31_up/r31_dn,
        s0[1][0] + r13_up/r13_dn,
        t31_up/t31_dn
    ])
    
    return s_out.T

def plot_s_vs_lam(svl_mat, use_freq = False, use_db = True):
    
    if use_freq:
        columne = 299792458/svl_mat[:,0]
        svl_mat[:,0] = columne
        # svl_mat = np.array([columne, svl_mat[:,1:]]).T
    
    if use_db:
        fig,ax = plt.subplots(4,1)
        ax[0].plot(
            svl_mat[:,0],
            10*np.log10(1 - np.abs(svl_mat[:,2])**2),
        )
        ax[1].plot(
            svl_mat[:,0],
            10*np.log10(np.abs(svl_mat[:,2])**2),
        )
        ax[0].set_title("power transmitted (dB)")
        ax[1].set_title("power reflected (dB)")
    else:
        ax[0].plot(
            svl_mat[:,0],
            1 - np.abs(svl_mat[:,2])**2,
            svl_mat[:,0],
            np.abs(svl_mat[:,2])**2,
        )
        ax[0].set_title("power (mag^2)")
        ax[0].legend(['t13', 'r13'])
    
    ax[-2].plot(svl_mat[:,0], np.real(svl_mat[:,(1,3)]))
    ax[-2].legend(['t13', 'r13'])
    ax[-2].set_title("real")
    
    ax[-1].plot(svl_mat[:,0], np.imag(svl_mat[:,(1,3)]))
    ax[-1].legend(['t13', 'r13'])
    ax[-1].set_title("imaginary")



class layer:
    def __init__(self, n, theta_deg, h = None):
        self.n = n
        self.h = h
        self.theta_deg = theta_deg
    
    def prop_m(self, wl):
        mp = m_prop(
            d = self.h,
            wl0 = wl,
            n = self.n,
            th_deg = self.theta_deg
        )
        
        self.prop_mat = mp
        return mp
    
    def bound_in_m(self, layer2, pol):
        return m_sb(
            th1_deg = layer2.theta_deg,
            th2_deg = self.theta_deg,
            n1 = layer2.n,
            n2 = self.n,
            pol = pol
        )
    
    def bound_out_m(self, layer2, pol):
        return m_sb(
            th1_deg = self.theta_deg,
            th2_deg = layer2.theta_deg,
            n1 = self.n,
            n2 = layer2.n,
            pol = pol
        )

def stack_m(list_prop_order: list|tuple, wl, pol):
    # creates S transfer matrix for a list of layer objects, ordered entry-to-exit,
    # this assumes that the first layer and final layer are infinite in length,
    # and does not account for the boundaries of those layers.
    
    if isinstance(wl, float|int):
        wl = (wl,)
    
    M_arr = 0j + np.zeros((len(wl), 5))
    
    for nn in range(1, len(list_prop_order)):
        lpo0 = list_prop_order[nn-1]
        lpo1 = list_prop_order[nn]
        list_prop_order[nn].theta_deg = 180/pi * np.arcsin(
            lpo0.n/lpo1.n * np.sin(lpo0.theta_deg * pi/180)
        )
        
    for wl_n in range(len(wl)):
        
        M_overall = list_prop_order[-1].bound_in_m(list_prop_order[-2], pol)
        
        if len(list_prop_order) > 2:
            for layer_num in range(2, len(list_prop_order)):
                M_prop = list_prop_order[-layer_num].prop_m(wl = wl[wl_n])
                M_bound = list_prop_order[-layer_num].bound_in_m(
                    layer2 = list_prop_order[-layer_num - 1],
                    pol = pol
                )
                M_overall = np.matmul(M_overall, M_prop)
                M_overall = np.matmul(M_overall, M_bound)
                
        M_arr[wl_n][:] = np.array([
            wl[wl_n], 
            M_overall[0][0], # A
            M_overall[0][1], # B
            M_overall[1][0], # C
            M_overall[1][1], # D
        ])
    
    return M_arr

# yem = stack_m([ln, box, si], wl = wl_arr, pol = 'te')


def svl_to_csv(
        svl_mat,
        csv_file_path,
        use_db = True,
        euler_fmt = True,
        csv_header_str = '',
    ):
    
    if not(csv_file_path[-4:] == '.csv'):
        csv_file_path += '.csv'
    
    svl_mat_2 = np.zeros((np.shape(svl_mat)[0], np.shape(svl_mat)[1] * 2 - 1))
    
    if euler_fmt:
        svl_mat_2[:,0] = svl_mat[:,0] # wavelength/freq column
        
        svl_mat_2[:,1] = np.abs(svl_mat[:,1])
        svl_mat_2[:,2] = np.angle(svl_mat[:,1]) * 180/pi
    
        svl_mat_2[:,3] = np.abs(svl_mat[:,2])
        svl_mat_2[:,4] = np.angle(svl_mat[:,2]) * 180/pi
    
        svl_mat_2[:,5] = np.abs(svl_mat[:,3])
        svl_mat_2[:,6] = np.angle(svl_mat[:,3]) * 180/pi
    
        svl_mat_2[:,7] = np.abs(svl_mat[:,4])
        svl_mat_2[:,8] = np.angle(svl_mat[:,4]) * 180/pi
        
        if use_db:
            svl_mat_2[:,(1,3,5,7)] = 20 * np.log10(svl_mat_2[:,(1,3,5,7)])
    
    else:
        svl_mat_2[:,0] = svl_mat[:,0] # wavelength/freq column
        
        svl_mat_2[:,1] = np.real(svl_mat[:,1])
        svl_mat_2[:,2] = np.imag(svl_mat[:,1])
    
        svl_mat_2[:,3] = np.real(svl_mat[:,2])
        svl_mat_2[:,4] = np.imag(svl_mat[:,2])
    
        svl_mat_2[:,5] = np.real(svl_mat[:,3])
        svl_mat_2[:,6] = np.imag(svl_mat[:,3])
    
        svl_mat_2[:,7] = np.real(svl_mat[:,4])
        svl_mat_2[:,8] = np.imag(svl_mat[:,4])
    
    np.savetxt(
        fname = csv_file_path,
        X = svl_mat_2,
        delimiter = ',',
        header = csv_header_str
    )
    
    print(f"\nsaved to:\n{csv_file_path}\n")



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    wl_global = 1.55E-6
    
    wl_arr = np.linspace(1.0, 2.0, 251) * 1e-6
    
    fiber_hmm = layer(
        n = 1.446,
        h = 10E-6,
        theta_deg = 8
    )
    
    air = layer(
        n = 1.0,
        h = 10E-6,
        theta_deg = 11.60973197
        # theta_deg = 8
    )
    
    clad = layer(
        n = 1.444,
        h = 1.4E-6,
        theta_deg = 8.011153057
        # theta_deg = 5.53077
    )
    
    grating_maybe = layer(
        n = 1.734547757,
        h = 0.20E-6,
        theta_deg = 6.6348
        # theta_deg = 5.396271382
        # theta_deg = 3.72898
    )
    
    ln = layer(
        n = 2.139906,
        h = 0.15E-6,
        theta_deg = 5.396271382
        # theta_deg = 3.72898
    )
    
    box = layer(
        n = 1.440,
        h = 10E-6,
        theta_deg = 8.033553035
        # theta_deg = 5.54618
    )
    
    si = layer(
        n = 3.48129,
        # h = 10E-6,
        theta_deg = 3.313967184
        # theta_deg = 2.29115
    )
    
    yem = stack_m([ln, box, si], wl = wl_global, pol = 'te')
    
    m_lower = np.matmul(box.bound_out_m(si, pol = "te"), box.prop_m(wl = wl_global))
    m_total = np.matmul(m_lower, box.bound_in_m(ln, pol = "te"))
    
    s_total = switch_ms(m_total)
    
    np.set_printoptions(suppress=True)
    print(f"s_total =\n{s_total}")
    print(f"s_magnitudes =\n{np.abs(s_total)}")
    print(f"s_phases =\n{180 / pi * np.angle(s_total)}")
    
    print(f"\nm_total =\n{m_total}")
    print(f"m_magnitudes =\n{np.abs(m_total)}")
    print(f"m_phases =\n{180 / pi * np.angle(m_total)}")
    
    
    # s_sb_ln_box = switch_ms(m_sb_ln_box)
    # s_sb_si_box = switch_ms(m_sb_si_box)
    # s_prop_box = switch_ms(m_prop_box)
    # s_sb_box_ln = switch_ms(m_sb_box_ln)
    # s_sb_box_si = switch_ms(m_sb_box_si)
    
    ln_box_si = airy_3lyr(
        s0 = switch_ms(box.bound_in_m(ln, pol = "te")),
        # s2 = s_sb_box_ln,
        s2 = switch_ms(box.bound_out_m(si, pol = "te")),
        wl_array = wl_arr,
        d1 = box.h,
        n1 = box.n,
        # th1_deg = 60,
        th1_deg = box.theta_deg,
        pol = 'te'
    )
    
    clad_ln_box = airy_3lyr(
        s0 = switch_ms(ln.bound_in_m(clad, pol = "te")),
        # s2 = s_sb_box_ln,
        s2 = switch_ms(ln.bound_out_m(box, pol = "te")),
        wl_array = wl_arr,
        d1 = ln.h,
        n1 = ln.n,
        # th1_deg = 60,
        th1_deg = ln.theta_deg,
        pol = 'te'
    )
    
    air_clad_ln = airy_3lyr(
        s0 = switch_ms(clad.bound_in_m(air, pol = "te")),
        # s2 = s_sb_ln_clad,
        s2 = switch_ms(clad.bound_out_m(ln, pol = "te")),
        wl_array = wl_arr,
        d1 = clad.h,
        n1 = clad.n,
        # th1_deg = 60,
        th1_deg = clad.theta_deg,
        pol = 'te'
    )
    
    big_stack = switch_ms_svl(stack_m(
        [fiber_hmm, air, clad, grating_maybe, ln, box, si],
        wl = wl_arr,
        pol = 'te'
    ))
    
    # test_sandwich = airy_3lyr(
    #     s0 = s_sb_box_si,
    #     s2 = s_sb_si_box,
    #     wl_array = wl_arr,
    #     d1 = h_box,
    #     n1 = n_si,
    #     th1_deg = 0,
    #     pol = 'te'
    # )
    
    # plt.plot(wl_arr, np.real(ln_box_si))
    # plt.plot(wl_arr, np.imag(ln_box_si))
    # plt.plot(wl_arr, np.abs(ln_box_si))
    
    if True:
        plt.close('all')
    
    use_freq_all = False
    
    plot_s_vs_lam(ln_box_si, use_freq=use_freq_all)
    plot_s_vs_lam(clad_ln_box, use_freq=use_freq_all)
    plot_s_vs_lam(air_clad_ln, use_freq=use_freq_all)
    plot_s_vs_lam(big_stack, use_freq=use_freq_all)
    
    
    csv_header_str = "wL," +\
        "t12_mag (db), t12_angle," +\
        "r21_mag (db), r21_angle," +\
        "r12_mag (db), r12_angle," +\
        "t21_mag (db), t21_angle"
    
    if True:
        svl_to_csv(
            svl_mat = big_stack,
            csv_file_path = csv_save_path + '/' + csv_file_name,
            csv_header_str = csv_header_str
        )
    
    # deebski = 10 * np.log10(np.abs(ln_box_si))
    # phaseski = np.angle(ln_box_si)
    
    # fig,ax = plt.subplots(2,1)
    # ax[0].plot(wl_arr, np.abs(ln_box_si))
    # ax[1].plot(wl_arr, phaseski)
    # ax[0].set_title("magnitude")
    # ax[1].set_title("phase")

    # fig2,ax2 = plt.subplots(2,1)
    # ax2[0].plot(wl_arr, np.real(ln_box_si))
    # ax2[1].plot(wl_arr, np.imag(ln_box_si))
    # ax2[0].set_title("real")
    # ax2[1].set_title("imag")
    
#end if __name__ == "__main__"
