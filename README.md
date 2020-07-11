# vid-process-lib
Generic tools for video inference like EDVR / DeOldify / DAIN? 
TODO:
video segmenting based on dur and resolution

# tf-utils
GDrive-Based model checkpointing from within Google's Colab service.
By https://github.com/Zahlii/colab-tf-utils
Usage:
    !wget https://raw.githubusercontent.com/Zahlii/colab-utils/master/utils.py
    import utils
    import os
    import keras

    def compare(best, new):
    return best.losses['val_acc'] < new.losses['val_acc']

    def path(new):
    if new.losses['val_acc'] > 0.8:
        return 'VGG16_%s.h5' % new.losses['val_acc']

    callbacks = cb = [
        utils.GDriveCheckpointer(compare,path),
        keras.callbacks.TensorBoard(log_dir=os.path.join(utils.LOG_DIR,'VGG16'))
    ]

## Downloading a file from google drive
    from utils import GDriveSync
    downloader=GDriveSync()
    filename='VGG16_0.81.h5'
    drive_file_path=downloader.find_items(filename)[0]
    downloader.download_file_to_folder(drive_file_path,filename)


# colab checkpointing tools
TODO
12 hr reset
countdown timer thread with terminate callback
execute jobs as threads in queue with exception/kill handler
when countdown timer expires
- terminate job
- nullify queue
- save checkpoint ect. to drive
- reload/reset colab?
- auto login colab?
- check and continue from checkpoint, restarting timer

90min idle disconnect 
https://gist.github.com/svmihar/8e1db06407749e918f9a273370c8a3fd
https://medium.com/@shivamrawat_756/how-to-prevent-google-colab-from-disconnecting-717b88a128c0 see comments