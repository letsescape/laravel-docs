# 에셋 번들링 (Vite) (Asset Bundling (Vite))

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치](#installing-node)
  - [Vite 및 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
  - [Vite 구성](#configuring-vite)
  - [스크립트 및 스타일 로딩](#loading-your-scripts-and-styles)
- [Vite 실행](#running-vite)
- [자바스크립트 작업](#working-with-scripts)
  - [별칭](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Svelte](#svelte)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 작업](#working-with-stylesheets)
- [Blade 및 라우트 작업](#working-with-blade-and-routes)
  - [Vite로 정적 에셋 처리](#blade-processing-static-assets)
  - [저장 시 새로고침](#blade-refreshing-on-save)
  - [별칭](#blade-aliases)
- [에셋 프리페치(prefetching)](#asset-prefetching)
- [커스텀 베이스 URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트에서 Vite 비활성화](#disabling-vite-in-tests)
- [서버 사이드 렌더링(SSR)](#ssr)
- [스크립트 및 스타일 태그 속성](#script-and-style-attributes)
  - [컨텐츠 보안 정책(CSP) nonce](#content-security-policy-csp-nonce)
  - [서브리소스 무결성(SRI)](#subresource-integrity-sri)
  - [임의 속성 지정](#arbitrary-attributes)
- [고급 커스터마이징](#advanced-customization)
  - [개발 서버 CORS](#cors)
  - [개발 서버 URL 수정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개 (Introduction)

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고 프로덕션 배포용 코드 번들링도 지원하는 최신 프론트엔드 빌드 도구입니다. Laravel로 애플리케이션을 개발할 때는 일반적으로 Vite를 사용해 애플리케이션의 CSS와 자바스크립트 파일을 프로덕션 환경에 적합한 에셋으로 번들링하게 됩니다.

Laravel은 공식 플러그인과 Blade 디렉티브를 통해 Vite와 자연스럽게 통합되며, 개발 및 배포 환경 모두에서 에셋을 손쉽게 로드할 수 있습니다.

<a name="installation"></a>
## 설치 및 설정 (Installation & Setup)

> [!NOTE]
> 아래 문서는 Laravel Vite 플러그인을 수동으로 설치하고 구성하는 방법에 대해 설명합니다. 하지만 Laravel의 [스타터 킷](/docs/12.x/starter-kits)에는 이미 모든 환경이 구성되어 있어, Laravel과 Vite를 가장 빠르게 시작하는 방법입니다.

<a name="installing-node"></a>
### Node 설치

Vite와 Laravel 플러그인을 사용하려면 반드시 Node.js(16 이상)와 NPM이 설치되어 있어야 합니다.

```shell
node -v
npm -v
```

최신 버전의 Node와 NPM은 [공식 Node 웹사이트](https://nodejs.org/en/download/)에서 제공하는 그래픽 설치 프로그램으로 쉽게 설치할 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/12.x/sail)을 사용하는 경우 Sail을 통해 Node와 NPM을 실행할 수 있습니다.

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite 및 Laravel 플러그인 설치

새로운 Laravel 프로젝트에는 애플리케이션 폴더 구조의 루트에 이미 `package.json` 파일이 생성되어 있습니다. 기본 `package.json` 파일은 Vite와 Laravel 플러그인 사용을 위한 모든 필수 항목이 포함되어 있습니다. NPM을 통해 프론트엔드 의존성을 설치하세요.

```shell
npm install
```

<a name="configuring-vite"></a>
### Vite 구성

Vite는 프로젝트 루트의 `vite.config.js` 파일을 통해 구성합니다. 이 파일은 필요에 따라 자유롭게 수정할 수 있으며, 필요에 따라 `@vitejs/plugin-react`, `@sveltejs/vite-plugin-svelte`, `@vitejs/plugin-vue` 등 다른 플러그인도 추가 설치할 수 있습니다.

Laravel Vite 플러그인은 애플리케이션의 진입점(entry point) 파일을 반드시 지정해야 합니다. 이 진입점은 JavaScript 또는 CSS 파일이며, TypeScript, JSX, TSX, Sass 등 전처리 언어 역시 사용할 수 있습니다.

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

만약 SPA(Single Page Application) 또는 Inertia를 사용하는 경우라면, Vite는 CSS 진입점 없이 동작하는 것이 가장 좋습니다.

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

이런 경우에는 CSS를 자바스크립트 파일에서 import 하는 방식으로 작성해 주세요. 일반적으로는 `resources/js/app.js` 파일에서 아래와 같이 import합니다.

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 다중 진입점 및 [SSR 진입점](#ssr)과 같은 고급 구성 옵션도 지원합니다.

#### 보안 개발 서버 사용

로컬 개발 웹 서버가 HTTPS로 애플리케이션을 서비스하는 경우, Vite 개발 서버 연결에 문제가 발생할 수도 있습니다.

[Laravel Herd](https://herd.laravel.com)에서 사이트를 보안 설정하거나, [Laravel Valet](/docs/12.x/valet)에서 [secure 명령어](/docs/12.x/valet#securing-sites)를 사용하고 있다면, Laravel Vite 플러그인이 자동으로 생성된 TLS 인증서를 감지해 설정합니다.

만약 사이트를 인증했는데, 인증서의 호스트가 애플리케이션 디렉터리 이름과 다르다면, 애플리케이션의 `vite.config.js` 파일에서 호스트를 직접 지정할 수 있습니다.

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

다른 웹 서버를 사용할 경우, 신뢰할 수 있는 인증서를 직접 생성하고, Vite에 수동으로 인증서를 지정해야 합니다.

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

시스템에서 신뢰된 인증서를 생성할 수 없는 경우, [@vitejs/plugin-basic-ssl 플러그인](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치해 설정할 수 있습니다. 신뢰되지 않은 인증서를 사용하는 경우, 브라우저에서 Vite 개발 서버에 접근할 때 인증서 경고를 수락해야 하며, `npm run dev` 명령어 실행 후 콘솔에 표시되는 "Local" 링크를 따라가 인증서를 수락할 수 있습니다.

#### WSL2 환경의 Sail에서 개발 서버 실행

[Laravel Sail](/docs/12.x/sail)을 Windows Subsystem for Linux 2(WSL2)에서 사용 중이라면, 브라우저가 개발 서버와 통신할 수 있도록 `vite.config.js`에 다음 설정을 추가해야 합니다.

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

개발 서버가 실행 중인데 파일 변경 사항이 브라우저에 반영되지 않는 경우에는 Vite의 [server.watch.usePolling 옵션](https://vitejs.dev/config/server-options.html#server-watch)도 추가로 설정해야 할 수 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트 및 스타일 로딩

Vite 진입점이 구성되었다면, 이 파일들은 애플리케이션의 루트 템플릿 `<head>` 영역에 `@vite()` Blade 디렉티브로 불러올 수 있습니다.

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

자바스크립트에서 CSS를 import하고 있다면, 자바스크립트 진입점만 포함하면 됩니다.

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 디렉티브는 Vite 개발 서버를 자동으로 감지해 Vite 클라이언트를 주입하며, Hot Module Replacement 기능을 사용할 수 있게 해줍니다. 빌드 모드일 때는 컴파일되고 버전이 부여된 에셋을 로드하며, import된 CSS도 포함됩니다.

필요할 경우, `@vite` 디렉티브에서 빌드 경로를 지정하여 컴파일된 에셋의 경로를 지정할 수 있습니다.

```blade
<!doctype html>
<head>
    {{-- 주어진 빌드 경로는 public 경로 기준 상대 경로입니다. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

#### 인라인 에셋

경우에 따라 에셋의 URL 링크 대신, 에셋의 원본 내용을 직접 포함해야 할 때가 있습니다. 예를 들어, HTML 콘텐츠를 PDF 생성기에 전달할 때 에셋 내용을 직접 페이지에 삽입해야 할 수 있습니다. 이때는 `Vite` 파사드에서 제공하는 `content` 메서드를 사용할 수 있습니다.

```blade
@use('Illuminate\Support\Facades\Vite')

<!doctype html>
<head>
    {{-- ... --}}

    
    <script>
        {!! Vite::content('resources/js/app.js') !!}
    </script>
</head>
```

<a name="running-vite"></a>
## Vite 실행 (Running Vite)

Vite는 두 가지 방법으로 실행할 수 있습니다. 첫째, 개발 작업을 할 때는 `dev` 명령어로 개발 서버를 실행하세요. 이 서버는 파일 변경을 자동으로 감지해 브라우저에 즉시 반영합니다.

둘째, `build` 명령어를 이용해 애플리케이션 에셋을 번들링 및 버전 관리하여 프로덕션 배포 파일로 만들 수 있습니다.

```shell
# Vite 개발 서버 실행
npm run dev

# 프로덕션 배포를 위한 에셋 빌드 및 버전 지정
npm run build
```

[WSL2 환경의 Sail](/docs/12.x/sail)에서 개발 서버를 실행한다면 [추가 설정](#configuring-hmr-in-sail-on-wsl2)이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## 자바스크립트 작업 (Working With JavaScript)

<a name="aliases"></a>
### 별칭 (Aliases)

기본적으로 Laravel 플러그인은 애플리케이션 에셋을 빠르게 import할 수 있도록 다음과 같은 일반적인 별칭을 제공합니다.

```js
{
    '@' => '/resources/js'
}
```

별칭 `'@'`을 원하는 대로 `vite.config.js`에서 직접 덮어쓸 수 있습니다.

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

[Vue](https://vuejs.org/) 프레임워크로 프론트엔드를 개발하려면, `@vitejs/plugin-vue` 플러그인도 별도로 설치해야 합니다.

```shell
npm install --save-dev @vitejs/plugin-vue
```

설치 후, 아래처럼 `vite.config.js`에 해당 플러그인을 추가하면 됩니다. Vue 플러그인을 Laravel과 함께 쓸 때는 몇 가지 추가 옵션을 지정해야 합니다.

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
                    // 싱글 파일 컴포넌트에서 참조하는 에셋 URL을
                    // Laravel 웹 서버가 아닌 Vite 서버로 재작성하도록 설정
                    base: null,

                    // 절대 URL은 public 디렉터리에 있는 에셋을 참조해야 할 때
                    // false로 둬야 경로가 수정되지 않음
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]
> Laravel의 [스타터 킷](/docs/12.x/starter-kits)은 Laravel, Vue, Vite 구성까지 모두 포함되어 있습니다. 이 스타터 킷을 활용하면 가장 빠르고 손쉽게 Laravel, Vue, Vite로 개발을 시작할 수 있습니다.

<a name="react"></a>
### React

[React](https://reactjs.org/) 프레임워크를 프론트엔드로 쓸 경우에는 `@vitejs/plugin-react` 플러그인을 설치해야 합니다.

```shell
npm install --save-dev @vitejs/plugin-react
```

설치 후 아래와 같이 `vite.config.js`에서 플러그인을 포함하세요.

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

JSX가 포함된 파일은 반드시 `.jsx` 또는 `.tsx` 확장자를 사용해야 하며, 진입점 파일도 위 예시처럼 변경해야 합니다. ([구성 방법 참고](#configuring-vite))

또한 기존 `@vite` 디렉티브와 함께 `@viteReactRefresh` Blade 디렉티브도 추가해야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh`는 반드시 `@vite`보다 먼저 호출되어야 합니다.

> [!NOTE]
> Laravel의 [스타터 킷](/docs/12.x/starter-kits)에는 Laravel, React, Vite 구성이 이미 포함되어 있어, 가장 빠르게 개발을 시작할 수 있습니다.

<a name="svelte"></a>
### Svelte

[Svelte](https://svelte.dev/) 프레임워크를 프론트엔드로 쓰려면 `@sveltejs/vite-plugin-svelte` 플러그인을 별도로 설치해야 합니다.

```shell
npm install --save-dev @sveltejs/vite-plugin-svelte
```

설치 후 아래와 같이 플러그인을 구성하세요.

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
> Laravel의 [스타터 킷](/docs/12.x/starter-kits)에는 Laravel, Svelte, Vite 구성이 모두 포함되어 있습니다.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트를 쉽게 resolve할 수 있는 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3에서 사용 예시이며, React, Svelte 등 다른 프레임워크에서도 사용할 수 있습니다.

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

Inertia에서 Vite의 코드 스플리팅 기능을 사용할 경우 [에셋 프리페치](#asset-prefetching)를 추가로 설정하는 것이 좋습니다.

> [!NOTE]
> Laravel의 [스타터 킷](/docs/12.x/starter-kits)에는 Laravel, Inertia, Vite 구성이 이미 포함되어 있습니다.

<a name="url-processing"></a>
### URL 처리 (URL Processing)

Vite를 사용할 때 애플리케이션의 HTML, CSS, JS에서 에셋을 참조할 때 몇 가지 주의사항이 있습니다. 먼저, 절대경로로 에셋을 참조하는 경우 Vite가 번들링 빌드에 포함하지 않으므로 반드시 public 디렉터리에 있어야 합니다. [별도 CSS 진입점](#configuring-vite)을 사용할 때도 절대 경로 사용을 피해야 하며, 개발 중에는 브라우저가 public 디렉터리가 아니라 Vite 개발 서버에서 해당 경로를 찾게 되기 때문입니다.

상대경로로 에셋을 참조할 경우, 해당 파일을 기준으로 경로가 평가됩니다. 상대경로로 참조된 에셋들은 Vite가 자동으로 재작성, 버전 부여(bundling)합니다.

프로젝트 구조 예시:

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

예시를 통해 Vite가 상대 URL과 절대 URL을 어떻게 처리하는지 확인할 수 있습니다.

```html
<!-- 이 에셋은 Vite가 처리하지 않아 빌드에 포함되지 않음 -->
<img src="/taylor.png" />

<!-- 이 에셋은 Vite가 재작성, 버전 부여 및 번들링함 -->
<img src="../../images/abigail.png" />
```

<a name="working-with-stylesheets"></a>
## 스타일시트 작업 (Working With Stylesheets)

> [!NOTE]
> Laravel의 [스타터 킷](/docs/12.x/starter-kits)에는 올바르게 설정된 Tailwind 및 Vite 구성이 이미 포함되어 있습니다. Starter Kit을 사용하지 않고 Tailwind와 Laravel을 사용하려면 [Tailwind의 Laravel 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

모든 Laravel 애플리케이션에는 이미 Tailwind와 적절하게 구성된 `vite.config.js` 파일이 포함되어 있습니다. 따라서 Vite 개발 서버를 시작하거나, 아래와 같이 Composer를 통해 `dev` 명령어를 실행하면 Laravel과 Vite 개발 서버가 모두 자동으로 시작됩니다.

```shell
composer run dev
```

애플리케이션의 CSS 파일은 `resources/css/app.css`에 작성할 수 있습니다.

<a name="working-with-blade-and-routes"></a>
## Blade 및 라우트 작업 (Working With Blade and Routes)

<a name="blade-processing-static-assets"></a>
### Vite로 정적 에셋 처리 (Processing Static Assets With Vite)

JavaScript나 CSS에서 에셋을 참조할 때, Vite는 이러한 파일을 자동으로 처리하여 버전 부여를 진행합니다. 추가로, Blade 기반 애플리케이션을 구축할 때는 Blade 템플릿에서만 참조되는 정적 에셋도 Vite가 처리 및 버전 부여할 수 있습니다.

이를 위해서는 Vite가 에셋의 존재를 인지할 수 있게, 정적 에셋을 애플리케이션의 진입점 파일에 import 해야 합니다. 예를 들어, `resources/images`에 저장된 이미지와 `resources/fonts`에 저장된 폰트 파일을 모두 처리하려면, 아래와 같이 `resources/js/app.js` 진입점 파일에 코드를 추가하세요.

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

이제 위 에셋들은 `npm run build` 시 Vite가 처리하게 됩니다. 이후 Blade 템플릿에서는 아래와 같이 `Vite::asset` 메서드로 해당 에셋의 버전 URL을 사용할 수 있습니다.

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}" />
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침 (Refreshing on Save)

Blade 기반의 전통적인 서버 사이드 렌더링 애플리케이션에서는 Vite가 뷰 파일을 수정할 때마다 브라우저를 자동으로 새로고침하며 개발 경험을 개선해 줍니다. 아래와 같이 `refresh` 옵션을 `true`로 지정하여 사용할 수 있습니다.

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

`refresh` 옵션이 `true`면, 아래 디렉터리 내 파일 저장 시 `npm run dev` 명령어 실행 중 브라우저에서 전체 페이지 새로고침이 수행됩니다.

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

`routes/**` 디렉터리 감시는 프론트엔드에서 [Ziggy](https://github.com/tighten/ziggy)로 라우트 링크를 생성하는 경우 유용합니다.

기본 제공 경로 대신 감시할 경로를 직접 지정할 수도 있습니다.

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

내부적으로 Laravel Vite 플러그인은 [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload) 패키지를 사용하며, 이 패키지의 다양한 고급 옵션을 직접 활용해 동작을 세밀하게 조정할 수도 있습니다. 필요하다면 아래와 같이 `config` 정의를 전달할 수 있습니다.

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
### 별칭 (Aliases)

자바스크립트 애플리케이션에서는 특정 경로의 디렉터리를 [별칭(alias)](#aliases)으로 지정해 두는 것이 일반적입니다. Blade에서도 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 사용해 별칭을 만들 수 있습니다. 보통 Service Provider의 `boot` 메서드에서 별칭을 등록합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

위처럼 매크로가 등록되면 Blade 템플릿 내에서 사용할 수 있습니다. 예를 들어, `resources/images/logo.png` 경로의 에셋을 다음과 같이 참조할 수 있습니다.

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo" />
```

<a name="asset-prefetching"></a>
## 에셋 프리페치(prefetching) (Asset Prefetching)

Vite 코드 스플리팅 기능을 사용하는 SPA를 개발할 때, 각 페이지 이동 시마다 필요한 에셋을 요청하게 됩니다. 이로 인해 UI 렌더링이 지연될 수 있는데, 이 현상이 문제될 경우 Laravel은 초기 페이지 로드 시 JavaScript와 CSS 에셋을 미리 프리페치할 수 있는 기능을 제공합니다.

ServiceProvider의 `boot` 메서드에서 `Vite::prefetch` 메서드를 호출해 에셋을 프리페치하도록 설정하세요.

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

위 예시에서 각 페이지 로드 시 한 번에 최대 3개 에셋을 동시 다운로드로 프리페치합니다. 필요에 따라 동시성 제한을 조정하거나, 모든 에셋을 한꺼번에 받아오도록(동시성 제한 없이) 설정할 수 있습니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch();
}
```

기본적으로 프리페치 동작은 [page load 이벤트](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event)가 발생할 때 시작합니다. 프리페치 시작 시점을 커스터마이즈하고 싶다면 Vite에서 감지할 이벤트명을 지정할 수 있습니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

이 경우 프리페치는 `window` 객체에서 `vite:prefetch` 이벤트를 수동으로 발생시킬 때 시작됩니다. 예를 들어, 페이지가 로드된 후 3초 뒤에 프리페치를 시작하려면 다음과 같이 할 수 있습니다.

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
## 커스텀 베이스 URL (Custom Base URLs)

Vite로 컴파일된 에셋을 애플리케이션과 다른 도메인, 예를 들어 CDN에 배포하는 경우, 애플리케이션의 `.env` 파일에서 `ASSET_URL` 환경 변수를 지정해야 합니다.

```env
ASSET_URL=https://cdn.example.com
```

이로써 모든 에셋 URL은 설정한 값이 접두어로 자동 추가됩니다.

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

[절대 URL은 Vite에서 재작성하지 않으므로](#url-processing) 접두어가 붙지 않음을 기억하세요.

<a name="environment-variables"></a>
## 환경 변수 (Environment Variables)

애플리케이션의 `.env` 파일에서 변수명 앞에 반드시 `VITE_`를 붙이면 해당 환경 변수를 자바스크립트로 주입할 수 있습니다.

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

주입된 환경변수는 `import.meta.env` 객체에서 사용합니다.

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트에서 Vite 비활성화 (Disabling Vite in Tests)

Laravel의 Vite 통합 기능은 테스트 수행 시에도 에셋 리졸브를 시도합니다. 이때 Vite 개발 서버가 실행 중이 아니거나 에셋이 빌드되지 않았다면 문제가 생길 수 있습니다.

테스트 중에는 Vite를 mocking 하고 싶다면, `TestCase` 클래스를 상속하는 모든 테스트에서 `withoutVite` 메서드를 호출할 수 있습니다.

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

모든 테스트에서 Vite를 아예 비활성화하고 싶다면, base `TestCase` 클래스의 `setUp` 메서드에서 이 메서드를 호출하면 됩니다.

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
## 서버 사이드 렌더링(SSR) (Server-Side Rendering (SSR))

Laravel Vite 플러그인을 통해 Vite의 서버 사이드 렌더링(SSR) 환경을 손쉽게 구축할 수 있습니다. 우선 `resources/js/ssr.js` 위치에 SSR 진입점 파일을 생성하고, 아래처럼 플러그인에 SSR 진입점 옵션을 지정합니다.

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

SSR 진입점 빌드 작업을 빠뜨리지 않도록, `package.json`의 "build" 스크립트를 아래와 같이 확장해 두길 권장합니다.

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

이제 아래 명령어로 SSR 서버를 빌드 및 실행할 수 있습니다.

```shell
npm run build
node bootstrap/ssr/ssr.js
```

[Inertia의 SSR](https://inertiajs.com/server-side-rendering)을 사용하는 경우, SSR 서버를 시작하려면 아래와 같이 Artisan 명령어를 사용할 수도 있습니다.

```shell
php artisan inertia:start-ssr
```

> [!NOTE]
> Laravel의 [스타터 킷](/docs/12.x/starter-kits)에는 Laravel, Inertia SSR, Vite 구성이 모두 포함되어 있습니다.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그 속성 (Script and Style Tag Attributes)

<a name="content-security-policy-csp-nonce"></a>
### 컨텐츠 보안 정책(CSP) nonce (Content Security Policy (CSP) Nonce)

[Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) 적용을 위해 스크립트 및 스타일 태그에 [nonce 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 추가하려면, 커스텀 [미들웨어](/docs/12.x/middleware)에서 `useCspNonce` 메서드를 호출하면 됩니다.

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

`useCspNonce` 호출 후에는, Laravel이 자동으로 모든 스크립트 및 스타일 태그에 nonce 속성을 부여합니다.

다른 곳에서도 nonce 값이 필요하다면, [Ziggy의 `@route` 디렉티브](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy)처럼, `cspNonce` 메서드로 값을 얻어 사용할 수 있습니다.

```blade
@routes(nonce: Vite::cspNonce())
```

이미 nonce 값이 있다면, `useCspNonce` 메서드에 해당 값을 전달해 Laravel에게 사용하도록 지정할 수 있습니다.

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### 서브리소스 무결성(SRI) (Subresource Integrity (SRI))

Vite 매니페스트에 에셋의 `integrity` 해시가 포함되어 있다면, Laravel은 생성되는 모든 스크립트 및 스타일 태그에 [서브리소스 무결성](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)을 위한 `integrity` 속성을 추가합니다. 기본적으로 Vite는 manifest에 무결성 해시를 포함하지 않으나, [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인을 설치해 이 기능을 활성화할 수 있습니다.

```shell
npm install --save-dev vite-plugin-manifest-sri
```

설치 후, 다음과 같이 `vite.config.js`에서 플러그인을 활성화하세요.

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

매니페스트의 키 이름을 직접 지정하고 싶으면 아래와 같이 할 수 있습니다.

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

무결성 해시 자동 감지를 비활성화하려면 `useIntegrityKey`에 `false`를 전달하세요.

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의 속성 지정 (Arbitrary Attributes)

스크립트 및 스타일 태그에 [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change)와 같은 추가 속성을 포함해야 한다면, `useScriptTagAttributes` 및 `useStyleTagAttributes` 메서드를 사용할 수 있습니다. 이 메서드는 보통 [서비스 프로바이더](/docs/12.x/providers)에서 호출합니다.

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 값을 지정하는 속성
    'async' => true, // 값 없는 속성
    'integrity' => false, // 기존 속성 제거
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

조건에 따라 속성을 동적으로 추가하고 싶다면, 콜백 함수를 전달하여 에셋의 경로, URL, 매니페스트 청크, 전체 매니페스트를 인자로 받아 처리할 수 있습니다.

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
> `$chunk` 및 `$manifest` 인자는 Vite 개발 서버 동작 중에는 `null` 값을 갖습니다.

<a name="advanced-customization"></a>
## 고급 커스터마이징 (Advanced Customization)

기본적으로 Laravel의 Vite 플러그인은 대부분의 애플리케이션에서 즉시 사용할 수 있게 적절한 convention을 따릅니다. 하지만 Vite의 동작을 더 세밀하게 조정하고 싶다면, `@vite` Blade 디렉티브 대신 다음과 같은 메서드와 옵션을 사용할 수 있습니다.

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 경로 커스텀
            ->useBuildDirectory('bundle') // 빌드 디렉토리 커스텀
            ->useManifestFilename('assets.json') // 매니페스트 파일 이름 커스텀
            ->withEntryPoints(['resources/js/app.js']) // 진입점 지정
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // 에셋 경로 생성 커스텀
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

`vite.config.js` 파일에서도 동일한 맞춤 구성을 지정해야 합니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // "hot" 파일 경로 커스텀
            buildDirectory: 'bundle', // 빌드 디렉토리 커스텀
            input: ['resources/js/app.js'], // 진입점 지정
        }),
    ],
    build: {
      manifest: 'assets.json', // 매니페스트 파일 이름 커스텀
    },
});
```

<a name="cors"></a>
### 개발 서버 CORS (Dev Server Cross-Origin Resource Sharing (CORS))

브라우저에서 Vite 개발 서버의 에셋을 불러올 때 CORS(Cross-Origin Resource Sharing) 오류가 발생한다면, 개발 서버가 외부 도메인 요청을 허용할 수 있게 설정해야 합니다. Laravel 플러그인 및 Vite에서는 다음과 같은 Origin은 별도 설정 없이 자동으로 허용됩니다.

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- 프로젝트 `.env` 내 `APP_URL`

가장 간단한 해결법은 `.env` 파일의 `APP_URL` 값을 실제 브라우저에서 접근하는 Origin과 일치시키는 것입니다. 예를 들어 `https://my-app.laravel`로 접속한다면 다음과 같이 설정해야 합니다.

```env
APP_URL=https://my-app.laravel
```

여러 Origin을 세밀하게 제어할 필요가 있다면, Vite의 [빌트인 CORS 설정](https://vite.dev/config/server-options.html#server-cors)을 사용하세요. 예를 들어 여러 Origin을 허용하려면 `vite.config.js`에서 `server.cors.origin` 옵션을 아래처럼 사용할 수 있습니다.

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

또한 정규 표현식을 사용해 특정 최상위 도메인(`*.laravel`)에 대해 모든 Origin을 허용할 수 있습니다.

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
                // 지원: SCHEME://DOMAIN.laravel[:PORT] [tl! add]
                /^https?:\/\/.*\.laravel(:\d+)?$/, //[tl! add]
            ], // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<a name="correcting-dev-server-urls"></a>
### 개발 서버 URL 수정 (Correcting Dev Server URLs)

Vite 에코시스템 내 일부 플러그인은 슬래시(`/`)로 시작하는 URL이 항상 Vite 개발 서버 경로라고 가정합니다. 하지만 Laravel과 연동된 상황에서는 반드시 그렇지 않습니다.

예를 들어, `vite-imagetools` 플러그인은 에셋을 Vite가 서빙할 때 다음과 같은 URL을 출력합니다.

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" />
```

이 플러그인은 `/@imagetools`로 시작하는 URL이 Vite에서 가로채져 처리되기를 기대하고 있습니다. 만약 이와 같은 플러그인을 사용한다면 URL을 직접 수정해야 하며, 이를 위해 `vite.config.js` 파일의 `transformOnServe` 옵션을 사용할 수 있습니다.

아래 예시에서처럼 `/@imagetools`가 포함된 모든 경로 앞에 개발 서버 URL을 붙여야 합니다.

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

이제 Vite가 에셋을 서빙할 때 아래와 같이 개발 서버 URL이 앞에 붙은 URL을 출력합니다.

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! add] -->
```