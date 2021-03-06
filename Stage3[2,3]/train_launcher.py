"""
TRAIN LAUNCHER 

"""
import os
import configparser
from hourglass_tiny import HourglassModel
from datagen import DataGenerator

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
'''
os.environ['KMP_DUPLICATE_LIB_OK']='True'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
'''


def process_config(conf_file):
    """
    """
    params = {}
    config = configparser.ConfigParser()
    config.read(conf_file, encoding='utf-8')
    for section in config.sections():
        if section == 'DataSetHG':
            for option in config.options(section):
                params[option] = eval(config.get(section, option))
        if section == 'Network':
            for option in config.options(section):
                params[option] = eval(config.get(section, option))
        if section == 'Train':
            for option in config.options(section):
                params[option] = eval(config.get(section, option))
        if section == 'Validation':
            for option in config.options(section):
                params[option] = eval(config.get(section, option))
        if section == 'Saver':
            for option in config.options(section):
                params[option] = eval(config.get(section, option))
    return params


if __name__ == '__main__':
    print('--Parsing Config File')
    params = process_config('config.cfg')

    print('--Creating Dataset')
    dataset = DataGenerator(params['joint_list'], params['img_directory'], params['training_txt_file'],
                            remove_joints=params['remove_joints'])
    dataset._create_train_table()
    dataset._randomize()
    dataset._create_sets()
    model = HourglassModel(nFeat=params['nfeats'], nStack=params['nstacks'], nModules=params['nmodules'],
                           nLow=params['nlow'], outputDim=params['num_joints'], batch_size=params['batch_size'],
                           attention=params['mcam'], training=True, drop_rate=params['dropout_rate'],
                           lear_rate=params['learning_rate'], decay=params['learning_rate_decay'],
                           decay_step=params['decay_step'], dataset=dataset,
                           name=params['name'], logdir_train=params['log_dir_train'],
                           logdir_test=params['log_dir_test'], tiny=params['tiny'], w_loss=params['weighted_loss'],
                           joints=params['joint_list'], modif=False)
    model.generate_model()
    model.training_init(nEpochs=params['nepochs'], epochSize=params['epoch_size'], saveStep=params['saver_step'],
                        dataset=None)

# tensorboard --logdir=F:\zwx\test\All
