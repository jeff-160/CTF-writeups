// Decompiled with JetBrains decompiler
// Type: ChooseOrDieWPF.MainWindow
// Assembly: ChooseOrDieWPF, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null
// MVID: E95DEF73-2EA7-40CB-8571-A258952664BC
// Assembly location: ChooseOrDieWPF.dll inside C:\Users\jeff-160\Documents\lnc\ChooseOrDie-Game\ChooseOrDie-Game\ChooseOrDie.exe)

using System;
using System.CodeDom.Compiler;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Markup;

#nullable disable
namespace ChooseOrDieWPF;

public class MainWindow : Window, IComponentConnector
{
  private string[] messages = new string[16 /*0x10*/]
  {
    "Are you Wibu-san?",
    "绝不会放弃你",
    "Nu te voi dezamăgi niciodată",
    "कहियो दौड़ैत-दौड़ैत अहाँकेँ छोड़ि नहि देब",
    "ፈጺሙ ከብክየካ ኣይክእልን እዩ።",
    "Nikdy neřeknu sbohem",
    "Ná inseoidh tú bréag agus ní ghortóidh sé thú",
    "Sauve-moi juste",
    "あなたはウィブさんですよね？",
    "צפית בסרט 'בחר או למות'?",
    "Are you a Vozer?",
    "550 : 2 = 225",
    "ПОМИЛКА!!",
    "Your KEY is:",
    "Sən axmaqsan",
    "ນີ້ບໍ່ແມ່ນກຸນແຈຄືກັນ"
  };
  internal Button PlayButton;
  internal Button DieButton;
  private bool _contentLoaded;

  public MainWindow() => this.InitializeComponent();

  private void PlayButton_Click(object sender, RoutedEventArgs e)
  {
    byte[] numArray = new byte[16 /*0x10*/]
    {
      (byte) 65,
      (byte) 16 /*0x10*/,
      (byte) 15,
      (byte) 140,
      (byte) 70,
      (byte) 198,
      (byte) 150,
      (byte) 54,
      (byte) 70,
      (byte) 142,
      (byte) 79,
      (byte) 122,
      (byte) 40,
      (byte) 70,
      (byte) 149,
      (byte) 167
    };
    byte[] buffer = new byte[0];
    for (int index = 0; index < 16 /*0x10*/; ++index)
    {
      MessageBoxResult messageBoxResult = MessageBox.Show(this.messages[index], "Challenge", MessageBoxButton.YesNo);
      buffer = Enumerable.ToArray<byte>(Enumerable.Append<byte>((IEnumerable<byte>) buffer, (byte) messageBoxResult));
    }
    using (Aes aes = Aes.Create())
    {
      if (string.op_Inequality(Convert.ToBase64String(MD5.Create().ComputeHash(buffer)), "LNSg2cOUwwiVgmq4nKdWBA=="))
      {
        int num = (int) MessageBox.Show("No luck for you today!", "DIE", MessageBoxButton.OK);
        this.Close();
      }
      else
      {
        aes.Key = buffer;
        aes.IV = numArray;
        ICryptoTransform decryptor = aes.CreateDecryptor(aes.Key, aes.IV);
        using (MemoryStream memoryStream1 = new MemoryStream(MainWindow.StringToByteArray("1e6debd445633aeab5531ecf5ea816275ac8483071ca023085a46e8d547c4ba976bf2c581547624695500522a1e449f6af732fb3c52005e1bb61c3480a584d64")))
        {
          using (CryptoStream cryptoStream = new CryptoStream((Stream) memoryStream1, decryptor, CryptoStreamMode.Read))
          {
            using (MemoryStream memoryStream2 = new MemoryStream())
            {
              cryptoStream.CopyTo((Stream) memoryStream2);
              int num = (int) MessageBox.Show(Encoding.UTF8.GetString(memoryStream2.ToArray()), "Congratulations!", MessageBoxButton.OK);
            }
          }
        }
      }
    }
  }

  private void DieButton_Click(object sender, RoutedEventArgs e) => this.Close();

  public static byte[] StringToByteArray(string hex)
  {
    return Enumerable.ToArray<byte>(Enumerable.Select<int, byte>(Enumerable.Where<int>(Enumerable.Range(0, hex.Length), (Func<int, bool>) (x => x % 2 == 0)), (Func<int, byte>) (x => Convert.ToByte(hex.Substring(x, 2), 16 /*0x10*/))));
  }

  [DebuggerNonUserCode]
  [GeneratedCode("PresentationBuildTasks", "7.0.20.0")]
  public void InitializeComponent()
  {
    if (this._contentLoaded)
      return;
    this._contentLoaded = true;
    Application.LoadComponent((object) this, new Uri("/ChooseOrDieWPF;component/mainwindow.xaml", (UriKind) 2));
  }

  [DebuggerNonUserCode]
  [GeneratedCode("PresentationBuildTasks", "7.0.20.0")]
  [EditorBrowsable]
  void IComponentConnector.Connect(int connectionId, object target)
  {
    if (connectionId != 1)
    {
      if (connectionId == 2)
      {
        this.DieButton = (Button) target;
        this.DieButton.Click += new RoutedEventHandler(this.DieButton_Click);
      }
      else
        this._contentLoaded = true;
    }
    else
    {
      this.PlayButton = (Button) target;
      this.PlayButton.Click += new RoutedEventHandler(this.PlayButton_Click);
    }
  }
}
