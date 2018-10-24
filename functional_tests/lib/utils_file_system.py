import logging
import os


def check_dir_exists_create_if_not(target_dir):

    if os.path.isdir(target_dir):
        cwd = os.getcwd()
        logging.info("Directory: %s already exists under current working dir:"
                     " %s", target_dir, cwd)
    else:
        logging.info("Trying to create new directory: %s ", target_dir)
        try:
            os.makedirs(target_dir)
        except OSError as e:
            logging.warning(str(e))

        if not os.path.isdir(target_dir):
            logging.warning("Directory still does not exist, giving up.")
            return False

    return True


def delete_all_files_within_directory(target_directory):

    logging.info("About to clear all files in specified directory, %s",
                 str(target_directory))
    if os.path.exists(target_directory):
        filelist = [f for f in
                    os.listdir(target_directory)]
        for f in filelist:
            logging.info("About to delete file: %s", f)
            os.remove(os.path.join(target_directory, f))
    else:
        logging.warning("Specified path does not exist")
