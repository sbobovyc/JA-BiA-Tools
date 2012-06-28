# first line below is necessary only in wxPython 2.8.11.0 since default 
# API in this wxPython is pubsub version 1 (expect later versions 
# of wxPython to use the kwargs API by default)

from pubsub import setupkwargs

# regular pubsub import
from pubsub import pub

import wx

########################################################################
class OtherFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Secondary Frame")
        panel = wx.Panel(self)
 
        msg = "Enter a Message to send to the main frame"
        instructions = wx.StaticText(panel, label=msg)
        self.msgTxt = wx.TextCtrl(panel, value="")
        closeBtn = wx.Button(panel, label="Send and Close")
        closeBtn.Bind(wx.EVT_BUTTON, self.onSendAndClose)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        flags = wx.ALL|wx.CENTER
        sizer.Add(instructions, 0, flags, 5)
        sizer.Add(self.msgTxt, 0, flags, 5)
        sizer.Add(closeBtn, 0, flags, 5)
        panel.SetSizer(sizer)
 
    #----------------------------------------------------------------------
    def onSendAndClose(self, event):
        """
        Send a message and close frame
        """
        msg = self.msgTxt.GetValue()
        pub.sendMessage("show.mainframe", data=msg)
        self.Close()
 
 
########################################################################
class MainPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
 
        pub.subscribe(self.showFrame, "show.mainframe")
 
        self.pubsubText = wx.TextCtrl(self, value="")
        hideBtn = wx.Button(self, label="Hide")
        hideBtn.Bind(wx.EVT_BUTTON, self.hideFrame)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.pubsubText, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(hideBtn, 0, wx.ALL|wx.CENTER, 5)
        self.SetSizer(sizer)
 
    #----------------------------------------------------------------------
    def hideFrame(self, event):
        """"""
        self.frame.Hide()
        new_frame = OtherFrame()
        new_frame.Show()
 
    #----------------------------------------------------------------------
    def showFrame(self, data):
        """
        Shows the frame and shows the message sent in the
        text control
        """
        self.pubsubText.SetValue(data)
        frame = self.GetParent()
        frame.Show()
 
########################################################################
class MainFrame(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Pubsub Tutorial")
        panel = MainPanel(self)
 
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
