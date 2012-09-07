"""
Created on July 2, 2012

@author: sbobovyc
"""
"""
Copyright (C) 2012 Stanislav Bobovych

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
#http://wiki.wxpython.org/ProportionalSplitterWindow
#http://wiki.wxpython.org/index.cgi/ModelViewController
#http://wiki.wxpython.org/Controlling%20GUI%20with%20pubsub

import os
import wx

from wx.lib.pubsub import pub

from cui_file import CUI_file

class Model(object):
    def __init__(self):
        self.cui_filepath = ""

    def openCUI(self, filepath):
        self.cui_filepath = filepath
        print self.cui_filepath
        self.CUI = CUI_file(filepath)
        #now tell anyone who cares that the value has been changed
        pub.sendMessage("CUI.LOADED", message=self.CUI)

class Controller(object):
    def __init__(self, app):
        # create model
        self.model = Model()

        self.mainFrame = MainFrame(None, -1, 'JABIA Tools Editor (CUI ed)')
        self.createMenubar()
        
        # create splitter
        self.split1 = ProportionalSplitter(self.mainFrame,-1, 0.35)

        # create controls to go in the splitter windows...
        self.panel_tree = wx.Panel (self.split1)
        self.panel_work = wx.Panel (self.split1)
        # add your controls to the splitters:
        self.split1.SplitVertically(self.panel_tree, self.panel_work)
        
        #self.panel_work.SetBackgroundColour("blue") #debug only

        # initialize tree
        #self.tree = wx.TreeCtrl(self.panel_tree, 1, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        self.tree = wx.TreeCtrl(self.panel_tree, 1, wx.DefaultPosition, (-1,-1), wx.TR_HAS_BUTTONS)
        
        # make the tree fill the panel
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.tree, 1, wx.EXPAND)
        hbox.Add(self.panel_tree, 1, wx.EXPAND)       
        self.panel_tree.SetSizer(vbox)

        # center 
        self.mainFrame.Centre()
        
        # bind events
        self.mainFrame.Bind(wx.EVT_MENU, self.OnOpen, self.fileMenu.openItem)
        self.mainFrame.Bind(wx.EVT_MENU, self.OnQuit, self.fileMenu.quitItem)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)
        pub.subscribe(self.CreateTree, 'CUI.LOADED')

        self.mainFrame.Show()
        
    def createMenubar(self):
        self.menubar = wx.MenuBar()
        self.fileMenu = FileMenu()
        self.helpMenu = HelpMenu()
        self.menubar.Append(self.fileMenu, '&File')
        self.menubar.Append(self.helpMenu, '&Help')
        self.mainFrame.SetMenuBar(self.menubar)

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
            
    def OnSelChanged(self, event):
        item =  event.GetItem()
        print item
        data = self.tree.GetItemData(item).GetData()
        print data
        # clear panel
        for child in self.panel_work.GetChildren():
            child.Destroy() 
#        self.display = wx.StaticText(self.panel_work, -1, '',(10,10), style=wx.ALIGN_CENTRE)
#        self.display.SetLabel(data.path)
        print data.__class__.__name__
        
        if data.__class__.__name__ == "CTX_ID": 
            CTX_ID_Panel(self.panel_work, data)
        elif data.__class__.__name__ == "CUI_ui_icon":
            print 'here'

    def CreateTree(self, message):
        root = self.tree.AddRoot('JABIA')
        cui_item = self.tree.AppendItem(root, 'CUI')
        ctx_tree = self.tree.AppendItem(cui_item, 'CTX')
        sound_tree = self.tree.AppendItem(cui_item, 'sounds')
        font_tree = self.tree.AppendItem(cui_item, 'fonts')
        ui_file_tree = self.tree.AppendItem(cui_item, 'ui files')
        ui_icon_tree = self.tree.AppendItem(cui_item, 'ui icons')
        
        # open cui file
        CUI = message
        CUI.open()
        CUI.unpack(verbose=False)
        # populate ctx ids
        for ctx_id in CUI.data.ctx_id_list:
            item = self.tree.AppendItem(ctx_tree, ctx_id.id_name)
            self.tree.SetItemData(item, wx.TreeItemData(ctx_id))
        # populate sounds
        for sound_id in CUI.data.sound_list:
            self.tree.AppendItem(sound_tree, sound_id.filename)
        # populate fonts
        for font_id in CUI.data.font_list:
            self.tree.AppendItem(font_tree, font_id.font_name)
        # populate ui files
        for ui_file_id in CUI.data.ui_resource_dict:
            self.tree.AppendItem(ui_file_tree, CUI.data.ui_resource_dict[ui_file_id].filename)
        # populate ui icons
        for ui_icon_id in CUI.data.ui_icon_dict:
            item = self.tree.AppendItem(ui_icon_tree, str(CUI.data.ui_icon_dict[ui_icon_id].icon_id))
            self.tree.SetItemData(item, wx.TreeItemData(CUI.data.ui_icon_dict[ui_icon_id]))
            
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

class ProportionalSplitter(wx.SplitterWindow):
        def __init__(self,parent, id = -1, proportion=0.66, size = wx.DefaultSize, **kwargs):
                wx.SplitterWindow.__init__(self,parent,id,wx.Point(0, 0),size, **kwargs)
                self.SetMinimumPaneSize(50) #the minimum size of a pane.
                self.proportion = proportion
                if not 0 < self.proportion < 1:
                        raise ValueError, "proportion value for ProportionalSplitter must be between 0 and 1."
                self.ResetSash()
                self.Bind(wx.EVT_SIZE, self.OnReSize)
                self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSashChanged, id=id)
                ##hack to set sizes on first paint event
                self.Bind(wx.EVT_PAINT, self.OnPaint)
                self.firstpaint = True

        def SplitHorizontally(self, win1, win2):
                if self.GetParent() is None: return False
                return wx.SplitterWindow.SplitHorizontally(self, win1, win2,
                        int(round(self.GetParent().GetSize().GetHeight() * self.proportion)))

        def SplitVertically(self, win1, win2):
                if self.GetParent() is None: return False
                return wx.SplitterWindow.SplitVertically(self, win1, win2,
                        int(round(self.GetParent().GetSize().GetWidth() * self.proportion)))

        def GetExpectedSashPosition(self):
                if self.GetSplitMode() == wx.SPLIT_HORIZONTAL:
                        tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().height)
                else:
                        tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().width)
                return int(round(tot * self.proportion))

        def ResetSash(self):
                self.SetSashPosition(self.GetExpectedSashPosition())

        def OnReSize(self, event):
                "Window has been resized, so we need to adjust the sash based on self.proportion."
                self.ResetSash()
                event.Skip()

        def OnSashChanged(self, event):
                "We'll change self.proportion now based on where user dragged the sash."
                pos = float(self.GetSashPosition())
                if self.GetSplitMode() == wx.SPLIT_HORIZONTAL:
                        tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().height)
                else:
                        tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().width)
                self.proportion = pos / tot
                event.Skip()

        def OnPaint(self,event):
                if self.firstpaint:
                        if self.GetSashPosition() != self.GetExpectedSashPosition():
                                self.ResetSash()
                        self.firstpaint = False
                event.Skip()

class CTX_ID_Panel(wx.Panel):
    def __init__(self, parent, CTX_ID_object):
        wx.Panel.__init__(self, parent)
        self.ctx_id_object = CTX_ID_object        
        
        # build gui
        self.id_text = wx.StaticText(self, label="CTX id:")
        self.id = wx.TextCtrl(self, -1, "", size=wx.Size(30, -1))
        self.path_text = wx.StaticText(self, label="Path:")        
        self.path = wx.TextCtrl(self, -1, "", size=wx.Size(250, -1)) 
        sizer = wx.GridBagSizer(5, 5)
        sizer.Add(self.id_text, (0,0))
        sizer.Add(self.id, (0,1))
        sizer.Add(self.path_text, (1,0))
        sizer.Add(self.path, (1,1))
        self.SetSizer(sizer)
        self.updateView()
        
    def updateView(self):
        self.id.WriteText(str(self.ctx_id_object.id))
        self.path.WriteText(str(self.ctx_id_object.path))
        self.Fit()
        
class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(600, 400))
            
if __name__ == "__main__":
    app = wx.App(False)
    controller = Controller(app)
    app.MainLoop()
