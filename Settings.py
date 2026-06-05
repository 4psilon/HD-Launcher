import tkinter as tk
from tkinter import ttk
from tkinter import StringVar, IntVar, messagebox, filedialog
import os
import sys
import configparser
import subprocess

#-------------------------------------Preparing to run------------------------------

#ypsilon: this class will display tool tips when user hovers mouse on button
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind('<Enter>', self.show_tooltip)
        self.widget.bind('<Leave>', self.hide_tooltip)
        self.widget.bind('<Button-1>', self.hide_tooltip)
        self.widget.bind('<FocusOut>', self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip and self.tooltip.winfo_exists():
            return
        x, y, _, _ = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f'+{x}+{y}')
        
        label = ttk.Label(self.tooltip, text=self.text, background='#ffffe0', relief='solid', borderwidth=1)
        label.pack()
        
        self.tooltip.after(5000, self.hide_tooltip)

    def hide_tooltip(self, event=None):
        try:
            if self.tooltip:
                self.tooltip.destroy()
                self.tooltip = None
        except Exception as err_msg:
            messagebox.showwarning('ToolTip error!', err_msg)
            self.tooltip = None

#ypsilon: this function verifies that item_name (either folder or file + extension) exists in dir_name inside game directory
#         and returns empty str if succeed or error message otherwise
def check_if_exists(dir_name, item_name, item_ext):
    dir_path = os.path.join(program_dir, dir_name)
    new_name = item_name + item_ext
    try:
        if os.path.isfile(os.path.join(dir_path, new_name)) or os.path.isdir(os.path.join(dir_path, item_name)):
            return ''
    except FileNotFoundError:
        return f'Data for "{item_name}" was not found in "{dir_name}" directory!'
    except PermissionError:
        return f'Cannot access the "{dir_path}" directory! Make sure you run Settings.exe as administrator!'
    except OSError:
        return f'Unexpected error occurred while checking for "{new_name}" in the "{dir_name}" directory!'
    return f'"{item_name}" does not exist in "{dir_name}" directory! Please make sure all game data is present.'

#ypsilon: firstly check if this code is executed from application (not just .py script!)
if getattr(sys, 'frozen', False):
    program_dir = os.path.dirname(sys.executable)
else:
    messagebox.showwarning('Expected to run as executable!', 'Please use this mode only during tests...')
    program_dir = os.path.dirname(os.path.abspath(__file__))

#-------------------------------------Creating Interface------------------------------

root = tk.Tk()
root.title('RK 1.42 HD Game Settings (v2)')  #ypsilon: please change (v...) whenever you are releasing new version of launcher
mainframe = ttk.Frame(root, padding='6 6 24 24')
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#creating responsive layouts in mainframe
mainframe.grid_columnconfigure(1, weight=1)
mainframe.grid_columnconfigure(2, weight=1)
mainframe.grid_columnconfigure(3, weight=1)
mainframe.grid_columnconfigure(4, weight=1)

#-------------------------------------Style list------------------------------

#ypsilon: this style is kinda an artifact from different interface idea, but it still highlights the labels well so...
style = ttk.Style()
style.configure('Description.TLabel', background='#bec8dc')  #relief='groove', anchor='s')

#-------------------------------------Image------------------------------

logo = tk.PhotoImage(file='logo.png')
logo_label = ttk.Label(mainframe, image=logo)
logo_label.grid(column=1, row=1, columnspan=4, pady=5)

#-------------------------------------Creating small frames------------------------------

#  username_frame 
username_frame = ttk.LabelFrame(mainframe, text='Username', padding=5)
username_frame.grid(column=1, row=2, sticky=(tk.W, tk.E), padx=5, pady=2)
username_frame.grid_columnconfigure(1, weight=1)  #ypsilon: to make entry field fill the whole column

username = StringVar()
username_entry = ttk.Entry(username_frame, width=15, textvariable=username)
username_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), padx=5)

#  resolution_frame 
resolution_frame = ttk.LabelFrame(mainframe, text='Resolution', padding=5)
resolution_frame.grid(column=2, row=2, sticky=(tk.W, tk.E), padx=5, pady=2)
resolution_frame.grid_columnconfigure(1, weight=1)

resolution = StringVar()
resolution_combo = ttk.Combobox(resolution_frame, width=12, textvariable=resolution)
resolution_combo.grid(column=1, row=1, sticky=(tk.W, tk.E))
resolution_combo['values'] = ('1024x768', '1280x720', '1360x768', '1600x900', '1920x1080')

fullscreen = StringVar()
full_check = ttk.Checkbutton(resolution_frame, text='Fullscreen', variable=fullscreen, onvalue='1', offvalue='0')
full_check.grid(column=1, row=2, sticky=(tk.W, tk.E))

#  sound_frame 
sound_frame = ttk.LabelFrame(mainframe, text='Sound', padding=5)
sound_frame.grid(column=1, row=3, sticky=(tk.W, tk.E), padx=5, pady=2)
sound_frame.grid_columnconfigure(2, weight=1)

sound = IntVar()
sound_set = ttk.Label(sound_frame)
sound_set.grid(column=1, row=1, sticky=tk.W)

def update_lbl_sound(val):
    sound_set['text'] = str(int(float(val))) + '%'

s = tk.Scale(sound_frame, orient='horizontal', length=120, from_=0.0, to=100.0, variable=sound, command=update_lbl_sound, showvalue=0)
s.grid(column=2, row=1, columnspan=2, sticky=(tk.W, tk.E))
s.set(50)

#  music_frame 
music_frame = ttk.LabelFrame(mainframe, text='Music', padding=5)
music_frame.grid(column=2, row=3, sticky=(tk.W, tk.E), padx=5, pady=2)
music_frame.grid_columnconfigure(2, weight=1)

music = IntVar()
music_set = ttk.Label(music_frame)
music_set.grid(column=1, row=1, sticky=tk.W)

def update_lbl_music(val):
    music_set['text'] = str(int(float(val))) + '%'

m = tk.Scale(music_frame, orient='horizontal', length=120, from_=0.0, to=100.0, variable=music, command=update_lbl_music, showvalue=0)
m.grid(column=2, row=1, columnspan=2, sticky=(tk.W, tk.E))
m.set(50)

#  speech_frame 
speech_frame = ttk.LabelFrame(mainframe, text='Speech', padding=5)
speech_frame.grid(column=1, row=4, sticky=(tk.W, tk.E), padx=5, pady=2)
speech_frame.grid_columnconfigure(2, weight=1)

speech = IntVar()
speech_set = ttk.Label(speech_frame)
speech_set.grid(column=1, row=1, sticky=tk.W)

def update_lbl_speech(val):
    speech_set['text'] = str(int(float(val))) + '%'

sp = tk.Scale(speech_frame, orient='horizontal', length=120, from_=0.0, to=100.0, variable=speech, command=update_lbl_speech, showvalue=0)
sp.grid(column=2, row=1, columnspan=2, sticky=(tk.W, tk.E))
sp.set(50)

#  scrollspeed_frame 
scrollspeed_frame = ttk.LabelFrame(mainframe, text='Scroll Speed', padding=5)
scrollspeed_frame.grid(column=2, row=4, sticky=(tk.W, tk.E), padx=5, pady=2)
scrollspeed_frame.grid_columnconfigure(2, weight=1)

scroll = IntVar()
scroll_set = ttk.Label(scrollspeed_frame)
scroll_set.grid(column=1, row=1, sticky=tk.W)

def update_lbl_scroll(val):
    scroll_set['text'] = str(int(float(val))) + '%'

sc = tk.Scale(scrollspeed_frame, orient='horizontal', length=120, from_=0.0, to=100.0, variable=scroll, command=update_lbl_scroll, showvalue=0)
sc.grid(column=2, row=1, columnspan=2, sticky=(tk.W, tk.E))
sc.set(50)

