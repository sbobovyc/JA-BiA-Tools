#!/usr/bin/python

# treectrl.py

import wx

class MyPopupMenu(wx.Menu):
    
    def __init__(self, parent):
        super(MyPopupMenu, self).__init__()
        
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Minimize')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnMinimize, mmi)

        cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        self.AppendItem(cmi)
        self.Bind(wx.EVT_MENU, self.OnClose, cmi)


    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, event):
        self.parent.Close()

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(450, 350))

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)



        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(self, -1)
        panel2 = wx.Panel(self, -1)

        self.tree = wx.TreeCtrl(panel1, 1, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        root = self.tree.AddRoot('Programmer')
        os = self.tree.AppendItem(root, 'Operating Systems')
        pl = self.tree.AppendItem(root, 'Programming Languages')
        tk = self.tree.AppendItem(root, 'Toolkits')
        self.tree.AppendItem(os, 'Linux')
        self.tree.AppendItem(os, 'FreeBSD')
        self.tree.AppendItem(os, 'OpenBSD')
        self.tree.AppendItem(os, 'NetBSD')
        self.tree.AppendItem(os, 'Solaris')
        cl = self.tree.AppendItem(pl, 'Compiled languages')
        sl = self.tree.AppendItem(pl, 'Scripting languages')
        self.tree.AppendItem(cl, 'Java')
        self.tree.AppendItem(cl, 'C++')
        self.tree.AppendItem(cl, 'C')
        self.tree.AppendItem(cl, 'Pascal')
        self.tree.AppendItem(sl, 'Python')
        self.tree.AppendItem(sl, 'Ruby')
        self.tree.AppendItem(sl, 'Tcl')
        self.tree.AppendItem(sl, 'PHP')
        self.tree.AppendItem(tk, 'Qt')
        self.tree.AppendItem(tk, 'MFC')
        self.tree.AppendItem(tk, 'wxPython')
        self.tree.AppendItem(tk, 'GTK+')
        self.tree.AppendItem(tk, 'Swing')
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)
        self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.RightClick, id=1)
        self.display = wx.StaticText(panel2, -1, '',(10,10), style=wx.ALIGN_CENTRE)
        vbox.Add(self.tree, 1, wx.EXPAND)
        hbox.Add(panel1, 1, wx.EXPAND)
        hbox.Add(panel2, 1, wx.EXPAND)
        panel1.SetSizer(vbox)
        self.SetSizer(hbox)
        self.Centre()

    def OnSelChanged(self, event):
        item =  event.GetItem()
        self.display.SetLabel(self.tree.GetItemText(item))

    def RightClick(self, event):
        item =  event.GetItem()
        #self.PopupMenu(MyPopupMenu(self), event.GetPosition())
        self.PopupMenu(MyPopupMenu(self))
        print self.tree.GetItemText(item)

    def OnQuit(self, event):
        self.Close()
    
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'treectrl.py')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()
