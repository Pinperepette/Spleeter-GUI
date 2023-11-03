#!/usr/bin/env python
import wx
import os
from spleeter.separator import Separator
import threading

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(400, 400))
        
        self.panel = wx.Panel(self)
        self.file_label = wx.StaticText(self.panel, label="Select File Path:")
        self.folder_label = wx.StaticText(self.panel, label="Select Output Folder:")
        
        self.file_text = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        self.folder_text = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        
        self.file_button = wx.Button(self.panel, label="Browse")
        self.Bind(wx.EVT_BUTTON, self.on_select_file, self.file_button)
        
        self.folder_button = wx.Button(self.panel, label="Browse")
        self.Bind(wx.EVT_BUTTON, self.on_select_folder, self.folder_button)
        
        options = ["Voice", "Instruments"]
        self.option_label = wx.StaticText(self.panel, label="Choose Voice or Instruments:")
        self.option_choice = wx.Choice(self.panel, choices=options)
        
        self.split_button = wx.Button(self.panel, label="Split")
        self.Bind(wx.EVT_BUTTON, self.on_split, self.split_button)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.file_label, 0, wx.ALL, 10)
        self.sizer.Add(self.file_text, 0, wx.EXPAND | wx.ALL, 10)
        self.sizer.Add(self.file_button, 0, wx.ALL, 10)
        self.sizer.Add(self.folder_label, 0, wx.ALL, 10)
        self.sizer.Add(self.folder_text, 0, wx.EXPAND | wx.ALL, 10)
        self.sizer.Add(self.folder_button, 0, wx.ALL, 10)
        self.sizer.Add(self.option_label, 0, wx.ALL, 10)
        self.sizer.Add(self.option_choice, 0, wx.ALL, 10)
        self.sizer.Add(self.split_button, 0, wx.ALL | wx.ALIGN_RIGHT, 10)
        
        self.panel.SetSizer(self.sizer)
        self.Centre()

    def on_select_file(self, event):
        file_dialog = wx.FileDialog(self, "Select a file", wildcard="Audio files (*.mp3;*.wav)|*.mp3;*.wav", style=wx.FD_OPEN)
        if file_dialog.ShowModal() == wx.ID_OK:
            file_path = file_dialog.GetPath()
            self.file_text.SetValue(file_path)
        file_dialog.Destroy()

    def on_select_folder(self, event):
        folder_dialog = wx.DirDialog(self, "Select an output folder", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if folder_dialog.ShowModal() == wx.ID_OK:
            folder_path = folder_dialog.GetPath()
            self.folder_text.SetValue(folder_path)
        folder_dialog.Destroy()

    def on_split(self, event):
        file_path = self.file_text.GetValue()
        folder_path = self.folder_text.GetValue()
        option = self.option_choice.GetStringSelection()
        if file_path and folder_path and option:
            option_spleeter = '2stems' if option == 'Voice' else '5stems'
            threading.Thread(target=self.split_audio, args=(file_path, folder_path, option_spleeter)).start()

    def split_audio(self, file_path, folder_path, option_spleeter):
        try:
            separator = Separator(f'spleeter:{option_spleeter}')
            separator.separate_to_file(file_path, folder_path)
            wx.CallAfter(wx.MessageBox, f"Split '{os.path.basename(file_path)}' into '{option_spleeter}' in folder '{folder_path}'", "Operation Completed", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.CallAfter(wx.MessageBox, f"Error during separation: {e}", "Error", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, "Spleeter GUI")
    frame.SetBackgroundColour('#272822')
    frame.Show()
    app.MainLoop()
