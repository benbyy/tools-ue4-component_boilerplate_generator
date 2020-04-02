#!/usr/bin/python3

import sys
import getopt
import os

validOptions=[('h', 'help'), ('C', 'class='), ('c','cat='), ('n', 'name='), ('g','get'), ('s','set'), ('a','attach'),('r','root')]
UNREAL_HEADERS_PATH = 'E:/Games/EpicGames/UE_4.24/Engine/Source'

def search_files(directory='.', extension='.h', className=''):
    matches={'files':[], 'paths':{}, 'pathsTok':{}}
    extension = extension.lower()
    className=className
    print('\n\nSearching header files for '+ className + 'includes...\t\n')
    for dirpath, dirnames, files in os.walk(directory):
        #print('\t/\t'.join(dirnames))
        for name in files:
            if className in str(name) and (extension and name.lower().endswith(extension)):
                matches['files'].append(os.path.join(os.path.normpath(dirpath), name))
                #matches['pathsTok'].setdefault(str(name),[]).append(os.path.split(os.path.normpath(dirpath)))
                #matches['paths'][str(name)] = prevVal + [dirpath]
            elif className[1:] in str(name) and (extension and name.lower().endswith(extension)):
                p = os.path.join(dirpath, name)
                p = os.path.normpath(p)
                pSplit = os.path.split(p)
                p=''
                while 'Source' not in pSplit[-1] \
                    and 'Classes' not in pSplit[-1] \
                    and 'Public' not in pSplit[-1] \
                    and 'Private' not in pSplit[-1] \
                    and pSplit[0] and pSplit[-1]:
                    p= ''.join([str(pSplit[-1]),'/',str(p)])
                    pSplit = os.path.split(pSplit[0])
                matches['files'].append(p[:-1])
                
    return matches
    


def main(argv):
    compClassName = str('')
    varName = str('')
    categoryName = str('')
    getter = False
    setter = False
    attach = False
    root = False

    try:
        opts, args = getopt.getopt(argv, "hCcngsarz:", ["class=", "cat=", "name=", "get", "set", "attach", "root"])
    #print('\n'.join(args)+'\n\n')

        for opt, arg in opts:

            if opt in ("-h", "--help"):
                usage_str='Valid options:\n'
                for p in validOptions:
                    usage_str = usage_str + '\t'.join([str(p),'\n'])           
                print(usage_str)
                sys.exit()

            if opt in ("-C","--class"):
                compClassName = str(arg)

            elif opt in ("-c", "--cat"):
                categoryName = str(arg)
                
            elif opt in ("-n", "--name"):
                varName = str(arg)
                
            elif opt in ("-g", "--get"):
                getter = True

            elif opt in ("-s", "--set"):
                setter = True
                
            elif opt in ("-a", "--attach"):
                attach = True

            elif opt in ("-r", "--root"):
                root = True

        # in cpp file
        creation_str = str('Set'+varName+'('+'CreateDefaultSubobject<' +
                        compClassName + '>(TEXT(' + varName + '0)));')

        # in *.h file
        uprop_str = str('UPROPERTY(Category = '+categoryName +
                        ', EditAnywhere, meta = (AllowPrivateAccess = "true"))')
        comp_class_str = str(compClassName+'* '+varName+';')
        getter_str = str('FORCEINLINE ' + compClassName +
                        '* Get'+varName+'() const { return '+varName+'; }')
        setter_str = str('FORCEINLINE void Set'+varName+'(' + compClassName +
                        '* in_' + varName + ') { '+varName+' = in_' + varName + '; }')
        root_str = str('SetRootComponent(Get'+varName+'());')
        attach_str = str(
            'Get'+varName+'()->SetupAttachment(GetRootComponent());')
        space_str = str(
            '\n/*------INSERT COMPONENT INITIALIZATION HERE------*/\n')
        print("\n.H /////////////////////////////////////:")
        print(uprop_str)
        print("\t"+comp_class_str)
        if getter is True:
            print(getter_str)
        if setter is True:
            print(setter_str)

        print("\n.CPP /////////////////////////////////////")
        print(creation_str)
        print(space_str)
        if attach is True:
            print(attach_str)
        if root is True and attach is True:
            print(root_str)
        print('\n\n\n')
        print("Potential Header Files:")
        headers=search_files(UNREAL_HEADERS_PATH, '.h', compClassName)
        if len(headers['files'])>0:
            print(os.path.commonpath(headers['files']))
            for f in headers['files']:
                #print('p:\t', os.path.commonpath([UNREAL_HEADERS_PATH, p]))
                #print('p:\t', p)
                f=str(f).split('Classes')[-1]
                print('#include "' + f + '"\n')
        else:
            print("<No matches found>\n")

    except getopt.GetoptError:
        print('ERROR:\t'+str(getopt.GetoptError.args) +'\n')
        #print('ERROR:\tCould not parse arguments:\n')
        usage_str='\tValid options:\t'
        for p in validOptions:
                 usage_str = usage_str + ' '.join(['-', str(p),'\n'])           
        print(usage_str)        
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit(0)