#  singleplayer_frame 
singleplayer_frame = ttk.LabelFrame(mainframe, text='Singleplayer Map Settings', padding=5)
singleplayer_frame.grid(column=1, row=5, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=2)

ttk.Label(singleplayer_frame, text=f'  Preselected Map:', style='Description.TLabel').grid(column=1, row=2, sticky=(tk.W, tk.E))
ttk.Label(singleplayer_frame, text='  Tutorial button status:', style='Description.TLabel').grid(column=1, row=1, sticky=(tk.W, tk.E))

singlemapvalue_set = ttk.Label(singleplayer_frame)
singlemapvalue_set.grid(column=2, row=2, sticky=tk.W)

singlemap = IntVar()
singlemap.prev_value = -1
singlemap.config_text = ''
singlemap.button_text = ''
singlemap.button_option2 = 'Preselected Map'

def singlemap_changed():
    if singlemap.get() == 1:
        file_path = filedialog.askopenfilename(
            title=f'Choose a map for "{singlemap.button_option2}" button',
            initialdir=program_dir,
            filetypes=[('Haemimont HPFS File', '*.bfhp')]
        )
        if file_path:
            rel_path = os.path.relpath(file_path, program_dir)
            new_dirname, new_filename = os.path.split(rel_path)
            new_filename_noext, new_ext = os.path.splitext(new_filename)
            temp_result = check_if_exists(new_dirname, new_filename_noext, new_ext)
            if temp_result == '':
                singlemap.config_text = new_dirname + '/' + new_filename_noext
                singlemap.button_text = f'[[SettingsCustomMap]]{singlemap.button_option2}[[]]'
            else:
                messagebox.showwarning('Failed to edit "Tutorial" field! ', temp_result)
                singlemap.set(singlemap.prev_value)
                return
        else:
            singlemap.set(singlemap.prev_value)
            return
    else:
        singlemap.config_text = 'Adventures/tutorial'
        singlemap.button_text = '[[21826997]]Tutorial[[]]'
    singlemapvalue_set['text'] = singlemap.config_text
    singlemap.prev_value = singlemap.get()

singlemap_check = ttk.Checkbutton(singleplayer_frame, text=f'Replace Tutorial button with {singlemap.button_option2} ', 
                                   variable=singlemap, command=singlemap_changed, onvalue='1', offvalue='0')
singlemap_check.grid(column=2, row=1, columnspan=2, sticky=(tk.W, tk.E))
singlemap_tooltip = ToolTip(singlemap_check, 'It is recommended to choose a Single Player Only map or Adventure')

#  language_frame 
language_frame = ttk.LabelFrame(mainframe, text='Language', padding=5)
language_frame.grid(column=3, row=2, sticky=(tk.W, tk.E), padx=5, pady=2)
language_frame.grid_columnconfigure(1, weight=1)

lang = StringVar()
lang_combo = ttk.Combobox(language_frame, width=12, textvariable=lang)
lang_combo.grid(column=1, row=1, sticky=(tk.W, tk.E))
lang_combo['values'] = ('English', 'Russian', 'German', 'Bulgarian', 'Chinese', 'French', 'Italian', 'Polish', 'Spanish')
lang_tooltip = ToolTip(lang_combo, 'If you have resources for a non-listed language in the "Local" directory, \nyou can simply enter its name here and press "Save" to change the language.')

#  particle_frame 
particle_frame = ttk.LabelFrame(mainframe, text='Particle System', padding=5)
particle_frame.grid(column=4, row=2, sticky=(tk.W, tk.E), padx=5, pady=2)

part = StringVar()
part_combo = ttk.Combobox(particle_frame, width=12, textvariable=part)
part_combo.grid(column=1, row=1, sticky=(tk.W, tk.E))
part_combo['values'] = ('Low', 'Medium', 'High')
part_tooltip = ToolTip(part_combo, 'It is recommended to set the Particle System to Low if you frequently experience game crashes.')

#  healthbaralt_frame 
healthbaralt_frame = ttk.LabelFrame(mainframe, text='Healthbars shown with Alt-Key', padding=5)
healthbaralt_frame.grid(column=3, row=3, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=2)

hp_alt = IntVar()
hp_alt_friendly = ttk.Radiobutton(healthbaralt_frame, text='Friendly', variable=hp_alt, value=2)
hp_alt_friendly.grid(column=1, row=1, sticky=(tk.W, tk.E), padx=5)

hp_alt_enemy = ttk.Radiobutton(healthbaralt_frame, text='Enemy', variable=hp_alt, value=4)
hp_alt_enemy.grid(column=2, row=1, sticky=(tk.W, tk.E), padx=5)

hp_alt_all = ttk.Radiobutton(healthbaralt_frame, text='All', variable=hp_alt, value=6)
hp_alt_all.grid(column=3, row=1, sticky=(tk.W, tk.E), padx=5)

hp_altsw = IntVar()
hp_altsw_check = ttk.Checkbutton(healthbaralt_frame, text='Severely wounded Units only', variable=hp_altsw, onvalue='1', offvalue='0')
hp_altsw_check.grid(column=1, row=2, columnspan=3, sticky=(tk.W, tk.E), padx=5)

#  healthbarctrl_frame 
healthbarctrl_frame = ttk.LabelFrame(mainframe, text='Healthbars shown with Ctrl-Key', padding=5)
healthbarctrl_frame.grid(column=3, row=4, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=2)

hp_ctrl = IntVar()
hp_ctrl_friendly = ttk.Radiobutton(healthbarctrl_frame, text='Friendly', variable=hp_ctrl, value=2)
hp_ctrl_friendly.grid(column=1, row=1, sticky=(tk.W, tk.E), padx=5)

hp_ctrl_enemy = ttk.Radiobutton(healthbarctrl_frame, text='Enemy', variable=hp_ctrl, value=4)
hp_ctrl_enemy.grid(column=2, row=1, sticky=(tk.W, tk.E), padx=5)

hp_ctrl_all = ttk.Radiobutton(healthbarctrl_frame, text='All', variable=hp_ctrl, value=6)
hp_ctrl_all.grid(column=3, row=1, sticky=(tk.W, tk.E), padx=5)

hp_ctrlsw = IntVar()
hp_ctrlsw_check = ttk.Checkbutton(healthbarctrl_frame, text='Severely wounded Units only', variable=hp_ctrlsw, onvalue='1', offvalue='0')
hp_ctrlsw_check.grid(column=1, row=2, columnspan=3, sticky=(tk.W, tk.E), padx=5)

#-------------------------------------Remaining elements on main frame------------------------------

# OpenSpy
openspy = StringVar()
openspy_check = ttk.Checkbutton(mainframe, text='Activate OpenSpy', variable=openspy, onvalue='1', offvalue='0')
openspy_check.grid(column=1, row=6, sticky=(tk.W, tk.E))

# Environanim
environ = StringVar()
environ_check = ttk.Checkbutton(mainframe, text='No Environmental Animations', variable=environ, onvalue='1', offvalue='0')
environ_check.grid(column=2, row=6, sticky=(tk.W, tk.E))

# Allow Transparent Units
transp = StringVar()
transp_check = ttk.Checkbutton(mainframe, text='No Transparent Units', variable=transp, onvalue='1', offvalue='0')
transp_check.grid(column=3, row=6, sticky=(tk.W, tk.E))

# View Fog Effect
fog = StringVar()
fog_check = ttk.Checkbutton(mainframe, text='View Fog Effect', variable=fog, onvalue='1', offvalue='0')
fog_check.grid(column=1, row=7, sticky=(tk.W, tk.E))
fog_tooltip = ToolTip(fog_check, 'Fog Effect works correctly only for 1024x768 resolution!')

# DebugKeys
debugkeys = StringVar()
debugkeys_check = ttk.Checkbutton(mainframe, text='Debug Keys enabled', variable=debugkeys, onvalue='1', offvalue='0')
debugkeys_check.grid(column=2, row=7, sticky=(tk.W, tk.E))

