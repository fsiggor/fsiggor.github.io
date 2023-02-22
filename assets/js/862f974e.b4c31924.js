"use strict";(self.webpackChunkblog=self.webpackChunkblog||[]).push([[216],{3905:(e,t,n)=>{n.d(t,{Zo:()=>p,kt:()=>m});var o=n(7294);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,o)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function c(e,t){if(null==e)return{};var n,o,r=function(e,t){if(null==e)return{};var n,o,r={},a=Object.keys(e);for(o=0;o<a.length;o++)n=a[o],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(o=0;o<a.length;o++)n=a[o],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var l=o.createContext({}),s=function(e){var t=o.useContext(l),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},p=function(e){var t=s(e.components);return o.createElement(l.Provider,{value:t},e.children)},u="mdxType",f={inlineCode:"code",wrapper:function(e){var t=e.children;return o.createElement(o.Fragment,{},t)}},g=o.forwardRef((function(e,t){var n=e.components,r=e.mdxType,a=e.originalType,l=e.parentName,p=c(e,["components","mdxType","originalType","parentName"]),u=s(n),g=r,m=u["".concat(l,".").concat(g)]||u[g]||f[g]||a;return n?o.createElement(m,i(i({ref:t},p),{},{components:n})):o.createElement(m,i({ref:t},p))}));function m(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var a=n.length,i=new Array(a);i[0]=g;var c={};for(var l in t)hasOwnProperty.call(t,l)&&(c[l]=t[l]);c.originalType=e,c[u]="string"==typeof e?e:r,i[1]=c;for(var s=2;s<a;s++)i[s]=n[s];return o.createElement.apply(null,i)}return o.createElement.apply(null,n)}g.displayName="MDXCreateElement"},5306:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>l,contentTitle:()=>i,default:()=>f,frontMatter:()=>a,metadata:()=>c,toc:()=>s});var o=n(7462),r=(n(7294),n(3905));const a={},i=void 0,c={unversionedId:"Golang/Performance/Using govet",id:"Golang/Performance/Using govet",title:"Using govet",description:"The govet tool is a static analysis tool without running code that can help you find potential issues in your Go code.",source:"@site/docs/Golang/Performance/Using govet.md",sourceDirName:"Golang/Performance",slug:"/Golang/Performance/Using govet",permalink:"/docs/Golang/Performance/Using govet",draft:!1,editUrl:"https://github.com/fsiggor/fsiggor.github.io/tree/main/packages/create-docusaurus/templates/shared/docs/Golang/Performance/Using govet.md",tags:[],version:"current",frontMatter:{},sidebar:"tutorialSidebar",previous:{title:"String concatenation",permalink:"/docs/Golang/Performance/String concatenation"},next:{title:"Reflection in Go",permalink:"/docs/Golang/Reflection in Go"}},l={},s=[],p={toc:s},u="wrapper";function f(e){let{components:t,...n}=e;return(0,r.kt)(u,(0,o.Z)({},p,n,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("p",null,"The ",(0,r.kt)("inlineCode",{parentName:"p"},"govet")," tool is a static analysis tool without running code that can help you find potential issues in your Go code."),(0,r.kt)("p",null,(0,r.kt)("inlineCode",{parentName:"p"},"govet")," checks your code for all sorts of problems that could cause bugs or lead to poor performance. It's like a code quality police, constantly checking to make sure you're not doing anything stupid."),(0,r.kt)("p",null,"To use ",(0,r.kt)("inlineCode",{parentName:"p"},"govet"),", you can run the ",(0,r.kt)("inlineCode",{parentName:"p"},"go tool vet")," command and pass the names of the Go source files you want to check as arguments:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"go tool vet main.go\n")),(0,r.kt)("p",null,"Reference: ",(0,r.kt)("a",{parentName:"p",href:"https://medium.com/@func25/go-performance-boosters-the-top-5-tips-and-tricks-you-need-to-know-e5cf6e5bc683"},"https://medium.com/@func25/go-performance-boosters-the-top-5-tips-and-tricks-you-need-to-know-e5cf6e5bc683")))}f.isMDXComponent=!0}}]);