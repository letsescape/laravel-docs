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
新しい Laravel アプリケーションの構築をすぐに始められるように、[application starter kits](https://laravel.com/starter-kits) を提供させていただきます。これらのスターター キットを使用すると、次の Laravel アプリケーションの構築をスムーズに始めることができ、アプリケーションのユーザーを登録および認証するために必要なルート、コントローラ、ビューが含まれています。スターター キットは、[Laravel Fortify](/docs/13.x/fortify) を使用して認証を提供します。

<!-- While you are welcome to use these starter kits, they are not required. You are free to build your own application from the ground up by simply installing a fresh copy of Laravel. Either way, we know you will build something great! -->
これらのスターター キットを使用しても構いませんが、必須ではありません。 Laravel の新しいコピーをインストールするだけで、独自のアプリケーションを最初から自由に構築できます。いずれにせよ、私たちはあなたが素晴らしいものを作り上げることを確信しています。

<a name="creating-an-application"></a>
<!-- ## Creating an Application Using a Starter Kit -->
## Creating an Application Using a Starter Kit

<!-- To create a new Laravel application using one of our starter kits, you should first [install PHP and the Laravel CLI tool](/docs/13.x/installation#installing-php). If you already have PHP and Composer installed, you may install the Laravel installer CLI tool via Composer: -->
スターターキットのいずれかを使用して新しい Laravel アプリケーションを作成するには、まず [install PHP and the Laravel CLI tool](/docs/13.x/installation#installing-php) を実行する必要があります。すでに PHP と Composer がインストールされている場合は、Composer 経由で Laravel インストーラー CLI ツールをインストールできます。

```shell
composer global require laravel/installer
```

<!-- Then, create a new Laravel application using the Laravel installer CLI. The Laravel installer will prompt you to select your preferred starter kit: -->
次に、Laravel インストーラー CLI を使用して、新しい Laravel アプリケーションを作成します。 Laravel インストーラーは、好みのスターター キットを選択するよう求めます。

```shell
laravel new my-app
```

<!-- After creating your Laravel application, you only need to install its frontend dependencies via NPM and start the Laravel development server: -->
Laravel アプリケーションを作成した後、NPM 経由でフロントエンドの依存関係をインストールし、Laravel 開発サーバーを起動するだけです。

```shell
cd my-app
npm install && npm run build
composer run dev
```

<!-- Once you have started the Laravel development server, your application will be accessible in your web browser at [http://localhost:8000](http://localhost:8000). -->
Laravel 開発サーバーを起動すると、Web ブラウザー ([http://localhost:8000](http://localhost:8000)) でアプリケーションにアクセスできるようになります。

<a name="available-starter-kits"></a>
<!-- ## Available Starter Kits -->
## Available Starter Kits

<a name="react"></a>
<!-- ### React -->
### React

<!-- Our React starter kit provides a robust, modern starting point for building Laravel applications with a React frontend using [Inertia](https://inertiajs.com). -->
当社の React スターター キットは、[Inertia](https://inertiajs.com) を使用して React フロントエンドで Laravel アプリケーションを構築するための堅牢で最新の開始点を提供します。

<!-- Inertia allows you to build modern, single-page React applications using classic server-side routing and controllers. This lets you enjoy the frontend power of React combined with the incredible backend productivity of Laravel and lightning-fast Vite compilation. -->
Inertia を使用すると、従来のサーバー側のルーティングとコントローラを使用して、最新の単一ページの React アプリケーションを構築できます。これにより、React のフロントエンドのパワーと、Laravel の驚異的なバックエンドの生産性および超高速の Vite コンパイルを組み合わせて楽しむことができます。

<!-- The React starter kit utilizes React 19, TypeScript, Tailwind, and the [shadcn/ui](https://ui.shadcn.com) component library. -->
React スターター キットは、React 19、TypeScript、Tailwind、および [shadcn/ui](https://ui.shadcn.com) コンポーネント ライブラリを利用します。

<a name="svelte"></a>
<!-- ### Svelte -->
### Svelte

<!-- Our Svelte starter kit provides a robust, modern starting point for building Laravel applications with a Svelte frontend using [Inertia](https://inertiajs.com). -->
当社の Svelte スターター キットは、[Inertia](https://inertiajs.com) を使用して Svelte フロントエンドを備えた Laravel アプリケーションを構築するための堅牢で最新の開始点を提供します。

<!-- Inertia allows you to build modern, single-page Svelte applications using classic server-side routing and controllers. This lets you enjoy the frontend power of Svelte combined with the incredible backend productivity of Laravel and lightning-fast Vite compilation. -->
Inertia を使用すると、従来のサーバー側のルーティングとコントローラを使用して、最新の単一ページの Svelte アプリケーションを構築できます。これにより、Svelte のフロントエンドのパワーと、Laravel の驚異的なバックエンドの生産性および超高速の Vite コンパイルを組み合わせて楽しむことができます。

<!-- The Svelte starter kit utilizes Svelte 5, TypeScript, Tailwind, and the [shadcn-svelte](https://www.shadcn-svelte.com/) component library. -->
Svelte スターター キットは、Svelte 5、TypeScript、Tailwind、および [shadcn-svelte](https://www.shadcn-svelte.com/) コンポーネント ライブラリを利用します。

<a name="vue"></a>
<!-- ### Vue -->
### Vue

<!-- Our Vue starter kit provides a great starting point for building Laravel applications with a Vue frontend using [Inertia](https://inertiajs.com). -->
Vue スターター キットは、[Inertia](https://inertiajs.com) を使用して Vue フロントエンドで Laravel アプリケーションを構築するための優れた開始点を提供します。

<!-- Inertia allows you to build modern, single-page Vue applications using classic server-side routing and controllers. This lets you enjoy the frontend power of Vue combined with the incredible backend productivity of Laravel and lightning-fast Vite compilation. -->
Inertia を使用すると、従来のサーバー側のルーティングとコントローラを使用して、最新の単一ページの Vue アプリケーションを構築できます。これにより、Vue のフロントエンドのパワーと、Laravel の驚異的なバックエンドの生産性および超高速の Vite コンパイルを組み合わせて楽しむことができます。

<!-- The Vue starter kit utilizes the Vue Composition API, TypeScript, Tailwind, and the [shadcn-vue](https://www.shadcn-vue.com/) component library. -->
Vue スターター キットは、Vue Composition API、TypeScript、Tailwind、および [shadcn-vue](https://www.shadcn-vue.com/) コンポーネント ライブラリを利用します。

<a name="livewire"></a>
<!-- ### Livewire -->
### Livewire

<!-- Our Livewire starter kit provides the perfect starting point for building Laravel applications with a [Laravel Livewire](https://livewire.laravel.com) frontend. -->
当社の Livewire スターター キットは、[Laravel Livewire](https://livewire.laravel.com) フロントエンドを使用して Laravel アプリケーションを構築するための完璧な開始点を提供します。

<!-- Livewire is a powerful way of building dynamic, reactive, frontend UIs using just PHP. It's a great fit for teams that primarily use Blade templates and are looking for a simpler alternative to JavaScript-driven SPA frameworks like React, Svelte, and Vue. -->
Livewire は、PHP だけを使用して動的でリアクティブなフロントエンド UI を構築する強力な方法です。これは、主に Blade テンプレートを使用し、React、Svelte、Vue などの JavaScript 駆動の SPA フレームワークのよりシンプルな代替手段を探しているチームに最適です。

<!-- The Livewire starter kit utilizes Livewire, Tailwind, and the [Flux UI](https://fluxui.dev) component library. -->
Livewire スターター キットは、Livewire、Tailwind、および [Flux UI](https://fluxui.dev) コンポーネント ライブラリを利用します。

<a name="starter-kit-customization"></a>
<!-- ## Starter Kit Customization -->
## Starter Kit Customization

<a name="react-customization"></a>
<!-- ### React -->
### React

<!-- Our React starter kit is built with Inertia 3, React 19, Tailwind 4, and [shadcn/ui](https://ui.shadcn.com). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization. -->
当社の React スターター キットは、Inertia 3、React 19、Tailwind 4、および [shadcn/ui](https://ui.shadcn.com) で構築されています。すべてのスターター キットと同様に、バックエンドとフロントエンドのコードはすべてアプリケーション内に存在し、完全なカスタマイズが可能です。

<!-- The majority of the frontend code is located in the `resources/js` directory. You are free to modify any of the code to customize the appearance and behavior of your application: -->
フロントエンド コードの大部分は、`resources/js` ディレクトリにあります。コードを自由に変更して、アプリケーションの外観と動作をカスタマイズできます。

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
追加の shadcn コンポーネントを公開するには、まず [find the component you want to publish](https://ui.shadcn.com) を実行します。次に、`npx` を使用してコンポーネントを公開します。

```shell
npx shadcn@latest add switch
```

<!-- In this example, the command will publish the Switch component to `resources/js/components/ui/switch.tsx`. Once the component has been published, you can use it in any of your pages: -->
この例では、コマンドはスイッチ コンポーネントを `resources/js/components/ui/switch.tsx` に公開します。コンポーネントが公開されると、どのページでも使用できるようになります。

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
React スターター キットには、「サイドバー」レイアウトと「ヘッダー」レイアウトという 2 つの異なる主なレイアウトから選択できます。サイドバー レイアウトがデフォルトですが、アプリケーションの `resources/js/layouts/app-layout.tsx` ファイルの先頭にインポートされるレイアウトを変更することで、ヘッダー レイアウトに切り替えることができます。

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
<!-- #### Sidebar Variants -->
#### Sidebar Variants

<!-- The sidebar layout includes three different variants: the default sidebar variant, the "inset" variant, and the "floating" variant. You may choose the variant you like best by modifying the `resources/js/components/app-sidebar.tsx` component: -->
サイドバーのレイアウトには、デフォルトのサイドバー バリアント、「インセット」バリアント、および「フローティング」バリアントの 3 つの異なるバリアントが含まれています。 `resources/js/components/app-sidebar.tsx` コンポーネントを変更することで、最も好みのバリアントを選択できます。

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
<!-- #### Authentication Page Layout Variants -->
#### Authentication Page Layout Variants

<!-- The authentication pages included with the React starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split". -->
React スターター キットに含まれる認証ページ (ログイン ページや登録ページなど) にも、「シンプル」、「カード」、「分割」の 3 つの異なるレイアウト バリアントが提供されています。

<!-- To change your authentication layout, modify the layout that is imported at the top of your application's `resources/js/layouts/auth-layout.tsx` file: -->
認証レイアウトを変更するには、アプリケーションの `resources/js/layouts/auth-layout.tsx` ファイルの先頭にインポートされるレイアウトを変更します。

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="svelte-customization"></a>
<!-- ### Svelte -->
### Svelte

<!-- Our Svelte starter kit is built with Inertia 3, Svelte 5, Tailwind, and [shadcn-svelte](https://www.shadcn-svelte.com/). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization. -->
当社の Svelte スターター キットは、Inertia 3、Svelte 5、Tailwind、および [shadcn-svelte](https://www.shadcn-svelte.com/) で構築されています。すべてのスターター キットと同様に、バックエンドとフロントエンドのコードはすべてアプリケーション内に存在し、完全なカスタマイズが可能です。

<!-- The majority of the frontend code is located in the `resources/js` directory. You are free to modify any of the code to customize the appearance and behavior of your application: -->
フロントエンド コードの大部分は、`resources/js` ディレクトリにあります。コードを自由に変更して、アプリケーションの外観と動作をカスタマイズできます。

```text
resources/js/
├── components/    # Reusable Svelte components
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration and Svelte rune modules
├── pages/         # Page components
└── types/         # TypeScript definitions
```

<!-- To publish additional shadcn-svelte components, first [find the component you want to publish](https://www.shadcn-svelte.com). Then, publish the component using `npx`: -->
追加の shadcn-svelte コンポーネントを公開するには、まず [find the component you want to publish](https://www.shadcn-svelte.com) を実行します。次に、`npx` を使用してコンポーネントを公開します。

```shell
npx shadcn-svelte@latest add switch
```

<!-- In this example, the command will publish the Switch component to `resources/js/components/ui/switch/switch.svelte`. Once the component has been published, you can use it in any of your pages: -->
この例では、コマンドはスイッチ コンポーネントを `resources/js/components/ui/switch/switch.svelte` に公開します。コンポーネントが公開されると、どのページでも使用できるようになります。

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
Svelte スターター キットには、「サイドバー」レイアウトと「ヘッダー」レイアウトという 2 つの異なる主なレイアウトから選択できます。サイドバー レイアウトがデフォルトですが、アプリケーションの `resources/js/layouts/AppLayout.svelte` ファイルの先頭にインポートされるレイアウトを変更することで、ヘッダー レイアウトに切り替えることができます。

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.svelte'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.svelte'; // [tl! add]
```

<a name="svelte-sidebar-variants"></a>
<!-- #### Sidebar Variants -->
#### Sidebar Variants

<!-- The sidebar layout includes three different variants: the default sidebar variant, the "inset" variant, and the "floating" variant. You may choose the variant you like best by modifying the `resources/js/components/AppSidebar.svelte` component: -->
サイドバーのレイアウトには、デフォルトのサイドバー バリアント、「インセット」バリアント、および「フローティング」バリアントの 3 つの異なるバリアントが含まれています。 `resources/js/components/AppSidebar.svelte` コンポーネントを変更することで、最も好みのバリアントを選択できます。

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="svelte-authentication-page-layout-variants"></a>
<!-- #### Authentication Page Layout Variants -->
#### Authentication Page Layout Variants

<!-- The authentication pages included with the Svelte starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split". -->
Svelte スターター キットに含まれる認証ページ (ログイン ページや登録ページなど) にも、「シンプル」、「カード」、「分割」の 3 つの異なるレイアウト バリアントが用意されています。

<!-- To change your authentication layout, modify the layout that is imported at the top of your application's `resources/js/layouts/AuthLayout.svelte` file: -->
認証レイアウトを変更するには、アプリケーションの `resources/js/layouts/AuthLayout.svelte` ファイルの先頭にインポートされるレイアウトを変更します。

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.svelte'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.svelte'; // [tl! add]
```

<a name="vue-customization"></a>
<!-- ### Vue -->
### Vue

<!-- Our Vue starter kit is built with Inertia 3, Vue 3 Composition API, Tailwind, and [shadcn-vue](https://www.shadcn-vue.com/). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization. -->
Vue スターター キットは、Inertia 3、Vue 3 Composition API、Tailwind、および [shadcn-vue](https://www.shadcn-vue.com/) で構築されています。すべてのスターター キットと同様に、バックエンドとフロントエンドのコードはすべてアプリケーション内に存在し、完全なカスタマイズが可能です。

<!-- The majority of the frontend code is located in the `resources/js` directory. You are free to modify any of the code to customize the appearance and behavior of your application: -->
フロントエンド コードの大部分は、`resources/js` ディレクトリにあります。コードを自由に変更して、アプリケーションの外観と動作をカスタマイズできます。

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
追加の shadcn-vue コンポーネントを公開するには、まず [find the component you want to publish](https://www.shadcn-vue.com) を実行します。次に、`npx` を使用してコンポーネントを公開します。

```shell
npx shadcn-vue@latest add switch
```

<!-- In this example, the command will publish the Switch component to `resources/js/components/ui/Switch.vue`. Once the component has been published, you can use it in any of your pages: -->
この例では、コマンドはスイッチ コンポーネントを `resources/js/components/ui/Switch.vue` に公開します。コンポーネントが公開されると、どのページでも使用できるようになります。

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
Vue スターター キットには、「サイドバー」レイアウトと「ヘッダー」レイアウトという 2 つの異なる主なレイアウトから選択できます。サイドバー レイアウトがデフォルトですが、アプリケーションの `resources/js/layouts/AppLayout.vue` ファイルの先頭にインポートされるレイアウトを変更することで、ヘッダー レイアウトに切り替えることができます。

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
<!-- #### Sidebar Variants -->
#### Sidebar Variants

<!-- The sidebar layout includes three different variants: the default sidebar variant, the "inset" variant, and the "floating" variant. You may choose the variant you like best by modifying the `resources/js/components/AppSidebar.vue` component: -->
サイドバーのレイアウトには、デフォルトのサイドバー バリアント、「インセット」バリアント、および「フローティング」バリアントの 3 つの異なるバリアントが含まれています。 `resources/js/components/AppSidebar.vue` コンポーネントを変更することで、最も好みのバリアントを選択できます。

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
<!-- #### Authentication Page Layout Variants -->
#### Authentication Page Layout Variants

<!-- The authentication pages included with the Vue starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split". -->
ログイン ページや登録ページなど、Vue スターター キットに含まれる認証ページにも、「シンプル」、「カード」、「分割」の 3 つの異なるレイアウト バリアントが提供されています。

<!-- To change your authentication layout, modify the layout that is imported at the top of your application's `resources/js/layouts/AuthLayout.vue` file: -->
認証レイアウトを変更するには、アプリケーションの `resources/js/layouts/AuthLayout.vue` ファイルの先頭にインポートされるレイアウトを変更します。

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
<!-- ### Livewire -->
### Livewire

<!-- Our Livewire starter kit is built with Livewire 4, Tailwind, and [Flux UI](https://fluxui.dev/). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization. -->
当社の Livewire スターター キットは、Livewire 4、Tailwind、および [Flux UI](https://fluxui.dev/) で構築されています。すべてのスターター キットと同様に、バックエンドとフロントエンドのコードはすべてアプリケーション内に存在し、完全なカスタマイズが可能です。

<!-- The majority of the frontend code is located in the `resources/views` directory. You are free to modify any of the code to customize the appearance and behavior of your application: -->
フロントエンド コードの大部分は、`resources/views` ディレクトリにあります。コードを自由に変更して、アプリケーションの外観と動作をカスタマイズできます。

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
Livewire スターター キットには、「サイドバー」レイアウトと「ヘッダー」レイアウトという 2 つの異なる主なレイアウトから選択できます。サイドバー レイアウトがデフォルトですが、アプリケーションの `resources/views/layouts/app.blade.php` ファイルで使用されるレイアウトを変更することで、ヘッダー レイアウトに切り替えることができます。さらに、メインの Flux コンポーネントに `container` 属性を追加する必要があります。

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
Livewire スターター キットに含まれる認証ページ (ログイン ページや登録ページなど) にも、「シンプル」、「カード」、「分割」という 3 つの異なるレイアウト バリアントが用意されています。

<!-- To change your authentication layout, modify the layout that is used by your application's `resources/views/layouts/auth.blade.php` file: -->
認証レイアウトを変更するには、アプリケーションの `resources/views/layouts/auth.blade.php` ファイルで使用されるレイアウトを変更します。

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a name="authentication"></a>
<!-- ## Authentication -->
## Authentication

<!-- All starter kits use [Laravel Fortify](/docs/13.x/fortify) to handle authentication. Fortify provides routes, controllers, and logic for login, registration, password reset, email verification, and more. -->
すべてのスターター キットは、[Laravel Fortify](/docs/13.x/fortify) を使用して認証を処理します。 Fortify は、ログイン、登録、パスワードのリセット、電子メール検証などのためのルート、コントローラ、ロジックを提供します。

<!-- Fortify automatically registers the following authentication routes based on the features that are enabled in your application's `config/fortify.php` configuration file: -->
Fortify は、アプリケーションの `config/fortify.php` 構成ファイルで有効になっている機能に基づいて、次の認証ルートを自動的に登録します。

<div class="overflow-auto">

<!-- | Route | Method | Description | | ---------------------------------- | ------ | ----------------------------------- | | `/login` | `GET` | Display login form | | `/login` | `POST` | Authenticate user | | `/logout` | `POST` | Log user out | | `/register` | `GET` | Display registration form | | `/register` | `POST` | Create new user | | `/forgot-password` | `GET` | Display password reset request form | | `/forgot-password` | `POST` | Send password reset link | | `/reset-password/{token}` | `GET` | Display password reset form | | `/reset-password` | `POST` | Update password | | `/email/verify` | `GET` | Display email verification notice | | `/email/verify/{id}/{hash}` | `GET` | Verify email address | | `/email/verification-notification` | `POST` | Resend verification email | | `/user/confirm-password` | `GET` | Display password confirmation form | | `/user/confirm-password` | `POST` | Confirm password | | `/two-factor-challenge` | `GET` | Display 2FA challenge form | | `/two-factor-challenge` | `POST` | Verify 2FA code | -->
| ルート                              | 方法 | 説明                         |
| ---------------------------------- | ------ | ----------------------------------- |
| `/login`                           | `GET`    | ログインフォームを表示する                  |
| `/login`                           | `POST`   | ユーザーを認証する                   |
| `/logout`                          | `POST`   | ユーザーをログアウトする                        |
| `/register`                        | `GET`    | 登録フォームを表示する           |
| `/register`                        | `POST`   | 新しいユーザーを作成する                     |
| `/forgot-password`                 | `GET`    | パスワードリセットリクエストフォームを表示する |
| `/forgot-password`                 | `POST`   | パスワードリセットリンクを送信する            |
| `/reset-password/{token}`          | `GET`    | パスワードリセットフォームを表示する         |
| `/reset-password`                  | `POST`   | パスワードを更新する                     |
| `/email/verify`                    | `GET`    | メール認証通知を表示する   |
| `/email/verify/{id}/{hash}`        | `GET`    | メールアドレスを確認してください                |
| `/email/verification-notification` | `POST`   | 確認メールを再送信する           |
| `/user/confirm-password`           | `GET`    | パスワード確認フォームを表示する  |
| `/user/confirm-password`           | `POST`   | パスワードを認証する                    |
| `/two-factor-challenge`            | `GET`    | 2FA チャレンジフォームを表示する          |
| `/two-factor-challenge`            | `POST`   | 2FA コードを検証する                     |

</div>

<!-- The `php artisan route:list` Artisan command can be used to display all of the routes in your application. -->
`php artisan route:list` Artisan コマンドを使用すると、アプリケーション内のすべてのルートを表示できます。

<a name="enabling-and-disabling-features"></a>
<!-- ### Enabling and Disabling Features -->
### Enabling and Disabling Features

<!-- You can control which Fortify features are enabled in your application's `config/fortify.php` configuration file: -->
どの Fortify 機能を有効にするかは、アプリケーションの `config/fortify.php` 構成ファイルで制御できます。

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
機能を無効にするには、その機能エントリを `features` 配列からコメント アウトするか削除します。たとえば、パブリック登録を無効にするには、`Features::registration()` を削除します。

<!-- When using the [React](#react), [Svelte](#svelte) or [Vue](#vue) starter kits, you will also need to remove any references to the disabled feature's routes in your frontend code. For example, if you disable email verification, you should remove the imports and references to the `verification` routes in your React, Svelte, or Vue components. This is necessary because these starter kits use Wayfinder for type-safe routing, which generates route definitions at build time. If you reference routes that no longer exist, your application will fail to build. -->
[React](#react)、[Svelte](#svelte)、または [Vue](#vue) スターター キットを使用する場合は、フロントエンド コード内の無効な機能のルートへの参照も削除する必要があります。たとえば、電子メール検証を無効にする場合は、React、Svelte、または Vue コンポーネント内の `verification` ルートへのインポートと参照を削除する必要があります。これらのスターター キットは、ビルド時にルート定義を生成するタイプ セーフ ルーティングに Wayfinder を使用するため、これが必要です。存在しないルートを参照すると、アプリケーションのビルドは失敗します。

<a name="customizing-actions"></a>
<!-- ### Customizing User Creation and Password Reset -->
### Customizing User Creation and Password Reset

<!-- When a user registers or resets their password, Fortify invokes action classes located in your application's `app/Actions/Fortify` directory: -->
ユーザーがパスワードを登録またはリセットすると、Fortify はアプリケーションの `app/Actions/Fortify` ディレクトリにあるアクション クラスを呼び出します。

<div class="overflow-auto">

<!-- | File | Description | | ----------------------------- | ------------------------------------- | | `CreateNewUser.php` | Validates and creates new users | | `ResetUserPassword.php` | Validates and updates user passwords | | `PasswordValidationRules.php` | Defines password validation rules | -->
| ファイル                          | 説明                           |
| ----------------------------- | ------------------------------------- |
| `CreateNewUser.php`           | 新しいユーザーを検証して作成します       |
| `ResetUserPassword.php`       | ユーザーのパスワードを検証して更新します  |
| `PasswordValidationRules.php` | パスワード検証ルールを定義します     |

</div>

<!-- For example, to customize your application's registration logic, you should edit the `CreateNewUser` action: -->
たとえば、アプリケーションの登録ロジックをカスタマイズするには、`CreateNewUser` アクションを編集する必要があります。

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
スターター キットには 2 要素認証 (2FA) が組み込まれており、ユーザーは TOTP 互換の認証アプリを使用してアカウントを保護できます。 2FA は、アプリケーションの `config/fortify.php` 構成ファイルの `Features::twoFactorAuthentication()` によってデフォルトで有効になります。

<!-- The `confirm` option requires users to verify a code before 2FA is fully enabled, while `confirmPassword` requires password confirmation before enabling or disabling 2FA. For more details, see [Fortify's two-factor authentication documentation](/docs/13.x/fortify#two-factor-authentication). -->
`confirm` オプションでは、2FA を完全に有効にする前にユーザーがコードを検証する必要がありますが、`confirmPassword` では、2FA を有効または無効にする前にパスワードの確認が必要です。詳細については、[Fortify's two-factor authentication documentation](/docs/13.x/fortify#two-factor-authentication) を参照してください。

<a name="rate-limiting"></a>
<!-- ### Rate Limiting -->
### Rate Limiting

<!-- Rate limiting prevents brute-forcing and repeated login attempts from overwhelming your authentication endpoints. You can customize Fortify's rate limiting behavior in your application's `FortifyServiceProvider`: -->
レート制限により、ブルートフォース攻撃やログイン試行の繰り返しによって認証エンドポイントに負荷がかかるのを防ぎます。 Fortify のレート制限動作は、アプリケーションの `FortifyServiceProvider` でカスタマイズできます。

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
React、Svelte、Vue、および Livewire スターター キットは、チーム サポートによって生成することもできます。チーム機能が有効になっている場合、各ユーザーは 1 つ以上のチームに属し、現在のチームを持ちます。登録中に、新規ユーザーには自動的に個人チームが与えられます。スターター キットには、チームの作成、チーム間の切り替え、メンバーの招待、チームの詳細の更新を行うためのチーム管理画面も含まれています。

<!-- When a route is scoped to the current team, the current team's slug is included in the URL. For example, the dashboard route becomes `/{current_team}/dashboard`, while team management pages use routes such as `settings/teams/{team}`. When using the `{current_team}` and `{team}` route parameters, the starter kits automatically ensure that the authenticated user belongs to the requested team before allowing access to the route. -->
ルートのスコープが現在のチームに設定されている場合、現在のチームのスラッグが URL に含まれます。たとえば、ダッシュボードのルートは `/{current_team}/dashboard` になりますが、チーム管理ページでは `settings/teams/{team}` などのルートが使用されます。 `{current_team}` および `{team}` ルート パラメーターを使用する場合、スターター キットは、ルートへのアクセスを許可する前に、認証されたユーザーが要求されたチームに属していることを自動的に確認します。

<!-- To make generating team-aware URLs more convenient, the starter kits register URL defaults for the authenticated user's current team. This allows calls to helpers such as `route('dashboard')` to automatically include the current team's slug. When a user signs in, registers, or switches teams, the starter kits update the current team and refresh these URL defaults so generated links continue to use the correct team context. -->
チーム対応 URL の生成をより便利にするために、スターター キットは認証されたユーザーの現在のチームの URL デフォルトを登録します。これにより、`route('dashboard')` などのヘルパの呼び出しに現在のチームのスラッグを自動的に含めることができます。ユーザーがサインイン、登録、またはチームの切り替えを行うと、スターター キットによって現在のチームが更新され、これらの URL デフォルトが更新されるため、生成されたリンクは引き続き正しいチーム コンテキストを使用します。

<!-- When creating or renaming a team, the starter kits also prevent users from choosing reserved names that could produce unsafe or conflicting route segments. For example, names that would collide with route prefixes such as `settings`, `login`, or `dashboard` may not be used. -->
スターター キットは、チームを作成または名前変更するときに、安全でないルート セグメントや競合するルート セグメントを生成する可能性のある予約名をユーザーが選択することも防止します。たとえば、`settings`、`login`、`dashboard` などのルート プレフィックスと衝突する名前は使用できません。

<a name="workos"></a>
<!-- ## WorkOS AuthKit Authentication -->
## WorkOS AuthKit Authentication

<!-- By default, the React, Svelte, Vue, and Livewire starter kits all utilize Laravel's built-in authentication system to offer login, registration, password reset, email verification, and more. In addition, we also offer a [WorkOS AuthKit](https://authkit.com) powered variant of each starter kit that offers: -->
デフォルトでは、React、Svelte、Vue、Livewire スターター キットはすべて、Laravel の組み込み認証システムを利用して、ログイン、登録、パスワードリセット、電子メール検証などを提供します。さらに、以下を提供する各スターター キットの [WorkOS AuthKit](https://authkit.com) パワード バリアントも提供しています。

<div class="content-list" markdown="1">

<!-- - Social authentication (Google, Microsoft, GitHub, and Apple) - Passkey authentication - Email based "Magic Auth" - SSO -->
- ソーシャル認証 (Google、Microsoft、GitHub、Apple)
- パスキー認証
- メールベースの「Magic Auth」
- SSO

</div>

<!-- Using WorkOS as your authentication provider [requires a WorkOS account](https://workos.com). WorkOS offers free authentication for applications up to 1 million monthly active users. -->
WorkOS を認証プロバイダ [requires a WorkOS account](https://workos.com) として使用します。 WorkOS は、月間アクティブ ユーザー 100 万人までのアプリケーションに対して無料の認証を提供します。

<!-- To use WorkOS AuthKit as your application's authentication provider, select the WorkOS option when creating your new starter kit powered application via `laravel new`. -->
WorkOS AuthKit をアプリケーションの認証プロバイダとして使用するには、`laravel new` 経由で新しいスターター キットを利用したアプリケーションを作成するときに、WorkOS オプションを選択します。

<a name="configuring-your-workos-starter-kit"></a>
<!-- ### Configuring Your WorkOS Starter Kit -->
### Configuring Your WorkOS Starter Kit

<!-- After creating a new application using a WorkOS powered starter kit, you should set the `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, and `WORKOS_REDIRECT_URL` environment variables in your application's `.env` file. These variables should match the values provided to you in the WorkOS dashboard for your application: -->
WorkOS 搭載スターター キットを使用して新しいアプリケーションを作成した後、アプリケーションの `.env` ファイルに `WORKOS_CLIENT_ID`、`WORKOS_API_KEY`、および `WORKOS_REDIRECT_URL` 環境変数を設定する必要があります。これらの変数は、アプリケーションの WorkOS ダッシュボードで提供される値と一致する必要があります。

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

<!-- Additionally, you should configure the application homepage URL in your WorkOS dashboard. This URL is where users will be redirected after they log out of your application. -->
さらに、WorkOS ダッシュボードでアプリケーションのホームページ URL を構成する必要があります。この URL は、ユーザーがアプリケーションからログアウトした後にリダイレクトされる場所です。

<a name="configuring-authkit-authentication-methods"></a>
<!-- #### Configuring AuthKit Authentication Methods -->
#### Configuring AuthKit Authentication Methods

<!-- When using a WorkOS powered starter kit, we recommend that you disable "Email + Password" authentication within your application's WorkOS AuthKit configuration settings, allowing users to only authenticate via social authentication providers, passkeys, "Magic Auth", and SSO. This allows your application to totally avoid handling user passwords. -->
WorkOS を利用したスターター キットを使用する場合は、アプリケーションの WorkOS AuthKit 構成設定内で「電子メール + パスワード」認証を無効にし、ユーザーがソーシャル認証プロバイダ、パスキー、「Magic Auth」、および SSO を介してのみ認証できるようにすることをお勧めします。これにより、アプリケーションはユーザー パスワードの処理を完全に回避できます。

<a name="configuring-authkit-session-timeouts"></a>
<!-- #### Configuring AuthKit Session Timeouts -->
#### Configuring AuthKit Session Timeouts

<!-- In addition, we recommend that you configure your WorkOS AuthKit session inactivity timeout to match your Laravel application's configured session timeout threshold, which is typically two hours. -->
さらに、Laravel アプリケーションに設定されているセッション タイムアウトしきい値 (通常は 2 時間) と一致するように、WorkOS AuthKit セッションの非アクティブ タイムアウトを設定することをお勧めします。

<a name="inertia-ssr"></a>
<!-- ### Inertia SSR -->
### Inertia SSR

<!-- The React, Svelte, and Vue starter kits are compatible with Inertia's [server-side rendering](https://inertiajs.com/server-side-rendering) capabilities. To build an Inertia SSR compatible bundle for your application, run the `build:ssr` command: -->
React、Svelte、および Vue スターター キットは、Inertia の [server-side rendering](https://inertiajs.com/server-side-rendering) 機能と互換性があります。アプリケーション用の Inertia SSR 互換バンドルを構築するには、`build:ssr` コマンドを実行します。

```shell
npm run build:ssr
```

<!-- For convenience, a `composer dev:ssr` command is also available. This command will start the Laravel development server and Inertia SSR server after building an SSR compatible bundle for your application, allowing you to test your application locally using Inertia's server-side rendering engine: -->
便宜上、`composer dev:ssr` コマンドも使用できます。このコマンドは、アプリケーション用の SSR 互換バンドルを構築した後、Laravel 開発サーバーと Inertia SSR サーバーを起動し、Inertia のサーバー側レンダリング エンジンを使用してアプリケーションをローカルでテストできるようにします。

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
<!-- ### Community Maintained Starter Kits -->
### Community Maintained Starter Kits

<!-- When creating a new Laravel application using the Laravel installer, you may provide any community maintained starter kit available on Packagist to the `--using` flag: -->
Laravel インストーラーを使用して新しい Laravel アプリケーションを作成する場合、Packagist で入手可能なコミュニティが管理するスターター キットを `--using` フラグに提供できます。

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
<!-- #### Creating Starter Kits -->
#### Creating Starter Kits

<!-- To ensure your starter kit is available to others, you will need to publish it to [Packagist](https://packagist.org). Your starter kit should define its required environment variables in its `.env.example` file, and any necessary post-installation commands should be listed in the `post-create-project-cmd` array of the starter kit's `composer.json` file. -->
スターター キットを他の人が確実に利用できるようにするには、[Packagist](https://packagist.org) に公開する必要があります。スターター キットは、`.env.example` ファイルで必要な環境変数を定義する必要があり、必要なインストール後のコマンドはスターター キットの `composer.json` ファイルの `post-create-project-cmd` 配列にリストされている必要があります。

<a name="faqs"></a>
<!-- ### Frequently Asked Questions -->
### Frequently Asked Questions

<a name="faq-upgrade"></a>
<!-- #### How do I upgrade? -->
#### How do I upgrade?

<!-- Every starter kit gives you a solid starting point for your next application. With full ownership of the code, you can tweak, customize, and build your application exactly as you envision. However, there is no need to update the starter kit itself. -->
すべてのスターター キットは、次のアプリケーションへの確実な出発点となります。コードの完全な所有権があれば、思い描いたとおりにアプリケーションを調整、カスタマイズ、構築できます。ただし、スターター キット自体をアップデートする必要はありません。

<a name="faq-enable-email-verification"></a>
<!-- #### How do I enable email verification? -->
#### How do I enable email verification?

<!-- Email verification can be added by uncommenting the `MustVerifyEmail` import in your `App/Models/User.php` model and ensuring the model implements the `MustVerifyEmail` interface: -->
電子メール検証を追加するには、`App/Models/User.php` モデル内の `MustVerifyEmail` インポートのコメントを解除し、モデルが `MustVerifyEmail` インターフェイスを実装していることを確認します。

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
登録後、ユーザーは確認メールを受け取ります。ユーザーの電子メール アドレスが確認されるまで特定のルートへのアクセスを制限するには、`verified` ミドルウェアをルートに追加します。

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> スターター キットの [WorkOS](#workos) バリアントを使用する場合、電子メール検証は必要ありません。

<a name="faq-modify-email-template"></a>
<!-- #### How do I modify the default email template? -->
#### How do I modify the default email template?

<!-- You may want to customize the default email template to better align with your application's branding. To modify this template, you should publish the email views to your application with the following command: -->
デフォルトの電子メール テンプレートをカスタマイズして、アプリケーションのブランドに合わせることもできます。このテンプレートを変更するには、次のコマンドを使用して電子メール ビューをアプリケーションに公開する必要があります。

```shell
php artisan vendor:publish --tag=laravel-mail
```

<!-- This will generate several files in `resources/views/vendor/mail`. You can modify any of these files as well as the `resources/views/vendor/mail/themes/default.css` file to change the look and appearance of the default email template. -->
これにより、`resources/views/vendor/mail` にいくつかのファイルが生成されます。これらのファイルと `resources/views/vendor/mail/themes/default.css` ファイルを変更して、デフォルトの電子メール テンプレートの外観を変更できます。
