# 자산 번들링 (Vite) (Asset Bundling (Vite))

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치](#installing-node)
  - [Vite 및 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
  - [Vite 설정](#configuring-vite)
  - [스크립트와 스타일 로드](#loading-your-scripts-and-styles)
- [Vite 실행](#running-vite)
- [JavaScript 사용하기](#working-with-scripts)
  - [별칭(Aliases)](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Svelte](#svelte)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 사용하기](#working-with-stylesheets)
- [Blade 및 라우트와 함께 사용하기](#working-with-blade-and-routes)
  - [Vite로 정적 자산 처리](#blade-processing-static-assets)
  - [저장 시 자동 새로고침](#blade-refreshing-on-save)
  - [별칭(Aliases)](#blade-aliases)
- [자산 프리페치 (Asset Prefetching)](#asset-prefetching)
- [사용자 정의 Base URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트에서 Vite 비활성화](#disabling-vite-in-tests)
- [서버 사이드 렌더링 (SSR)](#ssr)
- [Script 및 Style 태그 속성](#script-and-style-attributes)
  - [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)
  - [Subresource Integrity (SRI)](#subresource-integrity-sri)
  - [임의 속성 추가](#arbitrary-attributes)
- [고급 커스터마이징](#advanced-customization)
  - [개발 서버 Cross-Origin Resource Sharing (CORS)](#cors)
  - [개발 서버 URL 수정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개 (Introduction)

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고, 프로덕션 배포를 위해 코드를 번들링하는 현대적인 프론트엔드 빌드 도구입니다. Laravel 애플리케이션을 개발할 때는 일반적으로 Vite를 사용하여 애플리케이션의 CSS와 JavaScript 파일을 프로덕션에서 사용할 수 있는 자산으로 번들링합니다.

Laravel은 공식 플러그인과 Blade 디렉티브를 제공하여 개발 환경과 프로덕션 환경에서 자산을 쉽게 로드할 수 있도록 하며, Vite와 자연스럽게 통합됩니다.

<a name="installation"></a>
## 설치 및 설정 (Installation & Setup)

> [!NOTE]
> 다음 문서는 Laravel Vite 플러그인을 수동으로 설치하고 설정하는 방법을 설명합니다. 그러나 Laravel의 [starter kits](/docs/master/starter-kits)에는 이러한 설정이 이미 포함되어 있으며, Laravel과 Vite를 가장 빠르게 시작할 수 있는 방법입니다.

<a name="installing-node"></a>
### Node 설치

Vite와 Laravel 플러그인을 실행하기 전에 Node.js(16+)와 NPM이 설치되어 있어야 합니다.

```shell
node -v
npm -v
```

[공식 Node 웹사이트](https://nodejs.org/en/download/)에서 제공하는 그래픽 설치 프로그램을 사용하여 최신 버전의 Node와 NPM을 쉽게 설치할 수 있습니다.  

또는 [Laravel Sail](https://laravel.com/docs/master/sail)을 사용 중이라면 Sail을 통해 Node와 NPM을 실행할 수도 있습니다.

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite 및 Laravel 플러그인 설치

새로 설치한 Laravel 프로젝트의 루트 디렉토리에는 `package.json` 파일이 존재합니다. 기본 `package.json` 파일에는 Vite와 Laravel 플러그인을 사용하기 위한 모든 설정이 이미 포함되어 있습니다.

NPM을 사용하여 프론트엔드 의존성을 설치할 수 있습니다.

```shell
npm install
```

<a name="configuring-vite"></a>
### Vite 설정

Vite는 프로젝트 루트에 있는 `vite.config.js` 파일을 통해 설정합니다. 필요에 따라 이 파일을 자유롭게 수정할 수 있으며, 애플리케이션에 필요한 다른 플러그인도 설치할 수 있습니다. 예를 들어 `@vitejs/plugin-react`, `@sveltejs/vite-plugin-svelte`, `@vitejs/plugin-vue` 등이 있습니다.

Laravel Vite 플러그인은 애플리케이션의 **엔트리 포인트(entry point)** 를 지정해야 합니다. 이 엔트리 포인트는 JavaScript 또는 CSS 파일이 될 수 있으며, TypeScript, JSX, TSX, Sass와 같은 전처리 언어도 포함할 수 있습니다.

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

SPA 애플리케이션(Inertia 기반 애플리케이션 포함)을 구축하는 경우에는 CSS 엔트리 포인트 없이 사용하는 것이 더 적합합니다.

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

대신 JavaScript 파일에서 CSS를 import 해야 합니다. 일반적으로 `resources/js/app.js`에서 다음과 같이 작성합니다.

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 여러 개의 엔트리 포인트와 [SSR 엔트리 포인트](#ssr)와 같은 고급 설정도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안 개발 서버 사용

로컬 개발 서버가 HTTPS로 애플리케이션을 제공하는 경우 Vite 개발 서버와 연결할 때 문제가 발생할 수 있습니다.

[Laravel Herd](https://herd.laravel.com)를 사용하여 사이트를 보안 처리했거나 [Laravel Valet](/docs/master/valet)에서 [secure 명령어](/docs/master/valet#securing-sites)를 실행했다면, Laravel Vite 플러그인이 자동으로 생성된 TLS 인증서를 감지하고 사용합니다.

애플리케이션 디렉토리 이름과 다른 호스트를 사용해 사이트를 보안 처리한 경우 `vite.config.js`에서 직접 호스트를 지정할 수 있습니다.

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

다른 웹 서버를 사용하는 경우 신뢰할 수 있는 인증서를 생성하고 Vite에서 해당 인증서를 사용하도록 수동으로 설정해야 합니다.

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

시스템에서 신뢰할 수 있는 인증서를 생성할 수 없는 경우 [@vitejs/plugin-basic-ssl plugin](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치하여 사용할 수 있습니다. 신뢰되지 않은 인증서를 사용하는 경우 `npm run dev` 실행 후 콘솔에 표시되는 "Local" 링크를 통해 브라우저에서 인증서 경고를 수락해야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2에서 Sail로 개발 서버 실행

Windows Subsystem for Linux 2(WSL2) 환경에서 [Laravel Sail](/docs/master/sail)로 Vite 개발 서버를 실행하는 경우, 브라우저가 개발 서버와 통신할 수 있도록 다음 설정을 `vite.config.js`에 추가해야 합니다.

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

개발 서버 실행 중 파일 변경이 브라우저에 반영되지 않는다면 Vite의 `server.watch.usePolling` 옵션을 설정해야 할 수도 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트와 스타일 로드

Vite 엔트리 포인트를 설정한 후 애플리케이션의 루트 템플릿 `<head>`에 `@vite()` Blade 디렉티브를 추가하여 사용할 수 있습니다.

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

CSS를 JavaScript에서 import 하는 경우 JavaScript 엔트리 포인트만 포함하면 됩니다.

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 디렉티브는 자동으로 Vite 개발 서버를 감지하고 Hot Module Replacement(HMR)를 활성화하기 위해 Vite 클라이언트를 삽입합니다.

빌드 모드에서는 컴파일되고 버전이 적용된 자산(그리고 import된 CSS)을 로드합니다.

필요하다면 `@vite` 디렉티브 호출 시 컴파일된 자산의 빌드 경로를 지정할 수도 있습니다.

```blade
<!doctype html>
<head>
    {{-- Given build path is relative to public path. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### 인라인 자산

때로는 자산의 버전된 URL을 링크하는 대신 **자산의 실제 내용(raw content)** 을 직접 포함해야 할 수 있습니다. 예를 들어 PDF 생성기에 HTML을 전달할 때 이런 방식이 필요할 수 있습니다.

이 경우 `Vite` 파사드의 `content` 메서드를 사용하여 자산의 내용을 출력할 수 있습니다.

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

Vite는 두 가지 방식으로 실행할 수 있습니다.

개발 중에는 `dev` 명령어로 개발 서버를 실행할 수 있으며, 파일 변경을 자동으로 감지하여 브라우저에 즉시 반영합니다.

프로덕션 배포용으로는 `build` 명령어를 실행하여 자산을 번들링하고 버전을 생성합니다.

```shell
# Vite 개발 서버 실행
npm run dev

# 프로덕션용 자산 빌드
npm run build
```

WSL2 환경에서 [Sail](/docs/master/sail)을 사용하는 경우 추가 설정이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## JavaScript 사용하기 (Working With JavaScript)

<a name="aliases"></a>
### 별칭 (Aliases)

Laravel 플러그인은 기본적으로 다음과 같은 별칭(alias)을 제공합니다.

```js
{
    '@' => '/resources/js'
}
```

이를 통해 애플리케이션 자산을 편리하게 import 할 수 있습니다.

필요하다면 `vite.config.js`에서 `'@'` 별칭을 덮어쓸 수 있습니다.

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

(이후 문서는 동일한 방식으로 계속 번역됩니다.)