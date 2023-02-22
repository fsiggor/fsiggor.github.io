"use strict";(self.webpackChunkblog=self.webpackChunkblog||[]).push([[735],{3905:(e,t,a)=>{a.d(t,{Zo:()=>m,kt:()=>N});var n=a(7294);function l(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function r(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function i(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?r(Object(a),!0).forEach((function(t){l(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):r(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function o(e,t){if(null==e)return{};var a,n,l=function(e,t){if(null==e)return{};var a,n,l={},r=Object.keys(e);for(n=0;n<r.length;n++)a=r[n],t.indexOf(a)>=0||(l[a]=e[a]);return l}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(n=0;n<r.length;n++)a=r[n],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(l[a]=e[a])}return l}var p=n.createContext({}),s=function(e){var t=n.useContext(p),a=t;return e&&(a="function"==typeof e?e(t):i(i({},t),e)),a},m=function(e){var t=s(e.components);return n.createElement(p.Provider,{value:t},e.children)},k="mdxType",u={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},d=n.forwardRef((function(e,t){var a=e.components,l=e.mdxType,r=e.originalType,p=e.parentName,m=o(e,["components","mdxType","originalType","parentName"]),k=s(a),d=l,N=k["".concat(p,".").concat(d)]||k[d]||u[d]||r;return a?n.createElement(N,i(i({ref:t},m),{},{components:a})):n.createElement(N,i({ref:t},m))}));function N(e,t){var a=arguments,l=t&&t.mdxType;if("string"==typeof e||l){var r=a.length,i=new Array(r);i[0]=d;var o={};for(var p in t)hasOwnProperty.call(t,p)&&(o[p]=t[p]);o.originalType=e,o[k]="string"==typeof e?e:l,i[1]=o;for(var s=2;s<r;s++)i[s]=a[s];return n.createElement.apply(null,i)}return n.createElement.apply(null,a)}d.displayName="MDXCreateElement"},5097:(e,t,a)=>{a.r(t),a.d(t,{assets:()=>p,contentTitle:()=>i,default:()=>u,frontMatter:()=>r,metadata:()=>o,toc:()=>s});var n=a(7462),l=(a(7294),a(3905));const r={},i="Manjaro Post-Install",o={unversionedId:"OS/Manjaro Post-Install",id:"OS/Manjaro Post-Install",title:"Manjaro Post-Install",description:"1. Update system",source:"@site/docs/OS/Manjaro Post-Install.md",sourceDirName:"OS",slug:"/OS/Manjaro Post-Install",permalink:"/docs/OS/Manjaro Post-Install",draft:!1,editUrl:"https://github.com/fsiggor/fsiggor.github.io/tree/main/packages/create-docusaurus/templates/shared/docs/OS/Manjaro Post-Install.md",tags:[],version:"current",frontMatter:{},sidebar:"tutorialSidebar",previous:{title:"Intro",permalink:"/docs/OS/intro"},next:{title:"Windows Post-Install",permalink:"/docs/OS/Windows Post-Install"}},p={},s=[],m={toc:s},k="wrapper";function u(e){let{components:t,...a}=e;return(0,l.kt)(k,(0,n.Z)({},m,a,{components:t,mdxType:"MDXLayout"}),(0,l.kt)("h1",{id:"manjaro-post-install"},"Manjaro Post-Install"),(0,l.kt)("ol",null,(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"Update system"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"sudo pacman -Syyuu")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"sudo pacman -S base-devel"))),(0,l.kt)("ol",{start:2},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"yay"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install ",(0,l.kt)("inlineCode",{parentName:"li"},"sudo pacman -S yay"))),(0,l.kt)("ol",{start:3},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"preload"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S preload"))),(0,l.kt)("ol",{start:3},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"Bitwarden"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S bitwarden")," ")),(0,l.kt)("ol",{start:4},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"NordVPN"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S nordvpn-bin")),(0,l.kt)("li",{parentName:"ul"},"Enable ",(0,l.kt)("inlineCode",{parentName:"li"},"systemctl enable nordvpn")),(0,l.kt)("li",{parentName:"ul"},"Start ",(0,l.kt)("inlineCode",{parentName:"li"},"systemctl start nordvpn")),(0,l.kt)("li",{parentName:"ul"},"Add user ",(0,l.kt)("inlineCode",{parentName:"li"},"sudo usermod -aG nordvpn $USER")),(0,l.kt)("li",{parentName:"ul"},"Reboot ",(0,l.kt)("inlineCode",{parentName:"li"},"reboot")),(0,l.kt)("li",{parentName:"ul"},"Authenticate ",(0,l.kt)("inlineCode",{parentName:"li"},"nordvpn login")),(0,l.kt)("li",{parentName:"ul"},"Connect to VPN ",(0,l.kt)("inlineCode",{parentName:"li"},"nordvpn connect")),(0,l.kt)("li",{parentName:"ul"},"Set Autoconnect ",(0,l.kt)("inlineCode",{parentName:"li"},"nordvpn set autoconnect on")),(0,l.kt)("li",{parentName:"ul"},"Disable IPV6")),(0,l.kt)("ol",{start:5},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"btrfs Timeshift"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S timeshift"))),(0,l.kt)("ol",{start:6},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"SSH and GnuPG"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install openSSH ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S openssh")),(0,l.kt)("li",{parentName:"ul"},"Install GnuPG ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S gnupg")),(0,l.kt)("li",{parentName:"ul"},"Import or create keys")),(0,l.kt)("ol",{start:7},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"Browser"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Firefox ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S firefox"))),(0,l.kt)("ol",{start:8},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"Neovim"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S neovim"))),(0,l.kt)("ol",{start:9},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"Tmux"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S tmux"))),(0,l.kt)("ol",{start:10},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"Docker and docker-compose"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install docker ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S docker")),(0,l.kt)("li",{parentName:"ul"},"Add user ",(0,l.kt)("inlineCode",{parentName:"li"},"sudo usermod -aG docker $USER")),(0,l.kt)("li",{parentName:"ul"},"Reboot ",(0,l.kt)("inlineCode",{parentName:"li"},"reboot")),(0,l.kt)("li",{parentName:"ul"},"Install docker-compose ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S docker-compose"))),(0,l.kt)("ol",{start:11},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"asdf"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Install ",(0,l.kt)("inlineCode",{parentName:"p"},"yay -S asdf-vm"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Enable ",(0,l.kt)("inlineCode",{parentName:"p"},'echo ". /opt/asdf-vm/asdf.sh" >> ~/.zshrc')," and reload")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Add golang ",(0,l.kt)("inlineCode",{parentName:"p"},"asdf plugin add golang"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Install golang ",(0,l.kt)("inlineCode",{parentName:"p"},"asdf install golang latest"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Set golang ",(0,l.kt)("inlineCode",{parentName:"p"},"asdf global golang latest"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Add nodejs ",(0,l.kt)("inlineCode",{parentName:"p"},"asdf plugin add nodejs"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Install nodejs ",(0,l.kt)("inlineCode",{parentName:"p"},"asdf install nodejs lts"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Set nodejs ",(0,l.kt)("inlineCode",{parentName:"p"},"asdf global nodejs lts"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Update npm ",(0,l.kt)("inlineCode",{parentName:"p"},"npm install -g npm"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Update yarn ",(0,l.kt)("inlineCode",{parentName:"p"},"npm install -g yarn"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Add awscli ",(0,l.kt)("inlineCode",{parentName:"p"},"asdf plugin add awscli"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Install awscli ",(0,l.kt)("inlineCode",{parentName:"p"},"asdf install awscli latest"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Set awscli ",(0,l.kt)("inlineCode",{parentName:"p"},"asdf global awscli latest"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Add gcloud ",(0,l.kt)("inlineCode",{parentName:"p"},"asdf plugin add gcloud"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Install gcloud ",(0,l.kt)("inlineCode",{parentName:"p"},"asdf install gcloud latest"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},"Set gcloud ",(0,l.kt)("inlineCode",{parentName:"p"},"asdf global gcloud latest")))),(0,l.kt)("ol",{start:12},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"Git"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S git"))),(0,l.kt)("ol",{start:13},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"ZSH"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S zsh"))),(0,l.kt)("ol",{start:14},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"Twingate"))),(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"Sparrow Wallet")))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S sparrow-wallet"))),(0,l.kt)("ol",{start:16},(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"BISQ"))),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"Install ",(0,l.kt)("inlineCode",{parentName:"li"},"yay -S bisq-bin"))))}u.isMDXComponent=!0}}]);