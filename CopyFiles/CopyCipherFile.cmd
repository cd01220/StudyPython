@echo off
cd /D %~dp0%
set /p password="openssl password: "
set /p uid="gnupg uid: "
CopyCipherFile.py "C:\Users\LiuHao\AppData\Roaming\Electrum\wallets\default_wallet" "D:\MyDoc\MySecurityData\Xxx2016.gpg" %password% %uid%
