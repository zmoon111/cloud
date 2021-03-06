import sys
import os
import errno
import recordio
import paddle.v2.dataset as ds

import logging
import logging.config

dict_config={ 
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': { 
        'default': { 
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': { 
        '': { 
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
    } 
}

logging.config.dictConfig(dict_config)
logger = logging.getLogger('convert')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def convert(output_path, name):
    logger.info("proc " + name)
    mod = __import__("paddle.v2.dataset." + name, fromlist=[''])

    path = os.path.join(output_path, name)
    mkdir_p(path)

    mod.convert(path)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        logger.error("input format:python convert.py output_path")
        sys.exit(1)

    output_path=sys.argv[1]
    logger.info("output path:" + output_path)

    a = ['cifar', 'conll05', 'imdb', 'imikolov', 'mnist', 'movielens', 'sentiment', 'uci_housing', 'wmt14']
    for m in a:
        convert(output_path, m)
