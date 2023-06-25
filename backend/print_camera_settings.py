import gphoto2 as gp


def list_config(camera):
    config = camera.get_config()
    for section in gp.check_result(gp.gp_widget_get_children(config)):
        print(f"Section: {gp.check_result(gp.gp_widget_get_name(section))}")
        for child in gp.check_result(gp.gp_widget_get_children(section)):
            print(
                f"Name: {gp.check_result(gp.gp_widget_get_name(child))}, "
                f"Type: {gp.check_result(gp.gp_widget_get_type(child))}, "
                f"Current Value: {gp.check_result(gp.gp_widget_get_value(child))}"
            )
            if gp.check_result(gp.gp_widget_get_type(child)) == gp.GP_WIDGET_RADIO:
                choices = [
                    gp.check_result(gp.gp_widget_get_choice(child, i))
                    for i in range(gp.check_result(gp.gp_widget_count_choices(child)))
                ]
                print(f"Choices: {choices}")
            print("\n")


def main():
    context = gp.Context()
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera, context))
    list_config(camera)
    gp.check_result(gp.gp_camera_exit(camera, context))


if __name__ == "__main__":
    main()
