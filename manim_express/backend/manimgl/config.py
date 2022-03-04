from enum import IntEnum
import manimlib.config
from manimlib.config import *
from manimlib.config import __config_file__


class Size(IntEnum):
    small = 1
    medium = 2
    big = 3
    bigger = 4
    biggest = 5


def get_new_configuration(args):
    global __config_file__

    # ensure __config_file__ always exists
    if args.config_file is not None:
        if not os.path.exists(args.config_file):
            log.error(f"Can't find {args.config_file}.")
            if sys.platform == 'win32':
                log.info(f"Copying default configuration file to {args.config_file}...")
                os.system(f"copy default_config.yml {args.config_file}")
            elif sys.platform in ["linux2", "darwin"]:
                log.info(f"Copying default configuration file to {args.config_file}...")
                os.system(f"cp default_config.yml {args.config_file}")
            else:
                log.info("Please create the configuration file manually.")
            log.info("Read configuration from default_config.yml.")
        else:
            __config_file__ = args.config_file

    global_defaults_file = os.path.join(get_manim_dir(), "manimlib", "default_config.yml")

    if not (os.path.exists(global_defaults_file) or os.path.exists(__config_file__)):
        log.info("There is no configuration file detected. Switch to the config file initializer:")
        init_customization()

    elif not os.path.exists(__config_file__):
        log.info(f"Using the default configuration file, which you can modify in `{global_defaults_file}`")
        log.info(
            "If you want to create a local configuration file, you can create a file named"
            f" `{__config_file__}`, or run `manimgl --config`"
        )

    custom_config = get_custom_config()
    check_temporary_storage(custom_config)

    write_file = any([args.write_file, args.open, args.finder])
    if args.transparent:
        file_ext = ".mov"
    elif args.gif:
        file_ext = ".gif"
    else:
        file_ext = ".mp4"

    file_writer_config = {
        "write_to_movie": not args.skip_animations and write_file,
        "break_into_partial_movies": custom_config["break_into_partial_movies"],
        "save_last_frame": args.skip_animations and write_file,
        "save_pngs": args.save_pngs,
        # If -t is passed in (for transparent), this will be RGBA
        "png_mode": "RGBA" if args.transparent else "RGB",
        "movie_file_extension": file_ext,
        "mirror_module_path": custom_config["directories"]["mirror_module_path"],
        "output_directory": args.video_dir or custom_config["directories"]["output"],
        "file_name": args.file_name,
        "input_file_path": args.file or "",
        "open_file_upon_completion": args.open,
        "show_file_location_upon_completion": args.finder,
        "quiet": args.quiet,
    }

    if args.embed is None:
        module = get_module(args.file)
    else:
        with insert_embed_line(args.file, int(args.embed)) as alt_file:
            module = get_module(alt_file)

    config = {
        "module": module,
        "scene_names": args.scene_names,
        "file_writer_config": file_writer_config,
        "quiet": args.quiet or args.write_all,
        "write_all": args.write_all,
        "skip_animations": args.skip_animations,
        "start_at_animation_number": args.start_at_animation_number,
        "end_at_animation_number": None,
        "preview": not write_file,
        "presenter_mode": args.presenter_mode,
        "leave_progress_bars": args.leave_progress_bars,
    }

    # Camera configuration
    config["camera_config"] = get_camera_configuration(args, custom_config)

    # Default to making window half the screen size
    # but make it full screen if -f is passed in
    monitors = get_monitors()
    mon_index = custom_config["window_monitor"]
    monitor = monitors[min(mon_index, len(monitors) - 1)]
    window_width = monitor.width
    if not (args.full_screen or custom_config["full_screen"]):
        try:
            if args.screen_size == Size.biggest:
                pass
            elif args.screen_size == Size.small:
                window_width //= 3
            elif args.screen_size == Size.medium:
                window_width //= 2
            elif args.screen_size == Size.big:
                window_width = int(window_width / 1.5)
            elif args.screen_size == Size.bigger:
                window_width = int(window_width / 1.25)
            else:
                raise ValueError('Invalid screen_size parameter.')
        except:
            window_width //= 2
    window_height = window_width * 9 // 16
    config["window_config"] = {
        "size": (window_width, window_height),
    }

    # Arguments related to skipping
    stan = config["start_at_animation_number"]
    if stan is not None:
        if "," in stan:
            start, end = stan.split(",")
            config["start_at_animation_number"] = int(start)
            config["end_at_animation_number"] = int(end)
        else:
            config["start_at_animation_number"] = int(stan)

    return config


# register to manimlib
manimlib.config.get_configuration = get_new_configuration
