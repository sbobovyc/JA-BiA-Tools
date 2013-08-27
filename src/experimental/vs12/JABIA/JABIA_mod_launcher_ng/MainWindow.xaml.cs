/*
Copyright (C) 2013 Stanislav Bobovych

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
*/

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using DllInjection;

namespace JABIA_mod_launcher_ng
{
    enum GameVersion { JABIA, JAC, UNKNOWN };

    public class Mod
    {
        public string dllName;
        public string modPath;
        public bool enabled;

        public void init(string path)
        {
            modPath = path;
            dllName = System.IO.Path.GetFileName(path);
            //Check for missing dll name
        }

    }

    public class Settings
    {
        public String version = "1.01";
        public List<Mod> mods = new List<Mod>();
        public List<string> modPaths;       
    }

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        Settings settings;
        const string LAUNCHER_SETTINGS = @".\mods\JABIA_mod_launcher.xml";
        const string JABIA_LAUNCHER = "JaggedAllianceBIA.exe";
        const string JAC_LAUNCHER = "JaggedAllianceCF.exe";
        const string JABIA_PROCESS = "GameJABiA";
        const string JAC_PROCESS = "GameJACrossfire";
        

        public Settings Load()
        {
            System.Xml.Serialization.XmlSerializer reader =
                new System.Xml.Serialization.XmlSerializer(typeof(Settings));
            try
            {
                System.IO.StreamReader file = new System.IO.StreamReader(LAUNCHER_SETTINGS);
                Settings settings = (Settings)reader.Deserialize(file);
                file.Close();
                return settings;
            }
            catch (System.IO.FileNotFoundException e)
            {
                return new Settings();
            }
            
        }

        public void Save()
        {
            System.Xml.Serialization.XmlSerializer writer =
            new System.Xml.Serialization.XmlSerializer(typeof(Settings));
            System.IO.StreamWriter file = new System.IO.StreamWriter(LAUNCHER_SETTINGS);
            writer.Serialize(file, settings);
            file.Close();
        }

        public MainWindow()
        {
            InitializeComponent();
            settings = Load();
            LogTexBox.AppendText("Version " + settings.version);
            GameVersion version = GetGameVersion();
            if (version == GameVersion.JABIA)
            {
                LogTexBox.AppendText(" (BIA)");
            }
            else if (version == GameVersion.JAC)
            {
                LogTexBox.AppendText(" (CF)");
            }
            else
            {
                LogTexBox.AppendText("\nMissing game launcher. Make sure mod launcher is installed in correct directory.");
                LaunchButton.IsEnabled = false;
            }
            foreach (Mod mod in settings.mods)
            {
                System.Diagnostics.Debug.WriteLine(mod.dllName);
                AddModToView(mod);
            }

        }

        private GameVersion GetGameVersion()
        {
            string[] game = System.IO.Directory.GetFiles(".", JABIA_LAUNCHER);
            if (game.Length == 1)
            {
                System.Diagnostics.Debug.WriteLine(System.IO.Path.GetFileName(game[0]));
                return GameVersion.JABIA;
            }
            game = System.IO.Directory.GetFiles(".", JAC_LAUNCHER);
            if (game.Length == 1)
            {
                System.Diagnostics.Debug.WriteLine(System.IO.Path.GetFileName(game[0]));
                return GameVersion.JAC;
            }
            return GameVersion.UNKNOWN;
        }

        private void injectMods()
        {
            GameVersion version = GetGameVersion();
            string ProcName = "";
            string LauncherName ="";

            ModListBox.Dispatcher.Invoke((Action)delegate
            {
                ModListBox.IsEnabled = false;
            });

            if (version == GameVersion.JABIA)
                System.Diagnostics.Process.Start(JABIA_LAUNCHER);
            else
                System.Diagnostics.Process.Start(JAC_LAUNCHER);

            if (version == GameVersion.JABIA)
            {                
                LaunchButton.Dispatcher.Invoke((Action)delegate
                {
                    LogTexBox.AppendText("\nWaiting for proces to start: " + JABIA_PROCESS);
                });
                ProcName = JABIA_PROCESS;
                LauncherName = JABIA_LAUNCHER;
            }
            if (version == GameVersion.JAC)
            {                
                LaunchButton.Dispatcher.Invoke((Action)delegate
                {
                    LogTexBox.AppendText("\nWaiting for proces to start: " + JAC_PROCESS);
                });
                ProcName = JAC_PROCESS;
                LauncherName = JAC_LAUNCHER;
            }
            
            
            LaunchButton.Dispatcher.Invoke((Action)delegate
            {
                LaunchButton.IsEnabled = false;
            });

            if (settings.mods.Count != 0)
            {
                bool procFound = false;
                for(int i = 0; i < 10; i++)
                {
                    Process[] _procs = Process.GetProcesses();
                    for (int j = 0; j < _procs.Length; j++)
                    {
                        if (_procs[j].ProcessName == ProcName)
                        {
                            procFound = true;
                            break;
                        }
                    }
                    if (procFound)
                        break;
                    System.Threading.Thread.Sleep(500);
                }
                if (!procFound)
                {
                    LaunchButton.Dispatcher.Invoke((Action)delegate
                    {
                        LogTexBox.AppendText("\nProcess not found. Exiting");
                    });
                    System.Threading.Thread.Sleep(1000);
                    Process.GetCurrentProcess().Kill(); //TODO nasty, fix
                }
                
                DllInjector inj = DllInjector.GetInstance;
                foreach (Mod mod in settings.mods)
                {
                    if (mod.enabled)
                    {
                        LaunchButton.Dispatcher.Invoke((Action)delegate
                        {
                            LogTexBox.AppendText("\nInjecting " + mod.modPath);
                        });
                        DllInjectionResult result = inj.Inject(ProcName, mod.modPath);
                    }
                }
                
            }
            System.Threading.Thread.Sleep(1000);
            Process.GetCurrentProcess().Kill(); //TODO nasty, fix
        }

