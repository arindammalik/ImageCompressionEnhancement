#!/usr/bin/env python

import sys, os, os.path, getopt, time, shlex, subprocess, logging
from subprocess import CalledProcessError
#from optimiser.formats.png import OptimisePNG
from optimiser.formats.jpg import OptimiseJPG
#from optimiser.formats.gif import OptimiseGIF
#from optimiser.formats.animated_gif import OptimiseAnimatedGIF
from scratch import Scratch
##
from PIL import Image,ImageEnhance
from io import BytesIO
import requests
import time
##


# there should be an option to keep or strip meta data (e.g. exif data) from jpegs
def getImage(url,path):
    #response = requests.get(url)
    #picture = Image.open(BytesIO(response.content))
    picture = Image.open(os.getcwd()+"/Photos/"+'TestJS7i.jpeg')
    start_time = time.time()
    picture=getNewSizeImage(picture)
    enhanceImage(picture,path)

    picture=None
    args=[path]
    opts=[('-s', ''), ('-q', '')]
    beginSmushing(args,opts)
    #print(str(time.time()-start_time))
    
    return

def enhanceImage(picture,path):
    enhancer_object = ImageEnhance.Sharpness(picture)
    picture = enhancer_object.enhance(2.4)
    if picture.mode!="RGB" :
        picture=picture.convert('RGB')
    return

def getNewSizeImage(img):
    defW=990
    defH=512
    defRatio=defW/defH
    (w,h) = img.size
    ratio=float(w/h)
    (nw,nh) = img.size
    if ratio>defRatio:
        nh=(h/w)*defW
        nw=defW
    else:
        nh=defH
        nw=(w/h)*defH

    img = img.resize((int(nw), int(nh)), Image.ANTIALIAS)
    return img

class Smush():
    def __init__(self, **kwargs):
        self.optimisers = {
            #'PNG': OptimisePNG(**kwargs),
            'JPEG': OptimiseJPG(**kwargs),
            #'GIF': OptimiseGIF(**kwargs),
            #'GIFGIF': OptimiseAnimatedGIF(**kwargs)
        }

        self.__files_scanned = 0
        self.__start_time = time.time()
        self.exclude = {}
        for dir in kwargs.get('exclude'):
            if len(dir) == 0:
                continue
            self.exclude[dir] = True
        self.quiet = kwargs.get('quiet')
        self.identify_mime = kwargs.get('identify_mime')

        # setup tempfile for stdout and stderr
        self.stdout = Scratch()
        self.stderr = Scratch()

    def __del__(self):
        self.stdout.destruct()
        self.stderr.destruct()

    def __smush(self, file):
        """
        Optimises a file
        """
        key = self.__get_image_format(file)

        if key in self.optimisers:
            logging.info('optimising file %s' % (file))
            self.__files_scanned += 1
            self.optimisers[key].set_input(file)
            self.optimisers[key].optimise()


    def process(self, dir, recursive):
        """
        Iterates through the input directory optimising files
        """
        if recursive:
            self.__walk(dir, self.__smush)
        else:
            if os.path.isdir(dir):
                dir = os.path.abspath(dir)
                for file in os.listdir(dir):
                    if self.__checkExclude(file):
                        continue
                        
                    if self.identify_mime:
                        import mimetypes
                        (type,encoding) = mimetypes.guess_type(file)
                        if type and (type[:5] != "image"):
                            continue

                    self.__smush(os.path.join(dir, file))
            elif os.path.isfile(dir):
                self.__smush(dir)


    def __walk(self, dir, callback):
        """ Walks a directory, and executes a callback on each file """
        dir = os.path.abspath(dir)
        logging.info('walking %s' % (dir))
        for file in os.listdir(dir):
            if self.__checkExclude(file):
                continue
            
            if self.identify_mime:
                import mimetypes
                (type,encoding) = mimetypes.guess_type(file)        
                if type and (type[:5] != "image"):
                    continue

            nfile = os.path.join(dir, file)
            callback(nfile)
            if os.path.isdir(nfile):
                self.__walk(nfile, callback)


    def __get_image_format(self, input):
        """
        Returns the image format for a file.
        """
        test_command = 'identify -format %%m "%s"' % input
        args = shlex.split(test_command)

        try:
            retcode = subprocess.call(args, stdout=self.stdout.opened, stderr=self.stderr.opened)
            if retcode != 0:
                if self.quiet == False:
                    logging.warning(self.stderr.read().strip())
                return False

        except OSError:
            logging.error('Error executing command %s. Error was %s' % (test_command, OSError))
            sys.exit(1)
        except:
            # most likely no file matched
            if self.quiet == False:
                logging.warning('Cannot identify file.')
            return False

        return self.stdout.read().strip()[:6]


    def stats(self):
        output = []
        output.append('\n%d files scanned:' % (self.__files_scanned))
        arr = []

        for key, optimiser in self.optimisers.items():
            # divide optimiser.files_optimised by 2 for each optimiser since each optimised file
            # gets counted twice
            output.append('    %d %ss optimised out of %d scanned. Saved %dkb' % (
                    optimiser.files_optimised // 2,
                    key, 
                    optimiser.files_scanned, 
                    optimiser.bytes_saved / 1024))
            arr.extend(optimiser.array_optimised_file)

        if (len(arr) != 0):
            output.append('Modified files:')
            for filename in arr:
                output.append('    %s' % filename)
        output.append('Total time taken: %.2f seconds' % (time.time() - self.__start_time))
        return {'output': "\n".join(output), 'modified': arr}


    def __checkExclude(self, file):
        if file in self.exclude:
            logging.info('%s is excluded.' % (file))
            return True
        return False


def main():
    path=sys.argv[1]
    args=[path]
    opts=[('-s', '')]
    beginSmushing(args,opts)
    sys.exit(0)
    return

def beginSmushing(args,opts):
    
    if len(args) == 0:
        usage()
        sys.exit()
    recursive = False
    quiet = False
    strip_jpg_meta = False
    exclude = ['.bzr', '.git', '.hg', '.svn']
    list_only = False
    identify_mime = False

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-r', '--recursive'):
            recursive = True
        elif opt in ('-q', '--quiet'):
            quiet = True
        elif opt in ('-s', '--strip-meta'):
            strip_jpg_meta = True
        elif opt in ('--identify-mime'):
            identify_mime = True
        elif opt in ('--exclude'):
            exclude.extend(arg.strip().split(','))
        elif opt in ('--list-only'):
            list_only = True
            # quiet = True
        else:
            # unsupported option given
            usage()
            sys.exit(2)

    if quiet == True:
        logging.basicConfig(
            level=logging.WARNING,
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

    smush = Smush(strip_jpg_meta=strip_jpg_meta, exclude=exclude, list_only=list_only, quiet=quiet, identify_mime=identify_mime)
    
    for arg in args:
        try:
            smush.process(arg, recursive)
            logging.info('\nSmushing Finished')
        except KeyboardInterrupt:
            logging.info('\nSmushing aborted')

    result = smush.stats()
    if list_only and len(result['modified']) > 0:
        logging.error(result['output'])
        sys.exit(1)
    #print(result['output'])
    return    

def usage():
   print(" \n Options are any of: \n -h, --help         Display this help message and exit \n -r, --recursive    Recurse through given directories optimising images \n -q, --quiet        Don't display optimisation statistics at the end \n -s, --strip-meta   Strip all meta-data from JPEGs \n --exclude=EXCLUDES comma separated value for excluding files \n --identify-mime    Fast identify image files via mimetype \n --list-only        Perform a trial run with no changes made  ") 

   
if __name__ == '__main__':
    main()
