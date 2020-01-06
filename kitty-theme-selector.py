import os
import subprocess

TEMP_CONF_SETTINGS = 'temp'
TEMP_CONF_LAUNCH = 'temp1'
MAIN_CONF = 'kitty.conf'

# If options is a tuple then it is an index, 
# if it is a string then it is the theme name
def replace_line(pathdest, options):
    pathdest += '/kitty.conf'
    # TODO: add try/catch
    with open(pathdest) as f:
        lines = f.readlines()

    for line in lines:
        if 'include' in line:
            lines.remove(line)

    # theme name    
    if isinstance(options, str):
        lines.append('include themes/' + options + '.conf\n')
        write_config(lines, TEMP_CONF_SETTINGS) # write lines to show preview
        append_temp_config()
        if confirm(options):
            write_config(lines, MAIN_CONF) # If confirmed then write to the actual config
    # index number
    elif isinstance(options, tuple):
        lines.append('include themes/' + (options[1][options[0]]) + '.conf\n')
        write_config(lines, TEMP_CONF_SETTINGS)
        append_temp_config()
        #print(options[1][options[0]])
        if confirm(options[1][options[0]]): # If confirmed then write to the actual config
            write_config(lines, MAIN_CONF)

    os.remove(TEMP_CONF_SETTINGS)
    os.remove(TEMP_CONF_LAUNCH)

def write_config(lines, filename):
    with open(filename, 'w') as f:
        f.writelines(lines)

def append_temp_config():
    #TODO: Check the behaviour in Linux
    lines = ['launch bash -c "neofetch;echo This is a preview, press a key to exit;read -n 1 -s -r -p "..." "']
    with open(TEMP_CONF_LAUNCH, 'w') as f:
        f.writelines(lines)

def get_option():
    print('Please select a theme:')
    themes = os.listdir('themes')
    show_options(themes)

    selection = input('Enter the name or number of the desired theme: ')
    selection = selection.replace(')', '')
    # Checking if selection is valid input
    try:
        selection = int(selection) 
        if selection > len(themes) or selection < 1:
            raise ValueError
    except ValueError:
        # Not an int so check if the string is valid
        if selection not in themes:
            print('Invalid Selection')
            print('Exiting...')
            exit(1)
        return selection

    return (selection - 1, themes) # -1 because index reference

# Takes in files as themes
def show_options(themes):
    #for theme in themes:
    for i in range(len(themes)):
        # Discard files that aren't configuration files
        if '.conf' not in themes[i]:
            continue
        themes[i] = themes[i].split('.')[0]
        print(str(i + 1) + ') ', end='')
        print(themes[i])

def confirm(option):
    #TODO: Check if on Linux it changes right away or if opening a new window is necessary
    # if not then just change it
    FNULL = open(os.devnull, 'w')
    terminal = subprocess.Popen(['kitty', '-c', TEMP_CONF_SETTINGS, '--session', TEMP_CONF_LAUNCH], \
            close_fds=True, stdout=FNULL, stderr=subprocess.STDOUT)
    #terminal = subprocess.Popen(['kitty', '-c', TEMP_CONF_SETTINGS, '--session', TEMP_CONF_LAUNCH])
    if input('Confirm color scheme: {} (Y/n)'.format(option)) is not 'Y':
        terminal.kill()
        return False

    terminal.kill()
    return True

def main():
    try:
        os.chdir(str(os.path.expanduser('~')) + '/.config/kitty') # Kitty directory
    except FileNotFoundError:
        print('No kitty configuration folder found at ~/.config/kitty')
        print('Exiting...')
        exit(1)
    path = os.getcwd()
    option = get_option()
    replace_line(path, option)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted')
        print('Exiting...')
        os.remove(TEMP_CONF_SETTINGS)
        os.remove(TEMP_CONF_LAUNCH)
        exit(1)
else:
    exit(1)