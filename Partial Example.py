
from functools import partial

#Define partials and set fixed parameters
mc = partial(OpticalCoupler_InverseTaper_2layer_angleDE, angle = 0,  radius = 150,
             Taper1_tip = 0.1, Taper1_top = 'None', Taper1_lenght = 60,
             Taper2_sec1_type = 'Exponential', Taper2_sec2_type = 'Exponential',
             Taper2_sec1_tip = 1.1, Taper2_sec1_top = 6,
             Taper2_sec1_overhang = 10, Taper2_sec1_length = 'None',
             Taper2_sec2_tip = 0.08, Taper2_sec2_length = 160,
             Taper2_sec2_overhang = 0,
             growth1=-5.5, growth2=-5.5, mask_width = 50,
             tolerance=0.005, iterations = 100,
             DE_angle = 0, DE_width = 'None',
             layer_taper1 = 2, layer_taper2 = 6, layer_mask = 21, layer_DE = 91)
gc = partial(Grating_general, width_grating=15, focus_distance=35,
             taper_length=500, straight_length=10, number_of_teeth=20, type='in',
             window_width=50, window_height=50, lda=1.55,
             sin_theta=np.sin(-np.pi * 8 / 180), evaluations=99, layer_grating=4)


#Use partial to simplify main script
ebeam_mark = partial(Marker_Square_vernier_2alignments, layer_align1=layer_Au1, layer_align2=layer_Au2, delta1=0.025, delta2=0.025,
                     layer_mask=25, layer_mark=5, width=8, linewidth=0.5, spacing=10, number=11,
                     length=250, length_v=20, square_length=10)


e1 = gc(cell, m7, period=grating_period[wl], fill_frac=grating_fill_frac[wl], layer_backreflector=layer_BR[wl], type='out')

e2 = mc(cell, m6, type='in', Taper1_tip = rtw)

ebeam_mark(cell=cell, position=(Bottom_left[0], Bottom_left[1]-500))

