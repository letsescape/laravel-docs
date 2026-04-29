# 애셋 번들링 (Vite) (Asset Bundling (Vite))

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치](#installing-node)
  - [Vite와 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
  - [Vite 설정](#configuring-vite)
  - [스크립트와 스타일 불러오기](#loading-your-scripts-and-styles)
- [Vite 실행](#running-vite)
- [JavaScript 다루기](#working-with-scripts)
  - [별칭](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Svelte](#svelte)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 다루기](#working-with-stylesheets)
- [Blade와 라우트 다루기](#working-with-blade-and-routes)
  - [Vite로 정적 애셋 처리하기](#blade-processing-static-assets)
  - [저장 시 새로고침](#blade-refreshing-on-save)
  - [별칭](#blade-aliases)
- [애셋 미리 가져오기](#asset-prefetching)
- [사용자 정의 Base URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트에서 Vite 비활성화하기](#disabling-vite-in-tests)
- [서버 사이드 렌더링 (SSR)](#ssr)
- [스크립트와 스타일 태그 속성](#script-and-style-attributes)
  - [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)
  - [Subresource Integrity (SRI)](#subresource-integrity-sri)
  - [임의 속성](#arbitrary-attributes)
- [고급 사용자 정의](#advanced-customization)
  - [개발 서버 Cross-Origin Resource Sharing (CORS)](#cors)
  - [개발 서버 URL 수정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개 (Introduction)

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고, 프로덕션을 위해 코드를 번들링해 주는 최신 frontend 빌드 도구입니다. Laravel로 애플리케이션을 만들 때는 일반적으로 Vite를 사용하여 애플리케이션의 CSS와 JavaScript 파일을 프로덕션에 바로 사용할 수 있는 애셋으로 번들링합니다.

Laravel은 공식 플러그인과 Blade 디렉티브를 제공하여 Vite와 매끄럽게 통합되며, 개발 및 프로덕션 환경에서 애셋을 불러올 수 있게 해 줍니다.

<a name="installation"></a>
## 설치 및 설정 (Installation & Setup)

> [!NOTE]
> 다음 문서는 Laravel Vite 플러그인을 수동으로 설치하고 설정하는 방법을 설명합니다. 하지만 Laravel의 [starter kits](/docs/13.x/starter-kits)에는 이미 이 스캐폴딩이 모두 포함되어 있으며, Laravel과 Vite를 가장 빠르게 시작하는 방법입니다.

<a name="installing-node"></a>
### Node 설치

Vite와 Laravel 플러그인을 실행하기 전에 Node.js (16+)와 NPM이 설치되어 있는지 확인해야 합니다.

```shell
node -v
npm -v
```

[공식 Node 웹사이트](https://nodejs.org/en/download/)에서 제공하는 간단한 그래픽 설치 프로그램을 사용하면 최신 버전의 Node와 NPM을 쉽게 설치할 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/13.x/sail)을 사용 중이라면 Sail을 통해 Node와 NPM을 실행할 수 있습니다.

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite와 Laravel 플러그인 설치

새 Laravel 설치본에서는 애플리케이션 디렉터리 구조의 루트에 `package.json` 파일이 있습니다. 기본 `package.json` 파일에는 Vite와 Laravel 플러그인을 사용하기 위해 필요한 모든 것이 이미 포함되어 있습니다. NPM을 통해 애플리케이션의 frontend 의존성을 설치할 수 있습니다.

```shell
npm install
```

<a name="configuring-vite"></a>
### Vite 설정

Vite는 프로젝트 루트의 `vite.config.js` 파일을 통해 설정합니다. 필요에 따라 이 파일을 자유롭게 사용자 정의할 수 있으며, `@vitejs/plugin-react`, `@sveltejs/vite-plugin-svelte`, `@vitejs/plugin-vue`처럼 애플리케이션에 필요한 다른 플러그인도 설치할 수 있습니다.

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

대신 JavaScript를 통해 CSS를 import해야 합니다. 일반적으로 애플리케이션의 `resources/js/app.js` 파일에서 이 작업을 수행합니다.

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 여러 엔트리 포인트와 [SSR entry points](#ssr) 같은 고급 설정 옵션도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안 개발 서버 다루기

로컬 개발 웹 서버가 HTTPS를 통해 애플리케이션을 제공하는 경우, Vite 개발 서버에 연결할 때 문제가 발생할 수 있습니다.

[Laravel Herd](https://herd.laravel.com)를 사용하면서 사이트를 보안 처리했거나, [Laravel Valet](/docs/13.x/valet)을 사용하면서 애플리케이션에 대해 [secure command](/docs/13.x/valet#securing-sites)를 실행했다면, Laravel Vite 플러그인이 생성된 TLS 인증서를 자동으로 감지하여 사용합니다.

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

시스템에서 신뢰할 수 있는 인증서를 생성할 수 없다면 [@vitejs/plugin-basic-ssl plugin](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치하고 설정할 수 있습니다. 신뢰할 수 없는 인증서를 사용하는 경우, `npm run dev` 명령어를 실행할 때 콘솔에 표시되는 "Local" 링크를 따라 브라우저에서 Vite 개발 서버의 인증서 경고를 허용해야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2의 Sail에서 개발 서버 실행하기

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

개발 서버가 실행 중인데도 파일 변경 사항이 브라우저에 반영되지 않는다면, Vite의 [server.watch.usePolling option](https://vitejs.dev/config/server-options.html#server-watch)도 설정해야 할 수 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트와 스타일 불러오기

Vite 엔트리 포인트를 설정했다면, 이제 애플리케이션의 루트 템플릿 `<head>`에 추가하는 `@vite()` Blade 디렉티브에서 해당 엔트리 포인트를 참조할 수 있습니다.

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

JavaScript를 통해 CSS를 import하고 있다면 JavaScript 엔트리 포인트만 포함하면 됩니다.

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 디렉티브는 Vite 개발 서버를 자동으로 감지하고, Hot Module Replacement를 활성화하기 위해 Vite 클라이언트를 주입합니다. 빌드 모드에서는 import된 CSS를 포함하여 컴파일되고 버전이 부여된 애셋을 불러옵니다.

필요한 경우 `@vite` 디렉티브를 호출할 때 컴파일된 애셋의 빌드 경로도 지정할 수 있습니다.

```blade
<!doctype html>
<head>
    {{-- Given build path is relative to public path. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### 인라인 애셋

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
## Vite 실행 (Running Vite)

Vite를 실행하는 방법은 두 가지입니다. 로컬에서 개발하는 동안 유용한 `dev` 명령어로 개발 서버를 실행할 수 있습니다. 개발 서버는 파일 변경 사항을 자동으로 감지하고, 열려 있는 브라우저 창에 즉시 반영합니다.

또는 `build` 명령어를 실행하면 애플리케이션의 애셋에 버전을 부여하고 번들링하여 프로덕션에 배포할 준비를 합니다.

```shell
# Run the Vite development server...
npm run dev

# Build and version the assets for production...
npm run build
```

WSL2의 [Sail](/docs/13.x/sail)에서 개발 서버를 실행 중이라면 몇 가지 [추가 설정](#configuring-hmr-in-sail-on-wsl2) 옵션이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## JavaScript 다루기 (Working With JavaScript)

<a name="aliases"></a>
### 별칭

기본적으로 Laravel 플러그인은 빠르게 시작하고 애플리케이션의 애셋을 편리하게 import할 수 있도록 일반적인 별칭을 제공합니다.

```js
{
    '@' => '/resources/js'
}
```

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
### Vue

[Vue](https://vuejs.org/) 프레임워크를 사용하여 frontend를 만들고 싶다면 `@vitejs/plugin-vue` 플러그인도 설치해야 합니다.

```shell
npm install --save-dev @vitejs/plugin-vue
```

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
### React

[React](https://reactjs.org/) 프레임워크를 사용하여 frontend를 만들고 싶다면 `@vitejs/plugin-react` 플러그인도 설치해야 합니다.

```shell
npm install --save-dev @vitejs/plugin-react
```

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

JSX를 포함하는 모든 파일의 확장자가 `.jsx` 또는 `.tsx`인지 확인해야 하며, 필요한 경우 [위에서 설명한 것처럼](#configuring-vite) 엔트리 포인트도 업데이트해야 합니다.

기존 `@vite` 디렉티브와 함께 추가 `@viteReactRefresh` Blade 디렉티브도 포함해야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh` 디렉티브는 `@vite` 디렉티브보다 먼저 호출해야 합니다.

> [!NOTE]
> Laravel의 [starter kits](/docs/13.x/starter-kits)에는 이미 적절한 Laravel, React, Vite 설정이 포함되어 있습니다. 이러한 starter kits는 Laravel, React, Vite를 가장 빠르게 시작하는 방법을 제공합니다.

<a name="svelte"></a>
### Svelte

[Svelte](https://svelte.dev/) 프레임워크를 사용하여 frontend를 만들고 싶다면 `@sveltejs/vite-plugin-svelte` 플러그인도 설치해야 합니다.

```shell
npm install --save-dev @sveltejs/vite-plugin-svelte
```

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
> Laravel의 [스타터 키트](/docs/13.x/starter-kits)에는 이미 적절한 Laravel, Svelte, Vite 설정이 포함되어 있습니다. 이 스타터 키트는 Laravel, Svelte, Vite를 가장 빠르게 시작할 수 있는 방법을 제공합니다.

<a name="inertia"></a>
### Inertia

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

Inertia와 함께 Vite의 코드 분할 기능을 사용한다면 [애셋 프리페칭](#asset-prefetching)을 설정하는 것을 권장합니다.

> [!NOTE]
> Laravel의 [스타터 키트](/docs/13.x/starter-kits)에는 이미 적절한 Laravel, Inertia, Vite 설정이 포함되어 있습니다. 이 스타터 키트는 Laravel, Inertia, Vite를 가장 빠르게 시작할 수 있는 방법을 제공합니다.

<a name="url-processing"></a>
### URL 처리

Vite를 사용하면서 애플리케이션의 HTML, CSS, JS에서 애셋을 참조할 때는 몇 가지 주의할 점이 있습니다. 먼저, 절대 경로로 애셋을 참조하면 Vite는 해당 애셋을 빌드에 포함하지 않습니다. 따라서 해당 애셋이 public 디렉터리에 있어야 합니다. [전용 CSS 엔트리포인트](#configuring-vite)를 사용할 때는 절대 경로 사용을 피해야 합니다. 개발 중에는 브라우저가 public 디렉터리가 아니라 CSS가 호스팅되는 Vite 개발 서버에서 해당 경로를 불러오려고 하기 때문입니다.

상대 애셋 경로를 참조할 때는 해당 경로가 참조된 파일을 기준으로 한다는 점을 기억해야 합니다. 상대 경로로 참조된 모든 애셋은 Vite에 의해 다시 작성되고, 버전이 부여되며, 번들에 포함됩니다.

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

다음 예시는 Vite가 상대 URL과 절대 URL을 어떻게 처리하는지 보여줍니다.

```html
<!-- This asset is not handled by Vite and will not be included in the build -->
<img src="/taylor.png">

<!-- This asset will be re-written, versioned, and bundled by Vite -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
## 스타일시트 작업 (Working With Stylesheets)

> [!NOTE]
> Laravel의 [스타터 키트](/docs/13.x/starter-kits)에는 이미 적절한 Tailwind와 Vite 설정이 포함되어 있습니다. 또는 스타터 키트를 사용하지 않고 Tailwind와 Laravel을 함께 사용하고 싶다면 [Laravel용 Tailwind 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 확인하세요.

모든 Laravel 애플리케이션에는 이미 Tailwind와 올바르게 설정된 `vite.config.js` 파일이 포함되어 있습니다. 따라서 Vite 개발 서버를 시작하거나 `dev` Composer 명령어를 실행하기만 하면 됩니다. 이 명령어는 Laravel과 Vite 개발 서버를 모두 시작합니다.

```shell
composer run dev
```

애플리케이션의 CSS는 `resources/css/app.css` 파일에 배치할 수 있습니다.

<a name="working-with-blade-and-routes"></a>
## Blade와 라우트 작업 (Working With Blade and Routes)

<a name="blade-processing-static-assets"></a>
### Vite로 정적 애셋 처리하기

JavaScript나 CSS에서 애셋을 참조하면 Vite는 이를 자동으로 처리하고 버전을 부여합니다. 또한 Blade 기반 애플리케이션을 빌드할 때, Vite는 Blade 템플릿에서만 참조하는 정적 애셋도 처리하고 버전을 부여할 수 있습니다.

하지만 이를 수행하려면 플러그인의 `assets` 옵션에 애셋을 지정하여 Vite가 해당 애셋을 알 수 있도록 해야 합니다. 예를 들어 `resources/images`에 저장된 모든 이미지와 `resources/fonts`에 저장된 모든 폰트를 처리하고 버전을 부여하려면 Vite 설정에 다음을 추가해야 합니다.

```js
laravel({
    input: 'resources/js/app.js',
    assets: ['resources/images/**', 'resources/fonts/**'],
})
```

이제 `npm run build`를 실행하면 해당 애셋들이 Vite에 의해 처리됩니다. 그런 다음 Blade 템플릿에서 `Vite::asset` 메서드를 사용해 이 애셋들을 참조할 수 있으며, 이 메서드는 지정한 애셋의 버전이 적용된 URL을 반환합니다.

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

> [!NOTE]
> Laravel Vite 플러그인 3버전 이전에는 정적 애셋을 `import.meta.glob`을 사용해 애플리케이션의 엔트리포인트에서 가져와야 했습니다. `assets` 옵션은 Vite 8의 변경 사항 때문에 도입되었습니다.

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침

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

`refresh` 옵션이 `true`이면 `npm run dev`를 실행하는 동안 다음 디렉터리의 파일을 저장할 때 브라우저가 전체 페이지 새로고침을 수행합니다.

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

애플리케이션 프런트엔드에서 라우트 링크를 생성하기 위해 [Ziggy](https://github.com/tighten/ziggy)를 사용한다면 `routes/**` 디렉터리를 감시하는 것이 유용합니다.

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
### 별칭

JavaScript 애플리케이션에서는 자주 참조하는 디렉터리에 [별칭을 생성](#aliases)하는 것이 일반적입니다. 하지만 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 사용하여 Blade에서 사용할 별칭도 만들 수 있습니다. 일반적으로 “macro”는 [서비스 프로바이더](/docs/13.x/providers)의 `boot` 메서드 안에서 정의해야 합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

macro가 정의되면 템플릿 안에서 호출할 수 있습니다. 예를 들어 위에서 정의한 `image` macro를 사용해 `resources/images/logo.png`에 있는 애셋을 참조할 수 있습니다.

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="asset-prefetching"></a>
## 애셋 프리페칭 (Asset Prefetching)

Vite의 코드 분할 기능을 사용해 SPA를 빌드하면, 각 페이지 이동 시 필요한 애셋을 가져옵니다. 이 동작은 UI 렌더링 지연으로 이어질 수 있습니다. 사용 중인 프런트엔드 프레임워크에서 이것이 문제가 된다면, Laravel은 초기 페이지 로드 시 애플리케이션의 JavaScript와 CSS 애셋을 미리 적극적으로 가져올 수 있는 기능을 제공합니다.

[서비스 프로바이더](/docs/13.x/providers)의 `boot` 메서드에서 `Vite::prefetch` 메서드를 호출하여 Laravel이 애셋을 미리 가져오도록 지시할 수 있습니다.

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

기본적으로 프리페칭은 [페이지 _load_ 이벤트](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event)가 발생할 때 시작됩니다. 프리페칭이 시작되는 시점을 사용자 정의하고 싶다면 Vite가 수신할 이벤트를 지정할 수 있습니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

위 코드에 따르면 이제 `window` 객체에서 `vite:prefetch` 이벤트를 직접 발생시킬 때 프리페칭이 시작됩니다. 예를 들어 페이지가 로드된 후 3초 뒤에 프리페칭을 시작하도록 할 수 있습니다.

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
## 사용자 정의 기본 URL (Custom Base URLs)

Vite로 컴파일된 애셋을 CDN처럼 애플리케이션과 다른 도메인에 배포하는 경우, 애플리케이션의 `.env` 파일에 `ASSET_URL` 환경 변수를 지정해야 합니다.

```env
ASSET_URL=https://cdn.example.com
```

애셋 URL을 설정한 후에는 다시 작성된 모든 애셋 URL 앞에 설정한 값이 붙습니다.

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

[절대 URL은 Vite에 의해 다시 작성되지 않는다](#url-processing)는 점을 기억하세요. 따라서 절대 URL에는 이 값이 접두사로 붙지 않습니다.

<a name="environment-variables"></a>
## 환경 변수 (Environment Variables)

애플리케이션의 `.env` 파일에서 환경 변수 이름 앞에 `VITE_`를 붙이면 해당 환경 변수를 JavaScript에 주입할 수 있습니다.

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

주입된 환경 변수는 `import.meta.env` 객체를 통해 접근할 수 있습니다.

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트에서 Vite 비활성화하기 (Disabling Vite in Tests)

Laravel의 Vite 통합은 테스트를 실행하는 동안 애셋을 확인하려고 시도합니다. 따라서 Vite 개발 서버를 실행하거나 애셋을 빌드해야 합니다.

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
## 서버 사이드 렌더링 (SSR) (Server-Side Rendering (SSR))

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

SSR 엔트리포인트를 다시 빌드하는 것을 잊지 않도록, 애플리케이션의 `package.json`에 있는 `"build"` 스크립트를 확장하여 SSR 빌드를 생성하는 것을 권장합니다.

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

그런 다음 SSR 서버를 빌드하고 시작하려면 다음 명령어를 실행하면 됩니다.

```shell
npm run build
node bootstrap/ssr/ssr.js
```

[Inertia와 함께 SSR](https://inertiajs.com/server-side-rendering)을 사용하는 경우, 대신 `inertia:start-ssr` Artisan 명령어를 사용하여 SSR 서버를 시작할 수 있습니다.

```shell
php artisan inertia:start-ssr
```

> [!NOTE]
> Laravel의 [스타터 키트](/docs/13.x/starter-kits)에는 이미 적절한 Laravel, Inertia SSR, Vite 설정이 포함되어 있습니다. 이 스타터 키트는 Laravel, Inertia SSR, Vite를 가장 빠르게 시작할 수 있는 방법을 제공합니다.

<a name="script-and-style-attributes"></a>
## Script 및 Style 태그 속성 (Script and Style Tag Attributes)

<a name="content-security-policy-csp-nonce"></a>
### 콘텐츠 보안 정책(CSP) Nonce

[Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일부로 script 및 style 태그에 [nonce 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 포함하고 싶다면, 사용자 정의 [middleware](/docs/13.x/middleware) 안에서 `useCspNonce` 메서드를 사용하여 nonce를 생성하거나 지정할 수 있습니다.

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
`useCspNonce` 메서드를 호출하면 Laravel은 생성하는 모든 script 및 style 태그에 `nonce` 속성을 자동으로 포함합니다.

다른 위치에서 nonce를 지정해야 하는 경우, 예를 들어 Laravel의 [스타터 키트](/docs/13.x/starter-kits)에 포함된 [Ziggy `@route` 디렉티브](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy)에서 사용해야 한다면, `cspNonce` 메서드로 값을 가져올 수 있습니다.

```blade
@routes(nonce: Vite::cspNonce())
```

이미 사용하려는 nonce가 있고 Laravel이 해당 값을 사용하도록 지정하려면, `useCspNonce` 메서드에 nonce를 전달하면 됩니다.

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### 서브리소스 무결성(SRI)

Vite 매니페스트에 에셋의 `integrity` 해시가 포함되어 있으면, Laravel은 [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)를 적용하기 위해 생성하는 모든 script 및 style 태그에 `integrity` 속성을 자동으로 추가합니다. 기본적으로 Vite는 매니페스트에 `integrity` 해시를 포함하지 않지만, [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인을 설치하여 활성화할 수 있습니다.

```shell
npm install --save-dev vite-plugin-manifest-sri
```

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

필요하다면 무결성 해시를 찾을 매니페스트 키도 직접 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

이 자동 감지를 완전히 비활성화하려면 `useIntegrityKey` 메서드에 `false`를 전달하면 됩니다.

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의 속성

script 및 style 태그에 [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 속성과 같은 추가 속성을 포함해야 한다면, `useScriptTagAttributes` 및 `useStyleTagAttributes` 메서드를 통해 지정할 수 있습니다. 일반적으로 이 메서드들은 [서비스 프로바이더](/docs/13.x/providers)에서 호출해야 합니다.

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
## 고급 커스터마이징 (Advanced Customization)

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
### 개발 서버 교차 출처 리소스 공유(CORS)

Vite 개발 서버에서 에셋을 가져오는 동안 브라우저에서 Cross-Origin Resource Sharing(CORS) 문제가 발생한다면, 사용자 지정 origin이 개발 서버에 접근할 수 있도록 허용해야 할 수 있습니다. Vite와 Laravel 플러그인을 함께 사용하면 추가 설정 없이 다음 origin이 허용됩니다.

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- 프로젝트의 `.env`에 있는 `APP_URL`

프로젝트에서 사용자 지정 origin을 허용하는 가장 쉬운 방법은 애플리케이션의 `APP_URL` 환경 변수가 브라우저에서 방문 중인 origin과 일치하도록 하는 것입니다. 예를 들어 `https://my-app.laravel`에 방문 중이라면, `.env`를 다음과 같이 맞춰 업데이트해야 합니다.

```env
APP_URL=https://my-app.laravel
```

여러 origin을 지원하는 등 origin을 더 세밀하게 제어해야 한다면, [Vite의 포괄적이고 유연한 내장 CORS 서버 설정](https://vite.dev/config/server-options.html#server-cors)을 사용해야 합니다. 예를 들어 프로젝트의 `vite.config.js` 파일에서 `server.cors.origin` 설정 옵션에 여러 origin을 지정할 수 있습니다.

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
### 개발 서버 URL 보정

Vite 생태계의 일부 플러그인은 슬래시로 시작하는 URL이 항상 Vite 개발 서버를 가리킨다고 가정합니다. 그러나 Laravel 통합 방식의 특성상 실제로는 그렇지 않습니다.

예를 들어 Vite가 에셋을 제공하는 동안 `vite-imagetools` 플러그인은 다음과 같은 URL을 출력합니다.

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

`vite-imagetools` 플러그인은 출력된 URL이 Vite에 의해 가로채지고, 그다음 플러그인이 `/@imagetools`로 시작하는 모든 URL을 처리할 수 있을 것이라고 기대합니다. 이러한 동작을 기대하는 플러그인을 사용한다면 URL을 수동으로 보정해야 합니다. `vite.config.js` 파일에서 `transformOnServe` 옵션을 사용하면 됩니다.

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

이제 Vite가 Assets를 제공하는 동안 Vite 개발 서버를 가리키는 URL을 출력합니다.

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```
