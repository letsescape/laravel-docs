<!-- # Starter Kits -->
# Starter Kits

- [Introduction](#introduction)
- [Creating an Application Using a Starter Kit](#creating-an-application)
- [Available Starter Kits](#available-starter-kits)
    - [React](#react)
    - [Svelte](#svelte)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [Starter Kit Customization](#starter-kit-customization)
    - [React](#react-customization)
    - [Svelte](#svelte-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [Authentication](#authentication)
    - [Enabling and Disabling Features](#enabling-and-disabling-features)
    - [Customizing User Creation and Password Reset](#customizing-actions)
    - [Two-Factor Authentication](#two-factor-authentication)
    - [Rate Limiting](#rate-limiting)
- [Teams](#teams)
- [WorkOS AuthKit Authentication](#workos)
    - [Configuring Your WorkOS Starter Kit](#configuring-your-workos-starter-kit)
- [Inertia SSR](#inertia-ssr)
- [Community Maintained Starter Kits](#community-maintained-starter-kits)
- [Frequently Asked Questions](#faqs)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- To give you a head start building your new Laravel application, we are happy to offer [application starter kits](https://laravel.com/starter-kits). These starter kits give you a head start on building your next Laravel application, and include the routes, controllers, and views you need to register and authenticate your application's users. The starter kits use [Laravel Fortify](/docs/13.x/fortify) to provide authentication. -->
새 Laravel 애플리케이션을 더 빠르게 시작할 수 있도록, Laravel은 [application starter kits](https://laravel.com/starter-kits)를 제공합니다. 이 스타터 키트는 다음 Laravel 애플리케이션을 빠르게 구축할 수 있도록 도와주며, 애플리케이션 사용자를 등록하고 인증하는 데 필요한 라우트, 컨트롤러, 뷰를 포함합니다. 스타터 키트는 인증 기능을 제공하기 위해 [Laravel Fortify](/docs/13.x/fortify)를 사용합니다.

<!-- While you are welcome to use these starter kits, they are not required. You are free to build your own application from the ground up by simply installing a fresh copy of Laravel. Either way, we know you will build something great! -->
물론 이 스타터 키트를 사용할 수 있지만, 반드시 사용해야 하는 것은 아닙니다. Laravel을 새로 설치한 뒤 처음부터 직접 애플리케이션을 구축해도 됩니다. 어떤 방식을 선택하든 훌륭한 결과물을 만들 수 있을 것입니다!

<a name="creating-an-application"></a>
<!-- ## Creating an Application Using a Starter Kit -->
## Creating an Application Using a Starter Kit

<!-- To create a new Laravel application using one of our starter kits, you should first [install PHP and the Laravel CLI tool](/docs/13.x/installation#installing-php). If you already have PHP and Composer installed, you may install the Laravel installer CLI tool via Composer: -->
스타터 키트 중 하나를 사용하여 새 Laravel 애플리케이션을 만들려면 먼저 [install PHP and the Laravel CLI tool](/docs/13.x/installation#installing-php)해야 합니다. 이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel installer CLI 도구를 설치할 수 있습니다.

```shell
composer global require laravel/installer
```

<!-- Then, create a new Laravel application using the Laravel installer CLI. The Laravel installer will prompt you to select your preferred starter kit: -->
그런 다음 Laravel installer CLI를 사용하여 새 Laravel 애플리케이션을 만듭니다. Laravel installer는 원하는 스타터 키트를 선택하라는 메시지를 표시합니다.

```shell
laravel new my-app
```

<!-- After creating your Laravel application, you only need to install its frontend dependencies via NPM and start the Laravel development server: -->
Laravel 애플리케이션을 만든 뒤에는 NPM을 통해 프론트엔드 의존성을 설치하고 Laravel 개발 서버를 시작하기만 하면 됩니다.

```shell
cd my-app
npm install && npm run build
composer run dev
```

<!-- Once you have started the Laravel development server, your application will be accessible in your web browser at [http://localhost:8000](http://localhost:8000). -->
Laravel 개발 서버를 시작하면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접속할 수 있습니다.

<a name="available-starter-kits"></a>
<!-- ## Available Starter Kits -->
## Available Starter Kits

<a name="react"></a>
<!-- ### React -->
### React

<!-- Our React starter kit provides a robust, modern starting point for building Laravel applications with a React frontend using [Inertia](https://inertiajs.com). -->
React 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 React 프론트엔드를 갖춘 Laravel 애플리케이션을 만들기 위한 견고하고 현대적인 출발점을 제공합니다.

<!-- Inertia allows you to build modern, single-page React applications using classic server-side routing and controllers. This lets you enjoy the frontend power of React combined with the incredible backend productivity of Laravel and lightning-fast Vite compilation. -->
Inertia를 사용하면 전통적인 서버 사이드 라우팅과 컨트롤러를 그대로 사용하면서도 현대적인 싱글 페이지 React 애플리케이션을 만들 수 있습니다. 이를 통해 React의 강력한 프론트엔드 기능과 Laravel의 뛰어난 백엔드 생산성, 매우 빠른 Vite 컴파일을 함께 활용할 수 있습니다.

<!-- The React starter kit utilizes React 19, TypeScript, Tailwind, and the [shadcn/ui](https://ui.shadcn.com) component library. -->
React 스타터 키트는 React 19, TypeScript, Tailwind, [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="svelte"></a>
<!-- ### Svelte -->
### Svelte

<!-- Our Svelte starter kit provides a robust, modern starting point for building Laravel applications with a Svelte frontend using [Inertia](https://inertiajs.com). -->
Svelte 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 Svelte 프론트엔드를 갖춘 Laravel 애플리케이션을 만들기 위한 견고하고 현대적인 출발점을 제공합니다.

<!-- Inertia allows you to build modern, single-page Svelte applications using classic server-side routing and controllers. This lets you enjoy the frontend power of Svelte combined with the incredible backend productivity of Laravel and lightning-fast Vite compilation. -->
Inertia를 사용하면 전통적인 서버 사이드 라우팅과 컨트롤러를 그대로 사용하면서도 현대적인 싱글 페이지 Svelte 애플리케이션을 만들 수 있습니다. 이를 통해 Svelte의 강력한 프론트엔드 기능과 Laravel의 뛰어난 백엔드 생산성, 매우 빠른 Vite 컴파일을 함께 활용할 수 있습니다.

<!-- The Svelte starter kit utilizes Svelte 5, TypeScript, Tailwind, and the [shadcn-svelte](https://www.shadcn-svelte.com/) component library. -->
Svelte 스타터 키트는 Svelte 5, TypeScript, Tailwind, [shadcn-svelte](https://www.shadcn-svelte.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
<!-- ### Vue -->
### Vue

<!-- Our Vue starter kit provides a great starting point for building Laravel applications with a Vue frontend using [Inertia](https://inertiajs.com). -->
Vue 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 Vue 프론트엔드를 갖춘 Laravel 애플리케이션을 만들기 위한 훌륭한 출발점을 제공합니다.

<!-- Inertia allows you to build modern, single-page Vue applications using classic server-side routing and controllers. This lets you enjoy the frontend power of Vue combined with the incredible backend productivity of Laravel and lightning-fast Vite compilation. -->
Inertia를 사용하면 전통적인 서버 사이드 라우팅과 컨트롤러를 그대로 사용하면서도 현대적인 싱글 페이지 Vue 애플리케이션을 만들 수 있습니다. 이를 통해 Vue의 강력한 프론트엔드 기능과 Laravel의 뛰어난 백엔드 생산성, 매우 빠른 Vite 컴파일을 함께 활용할 수 있습니다.

<!-- The Vue starter kit utilizes the Vue Composition API, TypeScript, Tailwind, and the [shadcn-vue](https://www.shadcn-vue.com/) component library. -->
Vue 스타터 키트는 Vue Composition API, TypeScript, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
<!-- ### Livewire -->
### Livewire

<!-- Our Livewire starter kit provides the perfect starting point for building Laravel applications with a [Laravel Livewire](https://livewire.laravel.com) frontend. -->
Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드를 갖춘 Laravel 애플리케이션을 만들기 위한 완벽한 출발점을 제공합니다.

<!-- Livewire is a powerful way of building dynamic, reactive, frontend UIs using just PHP. It's a great fit for teams that primarily use Blade templates and are looking for a simpler alternative to JavaScript-driven SPA frameworks like React, Svelte, and Vue. -->
Livewire는 PHP만으로 동적이고 반응형인 프론트엔드 UI를 만들 수 있는 강력한 방식입니다. 주로 Blade 템플릿을 사용하고, React, Svelte, Vue와 같은 JavaScript 기반 SPA 프레임워크보다 단순한 대안을 찾는 팀에 잘 맞습니다.

<!-- The Livewire starter kit utilizes Livewire, Tailwind, and the [Flux UI](https://fluxui.dev) component library. -->
Livewire 스타터 키트는 Livewire, Tailwind, [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
<!-- ## Starter Kit Customization -->
## Starter Kit Customization

<a name="react-customization"></a>
<!-- ### React -->
### React

<!-- Our React starter kit is built with Inertia 3, React 19, Tailwind 4, and [shadcn/ui](https://ui.shadcn.com). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization. -->
React 스타터 키트는 Inertia 3, React 19, Tailwind 4, [shadcn/ui](https://ui.shadcn.com)를 기반으로 만들어졌습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프론트엔드 코드가 모두 애플리케이션 안에 있으므로 완전히 자유롭게 커스터마이징할 수 있습니다.

<!-- The majority of the frontend code is located in the `resources/js` directory. You are free to modify any of the code to customize the appearance and behavior of your application: -->
대부분의 프론트엔드 코드는 `resources/js` 디렉터리에 있습니다. 애플리케이션의 모양과 동작을 커스터마이징하기 위해 원하는 코드를 자유롭게 수정할 수 있습니다.

```text
resources/js/
├── components/    # Reusable React components
├── hooks/         # React hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

<!-- To publish additional shadcn components, first [find the component you want to publish](https://ui.shadcn.com). Then, publish the component using `npx`: -->
추가 shadcn 컴포넌트를 게시하려면 먼저 [find the component you want to publish](https://ui.shadcn.com). 그런 다음 `npx`를 사용하여 컴포넌트를 게시합니다.

```shell
npx shadcn@latest add switch
```

<!-- In this example, the command will publish the Switch component to `resources/js/components/ui/switch.tsx`. Once the component has been published, you can use it in any of your pages: -->
이 예제에서 이 명령어는 Switch 컴포넌트를 `resources/js/components/ui/switch.tsx`에 게시합니다. 컴포넌트가 게시되면 어떤 페이지에서든 사용할 수 있습니다.

```jsx
import { Switch } from "@/components/ui/switch"

const MyPage = () => {
  return (
    <div>
      <Switch />
    </div>
  );
};

export default MyPage;
```

<a name="react-available-layouts"></a>
<!-- #### Available Layouts -->
#### Available Layouts

<!-- The React starter kit includes two different primary layouts for you to choose from: a "sidebar" layout and a "header" layout. The sidebar layout is the default, but you can switch to the header layout by modifying the layout that is imported at the top of your application's `resources/js/layouts/app-layout.tsx` file: -->
React 스타터 키트에는 선택할 수 있는 두 가지 기본 레이아웃이 포함되어 있습니다. 바로 "sidebar" 레이아웃과 "header" 레이아웃입니다. 기본값은 sidebar 레이아웃이지만, 애플리케이션의 `resources/js/layouts/app-layout.tsx` 파일 상단에서 가져오는 레이아웃을 수정하여 header 레이아웃으로 전환할 수 있습니다.

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
<!-- #### Sidebar Variants -->
#### Sidebar Variants

<!-- The sidebar layout includes three different variants: the default sidebar variant, the "inset" variant, and the "floating" variant. You may choose the variant you like best by modifying the `resources/js/components/app-sidebar.tsx` component: -->
sidebar 레이아웃에는 세 가지 변형이 포함되어 있습니다. 기본 sidebar 변형, "inset" 변형, "floating" 변형입니다. `resources/js/components/app-sidebar.tsx` 컴포넌트를 수정하여 가장 마음에 드는 변형을 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
<!-- #### Authentication Page Layout Variants -->
#### Authentication Page Layout Variants

<!-- The authentication pages included with the React starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split". -->
React 스타터 키트에 포함된 로그인 페이지와 등록 페이지 같은 인증 페이지도 "simple", "card", "split"이라는 세 가지 레이아웃 변형을 제공합니다.

<!-- To change your authentication layout, modify the layout that is imported at the top of your application's `resources/js/layouts/auth-layout.tsx` file: -->
인증 레이아웃을 변경하려면 애플리케이션의 `resources/js/layouts/auth-layout.tsx` 파일 상단에서 가져오는 레이아웃을 수정합니다.

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="svelte-customization"></a>
<!-- ### Svelte -->
### Svelte

<!-- Our Svelte starter kit is built with Inertia 3, Svelte 5, Tailwind, and [shadcn-svelte](https://www.shadcn-svelte.com/). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization. -->
Svelte 스타터 키트는 Inertia 3, Svelte 5, Tailwind, [shadcn-svelte](https://www.shadcn-svelte.com/)를 기반으로 만들어졌습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프론트엔드 코드가 모두 애플리케이션 안에 있으므로 완전히 자유롭게 커스터마이징할 수 있습니다.

<!-- The majority of the frontend code is located in the `resources/js` directory. You are free to modify any of the code to customize the appearance and behavior of your application: -->
대부분의 프론트엔드 코드는 `resources/js` 디렉터리에 있습니다. 애플리케이션의 모양과 동작을 커스터마이징하기 위해 원하는 코드를 자유롭게 수정할 수 있습니다.

```text
resources/js/
├── components/    # Reusable Svelte components
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration and Svelte rune modules
├── pages/         # Page components
└── types/         # TypeScript definitions
```

<!-- To publish additional shadcn-svelte components, first [find the component you want to publish](https://www.shadcn-svelte.com). Then, publish the component using `npx`: -->
추가 shadcn-svelte 컴포넌트를 게시하려면 먼저 [find the component you want to publish](https://www.shadcn-svelte.com). 그런 다음 `npx`를 사용하여 컴포넌트를 게시합니다.

```shell
npx shadcn-svelte@latest add switch
```

<!-- In this example, the command will publish the Switch component to `resources/js/components/ui/switch/switch.svelte`. Once the component has been published, you can use it in any of your pages: -->
이 예제에서 이 명령어는 Switch 컴포넌트를 `resources/js/components/ui/switch/switch.svelte`에 게시합니다. 컴포넌트가 게시되면 어떤 페이지에서든 사용할 수 있습니다.

```svelte
<script lang="ts">
    import { Switch } from '@/components/ui/switch'
</script>

<div>
    <Switch />
</div>
```

<a name="svelte-available-layouts"></a>
<!-- #### Available Layouts -->
#### Available Layouts

<!-- The Svelte starter kit includes two different primary layouts for you to choose from: a "sidebar" layout and a "header" layout. The sidebar layout is the default, but you can switch to the header layout by modifying the layout that is imported at the top of your application's `resources/js/layouts/AppLayout.svelte` file: -->
Svelte 스타터 키트에는 선택할 수 있는 두 가지 기본 레이아웃이 포함되어 있습니다. 바로 "sidebar" 레이아웃과 "header" 레이아웃입니다. 기본값은 sidebar 레이아웃이지만, 애플리케이션의 `resources/js/layouts/AppLayout.svelte` 파일 상단에서 가져오는 레이아웃을 수정하여 header 레이아웃으로 전환할 수 있습니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.svelte'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.svelte'; // [tl! add]
```

<a name="svelte-sidebar-variants"></a>
<!-- #### Sidebar Variants -->
#### Sidebar Variants

<!-- The sidebar layout includes three different variants: the default sidebar variant, the "inset" variant, and the "floating" variant. You may choose the variant you like best by modifying the `resources/js/components/AppSidebar.svelte` component: -->
sidebar 레이아웃에는 세 가지 변형이 포함되어 있습니다. 기본 sidebar 변형, "inset" 변형, "floating" 변형입니다. `resources/js/components/AppSidebar.svelte` 컴포넌트를 수정하여 가장 마음에 드는 변형을 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="svelte-authentication-page-layout-variants"></a>
<!-- #### Authentication Page Layout Variants -->
#### Authentication Page Layout Variants

<!-- The authentication pages included with the Svelte starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split". -->
Svelte 스타터 키트에 포함된 로그인 페이지와 등록 페이지 같은 인증 페이지도 "simple", "card", "split"이라는 세 가지 레이아웃 변형을 제공합니다.

<!-- To change your authentication layout, modify the layout that is imported at the top of your application's `resources/js/layouts/AuthLayout.svelte` file: -->
인증 레이아웃을 변경하려면 애플리케이션의 `resources/js/layouts/AuthLayout.svelte` 파일 상단에서 가져오는 레이아웃을 수정합니다.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.svelte'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.svelte'; // [tl! add]
```

<a name="vue-customization"></a>
<!-- ### Vue -->
### Vue

<!-- Our Vue starter kit is built with Inertia 3, Vue 3 Composition API, Tailwind, and [shadcn-vue](https://www.shadcn-vue.com/). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization. -->
Vue 스타터 키트는 Inertia 3, Vue 3 Composition API, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/)를 기반으로 만들어졌습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프론트엔드 코드가 모두 애플리케이션 안에 있으므로 완전히 자유롭게 커스터마이징할 수 있습니다.

<!-- The majority of the frontend code is located in the `resources/js` directory. You are free to modify any of the code to customize the appearance and behavior of your application: -->
대부분의 프론트엔드 코드는 `resources/js` 디렉터리에 있습니다. 애플리케이션의 모양과 동작을 커스터마이징하기 위해 원하는 코드를 자유롭게 수정할 수 있습니다.

```text
resources/js/
├── components/    # Reusable Vue components
├── composables/   # Vue composables / hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

<!-- To publish additional shadcn-vue components, first [find the component you want to publish](https://www.shadcn-vue.com). Then, publish the component using `npx`: -->
추가 shadcn-vue 컴포넌트를 게시하려면 먼저 [find the component you want to publish](https://www.shadcn-vue.com). 그런 다음 `npx`를 사용하여 컴포넌트를 게시합니다.

```shell
npx shadcn-vue@latest add switch
```

<!-- In this example, the command will publish the Switch component to `resources/js/components/ui/Switch.vue`. Once the component has been published, you can use it in any of your pages: -->
이 예제에서 이 명령어는 Switch 컴포넌트를 `resources/js/components/ui/Switch.vue`에 게시합니다. 컴포넌트가 게시되면 어떤 페이지에서든 사용할 수 있습니다.

```vue
<script setup lang="ts">
import { Switch } from '@/components/ui/switch'
</script>

<template>
    <div>
        <Switch />
    </div>
</template>
```

<a name="vue-available-layouts"></a>
<!-- #### Available Layouts -->
#### Available Layouts

<!-- The Vue starter kit includes two different primary layouts for you to choose from: a "sidebar" layout and a "header" layout. The sidebar layout is the default, but you can switch to the header layout by modifying the layout that is imported at the top of your application's `resources/js/layouts/AppLayout.vue` file: -->
Vue 스타터 키트에는 선택할 수 있는 두 가지 기본 레이아웃이 포함되어 있습니다. 바로 "sidebar" 레이아웃과 "header" 레이아웃입니다. 기본값은 sidebar 레이아웃이지만, 애플리케이션의 `resources/js/layouts/AppLayout.vue` 파일 상단에서 가져오는 레이아웃을 수정하여 header 레이아웃으로 전환할 수 있습니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
<!-- #### Sidebar Variants -->
#### Sidebar Variants

<!-- The sidebar layout includes three different variants: the default sidebar variant, the "inset" variant, and the "floating" variant. You may choose the variant you like best by modifying the `resources/js/components/AppSidebar.vue` component: -->
sidebar 레이아웃에는 세 가지 변형이 포함되어 있습니다. 기본 sidebar 변형, "inset" 변형, "floating" 변형입니다. `resources/js/components/AppSidebar.vue` 컴포넌트를 수정하여 가장 마음에 드는 변형을 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
<!-- #### Authentication Page Layout Variants -->
#### Authentication Page Layout Variants

<!-- The authentication pages included with the Vue starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split". -->
Vue 스타터 키트에 포함된 로그인 페이지와 등록 페이지 같은 인증 페이지도 "simple", "card", "split"이라는 세 가지 레이아웃 변형을 제공합니다.

<!-- To change your authentication layout, modify the layout that is imported at the top of your application's `resources/js/layouts/AuthLayout.vue` file: -->
인증 레이아웃을 변경하려면 애플리케이션의 `resources/js/layouts/AuthLayout.vue` 파일 상단에서 가져오는 레이아웃을 수정합니다.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
<!-- ### Livewire -->
### Livewire

<!-- Our Livewire starter kit is built with Livewire 4, Tailwind, and [Flux UI](https://fluxui.dev/). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization. -->
Livewire 스타터 키트는 Livewire 4, Tailwind, [Flux UI](https://fluxui.dev/)를 기반으로 만들어졌습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프론트엔드 코드가 모두 애플리케이션 안에 있으므로 완전히 자유롭게 커스터마이징할 수 있습니다.

<!-- The majority of the frontend code is located in the `resources/views` directory. You are free to modify any of the code to customize the appearance and behavior of your application: -->
대부분의 프론트엔드 코드는 `resources/views` 디렉터리에 있습니다. 애플리케이션의 모양과 동작을 커스터마이징하기 위해 원하는 코드를 자유롭게 수정할 수 있습니다.

```text
resources/views
├── components            # Reusable components
├── flux                  # Customized Flux components
├── layouts               # Application layouts
├── pages                 # Livewire pages
├── partials              # Reusable Blade partials
├── dashboard.blade.php   # Authenticated user dashboard
├── welcome.blade.php     # Guest user welcome page
```

<a name="livewire-available-layouts"></a>
<!-- #### Available Layouts -->
#### Available Layouts

<!-- The Livewire starter kit includes two different primary layouts for you to choose from: a "sidebar" layout and a "header" layout. The sidebar layout is the default, but you can switch to the header layout by modifying the layout that is used by your application's `resources/views/layouts/app.blade.php` file. In addition, you should add the `container` attribute to the main Flux component: -->
Livewire 스타터 키트에는 선택할 수 있는 두 가지 기본 레이아웃이 포함되어 있습니다. 바로 "sidebar" 레이아웃과 "header" 레이아웃입니다. 기본값은 sidebar 레이아웃이지만, 애플리케이션의 `resources/views/layouts/app.blade.php` 파일에서 사용하는 레이아웃을 수정하여 header 레이아웃으로 전환할 수 있습니다. 또한 기본 Flux 컴포넌트에 `container` 속성을 추가해야 합니다.

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
<!-- #### Authentication Page Layout Variants -->
#### Authentication Page Layout Variants

<!-- The authentication pages included with the Livewire starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split". -->
Livewire 스타터 키트에 포함된 로그인 페이지와 등록 페이지 같은 인증 페이지도 "simple", "card", "split"이라는 세 가지 레이아웃 변형을 제공합니다.

<!-- To change your authentication layout, modify the layout that is used by your application's `resources/views/layouts/auth.blade.php` file: -->
인증 레이아웃을 변경하려면 애플리케이션의 `resources/views/layouts/auth.blade.php` 파일에서 사용하는 레이아웃을 수정합니다.

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a name="authentication"></a>
<!-- ## Authentication -->
## Authentication

<!-- All starter kits use [Laravel Fortify](/docs/13.x/fortify) to handle authentication. Fortify provides routes, controllers, and logic for login, registration, password reset, email verification, and more. -->
모든 스타터 키트는 인증을 처리하기 위해 [Laravel Fortify](/docs/13.x/fortify)를 사용합니다. Fortify는 로그인, 등록, 비밀번호 재설정, 이메일 인증 등을 위한 라우트, 컨트롤러, 로직을 제공합니다.

<!-- Fortify automatically registers the following authentication routes based on the features that are enabled in your application's `config/fortify.php` configuration file: -->
Fortify는 애플리케이션의 `config/fortify.php` 설정 파일에서 활성화된 기능에 따라 다음 인증 라우트를 자동으로 등록합니다.

<div class="overflow-auto">

<!-- | Route | Method | Description | | ---------------------------------- | ------ | ----------------------------------- | | `/login` | `GET` | Display login form | | `/login` | `POST` | Authenticate user | | `/logout` | `POST` | Log user out | | `/register` | `GET` | Display registration form | | `/register` | `POST` | Create new user | | `/forgot-password` | `GET` | Display password reset request form | | `/forgot-password` | `POST` | Send password reset link | | `/reset-password/{token}` | `GET` | Display password reset form | | `/reset-password` | `POST` | Update password | | `/email/verify` | `GET` | Display email verification notice | | `/email/verify/{id}/{hash}` | `GET` | Verify email address | | `/email/verification-notification` | `POST` | Resend verification email | | `/user/confirm-password` | `GET` | Display password confirmation form | | `/user/confirm-password` | `POST` | Confirm password | | `/two-factor-challenge` | `GET` | Display 2FA challenge form | | `/two-factor-challenge` | `POST` | Verify 2FA code | -->
| 라우트                             | 메서드 | 설명                                |
| ---------------------------------- | ------ | ----------------------------------- |
| `/login`                           | `GET`    | 로그인 폼 표시                      |
| `/login`                           | `POST`   | 사용자 인증                         |
| `/logout`                          | `POST`   | 사용자 로그아웃                     |
| `/register`                        | `GET`    | 등록 폼 표시                        |
| `/register`                        | `POST`   | 새 사용자 생성                      |
| `/forgot-password`                 | `GET`    | 비밀번호 재설정 요청 폼 표시        |
| `/forgot-password`                 | `POST`   | 비밀번호 재설정 링크 전송           |
| `/reset-password/{token}`          | `GET`    | 비밀번호 재설정 폼 표시             |
| `/reset-password`                  | `POST`   | 비밀번호 업데이트                   |
| `/email/verify`                    | `GET`    | 이메일 인증 안내 표시               |
| `/email/verify/{id}/{hash}`        | `GET`    | 이메일 주소 인증                    |
| `/email/verification-notification` | `POST`   | 인증 이메일 재전송                  |
| `/user/confirm-password`           | `GET`    | 비밀번호 확인 폼 표시               |
| `/user/confirm-password`           | `POST`   | 비밀번호 확인                       |
| `/two-factor-challenge`            | `GET`    | 2FA 확인 폼 표시                    |
| `/two-factor-challenge`            | `POST`   | 2FA 코드 검증                       |

</div>

<!-- The `php artisan route:list` Artisan command can be used to display all of the routes in your application. -->
`php artisan route:list` Artisan 명령어를 사용하면 애플리케이션의 모든 라우트를 표시할 수 있습니다.

<a name="enabling-and-disabling-features"></a>
<!-- ### Enabling and Disabling Features -->
### Enabling and Disabling Features

<!-- You can control which Fortify features are enabled in your application's `config/fortify.php` configuration file: -->
애플리케이션의 `config/fortify.php` 설정 파일에서 어떤 Fortify 기능을 활성화할지 제어할 수 있습니다.

```php
use Laravel\Fortify\Features;

'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
    Features::twoFactorAuthentication([
        'confirm' => true,
        'confirmPassword' => true,
    ]),
],
```

<!-- To disable a feature, comment out or remove that feature entry from the `features` array. For example, remove `Features::registration()` to disable public registration. -->
기능을 비활성화하려면 `features` 배열에서 해당 기능 항목을 주석 처리하거나 제거합니다. 예를 들어 공개 등록을 비활성화하려면 `Features::registration()`을 제거합니다.

<!-- When using the [React](#react), [Svelte](#svelte) or [Vue](#vue) starter kits, you will also need to remove any references to the disabled feature's routes in your frontend code. For example, if you disable email verification, you should remove the imports and references to the `verification` routes in your React, Svelte, or Vue components. This is necessary because these starter kits use Wayfinder for type-safe routing, which generates route definitions at build time. If you reference routes that no longer exist, your application will fail to build. -->
[React](#react), [Svelte](#svelte) 또는 [Vue](#vue) 스타터 키트를 사용하는 경우, 프론트엔드 코드에서도 비활성화된 기능의 라우트를 참조하는 부분을 제거해야 합니다. 예를 들어 이메일 인증을 비활성화했다면 React, Svelte 또는 Vue 컴포넌트에서 `verification` 라우트를 가져오거나 참조하는 부분을 제거해야 합니다. 이러한 작업이 필요한 이유는 이 스타터 키트들이 타입 안전 라우팅을 위해 Wayfinder를 사용하며, Wayfinder가 빌드 시점에 라우트 정의를 생성하기 때문입니다. 더 이상 존재하지 않는 라우트를 참조하면 애플리케이션 빌드가 실패합니다.

<a name="customizing-actions"></a>
<!-- ### Customizing User Creation and Password Reset -->
### Customizing User Creation and Password Reset

<!-- When a user registers or resets their password, Fortify invokes action classes located in your application's `app/Actions/Fortify` directory: -->
사용자가 회원가입하거나 비밀번호를 재설정하면, Fortify는 애플리케이션의 `app/Actions/Fortify` 디렉터리에 있는 액션 클래스를 호출합니다.

<div class="overflow-auto">

<!-- | File | Description | | ----------------------------- | ------------------------------------- | | `CreateNewUser.php` | Validates and creates new users | | `ResetUserPassword.php` | Validates and updates user passwords | | `PasswordValidationRules.php` | Defines password validation rules | -->
| 파일                          | 설명                                  |
| ----------------------------- | ------------------------------------- |
| `CreateNewUser.php`           | 새 사용자를 유효성 검증하고 생성합니다 |
| `ResetUserPassword.php`       | 사용자 비밀번호를 유효성 검증하고 업데이트합니다 |
| `PasswordValidationRules.php` | 비밀번호 유효성 검증 규칙을 정의합니다 |

</div>

<!-- For example, to customize your application's registration logic, you should edit the `CreateNewUser` action: -->
예를 들어, 애플리케이션의 회원가입 로직을 사용자 정의하려면 `CreateNewUser` 액션을 수정해야 합니다.

```php
public function create(array $input): User
{
    Validator::make($input, [
        'name' => ['required', 'string', 'max:255'],
        'email' => ['required', 'email', 'max:255', 'unique:users'],
        'phone' => ['required', 'string', 'max:20'], // [tl! add]
        'password' => $this->passwordRules(),
    ])->validate();

    return User::create([
        'name' => $input['name'],
        'email' => $input['email'],
        'phone' => $input['phone'], // [tl! add]
        'password' => Hash::make($input['password']),
    ]);
}
```

<a name="two-factor-authentication"></a>
<!-- ### Two-Factor Authentication -->
### Two-Factor Authentication

<!-- Starter kits include built-in two-factor authentication (2FA), allowing users to secure their accounts using any TOTP-compatible authenticator app. 2FA is enabled by default via `Features::twoFactorAuthentication()` in your application's `config/fortify.php` configuration file. -->
스타터 키트에는 기본 제공 2단계 인증(2FA)이 포함되어 있어, 사용자가 TOTP와 호환되는 인증 앱을 사용해 계정을 보호할 수 있습니다. 2FA는 애플리케이션의 `config/fortify.php` 설정 파일에서 `Features::twoFactorAuthentication()`을 통해 기본적으로 활성화됩니다.

<!-- The `confirm` option requires users to verify a code before 2FA is fully enabled, while `confirmPassword` requires password confirmation before enabling or disabling 2FA. For more details, see [Fortify's two-factor authentication documentation](/docs/13.x/fortify#two-factor-authentication). -->
`confirm` 옵션은 2FA가 완전히 활성화되기 전에 사용자가 코드를 확인하도록 요구하며, `confirmPassword`는 2FA를 활성화하거나 비활성화하기 전에 비밀번호 확인을 요구합니다. 자세한 내용은 [Fortify's two-factor authentication documentation](/docs/13.x/fortify#two-factor-authentication)를 참고하십시오.

<a name="rate-limiting"></a>
<!-- ### Rate Limiting -->
### Rate Limiting

<!-- Rate limiting prevents brute-forcing and repeated login attempts from overwhelming your authentication endpoints. You can customize Fortify's rate limiting behavior in your application's `FortifyServiceProvider`: -->
요청 속도 제한은 무차별 대입 공격과 반복적인 로그인 시도로 인해 인증 엔드포인트에 과도한 부하가 걸리는 것을 방지합니다. 애플리케이션의 `FortifyServiceProvider`에서 Fortify의 요청 속도 제한 동작을 사용자 정의할 수 있습니다.

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="teams"></a>
<!-- ## Teams -->
## Teams

<!-- The React, Svelte, Vue, and Livewire starter kits may also be generated with team support. When the teams feature is enabled, each user belongs to one or more teams and has a current team. During registration, new users are automatically given a personal team. The starter kits also include team management screens for creating teams, switching between teams, inviting members, and updating team details. -->
React, Svelte, Vue, Livewire 스타터 키트는 팀 지원 기능을 포함하여 생성할 수도 있습니다. 팀 기능이 활성화되면 각 사용자는 하나 이상의 팀에 속하며 현재 팀을 가집니다. 회원가입 중에는 새 사용자에게 개인 팀이 자동으로 제공됩니다. 또한 스타터 키트에는 팀 생성, 팀 전환, 멤버 초대, 팀 세부 정보 업데이트를 위한 팀 관리 화면도 포함되어 있습니다.

<!-- When a route is scoped to the current team, the current team's slug is included in the URL. For example, the dashboard route becomes `/{current_team}/dashboard`, while team management pages use routes such as `settings/teams/{team}`. When using the `{current_team}` and `{team}` route parameters, the starter kits automatically ensure that the authenticated user belongs to the requested team before allowing access to the route. -->
라우트가 현재 팀 범위로 지정되면 현재 팀의 슬러그가 URL에 포함됩니다. 예를 들어 대시보드 라우트는 `/{current_team}/dashboard`가 되며, 팀 관리 페이지는 `settings/teams/{team}` 같은 라우트를 사용합니다. `{current_team}` 및 `{team}` 라우트 파라미터를 사용할 때, 스타터 키트는 라우트 접근을 허용하기 전에 인증된 사용자가 요청한 팀에 속해 있는지 자동으로 확인합니다.

<!-- To make generating team-aware URLs more convenient, the starter kits register URL defaults for the authenticated user's current team. This allows calls to helpers such as `route('dashboard')` to automatically include the current team's slug. When a user signs in, registers, or switches teams, the starter kits update the current team and refresh these URL defaults so generated links continue to use the correct team context. -->
팀을 고려한 URL을 더 편리하게 생성할 수 있도록, 스타터 키트는 인증된 사용자의 현재 팀에 대한 URL 기본값을 등록합니다. 이를 통해 `route('dashboard')` 같은 헬퍼 호출이 현재 팀의 슬러그를 자동으로 포함할 수 있습니다. 사용자가 로그인하거나 회원가입하거나 팀을 전환하면, 스타터 키트는 현재 팀을 업데이트하고 이러한 URL 기본값을 새로고침하여 생성된 링크가 계속 올바른 팀 컨텍스트를 사용하도록 합니다.

<!-- When creating or renaming a team, the starter kits also prevent users from choosing reserved names that could produce unsafe or conflicting route segments. For example, names that would collide with route prefixes such as `settings`, `login`, or `dashboard` may not be used. -->
팀을 생성하거나 이름을 변경할 때, 스타터 키트는 안전하지 않거나 충돌하는 라우트 세그먼트를 만들 수 있는 예약된 이름을 사용자가 선택하지 못하도록 방지합니다. 예를 들어 `settings`, `login`, `dashboard` 같은 라우트 접두어와 충돌할 수 있는 이름은 사용할 수 없습니다.

<a name="workos"></a>
<!-- ## WorkOS AuthKit Authentication -->
## WorkOS AuthKit Authentication

<!-- By default, the React, Svelte, Vue, and Livewire starter kits all utilize Laravel's built-in authentication system to offer login, registration, password reset, email verification, and more. In addition, we also offer a [WorkOS AuthKit](https://authkit.com) powered variant of each starter kit that offers: -->
기본적으로 React, Svelte, Vue, Livewire 스타터 키트는 모두 Laravel의 내장 인증 시스템을 사용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등을 제공합니다. 또한 각 스타터 키트에는 [WorkOS AuthKit](https://authkit.com) 기반 변형도 제공되며, 다음 기능을 제공합니다.

<div class="content-list" markdown="1">

<!-- - Social authentication (Google, Microsoft, GitHub, and Apple) - Passkey authentication - Email based "Magic Auth" - SSO -->
- 소셜 인증(Google, Microsoft, GitHub, Apple)
- 패스키 인증
- 이메일 기반 "Magic Auth"
- SSO

</div>

<!-- Using WorkOS as your authentication provider [requires a WorkOS account](https://workos.com). WorkOS offers free authentication for applications up to 1 million monthly active users. -->
WorkOS를 인증 제공자로 사용하려면 [requires a WorkOS account](https://workos.com)이 필요합니다. WorkOS는 월간 활성 사용자 100만 명 이하의 애플리케이션에 무료 인증을 제공합니다.

<!-- To use WorkOS AuthKit as your application's authentication provider, select the WorkOS option when creating your new starter kit powered application via `laravel new`. -->
WorkOS AuthKit을 애플리케이션의 인증 제공자로 사용하려면, `laravel new`를 통해 새 스타터 키트 기반 애플리케이션을 만들 때 WorkOS 옵션을 선택하십시오.

<a name="configuring-your-workos-starter-kit"></a>
<!-- ### Configuring Your WorkOS Starter Kit -->
### Configuring Your WorkOS Starter Kit

<!-- After creating a new application using a WorkOS powered starter kit, you should set the `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, and `WORKOS_REDIRECT_URL` environment variables in your application's `.env` file. These variables should match the values provided to you in the WorkOS dashboard for your application: -->
WorkOS 기반 스타터 키트를 사용하여 새 애플리케이션을 만든 후에는 애플리케이션의 `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 이 변수들은 WorkOS 대시보드에서 애플리케이션에 대해 제공된 값과 일치해야 합니다.

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

<!-- Additionally, you should configure the application homepage URL in your WorkOS dashboard. This URL is where users will be redirected after they log out of your application. -->
또한 WorkOS 대시보드에서 애플리케이션 홈페이지 URL을 설정해야 합니다. 이 URL은 사용자가 애플리케이션에서 로그아웃한 뒤 리디렉션될 위치입니다.

<a name="configuring-authkit-authentication-methods"></a>
<!-- #### Configuring AuthKit Authentication Methods -->
#### Configuring AuthKit Authentication Methods

<!-- When using a WorkOS powered starter kit, we recommend that you disable "Email + Password" authentication within your application's WorkOS AuthKit configuration settings, allowing users to only authenticate via social authentication providers, passkeys, "Magic Auth", and SSO. This allows your application to totally avoid handling user passwords. -->
WorkOS 기반 스타터 키트를 사용할 때는 애플리케이션의 WorkOS AuthKit 설정에서 "Email + Password" 인증을 비활성화하는 것을 권장합니다. 이렇게 하면 사용자는 소셜 인증 제공자, 패스키, "Magic Auth", SSO를 통해서만 인증할 수 있습니다. 이를 통해 애플리케이션은 사용자 비밀번호를 직접 처리하지 않아도 됩니다.

<a name="configuring-authkit-session-timeouts"></a>
<!-- #### Configuring AuthKit Session Timeouts -->
#### Configuring AuthKit Session Timeouts

<!-- In addition, we recommend that you configure your WorkOS AuthKit session inactivity timeout to match your Laravel application's configured session timeout threshold, which is typically two hours. -->
또한 WorkOS AuthKit 세션 비활성 타임아웃을 Laravel 애플리케이션에 설정된 세션 타임아웃 기준과 일치하도록 설정하는 것을 권장합니다. 일반적으로 이 값은 2시간입니다.

<a name="inertia-ssr"></a>
<!-- ### Inertia SSR -->
### Inertia SSR

<!-- The React, Svelte, and Vue starter kits are compatible with Inertia's [server-side rendering](https://inertiajs.com/server-side-rendering) capabilities. To build an Inertia SSR compatible bundle for your application, run the `build:ssr` command: -->
React, Svelte, Vue 스타터 키트는 Inertia의 [server-side rendering](https://inertiajs.com/server-side-rendering) 기능과 호환됩니다. 애플리케이션용 Inertia SSR 호환 번들을 빌드하려면 `build:ssr` 명령어를 실행하십시오.

```shell
npm run build:ssr
```

<!-- For convenience, a `composer dev:ssr` command is also available. This command will start the Laravel development server and Inertia SSR server after building an SSR compatible bundle for your application, allowing you to test your application locally using Inertia's server-side rendering engine: -->
편의를 위해 `composer dev:ssr` 명령어도 제공됩니다. 이 명령어는 애플리케이션용 SSR 호환 번들을 빌드한 뒤 Laravel 개발 서버와 Inertia SSR 서버를 시작합니다. 이를 통해 Inertia의 서버 사이드 렌더링 엔진을 사용하여 애플리케이션을 로컬에서 테스트할 수 있습니다.

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
<!-- ### Community Maintained Starter Kits -->
### Community Maintained Starter Kits

<!-- When creating a new Laravel application using the Laravel installer, you may provide any community maintained starter kit available on Packagist to the `--using` flag: -->
Laravel 설치 프로그램을 사용하여 새 Laravel 애플리케이션을 만들 때, Packagist에서 제공되는 커뮤니티 유지보수 스타터 키트를 `--using` 플래그에 지정할 수 있습니다.

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
<!-- #### Creating Starter Kits -->
#### Creating Starter Kits

<!-- To ensure your starter kit is available to others, you will need to publish it to [Packagist](https://packagist.org). Your starter kit should define its required environment variables in its `.env.example` file, and any necessary post-installation commands should be listed in the `post-create-project-cmd` array of the starter kit's `composer.json` file. -->
스타터 키트를 다른 사람들이 사용할 수 있도록 하려면 [Packagist](https://packagist.org)에 게시해야 합니다. 스타터 키트는 필요한 환경 변수를 `.env.example` 파일에 정의해야 하며, 필요한 설치 후 명령어는 스타터 키트의 `composer.json` 파일에 있는 `post-create-project-cmd` 배열에 나열해야 합니다.

<a name="faqs"></a>
<!-- ### Frequently Asked Questions -->
### Frequently Asked Questions

<a name="faq-upgrade"></a>
<!-- #### How do I upgrade? -->
#### How do I upgrade?

<!-- Every starter kit gives you a solid starting point for your next application. With full ownership of the code, you can tweak, customize, and build your application exactly as you envision. However, there is no need to update the starter kit itself. -->
모든 스타터 키트는 다음 애플리케이션을 위한 견고한 출발점을 제공합니다. 코드를 완전히 소유하므로, 애플리케이션을 원하는 모습에 맞게 조정하고 사용자 정의하며 구축할 수 있습니다. 그러나 스타터 키트 자체를 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
<!-- #### How do I enable email verification? -->
#### How do I enable email verification?

<!-- Email verification can be added by uncommenting the `MustVerifyEmail` import in your `App/Models/User.php` model and ensuring the model implements the `MustVerifyEmail` interface: -->
이메일 인증은 `App/Models/User.php` 모델에서 `MustVerifyEmail` import의 주석을 해제하고, 해당 모델이 `MustVerifyEmail` 인터페이스를 구현하도록 하면 추가할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
// ...

class User extends Authenticatable implements MustVerifyEmail
{
    // ...
}
```

<!-- After registration, users will receive a verification email. To restrict access to certain routes until the user's email address is verified, add the `verified` middleware to the routes: -->
회원가입 후 사용자는 인증 이메일을 받게 됩니다. 사용자의 이메일 주소가 인증될 때까지 특정 라우트에 대한 접근을 제한하려면 라우트에 `verified` 미들웨어를 추가하십시오.

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> 스타터 키트의 [WorkOS](#workos) 변형을 사용할 때는 이메일 인증이 필요하지 않습니다.

<a name="faq-modify-email-template"></a>
<!-- #### How do I modify the default email template? -->
#### How do I modify the default email template?

<!-- You may want to customize the default email template to better align with your application's branding. To modify this template, you should publish the email views to your application with the following command: -->
애플리케이션의 브랜딩에 더 잘 맞도록 기본 이메일 템플릿을 사용자 정의하고 싶을 수 있습니다. 이 템플릿을 수정하려면 다음 명령어로 이메일 뷰를 애플리케이션에 게시해야 합니다.

```shell
php artisan vendor:publish --tag=laravel-mail
```

<!-- This will generate several files in `resources/views/vendor/mail`. You can modify any of these files as well as the `resources/views/vendor/mail/themes/default.css` file to change the look and appearance of the default email template. -->
이 명령어는 `resources/views/vendor/mail`에 여러 파일을 생성합니다. 기본 이메일 템플릿의 모양과 외형을 변경하려면 이 파일들뿐만 아니라 `resources/views/vendor/mail/themes/default.css` 파일도 수정할 수 있습니다.
