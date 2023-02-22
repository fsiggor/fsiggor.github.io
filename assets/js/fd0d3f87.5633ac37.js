"use strict";(self.webpackChunkblog=self.webpackChunkblog||[]).push([[147],{3905:(e,t,n)=>{n.d(t,{Zo:()=>c,kt:()=>g});var r=n(7294);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var u=r.createContext({}),s=function(e){var t=r.useContext(u),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},c=function(e){var t=s(e.components);return r.createElement(u.Provider,{value:t},e.children)},p="mdxType",m={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,o=e.originalType,u=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),p=s(n),f=a,g=p["".concat(u,".").concat(f)]||p[f]||m[f]||o;return n?r.createElement(g,i(i({ref:t},c),{},{components:n})):r.createElement(g,i({ref:t},c))}));function g(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=n.length,i=new Array(o);i[0]=f;var l={};for(var u in t)hasOwnProperty.call(t,u)&&(l[u]=t[u]);l.originalType=e,l[p]="string"==typeof e?e:a,i[1]=l;for(var s=2;s<o;s++)i[s]=n[s];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},6847:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>u,contentTitle:()=>i,default:()=>m,frontMatter:()=>o,metadata:()=>l,toc:()=>s});var r=n(7462),a=(n(7294),n(3905));const o={},i="Default Values to Function Parameters",l={unversionedId:"Golang/Default Values to Function Parameters",id:"Golang/Default Values to Function Parameters",title:"Default Values to Function Parameters",description:"Functional options pattern",source:"@site/docs/Golang/Default Values to Function Parameters.md",sourceDirName:"Golang",slug:"/Golang/Default Values to Function Parameters",permalink:"/docs/Golang/Default Values to Function Parameters",draft:!1,editUrl:"https://github.com/fsiggor/fsiggor.github.io/tree/main/packages/create-docusaurus/templates/shared/docs/Golang/Default Values to Function Parameters.md",tags:[],version:"current",frontMatter:{},sidebar:"tutorialSidebar",previous:{title:"Expo",permalink:"/docs/CLI/expo"},next:{title:"Go Enums",permalink:"/docs/Golang/Go Enums"}},u={},s=[{value:"Functional options pattern",id:"functional-options-pattern",level:3}],c={toc:s},p="wrapper";function m(e){let{components:t,...n}=e;return(0,a.kt)(p,(0,r.Z)({},c,n,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("h1",{id:"default-values-to-function-parameters"},"Default Values to Function Parameters"),(0,a.kt)("h3",{id:"functional-options-pattern"},"Functional options pattern"),(0,a.kt)("ol",null,(0,a.kt)("li",{parentName:"ol"},"Create a struct to hold our arguments:")),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-go"},"type GreetingOptions struct {  \n  Name string  \n  Age  int  \n}\n")),(0,a.kt)("ol",{start:2},(0,a.kt)("li",{parentName:"ol"},"Now let\u2019s define the function:")),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-go"},'func Greet(options GreetingOptions) string {\n  return "My name is " + options.Name + " and I am " + strconv.Itoa(options.Age) + " years old."\n}\n')),(0,a.kt)("ol",{start:3},(0,a.kt)("li",{parentName:"ol"},"Define functional options for the fields in the struct:")),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-go"},"type GreetingOption func(*GreetingOptions)  \n  \nfunc WithName(name string) GreetingOption {  \n  return func(o *GreetingOptions) {  \n    o.Name = name  \n  }  \n}  \n  \nfunc WithAge(age int) GreetingOption {  \n  return func(o *GreetingOptions) {  \n    o.Age = age  \n  }  \n}\n")),(0,a.kt)("ol",{start:4},(0,a.kt)("li",{parentName:"ol"},"Create a wrapper:")),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-go"},'func GreetWithDefaultOptions(options ...GreetingOption) string {  \n  opts := GreetingOptions{  \n    Name: "Aiden",  \n    Age:  30,  \n  }  \n  for _, o := range options {  \n    o(&opts)  \n  }  \n  return Greet(opts)  \n}\n')),(0,a.kt)("ol",{start:5},(0,a.kt)("li",{parentName:"ol"},"Use:")),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-go"},'greeting := GreetWithDefaultOptions(WithName("Alice"), WithAge(20))  \n// Out: "My name is Alice and I am 20 years old."\n')),(0,a.kt)("p",null,"Reference: ",(0,a.kt)("a",{parentName:"p",href:"https://medium.com/@func25/golang-secret-how-to-add-default-values-to-function-parameters-60bd1e9625dc"},"https://medium.com/@func25/golang-secret-how-to-add-default-values-to-function-parameters-60bd1e9625dc")))}m.isMDXComponent=!0}}]);