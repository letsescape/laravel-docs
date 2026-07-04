<!-- # Asset Bundling (Vite) -->
# Asset Bundling (Vite)

- [Introduction](#introduction)
- [Installation & Setup](#installation)
  - [Installing Node](#installing-node)
  - [Installing Vite and the Laravel Plugin](#installing-vite-and-laravel-plugin)
  - [Configuring Vite](#configuring-vite)
  - [Loading Your Scripts and Styles](#loading-your-scripts-and-styles)
- [Running Vite](#running-vite)
- [Working With JavaScript](#working-with-scripts)
  - [Aliases](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Svelte](#svelte)
  - [Inertia](#inertia)
  - [URL Processing](#url-processing)
- [Working With Stylesheets](#working-with-stylesheets)
- [Working With Fonts](#working-with-fonts)
  - [Font Providers](#font-providers)
  - [Local Fonts](#local-fonts)
  - [Font Options](#font-options)
- [Working With Blade and Routes](#working-with-blade-and-routes)
  - [Processing Static Assets With Vite](#blade-processing-static-assets)
  - [Refreshing on Save](#blade-refreshing-on-save)
  - [Aliases](#blade-aliases)
- [Asset Prefetching](#asset-prefetching)
- [Custom Base URLs](#custom-base-urls)
- [Environment Variables](#environment-variables)
- [Disabling Vite in Tests](#disabling-vite-in-tests)
- [Server-Side Rendering (SSR)](#ssr)
- [Script and Style Tag Attributes](#script-and-style-attributes)
  - [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)
  - [Subresource Integrity (SRI)](#subresource-integrity-sri)
  - [Arbitrary Attributes](#arbitrary-attributes)
- [Advanced Customization](#advanced-customization)
  - [Dev Server Cross-Origin Resource Sharing (CORS)](#cors)
  - [Correcting Dev Server URLs](#correcting-dev-server-urls)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Vite](https://vitejs.dev) is a modern frontend build tool that provides an extremely fast development environment and bundles your code for production. When building applications with Laravel, you will typically use Vite to bundle your application's CSS and JavaScript files into production-ready assets. -->
[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고, 프로덕션을 위해 코드를 번들링해 주는 최신 frontend 빌드 도구입니다. Laravel로 애플리케이션을 만들 때는 일반적으로 Vite를 사용하여 애플리케이션의 CSS와 JavaScript 파일을 프로덕션에 바로 사용할 수 있는 애셋으로 번들링합니다.

<!-- Laravel integrates seamlessly with Vite by providing an official plugin and Blade directive to load your assets for development and production. -->
Laravel은 공식 플러그인과 Blade 디렉티브를 제공하여 Vite와 매끄럽게 통합되며, 개발 및 프로덕션 환경에서 애셋을 불러올 수 있게 해 줍니다.

<a name="installation"></a>
<!-- ## Installation & Setup -->
## Installation & Setup

> [!NOTE]
> 다음 문서는 Laravel Vite 플러그인을 수동으로 설치하고 설정하는 방법을 설명합니다. 하지만 Laravel의 [starter kits](/docs/13.x/starter-kits)에는 이미 이 스캐폴딩이 모두 포함되어 있으며, Laravel과 Vite를 가장 빠르게 시작하는 방법입니다.

<a name="installing-node"></a>
<!-- ### Installing Node -->
### Installing Node

<!-- You must ensure that Node.js (16+) and NPM are installed before running Vite and the Laravel plugin: -->
Vite와 Laravel 플러그인을 실행하기 전에 Node.js (16+)와 NPM이 설치되어 있는지 확인해야 합니다.

```shell
node -v
npm -v
```

<!-- You can easily install the latest version of Node and NPM using simple graphical installers from [the official Node website](https://nodejs.org/en/download/). Or, if you are using [Laravel Sail](https://laravel.com/docs/13.x/sail), you may invoke Node and NPM through Sail: -->
[the official Node website](https://nodejs.org/en/download/)에서 제공하는 간단한 그래픽 설치 프로그램을 사용하면 최신 버전의 Node와 NPM을 쉽게 설치할 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/13.x/sail)을 사용 중이라면 Sail을 통해 Node와 NPM을 실행할 수 있습니다.

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
<!-- ### Installing Vite and the Laravel Plugin -->
### Installing Vite and the Laravel Plugin

<!-- Within a fresh installation of Laravel, you will find a `package.json` file in the root of your application's directory structure. The default `package.json` file already includes everything you need to get started using Vite and the Laravel plugin. You may install your application's frontend dependencies via NPM: -->
새 Laravel 설치본에서는 애플리케이션 디렉터리 구조의 루트에 `package.json` 파일이 있습니다. 기본 `package.json` 파일에는 Vite와 Laravel 플러그인을 사용하기 위해 필요한 모든 것이 이미 포함되어 있습니다. NPM을 통해 애플리케이션의 frontend 의존성을 설치할 수 있습니다.

```shell
npm install
```

<a name="configuring-vite"></a>
<!-- ### Configuring Vite -->
### Configuring Vite

<!-- Vite is configured via a `vite.config.js` file in the root of your project. You are free to customize this file based on your needs, and you may also install any other plugins your application requires, such as `@vitejs/plugin-react`, `@sveltejs/vite-plugin-svelte` or `@vitejs/plugin-vue`. -->
Vite는 프로젝트 루트의 `vite.config.js` 파일을 통해 설정합니다. 필요에 따라 이 파일을 자유롭게 사용자 정의할 수 있으며, `@vitejs/plugin-react`, `@sveltejs/vite-plugin-svelte`, `@vitejs/plugin-vue`처럼 애플리케이션에 필요한 다른 플러그인도 설치할 수 있습니다.

<!-- The Laravel Vite plugin requires you to specify the entry points for your application. These may be JavaScript or CSS files, and include preprocessed languages such as TypeScript, JSX, TSX, and Sass. -->
Laravel Vite 플러그인은 애플리케이션의 엔트리 포인트를 지정해야 합니다. 엔트리 포인트는 JavaScript 또는 CSS 파일일 수 있으며, TypeScript, JSX, TSX, Sass 같은 전처리 언어도 포함할 수 있습니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css',
            'resources/js/app.js',
        ]),
    ],
});
```

<!-- If you are building an SPA, including applications built using Inertia, Vite works best without CSS entry points: -->
Inertia를 사용해 만든 애플리케이션을 포함하여 SPA를 빌드하는 경우, Vite는 CSS 엔트리 포인트 없이 사용할 때 가장 잘 동작합니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css', // [tl! remove]
            'resources/js/app.js',
        ]),
    ],
});
```

<!-- Instead, you should import your CSS via JavaScript. Typically, this would be done in your application's `resources/js/app.js` file: -->
대신 JavaScript를 통해 CSS를 import해야 합니다. 일반적으로 애플리케이션의 `resources/js/app.js` 파일에서 이 작업을 수행합니다.

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

<!-- The Laravel plugin also supports multiple entry points and advanced configuration options such as [SSR entry points](#ssr). -->
Laravel 플러그인은 여러 엔트리 포인트와 [SSR entry points](#ssr) 같은 고급 설정 옵션도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
<!-- #### Working With a Secure Development Server -->
#### Working With a Secure Development Server

<!-- If your local development web server is serving your application via HTTPS, you may run into issues connecting to the Vite development server. -->
로컬 개발 웹 서버가 HTTPS를 통해 애플리케이션을 제공하는 경우, Vite 개발 서버에 연결할 때 문제가 발생할 수 있습니다.

<!-- If you are using [Laravel Herd](https://herd.laravel.com) and have secured the site or you are using [Laravel Valet](/docs/13.x/valet) and have run the [secure command](/docs/13.x/valet#securing-sites) against your application, the Laravel Vite plugin will automatically detect and use the generated TLS certificate for you. -->
[Laravel Herd](https://herd.laravel.com)를 사용하면서 사이트를 보안 처리했거나, [Laravel Valet](/docs/13.x/valet)을 사용하면서 애플리케이션에 대해 [secure command](/docs/13.x/valet#securing-sites)를 실행했다면, Laravel Vite 플러그인이 생성된 TLS 인증서를 자동으로 감지하여 사용합니다.

<!-- If you secured the site using a host that does not match the application's directory name, you may manually specify the host in your application's `vite.config.js` file: -->
애플리케이션의 디렉터리 이름과 일치하지 않는 host로 사이트를 보안 처리했다면, 애플리케이션의 `vite.config.js` 파일에서 host를 직접 지정할 수 있습니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            detectTls: 'my-app.test', // [tl! add]
        }),
    ],
});
```

<!-- When using another web server, you should generate a trusted certificate and manually configure Vite to use the generated certificates: -->
다른 웹 서버를 사용하는 경우에는 신뢰할 수 있는 인증서를 생성하고, 생성된 인증서를 사용하도록 Vite를 직접 설정해야 합니다.

```js
// ...
import fs from 'fs'; // [tl! add]

const host = 'my-app.test'; // [tl! add]

export default defineConfig({
    // ...
    server: { // [tl! add]
        host, // [tl! add]
        hmr: { host }, // [tl! add]
        https: { // [tl! add]
            key: fs.readFileSync(`/path/to/${host}.key`), // [tl! add]
            cert: fs.readFileSync(`/path/to/${host}.crt`), // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<!-- If you are unable to generate a trusted certificate for your system, you may install and configure the [@vitejs/plugin-basic-ssl plugin](https://github.com/vitejs/vite-plugin-basic-ssl). When using untrusted certificates, you will need to accept the certificate warning for Vite's development server in your browser by following the "Local" link in your console when running the `npm run dev` command. -->
시스템에서 신뢰할 수 있는 인증서를 생성할 수 없다면 [@vitejs/plugin-basic-ssl plugin](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치하고 설정할 수 있습니다. 신뢰할 수 없는 인증서를 사용하는 경우, `npm run dev` 명령어를 실행할 때 콘솔에 표시되는 "Local" 링크를 따라 브라우저에서 Vite 개발 서버의 인증서 경고를 허용해야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
<!-- #### Running the Development Server in Sail on WSL2 -->
#### Running the Development Server in Sail on WSL2

<!-- When running the Vite development server within [Laravel Sail](/docs/13.x/sail) on Windows Subsystem for Linux 2 (WSL2), you should add the following configuration to your `vite.config.js` file to ensure the browser can communicate with the development server: -->
Windows Subsystem for Linux 2 (WSL2)의 [Laravel Sail](/docs/13.x/sail) 안에서 Vite 개발 서버를 실행하는 경우, 브라우저가 개발 서버와 통신할 수 있도록 `vite.config.js` 파일에 다음 설정을 추가해야 합니다.

```js
// ...

export default defineConfig({
    // ...
    server: { // [tl! add:start]
        hmr: {
            host: 'localhost',
        },
    }, // [tl! add:end]
});
```

<!-- If your file changes are not being reflected in the browser while the development server is running, you may also need to configure Vite's [server.watch.usePolling option](https://vitejs.dev/config/server-options.html#server-watch). -->
개발 서버가 실행 중인데도 파일 변경 사항이 브라우저에 반영되지 않는다면, Vite의 [server.watch.usePolling option](https://vitejs.dev/config/server-options.html#server-watch)도 설정해야 할 수 있습니다.

<a name="loading-your-scripts-and-styles"></a>
<!-- ### Loading Your Scripts and Styles -->
### Loading Your Scripts and Styles

<!-- With your Vite entry points configured, you may now reference them in a `@vite()` Blade directive that you add to the `<head>` of your application's root template: -->
Vite 엔트리 포인트를 설정했다면, 이제 애플리케이션의 루트 템플릿 `<head>`에 추가하는 `@vite()` Blade 디렉티브에서 해당 엔트리 포인트를 참조할 수 있습니다.

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

<!-- If you're importing your CSS via JavaScript, you only need to include the JavaScript entry point: -->
JavaScript를 통해 CSS를 import하고 있다면 JavaScript 엔트리 포인트만 포함하면 됩니다.

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

<!-- The `@vite` directive will automatically detect the Vite development server and inject the Vite client to enable Hot Module Replacement. In build mode, the directive will load your compiled and versioned assets, including any imported CSS. -->
`@vite` 디렉티브는 Vite 개발 서버를 자동으로 감지하고, Hot Module Replacement를 활성화하기 위해 Vite 클라이언트를 주입합니다. 빌드 모드에서는 import된 CSS를 포함하여 컴파일되고 버전이 부여된 애셋을 불러옵니다.

<!-- If needed, you may also specify the build path of your compiled assets when invoking the `@vite` directive: -->
필요한 경우 `@vite` 디렉티브를 호출할 때 컴파일된 애셋의 빌드 경로도 지정할 수 있습니다.

```blade
<!doctype html>
<head>
    {{-- Given build path is relative to public path. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
<!-- #### Inline Assets -->
#### Inline Assets

<!-- Sometimes it may be necessary to include the raw content of assets rather than linking to the versioned URL of the asset. For example, you may need to include asset content directly into your page when passing HTML content to a PDF generator. You may output the content of Vite assets using the `content` method provided by the `Vite` facade: -->
때로는 애셋의 버전이 부여된 URL에 링크하는 대신, 애셋의 원본 내용을 직접 포함해야 할 수 있습니다. 예를 들어 PDF 생성기에 HTML 콘텐츠를 전달할 때 애셋 내용을 페이지에 직접 포함해야 할 수 있습니다. `Vite` facade가 제공하는 `content` 메서드를 사용하여 Vite 애셋의 내용을 출력할 수 있습니다.

```blade
@use('Illuminate\Support\Facades\Vite')

<!doctype html>
<head>
    {{-- ... --}}

    <style>
        {!! Vite::content('resources/css/app.css') !!}
    </style>
    <script>
        {!! Vite::content('resources/js/app.js') !!}
    </script>
</head>
```

<a name="running-vite"></a>
<!-- ## Running Vite -->
## Running Vite

<!-- There are two ways you can run Vite. You may run the development server via the `dev` command, which is useful while developing locally. The development server will automatically detect changes to your files and instantly reflect them in any open browser windows. -->
Vite를 실행하는 방법은 두 가지입니다. 로컬에서 개발하는 동안 유용한 `dev` 명령어로 개발 서버를 실행할 수 있습니다. 개발 서버는 파일 변경 사항을 자동으로 감지하고, 열려 있는 브라우저 창에 즉시 반영합니다.

<!-- Or, running the `build` command will version and bundle your application's assets and get them ready for you to deploy to production: -->
또는 `build` 명령어를 실행하면 애플리케이션의 애셋에 버전을 부여하고 번들링하여 프로덕션에 배포할 준비를 합니다.

```shell
# Run the Vite development server...
npm run dev

# Build and version the assets for production...
npm run build
```

<!-- If you are running the development server in [Sail](/docs/13.x/sail) on WSL2, you may need some [additional configuration](#configuring-hmr-in-sail-on-wsl2) options. -->
WSL2의 [Sail](/docs/13.x/sail)에서 개발 서버를 실행 중이라면 몇 가지 [additional configuration](#configuring-hmr-in-sail-on-wsl2) 옵션이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
<!-- ## Working With JavaScript -->
## Working With JavaScript

<a name="aliases"></a>
<!-- ### Aliases -->
### Aliases

<!-- By default, The Laravel plugin provides a common alias to help you hit the ground running and conveniently import your application's assets: -->
기본적으로 Laravel 플러그인은 빠르게 시작하고 애플리케이션의 애셋을 편리하게 import할 수 있도록 일반적인 별칭을 제공합니다.

```js
{
    '@' => '/resources/js'
}
```

<!-- You may overwrite the `'@'` alias by adding your own to the `vite.config.js` configuration file: -->
`vite.config.js` 설정 파일에 직접 별칭을 추가하여 `'@'` 별칭을 덮어쓸 수 있습니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel(['resources/ts/app.tsx']),
    ],
    resolve: {
        alias: {
            '@': '/resources/ts',
        },
    },
});
```

<a name="vue"></a>
<!-- ### Vue -->
### Vue

<!-- If you would like to build your frontend using the [Vue](https://vuejs.org/) framework, then you will also need to install the `@vitejs/plugin-vue` plugin: -->
[Vue](https://vuejs.org/) 프레임워크를 사용하여 frontend를 만들고 싶다면 `@vitejs/plugin-vue` 플러그인도 설치해야 합니다.

```shell
npm install --save-dev @vitejs/plugin-vue
```

<!-- You may then include the plugin in your `vite.config.js` configuration file. There are a few additional options you will need when using the Vue plugin with Laravel: -->
그런 다음 `vite.config.js` 설정 파일에 플러그인을 포함할 수 있습니다. Laravel에서 Vue 플러그인을 사용할 때 필요한 추가 옵션이 몇 가지 있습니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [
        laravel(['resources/js/app.js']),
        vue({
            template: {
                transformAssetUrls: {
                    // The Vue plugin will re-write asset URLs, when referenced
                    // in Single File Components, to point to the Laravel web
                    // server. Setting this to `null` allows the Laravel plugin
                    // to instead re-write asset URLs to point to the Vite
                    // server instead.
                    base: null,

                    // The Vue plugin will parse absolute URLs and treat them
                    // as absolute paths to files on disk. Setting this to
                    // `false` will leave absolute URLs un-touched so they can
                    // reference assets in the public directory as expected.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]
> Laravel의 [starter kits](/docs/13.x/starter-kits)에는 이미 적절한 Laravel, Vue, Vite 설정이 포함되어 있습니다. 이러한 starter kits는 Laravel, Vue, Vite를 가장 빠르게 시작하는 방법을 제공합니다.

<a name="react"></a>
<!-- ### React -->
### React

<!-- If you would like to build your frontend using the [React](https://reactjs.org/) framework, then you will also need to install the `@vitejs/plugin-react` plugin: -->
[React](https://reactjs.org/) 프레임워크를 사용하여 frontend를 만들고 싶다면 `@vitejs/plugin-react` 플러그인도 설치해야 합니다.

```shell
npm install --save-dev @vitejs/plugin-react
```

<!-- You may then include the plugin in your `vite.config.js` configuration file: -->
그런 다음 `vite.config.js` 설정 파일에 플러그인을 포함할 수 있습니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [
        laravel(['resources/js/app.jsx']),
        react(),
    ],
});
```

<!-- You will need to ensure that any files containing JSX have a `.jsx` or `.tsx` extension, remembering to update your entry point, if required, as [shown above](#configuring-vite). -->
JSX를 포함하는 모든 파일의 확장자가 `.jsx` 또는 `.tsx`인지 확인해야 하며, 필요한 경우 [shown above](#configuring-vite) 엔트리 포인트도 업데이트해야 합니다.

<!-- You will also need to include the additional `@viteReactRefresh` Blade directive alongside your existing `@vite` directive. -->
기존 `@vite` 디렉티브와 함께 추가 `@viteReactRefresh` Blade 디렉티브도 포함해야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

<!-- The `@viteReactRefresh` directive must be called before the `@vite` directive. -->
`@viteReactRefresh` 디렉티브는 `@vite` 디렉티브보다 먼저 호출해야 합니다.

> [!NOTE]
> Laravel의 [starter kits](/docs/13.x/starter-kits)에는 이미 적절한 Laravel, React, Vite 설정이 포함되어 있습니다. 이러한 starter kits는 Laravel, React, Vite를 가장 빠르게 시작하는 방법을 제공합니다.

<a name="svelte"></a>
<!-- ### Svelte -->
### Svelte

<!-- If you would like to build your frontend using the [Svelte](https://svelte.dev/) framework, then you will also need to install the `@sveltejs/vite-plugin-svelte` plugin: -->
[Svelte](https://svelte.dev/) 프레임워크를 사용하여 frontend를 만들고 싶다면 `@sveltejs/vite-plugin-svelte` 플러그인도 설치해야 합니다.

```shell
npm install --save-dev @sveltejs/vite-plugin-svelte
```

<!-- You may then include the plugin in your `vite.config.js` configuration file. -->
그런 다음 `vite.config.js` 설정 파일에 플러그인을 포함할 수 있습니다.

```js
import { svelte } from '@sveltejs/vite-plugin-svelte';
import laravel from 'laravel-vite-plugin';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [
    laravel({
      input: ['resources/js/app.ts'],
      ssr: 'resources/js/ssr.ts',
      refresh: true,
    }),
    svelte(),
  ],
});
```
> [!NOTE]
> Laravel의 [starter kits](/docs/13.x/starter-kits)에는 이미 적절한 Laravel, Svelte, Vite 설정이 포함되어 있습니다. 이 스타터 키트는 Laravel, Svelte, Vite를 가장 빠르게 시작할 수 있는 방법을 제공합니다.

<a name="inertia"></a>
<!-- ### Inertia -->
### Inertia

<!-- The Laravel Vite plugin provides a convenient `resolvePageComponent` function to help you resolve your Inertia page components. Below is an example of the helper in use with Vue 3; however, you may also utilize the function in other frameworks such as React or Svelte: -->
Laravel Vite 플러그인은 Inertia 페이지 컴포넌트를 쉽게 확인하고 가져올 수 있도록 편리한 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3에서 이 헬퍼를 사용하는 예시입니다. 하지만 React나 Svelte 같은 다른 프레임워크에서도 이 함수를 사용할 수 있습니다.

```js
import { createApp, h } from 'vue';
import { createInertiaApp } from '@inertiajs/vue3';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';

createInertiaApp({
  resolve: (name) => resolvePageComponent(`./Pages/${name}.vue`, import.meta.glob('./Pages/**/*.vue')),
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el)
  },
});
```

<!-- If you are using Vite's code splitting feature with Inertia, we recommend configuring [asset prefetching](#asset-prefetching). -->
Inertia와 함께 Vite의 코드 분할 기능을 사용한다면 [asset prefetching](#asset-prefetching)을 설정하는 것을 권장합니다.

> [!NOTE]
> Laravel의 [starter kits](/docs/13.x/starter-kits)에는 이미 적절한 Laravel, Inertia, Vite 설정이 포함되어 있습니다. 이 스타터 키트는 Laravel, Inertia, Vite를 가장 빠르게 시작할 수 있는 방법을 제공합니다.

<a name="url-processing"></a>
<!-- ### URL Processing -->
### URL Processing

<!-- When using Vite and referencing assets in your application's HTML, CSS, or JS, there are a couple of caveats to consider. First, if you reference assets with an absolute path, Vite will not include the asset in the build; therefore, you should ensure that the asset is available in your public directory. You should avoid using absolute paths when using a [dedicated CSS entrypoint](#configuring-vite) because, during development, browsers will try to load these paths from the Vite development server, where the CSS is hosted, rather than from your public directory. -->
Vite를 사용하면서 애플리케이션의 HTML, CSS, JS에서 애셋을 참조할 때는 몇 가지 주의할 점이 있습니다. 먼저, 절대 경로로 애셋을 참조하면 Vite는 해당 애셋을 빌드에 포함하지 않습니다. 따라서 해당 애셋이 public 디렉터리에 있어야 합니다. [dedicated CSS entrypoint](#configuring-vite)를 사용할 때는 절대 경로 사용을 피해야 합니다. 개발 중에는 브라우저가 public 디렉터리가 아니라 CSS가 호스팅되는 Vite 개발 서버에서 해당 경로를 불러오려고 하기 때문입니다.

<!-- When referencing relative asset paths, you should remember that the paths are relative to the file where they are referenced. Any assets referenced via a relative path will be re-written, versioned, and bundled by Vite. -->
상대 애셋 경로를 참조할 때는 해당 경로가 참조된 파일을 기준으로 한다는 점을 기억해야 합니다. 상대 경로로 참조된 모든 애셋은 Vite에 의해 다시 작성되고, 버전이 부여되며, 번들에 포함됩니다.

<!-- Consider the following project structure: -->
다음 프로젝트 구조를 살펴보겠습니다.

```text
public/
  taylor.png
resources/
  js/
    Pages/
      Welcome.vue
  images/
    abigail.png
```

<!-- The following example demonstrates how Vite will treat relative and absolute URLs: -->
다음 예시는 Vite가 상대 URL과 절대 URL을 어떻게 처리하는지 보여줍니다.

```html
<!-- This asset is not handled by Vite and will not be included in the build -->
<img src="/taylor.png">

<!-- This asset will be re-written, versioned, and bundled by Vite -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
<!-- ## Working With Stylesheets -->
## Working With Stylesheets

> [!NOTE]
> Laravel의 [starter kits](/docs/13.x/starter-kits)에는 이미 적절한 Tailwind와 Vite 설정이 포함되어 있습니다. 또는 스타터 키트를 사용하지 않고 Tailwind와 Laravel을 함께 사용하고 싶다면 [Tailwind's installation guide for Laravel](https://tailwindcss.com/docs/guides/laravel)를 확인하세요.

<!-- All Laravel applications already include Tailwind and a properly configured `vite.config.js` file. So, you only need to start the Vite development server or run the `dev` Composer command, which will start both the Laravel and Vite development servers: -->
모든 Laravel 애플리케이션에는 이미 Tailwind와 올바르게 설정된 `vite.config.js` 파일이 포함되어 있습니다. 따라서 Vite 개발 서버를 시작하거나 `dev` Composer 명령어를 실행하기만 하면 됩니다. 이 명령어는 Laravel과 Vite 개발 서버를 모두 시작합니다.

```shell
composer run dev
```

<!-- Your application's CSS may be placed within the `resources/css/app.css` file. -->
애플리케이션의 CSS는 `resources/css/app.css` 파일에 배치할 수 있습니다.

<a name="working-with-fonts"></a>
<!-- ## Working With Fonts -->
## Working With Fonts

<!-- The Laravel Vite plugin can serve optimized, self-hosted fonts for your application. When fonts are configured, the plugin resolves the requested font files, emits them as Vite assets, generates font CSS, and writes a font manifest that may be consumed by Blade's [`@fonts` directive](/docs/13.x/blade#fonts). -->
Laravel Vite 플러그인은 애플리케이션을 위해 최적화된 self-hosted 폰트를 제공할 수 있습니다. 폰트가 설정되면 플러그인은 요청된 폰트 파일을 확인하고, 이를 Vite 애셋으로 내보내며, 폰트 CSS를 생성하고, Blade의 [`@fonts` directive](/docs/13.x/blade#fonts)가 사용할 수 있는 폰트 manifest를 기록합니다.

<!-- To configure fonts, import one or more provider helpers from `laravel-vite-plugin/fonts` and add them to the Laravel plugin's `fonts` option: -->
폰트를 설정하려면 `laravel-vite-plugin/fonts`에서 하나 이상의 provider 헬퍼를 가져와 Laravel 플러그인의 `fonts` 옵션에 추가합니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import { google } from 'laravel-vite-plugin/fonts';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            fonts: [
                google('Inter', {
                    alias: 'sans',
                    weights: [400, 500, 600, 700],
                    styles: ['normal', 'italic'],
                    subsets: ['latin'],
                    display: 'swap',
                    preload: [
                        { weight: 400 },
                        { weight: 700 },
                    ],
                    fallbacks: ['system-ui', 'sans-serif'],
                }),
            ],
        }),
    ],
});
```

<!-- In this example, the `Inter` font will be available through the `sans` alias. The plugin will generate a `--font-sans` CSS variable and a `.font-sans` utility class that applies the generated font stack. -->
이 예시에서 `Inter` 폰트는 `sans` alias를 통해 사용할 수 있습니다. 플러그인은 `--font-sans` CSS variable과 생성된 폰트 스택을 적용하는 `.font-sans` utility class를 생성합니다.

<a name="font-providers"></a>
<!-- ### Font Providers -->
### Font Providers

<!-- The Laravel Vite plugin includes provider helpers for Google Fonts, Bunny Fonts, Fontsource, and local fonts: -->
Laravel Vite 플러그인에는 Google Fonts, Bunny Fonts, Fontsource, local fonts를 위한 provider 헬퍼가 포함되어 있습니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import { bunny, fontsource, google, local } from 'laravel-vite-plugin/fonts';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            fonts: [
                google('Inter', { alias: 'sans' }),
                bunny('Figtree', { alias: 'body' }),
                fontsource('JetBrains Mono', { alias: 'mono' }),
                local('Brand Sans', {
                    alias: 'brand',
                    src: 'resources/fonts/brand-sans',
                }),
            ],
        }),
    ],
});
```

<!-- The `fontsource` provider reads fonts from an installed Fontsource package. By default, the package name is derived from the font family, such as `@fontsource/jetbrains-mono`. If your application uses a different package name, you may specify it using the `package` option. -->
`fontsource` provider는 설치된 Fontsource package에서 폰트를 읽습니다. 기본적으로 package 이름은 `@fontsource/jetbrains-mono`처럼 폰트 family에서 파생됩니다. 애플리케이션이 다른 package 이름을 사용한다면 `package` 옵션으로 지정할 수 있습니다.

<a name="local-fonts"></a>
<!-- ### Local Fonts -->
### Local Fonts

<!-- When using local fonts, the `src` option may point to a single font file, a directory, or a glob pattern. The plugin will discover supported font files and infer their weight and style from their filenames: -->
로컬 폰트를 사용할 때 `src` 옵션은 단일 폰트 파일, 디렉터리 또는 glob 패턴을 가리킬 수 있습니다. 플러그인은 지원되는 폰트 파일을 발견하고 파일 이름에서 weight와 style을 추론합니다.

```js
local('Brand Sans', {
    alias: 'brand',
    src: 'resources/fonts/brand-sans/*.woff2',
})
```

<!-- If you need full control over the available variants, you may define them explicitly using the `variants` option: -->
사용 가능한 variants를 완전히 제어해야 한다면 `variants` 옵션을 사용하여 명시적으로 정의할 수 있습니다.

```js
local('Brand Sans', {
    alias: 'brand',
    variants: [
        { src: 'resources/fonts/BrandSans-Regular.woff2', weight: 400 },
        { src: 'resources/fonts/BrandSans-Italic.woff2', weight: 400, style: 'italic' },
        { src: ['resources/fonts/BrandSans-Bold.woff2', 'resources/fonts/BrandSans-Bold.ttf'], weight: 700 },
    ],
})
```

<a name="font-options"></a>
<!-- ### Font Options -->
### Font Options

<!-- Depending on the provider, font definitions may accept several options that allow you to customize the generated font CSS: -->
provider에 따라 폰트 정의는 생성되는 폰트 CSS를 사용자 정의할 수 있는 여러 옵션을 받을 수 있습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `alias` defines the name used by Blade's `@fonts` directive and defaults to a slug of the font family.
- `variable` defines the generated CSS variable and defaults to `--font-{alias}`.
- `weights` defines the remote or Fontsource font weights that should be resolved and defaults to `[400]`.
- `styles` defines the remote or Fontsource font styles that should be resolved and defaults to `['normal']`.
- `subsets` defines the remote or Fontsource font subsets that should be resolved and defaults to `['latin']`.
- `display` defines the `font-display` value and defaults to `swap`.
- `preload` controls which WOFF2 font variants should be preloaded. This option may be `true`, `false`, or an array of `{ weight, style }` selectors.
- `fallbacks` defines additional fallback fonts that should be appended to the generated font stack.
- `optimizedFallbacks` attempts to generate metric-adjusted fallback font faces using the optional `fontaine` package and defaults to `true`.
-->
- `alias`는 Blade의 `@fonts` directive가 사용하는 이름을 정의하며, 기본값은 폰트 family의 slug입니다.
- `variable`은 생성되는 CSS variable을 정의하며, 기본값은 `--font-{alias}`입니다.
- `weights`는 확인해야 하는 remote 또는 Fontsource 폰트 weights를 정의하며, 기본값은 `[400]`입니다.
- `styles`는 확인해야 하는 remote 또는 Fontsource 폰트 styles를 정의하며, 기본값은 `['normal']`입니다.
- `subsets`는 확인해야 하는 remote 또는 Fontsource 폰트 subsets를 정의하며, 기본값은 `['latin']`입니다.
- `display`는 `font-display` 값을 정의하며, 기본값은 `swap`입니다.
- `preload`는 preload해야 하는 WOFF2 폰트 variants를 제어합니다. 이 옵션은 `true`, `false` 또는 `{ weight, style }` selector 배열일 수 있습니다.
- `fallbacks`는 생성된 폰트 스택에 추가할 fallback 폰트를 정의합니다.
- `optimizedFallbacks`는 선택 사항인 `fontaine` package를 사용해 metric-adjusted fallback font face 생성을 시도하며, 기본값은 `true`입니다.

<!-- </div> -->
</div>

<!-- Optimized fallbacks require the `fontaine` package, which is not installed by default. If you want Laravel to generate metric-adjusted fallback font faces, you should install `fontaine` as a development dependency: -->
최적화된 fallback에는 기본적으로 설치되지 않는 `fontaine` package가 필요합니다. Laravel이 metric-adjusted fallback font face를 생성하도록 하려면 `fontaine`을 development dependency로 설치해야 합니다.

```shell
npm install --save-dev fontaine
```

<!-- If `fontaine` is not installed or cannot read a font file, Laravel will skip the optimized fallback for that font and continue using any fonts configured via the `fallbacks` option. -->
`fontaine`이 설치되어 있지 않거나 폰트 파일을 읽을 수 없다면, Laravel은 해당 폰트에 대한 최적화된 fallback을 건너뛰고 `fallbacks` 옵션으로 설정된 폰트를 계속 사용합니다.

<!-- Local fonts are resolved from the `src` or `variants` options described above instead of using `weights`, `styles`, and `subsets`. -->
로컬 폰트는 `weights`, `styles`, `subsets` 대신 위에서 설명한 `src` 또는 `variants` 옵션에서 확인됩니다.

<a name="working-with-blade-and-routes"></a>
<!-- ## Working With Blade and Routes -->
## Working With Blade and Routes

<a name="blade-processing-static-assets"></a>
<!-- ### Processing Static Assets With Vite -->
### Processing Static Assets With Vite

<!-- When referencing assets in your JavaScript or CSS, Vite automatically processes and versions them. In addition, when building Blade-based applications, Vite can also process and version static assets that you reference solely in Blade templates. -->
JavaScript나 CSS에서 애셋을 참조하면 Vite는 이를 자동으로 처리하고 버전을 부여합니다. 또한 Blade 기반 애플리케이션을 빌드할 때, Vite는 Blade 템플릿에서만 참조하는 정적 애셋도 처리하고 버전을 부여할 수 있습니다.

<!-- However, to accomplish this, you need to make Vite aware of your assets by specifying them in the plugin's `assets` option. This option is intended for static files that you want to reference directly with `Vite::asset`. If you want Laravel to generate font CSS and preload links, use the [`fonts` option](#working-with-fonts) instead. -->
하지만 이를 수행하려면 플러그인의 `assets` 옵션에 애셋을 지정하여 Vite가 해당 애셋을 알 수 있도록 해야 합니다. 이 옵션은 `Vite::asset`으로 직접 참조하려는 정적 파일을 위한 것입니다. Laravel이 폰트 CSS와 preload 링크를 생성하게 하려면 대신 [`fonts` option](#working-with-fonts)을 사용하십시오.

<!-- For example, if you want to process and version all images stored in `resources/images` and all fonts stored in `resources/fonts`, you should add the following to your Vite configuration: -->
예를 들어 `resources/images`에 저장된 모든 이미지와 `resources/fonts`에 저장된 모든 폰트를 처리하고 버전을 부여하려면 Vite 설정에 다음을 추가해야 합니다.

```js
laravel({
    input: 'resources/js/app.js',
    assets: ['resources/images/**', 'resources/fonts/**'],
})
```

<!-- These assets will now be processed by Vite when running `npm run build`. You can then reference these assets in Blade templates using the `Vite::asset` method, which will return the versioned URL for a given asset: -->
이제 `npm run build`를 실행하면 해당 애셋들이 Vite에 의해 처리됩니다. 그런 다음 Blade 템플릿에서 `Vite::asset` 메서드를 사용해 이 애셋들을 참조할 수 있으며, 이 메서드는 지정한 애셋의 버전이 적용된 URL을 반환합니다.

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

> [!NOTE]
> Laravel Vite 플러그인 3버전 이전에는 정적 애셋을 `import.meta.glob`을 사용해 애플리케이션의 엔트리포인트에서 가져와야 했습니다. `assets` 옵션은 Vite 8의 변경 사항 때문에 도입되었습니다.

<a name="blade-refreshing-on-save"></a>
<!-- ### Refreshing on Save -->
### Refreshing on Save

<!-- When your application is built using traditional server-side rendering with Blade, Vite can improve your development workflow by automatically refreshing the browser when you make changes to view files in your application. To get started, you can simply specify the `refresh` option as `true`. -->
애플리케이션이 Blade를 사용한 전통적인 서버 사이드 렌더링 방식으로 만들어졌다면, Vite는 애플리케이션의 뷰 파일을 변경할 때 브라우저를 자동으로 새로고침하여 개발 워크플로를 개선할 수 있습니다. 시작하려면 `refresh` 옵션을 `true`로 지정하면 됩니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: true,
        }),
    ],
});
```

<!-- When the `refresh` option is `true`, saving files in the following directories will trigger the browser to perform a full page refresh while you are running `npm run dev`: -->
`refresh` 옵션이 `true`이면 `npm run dev`를 실행하는 동안 다음 디렉터리의 파일을 저장할 때 브라우저가 전체 페이지 새로고침을 수행합니다.

<!--
- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`
-->
- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

<!-- Watching the `routes/**` directory is useful if you are utilizing [Ziggy](https://github.com/tighten/ziggy) to generate route links within your application's frontend. -->
애플리케이션 프런트엔드에서 라우트 링크를 생성하기 위해 [Ziggy](https://github.com/tighten/ziggy)를 사용한다면 `routes/**` 디렉터리를 감시하는 것이 유용합니다.

<!-- If these default paths do not suit your needs, you can specify your own list of paths to watch: -->
이 기본 경로들이 필요에 맞지 않는다면 감시할 경로 목록을 직접 지정할 수 있습니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: ['resources/views/**'],
        }),
    ],
});
```

<!-- Under the hood, the Laravel Vite plugin uses the [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload) package, which offers some advanced configuration options to fine-tune this feature's behavior. If you need this level of customization, you may provide a `config` definition: -->
내부적으로 Laravel Vite 플러그인은 [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload) 패키지를 사용합니다. 이 패키지는 이 기능의 동작을 세밀하게 조정할 수 있는 몇 가지 고급 설정 옵션을 제공합니다. 이런 수준의 사용자 정의가 필요하다면 `config` 정의를 제공할 수 있습니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: [{
                paths: ['path/to/watch/**'],
                config: { delay: 300 }
            }],
        }),
    ],
});
```

<a name="blade-aliases"></a>
<!-- ### Aliases -->
### Aliases

<!-- It is common in JavaScript applications to [create aliases](#aliases) to regularly referenced directories. But, you may also create aliases to use in Blade by using the `macro` method on the `Illuminate\Support\Facades\Vite` class. Typically, "macros" should be defined within the `boot` method of a [service provider](/docs/13.x/providers): -->
JavaScript 애플리케이션에서는 자주 참조하는 디렉터리에 [create aliases](#aliases)하는 것이 일반적입니다. 하지만 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 사용하여 Blade에서 사용할 별칭도 만들 수 있습니다. 일반적으로 “macro”는 [service provider](/docs/13.x/providers)의 `boot` 메서드 안에서 정의해야 합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

<!-- Once a macro has been defined, it can be invoked within your templates. For example, we can use the `image` macro defined above to reference an asset located at `resources/images/logo.png`: -->
macro가 정의되면 템플릿 안에서 호출할 수 있습니다. 예를 들어 위에서 정의한 `image` macro를 사용해 `resources/images/logo.png`에 있는 애셋을 참조할 수 있습니다.

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="asset-prefetching"></a>
<!-- ## Asset Prefetching -->
## Asset Prefetching

<!-- When building an SPA using Vite's code splitting feature, required assets are fetched on each page navigation. This behavior can lead to delayed UI rendering. If this is a problem for your frontend framework of choice, Laravel offers the ability to eagerly prefetch your application's JavaScript and CSS assets on initial page load. -->
Vite의 코드 분할 기능을 사용해 SPA를 빌드하면, 각 페이지 이동 시 필요한 애셋을 가져옵니다. 이 동작은 UI 렌더링 지연으로 이어질 수 있습니다. 사용 중인 프런트엔드 프레임워크에서 이것이 문제가 된다면, Laravel은 초기 페이지 로드 시 애플리케이션의 JavaScript와 CSS 애셋을 미리 적극적으로 가져올 수 있는 기능을 제공합니다.

<!-- You can instruct Laravel to eagerly prefetch your assets by invoking the `Vite::prefetch` method in the `boot` method of a [service provider](/docs/13.x/providers): -->
[service provider](/docs/13.x/providers)의 `boot` 메서드에서 `Vite::prefetch` 메서드를 호출하여 Laravel이 애셋을 미리 가져오도록 지시할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Vite;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Vite::prefetch(concurrency: 3);
    }
}
```

<!-- In the example above, assets will be prefetched with a maximum of `3` concurrent downloads on each page load. You can modify the concurrency to suit your application's needs or specify no concurrency limit if the application should download all assets at once: -->
위 예시에서는 각 페이지 로드 시 최대 `3`개의 동시 다운로드로 애셋을 미리 가져옵니다. 애플리케이션의 필요에 맞게 동시성을 수정하거나, 애플리케이션이 모든 애셋을 한 번에 다운로드해야 한다면 동시성 제한을 지정하지 않을 수 있습니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch();
}
```

<!-- By default, prefetching will begin when the [page _load_ event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event) fires. If you would like to customize when prefetching begins, you may specify an event that Vite will listen for: -->
기본적으로 프리페칭은 [page _load_ event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event)가 발생할 때 시작됩니다. 프리페칭이 시작되는 시점을 사용자 정의하고 싶다면 Vite가 수신할 이벤트를 지정할 수 있습니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

<!-- Given the code above, prefetching will now begin when you manually dispatch the `vite:prefetch` event on the `window` object. For example, you could have prefetching begin three seconds after the page loads: -->
위 코드에 따르면 이제 `window` 객체에서 `vite:prefetch` 이벤트를 직접 발생시킬 때 프리페칭이 시작됩니다. 예를 들어 페이지가 로드된 후 3초 뒤에 프리페칭을 시작하도록 할 수 있습니다.

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
<!-- ## Custom Base URLs -->
## Custom Base URLs

<!-- If your Vite compiled assets are deployed to a domain separate from your application, such as via a CDN, you must specify the `ASSET_URL` environment variable within your application's `.env` file: -->
Vite로 컴파일된 애셋을 CDN처럼 애플리케이션과 다른 도메인에 배포하는 경우, 애플리케이션의 `.env` 파일에 `ASSET_URL` 환경 변수를 지정해야 합니다.

```env
ASSET_URL=https://cdn.example.com
```

<!-- After configuring the asset URL, all re-written URLs to your assets will be prefixed with the configured value: -->
애셋 URL을 설정한 후에는 다시 작성된 모든 애셋 URL 앞에 설정한 값이 붙습니다.

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

<!-- Remember that [absolute URLs are not re-written by Vite](#url-processing), so they will not be prefixed. -->
[absolute URLs are not re-written by Vite](#url-processing)는 점을 기억하세요. 따라서 절대 URL에는 이 값이 접두사로 붙지 않습니다.

<a name="environment-variables"></a>
<!-- ## Environment Variables -->
## Environment Variables

<!-- You may inject environment variables into your JavaScript by prefixing them with `VITE_` in your application's `.env` file: -->
애플리케이션의 `.env` 파일에서 환경 변수 이름 앞에 `VITE_`를 붙이면 해당 환경 변수를 JavaScript에 주입할 수 있습니다.

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

<!-- You may access injected environment variables via the `import.meta.env` object: -->
주입된 환경 변수는 `import.meta.env` 객체를 통해 접근할 수 있습니다.

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
<!-- ## Disabling Vite in Tests -->
## Disabling Vite in Tests

<!-- Laravel's Vite integration will attempt to resolve your assets while running your tests, which requires you to either run the Vite development server or build your assets. -->
Laravel의 Vite 통합은 테스트를 실행하는 동안 애셋을 확인하려고 시도합니다. 따라서 Vite 개발 서버를 실행하거나 애셋을 빌드해야 합니다.

<!-- If you would prefer to mock Vite during testing, you may call the `withoutVite` method, which is available for any tests that extend Laravel's `TestCase` class: -->
테스트 중에 Vite를 mock 처리하고 싶다면 Laravel의 `TestCase` 클래스를 확장하는 모든 테스트에서 사용할 수 있는 `withoutVite` 메서드를 호출할 수 있습니다.

```php tab=Pest
test('without vite example', function () {
    $this->withoutVite();

    // ...
});
```

```php tab=PHPUnit
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_without_vite_example(): void
    {
        $this->withoutVite();

        // ...
    }
}
```

<!-- If you would like to disable Vite for all tests, you may call the `withoutVite` method from the `setUp` method on your base `TestCase` class: -->
모든 테스트에서 Vite를 비활성화하고 싶다면 기본 `TestCase` 클래스의 `setUp` 메서드에서 `withoutVite` 메서드를 호출할 수 있습니다.

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void// [tl! add:start]
    {
        parent::setUp();

        $this->withoutVite();
    }// [tl! add:end]
}
```

<a name="ssr"></a>
<!-- ## Server-Side Rendering (SSR) -->
## Server-Side Rendering (SSR)

<!-- The Laravel Vite plugin makes it painless to set up server-side rendering with Vite. To get started, create an SSR entry point at `resources/js/ssr.js` and specify the entry point by passing a configuration option to the Laravel plugin: -->
Laravel Vite 플러그인은 Vite로 서버 사이드 렌더링을 쉽게 설정할 수 있게 해줍니다. 시작하려면 `resources/js/ssr.js`에 SSR 엔트리포인트를 만들고, Laravel 플러그인에 설정 옵션을 전달하여 해당 엔트리포인트를 지정합니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            ssr: 'resources/js/ssr.js',
        }),
    ],
});
```

<!-- To ensure you don't forget to rebuild the SSR entry point, we recommend augmenting the "build" script in your application's `package.json` to create your SSR build: -->
SSR 엔트리포인트를 다시 빌드하는 것을 잊지 않도록, 애플리케이션의 `package.json`에 있는 "build" 스크립트를 확장하여 SSR 빌드를 생성하는 것을 권장합니다.

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

<!-- Then, to build and start the SSR server, you may run the following commands: -->
그런 다음 SSR 서버를 빌드하고 시작하려면 다음 명령어를 실행하면 됩니다.

```shell
npm run build
node bootstrap/ssr/ssr.js
```

<!-- If you are using [SSR with Inertia](https://inertiajs.com/server-side-rendering), you may instead use the `inertia:start-ssr` Artisan command to start the SSR server: -->
[SSR with Inertia](https://inertiajs.com/server-side-rendering)을 사용하는 경우, 대신 `inertia:start-ssr` Artisan 명령어를 사용하여 SSR 서버를 시작할 수 있습니다.

```shell
php artisan inertia:start-ssr
```

> [!NOTE]
> Laravel의 [starter kits](/docs/13.x/starter-kits)에는 이미 적절한 Laravel, Inertia SSR, Vite 설정이 포함되어 있습니다. 이 스타터 키트는 Laravel, Inertia SSR, Vite를 가장 빠르게 시작할 수 있는 방법을 제공합니다.

<a name="script-and-style-attributes"></a>
<!-- ## Script and Style Tag Attributes -->
## Script and Style Tag Attributes

<a name="content-security-policy-csp-nonce"></a>
<!-- ### Content Security Policy (CSP) Nonce -->
### Content Security Policy (CSP) Nonce

<!-- If you wish to include a [nonce attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) on your script and style tags as part of your [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP), you may generate or specify a nonce using the `useCspNonce` method within a custom [middleware](/docs/13.x/middleware): -->
스크립트 및 스타일 태그에 [nonce attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일부로 포함하고 싶다면, 사용자 정의 [middleware](/docs/13.x/middleware) 안에서 `useCspNonce` 메서드를 사용하여 nonce를 생성하거나 지정할 수 있습니다.

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Vite;
use Symfony\Component\HttpFoundation\Response;

class AddContentSecurityPolicyHeaders
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        Vite::useCspNonce();

        return $next($request)->withHeaders([
            'Content-Security-Policy' => "script-src 'nonce-".Vite::cspNonce()."'",
        ]);
    }
}
```
<!-- After invoking the `useCspNonce` method, Laravel will automatically include the `nonce` attributes on all generated script and style tags. -->
`useCspNonce` 메서드를 호출하면 Laravel은 생성하는 모든 script 및 style 태그에 `nonce` 속성을 자동으로 포함합니다.

<!-- If you need to specify the nonce elsewhere, including the [Ziggy `@route` directive](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) included with Laravel's [starter kits](/docs/13.x/starter-kits), you may retrieve it using the `cspNonce` method: -->
다른 위치에서 nonce를 지정해야 하는 경우, 예를 들어 Laravel의 [Ziggy `@route` directive](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy)에 포함된 [starter kits](/docs/13.x/starter-kits)에서 사용해야 한다면, `cspNonce` 메서드로 값을 가져올 수 있습니다.

```blade
@routes(nonce: Vite::cspNonce())
```

<!-- If you already have a nonce that you would like to instruct Laravel to use, you may pass the nonce to the `useCspNonce` method: -->
이미 사용하려는 nonce가 있고 Laravel이 해당 값을 사용하도록 지정하려면, `useCspNonce` 메서드에 nonce를 전달하면 됩니다.

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
<!-- ### Subresource Integrity (SRI) -->
### Subresource Integrity (SRI)

<!-- If your Vite manifest includes `integrity` hashes for your assets, Laravel will automatically add the `integrity` attribute on any script and style tags it generates in order to enforce [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity). By default, Vite does not include the `integrity` hash in its manifest, but you may enable it by installing the [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM plugin: -->
Vite 매니페스트에 에셋의 `integrity` 해시가 포함되어 있으면, Laravel은 [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)를 적용하기 위해 생성하는 모든 script 및 style 태그에 `integrity` 속성을 자동으로 추가합니다. 기본적으로 Vite는 매니페스트에 `integrity` 해시를 포함하지 않지만, [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인을 설치하여 활성화할 수 있습니다.

```shell
npm install --save-dev vite-plugin-manifest-sri
```

<!-- You may then enable this plugin in your `vite.config.js` file: -->
그런 다음 `vite.config.js` 파일에서 이 플러그인을 활성화할 수 있습니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import manifestSRI from 'vite-plugin-manifest-sri';// [tl! add]

export default defineConfig({
    plugins: [
        laravel({
            // ...
        }),
        manifestSRI(),// [tl! add]
    ],
});
```

<!-- If required, you may also customize the manifest key where the integrity hash can be found: -->
필요하다면 무결성 해시를 찾을 매니페스트 키도 직접 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

<!-- If you would like to disable this auto-detection completely, you may pass `false` to the `useIntegrityKey` method: -->
이 자동 감지를 완전히 비활성화하려면 `useIntegrityKey` 메서드에 `false`를 전달하면 됩니다.

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
<!-- ### Arbitrary Attributes -->
### Arbitrary Attributes

<!-- If you need to include additional attributes on your script and style tags, such as the [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) attribute, you may specify them via the `useScriptTagAttributes` and `useStyleTagAttributes` methods. Typically, this methods should be invoked from a [service provider](/docs/13.x/providers): -->
script 및 style 태그에 [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 속성과 같은 추가 속성을 포함해야 한다면, `useScriptTagAttributes` 및 `useStyleTagAttributes` 메서드를 통해 지정할 수 있습니다. 일반적으로 이 메서드들은 [service provider](/docs/13.x/providers)에서 호출해야 합니다.

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // Specify a value for the attribute...
    'async' => true, // Specify an attribute without a value...
    'integrity' => false, // Exclude an attribute that would otherwise be included...
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

<!-- If you need to conditionally add attributes, you may pass a callback that will receive the asset source path, its URL, its manifest chunk, and the entire manifest: -->
조건부로 속성을 추가해야 한다면, 에셋 소스 경로, URL, 매니페스트 청크, 전체 매니페스트를 전달받는 콜백을 넘길 수 있습니다.

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $src === 'resources/js/app.js' ? 'reload' : false,
]);

Vite::useStyleTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $chunk && $chunk['isEntry'] ? 'reload' : false,
]);
```

> [!WARNING]
> Vite 개발 서버가 실행 중일 때는 `$chunk` 및 `$manifest` 인수가 `null`입니다.

<a name="advanced-customization"></a>
<!-- ## Advanced Customization -->
## Advanced Customization

<!-- Out of the box, Laravel's Vite plugin uses sensible conventions that should work for the majority of applications; however, sometimes you may need to customize Vite's behavior. To enable additional customization options, we offer the following methods and options which can be used in place of the `@vite` Blade directive: -->
Laravel의 Vite 플러그인은 기본적으로 대부분의 애플리케이션에서 잘 동작하는 합리적인 관례를 사용합니다. 하지만 때로는 Vite의 동작을 커스터마이징해야 할 수 있습니다. 추가 커스터마이징 옵션을 사용하려면, `@vite` Blade 디렉티브 대신 다음 메서드와 옵션을 사용할 수 있습니다.

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // Customize the "hot" file...
            ->useBuildDirectory('bundle') // Customize the build directory...
            ->useManifestFilename('assets.json') // Customize the manifest filename...
            ->withEntryPoints(['resources/js/app.js']) // Specify the entry points...
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // Customize the backend path generation for built assets...
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

<!-- Within the `vite.config.js` file, you should then specify the same configuration: -->
그런 다음 `vite.config.js` 파일에서도 동일한 설정을 지정해야 합니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // Customize the "hot" file...
            buildDirectory: 'bundle', // Customize the build directory...
            input: ['resources/js/app.js'], // Specify the entry points...
        }),
    ],
    build: {
      manifest: 'assets.json', // Customize the manifest filename...
    },
});
```

<a name="cors"></a>
<!-- ### Dev Server Cross-Origin Resource Sharing (CORS) -->
### Dev Server Cross-Origin Resource Sharing (CORS)

<!-- If you are experiencing Cross-Origin Resource Sharing (CORS) issues in the browser while fetching assets from the Vite dev server, you may need to grant your custom origin access to the dev server. Vite combined with the Laravel plugin allows the following origins without any additional configuration: -->
Vite 개발 서버에서 에셋을 가져오는 동안 브라우저에서 Cross-Origin Resource Sharing(CORS) 문제가 발생한다면, 사용자 지정 origin이 개발 서버에 접근할 수 있도록 허용해야 할 수 있습니다. Vite와 Laravel 플러그인을 함께 사용하면 추가 설정 없이 다음 origin이 허용됩니다.

<!--
- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- `APP_URL` in the project's `.env`
-->
- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- 프로젝트의 `.env`에 있는 `APP_URL`

<!-- The easiest way to allow a custom origin for your project is to ensure that your application's `APP_URL` environment variable matches the origin you are visiting in your browser. For example, if you visiting `https://my-app.laravel`, you should update your `.env` to match: -->
프로젝트에서 사용자 지정 origin을 허용하는 가장 쉬운 방법은 애플리케이션의 `APP_URL` 환경 변수가 브라우저에서 방문 중인 origin과 일치하도록 하는 것입니다. 예를 들어 `https://my-app.laravel`에 방문 중이라면, `.env`를 다음과 같이 맞춰 업데이트해야 합니다.

```env
APP_URL=https://my-app.laravel
```

<!-- If you need more fine-grained control over the origins, such as supporting multiple origins, you should utilize [Vite's comprehensive and flexible built-in CORS server configuration](https://vite.dev/config/server-options.html#server-cors). For example, you may specify multiple origins in the `server.cors.origin` configuration option in the project's `vite.config.js` file: -->
여러 origin을 지원하는 등 origin을 더 세밀하게 제어해야 한다면, [Vite's comprehensive and flexible built-in CORS server configuration](https://vite.dev/config/server-options.html#server-cors)을 사용해야 합니다. 예를 들어 프로젝트의 `vite.config.js` 파일에서 `server.cors.origin` 설정 옵션에 여러 origin을 지정할 수 있습니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            refresh: true,
        }),
    ],
    server: {  // [tl! add]
        cors: {  // [tl! add]
            origin: [  // [tl! add]
                'https://backend.laravel',  // [tl! add]
                'http://admin.laravel:8566',  // [tl! add]
            ],  // [tl! add]
        },  // [tl! add]
    },  // [tl! add]
});
```

<!-- You may also include regex patterns, which can be helpful if you would like to allow all origins for a given top-level domain, such as `*.laravel`: -->
정규 표현식 패턴도 포함할 수 있습니다. 예를 들어 `*.laravel`처럼 특정 최상위 도메인의 모든 origin을 허용하려는 경우에 유용합니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            refresh: true,
        }),
    ],
    server: {  // [tl! add]
        cors: {  // [tl! add]
            origin: [ // [tl! add]
                // Supports: SCHEME://DOMAIN.laravel[:PORT] [tl! add]
                /^https?:\/\/.*\.laravel(:\d+)?$/, //[tl! add]
            ], // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<a name="correcting-dev-server-urls"></a>
<!-- ### Correcting Dev Server URLs -->
### Correcting Dev Server URLs

<!-- Some plugins within the Vite ecosystem assume that URLs which begin with a forward-slash will always point to the Vite dev server. However, due to the nature of the Laravel integration, this is not the case. -->
Vite 생태계의 일부 플러그인은 슬래시로 시작하는 URL이 항상 Vite 개발 서버를 가리킨다고 가정합니다. 그러나 Laravel 통합 방식의 특성상 실제로는 그렇지 않습니다.

<!-- For example, the `vite-imagetools` plugin outputs URLs like the following while Vite is serving your assets: -->
예를 들어 Vite가 에셋을 제공하는 동안 `vite-imagetools` 플러그인은 다음과 같은 URL을 출력합니다.

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

<!-- The `vite-imagetools` plugin is expecting that the output URL will be intercepted by Vite and the plugin may then handle all URLs that start with `/@imagetools`. If you are using plugins that are expecting this behavior, you will need to manually correct the URLs. You can do this in your `vite.config.js` file by using the `transformOnServe` option. -->
`vite-imagetools` 플러그인은 출력된 URL이 Vite에 의해 가로채지고, 그다음 플러그인이 `/@imagetools`로 시작하는 모든 URL을 처리할 수 있을 것이라고 기대합니다. 이러한 동작을 기대하는 플러그인을 사용한다면 URL을 수동으로 보정해야 합니다. `vite.config.js` 파일에서 `transformOnServe` 옵션을 사용하면 됩니다.

<!-- In this particular example, we will prepend the dev server URL to all occurrences of `/@imagetools` within the generated code: -->
이 특정 예시에서는 생성된 코드 안의 `/@imagetools`가 나타나는 모든 위치 앞에 개발 서버 URL을 붙입니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import { imagetools } from 'vite-imagetools';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            transformOnServe: (code, devServerUrl) => code.replaceAll('/@imagetools', devServerUrl+'/@imagetools'),
        }),
        imagetools(),
    ],
});
```

<!-- Now, while Vite is serving Assets, it will output URLs that point to the Vite dev server: -->
이제 Vite가 Assets를 제공하는 동안 Vite 개발 서버를 가리키는 URL을 출력합니다.

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```
