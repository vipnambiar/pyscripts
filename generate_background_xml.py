import mimetypes
import os
import sys
import xml.etree.ElementTree as ET

xmlFile = '/home/vipin/Pictures/Precise_Wallpapers/precise-wallpapers.xml'

def getWP_elems(tree):
    EXCLUDE = '/usr/share/backgrounds/contest/precise.xml'
    return [ elem for elem in tree.iter(tag='wallpaper')  if not EXCLUDE in [i.text for i in elem.iter(tag='filename')] ]

def _createContestXml_elem():
    contest_xml  = '/usr/share/backgrounds/contest/precise.xml'
    contest_name = 'Ubuntu 12.04 Community Wallpapers'
    
    elem              = ET.Element('wallpaper', {'deleted':"false"})
    name_elem         = ET.Element('name')
    fname_elem        = ET.Element('filename')
    options_elem      = ET.Element('options')
    
    name_elem.text    = contest_name
    fname_elem.text   = contest_xml
    options_elem.text = 'zoom'
    
    elem.extend([name_elem, fname_elem, options_elem])
    
    return elem

def _createWP_elem(name, filename):
    sub_tags = [ 'name', 'filename', 'options', 'p_color', 's_color', 'shade_type' ]
    sub_dict = { 
                 'name'       : name,
                 'filename'   : filename,
                 'options'    : 'zoom',
                 'p_color'    : '#000000',
                 's_color'    : '#000000',
                 'shade_type' : 'solid',
               }
    
    w_elem = ET.Element('wallpaper')
    for tag in sub_tags:
        sub_elem = ET.Element(tag)
        sub_elem.text = sub_dict[tag]
        w_elem.append(sub_elem)
    return w_elem

def addWallpaper(tree, name, filepath):
    root_elem = tree.getroot()
    if os.path.exists(filepath):
        wp_elem = _createWP_elem(name, filepath)
        root_elem.append(wp_elem)
        tree._setroot(root_elem)
    else:
        print "File not found!"
    fo = open(xmlFile, 'w')
    tree.write(fo)
    fo.close()

def getFiles(path='/usr/share/backgrounds'):
    IMAGE_TYPES = ('image/jpeg', 'image/png')
    file_list = []
    
    if not os.path.isdir(path):
        raise RuntimeError, "%s Not a valid path!" % path
    
    codec = sys.getfilesystemencoding()
    
    for root,dirs,files in os.walk(path.rstrip('/')):
        for file in files:
            f_name = file.decode(codec)
            path   = root.decode(codec)
            img_type, _ = mimetypes.guess_type(f_name)
            if img_type in IMAGE_TYPES:
                file_list.append(os.path.join(path,f_name)) #file_list.append(root + '/' + file)
    return file_list

def createXmlTree(file_list=None):
    if not file_list: file_list = []
    
    tree         = ET.ElementTree()
    root_elem    = ET.Element('wallpapers')
    contest_elem = _createContestXml_elem()
    root_elem.append(contest_elem)
    
    for file in file_list:
        
        try:
            file = unicode(file)
        except UnicodeDecodeError as e:
            print e
            continue
        
        fname = os.path.basename(file)
        
        # strip the filename extension
        name_split = fname.rpartition('.')
        if name_split[0]:
            name = name_split[0] # case: fname has extension
        else:
            name = name_split[2] # case: No extension in fname
            
        name = name.replace('_',' ') # replace '_' with whitespace
        wp_elem = _createWP_elem(name, file)
        root_elem.append(wp_elem)
    
    tree._setroot(root_elem)
    fo = open('/home/vipin/Pictures/Precise_Wallpapers/test.xml', "w")
    tree.write(fo, encoding="UTF-8")
    fo.close()
    
    

if __name__ == '__main__':
    path = '/usr/share/backgrounds/'
    try:
        list = getFiles(path)
        createXmlTree(list)
    except Exception as e:
        print e
        sys.exit(-1)
