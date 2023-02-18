# Manjaro Post-Install

1. **Update system**
- `sudo pacman -Syyuu`
- `sudo pacman -S base-devel`

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

8. **Neovim**
- Install `yay -S neovim`

9. **Tmux**
- Install `yay -S tmux`

10. **Docker and docker-compose**
- Install docker `yay -S docker`
- Add user `sudo usermod -aG docker $USER`
- Reboot ``reboot`
- Install docker-compose `yay -S docker-compose`

11. **asdf**
- Install `yay -S asdf-vm`
- Enable `echo ". /opt/asdf-vm/asdf.sh" >> ~/.zshrc` and reload
- Add golang
- Add nodejs
- Add awscli
- Add gcloud

12. **Git**
- Install `yay -S git`

13. **ZSH**
- Install `yay -S zsh`

14. **Twingate**

15. **Sparrow Wallet**
- Install `yay -S sparrow-wallet`

16. **BISQ**
- Install `yay -S bisq-bin`