# DxWrapper
wrapper = IntVar()
wrapper_check = ttk.Checkbutton(mainframe, text='Activate DxWrapper', variable=wrapper, onvalue='1', offvalue='0')
wrapper_check.grid(column=3, row=7, sticky=(tk.W, tk.E))

# Always Show Champion Healthbar
champ = StringVar()
champ_check = ttk.Checkbutton(mainframe, text='Show Champion Healthbars', variable=champ, onvalue='1', offvalue='0')
champ_check.grid(column=1, row=8, sticky=(tk.W, tk.E))

# empty offset line
blankspace_z = tk.Label(mainframe, width=2, height=2)
blankspace_z.grid(column=1, row=9)

#-------------------------------------Read DATA------------------------------

#reading config.ini 
config = configparser.ConfigParser(allow_no_value=True, strict=False)
config.read('config.ini', encoding='utf-8')

username.set(config['system']['DefaultPlayerName'])

if config['system']['windowx'] == '1920':
    resolution.set('1920x1080')
elif config['system']['windowx'] == '1600':
    resolution.set('1600x900')
elif config['system']['windowx'] == '1360':
    resolution.set('1360x768')
elif config['system']['windowx'] == '1280':
    resolution.set('1280x720')
else:
    resolution.set('1024x768')

openspy.set(config['system']['gamespyingame'])

fullscreen.set(config['system']['fullscreen'])

debugkeys.set(config['system']['debugkeys'])

singlemap.config_text = config['system']['singlepalyermap']
if singlemap.config_text == 'Adventures/tutorial':
    singlemap.set(0)
    singlemap.button_text = '[[21826997]]Tutorial[[]]'
else:
    singlemap.set(1)
    singlemap.button_text = f'[[SettingsCustomMap]]{singlemap.button_option2}[[]]'
singlemap.prev_value = singlemap.get()
singlemapvalue_set['text'] = singlemap.config_text

#reading vxSettings.ini
settingsconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
settingsconfig.read('vxSettings.ini', encoding='utf-8')

lang.set(settingsconfig['Language']['default'])

if settingsconfig['Options']['noviewfog'] == '1':
    fog.set(0)
else:
    fog.set(1)

champ.set(settingsconfig['Options']['herohealthbars'])

sound.set(settingsconfig['Options']['soundvolume'])
music.set(settingsconfig['Options']['musicvolume'])
speech.set(settingsconfig['Options']['speechvolume'])
scroll.set(settingsconfig['Options']['scrollspeed'])

if settingsconfig['Options']['particlesystemdetails'] == '2':
    part.set('High')
elif settingsconfig['Options']['particlesystemdetails'] == '1':
    part.set('Medium')
else:
    part.set('Low')

environ.set(settingsconfig['Options']['noobjectanimations'])
transp.set(settingsconfig['Options']['nobuildingglowanims'])

if settingsconfig['Options']['healthbaraltflags'] in ['2', '4', '6']:
    hp_alt.set(int(settingsconfig['Options']['healthbaraltflags']))
    hp_altsw.set(0)
else:
    read_hp_alt = int(settingsconfig['Options']['healthbaraltflags']) - 1
    hp_alt.set(read_hp_alt)
    hp_altsw.set(1)

if settingsconfig['Options']['healthbarctrlflags'] in ['2', '4', '6']:
    hp_ctrl.set(int(settingsconfig['Options']['healthbarctrlflags']))
    hp_ctrlsw.set(0)
else:
    read_hp_ctrl = int(settingsconfig['Options']['healthbarctrlflags']) - 1
    hp_ctrl.set(read_hp_ctrl)
    hp_ctrlsw.set(1)

#reading dxwrapper.ini
wrapperconfig = configparser.ConfigParser()
wrapperconfig.read('dxwrapper.ini', encoding='utf-8')
if wrapperconfig['General']['IncludeProcess'] == 'rk.exe':
    wrapper.set(1)
else:
    wrapper.set(0)

#-------------------------------------DATA creation--------------------------

