#  note that this script wont independently do anything.
#  it contains the code bit that you need to add to the "main"
#  section of the file you want to save.

if __name__ == "__main__":
    # Import the technology here to load the correct Layers, CrossSections, etc.
    c = gf.Component("dp_iqm_die example")
    # ^ so that if the file is open in klayout, it will update in-place rather
    # than in a new tab

    component_ref = c << dp_iqm_die()
    c.add_ports(ports=component_ref.ports)
    c.show(show_ports=True)
    
    
    
    
    
    
    ## this is the part you need to copy
    did_string = __file__.split("hl_cad/")[1].split("/")[0]
    picture_name = c.name.replace(" ", "_")

    layers_to_remove = ("FILL_KEEPOUT", "LN1_KEEPOUT")
    remove_layer_list = []
    for ko_layer_name in layers_to_remove:
        try:
            layer_got = gf.get_layer(ko_layer_name)
        except ValueError:
            pass
        else:
            if layer_got in c.layers:
                remove_layer_list.append(layer_got)

    if len(remove_layer_list) > 0:
        c_new = c.remove_layers(layers=remove_layer_list)
    else:
        c_new = c

    figgy = c_new.plot_klayout(
        #  optional:
        #  show_ports = True,
    )
    save_dir = "/home/miles/Documents/tapeouts/tapeout_pictures/"
    full_fname = f"{save_dir}{did_string}_{picture_name}.png"
    #

    ####### quick small scaling #######
    output_scaling_factor = 2
    figure_original_size_inches = figgy.get_size_inches()
    figgy.set_size_inches(
        (
            figure_original_size_inches[0] * output_scaling_factor,
            figure_original_size_inches[1] * output_scaling_factor,
        )
    )
    figgy.savefig(fname=full_fname)
    print(f"\nsaved image as:\n{full_fname}\n")


    ####### unnecessary old scaling #######
    # output_scaling_factor = 1
    # screen_diagonal_inches = 27
    # screen_size_pixels = (3840, 2160)
    # screen_diagonal_pixels = (
    #                              screen_size_pixels[0] ** 2 + screen_size_pixels[1] ** 2
    #                          ) ** 0.5
    # figure_original_size_inches = figgy.get_size_inches()
    # figure_original_diagonal_inches = (
    #                                       figure_original_size_inches[0] ** 2 + figure_original_size_inches[1] ** 2
    #                                   ) ** 0.5
    # 
    # screen_dpi = screen_diagonal_pixels / screen_diagonal_inches
    # 
    # if figure_original_size_inches[0] > figure_original_size_inches[1]:
    #     horiz_inches_new = min(
    #         figure_original_size_inches[0] * \
    #         screen_diagonal_inches / figure_original_diagonal_inches,
    #         screen_size_pixels[0] / screen_dpi,
    #     )
    #     vert_inches_new = horiz_inches_new * (
    #         figure_original_size_inches[1] / figure_original_size_inches[0]
    #     )
    # else:
    #     vert_inches_new = min(
    #         figure_original_size_inches[1] * \
    #         screen_diagonal_inches / figure_original_diagonal_inches,
    #         screen_size_pixels[1] / screen_dpi,
    #     )
    #     horiz_inches_new = vert_inches_new * (
    #         figure_original_size_inches[0] / figure_original_size_inches[1]
    #     )
    # 
    # figgy.set_dpi(int(screen_dpi))
    # figgy.set_size_inches(
    #     (
    #         horiz_inches_new * output_scaling_factor,
    #         vert_inches_new * output_scaling_factor
    #     )
    # )
