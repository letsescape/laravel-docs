# 스타터 키트 (Starter Kits)

- [소개](#introduction)
- [스타터 키트를 사용하여 애플리케이션 만들기](#creating-an-application)
- [사용 가능한 스타터 키트](#available-starter-kits)
    - [React](#react)
    - [Svelte](#svelte)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 키트 커스터마이징](#starter-kit-customization)
    - [React](#react-customization)
    - [Svelte](#svelte-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [인증](#authentication)
    - [기능 활성화 및 비활성화](#enabling-and-disabling-features)
    - [사용자 생성 및 비밀번호 재설정 커스터마이징](#customizing-actions)
    - [2단계 인증](#two-factor-authentication)
    - [요청 제한](#rate-limiting)
- [팀](#teams)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티에서 유지 관리하는 스타터 키트](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개 (Introduction)

새 Laravel 애플리케이션을 더 빠르게 시작할 수 있도록, Laravel은 [애플리케이션 스타터 키트](https://laravel.com/starter-kits)를 제공합니다. 이 스타터 키트는 다음 Laravel 애플리케이션을 빠르게 구축할 수 있도록 도와주며, 애플리케이션 사용자를 등록하고 인증하는 데 필요한 라우트, 컨트롤러, 뷰를 포함합니다. 스타터 키트는 인증 기능을 제공하기 위해 [Laravel Fortify](/docs/13.x/fortify)를 사용합니다.

물론 이 스타터 키트를 사용할 수 있지만, 반드시 사용해야 하는 것은 아닙니다. Laravel을 새로 설치한 뒤 처음부터 직접 애플리케이션을 구축해도 됩니다. 어떤 방식을 선택하든 훌륭한 결과물을 만들 수 있을 것입니다!

<a name="creating-an-application"></a>
## 스타터 키트를 사용하여 애플리케이션 만들기 (Creating an Application Using a Starter Kit)

스타터 키트 중 하나를 사용하여 새 Laravel 애플리케이션을 만들려면 먼저 [PHP와 Laravel CLI 도구를 설치](/docs/13.x/installation#installing-php)해야 합니다. 이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel installer CLI 도구를 설치할 수 있습니다.

```shell
composer global require laravel/installer
```

그런 다음 Laravel installer CLI를 사용하여 새 Laravel 애플리케이션을 만듭니다. Laravel installer는 원하는 스타터 키트를 선택하라는 메시지를 표시합니다.

```shell
laravel new my-app
```

Laravel 애플리케이션을 만든 뒤에는 NPM을 통해 프론트엔드 의존성을 설치하고 Laravel 개발 서버를 시작하기만 하면 됩니다.

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버를 시작하면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접속할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 키트 (Available Starter Kits)

<a name="react"></a>
### React

React 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 React 프론트엔드를 갖춘 Laravel 애플리케이션을 만들기 위한 견고하고 현대적인 출발점을 제공합니다.

Inertia를 사용하면 전통적인 서버 사이드 라우팅과 컨트롤러를 그대로 사용하면서도 현대적인 싱글 페이지 React 애플리케이션을 만들 수 있습니다. 이를 통해 React의 강력한 프론트엔드 기능과 Laravel의 뛰어난 백엔드 생산성, 매우 빠른 Vite 컴파일을 함께 활용할 수 있습니다.

React 스타터 키트는 React 19, TypeScript, Tailwind, [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="svelte"></a>
### Svelte

Svelte 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 Svelte 프론트엔드를 갖춘 Laravel 애플리케이션을 만들기 위한 견고하고 현대적인 출발점을 제공합니다.

Inertia를 사용하면 전통적인 서버 사이드 라우팅과 컨트롤러를 그대로 사용하면서도 현대적인 싱글 페이지 Svelte 애플리케이션을 만들 수 있습니다. 이를 통해 Svelte의 강력한 프론트엔드 기능과 Laravel의 뛰어난 백엔드 생산성, 매우 빠른 Vite 컴파일을 함께 활용할 수 있습니다.

Svelte 스타터 키트는 Svelte 5, TypeScript, Tailwind, [shadcn-svelte](https://www.shadcn-svelte.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 Vue 프론트엔드를 갖춘 Laravel 애플리케이션을 만들기 위한 훌륭한 출발점을 제공합니다.

Inertia를 사용하면 전통적인 서버 사이드 라우팅과 컨트롤러를 그대로 사용하면서도 현대적인 싱글 페이지 Vue 애플리케이션을 만들 수 있습니다. 이를 통해 Vue의 강력한 프론트엔드 기능과 Laravel의 뛰어난 백엔드 생산성, 매우 빠른 Vite 컴파일을 함께 활용할 수 있습니다.

Vue 스타터 키트는 Vue Composition API, TypeScript, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드를 갖춘 Laravel 애플리케이션을 만들기 위한 완벽한 출발점을 제공합니다.

Livewire는 PHP만으로 동적이고 반응형인 프론트엔드 UI를 만들 수 있는 강력한 방식입니다. 주로 Blade 템플릿을 사용하고, React, Svelte, Vue와 같은 JavaScript 기반 SPA 프레임워크보다 단순한 대안을 찾는 팀에 잘 맞습니다.

Livewire 스타터 키트는 Livewire, Tailwind, [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
## 스타터 키트 커스터마이징 (Starter Kit Customization)

<a name="react-customization"></a>
### React

React 스타터 키트는 Inertia 3, React 19, Tailwind 4, [shadcn/ui](https://ui.shadcn.com)를 기반으로 만들어졌습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프론트엔드 코드가 모두 애플리케이션 안에 있으므로 완전히 자유롭게 커스터마이징할 수 있습니다.

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

추가 shadcn 컴포넌트를 게시하려면 먼저 [게시하려는 컴포넌트를 찾습니다](https://ui.shadcn.com). 그런 다음 `npx`를 사용하여 컴포넌트를 게시합니다.

```shell
npx shadcn@latest add switch
```

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
#### 사용 가능한 레이아웃

React 스타터 키트에는 선택할 수 있는 두 가지 기본 레이아웃이 포함되어 있습니다. 바로 "sidebar" 레이아웃과 "header" 레이아웃입니다. 기본값은 sidebar 레이아웃이지만, 애플리케이션의 `resources/js/layouts/app-layout.tsx` 파일 상단에서 가져오는 레이아웃을 수정하여 header 레이아웃으로 전환할 수 있습니다.

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### 사이드바 변형

sidebar 레이아웃에는 세 가지 변형이 포함되어 있습니다. 기본 sidebar 변형, "inset" 변형, "floating" 변형입니다. `resources/js/components/app-sidebar.tsx` 컴포넌트를 수정하여 가장 마음에 드는 변형을 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

React 스타터 키트에 포함된 로그인 페이지와 등록 페이지 같은 인증 페이지도 "simple", "card", "split"이라는 세 가지 레이아웃 변형을 제공합니다.

인증 레이아웃을 변경하려면 애플리케이션의 `resources/js/layouts/auth-layout.tsx` 파일 상단에서 가져오는 레이아웃을 수정합니다.

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="svelte-customization"></a>
### Svelte

Svelte 스타터 키트는 Inertia 3, Svelte 5, Tailwind, [shadcn-svelte](https://www.shadcn-svelte.com/)를 기반으로 만들어졌습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프론트엔드 코드가 모두 애플리케이션 안에 있으므로 완전히 자유롭게 커스터마이징할 수 있습니다.

대부분의 프론트엔드 코드는 `resources/js` 디렉터리에 있습니다. 애플리케이션의 모양과 동작을 커스터마이징하기 위해 원하는 코드를 자유롭게 수정할 수 있습니다.

```text
resources/js/
├── components/    # Reusable Svelte components
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration and Svelte rune modules
├── pages/         # Page components
└── types/         # TypeScript definitions
```

추가 shadcn-svelte 컴포넌트를 게시하려면 먼저 [게시하려는 컴포넌트를 찾습니다](https://www.shadcn-svelte.com). 그런 다음 `npx`를 사용하여 컴포넌트를 게시합니다.

```shell
npx shadcn-svelte@latest add switch
```

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
#### 사용 가능한 레이아웃

Svelte 스타터 키트에는 선택할 수 있는 두 가지 기본 레이아웃이 포함되어 있습니다. 바로 "sidebar" 레이아웃과 "header" 레이아웃입니다. 기본값은 sidebar 레이아웃이지만, 애플리케이션의 `resources/js/layouts/AppLayout.svelte` 파일 상단에서 가져오는 레이아웃을 수정하여 header 레이아웃으로 전환할 수 있습니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.svelte'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.svelte'; // [tl! add]
```

<a name="svelte-sidebar-variants"></a>
#### 사이드바 변형

sidebar 레이아웃에는 세 가지 변형이 포함되어 있습니다. 기본 sidebar 변형, "inset" 변형, "floating" 변형입니다. `resources/js/components/AppSidebar.svelte` 컴포넌트를 수정하여 가장 마음에 드는 변형을 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="svelte-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Svelte 스타터 키트에 포함된 로그인 페이지와 등록 페이지 같은 인증 페이지도 "simple", "card", "split"이라는 세 가지 레이아웃 변형을 제공합니다.

인증 레이아웃을 변경하려면 애플리케이션의 `resources/js/layouts/AuthLayout.svelte` 파일 상단에서 가져오는 레이아웃을 수정합니다.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.svelte'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.svelte'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 키트는 Inertia 3, Vue 3 Composition API, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/)를 기반으로 만들어졌습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프론트엔드 코드가 모두 애플리케이션 안에 있으므로 완전히 자유롭게 커스터마이징할 수 있습니다.

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

추가 shadcn-vue 컴포넌트를 게시하려면 먼저 [게시하려는 컴포넌트를 찾습니다](https://www.shadcn-vue.com). 그런 다음 `npx`를 사용하여 컴포넌트를 게시합니다.

```shell
npx shadcn-vue@latest add switch
```

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
#### 사용 가능한 레이아웃

Vue 스타터 키트에는 선택할 수 있는 두 가지 기본 레이아웃이 포함되어 있습니다. 바로 "sidebar" 레이아웃과 "header" 레이아웃입니다. 기본값은 sidebar 레이아웃이지만, 애플리케이션의 `resources/js/layouts/AppLayout.vue` 파일 상단에서 가져오는 레이아웃을 수정하여 header 레이아웃으로 전환할 수 있습니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 변형

sidebar 레이아웃에는 세 가지 변형이 포함되어 있습니다. 기본 sidebar 변형, "inset" 변형, "floating" 변형입니다. `resources/js/components/AppSidebar.vue` 컴포넌트를 수정하여 가장 마음에 드는 변형을 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Vue 스타터 키트에 포함된 로그인 페이지와 등록 페이지 같은 인증 페이지도 "simple", "card", "split"이라는 세 가지 레이아웃 변형을 제공합니다.

인증 레이아웃을 변경하려면 애플리케이션의 `resources/js/layouts/AuthLayout.vue` 파일 상단에서 가져오는 레이아웃을 수정합니다.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 키트는 Livewire 4, Tailwind, [Flux UI](https://fluxui.dev/)를 기반으로 만들어졌습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프론트엔드 코드가 모두 애플리케이션 안에 있으므로 완전히 자유롭게 커스터마이징할 수 있습니다.

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
#### 사용 가능한 레이아웃

Livewire 스타터 키트에는 선택할 수 있는 두 가지 기본 레이아웃이 포함되어 있습니다. 바로 "sidebar" 레이아웃과 "header" 레이아웃입니다. 기본값은 sidebar 레이아웃이지만, 애플리케이션의 `resources/views/layouts/app.blade.php` 파일에서 사용하는 레이아웃을 수정하여 header 레이아웃으로 전환할 수 있습니다. 또한 기본 Flux 컴포넌트에 `container` 속성을 추가해야 합니다.

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Livewire 스타터 키트에 포함된 로그인 페이지와 등록 페이지 같은 인증 페이지도 "simple", "card", "split"이라는 세 가지 레이아웃 변형을 제공합니다.

인증 레이아웃을 변경하려면 애플리케이션의 `resources/views/layouts/auth.blade.php` 파일에서 사용하는 레이아웃을 수정합니다.

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a name="authentication"></a>
## 인증 (Authentication)

모든 스타터 키트는 인증을 처리하기 위해 [Laravel Fortify](/docs/13.x/fortify)를 사용합니다. Fortify는 로그인, 등록, 비밀번호 재설정, 이메일 인증 등을 위한 라우트, 컨트롤러, 로직을 제공합니다.

Fortify는 애플리케이션의 `config/fortify.php` 설정 파일에서 활성화된 기능에 따라 다음 인증 라우트를 자동으로 등록합니다.

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

`php artisan route:list` Artisan 명령어를 사용하면 애플리케이션의 모든 라우트를 표시할 수 있습니다.

<a name="enabling-and-disabling-features"></a>
### 기능 활성화 및 비활성화

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

기능을 비활성화하려면 `features` 배열에서 해당 기능 항목을 주석 처리하거나 제거합니다. 예를 들어 공개 등록을 비활성화하려면 `Features::registration()`을 제거합니다.

[React](#react), [Svelte](#svelte) 또는 [Vue](#vue) 스타터 키트를 사용하는 경우, 프론트엔드 코드에서도 비활성화된 기능의 라우트를 참조하는 부분을 제거해야 합니다. 예를 들어 이메일 인증을 비활성화했다면 React, Svelte 또는 Vue 컴포넌트에서 `verification` 라우트를 가져오거나 참조하는 부분을 제거해야 합니다. 이러한 작업이 필요한 이유는 이 스타터 키트들이 타입 안전 라우팅을 위해 Wayfinder를 사용하며, Wayfinder가 빌드 시점에 라우트 정의를 생성하기 때문입니다. 더 이상 존재하지 않는 라우트를 참조하면 애플리케이션 빌드가 실패합니다.

<a name="customizing-actions"></a>
### 사용자 생성 및 비밀번호 재설정 사용자 정의

사용자가 회원가입하거나 비밀번호를 재설정하면, Fortify는 애플리케이션의 `app/Actions/Fortify` 디렉터리에 있는 액션 클래스를 호출합니다.

| 파일                          | 설명                                  |
| ----------------------------- | ------------------------------------- |
| `CreateNewUser.php`           | 새 사용자를 유효성 검증하고 생성합니다 |
| `ResetUserPassword.php`       | 사용자 비밀번호를 유효성 검증하고 업데이트합니다 |
| `PasswordValidationRules.php` | 비밀번호 유효성 검증 규칙을 정의합니다 |

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
### 2단계 인증

스타터 키트에는 기본 제공 2단계 인증(2FA)이 포함되어 있어, 사용자가 TOTP와 호환되는 인증 앱을 사용해 계정을 보호할 수 있습니다. 2FA는 애플리케이션의 `config/fortify.php` 설정 파일에서 `Features::twoFactorAuthentication()`을 통해 기본적으로 활성화됩니다.

`confirm` 옵션은 2FA가 완전히 활성화되기 전에 사용자가 코드를 확인하도록 요구하며, `confirmPassword`는 2FA를 활성화하거나 비활성화하기 전에 비밀번호 확인을 요구합니다. 자세한 내용은 [Fortify의 2단계 인증 문서](/docs/13.x/fortify#two-factor-authentication)를 참고하십시오.

<a name="rate-limiting"></a>
### 요청 속도 제한

요청 속도 제한은 무차별 대입 공격과 반복적인 로그인 시도로 인해 인증 엔드포인트에 과도한 부하가 걸리는 것을 방지합니다. 애플리케이션의 `FortifyServiceProvider`에서 Fortify의 요청 속도 제한 동작을 사용자 정의할 수 있습니다.

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="teams"></a>
## 팀 (Teams)

React, Svelte, Vue, Livewire 스타터 키트는 팀 지원 기능을 포함하여 생성할 수도 있습니다. 팀 기능이 활성화되면 각 사용자는 하나 이상의 팀에 속하며 현재 팀을 가집니다. 회원가입 중에는 새 사용자에게 개인 팀이 자동으로 제공됩니다. 또한 스타터 키트에는 팀 생성, 팀 전환, 멤버 초대, 팀 세부 정보 업데이트를 위한 팀 관리 화면도 포함되어 있습니다.

라우트가 현재 팀 범위로 지정되면 현재 팀의 슬러그가 URL에 포함됩니다. 예를 들어 대시보드 라우트는 `/{current_team}/dashboard`가 되며, 팀 관리 페이지는 `settings/teams/{team}` 같은 라우트를 사용합니다. `{current_team}` 및 `{team}` 라우트 파라미터를 사용할 때, 스타터 키트는 라우트 접근을 허용하기 전에 인증된 사용자가 요청한 팀에 속해 있는지 자동으로 확인합니다.

팀을 고려한 URL을 더 편리하게 생성할 수 있도록, 스타터 키트는 인증된 사용자의 현재 팀에 대한 URL 기본값을 등록합니다. 이를 통해 `route('dashboard')` 같은 헬퍼 호출이 현재 팀의 슬러그를 자동으로 포함할 수 있습니다. 사용자가 로그인하거나 회원가입하거나 팀을 전환하면, 스타터 키트는 현재 팀을 업데이트하고 이러한 URL 기본값을 새로고침하여 생성된 링크가 계속 올바른 팀 컨텍스트를 사용하도록 합니다.

팀을 생성하거나 이름을 변경할 때, 스타터 키트는 안전하지 않거나 충돌하는 라우트 세그먼트를 만들 수 있는 예약된 이름을 사용자가 선택하지 못하도록 방지합니다. 예를 들어 `settings`, `login`, `dashboard` 같은 라우트 접두어와 충돌할 수 있는 이름은 사용할 수 없습니다.

<a name="workos"></a>
## WorkOS AuthKit 인증 (WorkOS AuthKit Authentication)

기본적으로 React, Svelte, Vue, Livewire 스타터 키트는 모두 Laravel의 내장 인증 시스템을 사용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등을 제공합니다. 또한 각 스타터 키트에는 [WorkOS AuthKit](https://authkit.com) 기반 변형도 제공되며, 다음 기능을 제공합니다.

<div class="content-list" markdown="1">

- 소셜 인증(Google, Microsoft, GitHub, Apple)
- 패스키 인증
- 이메일 기반 "Magic Auth"
- SSO

</div>

WorkOS를 인증 제공자로 사용하려면 [WorkOS 계정](https://workos.com)이 필요합니다. WorkOS는 월간 활성 사용자 100만 명 이하의 애플리케이션에 무료 인증을 제공합니다.

WorkOS AuthKit을 애플리케이션의 인증 제공자로 사용하려면, `laravel new`를 통해 새 스타터 키트 기반 애플리케이션을 만들 때 WorkOS 옵션을 선택하십시오.

### WorkOS 스타터 키트 설정

WorkOS 기반 스타터 키트를 사용하여 새 애플리케이션을 만든 후에는 애플리케이션의 `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 이 변수들은 WorkOS 대시보드에서 애플리케이션에 대해 제공된 값과 일치해야 합니다.

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한 WorkOS 대시보드에서 애플리케이션 홈페이지 URL을 설정해야 합니다. 이 URL은 사용자가 애플리케이션에서 로그아웃한 뒤 리디렉션될 위치입니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방식 설정

WorkOS 기반 스타터 키트를 사용할 때는 애플리케이션의 WorkOS AuthKit 설정에서 "Email + Password" 인증을 비활성화하는 것을 권장합니다. 이렇게 하면 사용자는 소셜 인증 제공자, 패스키, "Magic Auth", SSO를 통해서만 인증할 수 있습니다. 이를 통해 애플리케이션은 사용자 비밀번호를 직접 처리하지 않아도 됩니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 타임아웃 설정

또한 WorkOS AuthKit 세션 비활성 타임아웃을 Laravel 애플리케이션에 설정된 세션 타임아웃 기준과 일치하도록 설정하는 것을 권장합니다. 일반적으로 이 값은 2시간입니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React, Svelte, Vue 스타터 키트는 Inertia의 [서버 사이드 렌더링](https://inertiajs.com/server-side-rendering) 기능과 호환됩니다. 애플리케이션용 Inertia SSR 호환 번들을 빌드하려면 `build:ssr` 명령어를 실행하십시오.

```shell
npm run build:ssr
```

편의를 위해 `composer dev:ssr` 명령어도 제공됩니다. 이 명령어는 애플리케이션용 SSR 호환 번들을 빌드한 뒤 Laravel 개발 서버와 Inertia SSR 서버를 시작합니다. 이를 통해 Inertia의 서버 사이드 렌더링 엔진을 사용하여 애플리케이션을 로컬에서 테스트할 수 있습니다.

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지보수 스타터 키트

Laravel 설치 프로그램을 사용하여 새 Laravel 애플리케이션을 만들 때, Packagist에서 제공되는 커뮤니티 유지보수 스타터 키트를 `--using` 플래그에 지정할 수 있습니다.

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 키트 만들기

스타터 키트를 다른 사람들이 사용할 수 있도록 하려면 [Packagist](https://packagist.org)에 게시해야 합니다. 스타터 키트는 필요한 환경 변수를 `.env.example` 파일에 정의해야 하며, 필요한 설치 후 명령어는 스타터 키트의 `composer.json` 파일에 있는 `post-create-project-cmd` 배열에 나열해야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문

<a name="faq-upgrade"></a>
#### 어떻게 업그레이드합니까?

모든 스타터 키트는 다음 애플리케이션을 위한 견고한 출발점을 제공합니다. 코드를 완전히 소유하므로, 애플리케이션을 원하는 모습에 맞게 조정하고 사용자 정의하며 구축할 수 있습니다. 그러나 스타터 키트 자체를 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증은 어떻게 활성화합니까?

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
#### 기본 이메일 템플릿은 어떻게 수정합니까?

애플리케이션의 브랜딩에 더 잘 맞도록 기본 이메일 템플릿을 사용자 정의하고 싶을 수 있습니다. 이 템플릿을 수정하려면 다음 명령어로 이메일 뷰를 애플리케이션에 게시해야 합니다.

```
php artisan vendor:publish --tag=laravel-mail
```

이 명령어는 `resources/views/vendor/mail`에 여러 파일을 생성합니다. 기본 이메일 템플릿의 모양과 외형을 변경하려면 이 파일들뿐만 아니라 `resources/views/vendor/mail/themes/default.css` 파일도 수정할 수 있습니다.
