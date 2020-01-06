import os
import subprocess

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
        lines.append('include themes/' + options + '.conf')
    # index number
    if isinstance(options, tuple):
        lines.append('include themes/' + options[1][options[0]] + '.conf')

    f = open('kitty.conf', 'w')
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
        # Not an int so check for name 
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
    pass

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
    confirm(option)

if __name__ == '__main__':
    main()
else:
    exit(1)