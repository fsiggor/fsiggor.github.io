# Manjaro Post-Install

1. **Update system**
- `sudo pacman -Syyuu`
2. **yay**
- Install `sudo pacman -S yay`
3. **Bitwarden**
- Install `yay -S bitwarden` 
4. **NordVPN**
- Install `yay -S nordvpn-bin`
- Enable `systemctl enable nordvpn`
- Start `systemctl start nordvpn`
- Add user `sudo usermod -aG nordvpn $USER`
- Reboot `reboot`
- Authenticate `nordvpn login`
- Connect to VPN `nordvpn connect`
- Set Autoconnect `nordvpn set autoconnect on`
- Disable IPV6
5. **btrfs Timeshift**
- Install `yay -S timeshift`
6. **SSH and GnuPG**
- Install openSSH `yay -S openssh`
- Install GnuPG `yay -S gnupg`
- Import or create keys
7. **Browser**
- Firefox `yay -S firefox`
