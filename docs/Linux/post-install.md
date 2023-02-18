# Manjaro Post-Install

1. **Update system**
- `sudo pacman -Syyuu`
2. **yay**
- Install `sudo pacman -S yay`
3. **Bitwarden**
- Install `yay -S bitwarden` 
4. **NordVPN**
- Install `yay -S nordvpn-bin`
- Add user `sudo usermod -aG nordvpn $USER`
- Reboot `reboot`
- Authenticate `nordvpn login`
- Connect to VPN `nordvpn connect`
5. **Disable IPV6**
6. **Install Browsers**
- Firefox `yay -S firefox`
- Tor `yay -S tor`

