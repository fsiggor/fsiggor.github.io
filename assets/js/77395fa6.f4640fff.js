"use strict";(self.webpackChunkblog=self.webpackChunkblog||[]).push([[783],{3905:(e,t,n)=>{n.d(t,{Zo:()=>c,kt:()=>f});var r=n(7294);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function i(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var s=r.createContext({}),p=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):l(l({},t),e)),n},c=function(e){var t=p(e.components);return r.createElement(s.Provider,{value:t},e.children)},u="mdxType",m={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},d=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,o=e.originalType,s=e.parentName,c=i(e,["components","mdxType","originalType","parentName"]),u=p(n),d=a,f=u["".concat(s,".").concat(d)]||u[d]||m[d]||o;return n?r.createElement(f,l(l({ref:t},c),{},{components:n})):r.createElement(f,l({ref:t},c))}));function f(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=n.length,l=new Array(o);l[0]=d;var i={};for(var s in t)hasOwnProperty.call(t,s)&&(i[s]=t[s]);i.originalType=e,i[u]="string"==typeof e?e:a,l[1]=i;for(var p=2;p<o;p++)l[p]=n[p];return r.createElement.apply(null,l)}return r.createElement.apply(null,n)}d.displayName="MDXCreateElement"},7041:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>s,contentTitle:()=>l,default:()=>m,frontMatter:()=>o,metadata:()=>i,toc:()=>p});var r=n(7462),a=(n(7294),n(3905));const o={},l="Windows Setup",i={unversionedId:"Windows/setup",id:"Windows/setup",title:"Windows Setup",description:"1. Debloat Windows with this Script",source:"@site/docs/Windows/setup.md",sourceDirName:"Windows",slug:"/Windows/setup",permalink:"/docs/Windows/setup",draft:!1,editUrl:"https://github.com/fsiggor/fsiggor.github.io/tree/main/packages/create-docusaurus/templates/shared/docs/Windows/setup.md",tags:[],version:"current",frontMatter:{},sidebar:"tutorialSidebar",previous:{title:"Manjaro Post-Install",permalink:"/docs/Linux/post-install"},next:{title:"Backend",permalink:"/docs/category/backend"}},s={},p=[],c={toc:p},u="wrapper";function m(e){let{components:t,...n}=e;return(0,a.kt)(u,(0,r.Z)({},c,n,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("h1",{id:"windows-setup"},"Windows Setup"),(0,a.kt)("ol",null,(0,a.kt)("li",{parentName:"ol"},"Debloat Windows with this ",(0,a.kt)("a",{parentName:"li",href:"https://github.com/LeDragoX/Win-Debloat-Tools"},"Script")),(0,a.kt)("li",{parentName:"ol"},"Install WSL using the PowerShell: ",(0,a.kt)("inlineCode",{parentName:"li"},"wsl --install")),(0,a.kt)("li",{parentName:"ol"},"Download and Install ",(0,a.kt)("a",{parentName:"li",href:"https://github.com/yuk7/ArchWSL"},"ArchWSL")),(0,a.kt)("li",{parentName:"ol"},"Create a new linux user and update packages"),(0,a.kt)("li",{parentName:"ol"},"Install ",(0,a.kt)("a",{parentName:"li",href:"https://github.com/Jguer/yay"},"Yay")),(0,a.kt)("li",{parentName:"ol"},"Instal ZShell: ",(0,a.kt)("inlineCode",{parentName:"li"},"yay -S zsh")),(0,a.kt)("li",{parentName:"ol"},"Install ",(0,a.kt)("a",{parentName:"li",href:"https://github.com/romkatv/powerlevel10k#arch-linux"},"PowerLevel10k")),(0,a.kt)("li",{parentName:"ol"},"Change shell to zsh: ",(0,a.kt)("inlineCode",{parentName:"li"},"chsh -s /usr/bin/zsh")),(0,a.kt)("li",{parentName:"ol"},"Add ",(0,a.kt)("a",{parentName:"li",href:"https://github.com/romkatv/powerlevel10k#manual-font-installation"},"font")," to WSL"),(0,a.kt)("li",{parentName:"ol"},"Configure PowerLevel10k: ",(0,a.kt)("inlineCode",{parentName:"li"},"p10k configure")),(0,a.kt)("li",{parentName:"ol"},"Install ",(0,a.kt)("a",{parentName:"li",href:"https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#manual-git-clone"},"ZSH Autosuggestions")),(0,a.kt)("li",{parentName:"ol"},"Install asdf and programming languages"),(0,a.kt)("li",{parentName:"ol"},"Rust system tools and define alias(ls->exa, cat->bat...)"),(0,a.kt)("li",{parentName:"ol"},"Install Docker Desktop")))}m.isMDXComponent=!0}}]);