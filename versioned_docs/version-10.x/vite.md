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
  - [Inertia](#inertia)
  - [URL Processing](#url-processing)
- [Working With Stylesheets](#working-with-stylesheets)
- [Working With Blade and Routes](#working-with-blade-and-routes)
  - [Processing Static Assets With Vite](#blade-processing-static-assets)
  - [Refreshing on Save](#blade-refreshing-on-save)
  - [Aliases](#blade-aliases)
- [Custom Base URLs](#custom-base-urls)
- [Environment Variables](#environment-variables)
- [Disabling Vite in Tests](#disabling-vite-in-tests)
- [Server-Side Rendering (SSR)](#ssr)
- [Script and Style Tag Attributes](#script-and-style-attributes)
  - [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)
  - [Subresource Integrity (SRI)](#subresource-integrity-sri)
  - [Arbitrary Attributes](#arbitrary-attributes)
- [Advanced Customization](#advanced-customization)
  - [Correcting Dev Server URLs](#correcting-dev-server-urls)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Vite](https://vitejs.dev) is a modern frontend build tool that provides an extremely fast development environment and bundles your code for production. When building applications with Laravel, you will typically use Vite to bundle your application's CSS and JavaScript files into production ready assets. -->
[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고 프로덕션용 코드 번들링을 지원하는 최신 프론트엔드 빌드 도구입니다. Laravel로 애플리케이션을 개발할 때, 일반적으로 Vite를 사용해 앱의 CSS 및 JavaScript 파일을 프로덕션에 배포 가능한 자산(asset)으로 번들링하게 됩니다.

<!-- Laravel integrates seamlessly with Vite by providing an official plugin and Blade directive to load your assets for development and production. -->
Laravel은 공식 Vite 플러그인과 Blade 디렉티브를 제공하여, 개발 및 프로덕션 모두에서 에셋을 불러오는 과정을 자연스럽게 통합합니다.

> [!NOTE]
> 이전에 Laravel Mix를 사용하고 계시나요? 이제 새로운 Laravel 프로젝트에서는 Vite가 기본이며, Mix는 더 이상 사용되지 않습니다. Mix 문서는 [Laravel Mix](https://laravel-mix.com/) 공식 사이트에서 확인할 수 있습니다. Vite로 전환하려면 [migration guide](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하세요.

<a name="vite-or-mix"></a>
<!-- #### Choosing Between Vite and Laravel Mix -->
#### Choosing Between Vite and Laravel Mix

<!-- Before transitioning to Vite, new Laravel applications utilized [Mix](https://laravel-mix.com/), which is powered by [webpack](https://webpack.js.org/), when bundling assets. Vite focuses on providing a faster and more productive experience when building rich JavaScript applications. If you are developing a Single Page Application (SPA), including those developed with tools like [Inertia](https://inertiajs.com), Vite will be the perfect fit. -->
Vite로 전환되기 전까지, Laravel의 신규 애플리케이션은 에셋 번들링 시 [Mix](https://laravel-mix.com/)를 기본으로 사용했으며, Mix는 [webpack](https://webpack.js.org/)을 기반으로 동작합니다. Vite는 더욱 빠르고 생산적인 JavaScript 애플리케이션 개발 환경을 추구합니다. [Inertia](https://inertiajs.com) 같은 도구로 SPA(Single Page Application)를 개발할 때, Vite는 특히 잘 어울립니다.

<!-- Vite also works well with traditional server-side rendered applications with JavaScript "sprinkles", including those using [Livewire](https://livewire.laravel.com). However, it lacks some features that Laravel Mix supports, such as the ability to copy arbitrary assets into the build that are not referenced directly in your JavaScript application. -->
Vite는 [Livewire](https://livewire.laravel.com)처럼 JavaScript가 "스프링클(점진적 적용)"된 기존 서버 사이드 렌더링 환경과도 잘 호환됩니다. 다만, JavaScript 애플리케이션에서 직접 참조하지 않는 임의의 에셋을 빌드에 복사하는 등, 일부 Mix에서 제공하던 기능은 지원하지 않습니다.

<a name="migrating-back-to-mix"></a>
<!-- #### Migrating Back to Mix -->
#### Migrating Back to Mix

<!-- Have you started a new Laravel application using our Vite scaffolding but need to move back to Laravel Mix and webpack? No problem. Please consult our [official guide on migrating from Vite to Mix](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix). -->
Vite 스캐폴딩을 사용해 새 Laravel 애플리케이션을 시작했지만, Mix(webpack)로 다시 이동해야 하는 경우도 있을 수 있습니다. 문제 없습니다. [official guide on migrating from Vite to Mix](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix)를 참고하세요.

<a name="installation"></a>
<!-- ## Installation & Setup -->
## Installation & Setup

> [!NOTE]
> 이 문서에서는 Laravel Vite 플러그인을 수동으로 설치하고 설정하는 방법을 다룹니다. 하지만 Laravel의 [starter kits](/docs/10.x/starter-kits)는 이미 필요한 구성이 포함되어 있어, Laravel과 Vite를 가장 빠르게 시작할 수 있는 방법입니다.

<a name="installing-node"></a>
<!-- ### Installing Node -->
### Installing Node

<!-- You must ensure that Node.js (16+) and NPM are installed before running Vite and the Laravel plugin: -->
Vite와 Laravel 플러그인을 실행하려면 Node.js(16버전 이상)와 NPM이 반드시 설치되어 있어야 합니다:

```sh
node -v
npm -v
```

<!-- You can easily install the latest version of Node and NPM using simple graphical installers from [the official Node website](https://nodejs.org/en/download/). Or, if you are using [Laravel Sail](https://laravel.com/docs/10.x/sail), you may invoke Node and NPM through Sail: -->
Node 및 NPM은 [the official Node website](https://nodejs.org/en/download/)에서 제공되는 간편한 설치 프로그램을 통해 쉽게 설치할 수 있습니다. [Laravel Sail](https://laravel.com/docs/10.x/sail)을 사용할 경우, Sail 명령어로 Node와 NPM의 버전을 확인할 수도 있습니다:

```sh
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
<!-- ### Installing Vite and the Laravel Plugin -->
### Installing Vite and the Laravel Plugin

<!-- Within a fresh installation of Laravel, you will find a `package.json` file in the root of your application's directory structure. The default `package.json` file already includes everything you need to get started using Vite and the Laravel plugin. You may install your application's frontend dependencies via NPM: -->
새로 설치된 Laravel 프로젝트의 루트 디렉터리에는 `package.json` 파일이 존재합니다. 기본 `package.json`에는 이미 Vite와 Laravel 플러그인을 사용하는 데 필요한 설정이 모두 포함되어 있습니다. NPM 명령어로 프런트엔드 의존성을 설치하세요:

```sh
npm install
```

<a name="configuring-vite"></a>
<!-- ### Configuring Vite -->
### Configuring Vite

<!-- Vite is configured via a `vite.config.js` file in the root of your project. You are free to customize this file based on your needs, and you may also install any other plugins your application requires, such as `@vitejs/plugin-vue` or `@vitejs/plugin-react`. -->
Vite의 설정은 프로젝트 루트의 `vite.config.js` 파일을 통해 이루어집니다. 이 파일은 프로젝트 요구 사항에 맞게 자유롭게 커스터마이즈할 수 있으며, `@vitejs/plugin-vue`나 `@vitejs/plugin-react`처럼 추가 플러그인을 설치해 사용할 수 있습니다.

<!-- The Laravel Vite plugin requires you to specify the entry points for your application. These may be JavaScript or CSS files, and include preprocessed languages such as TypeScript, JSX, TSX, and Sass. -->
Laravel Vite 플러그인을 사용할 때는 애플리케이션의 엔트리 포인트를 지정해야 합니다. 이 엔트리 포인트는 JavaScript나 CSS 파일일 수 있고, TypeScript, JSX, TSX, Sass 등 전처리 언어도 지원됩니다.

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
SPA(특히 Inertia를 사용하는 앱 등)를 개발할 경우, Vite는 CSS 엔트리 포인트 없이 사용하는 것이 가장 좋습니다:

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
대신, CSS를 JavaScript 파일에서 직접 import해야 합니다. 일반적으로 애플리케이션의 `resources/js/app.js` 파일에서 이 작업을 수행합니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

<!-- The Laravel plugin also supports multiple entry points and advanced configuration options such as [SSR entry points](#ssr). -->
Laravel 플러그인은 여러 엔트리 포인트 및 [SSR entry points](#ssr)처럼 고급 설정도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
<!-- #### Working With a Secure Development Server -->
#### Working With a Secure Development Server

<!-- If your local development web server is serving your application via HTTPS, you may run into issues connecting to the Vite development server. -->
로컬 개발 웹서버가 HTTPS로 애플리케이션을 서비스하는 경우, Vite 개발 서버와의 연결에 문제가 발생할 수 있습니다.

<!-- If you are using [Laravel Herd](https://herd.laravel.com) and have secured the site or you are using [Laravel Valet](/docs/10.x/valet) and have run the [secure command](/docs/10.x/valet#securing-sites) against your application, the Laravel Vite plugin will automatically detect and use the generated TLS certificate for you. -->
[Laravel Herd](https://herd.laravel.com)에서 사이트를 보안 처리했거나, [Laravel Valet](/docs/10.x/valet)에서 [secure command](/docs/10.x/valet#securing-sites)를 실행했다면, Laravel Vite 플러그인이 자동으로 TLS 인증서를 인식해 사용합니다.

<!-- If you secured the site using a host that does not match the application's directory name, you may manually specify the host in your application's `vite.config.js` file: -->
만약 사이트를 애플리케이션 디렉터리명과 일치하지 않는 호스트로 보안 처리했다면, 애플리케이션의 `vite.config.js` 파일에 호스트를 직접 지정할 수 있습니다:

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
별도의 웹 서버를 사용하는 경우, 신뢰할 수 있는 인증서를 생성한 후, 직접 Vite에 해당 인증서를 사용하도록 설정해야 합니다:

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

<!-- If you are unable to generate a trusted certificate for your system, you may install and configure the [`@vitejs/plugin-basic-ssl` plugin](https://github.com/vitejs/vite-plugin-basic-ssl). When using untrusted certificates, you will need to accept the certificate warning for Vite's development server in your browser by following the "Local" link in your console when running the `npm run dev` command. -->
시스템에 신뢰할 수 있는 인증서를 생성할 수 없다면, [`@vitejs/plugin-basic-ssl` plugin](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치해 설정할 수 있습니다. 신뢰되지 않는 인증서로 개발할 경우, 브라우저에서 Vite 개발 서버의 "Local" 링크에 직접 접속해 인증서 경고를 수락해야 합니다. (예: `npm run dev` 실행 후)

<a name="configuring-hmr-in-sail-on-wsl2"></a>
<!-- #### Running the Development Server in Sail on WSL2 -->
#### Running the Development Server in Sail on WSL2

<!-- When running the Vite development server within [Laravel Sail](/docs/10.x/sail) on Windows Subsystem for Linux 2 (WSL2), you should add the following configuration to your `vite.config.js` file to ensure the browser can communicate with the development server: -->
[Laravel Sail](/docs/10.x/sail)을 Windows Subsystem for Linux 2(WSL2)에서 사용한다면, 브라우저가 개발 서버와 정상적으로 통신할 수 있도록 `vite.config.js`에 아래와 같은 설정을 추가해야 합니다:

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

<!-- If your file changes are not being reflected in the browser while the development server is running, you may also need to configure Vite's [`server.watch.usePolling` option](https://vitejs.dev/config/server-options.html#server-watch). -->
개발 서버 실행 중 파일 변경 사항이 브라우저에 반영되지 않는다면, Vite의 [`server.watch.usePolling` option](https://vitejs.dev/config/server-options.html#server-watch) 설정도 고려해보세요.

<a name="loading-your-scripts-and-styles"></a>
<!-- ### Loading Your Scripts and Styles -->
### Loading Your Scripts and Styles

<!-- With your Vite entry points configured, you may now reference them in a `@vite()` Blade directive that you add to the `<head>` of your application's root template: -->
Vite 엔트리 포인트를 설정했다면, 이제 블레이드 템플릿의 `<head>` 태그 내부에서 `@vite()` 디렉티브로 에셋을 참조할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

<!-- If you're importing your CSS via JavaScript, you only need to include the JavaScript entry point: -->
CSS를 JavaScript 파일을 통해 import하는 경우에는 JavaScript 엔트리 포인트만 지정해도 충분합니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

<!-- The `@vite` directive will automatically detect the Vite development server and inject the Vite client to enable Hot Module Replacement. In build mode, the directive will load your compiled and versioned assets, including any imported CSS. -->
`@vite` 디렉티브는 개발 모드에서 Vite 개발 서버를 자동으로 감지하여 Hot Module Replacement를 위해 Vite 클라이언트를 주입합니다. 빌드 모드에서는 컴파일되고 버전이 적용된 에셋(및 import된 CSS)을 불러옵니다.

<!-- If needed, you may also specify the build path of your compiled assets when invoking the `@vite` directive: -->
빌드 된 에셋의 경로가 기본이 아닌 경우, `@vite` 디렉티브에 빌드 경로를 추가로 지정할 수 있습니다:

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
경우에 따라 에셋을 외부에서 링크하지 않고, 자산의 실제 내용을 직접 포함해야 할 때가 있습니다. 예를 들어, HTML 내용을 PDF 생성기에 전달할 때 페이지에 직접 자산 내용을 삽입할 수도 있습니다. `Vite` 파사드에서 제공하는 `content` 메서드를 사용해 에셋의 내용을 출력할 수 있습니다:

```blade
@php
use Illuminate\Support\Facades\Vite;
@endphp

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
Vite를 실행하는 방법은 두 가지가 있습니다. 로컬 개발 시에는 `dev` 명령어로 개발 서버를 실행하면 됩니다. 개발 서버는 파일 변경을 자동으로 감지해, 열린 브라우저 창에 즉시 반영합니다.

<!-- Or, running the `build` command will version and bundle your application's assets and get them ready for you to deploy to production: -->
또는, `build` 명령어로 자산을 버전 관리하며 번들링하여, 프로덕션 배포용으로 준비할 수 있습니다:

```shell
# Run the Vite development server...
npm run dev

# Build and version the assets for production...
npm run build
```

<!-- If you are running the development server in [Sail](/docs/10.x/sail) on WSL2, you may need some [additional configuration](#configuring-hmr-in-sail-on-wsl2) options. -->
[Sail](/docs/10.x/sail)을 WSL2 환경에서 개발 서버를 실행하는 경우 [additional configuration](#configuring-hmr-in-sail-on-wsl2)이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
<!-- ## Working With JavaScript -->
## Working With JavaScript

<a name="aliases"></a>
<!-- ### Aliases -->
### Aliases

<!-- By default, The Laravel plugin provides a common alias to help you hit the ground running and conveniently import your application's assets: -->
기본적으로 Laravel 플러그인은, 여러분이 바로 생산성을 낼 수 있도록 자주 사용하는 경로에 대한 일반적인 별칭을 제공합니다:

```js
{
    '@' => '/resources/js'
}
```

<!-- You may overwrite the `'@'` alias by adding your own to the `vite.config.js` configuration file: -->
이 `'@'` 별칭은 `vite.config.js` 파일에서 직접 덮어써 원하는 경로로 변경할 수 있습니다:

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
[Vue](https://vuejs.org/) 프레임워크로 프론트엔드를 개발하려면, `@vitejs/plugin-vue` 플러그인을 추가로 설치해야 합니다:

```sh
npm install --save-dev @vitejs/plugin-vue
```

<!-- You may then include the plugin in your `vite.config.js` configuration file. There are a few additional options you will need when using the Vue plugin with Laravel: -->
그 후, 해당 플러그인을 `vite.config.js` 파일에 아래와 같이 적용합니다. Laravel과 함께 Vue 플러그인을 사용할 때에는 몇 가지 추가 옵션 지정이 필요합니다:

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
> Laravel의 [starter kits](/docs/10.x/starter-kits)에는 이미 Laravel, Vue, Vite가 올바르게 구성되어 있습니다. Laravel, Vue, Vite를 가장 빠르게 시작하려면 [Laravel Breeze](/docs/10.x/starter-kits#breeze-and-inertia)를 확인하세요.

<a name="react"></a>
<!-- ### React -->
### React

<!-- If you would like to build your frontend using the [React](https://reactjs.org/) framework, then you will also need to install the `@vitejs/plugin-react` plugin: -->
[React](https://reactjs.org/) 프레임워크로 프론트엔드를 개발하려면, `@vitejs/plugin-react` 플러그인을 추가로 설치해야 합니다:

```sh
npm install --save-dev @vitejs/plugin-react
```

<!-- You may then include the plugin in your `vite.config.js` configuration file: -->
그 후, 해당 플러그인을 `vite.config.js` 파일에 아래와 같이 적용합니다:

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
JSX가 포함된 파일은 `.jsx` 또는 `.tsx` 확장자로 저장해야 하며, 필요하다면 엔트리 포인트도 [shown above](#configuring-vite) 수정해야 합니다.

<!-- You will also need to include the additional `@viteReactRefresh` Blade directive alongside your existing `@vite` directive. -->
또한, 기존의 `@vite` 디렉티브와 함께 추가로 `@viteReactRefresh` Blade 디렉티브를 포함해야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

<!-- The `@viteReactRefresh` directive must be called before the `@vite` directive. -->
`@viteReactRefresh` 디렉티브는 반드시 `@vite` 디렉티브 이전에 호출해야 합니다.

> [!NOTE]
> Laravel의 [starter kits](/docs/10.x/starter-kits)에는 이미 Laravel, React, Vite가 올바르게 구성되어 있습니다. Laravel, React, Vite를 가장 빠르게 시작하려면 [Laravel Breeze](/docs/10.x/starter-kits#breeze-and-inertia)를 확인하세요.

<a name="inertia"></a>
<!-- ### Inertia -->
### Inertia

<!-- The Laravel Vite plugin provides a convenient `resolvePageComponent` function to help you resolve your Inertia page components. Below is an example of the helper in use with Vue 3; however, you may also utilize the function in other frameworks such as React: -->
Laravel Vite 플러그인은 Inertia 페이지 컴포넌트 로딩을 쉽게 해주는 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3에서의 사용 예시이지만 React 등 다른 프레임워크에서도 동일하게 활용할 수 있습니다:

```js
import { createApp, h } from 'vue';
import { createInertiaApp } from '@inertiajs/vue3';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';

createInertiaApp({
  resolve: (name) => resolvePageComponent(`./Pages/${name}.vue`, import.meta.glob('./Pages/**/*.vue')),
  setup({ el, App, props, plugin }) {
    return createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el)
  },
});
```

> [!NOTE]
> Laravel의 [starter kits](/docs/10.x/starter-kits)에는 이미 Laravel, Inertia, Vite가 올바르게 구성되어 있습니다. Laravel, Inertia, Vite를 가장 빠르게 시작하려면 [Laravel Breeze](/docs/10.x/starter-kits#breeze-and-inertia)를 확인하세요.

<a name="url-processing"></a>
<!-- ### URL Processing -->
### URL Processing

<!-- When using Vite and referencing assets in your application's HTML, CSS, or JS, there are a couple of caveats to consider. First, if you reference assets with an absolute path, Vite will not include the asset in the build; therefore, you should ensure that the asset is available in your public directory. -->
Vite를 사용할 때, HTML, CSS, JS에서 에셋을 참조하는 방법에는 몇 가지 주의사항이 있습니다. 첫째, **절대 경로**로 자산을 참조하면 Vite가 해당 에셋을 빌드에 포함하지 않습니다. 따라서 public 디렉터리에 해당 에셋이 존재해야 합니다.

<!-- When referencing relative asset paths, you should remember that the paths are relative to the file where they are referenced. Any assets referenced via a relative path will be re-written, versioned, and bundled by Vite. -->
반면, **상대 경로**로 자산을 참조하면, Vite가 경로를 다시 작성하여 버전 및 번들링 처리해줍니다. 경로는 파일 위치 기준임에 유의해야 합니다.

<!-- Consider the following project structure: -->
다음은 예시 프로젝트 구조입니다:

```nothing
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
그리고, Vite가 상대/절대 경로를 처리하는 예시는 다음과 같습니다:

```html
<!-- This asset is not handled by Vite and will not be included in the build -->
<img src="/taylor.png">

<!-- This asset will be re-written, versioned, and bundled by Vite -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
<!-- ## Working With Stylesheets -->
## Working With Stylesheets

<!-- You can learn more about Vite's CSS support within the [Vite documentation](https://vitejs.dev/guide/features.html#css). If you are using PostCSS plugins such as [Tailwind](https://tailwindcss.com), you may create a `postcss.config.js` file in the root of your project and Vite will automatically apply it: -->
Vite의 CSS 지원에 대한 좀 더 상세한 내용은 [Vite documentation](https://vitejs.dev/guide/features.html#css)에서 확인할 수 있습니다. [Tailwind](https://tailwindcss.com)처럼 PostCSS 플러그인을 사용할 경우, 프로젝트 루트에 `postcss.config.js` 파일을 생성하세요. Vite가 자동으로 적용합니다:

```js
export default {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
```

> [!NOTE]
> Laravel의 [starter kits](/docs/10.x/starter-kits)에는 Tailwind, PostCSS, Vite 설정이 이미 모두 포함되어 있습니다. 별도의 스타터 키트 없이 Tailwind + Laravel을 사용하고 싶다면 [Tailwind's installation guide for Laravel](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

<a name="working-with-blade-and-routes"></a>
<!-- ## Working With Blade and Routes -->
## Working With Blade and Routes

<a name="blade-processing-static-assets"></a>
<!-- ### Processing Static Assets With Vite -->
### Processing Static Assets With Vite

<!-- When referencing assets in your JavaScript or CSS, Vite automatically processes and versions them. In addition, when building Blade based applications, Vite can also process and version static assets that you reference solely in Blade templates. -->
JS나 CSS에서 에셋을 참조할 때 Vite가 자산을 자동으로 처리하고, 버전까지 부여합니다. Blade 기반 애플리케이션을 빌드할 때, Blade 템플릿에서만 참조되는 정적 자산도 Vite로 처리 및 버전 관리할 수 있습니다.

<!-- However, in order to accomplish this, you need to make Vite aware of your assets by importing the static assets into the application's entry point. For example, if you want to process and version all images stored in `resources/images` and all fonts stored in `resources/fonts`, you should add the following in your application's `resources/js/app.js` entry point: -->
이를 위해서는 해당 에셋들을 애플리케이션의 엔트리 포인트에서 import해 Vite가 인식할 수 있게 해야 합니다. 예를 들어, `resources/images` 폴더의 모든 이미지와 `resources/fonts`의 모든 폰트를 처리하려면, `resources/js/app.js` 파일에 다음을 추가하세요:

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

<!-- These assets will now be processed by Vite when running `npm run build`. You can then reference these assets in Blade templates using the `Vite::asset` method, which will return the versioned URL for a given asset: -->
이제 위 자산들은 `npm run build` 시 Vite가 모두 처리하게 됩니다. Blade 템플릿에서는 `Vite::asset` 메서드로 버전 URL을 쉽게 참조할 수 있습니다:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

<a name="blade-refreshing-on-save"></a>
<!-- ### Refreshing on Save -->
### Refreshing on Save

<!-- When your application is built using traditional server-side rendering with Blade, Vite can improve your development workflow by automatically refreshing the browser when you make changes to view files in your application. To get started, you can simply specify the `refresh` option as `true`. -->
Blade 기반의 전통적인 서버 사이드 렌더링 애플리케이션에서도, 개발 중 뷰 파일을 수정하면 Vite가 자동으로 브라우저 새로고침을 수행할 수 있습니다. 가장 간단한 방법은 `refresh` 옵션을 `true`로 지정하는 것입니다.

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
`refresh` 옵션이 `true`인 경우, 아래 경로 내 파일 저장 시 `npm run dev` 실행 중 자동으로 전체 페이지가 새로고침됩니다:

<!--
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`
-->
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

<!-- Watching the `routes/**` directory is useful if you are utilizing [Ziggy](https://github.com/tighten/ziggy) to generate route links within your application's frontend. -->
`routes/**` 디렉터리도 감시하는데, [Ziggy](https://github.com/tighten/ziggy)로 프론트엔드 라우트 링크 생성을 활용할 때 유용합니다.

<!-- If these default paths do not suit your needs, you can specify your own list of paths to watch: -->
기본 경로 이외에 다른 경로를 감시하고 싶다면, 경로 배열을 직접 지정할 수 있습니다:

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

<!-- Under the hood, the Laravel Vite plugin uses the [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload) package, which offers some advanced configuration options to fine-tune this feature's behavior. If you need this level of customization, you may provide a `config` definition: -->
실제로는 [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload) 패키지를 사용하므로, 고급 옵션이 필요하다면 `config` 오브젝트로 세부 설정이 가능합니다:

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

<!-- It is common in JavaScript applications to [create aliases](#aliases) to regularly referenced directories. But, you may also create aliases to use in Blade by using the `macro` method on the `Illuminate\Support\Facades\Vite` class. Typically, "macros" should be defined within the `boot` method of a [service provider](/docs/10.x/providers): -->
JavaScript에서는 자주 참조하는 디렉터리에 [create aliases](#aliases)을 만드는 일이 흔합니다. Blade에서도 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 이용해 별칭을 정의할 수 있습니다. 일반적으로 "매크로"는 [service provider](/docs/10.x/providers)의 `boot` 메서드 내에 정의합니다:

```
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

<!-- Once a macro has been defined, it can be invoked within your templates. For example, we can use the `image` macro defined above to reference an asset located at `resources/images/logo.png`: -->
매크로가 정의된 후에는, Blade 템플릿에서 사용할 수 있습니다. 예를 들어, 위의 `image` 매크로를 사용하면 `resources/images/logo.png` 경로의 에셋을 다음과 같이 참조할 수 있습니다:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="custom-base-urls"></a>
<!-- ## Custom Base URLs -->
## Custom Base URLs

<!-- If your Vite compiled assets are deployed to a domain separate from your application, such as via a CDN, you must specify the `ASSET_URL` environment variable within your application's `.env` file: -->
Vite로 빌드된 에셋을 별도의 도메인(예: CDN)에서 서비스하는 경우, 애플리케이션의 `.env` 파일에 `ASSET_URL` 환경 변수를 지정해야 합니다:

```env
ASSET_URL=https://cdn.example.com
```

<!-- After configuring the asset URL, all re-written URLs to your assets will be prefixed with the configured value: -->
설정 후, 에셋의 경로는 지정한 값으로 자동으로 접두어가 붙어 출력됩니다:

```nothing
https://cdn.example.com/build/assets/app.9dce8d17.js
```

<!-- Remember that [absolute URLs are not re-written by Vite](#url-processing), so they will not be prefixed. -->
[absolute URLs are not re-written by Vite](#url-processing). 즉, 이러한 경로에는 접두어가 적용되지 않습니다.

<a name="environment-variables"></a>
<!-- ## Environment Variables -->
## Environment Variables

<!-- You may inject environment variables into your JavaScript by prefixing them with `VITE_` in your application's `.env` file: -->
`.env` 파일에서 `VITE_`로 시작하는 환경 변수는 JavaScript 코드에 주입할 수 있습니다:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

<!-- You may access injected environment variables via the `import.meta.env` object: -->
주입된 변수는 `import.meta.env` 오브젝트에서 접근할 수 있습니다:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
<!-- ## Disabling Vite in Tests -->
## Disabling Vite in Tests

<!-- Laravel's Vite integration will attempt to resolve your assets while running your tests, which requires you to either run the Vite development server or build your assets. -->
테스트 실행 중에도 Laravel의 Vite 통합이 자산을 해결하려고 시도하며, 이때 Vite 개발 서버를 실행하거나 빌드된 에셋이 존재해야 합니다.

<!-- If you would prefer to mock Vite during testing, you may call the `withoutVite` method, which is available for any tests that extend Laravel's `TestCase` class: -->
테스트에서 Vite 관련 처리를 mock(생략)하고 싶다면, Laravel의 `TestCase` 클래스를 확장한 테스트에서 제공되는 `withoutVite` 메서드를 호출하면 됩니다:

```php
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
모든 테스트에서 항상 Vite를 비활성화하려면, 베이스 `TestCase` 클래스의 `setUp` 메서드에서 `withoutVite`를 호출하세요:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;

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
Laravel Vite 플러그인을 사용하면 Vite 기반의 서버 사이드 렌더링도 손쉽게 설정 가능합니다. 먼저 `resources/js/ssr.js` 위치에 SSR 엔트리 포인트 파일을 생성한 뒤, 플러그인 설정에 해당 엔트리 포인트를 명시합니다:

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
SSR 엔트리 포인트 빌드를 잊지 않기 위해, 애플리케이션의 `package.json`의 "build" 스크립트를 다음과 같이 보강하는 방법을 권장합니다:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

<!-- Then, to build and start the SSR server, you may run the following commands: -->
이제 SSR 서버를 빌드 및 실행하려면 아래 명령어를 사용하세요:

```sh
npm run build
node bootstrap/ssr/ssr.js
```

<!-- If you are using [SSR with Inertia](https://inertiajs.com/server-side-rendering), you may instead use the `inertia:start-ssr` Artisan command to start the SSR server: -->
[SSR with Inertia](https://inertiajs.com/server-side-rendering), `inertia:start-ssr` Artisan 명령어로도 SSR 서버를 시작할 수 있습니다:

```sh
php artisan inertia:start-ssr
```

> [!NOTE]
> Laravel의 [starter kits](/docs/10.x/starter-kits)에는 Inertia SSR 및 Vite가 올바르게 구성되어 있습니다. Laravel, Inertia SSR, Vite를 가장 빠르게 시작하려면 [Laravel Breeze](/docs/10.x/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="script-and-style-attributes"></a>
<!-- ## Script and Style Tag Attributes -->
## Script and Style Tag Attributes

<a name="content-security-policy-csp-nonce"></a>
<!-- ### Content Security Policy (CSP) Nonce -->
### Content Security Policy (CSP) Nonce

<!-- If you wish to include a [`nonce` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) on your script and style tags as part of your [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP), you may generate or specify a nonce using the `useCspNonce` method within a custom [middleware](/docs/10.x/middleware): -->
[`nonce` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)의 일부로서, 스크립트와 스타일 태그에 [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)을 포함하고 싶다면, 커스텀 [middleware](/docs/10.x/middleware)에서 `useCspNonce` 메서드로 nonce를 생성 또는 지정할 수 있습니다:

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
`useCspNonce` 메서드 호출 이후에는, 생성되는 모든 스크립트 및 스타일 태그에 자동으로 `nonce` 속성이 추가됩니다.

<!-- If you need to specify the nonce elsewhere, including the [Ziggy `@route` directive](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) included with Laravel's [starter kits](/docs/10.x/starter-kits), you may retrieve it using the `cspNonce` method: -->
[Ziggy `@route` directive](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy)처럼 Laravel의 [starter kits](/docs/10.x/starter-kits)에 포함된 곳을 비롯해 다른 위치에서 nonce를 지정해야 한다면, `cspNonce` 메서드로 값을 가져올 수 있습니다:

```blade
@routes(nonce: Vite::cspNonce())
```

<!-- If you already have a nonce that you would like to instruct Laravel to use, you may pass the nonce to the `useCspNonce` method: -->
이미 보유 중인 nonce 값을 Laravel에 지정하려면, `useCspNonce` 메서드에 해당 값을 전달하세요:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
<!-- ### Subresource Integrity (SRI) -->
### Subresource Integrity (SRI)

<!-- If your Vite manifest includes `integrity` hashes for your assets, Laravel will automatically add the `integrity` attribute on any script and style tags it generates in order to enforce [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity). By default, Vite does not include the `integrity` hash in its manifest, but you may enable it by installing the [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM plugin: -->
Vite 매니페스트에 에셋별 `integrity` 해시가 포함되어 있다면, Laravel은 자동으로 생성되는 모든 스크립트 및 스타일 태그에 `integrity` 속성을 추가하여 [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)를 적용합니다. 기본적으로 Vite는 manifest에 `integrity` 해시를 포함하지 않으나, [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) 플러그인을 설치해 활성화할 수 있습니다:

```shell
npm install --save-dev vite-plugin-manifest-sri
```

<!-- You may then enable this plugin in your `vite.config.js` file: -->
그 후, `vite.config.js` 파일에서 해당 플러그인을 아래와 같이 적용합니다:

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
필요하다면 매니페스트에서 무결성 해시가 저장된 키명을 커스텀할 수도 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

<!-- If you would like to disable this auto-detection completely, you may pass `false` to the `useIntegrityKey` method: -->
자동 감지를 완전히 비활성화하고 싶다면, `useIntegrityKey`에 `false`를 전달하세요:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
<!-- ### Arbitrary Attributes -->
### Arbitrary Attributes

<!-- If you need to include additional attributes on your script and style tags, such as the [`data-turbo-track`](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) attribute, you may specify them via the `useScriptTagAttributes` and `useStyleTagAttributes` methods. Typically, this methods should be invoked from a [service provider](/docs/10.x/providers): -->
[`data-turbo-track`](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 등 추가 속성을 스크립트, 스타일 태그에 지정하고 싶을 때는, `useScriptTagAttributes`, `useStyleTagAttributes` 메서드로 지정할 수 있습니다. 보통 이런 설정은 [service provider](/docs/10.x/providers)에서 수행합니다:

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
조건부로 속성 값을 지정하고 싶다면, 콜백을 넘겨서 asset 소스 경로, URL, 매니페스트 청크 및 전체 매니페스트를 기준으로 처리할 수 있습니다:

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
> Vite 개발 서버가 동작하는 동안에는 `$chunk`, `$manifest` 인자가 `null` 값이 될 수 있습니다.

<a name="advanced-customization"></a>
<!-- ## Advanced Customization -->
## Advanced Customization

<!-- Out of the box, Laravel's Vite plugin uses sensible conventions that should work for the majority of applications; however, sometimes you may need to customize Vite's behavior. To enable additional customization options, we offer the following methods and options which can be used in place of the `@vite` Blade directive: -->
기본적으로 Laravel의 Vite 플러그인은 대부분의 프로젝트에 적합하도록 합리적인 기본 설정을 제공합니다. 하지만 Vite의 동작을 추가로 조정해야 할 경우, `@vite` Blade 디렉티브 대신 다음과 같은 메서드 및 옵션으로 세밀하게 설정할 수 있습니다:

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
또한 `vite.config.js`에서도 동일한 커스터마이즈로 동작을 일치시켜야 합니다:

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

<a name="correcting-dev-server-urls"></a>
<!-- ### Correcting Dev Server URLs -->
### Correcting Dev Server URLs

<!-- Some plugins within the Vite ecosystem assume that URLs which begin with a forward-slash will always point to the Vite dev server. However, due to the nature of the Laravel integration, this is not the case. -->
Vite 에코시스템 내 일부 플러그인들은 슬래시(/)로 시작하는 URL이면 Vite 개발 서버를 향한다고 가정합니다. 그러나 Laravel 통합 환경에서는 항상 그렇지 않을 수 있습니다.

<!-- For example, the `vite-imagetools` plugin outputs URLs like the following while Vite is serving your assets: -->
예를 들어, `vite-imagetools` 플러그인은 에셋을 Vite가 서비스할 때 다음과 같은 URL을 출력합니다:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

<!-- The `vite-imagetools` plugin is expecting that the output URL will be intercepted by Vite and the plugin may then handle all URLs that start with `/@imagetools`. If you are using plugins that are expecting this behaviour, you will need to manually correct the URLs. You can do this in your `vite.config.js` file by using the `transformOnServe` option. -->
이 때 `vite-imagetools` 플러그인은 `/@imagetools`로 시작하는 URL이 Vite에 의해 가로채진다고 기대합니다. 이러한 플러그인과 함께 사용할 때는 URL을 수동으로 수정해야 할 수 있습니다. `vite.config.js`의 `transformOnServe` 옵션을 사용하면 해결할 수 있습니다.

<!-- In this particular example, we will prepend the dev server URL to all occurrences of `/@imagetools` within the generated code: -->
아래 예시처럼, 생성된 코드 내의 `/@imagetools` 부분을 dev 서버 URL로 교체할 수 있습니다:

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
이제 Vite가 에셋을 서비스하면, 아래처럼 개발 서버 주소가 붙어 출력됩니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```
