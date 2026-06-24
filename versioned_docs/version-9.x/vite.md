<!-- # Asset Bundling (Vite) -->
# Asset Bundling (Vite)

- [Introduction](#introduction)
- [Installation & Setup](#installation)
    - [Installing Node](#installing-node)
    - [Installing Vite And The Laravel Plugin](#installing-vite-and-laravel-plugin)
    - [Configuring Vite](#configuring-vite)
    - [Loading Your Scripts And Styles](#loading-your-scripts-and-styles)
- [Running Vite](#running-vite)
- [Working With JavaScript](#working-with-scripts)
    - [Aliases](#aliases)
    - [Vue](#vue)
    - [React](#react)
    - [Inertia](#inertia)
    - [URL Processing](#url-processing)
- [Working With Stylesheets](#working-with-stylesheets)
- [Working With Blade & Routes](#working-with-blade-and-routes)
    - [Processing Static Assets With Vite](#blade-processing-static-assets)
    - [Refreshing On Save](#blade-refreshing-on-save)
    - [Aliases](#blade-aliases)
- [Custom Base URLs](#custom-base-urls)
- [Environment Variables](#environment-variables)
- [Disabling Vite In Tests](#disabling-vite-in-tests)
- [Server-Side Rendering (SSR)](#ssr)
- [Script & Style Tag Attributes](#script-and-style-attributes)
    - [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)
    - [Subresource Integrity (SRI)](#subresource-integrity-sri)
    - [Arbitrary Attributes](#arbitrary-attributes)
- [Advanced Customization](#advanced-customization)
    - [Correcting Dev Server URLs](#correcting-dev-server-urls)

<a name="introduction"></a>

<!-- ## Introduction -->
## Introduction

<!-- [Vite](https://vitejs.dev) is a modern frontend build tool that provides an extremely fast development environment and bundles your code for production. When building applications with Laravel, you will typically use Vite to bundle your application's CSS and JavaScript files into production ready assets. -->
[Vite](https://vitejs.dev)는 최신 프론트엔드 빌드 도구로, 매우 빠른 개발 환경을 제공하며 코드를 프로덕션용으로 번들링할 수 있게 해줍니다. Laravel로 애플리케이션을 개발할 때, 보통 Vite를
사용하여 애플리케이션의 CSS와 자바스크립트 파일을 프로덕션에 배포할 수 있는 에셋으로 번들링합니다.

<!-- Laravel integrates seamlessly with Vite by providing an official plugin and Blade directive to load your assets for development and production. -->
Laravel은 공식 플러그인과 Blade 디렉티브를 제공하여 개발 및 프로덕션 환경 모두에서 Vite와의 통합을 매우 쉽게 지원합니다.

> [!NOTE]
> Laravel Mix를 사용하고 계신가요? 이제 Vite가 새로운 Laravel 설치의 기본 빌드 도구가 되었습니다. Mix 관련 문서는 [Laravel Mix](https://laravel-mix.com/) 공식 사이트에서
> 확인하실 수 있습니다. Vite로
> 전환하려면 [migration guide](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고해
> 주세요.

<a name="vite-or-mix"></a>

<!-- #### Choosing Between Vite And Laravel Mix -->
#### Choosing Between Vite And Laravel Mix

<!-- Before transitioning to Vite, new Laravel applications utilized [Mix](https://laravel-mix.com/), which is powered by [webpack](https://webpack.js.org/), when bundling assets. Vite focuses on providing a faster and more productive experience when building rich JavaScript applications. If you are developing a Single Page Application (SPA), including those developed with tools like [Inertia](https://inertiajs.com), Vite will be the perfect fit. -->
이전에는 새로 만든 Laravel 애플리케이션에서 에셋 번들링에 [Mix](https://laravel-mix.com/)를 사용했습니다. Mix는 [webpack](https://webpack.js.org/) 기반입니다.
Vite는 리치 자바스크립트 애플리케이션 개발 시 훨씬 빠르고 생산적인 개발 경험을 제공하는 것을 목표로 하고 있습니다. [Inertia](https://inertiajs.com) 등과 같은 도구를 활용한 싱글
페이지 애플리케이션(SPA)을 개발한다면 Vite가 매우 잘 맞습니다.

<!-- Vite also works well with traditional server-side rendered applications with JavaScript "sprinkles", including those using [Livewire](https://laravel-livewire.com). However, it lacks some features that Laravel Mix supports, such as the ability to copy arbitrary assets into the build that are not referenced directly in your JavaScript application. -->
Vite는 [Livewire](https://laravel-livewire.com)와 같이 전통적인 서버 사이드 렌더링 방식의 애플리케이션에서도 자바스크립트 "스프링클"이 필요한 부분에 무리 없이 사용할 수
있습니다. 다만, Laravel Mix가 지원하는 임의의 에셋을 번들에 포함하는 기능 등 몇몇 기능은 제공하지 않습니다. 즉, 자바스크립트에서 직접 참조되지 않는 파일을 복사하는 기능 등은 Mix만 지원합니다.

<a name="migrating-back-to-mix"></a>

<!-- #### Migrating Back To Mix -->
#### Migrating Back To Mix

<!-- Have you started a new Laravel application using our Vite scaffolding but need to move back to Laravel Mix and webpack? No problem. Please consult our [official guide on migrating from Vite to Mix](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix). -->
Vite 구조로 새 Laravel 애플리케이션을 시작했지만, 다시 Laravel Mix와 webpack으로 돌아가야 할 필요가 생겼나요? 문제
없습니다. [official guide on migrating from Vite to Mix](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix)
를 참고해 주세요.

<a name="installation"></a>

<!-- ## Installation & Setup -->
## Installation & Setup

> [!NOTE]
> 여기의 문서는 Laravel Vite 플러그인을 직접 설치하고 설정하는 방법에 대해 설명합니다. 하지만 Laravel의 [starter kits](/docs/9.x/starter-kits)는 이 모든 설정을 포함하고 있으니, Laravel과
> Vite를 빠르게 시작하고 싶다면 스타터 키트를 활용하는 것이 가장 쉽습니다.

<a name="installing-node"></a>

<!-- ### Installing Node -->
### Installing Node

<!-- You must ensure that Node.js (16+) and NPM are installed before running Vite and the Laravel plugin: -->
Vite와 Laravel 플러그인을 실행하려면 반드시 Node.js(16 이상)와 NPM이 설치되어 있어야 합니다.

```sh
node -v
npm -v
```

<!-- You can easily install the latest version of Node and NPM using simple graphical installers from [the official Node website](https://nodejs.org/en/download/). Or, if you are using [Laravel Sail](https://laravel.com/docs/9.x/sail), you may invoke Node and NPM through Sail: -->
최신 버전의 Node와 NPM은 [the official Node website](https://nodejs.org/en/download/)의 그래픽 설치 프로그램을 통해 쉽게 설치할 수 있습니다.
또는 [Laravel Sail](https://laravel.com/docs/9.x/sail)을 사용 중이라면 아래와 같이 Sail 명령어를 통해 Node와 NPM을 실행할 수도 있습니다.

```sh
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>

<!-- ### Installing Vite And The Laravel Plugin -->
### Installing Vite And The Laravel Plugin

<!-- Within a fresh installation of Laravel, you will find a `package.json` file in the root of your application's directory structure. The default `package.json` file already includes everything you need to get started using Vite and the Laravel plugin. You may install your application's frontend dependencies via NPM: -->
새로 설치한 Laravel 프로젝트의 루트 디렉터리에는 `package.json` 파일이 있습니다. 이 기본 `package.json` 파일 안에는 Vite 및 Laravel 플러그인을 사용하는 데 필요한 설정이 이미 포함되어
있습니다. NPM을 사용해 프론트엔드 의존성을 설치할 수 있습니다.

```sh
npm install
```

<a name="configuring-vite"></a>

<!-- ### Configuring Vite -->
### Configuring Vite

<!-- Vite is configured via a `vite.config.js` file in the root of your project. You are free to customize this file based on your needs, and you may also install any other plugins your application requires, such as `@vitejs/plugin-vue` or `@vitejs/plugin-react`. -->
Vite는 프로젝트 루트의 `vite.config.js` 파일을 통해 설정할 수 있습니다. 이 파일을 자신의 필요에 맞게 자유롭게 수정할 수 있으며, `@vitejs/plugin-vue`,
`@vitejs/plugin-react`와 같은 추가 플러그인도 설치할 수 있습니다.

<!-- The Laravel Vite plugin requires you to specify the entry points for your application. These may be JavaScript or CSS files, and include preprocessed languages such as TypeScript, JSX, TSX, and Sass. -->
Laravel Vite 플러그인에서는 애플리케이션의 엔트리 포인트를 명시해야 합니다. 이 엔트리 포인트는 자바스크립트 또는 CSS 파일일 수 있으며, TypeScript, JSX, TSX, Sass와 같은 사전처리 언어도
사용할 수 있습니다.

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
SPA(싱글 페이지 애플리케이션), 특히 Inertia 등으로 개발하는 경우에는 CSS 엔트리 포인트를 제외하는 것이 Vite와 가장 잘 맞습니다.

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
이 경우 CSS는 자바스크립트 내부에서 임포트해야 합니다. 보통 `resources/js/app.js` 파일에서 아래와 같이 작성합니다.

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

<!-- The Laravel plugin also supports multiple entry points and advanced configuration options such as [SSR entry points](#ssr). -->
Laravel 플러그인은 여러 엔트리 포인트 및 [SSR entry points](#ssr)와 같은 고급 설정도 지원합니다.

<a name="working-with-a-secure-development-server"></a>

<!-- #### Working With A Secure Development Server -->
#### Working With A Secure Development Server

<!-- If your local development web server is serving your application via HTTPS, you may run into issues connecting to the Vite development server. -->
로컬 개발용 웹 서버가 HTTPS로 애플리케이션을 서빙하는 경우, Vite 개발 서버와의 연결에서 문제가 발생할 수 있습니다.

<!-- If you are using [Laravel Valet](/docs/9.x/valet) for local development and have run the [secure command](/docs/9.x/valet#securing-sites) against your application, you may configure the Vite development server to automatically use Valet's generated TLS certificates: -->
[Laravel Valet](/docs/9.x/valet)를 사용해 로컬 개발을 진행하며 [secure command](/docs/9.x/valet#securing-sites)를 실행한 경우, 아래처럼 Valet가 생성한 TLS
인증서를 Vite 개발 서버에서 자동으로 사용하도록 설정할 수 있습니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            valetTls: 'my-app.test', // [tl! add]
        }),
    ],
});
```

<!-- When using another web server, you should generate a trusted certificate and manually configure Vite to use the generated certificates: -->
다른 웹 서버를 사용하는 경우에는 직접 신뢰할 수 있는 인증서를 생성하고, Vite에 해당 인증서 경로를 지정해야 합니다.

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
시스템에 신뢰할 수 있는 인증서를 발급할 수 없는 경우, [`@vitejs/plugin-basic-ssl` plugin](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치해
사용할 수 있습니다. 신뢰되지 않은 인증서를 사용할 때는 브라우저에서 인증서 경고를 수락해야 하며, `npm run dev` 명령어 실행 후 콘솔에 보이는 "Local" 링크를 클릭해서 접속하면 됩니다.

<a name="loading-your-scripts-and-styles"></a>

<!-- ### Loading Your Scripts And Styles -->
### Loading Your Scripts And Styles

<!-- With your Vite entry points configured, you only need reference them in a `@vite()` Blade directive that you add to the `<head>` of your application's root template: -->
Vite의 엔트리 포인트를 지정했다면, 이제 `@vite()` Blade 디렉티브를 애플리케이션의 루트 템플릿 `<head>` 부분에 추가하면 됩니다.

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

<!-- If you're importing your CSS via JavaScript, you only need to include the JavaScript entry point: -->
자바스크립트에서 CSS를 직접 임포트하는 경우, 자바스크립트 엔트리 포인트만 지정하면 됩니다.

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

<!-- The `@vite` directive will automatically detect the Vite development server and inject the Vite client to enable Hot Module Replacement. In build mode, the directive will load your compiled and versioned assets, including any imported CSS. -->
`@vite` 디렉티브는 Vite 개발 서버를 자동으로 감지하여 Hot Module Replacement를 위한 Vite 클라이언트를 주입해 줍니다. 빌드 모드에서는 번들링되고 버전이 적용된 에셋(임포트된 CSS
포함)을 자동으로 불러옵니다.

<!-- If needed, you may also specify the build path of your compiled assets when invoking the `@vite` directive: -->
필요하다면, `@vite` 디렉티브에서 빌드된 에셋의 경로를 직접 지정할 수도 있습니다.

```blade
<!doctype html>
<head>
    {{-- Given build path is relative to public path. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="running-vite"></a>

<!-- ## Running Vite -->
## Running Vite

<!-- There are two ways you can run Vite. You may run the development server via the `dev` command, which is useful while developing locally. The development server will automatically detect changes to your files and instantly reflect them in any open browser windows. -->
Vite를 실행하는 방법은 두 가지가 있습니다. 개발 과정에서는 `dev` 명령어로 개발 서버를 실행할 수 있습니다. 개발 서버는 파일 변경을 자동으로 감지하고, 열린 브라우저 창에서 바로 반영됩니다.

<!-- Or, running the `build` command will version and bundle your application's assets and get them ready for you to deploy to production: -->
또는, `build` 명령어를 사용하면 애플리케이션의 에셋이 번들링되고 버전이 적용되어 프로덕션 배포를 위해 준비됩니다.

```shell
# Run the Vite development server...
npm run dev

# Build and version the assets for production...
npm run build
```

<a name="working-with-scripts"></a>

<!-- ## Working With JavaScript -->
## Working With JavaScript

<a name="aliases"></a>

<!-- ### Aliases -->
### Aliases

<!-- By default, The Laravel plugin provides a common alias to help you hit the ground running and conveniently import your application's assets: -->
기본적으로 Laravel 플러그인은 애플리케이션 에셋을 더 쉽게 임포트할 수 있도록 아래와 같은 공통 별칭을 제공합니다.

```js
{
    '@' => '/resources/js'
}
```

<!-- You may overwrite the `'@'` alias by adding your own to the `vite.config.js` configuration file: -->
직접 `vite.config.js` 설정 파일에서 `'@'` 별칭을 덮어쓸 수도 있습니다.

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

<!-- If you would like to build your front-end using the [Vue](https://vuejs.org/) framework, then you will also need to install the `@vitejs/plugin-vue` plugin: -->
[Vue](https://vuejs.org/) 프레임워크로 프론트엔드를 개발하고자 한다면, `@vitejs/plugin-vue` 플러그인을 추가로 설치해야 합니다.

```sh
npm install --save-dev @vitejs/plugin-vue
```

<!-- You may then include the plugin in your `vite.config.js` configuration file. There are a few additional options you will need when using the Vue plugin with Laravel: -->
이후 `vite.config.js` 설정 파일에 해당 플러그인을 포함하면 됩니다. 또한, Laravel과 함께 Vue 플러그인을 사용할 때 몇 가지 옵션을 추가로 지정해주는 것이 좋습니다.

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
> Laravel의 [starter kits](/docs/9.x/starter-kits)에는 이미 올바른 Laravel, Vue, Vite 설정이 모두 포함되어 있습니다. Laravel, Vue, Vite를 빠르게 시작하고
> 싶다면 [Laravel Breeze](/docs/9.x/starter-kits#breeze-and-inertia)를 추천합니다.

<a name="react"></a>

<!-- ### React -->
### React

<!-- If you would like to build your front-end using the [React](https://reactjs.org/) framework, then you will also need to install the `@vitejs/plugin-react` plugin: -->
[React](https://reactjs.org/) 프레임워크를 사용할 때는 `@vitejs/plugin-react` 플러그인을 추가로 설치해야 합니다.

```sh
npm install --save-dev @vitejs/plugin-react
```

<!-- You may then include the plugin in your `vite.config.js` configuration file: -->
이 플러그인 역시 `vite.config.js` 설정 파일에 추가해줍니다.

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
JSX를 포함하는 파일은 `.jsx` 또는 `.tsx` 확장자를 사용해야 하며, 필요하다면 엔트리 포인트 역시 [shown above](#configuring-vite) 변경해야 합니다.

<!-- You will also need to include the additional `@viteReactRefresh` Blade directive alongside your existing `@vite` directive. -->
그리고 기존의 `@vite` 디렉티브와 함께 추가로 `@viteReactRefresh` Blade 디렉티브를 포함해야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

<!-- The `@viteReactRefresh` directive must be called before the `@vite` directive. -->
`@viteReactRefresh`는 반드시 `@vite`보다 먼저 호출되어야 합니다.

> [!NOTE]
> Laravel의 [starter kits](/docs/9.x/starter-kits)는 이미 Laravel, React, Vite의 적절한 설정을
> 제공합니다. [Laravel Breeze](/docs/9.x/starter-kits#breeze-and-inertia)로 시작하면 빠르고 편하게 React와 Vite를 사용할 수 있습니다.

<a name="inertia"></a>

<!-- ### Inertia -->
### Inertia

<!-- The Laravel Vite plugin provides a convenient `resolvePageComponent` function to help you resolve your Inertia page components. Below is an example of the helper in use with Vue 3; however, you may also utilize the function in other frameworks such as React: -->
Laravel Vite 플러그인은 Inertia 페이지 컴포넌트를 편리하게 불러오는 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3용 예제이지만, React 등 다른 프레임워크에서도 동일하게
활용할 수 있습니다.

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
> Laravel [starter kits](/docs/9.x/starter-kits)에는 이미 Inertia와 관련된 적절한 설정이 되어
> 있습니다. [Laravel Breeze](/docs/9.x/starter-kits#breeze-and-inertia)를 활용하면 Laravel, Inertia, Vite를 가장 쉽게 시작할 수 있습니다.

<a name="url-processing"></a>

<!-- ### URL Processing -->
### URL Processing

<!-- When using Vite and referencing assets in your application's HTML, CSS, or JS, there are a couple of caveats to consider. First, if you reference assets with an absolute path, Vite will not include the asset in the build; therefore, you should ensure that the asset is available in your public directory. -->
Vite와 함께 애플리케이션의 HTML, CSS, JS 등에서 에셋을 참조할 때는 몇 가지 주의해야 할 점이 있습니다. 먼저, 절대 경로(/로 시작하는 경로)로 에셋을 참조하면, Vite는 해당 파일을 빌드에
포함하지 않습니다. 그러므로 이 경우 해당 에셋이 public 디렉터리에 있어야 합니다.

<!-- When referencing relative asset paths, you should remember that the paths are relative to the file where they are referenced. Any assets referenced via a relative path will be re-written, versioned, and bundled by Vite. -->
상대 경로로 에셋을 참조하는 경우, 그 경로는 해당 파일(자바스크립트, CSS 등) 위치를 기준으로 합니다. 상대 경로를 사용한 에셋은 Vite가 자동으로 재작성, 버전 적용, 번들링을 해줍니다.

<!-- Consider the following project structure: -->
다음은 프로젝트 구조 예시입니다.

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
아래 예시는 Vite가 상대/절대 경로를 어떻게 처리하는지 보여줍니다.

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
Vite의 CSS 지원에 대한 자세한 내용은 [Vite documentation](https://vitejs.dev/guide/features.html#css)에서 확인할 수
있습니다. [Tailwind](https://tailwindcss.com)와 같은 PostCSS 플러그인을 사용한다면, 프로젝트 루트에 `postcss.config.js` 파일을 생성하면 Vite가 이를 자동으로
적용해줍니다.

```js
module.exports = {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
```

<a name="working-with-blade-and-routes"></a>

<!-- ## Working With Blade & Routes -->
## Working With Blade & Routes

<a name="blade-processing-static-assets"></a>

<!-- ### Processing Static Assets With Vite -->
### Processing Static Assets With Vite

<!-- When referencing assets in your JavaScript or CSS, Vite automatically processes and versions them. In addition, when building Blade based applications, Vite can also process and version static assets that you reference solely in Blade templates. -->
자바스크립트나 CSS에서 에셋을 참조할 경우, Vite가 자동으로 해당 에셋을 처리(버전 관리 및 빌드)해줍니다. 그리고 Blade 기반 애플리케이션의 경우, Blade 템플릿에서만 참조하는 정적 에셋도 Vite가
처리할 수 있습니다.

<!-- However, in order to accomplish this, you need to make Vite aware of your assets by importing the static assets into the application's entry point. For example, if you want to process and version all images stored in `resources/images` and all fonts stored in `resources/fonts`, you should add the following in your application's `resources/js/app.js` entry point: -->
이를 위해서는 반드시 해당 에셋을 애플리케이션의 엔트리 포인트에 임포트하여 Vite가 인식할 수 있도록 해야 합니다. 예를 들어, `resources/images`에 있는 모든 이미지와,
`resources/fonts`에 있는 모든 폰트 파일을 처리하고 싶다면, `resources/js/app.js` 엔트리 포인트에 아래와 같이 추가해야 합니다.

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

<!-- These assets will now be processed by Vite when running `npm run build`. You can then reference these assets in Blade templates using the `Vite::asset` method, which will return the versioned URL for a given asset: -->
이제 `npm run build`를 실행하면 해당 에셋들도 Vite에 의해 빌드됩니다. Blade 템플릿에서 해당 에셋을 참조할 때는 `Vite::asset` 메서드를 사용하면 버전이 포함된 URL이 반환됩니다.

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

<a name="blade-refreshing-on-save"></a>

<!-- ### Refreshing On Save -->
### Refreshing On Save

<!-- When your application is built using traditional server-side rendering with Blade, Vite can improve your development workflow by automatically refreshing the browser when you make changes to view files in your application. To get started, you can simply specify the `refresh` option as `true`. -->
Blade를 이용한 전통적인 서버 사이드 렌더링 애플리케이션이라면, Vite를 활용해 view 파일 저장 시 브라우저를 자동으로 새로고침할 수 있습니다. `refresh` 옵션을 `true`로 지정하면 바로 사용할
수 있습니다.

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
`refresh` 옵션을 `true`로 설정하면 아래 경로의 파일을 저장할 때, `npm run dev`로 실행 중인 브라우저에서 전체 페이지가 새로고침됩니다.

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
`routes/**` 디렉터리를 감시하는 것은 [Ziggy](https://github.com/tighten/ziggy)를 사용해 프론트엔드에서 라우트 링크를 생성하는 경우 유용합니다.

<!-- If these default paths do not suit your needs, you can specify your own list of paths to watch: -->
기본 경로가 필요에 맞지 않는 경우, 감시할 경로 목록을 직접 지정할 수도 있습니다.

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
내부적으로 Laravel Vite 플러그인은 [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload) 패키지를 사용하며, 고급 설정
옵션도 지원합니다. 좀 더 세밀하게 제어하고 싶다면 다음과 같이 `config` 옵션을 줄 수 있습니다.

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

<!-- It is common in JavaScript applications to [create aliases](#aliases) to regularly referenced directories. But, you may also create aliases to use in Blade by using the `macro` method on the `Illuminate\Support\Facades\Vite` class. Typically, "macros" should be defined within the `boot` method of a [service provider](/docs/9.x/providers): -->
자바스크립트에서는 [create aliases](#aliases) 자주 접근하는 경로를 편리하게 사용할 수 있습니다. 이와 비슷하게, Blade에서도 별칭을 사용할 수 있습니다. 이를 위해서는
`Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 활용하면 됩니다. 보통 [service provider](/docs/9.x/providers)의 `boot` 메서드에서 "매크로"를 등록합니다.

```
/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Vite::macro('image', fn ($asset) => $this->asset("resources/images/{$asset}"));
}
```

<!-- Once a macro has been defined, it can be invoked within your templates. For example, we can use the `image` macro defined above to reference an asset located at `resources/images/logo.png`: -->
매크로가 정의되면, 템플릿에서 다음과 같이 사용할 수 있습니다. 예를 들어, 위에서 정의한 `image` 매크로로 `resources/images/logo.png`에 있는 에셋을 참조할 수 있습니다.

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="custom-base-urls"></a>

<!-- ## Custom Base URLs -->
## Custom Base URLs

<!-- If your Vite compiled assets are deployed to a domain separate from your application, such as via a CDN, you must specify the `ASSET_URL` environment variable within your application's `.env` file: -->
Vite로 빌드된 에셋을 애플리케이션과 다른 도메인(예: CDN)에 배포하는 경우, `.env` 파일에서 `ASSET_URL` 환경 변수를 반드시 설정해 주세요.

```env
ASSET_URL=https://cdn.example.com
```

<!-- After configuring the asset URL, all re-written URLs to your assets will be prefixed with the configured value: -->
이렇게 설정한 후에는 모든 에셋 URL이 해당 값으로 프리픽스되어 사용됩니다.

```nothing
https://cdn.example.com/build/assets/app.9dce8d17.js
```

<!-- Remember that [absolute URLs are not re-written by Vite](#url-processing), so they will not be prefixed. -->
[absolute URLs are not re-written by Vite](#url-processing), 프리픽스가 적용되지 않는다는 점을 기억해야 합니다.

<a name="environment-variables"></a>

<!-- ## Environment Variables -->
## Environment Variables

<!-- You may inject environment variables into your JavaScript by prefixing them with `VITE_` in your application's `.env` file: -->
애플리케이션의 `.env` 파일에서 환경 변수명을 `VITE_`로 시작하도록 지정하면, 해당 변수를 자바스크립트 코드에서 사용할 수 있습니다.

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

<!-- You may access injected environment variables via the `import.meta.env` object: -->
주입된 환경 변수는 `import.meta.env` 객체를 통해 접근할 수 있습니다.

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>

<!-- ## Disabling Vite In Tests -->
## Disabling Vite In Tests

<!-- Laravel's Vite integration will attempt to resolve your assets while running your tests, which requires you to either run the Vite development server or build your assets. -->
Laravel의 Vite 통합 기능은 테스트 실행 시에도 에셋을 자동으로 처리하려고 시도합니다. 이 때에는 Vite 개발 서버를 실행 중이거나 미리 에셋 빌드가 필요합니다.

<!-- If you would prefer to mock Vite during testing, you may call the `withoutVite` method, which is is available for any tests that extend Laravel's `TestCase` class: -->
테스트 중에 Vite를 모킹(mock)하고 싶다면, `TestCase` 클래스를 확장한 모든 테스트에서 사용할 수 있는 `withoutVite` 메서드를 호출하면 됩니다.

```php
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_without_vite_example()
    {
        $this->withoutVite();

        // ...
    }
}
```

<!-- If you would like to disable Vite for all tests, you may call the `withoutVite` method from the `setUp` method on your base `TestCase` class: -->
모든 테스트에서 기본적으로 Vite를 비활성화하는 것이 필요하다면, 베이스 `TestCase` 클래스의 `setUp` 메서드에서 `withoutVite` 메서드를 호출하세요.

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
Laravel Vite 플러그인을 이용하면 서버 사이드 렌더링(SSR)도 간단하게 구축할 수 있습니다. 먼저 `resources/js/ssr.js` 경로에 SSR 엔트리 포인트 파일을 생성하고, Laravel 플러그인에 해당
경로를 옵션으로 지정합니다.

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
SSR 엔트리 포인트 빌드를 잊지 않도록, 애플리케이션의 `package.json` 내 "build" 스크립트를 아래와 같이 보강할 것을 권장합니다.

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

<!-- Then, to build and start the SSR server, you may run the following commands: -->
이제 SSR 서버를 빌드하고 시작하려면 아래 명령어를 실행합니다.

```sh
npm run build
node bootstrap/ssr/ssr.mjs
```

> [!NOTE]
> Laravel [starter kits](/docs/9.x/starter-kits)에는 이미 Inertia SSR 및 Vite의 적절한 설정이 포함되어
> 있습니다. [Laravel Breeze](/docs/9.x/starter-kits#breeze-and-inertia)로 시작하면, Inertia SSR 및 Vite 환경을 바로 구축할 수 있습니다.

<a name="script-and-style-attributes"></a>

<!-- ## Script & Style Tag Attributes -->
## Script & Style Tag Attributes

<a name="content-security-policy-csp-nonce"></a>

<!-- ### Content Security Policy (CSP) Nonce -->
### Content Security Policy (CSP) Nonce

<!-- If you wish to include a [`nonce` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) on your script and style tags as part of your [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP), you may generate or specify a nonce using the `useCspNonce` method within a custom [middleware](/docs/9.x/middleware): -->
[`nonce` attribute](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일환으로, 스크립트 및 스타일 태그에 [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 포함하고 싶다면,
커스텀 [middleware](/docs/9.x/middleware)에서 `useCspNonce` 메서드를 호출해 nonce를 생성하거나 지정할 수 있습니다.

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\Vite;

class AddContentSecurityPolicyHeaders
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        Vite::useCspNonce();

        return $next($request)->withHeaders([
            'Content-Security-Policy' => "script-src 'nonce-".Vite::cspNonce()."'",
        ]);
    }
}
```

<!-- After invoking the `useCspNonce` method, Laravel will automatically include the `nonce` attributes on all generated script and style tags. -->
`useCspNonce` 메서드를 호출하면 Laravel은 생성하는 모든 스크립트 및 스타일 태그에 자동으로 `nonce` 속성을 추가해 줍니다.

<!-- If you need to specify the nonce elsewhere, including the [Ziggy `@route` directive](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) included with Laravel's [starter kits](/docs/9.x/starter-kits), you may retrieve it using the `cspNonce` method: -->
Laravel의 [Ziggy `@route` directive](/docs/9.x/starter-kits)에 포함된 Ziggy의 [starter kits](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) 등, 다른 곳에서도 nonce가
필요하다면 `cspNonce` 메서드로 값을 받아올 수 있습니다.

```blade
@routes(nonce: Vite::cspNonce())
```

<!-- If you already have a nonce that you would like to instruct Laravel to use, you may pass the nonce to the `useCspNonce` method: -->
이미 가지고 있는 nonce 값을 Laravel에 사용하도록 지정하려면, `useCspNonce`에 nonce 값을 인자로 전달하면 됩니다.

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>

<!-- ### Subresource Integrity (SRI) -->
### Subresource Integrity (SRI)

<!-- If your Vite manifest includes `integrity` hashes for your assets, Laravel will automatically add the `integrity` attribute on any script and style tags it generates in order to enforce [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity). By default, Vite does not include the `integrity` hash in its manifest, but you may enable it by installing the [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM plugin: -->
Vite 매니페스트에 에셋의 `integrity` 해시가 포함된 경우, Laravel은 자동으로 생성된 스크립트 및 스타일 태그에 `integrity` 속성을
추가하여 [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)을
보장합니다. 기본적으로 Vite는 매니페스트에 `integrity` 값을 포함하지 않지만, [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인을 설치하면 이를 활성화할 수 있습니다.

```shell
npm install --save-dev vite-plugin-manifest-sri
```

<!-- You may then enable this plugin in your `vite.config.js` file: -->
설치 후 `vite.config.js` 파일에 플러그인을 추가하면 됩니다.

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
필요하다면, 무결성 해시가 저장되는 매니페스트의 키 이름을 커스텀할 수도 있습니다.

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

<!-- If you would like to disable this auto-detection completely, you may pass `false` to the `useIntegrityKey` method: -->
이 기능의 자동 감지를 완전히 비활성화하려면, `useIntegrityKey`에 `false`를 전달하면 됩니다.

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>

<!-- ### Arbitrary Attributes -->
### Arbitrary Attributes

<!-- If you need to include additional attributes on your script and style tags, such as the [`data-turbo-track`](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) attribute, you may specify them via the `useScriptTagAttributes` and `useStyleTagAttributes` methods. Typically, this methods should be invoked from a [service provider](/docs/9.x/providers): -->
스크립트 혹은 스타일 태그에 [`data-turbo-track`](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 등과 같은 추가
속성이 필요하다면, `useScriptTagAttributes`와 `useStyleTagAttributes` 메서드를 사용해 지정할 수 있습니다. 일반적으로 이
메서드는 [service provider](/docs/9.x/providers)에서 호출합니다.

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
속성을 조건부로 추가해야 한다면, 에셋의 소스 경로, URL, 매니페스트 청크, 전체 매니페스트를 인자로 받는 콜백을 전달할 수 있습니다.

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
> Vite 개발 서버가 실행 중일 때는 `$chunk`와 `$manifest` 인자가 `null`이 됩니다.

<a name="advanced-customization"></a>

<!-- ## Advanced Customization -->
## Advanced Customization

<!-- Out of the box, Laravel's Vite plugin uses sensible conventions that should work for the majority of applications; however, sometimes you may need to customize Vite's behavior. To enable additional customization options, we offer the following methods and options which can be used in place of the `@vite` Blade directive: -->
기본적으로 Laravel의 Vite 플러그인은 대부분의 애플리케이션에서 바로 사용할 수 있도록 합리적인 설정을 제공합니다. 하지만 특별히 Vite의 동작 방식을 수정하고 싶을 때는, `@vite` Blade 디렉티브 대신
아래와 같이 여러 메서드와 옵션을 조합해 사용할 수 있습니다.

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // Customize the "hot" file...
            ->useBuildDirectory('bundle') // Customize the build directory...
            ->useManifestFilename('assets.json') // Customize the manifest filename...
            ->withEntryPoints(['resources/js/app.js']) // Specify the entry points...
    }}
</head>
```

<!-- Within the `vite.config.js` file, you should then specify the same configuration: -->
동일한 설정을 `vite.config.js` 파일에도 맞춰 작성해야 합니다.

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
Vite 생태계의 일부 플러그인은 /로 시작하는 URL이 항상 Vite 개발 서버를 가리킨다고 가정합니다. 하지만 Laravel과 통합된 경우에는 항상 그렇지 않을 수 있습니다.

<!-- For example, the `vite-imagetools` plugin outputs URLs like the following while Vite is serving your assets: -->
예를 들어, `vite-imagetools` 플러그인은 아래와 같이 개발 서버에서 에셋을 제공할 때 다음과 같은 URL을 출력합니다.

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

<!-- The `vite-imagetools` plugin is expecting that the output URL will be intercepted by Vite and the plugin may then handle all URLs that start with `/@imagetools`. If you are using plugins that are expecting this behaviour, you will need to manually correct the URLs. You can do this in your `vite.config.js` file by using the `transformOnServe` option. -->
`vite-imagetools` 플러그인은 `/@imagetools`로 시작하는 URL을 Vite가 가로채서 해당 플러그인이 처리하기를 기대합니다. 이런 동작을 원하는 플러그인을 사용할 때는 URL을 수동으로 교정해야 할 수 있습니다. 이 때는
`vite.config.js`의 `transformOnServe` 옵션을 활용하면 됩니다.

<!-- In this particular example, we will append the dev server URL to all occurrences of `/@imagetools` within the generated code: -->
아래 예시에서는, 생성된 코드 내 모든 `/@imagetools` 경로에 개발 서버 URL을 자동으로 앞에 붙여줍니다.

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
이제 Vite가 에셋을 서빙할 때, 생성된 URL이 아래와 같이 개발 서버 주소를 포함하게 됩니다.

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```