def save():
    #DxWrapper
    if wrapper.get() == 0:
        dxwrapper1 = 'none.exe'
    else:
        dxwrapper1 = 'rk.exe'

    wrapperconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    wrapperconfig.read('dxwrapper.ini', encoding='utf-8')
    wrapperconfig['General']['IncludeProcess'] = str(dxwrapper1)

    with open('dxwrapper.ini', 'w', encoding='utf-8') as wrapperfile:
        wrapperconfig.write(wrapperfile)

    #-config.ini-
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    username1 = username.get()
    config['system']['DefaultPlayerName'] = str(username1)

    openspy1 = '1' if openspy.get() == '1' else '0'
    config['system']['gamespyingame'] = openspy1

    debugkeys1 = '1' if debugkeys.get() == '1' else '0'
    config['system']['debugkeys'] = debugkeys1

    fullscreen1 = '1' if fullscreen.get() == '1' else '0'
    config['system']['fullscreen'] = fullscreen1

    config['system']['singlepalyermap'] = singlemap.config_text

    if resolution.get() == '1920x1080':
        res_x = '1920'
        res_y = '1080'
    elif resolution.get() == '1360x768':
        res_x = '1360'
        res_y = '768'
    elif resolution.get() == '1280x720':
        res_x = '1280'
        res_y = '720'
    elif resolution.get() == '1600x900':
        res_x = '1600'
        res_y = '900'
    else:
        res_x = '1024'
        res_y = '768'

    config['system']['windowx'] = res_x
    config['system']['windowy'] = res_y

    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)

    #-vxSettings.ini-
    settingsconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    settingsconfig.read('vxSettings.ini', encoding='utf-8')

    if lang.get() == '':
        lang1 = 'english'
    else:
        lang1 = lang.get()

    temp_result = check_if_exists('Local', lang1, '.pak')
    if temp_result == '':
        settingsconfig['Language']['default'] = str(lang1)
    else:
        messagebox.showwarning('Failed to edit "Language" field! ', temp_result)

    fog1 = '1' if fog.get() == '0' else '0'
    settingsconfig['Options']['noviewfog'] = fog1

    champ1 = '1' if champ.get() == '1' else '0'
    settingsconfig['Options']['herohealthbars'] = champ1

    settingsconfig['Options']['scrollspeed'] = str(scroll.get())
    settingsconfig['Options']['soundvolume'] = str(sound.get())
    settingsconfig['Options']['musicvolume'] = str(music.get())
    settingsconfig['Options']['speechvolume'] = str(speech.get())

    hp_alt_value = hp_alt.get() + hp_altsw.get()
    settingsconfig['Options']['healthbaraltflags'] = str(hp_alt_value)

    hp_ctrl_value = hp_ctrl.get() + hp_ctrlsw.get()
    settingsconfig['Options']['healthbarctrlflags'] = str(hp_ctrl_value)

    settingsconfig['OnlineBattle']['lastusername'] = str(username1)

    environ1 = '1' if environ.get() == '1' else '0'
    settingsconfig['Options']['noobjectanimations'] = environ1

    transp1 = '1' if transp.get() == '1' else '0'
    settingsconfig['Options']['nobuildingglowanims'] = transp1

    if part.get() == 'High':
        part1 = '2'
    elif part.get() == 'Medium':
        part1 = '1'
    else:
        part1 = '0'
    settingsconfig['Options']['particlesystemdetails'] = part1

    with open('vxSettings.ini', 'w', encoding='utf-8') as settingsfile:
        settingsconfig.write(settingsfile)

    #--DATA\VXCONST.ini--
    constconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    constconfig.read(r'DATA\VXCONST.ini', encoding='utf-8')

    if res_y == '1080':
        constconfig['FrameDarklings']['Texture'] = 'assets/interface/darkling/interface_top_hd.tga'
        constconfig['FrameDarklings']['dest1'] = '0, 766'
        constconfig['FrameDarklings']['dest2'] = '992, 754'
        constconfig['FrameDarklings']['dest3'] = '227, 811'
        constconfig['FrameDarklings']['dest4'] = '453, 846'
        constconfig['FrameDarklings']['dest5'] = '483, 833'
        constconfig['FrameDarklings']['dest6'] = '738, 771'
        constconfig['FrameDarklings']['src6'] = '0, 172, 511, 255'

        constconfig['FrameForesters']['Texture'] = 'assets/interface/forester/interface_top_hd.tga'
        constconfig['FrameForesters']['dest1'] = '0, 782'
        constconfig['FrameForesters']['dest2'] = '226, 839'
        constconfig['FrameForesters']['dest3'] = '483, 857'
        constconfig['FrameForesters']['dest4'] = '739, 819'
        constconfig['FrameForesters']['dest5'] = '995, 848'
        constconfig['FrameForesters']['dest6'] = '223, 878'
        constconfig['FrameForesters']['src4'] = '0, 163, 512, 212'

        constconfig['FrameHumans']['Texture'] = 'assets/interface/human/interface_top_hd.tga'
        constconfig['FrameHumans']['dest1'] = '0, 799'
        constconfig['FrameHumans']['dest2'] = '799, 834'
        constconfig['FrameHumans']['dest3'] = '223, 868'
        constconfig['FrameHumans']['dest4'] = '479, 874'
        constconfig['FrameHumans']['dest5'] = '735, 868'
        constconfig['FrameHumans']['src2'] = '32, 72, 512, 106'

        constconfig['Frame']['Texture'] = 'assets/interface/human/interface_top_hd.tga'
        constconfig['Frame']['dest1'] = '0, 799'
        constconfig['Frame']['dest2'] = '799, 834'
        constconfig['Frame']['dest3'] = '223, 868'
        constconfig['Frame']['dest4'] = '479, 874'
        constconfig['Frame']['dest5'] = '735, 868'
        constconfig['Frame']['src2'] = '32, 72, 512, 106'

        constconfig['IndRaceIcons']['x'] = '1866'
        constconfig['GamePlay']['HintYPosLeft'] = '812'
        constconfig['GamePlay']['HintYPosRight'] = '812'

    elif res_y == '720':
        constconfig['FrameDarklings']['Texture'] = 'assets/interface/darkling/interface_top_hd.tga'
        constconfig['FrameDarklings']['dest1'] = '0, 426'
        constconfig['FrameDarklings']['dest2'] = '992, 415'
        constconfig['FrameDarklings']['dest3'] = '227, 471'
        constconfig['FrameDarklings']['dest4'] = '453, 506'
        constconfig['FrameDarklings']['dest5'] = '483, 493'
        constconfig['FrameDarklings']['dest6'] = '739, 431'
        constconfig['FrameDarklings']['src6'] = '0, 172, 511, 255'

        constconfig['FrameForesters']['Texture'] = 'assets/interface/forester/interface_top_hd.tga'
        constconfig['FrameForesters']['dest1'] = '0, 422'
        constconfig['FrameForesters']['dest2'] = '226, 479'
        constconfig['FrameForesters']['dest3'] = '483, 497'
        constconfig['FrameForesters']['dest4'] = '739, 459'
        constconfig['FrameForesters']['dest5'] = '995, 488'
        constconfig['FrameForesters']['dest6'] = '223, 518'
        constconfig['FrameForesters']['src4'] = '0, 163, 512, 212'

        constconfig['FrameHumans']['Texture'] = 'assets/interface/human/interface_top_hd.tga'
        constconfig['FrameHumans']['dest1'] = '0, 439'
        constconfig['FrameHumans']['dest2'] = '799, 474'
        constconfig['FrameHumans']['dest3'] = '223, 508'
        constconfig['FrameHumans']['dest4'] = '479, 514'
        constconfig['FrameHumans']['dest5'] = '735, 508'
        constconfig['FrameHumans']['src2'] = '32, 72, 512, 106'

        constconfig['Frame']['Texture'] = 'assets/interface/human/interface_top_hd.tga'
        constconfig['Frame']['dest1'] = '0, 439'
        constconfig['Frame']['dest2'] = '799, 474'
        constconfig['Frame']['dest3'] = '223, 508'
        constconfig['Frame']['dest4'] = '479, 514'
        constconfig['Frame']['dest5'] = '735, 508'
        constconfig['Frame']['src2'] = '32, 72, 512, 106'

        constconfig['IndRaceIcons']['x'] = '1226'
        constconfig['GamePlay']['HintYPosLeft'] = '452'
        constconfig['GamePlay']['HintYPosRight'] = '452'

    elif res_y == '900':
        constconfig['FrameDarklings']['Texture'] = 'assets/interface/darkling/interface_top_hd.tga'
        constconfig['FrameDarklings']['dest1'] = '0, 586'
        constconfig['FrameDarklings']['dest2'] = '992, 575'
        constconfig['FrameDarklings']['dest3'] = '227, 631'
        constconfig['FrameDarklings']['dest4'] = '453, 666'
        constconfig['FrameDarklings']['dest5'] = '483, 653'
        constconfig['FrameDarklings']['dest6'] = '738, 591'
        constconfig['FrameDarklings']['src6'] = '0, 172, 511, 255'

        constconfig['FrameForesters']['Texture'] = 'assets/interface/forester/interface_top_hd.tga'
        constconfig['FrameForesters']['dest1'] = '0, 602'
        constconfig['FrameForesters']['dest2'] = '226, 659'
        constconfig['FrameForesters']['dest3'] = '483, 677'
        constconfig['FrameForesters']['dest4'] = '739, 639'
        constconfig['FrameForesters']['dest5'] = '995, 668'
        constconfig['FrameForesters']['dest6'] = '223, 698'
        constconfig['FrameForesters']['src4'] = '0, 163, 512, 212'

        constconfig['FrameHumans']['Texture'] = 'assets/interface/human/interface_top_hd.tga'
        constconfig['FrameHumans']['dest1'] = '0, 619'
        constconfig['FrameHumans']['dest2'] = '799, 654'
        constconfig['FrameHumans']['dest3'] = '223, 688'
        constconfig['FrameHumans']['dest4'] = '479, 694'
        constconfig['FrameHumans']['dest5'] = '735, 688'
        constconfig['FrameHumans']['src2'] = '32, 72, 512, 106'

        constconfig['Frame']['Texture'] = 'assets/interface/human/interface_top_hd.tga'
        constconfig['Frame']['dest1'] = '0, 619'
        constconfig['Frame']['dest2'] = '799, 654'
        constconfig['Frame']['dest3'] = '223, 688'
        constconfig['Frame']['dest4'] = '479, 694'
        constconfig['Frame']['dest5'] = '735, 688'
        constconfig['Frame']['src2'] = '32, 72, 512, 106'

        constconfig['IndRaceIcons']['x'] = '1546'
        constconfig['GamePlay']['HintYPosLeft'] = '632'
        constconfig['GamePlay']['HintYPosRight'] = '632'

    else:  # 768 resolution
        constconfig['FrameDarklings']['Texture'] = 'assets/interface/darkling/interface_top.tga'
        constconfig['FrameDarklings']['dest1'] = '0, 474'
        constconfig['FrameDarklings']['dest2'] = '994, 463'
        constconfig['FrameDarklings']['dest3'] = '227, 519'
        constconfig['FrameDarklings']['dest4'] = '453, 554'
        constconfig['FrameDarklings']['dest5'] = '483, 541'
        constconfig['FrameDarklings']['dest6'] = '739, 479'
        constconfig['FrameDarklings']['src6'] = '0, 172, 255, 255'

        constconfig['FrameForesters']['Texture'] = 'assets/interface/forester/interface_top.tga'
        constconfig['FrameForesters']['dest1'] = '0, 473'
        constconfig['FrameForesters']['dest2'] = '226, 530'
        constconfig['FrameForesters']['dest3'] = '483, 548'
        constconfig['FrameForesters']['dest4'] = '739, 510'
        constconfig['FrameForesters']['dest5'] = '995, 539'
        constconfig['FrameForesters']['dest6'] = '223, 569'
        constconfig['FrameForesters']['src4'] = '0, 163, 256, 212'

        constconfig['FrameHumans']['Texture'] = 'assets/interface/human/interface_top.tga'
        constconfig['FrameHumans']['dest1'] = '0, 487'
        constconfig['FrameHumans']['dest2'] = '799, 522'
        constconfig['FrameHumans']['dest3'] = '223, 556'
        constconfig['FrameHumans']['dest4'] = '479, 562'
        constconfig['FrameHumans']['dest5'] = '735, 556'
        constconfig['FrameHumans']['src2'] = '32, 72, 256, 106'

        constconfig['Frame']['Texture'] = 'assets/interface/human/interface_top.tga'
        constconfig['Frame']['dest1'] = '0, 487'
        constconfig['Frame']['dest2'] = '799, 522'
        constconfig['Frame']['dest3'] = '223, 556'
        constconfig['Frame']['dest4'] = '479, 562'
        constconfig['Frame']['dest5'] = '735, 556'
        constconfig['Frame']['src2'] = '32, 72, 256, 106'

        if res_x == '1360':
            constconfig['IndRaceIcons']['x'] = '1312'
            constconfig['GamePlay']['HintYPosLeft'] = '500'
            constconfig['GamePlay']['HintYPosRight'] = '520'
        else:
            constconfig['IndRaceIcons']['x'] = '950'
            constconfig['GamePlay']['HintYPosLeft'] = '500'
            constconfig['GamePlay']['HintYPosRight'] = '520'

    with open(r'DATA\VXCONST.ini', 'w', encoding='utf-8') as constfile:
        constconfig.write(constfile)

    #profiles\noname
    profileconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    profileconfig.read(r'PROFILES\NONAME\PLAYER.ini', encoding='utf-8')

    profileconfig['Player']['name'] = str(username1)
    profileconfig['Player 0']['plrname'] = str(username1)

    with open(r'PROFILES\NONAME\PLAYER.ini', 'w', encoding='utf-8') as profilefile:
        profileconfig.write(profilefile)

    #DATA\INTERFACE\MENU\MainMenu.ini
    mainconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    mainconfig.read(r'DATA\INTERFACE\MENU\MAINMENU.ini', encoding='utf-8')

    if res_y == '1080':
        mainconfig['MainMenu']['RectWH'] = '0, 0, 1920, 1080'
        mainconfig['Sheath']['RectWH'] = '726, 595, 276, 489'
        mainconfig['Sheath']['Image'] = 'menures/sheath_hd.bmp, 0, 0'
    elif res_y == '720':
        mainconfig['MainMenu']['RectWH'] = '0, 0, 1280, 720'
        mainconfig['Sheath']['RectWH'] = '734, 595, 264, 177'
        mainconfig['Sheath']['Image'] = 'menures/sheath.bmp, 0, 0'
    elif res_x == '1360':
        mainconfig['MainMenu']['RectWH'] = '0, 0, 1360, 768'
        mainconfig['Sheath']['RectWH'] = '734, 595, 264, 177'
        mainconfig['Sheath']['Image'] = 'menures/sheath.bmp, 0, 0'
    elif res_y == '900':
        mainconfig['MainMenu']['RectWH'] = '0, 0, 1600, 900'
        mainconfig['Sheath']['RectWH'] = '726, 595, 276, 489'
        mainconfig['Sheath']['Image'] = 'menures/sheath_hd.bmp, 0, 0'
    else:
        mainconfig['MainMenu']['RectWH'] = '0, 0, 1024, 768'
        mainconfig['Sheath']['RectWH'] = '734, 595, 264, 177'
        mainconfig['Sheath']['Image'] = 'menures/sheath.bmp, 0, 0'

    mainconfig['Tutorial']['Text'] = singlemap.button_text

    with open(r'DATA\INTERFACE\MENU\MAINMENU.ini', 'w', encoding='utf-8') as mainfile:
        mainconfig.write(mainfile)

    #DATA\INTERFACE\MENU\MenuBack.ini
    backconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    backconfig.read(r'DATA\INTERFACE\MENU\MENUBACK.ini', encoding='utf-8')

    if res_y == '1080':
        backconfig['MenuBack']['rectwh'] = '0, 0, 1920, 1080'
        backconfig['Back']['Image'] = 'menures/main_background_hd.bmp, 400, 300'
        backconfig['Back']['RectWH'] = '0, 0, 1920, 1080'
        backconfig['BlackBkg']['rectwh'] = '0, 0, 1920, 1080'
    elif res_y == '720':
        backconfig['MenuBack']['rectwh'] = '0, 0, 1280, 720'
        backconfig['Back']['Image'] = 'menures/main_background_1280.bmp, 400, 300'
        backconfig['Back']['RectWH'] = '0, 0, 1280, 720'
        backconfig['BlackBkg']['rectwh'] = '0, 0, 1280, 720'
    elif res_x == '1360':
        backconfig['MenuBack']['rectwh'] = '0, 0, 1360, 768'
        backconfig['Back']['Image'] = 'menures/main_background_1360.bmp, 400, 300'
        backconfig['Back']['RectWH'] = '0, 0, 1360, 768'
        backconfig['BlackBkg']['rectwh'] = '0, 0, 1360, 768'
    elif res_y == '900':
        backconfig['MenuBack']['rectwh'] = '0, 0, 1600, 900'
        backconfig['Back']['Image'] = 'menures/main_background_1600.bmp, 400, 300'
        backconfig['Back']['RectWH'] = '0, 0, 1600, 900'
        backconfig['BlackBkg']['rectwh'] = '0, 0, 1600, 900'
    else:
        backconfig['MenuBack']['rectwh'] = '0, 0, 1024, 768'
        backconfig['Back']['Image'] = 'menures/main_background.bmp, 400, 300'
        backconfig['Back']['RectWH'] = '0, 0, 1024, 768'
        backconfig['BlackBkg']['rectwh'] = '0, 0, 1024, 768'

    with open(r'DATA\INTERFACE\MENU\MENUBACK.ini', 'w', encoding='utf-8') as backfile:
        backconfig.write(backfile)

    #DATA\INTERFACE\MENU\OB_LOBBY.ini
    oblobbyconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    oblobbyconfig.read(r'DATA\INTERFACE\MENU\OB_LOBBY.ini', encoding='utf-8')

    if res_y == '1080':
        oblobbyconfig['Ob_lobby']['RectWH'] = '0, 0, 1920, 1080'
        oblobbyconfig['Ob_lobby Params']['DialogRect'] = '0, 0, 1920, 1080'
    elif res_y == '720':
        oblobbyconfig['Ob_lobby']['RectWH'] = '0, 0, 1280, 720'
        oblobbyconfig['Ob_lobby Params']['DialogRect'] = '0, 0, 1280, 720'
    elif res_x == '1360':
        oblobbyconfig['Ob_lobby']['RectWH'] = '0, 0, 1360, 768'
        oblobbyconfig['Ob_lobby Params']['DialogRect'] = '0, 0, 1360, 768'
    elif res_y == '900':
        oblobbyconfig['Ob_lobby']['RectWH'] = '0, 0, 1600, 900'
        oblobbyconfig['Ob_lobby Params']['DialogRect'] = '0, 0, 1600, 900'
    else:
        oblobbyconfig['Ob_lobby']['RectWH'] = '0, 0, 1024, 768'
        oblobbyconfig['Ob_lobby Params']['DialogRect'] = '0, 0, 1024, 768'

    with open(r'DATA\INTERFACE\MENU\OB_LOBBY.ini', 'w', encoding='utf-8') as oblobbyfile:
        oblobbyconfig.write(oblobbyfile)

    #DATA\INTERFACE\MENU\OB_PROFILE.ini
    obprofileconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    obprofileconfig.read(r'DATA\INTERFACE\MENU\OB_PROFILE.ini', encoding='utf-8')

    if res_y == '1080':
        obprofileconfig['Ob_profile']['RectWH'] = '0, 0, 1920, 1080'
        obprofileconfig['Ob_profile Params']['DialogRect'] = '0, 0, 1920, 1080'
    elif res_y == '720':
        obprofileconfig['Ob_profile']['RectWH'] = '0, 0, 1280, 720'
        obprofileconfig['Ob_profile Params']['DialogRect'] = '0, 0, 1280, 720'
    elif res_x == '1360':
        obprofileconfig['Ob_profile']['RectWH'] = '0, 0, 1360, 768'
        obprofileconfig['Ob_profile Params']['DialogRect'] = '0, 0, 1360, 768'
    elif res_y == '900':
        obprofileconfig['Ob_profile']['RectWH'] = '0, 0, 1600, 900'
        obprofileconfig['Ob_profile Params']['DialogRect'] = '0, 0, 1600, 900'
    else:
        obprofileconfig['Ob_profile']['RectWH'] = '0, 0, 1024, 768'
        obprofileconfig['Ob_profile Params']['DialogRect'] = '0, 0, 1024, 768'

    with open(r'DATA\INTERFACE\MENU\OB_PROFILE.ini', 'w', encoding='utf-8') as obprofilefile:
        obprofileconfig.write(obprofilefile)

    #DATA\INTERFACE\MENU\OB_LOGIN.ini
    obloginconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    obloginconfig.read(r'DATA\INTERFACE\MENU\OB_LOGIN.ini', encoding='utf-8')

    if res_y == '1080':
        obloginconfig['Ob_login']['RectWH'] = '0, 0, 1920, 1080'
        obloginconfig['Ob_login Params']['DialogRect'] = '0, 0, 1920, 1080'
    elif res_y == '720':
        obloginconfig['Ob_login']['RectWH'] = '0, 0, 1280, 720'
        obloginconfig['Ob_login Params']['DialogRect'] = '0, 0, 1280, 720'
    elif res_x == '1360':
        obloginconfig['Ob_login']['RectWH'] = '0, 0, 1360, 768'
        obloginconfig['Ob_login Params']['DialogRect'] = '0, 0, 1360, 768'
    elif res_y == '900':
        obloginconfig['Ob_login']['RectWH'] = '0, 0, 1600, 900'
        obloginconfig['Ob_login Params']['DialogRect'] = '0, 0, 1600, 900'
    else:
        obloginconfig['Ob_login']['RectWH'] = '0, 0, 1024, 768'
        obloginconfig['Ob_login Params']['DialogRect'] = '0, 0, 1024, 768'

    with open(r'DATA\INTERFACE\MENU\OB_LOGIN.ini', 'w', encoding='utf-8') as obloginfile:
        obloginconfig.write(obloginfile)

    #DATA\INTERFACE\MENU\OB_REGISTER.ini
    obregisterconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    obregisterconfig.read(r'DATA\INTERFACE\MENU\OB_REGISTER.ini', encoding='utf-8')

    if res_y == '1080':
        obregisterconfig['Ob_register']['RectWH'] = '0, 0, 1920, 1080'
        obregisterconfig['Ob_register Params']['DialogRect'] = '0, 0, 1920, 1080'
    elif res_y == '720':
        obregisterconfig['Ob_register']['RectWH'] = '0, 0, 1280, 720'
        obregisterconfig['Ob_register Params']['DialogRect'] = '0, 0, 1280, 720'
    elif res_x == '1360':
        obregisterconfig['Ob_register']['RectWH'] = '0, 0, 1360, 768'
        obregisterconfig['Ob_register Params']['DialogRect'] = '0, 0, 1360, 768'
    elif res_y == '900':
        obregisterconfig['Ob_register']['RectWH'] = '0, 0, 1600, 900'
        obregisterconfig['Ob_register Params']['DialogRect'] = '0, 0, 1600, 900'
    else:
        obregisterconfig['Ob_register']['RectWH'] = '0, 0, 1024, 768'
        obregisterconfig['Ob_register Params']['DialogRect'] = '0, 0, 1024, 768'

    with open(r'DATA\INTERFACE\MENU\OB_REGISTER.ini', 'w', encoding='utf-8') as obregisterfile:
        obregisterconfig.write(obregisterfile)

    #DATA\INTERFACE\MENU\OB_HALLOFFAME.ini
    obhofconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    obhofconfig.read(r'DATA\INTERFACE\MENU\OB_HALLOFFAME.ini', encoding='utf-8')

    if res_y == '1080':
        obhofconfig['Ob_halloffame']['RectWH'] = '0, 0, 1920, 1080'
        obhofconfig['Ob_halloffame Params']['DialogRect'] = '0, 0, 1920, 1080'
    elif res_y == '720':
        obhofconfig['Ob_halloffame']['RectWH'] = '0, 0, 1280, 720'
        obhofconfig['Ob_halloffame Params']['DialogRect'] = '0, 0, 1280, 720'
    elif res_x == '1360':
        obhofconfig['Ob_halloffame']['RectWH'] = '0, 0, 1360, 768'
        obhofconfig['Ob_halloffame Params']['DialogRect'] = '0, 0, 1360, 768'
    elif res_y == '900':
        obhofconfig['Ob_halloffame']['RectWH'] = '0, 0, 1600, 900'
        obhofconfig['Ob_halloffame Params']['DialogRect'] = '0, 0, 1600, 900'
    else:
        obhofconfig['Ob_halloffame']['RectWH'] = '0, 0, 1024, 768'
        obhofconfig['Ob_halloffame Params']['DialogRect'] = '0, 0, 1024, 768'

    with open(r'DATA\INTERFACE\MENU\OB_HALLOFFAME.ini', 'w', encoding='utf-8') as obhoffile:
        obhofconfig.write(obhoffile)

    #DATA\INTERFACE\MENU\OB_AUTOMATCH.ini
    obautoconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    obautoconfig.read(r'DATA\INTERFACE\MENU\OB_AUTOMATCH.ini', encoding='utf-8')

    if res_y == '1080':
        obautoconfig['Ob_automatch']['RectWH'] = '0, 0, 1920, 1080'
        obautoconfig['Ob_automatch Params']['DialogRect'] = '0, 0, 1920, 1080'
    elif res_y == '720':
        obautoconfig['Ob_automatch']['RectWH'] = '0, 0, 1280, 720'
        obautoconfig['Ob_automatch Params']['DialogRect'] = '0, 0, 1280, 720'
    elif res_x == '1360':
        obautoconfig['Ob_automatch']['RectWH'] = '0, 0, 1360, 768'
        obautoconfig['Ob_automatch Params']['DialogRect'] = '0, 0, 1360, 768'
    elif res_y == '900':
        obautoconfig['Ob_automatch']['RectWH'] = '0, 0, 1600, 900'
        obautoconfig['Ob_automatch Params']['DialogRect'] = '0, 0, 1600, 900'
    else:
        obautoconfig['Ob_automatch']['RectWH'] = '0, 0, 1024, 768'
        obautoconfig['Ob_automatch Params']['DialogRect'] = '0, 0, 1024, 768'

    with open(r'DATA\INTERFACE\MENU\OB_AUTOMATCH.ini', 'w', encoding='utf-8') as obautofile:
        obautoconfig.write(obautofile)

    #DATA\INTERFACE\MENU\GAMEMENU.ini
    gmconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    gmconfig.read(r'DATA\INTERFACE\MENU\GAMEMENU.ini', encoding='utf-8')

    if res_y == '1080':
        gmconfig['gamemenu']['RectWH'] = '0, 0, 1920, 1080'
    elif res_y == '720':
        gmconfig['gamemenu']['RectWH'] = '0, 0, 1280, 720'
    elif res_x == '1360':
        gmconfig['gamemenu']['RectWH'] = '0, 0, 1360, 768'
    elif res_y == '900':
        gmconfig['gamemenu']['RectWH'] = '0, 0, 1600, 900'
    else:
        gmconfig['gamemenu']['RectWH'] = '0, 0, 1024, 768'

    with open(r'DATA\INTERFACE\MENU\GAMEMENU.ini', 'w', encoding='utf-8') as gmfile:
        gmconfig.write(gmfile)

    #DATA\INTERFACE\MENU\GAMEOPTIONS.ini
    goconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    goconfig.read(r'DATA\INTERFACE\MENU\GAMEOPTIONS.ini', encoding='utf-8')

    if res_y == '1080':
        goconfig['GameOptions']['RectWH'] = '0, 0, 1920, 1080'
    elif res_y == '720':
        goconfig['GameOptions']['RectWH'] = '0, 0, 1280, 720'
    elif res_x == '1360':
        goconfig['GameOptions']['RectWH'] = '0, 0, 1360, 768'
    elif res_y == '900':
        goconfig['GameOptions']['RectWH'] = '0, 0, 1600, 900'
    else:
        goconfig['GameOptions']['RectWH'] = '0, 0, 1024, 768'

    with open(r'DATA\INTERFACE\MENU\GAMEOPTIONS.ini', 'w', encoding='utf-8') as gofile:
        goconfig.write(gofile)

    #-Darklings\CMDBAR.INI-
    darklingsconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    darklingsconfig.read(r'DATA\INTERFACE\Darklings\CMDBAR.ini', encoding='utf-8')

    if res_x == '1920':
        darklingsconfig['Cmdbar']['RectWH'] = '0, 0, 1920, 247'
        darklingsconfig['Bottom']['Image'] = 'assets/interface/darkling/interface_BOTTOM_hd.bmp, 100, 100'
        darklingsconfig['Bottom']['RectWH'] = '0, 0, 1920, 247'
    elif res_x == '1280':
        darklingsconfig['Cmdbar']['RectWH'] = '0, 0, 1280, 247'
        darklingsconfig['Bottom']['Image'] = 'assets/interface/darkling/interface_BOTTOM_1280.bmp, 100, 100'
        darklingsconfig['Bottom']['RectWH'] = '0, 0, 1280, 247'
    elif res_x == '1360':
        darklingsconfig['Cmdbar']['RectWH'] = '0, 0, 1360, 247'
        darklingsconfig['Bottom']['Image'] = 'assets/interface/darkling/interface_BOTTOM_1360.bmp, 100, 100'
        darklingsconfig['Bottom']['RectWH'] = '0, 0, 1360, 247'
    elif res_x == '1600':
        darklingsconfig['Cmdbar']['RectWH'] = '0, 0, 1600, 247'
        darklingsconfig['Bottom']['Image'] = 'assets/interface/darkling/interface_BOTTOM_1600.bmp, 100, 100'
        darklingsconfig['Bottom']['RectWH'] = '0, 0, 1600, 247'
    else:
        darklingsconfig['Cmdbar']['RectWH'] = '0, 0, 1024, 227'
        darklingsconfig['Bottom']['Image'] = 'assets/interface/darkling/interface_BOTTOM.bmp, 100, 100'
        darklingsconfig['Bottom']['RectWH'] = '0, 0, 1024, 227'

    with open(r'DATA\INTERFACE\Darklings\CMDBAR.ini', 'w', encoding='utf-8') as darklingsfile:
        darklingsconfig.write(darklingsfile)

    #-Foresters\CMDBAR.INI-
    forestersconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    forestersconfig.read(r'DATA\INTERFACE\Foresters\CMDBAR.ini', encoding='utf-8')

    if res_x == '1920':
        forestersconfig['Cmdbar']['RectWH'] = '0, 0, 1920, 227'
        forestersconfig['Bottom']['Image'] = 'assets/interface/forester/interface_BOTTOM_hd.bmp, 100, 100'
        forestersconfig['Bottom']['RectWH'] = '0, 0, 1920, 227'
    elif res_x == '1280':
        forestersconfig['Cmdbar']['RectWH'] = '0, 0, 1280, 227'
        forestersconfig['Bottom']['Image'] = 'assets/interface/forester/interface_BOTTOM_1280.bmp, 100, 100'
        forestersconfig['Bottom']['RectWH'] = '0, 0, 1280, 227'
    elif res_x == '1360':
        forestersconfig['Cmdbar']['RectWH'] = '0, 0, 1360, 227'
        forestersconfig['Bottom']['Image'] = 'assets/interface/forester/interface_BOTTOM_1360.bmp, 100, 100'
        forestersconfig['Bottom']['RectWH'] = '0, 0, 1360, 227'
    elif res_x == '1600':
        forestersconfig['Cmdbar']['RectWH'] = '0, 0, 1600, 227'
        forestersconfig['Bottom']['Image'] = 'assets/interface/forester/interface_BOTTOM_1600.bmp, 100, 100'
        forestersconfig['Bottom']['RectWH'] = '0, 0, 1600, 227'
    else:
        forestersconfig['Cmdbar']['RectWH'] = '0, 0, 1024, 227'
        forestersconfig['Bottom']['Image'] = 'assets/interface/forester/interface_BOTTOM.bmp, 100, 100'
        forestersconfig['Bottom']['RectWH'] = '0, 0, 1024, 227'

    with open(r'DATA\INTERFACE\Foresters\CMDBAR.ini', 'w', encoding='utf-8') as forestersfile:
        forestersconfig.write(forestersfile)

    #-Humans\CMDBAR.INI-
    humansconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    humansconfig.read(r'DATA\INTERFACE\Humans\CMDBAR.ini', encoding='utf-8')

    if res_x == '1920':
        humansconfig['Cmdbar']['RectWH'] = '0, 0, 1920, 227'
        humansconfig['Bottom']['Image'] = 'assets/interface/human/interface_BOTTOM_hd.bmp, 100, 100, 100, 100'
        humansconfig['Bottom']['RectWH'] = '0, 0, 1920, 227'
    elif res_x == '1280':
        humansconfig['Cmdbar']['RectWH'] = '0, 0, 1280, 227'
        humansconfig['Bottom']['Image'] = 'assets/interface/human/interface_BOTTOM_1280.bmp, 100, 100, 100, 100'
        humansconfig['Bottom']['RectWH'] = '0, 0, 1280, 227'
    elif res_x == '1360':
        humansconfig['Cmdbar']['RectWH'] = '0, 0, 1360, 227'
        humansconfig['Bottom']['Image'] = 'assets/interface/human/interface_BOTTOM_1360.bmp, 100, 100, 100, 100'
        humansconfig['Bottom']['RectWH'] = '0, 0, 1360, 227'
    elif res_x == '1600':
        humansconfig['Cmdbar']['RectWH'] = '0, 0, 1600, 227'
        humansconfig['Bottom']['Image'] = 'assets/interface/human/interface_BOTTOM_1600.bmp, 100, 100, 100, 100'
        humansconfig['Bottom']['RectWH'] = '0, 0, 1600, 227'
    else:
        humansconfig['Cmdbar']['RectWH'] = '0, 0, 1024, 227'
        humansconfig['Bottom']['Image'] = 'assets/interface/human/interface_BOTTOM.bmp, 100, 100, 100, 100'
        humansconfig['Bottom']['RectWH'] = '0, 0, 1024, 227'

    with open(r'DATA\INTERFACE\Humans\CMDBAR.ini', 'w', encoding='utf-8') as humansfile:
        humansconfig.write(humansfile)

    #-COMMON-
    commonconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    commonconfig.read(r'DATA\INTERFACE\CMDBAR.ini', encoding='utf-8')

    if res_x == '1920':
        commonconfig['Cmdbar']['RectWH'] = '0, 0, 1920, 227'
        commonconfig['Bottom']['Image'] = 'assets/interface/human/interface_BOTTOM_hd.bmp, 100, 100, 100, 100'
        commonconfig['Bottom']['RectWH'] = '0, 0, 1920, 227'
    elif res_x == '1280':
        commonconfig['Cmdbar']['RectWH'] = '0, 0, 1280, 227'
        commonconfig['Bottom']['Image'] = 'assets/interface/human/interface_BOTTOM_1280.bmp, 100, 100, 100, 100'
        commonconfig['Bottom']['RectWH'] = '0, 0, 1280, 227'
    elif res_x == '1360':
        commonconfig['Cmdbar']['RectWH'] = '0, 0, 1360, 227'
        commonconfig['Bottom']['Image'] = 'assets/interface/human/interface_BOTTOM_1360.bmp, 100, 100, 100, 100'
        commonconfig['Bottom']['RectWH'] = '0, 0, 1360, 227'
    elif res_x == '1600':
        commonconfig['Cmdbar']['RectWH'] = '0, 0, 1600, 227'
        commonconfig['Bottom']['Image'] = 'assets/interface/human/interface_BOTTOM_1600.bmp, 100, 100, 100, 100'
        commonconfig['Bottom']['RectWH'] = '0, 0, 1600, 227'
    else:
        commonconfig['Cmdbar']['RectWH'] = '0, 0, 1024, 227'
        commonconfig['Bottom']['Image'] = 'assets/interface/human/interface_BOTTOM.bmp, 100, 100, 100, 100'
        commonconfig['Bottom']['RectWH'] = '0, 0, 1024, 227'

    with open(r'DATA\INTERFACE\CMDBAR.ini', 'w', encoding='utf-8') as commonfile:
        commonconfig.write(commonfile)

    #EDITOR\infobar.ini
    infoconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    infoconfig.read(r'DATA\INTERFACE\EDITOR\INFOBAREDITOR.ini', encoding='utf-8')

    if res_y == '1080':
        infoconfig['InfobarEditor']['RectWH'] = '0, 0, 1920, 80'
        infoconfig['Background']['RectWH'] = '0, 0, 1920, 80'
        infoconfig['Background']['Image'] = 'assets/interface/editor/cmdbar_hd.bmp'
        infoconfig['AreaVisibility']['RectWH'] = '#277+448#, 5, 80, 80'
    elif res_y == '720':
        infoconfig['InfobarEditor']['RectWH'] = '0, 0, 1280, 80'
        infoconfig['Background']['RectWH'] = '0, 0, 1280, 80'
        infoconfig['Background']['Image'] = 'assets/interface/editor/cmdbar.bmp'
        infoconfig['AreaVisibility']['RectWH'] = '#277+128#, 5, 80, 80'
    elif res_x == '1360':
        infoconfig['InfobarEditor']['RectWH'] = '0, 0, 1360, 80'
        infoconfig['Background']['RectWH'] = '0, 0, 1360, 80'
        infoconfig['Background']['Image'] = 'assets/interface/editor/cmdbar.bmp'
        infoconfig['AreaVisibility']['RectWH'] = '#277+168#, 5, 80, 80'
    elif res_y == '900':
        infoconfig['InfobarEditor']['RectWH'] = '0, 0, 1600, 80'
        infoconfig['Background']['RectWH'] = '0, 0, 1600, 80'
        infoconfig['Background']['Image'] = 'assets/interface/editor/cmdbar_hd.bmp'
        infoconfig['AreaVisibility']['RectWH'] = '#277+288#, 5, 80, 80'
    else:
        infoconfig['InfobarEditor']['RectWH'] = '0, 0, 1280, 80'
        infoconfig['Background']['RectWH'] = '0, 0, 1280, 80'
        infoconfig['Background']['Image'] = 'assets/interface/editor/cmdbar.bmp'
        infoconfig['AreaVisibility']['RectWH'] = '#277+128#, 5, 80, 80'

    with open(r'DATA\INTERFACE\EDITOR\INFOBAREDITOR.ini', 'w', encoding='utf-8') as infofile:
        infoconfig.write(infofile)

    #EDITOR\cmdbar.ini
    editcmdconfig = configparser.ConfigParser(allow_no_value=True, strict=False)
    editcmdconfig.read(r'DATA\INTERFACE\EDITOR\CMDBAREDITOR.ini', encoding='utf-8')

    if res_y == '1080':
        editcmdconfig['CmdbarEditor']['RectWH'] = '0, 0, 1920, 80'
        editcmdconfig['Background']['RectWH'] = '0, 0, 1920, 80'
        editcmdconfig['Background']['Image'] = 'assets/interface/editor/infobar_hd.bmp'
        editcmdconfig['NewScenario']['RectWH'] = '#232+448#, 6, 80, 68'
    elif res_y == '720':
        editcmdconfig['CmdbarEditor']['RectWH'] = '0, 0, 1280, 80'
        editcmdconfig['Background']['RectWH'] = '0, 0, 1280, 80'
        editcmdconfig['Background']['Image'] = 'assets/interface/editor/infobar.bmp'
        editcmdconfig['NewScenario']['RectWH'] = '#232+128#, 6, 80, 68'
    elif res_x == '1360':
        editcmdconfig['CmdbarEditor']['RectWH'] = '0, 0, 1360, 80'
        editcmdconfig['Background']['RectWH'] = '0, 0, 1360, 80'
        editcmdconfig['Background']['Image'] = 'assets/interface/editor/infobar.bmp'
        editcmdconfig['NewScenario']['RectWH'] = '#232+168#, 6, 80, 68'
    elif res_y == '900':
        editcmdconfig['CmdbarEditor']['RectWH'] = '0, 0, 1600, 80'
        editcmdconfig['Background']['RectWH'] = '0, 0, 1600, 80'
        editcmdconfig['Background']['Image'] = 'assets/interface/editor/infobar_hd.bmp'
        editcmdconfig['NewScenario']['RectWH'] = '#232+288#, 6, 80, 68'
    else:
        editcmdconfig['CmdbarEditor']['RectWH'] = '0, 0, 1280, 80'
        editcmdconfig['Background']['RectWH'] = '0, 0, 1280, 80'
        editcmdconfig['Background']['Image'] = 'assets/interface/editor/infobar.bmp'
        editcmdconfig['NewScenario']['RectWH'] = '#232+128#, 6, 80, 68'

    with open(r'DATA\INTERFACE\EDITOR\CMDBAREDITOR.ini', 'w', encoding='utf-8') as editcmdfile:
        editcmdconfig.write(editcmdfile)

