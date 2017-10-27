

def set_lock(file):
    """
    """
    lf_path='/tmp/habitat.lock'
    lf_flags=os.O_WRONLY|os.O_CREAT
    lf_mode=stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
    umask_original=os.umask(0)
    try:
            lf_fd=os.open(lf_path,lf_flags,lf_mode)
    except IOError as er:
            print('IO Error:{0} attempting to open lock file'.format(er.strerror))
    finally:
            os.umask(umask_original)

    try:
            fcntl.lockf(lf_fd,fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError as er:
            print('IO Error:{0} attempting to lock file'.format(er.strerror))
