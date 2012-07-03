import os
import wx

from wx.lib.pubsub import Publisher as pub

from cui_file import CUI_file

class Model(object):
    def __init__(self):
        self.cui_filepath = ""

    def openCUI(self, filepath):
        self.cui_filepath = filepath
        print self.cui_filepath
        self.CUI = CUI_file(filepath)
        #now tell anyone who cares that the value has been changed
        pub.sendMessage("CUI LOADED", data=self.CUI)

class Controller(object):
    def __init__(self, app):
        # create model
        self.model = Model()

        self.mainFrame = MainFrame(None, -1, 'JABIA Tools Editor (CUI ed)')

        self.menubar = wx.MenuBar()
        self.fileMenu = FileMenu()
        self.helpMenu = HelpMenu()
        self.menubar.Append(self.fileMenu, '&File')
        self.menubar.Append(self.helpMenu, '&Help')
        self.mainFrame.SetMenuBar(self.menubar)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        # create panels
        self.panel_tree = wx.Panel(self.mainFrame)
        self.panel_work = wx.Panel(self.mainFrame)

        # initialize tree
        #self.tree = wx.TreeCtrl(self.panel_tree, 1, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        self.tree = wx.TreeCtrl(self.panel_tree, 1, wx.DefaultPosition, (-1,-1), wx.TR_HAS_BUTTONS)
        
        # set the look of main frame
        vbox.Add(self.tree, 1, wx.EXPAND)
        hbox.Add(self.panel_tree, 1, wx.EXPAND)
        hbox.Add(self.panel_work, 1, wx.EXPAND)        
        self.panel_tree.SetSizer(vbox)
        self.mainFrame.SetSizer(hbox)
        self.mainFrame.Centre()
        
        # bind events
        self.mainFrame.Bind(wx.EVT_MENU, self.OnOpen, self.fileMenu.openItem)
        self.mainFrame.Bind(wx.EVT_MENU, self.OnQuit, self.fileMenu.quitItem)
        pub.subscribe(self.CreateTree, 'CUI LOADED')

        self.mainFrame.Show()
        
    def get_item_by_label(self, tree, search_text, root_item):
        item, cookie = tree.GetFirstChild(root_item)

        while item.IsOk():
            text = tree.GetItemText(item)
            if text.lower() == search_text.lower():
                return item
            if tree.ItemHasChildren(item):
                match = self.get_item_by_label(tree, search_text, item)
                if match.IsOk():
                    return match
            item, cookie = tree.GetNextChild(root_item, cookie)

        return wx.TreeItemId()
        
    def OnQuit(self, event):
        self.mainFrame.Close()

    def OnOpen(self,e):
            """ Open a file"""
            self.dirname = ''
            dlg = wx.FileDialog(self.mainFrame, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                filepath = os.path.join(self.dirname, self.filename)
                self.model.openCUI(filepath)
            dlg.Destroy()

    def CreateTree(self, message):
        root = self.tree.AddRoot('JABIA')
        cui_item = self.tree.AppendItem(root, 'CUI')
        ctx_tree = self.tree.AppendItem(cui_item, 'CTX')
        sound_tree = self.tree.AppendItem(cui_item, 'sounds')
        font_tree = self.tree.AppendItem(cui_item, 'fonts')
        ui_file_tree = self.tree.AppendItem(cui_item, 'ui files')
        
        # open cui file
        CUI = message.data
        CUI.open()
        CUI.unpack(verbose=False)
        # populate ctx ids
        for ctx_id in CUI.data.ctx_id_list:
            self.tree.AppendItem(ctx_tree, ctx_id.id_name)
        # populate sounds
        for sound_id in CUI.data.sound_list:
            self.tree.AppendItem(sound_tree, sound_id.filename)
        # populate fonts
        for font_id in CUI.data.font_list:
            self.tree.AppendItem(font_tree, font_id.font_name)
        # populate ui files
        for ui_file_id in CUI.data.ui_resource_dict:
            self.tree.AppendItem(ui_file_tree, CUI.data.ui_resource_dict[ui_file_id].filename)
            
        self.tree.Expand(root)
        self.tree.Expand(cui_item)        
        self.tree.Expand(ctx_tree)




class HelpMenu(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)
        self.aboutItem = self.Append(wx.ID_ABOUT, 'About', '')        
        
class FileMenu(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)
        self.openItem = self.Append(wx.ID_OPEN, 'Open', 'Open file')
        self.quitItem = self.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        
class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(450, 350))
            
if __name__ == "__main__":
    app = wx.App(False)
    controller = Controller(app)
    app.MainLoop()
