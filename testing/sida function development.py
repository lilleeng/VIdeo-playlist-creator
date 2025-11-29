# Make a function 'sia' or 'sida', say-input-assign or say-input-do-assign
# that allows for easy edit and making of main program logic/flow.
# Encapsulate all functionality in the program in functions and call them
# from the 'sia'/'sida' function.

# funksjon signatur
# funksjon(say, var_names*, *, verify_func=None, do_func, ooo )
# 'ooo' = 'order of operation'

# funksjon (
#	"...
#	...
#	...", 
#	var_name_1, var_name_2, ...,	
#	verify=...)

# say, input, verify input, assign, do?, order of operation?


mem = {}
def datadir_input(say, verify):
    print(say)
    t = input()
    while (not verify(t)):  # verify = os.path.isdir
        t = input()
    mem['datadir'] = t

def playlist_form_choice(say, verify):
    print(say)
    t = input()
    while (not verify(t)):  # verify = lambda x: x in ['1', '2']
        t = input()
    mem['PLAYLIST_FORM_CHOICE'] = t

def video_output_dir(say, verify):
    print(say)
    t = input()
    while (not verify(t)):  # verify = os.path.isdir
        t = input()
    mem['video_output_dir'] = t

def enter_to_proceed(say, verify):
    print(say)
    t = input()
    while (not verify(t)):  # verify = None
        t = input()
    mem['video_output_dir'] = t

def sia(say='',*, verify=None, var_name='UNUSED VARIABLE'):   # say-input-assign
    print(say)
    t = input()
    if (verify != None):
        while (not verify(t)):
            t = input()
        mem[var_name]

sia("Album folder directory:\n"
    "- ", 
    verify=os.path.isdir, 
    var_name='DATA DIRECTORY')
sia("Choose an option\n" \
    "1: Single long video\n" \
    "2: Multiple videos\n"
    "- ", 
    verify=lambda x: x in ['1', '2'], 
    var_name='PLAYLIST FORM CHOICE')
sia("Video playlist output path:\n" \
    "- ", 
    verify=os.path.isdir, 
    var_name='VIDEO OUTPUT DIRECTORY')