#-------------------------------------Default Settings------------------------------

def default():
    username.set('Player')
    resolution.set('1024x768')
    sound.set(50)
    music.set(50)
    speech.set(50)
    scroll.set(50)
    fullscreen.set('1')
    lang.set('English')
    part.set('Low')
    openspy.set('1')
    debugkeys.set('1')
    singlemap.set('0')
    singlemap.button_text = '[[21826997]]Tutorial[[]]'
    singlemap.config_text = 'Adventures/tutorial'
    singlemapvalue_set['text'] = singlemap.config_text
    singlemap.prev_value = 0
    environ.set('0')
    transp.set('0')
    fog.set('0')
    wrapper.set(1)
    champ.set('1')
    hp_alt.set(2)
    hp_altsw.set(0)
    hp_ctrl.set(6)
    hp_ctrlsw.set(0)

#-------------------------------------Bottom Tab------------------------------

#Reset
ttk.Button(mainframe, text='Reset to Default', command=default).grid(column=1, row=36, sticky=(tk.W))

#Save
ttk.Button(mainframe, text='Save', command=save).grid(column=2, row=36, sticky=(tk.E))

#Start
def start():
    subprocess.Popen('"rk.exe"', shell=True)
    root.destroy()

ttk.Button(mainframe, text='Start', command=start).grid(column=3, row=36, sticky=(tk.W))

#Exit
ttk.Button(mainframe, text='Exit', command=lambda: root.destroy()).grid(column=4, row=36, sticky=(tk.E))
root.mainloop()
