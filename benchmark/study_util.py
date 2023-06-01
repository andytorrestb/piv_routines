# from openpiv import tools
import tools

def save_results(results_path, x, y, u, v, path_to_dir, img_file, id):
    # Save results as a text file.
    results_txt = results_path + '/results_' + str(id) + '.txt'
    tools.save(results_txt, x, y, u, v)

    # Display results as a vector field and save image file.
    results_img = results_path + '/results_'+ str(id)+ '.png'
    fig, ax = tools.display_vector_field(
            filename = results_txt,
            on_img = True,
            image_name = path_to_dir + img_file,
            show_plot = False,
        )
    ax.set_title("PIV Results")
    fig.savefig(results_img)

    return