        private Mod AddModToModel(string file)
        {
            bool modAlreadyAdded = false;
            Mod mod = new Mod();
            mod.init(file);
            mod.enabled = true;
            //TODO check for duplicate mods
            foreach (Mod addedMod in this.settings.mods)
            {
                if (mod.dllName == addedMod.dllName)
                    modAlreadyAdded = true;
            }

            if (!modAlreadyAdded)
            {
                this.settings.mods.Add(mod);
                return mod;
            }
            else
            {
                return null;
            }
        }

        private void AddModToView(Mod mod)
        {
            CheckBox cb = new CheckBox();
            cb.IsChecked = mod.enabled;
            cb.Content = mod.dllName;
            cb.Click += new RoutedEventHandler(CheckBox_CheckedChanged);
            ModListBox.Items.Add(cb);
        }

        private void AddModFromGUI()
        {
            // show file chooser
            // get path 
            // create new mod
                        // Create an instance of the open file dialog box.
            System.Windows.Forms.OpenFileDialog openFileDialog1 = new System.Windows.Forms.OpenFileDialog();

            // Set filter options and filter index.
            openFileDialog1.Filter = "DLL Files (.dll)|*.dll|All Files (*.*)|*.*";
            openFileDialog1.FilterIndex = 1;

            openFileDialog1.Multiselect = false;

            // Call the ShowDialog method to show the dialog box.
            System.Windows.Forms.DialogResult result = openFileDialog1.ShowDialog();

            // Process input if the user clicked OK.
            if (result == System.Windows.Forms.DialogResult.OK)
            {
                // change model
                Mod mod = AddModToModel(openFileDialog1.FileName);                

                // change view
                if(mod != null)
                    AddModToView(mod);
 
            }
        }

        private void RemoveModFromModel(string dllName)
        {
            int i = 0;
            System.Diagnostics.Debug.WriteLine(dllName);
            foreach (Mod mod in settings.mods)
            {
                if (mod.dllName == dllName)
                {
                    break;
                }
                i++;
            }
            settings.mods.RemoveAt(i);
        }

        private void RemoveModFromGUI()
        {            
            System.Diagnostics.Debug.WriteLine(ModListBox.SelectedItem);
            CheckBox cb = (CheckBox)ModListBox.SelectedItem;
            ModListBox.Items.Remove(ModListBox.SelectedItem); 
            if(cb != null)
                RemoveModFromModel(cb.Content.ToString());
            
        }

        private void DisableMod(string dllName)
        {
            int i = 0;
            System.Diagnostics.Debug.WriteLine(dllName);
            foreach (Mod mod in settings.mods)
            {                
                if (mod.dllName == dllName)
                {
                    settings.mods[i].enabled = false;
                }
                i++;
            }
        }

        private void EnableMod(string dllName)
        {
            int i = 0;
            System.Diagnostics.Debug.WriteLine(dllName);
            foreach (Mod mod in settings.mods)
            {
                if (mod.dllName == dllName)
                {
                    settings.mods[i].enabled = true;
                }
                i++;
            }
        }

        private void Button_Click_Launch(object sender, RoutedEventArgs e)
        {            
            Save();
        
            System.Threading.Thread t = new System.Threading.Thread(new System.Threading.ThreadStart(injectMods));
            t.SetApartmentState(System.Threading.ApartmentState.STA);
            t.Start();                   
        }

        private void Button_Click_AddMod(object sender, RoutedEventArgs e)
        {
            AddModFromGUI();
        }

        private void Button_Click_RemoveMod(object sender, System.Windows.RoutedEventArgs e)
        {
            RemoveModFromGUI();         
        }

        protected void CheckBox_CheckedChanged(object sender, EventArgs e)
        {
            CheckBox cb = (CheckBox)sender;
            if (cb.IsChecked == false)
            {
                DisableMod(((CheckBox)sender).Content.ToString());
            }
            else 
            {
                EnableMod(((CheckBox)sender).Content.ToString());
            }
        }

        private void Hyperlink_RequestNavigate(object sender, System.Windows.Navigation.RequestNavigateEventArgs e)
        {
            System.Diagnostics.Process.Start(e.Uri.AbsoluteUri);
        }
    }
}
