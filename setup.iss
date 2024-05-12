[Setup]
AppName=Facebook Tab On Multi Google Chrome Profile
AppVersion=1.0
DefaultDirName={pf}\
DefaultGroupName=Develop by Mr.HUN
UninstallDisplayIcon={app}\fb_chrome_tab.exe
Compression=lzma
SolidCompression=yes
OutputDir=Output

[Files]
Source: "dist\main.exe"; DestDir: "{app}"
Source: "image.ico"; DestDir: "{app}"
Source: "chromedriver.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\fb_chrome_tab"; Filename: "{app}\fb_chrome_tab.exe"
