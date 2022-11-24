# Note: segmented documents must have filename "segmented_docs.txt"

import os

dir = os.path.dirname(os.path.realpath(__file__))
cmd_filename = 'commands.sh'
output_dir = 'output_files/'

for local_folder in os.listdir(output_dir):

    local_path = output_dir + local_folder

    # copy commands.sh into local folder
    os.chdir(dir)
    os.system('cp ' + cmd_filename + ' ' + local_path + '/' + cmd_filename)

    # run commands from local folder
    os.chdir(local_path)
    os.system('bash ' + cmd_filename)

    # delete commands from local folder
    os.remove(cmd_filename)
    os.chdir(dir)