# 스타터 키트 (Starter Kits)

- [소개](#introduction)
- [스타터 키트를 사용하여 애플리케이션 생성](#creating-an-application)
- [사용 가능한 스타터 키트](#available-starter-kits)
    - [React](#react)
    - [Svelte](#svelte)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 키트 사용자 지정](#starter-kit-customization)
    - [React](#react-customization)
    - [Svelte](#svelte-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [인증](#authentication)
    - [기능 활성화 및 비활성화](#enabling-and-disabling-features)
    - [사용자 생성 및 비밀번호 재설정 사용자 지정](#customizing-actions)
    - [2단계 인증](#two-factor-authentication)
    - [속도 제한](#rate-limiting)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 유지 스타터 키트](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션 구축을 한 발 앞서 시작할 수 있도록 [애플리케이션 스타터 키트](https://laravel.com/starter-kits)를 제공하게 되어 기쁘게 생각합니다. 이러한 스타터 키트는 다음 Laravel 애플리케이션 구축을 시작하는 데 도움이 되며, 애플리케이션 사용자를 등록하고 인증하는 데 필요한 라우트, 컨트롤러 및 뷰를 포함합니다. 스타터 키트는 [Laravel Fortify](/docs/12.x/fortify)를 사용하여 인증을 제공합니다.

이러한 스타터 키트를 사용해도 좋지만 필수는 아닙니다. Laravel의 새로운 사본을 설치하기만 하면 처음부터 자신만의 애플리케이션을 자유롭게 구축할 수 있습니다. 어느 쪽이든, 우리는 당신이 훌륭한 것을 만들 것이라는 것을 알고 있습니다!

<a name="creating-an-application"></a>
## 스타터 키트를 사용하여 애플리케이션 생성 (Creating an Application Using a Starter Kit)

스타터 키트 중 하나를 사용하여 새로운 Laravel 애플리케이션을 만들려면 먼저 [PHP 및 Laravel CLI 도구를 설치](/docs/12.x/installation#installing-php)해야 합니다. PHP 및 Composer가 이미 설치되어 있는 경우 Composer를 통해 Laravel 설치 프로그램 CLI 도구를 설치할 수 있습니다.

```shell
composer global require laravel/installer
```

그런 다음 Laravel 설치 프로그램 CLI를 사용하여 새 Laravel 애플리케이션을 만듭니다. Laravel 설치 프로그램은 원하는 스타터 키트를 선택하라는 메시지를 표시합니다.

```shell
laravel new my-app
```

Laravel 애플리케이션을 생성한 후 NPM을 통해 프론트엔드 종속성을 설치하고 Laravel 개발 서버를 시작하기만 하면 됩니다.

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버를 시작하면 웹 브라우저의 [http://localhost:8000](http://localhost:8000)에서 애플리케이션에 액세스할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 키트 (Available Starter Kits)

<a name="react"></a>
### React

React 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 React 프론트엔드로 Laravel 애플리케이션을 구축하기 위한 강력하고 현대적인 시작점을 제공합니다.

Inertia를 사용하면 클래식 서버 측 라우팅 및 컨트롤러를 사용하여 현대적인 단일 페이지 React 애플리케이션을 구축할 수 있습니다. 이를 통해 Laravel의 놀라운 백엔드 생산성 및 초고속 Vite 컴파일과 결합된 React의 프론트엔드 성능을 즐길 수 있습니다.

React 스타터 키트는 React 19, TypeScript, Tailwind 및 [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 활용합니다.

<a name="svelte"></a>
### Svelte

Svelte 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 Svelte 프론트엔드로 Laravel 애플리케이션을 구축하기 위한 강력하고 현대적인 시작점을 제공합니다.

Inertia를 사용하면 클래식 서버 측 라우팅 및 컨트롤러를 사용하여 현대적인 단일 페이지 Svelte 애플리케이션을 구축할 수 있습니다. 이를 통해 Laravel의 놀라운 백엔드 생산성 및 초고속 Vite 컴파일과 결합된 Svelte의 프론트엔드 성능을 즐길 수 있습니다.

Svelte 스타터 키트는 Svelte 5, TypeScript, Tailwind 및 [shadcn-svelte](https://www.shadcn-svelte.com/) 컴포넌트 라이브러리를 활용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 Vue 프론트엔드로 Laravel 애플리케이션을 구축하기 위한 훌륭한 시작점을 제공합니다.

Inertia를 사용하면 클래식 서버 측 라우팅 및 컨트롤러를 사용하여 최신 단일 페이지 Vue 애플리케이션을 구축할 수 있습니다. 이를 통해 Laravel의 놀라운 백엔드 생산성 및 초고속 Vite 컴파일과 결합된 Vue의 프론트엔드 성능을 즐길 수 있습니다.

Vue 스타터 키트는 Vue 구성 API, TypeScript, Tailwind 및 [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 활용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드로 Laravel 애플리케이션을 구축하기 위한 완벽한 시작점을 제공합니다.

Livewire는 PHP만 사용하여 동적, 반응형 프론트엔드 UI를 구축하는 강력한 방법입니다. 주로 Blade 템플릿을 사용하고 React, Svelte 및 Vue와 같은 JavaScript 기반 SPA 프레임워크에 대한 더 간단한 대안을 찾고 있는 팀에 매우 적합합니다.

Livewire 스타터 키트는 Livewire, Tailwind 및 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 활용합니다.

<a name="starter-kit-customization"></a>
## 스타터 키트 사용자 지정 (Starter Kit Customization)

<a name="react-customization"></a>
### React

React 스타터 키트는 Inertia 2, React 19, Tailwind 4 및 [shadcn/ui](https://ui.shadcn.com)로 제작되었습니다. 모든 스타터 키트와 마찬가지로 모든 백엔드 및 프론트엔드 코드가 애플리케이션 내에 존재하므로 완전한 사용자 지정가 가능합니다.

프론트엔드 코드의 대부분은 `resources/js` 디렉터리에 있습니다. 애플리케이션의 모양과 동작을 사용자 지정하기 위해 코드를 자유롭게 수정할 수 있습니다.

```text
resources/js/
├── components/    # Reusable React components
├── hooks/         # React hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

추가 shadcn 컴포넌트를 게시하려면 먼저 [게시하려는 컴포넌트를 찾으세요](https://ui.shadcn.com). 그런 다음 `npx`를 사용하여 컴포넌트를 게시합니다.

```shell
npx shadcn@latest add switch
```

이 예에서 명령은 스위치 컴포넌트를 `resources/js/components/ui/switch.tsx`에 게시합니다. 컴포넌트가 게시되면 모든 페이지에서 사용할 수 있습니다.

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

React 스타터 키트에는 "사이드바" 레이아웃과 "헤더" 레이아웃이라는 두 가지 기본 레이아웃이 포함되어 있습니다. 사이드바 레이아웃이 기본값이지만 애플리케이션의 `resources/js/layouts/app-layout.tsx` 파일 상단에서 가져온 레이아웃을 수정하여 헤더 레이아웃으로 전환할 수 있습니다.

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃에는 기본 사이드바 변형, "삽입" 변형, "부동" 변형의 세 가지 변형이 포함되어 있습니다. `resources/js/components/app-sidebar.tsx` 컴포넌트를 수정하여 가장 좋아하는 변형을 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

로그인 페이지 및 등록 페이지와 같이 React 스타터 키트에 포함된 인증 페이지는 "단순", "카드" 및 "분할"의 세 가지 레이아웃 변형도 제공합니다.

인증 레이아웃을 변경하려면 애플리케이션의 `resources/js/layouts/auth-layout.tsx` 파일 상단에서 가져온 레이아웃을 수정하세요.

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="svelte-customization"></a>
### Svelte

Svelte 스타터 키트는 Inertia 2, Svelte 5, Tailwind 및 [shadcn-svelte](https://www.shadcn-svelte.com/)로 제작되었습니다. 모든 스타터 키트와 마찬가지로 모든 백엔드 및 프론트엔드 코드가 애플리케이션 내에 존재하므로 완전한 사용자 지정가 가능합니다.

프론트엔드 코드의 대부분은 `resources/js` 디렉터리에 있습니다. 애플리케이션의 모양과 동작을 사용자 지정하기 위해 코드를 자유롭게 수정할 수 있습니다.

```text
resources/js/
├── components/    # Reusable Svelte components
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration and Svelte rune modules
├── pages/         # Page components
└── types/         # TypeScript definitions
```

추가 shadcn-svelte 컴포넌트를 게시하려면 먼저 [게시할 컴포넌트를 찾으세요](https://www.shadcn-svelte.com). 그런 다음 `npx`를 사용하여 컴포넌트를 게시합니다.

```shell
npx shadcn-svelte@latest add switch
```

이 예에서 명령은 스위치 컴포넌트를 `resources/js/components/ui/switch/switch.svelte`에 게시합니다. 컴포넌트가 게시되면 모든 페이지에서 사용할 수 있습니다.

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

Svelte 스타터 키트에는 "사이드바" 레이아웃과 "헤더" 레이아웃이라는 두 가지 기본 레이아웃이 포함되어 있습니다. 사이드바 레이아웃이 기본값이지만 애플리케이션의 `resources/js/layouts/AppLayout.svelte` 파일 상단에서 가져온 레이아웃을 수정하여 헤더 레이아웃으로 전환할 수 있습니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.svelte'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.svelte'; // [tl! add]
```

<a name="svelte-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃에는 기본 사이드바 변형, "삽입" 변형, "부동" 변형의 세 가지 변형이 포함되어 있습니다. `resources/js/components/AppSidebar.svelte` 컴포넌트를 수정하여 가장 좋아하는 변형을 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="svelte-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

로그인 페이지 및 등록 페이지와 같이 Svelte 스타터 키트에 포함된 인증 페이지는 "단순", "카드" 및 "분할"의 세 가지 레이아웃 변형도 제공합니다.

인증 레이아웃을 변경하려면 애플리케이션의 `resources/js/layouts/AuthLayout.svelte` 파일 상단에서 가져온 레이아웃을 수정하세요.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.svelte'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.svelte'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 키트는 Inertia 2, Vue 3 구성 API, Tailwind 및 [shadcn-vue](https://www.shadcn-vue.com/)로 제작되었습니다. 모든 스타터 키트와 마찬가지로 모든 백엔드 및 프론트엔드 코드가 애플리케이션 내에 존재하므로 완전한 사용자 지정가 가능합니다.

프론트엔드 코드의 대부분은 `resources/js` 디렉터리에 있습니다. 애플리케이션의 모양과 동작을 사용자 지정하기 위해 코드를 자유롭게 수정할 수 있습니다.

```text
resources/js/
├── components/    # Reusable Vue components
├── composables/   # Vue composables / hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

추가 shadcn-vue 컴포넌트를 게시하려면 먼저 [게시할 컴포넌트를 찾으세요](https://www.shadcn-vue.com). 그런 다음 `npx`를 사용하여 컴포넌트를 게시합니다.

```shell
npx shadcn-vue@latest add switch
```

이 예에서 명령은 스위치 컴포넌트를 `resources/js/components/ui/Switch.vue`에 게시합니다. 컴포넌트가 게시되면 모든 페이지에서 사용할 수 있습니다.

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

Vue 스타터 키트에는 "사이드바" 레이아웃과 "헤더" 레이아웃이라는 두 가지 기본 레이아웃이 포함되어 있습니다. 사이드바 레이아웃이 기본값이지만 애플리케이션의 `resources/js/layouts/AppLayout.vue` 파일 상단에서 가져온 레이아웃을 수정하여 헤더 레이아웃으로 전환할 수 있습니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃에는 기본 사이드바 변형, "삽입" 변형, "부동" 변형의 세 가지 변형이 포함되어 있습니다. `resources/js/components/AppSidebar.vue` 컴포넌트를 수정하여 가장 좋아하는 변형을 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

로그인 페이지 및 등록 페이지와 같이 Vue 스타터 키트에 포함된 인증 페이지는 "단순", "카드" 및 "분할"의 세 가지 레이아웃 변형도 제공합니다.

인증 레이아웃을 변경하려면 애플리케이션의 `resources/js/layouts/AuthLayout.vue` 파일 상단에서 가져온 레이아웃을 수정하세요.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 키트는 Livewire 4, Tailwind 및 [Flux UI](https://fluxui.dev/)로 제작되었습니다. 모든 스타터 키트와 마찬가지로 모든 백엔드 및 프론트엔드 코드가 애플리케이션 내에 존재하므로 완전한 사용자 지정가 가능합니다.

프론트엔드 코드의 대부분은 `resources/views` 디렉터리에 있습니다. 애플리케이션의 모양과 동작을 사용자 지정하기 위해 코드를 자유롭게 수정할 수 있습니다.

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

Livewire 스타터 키트에는 선택할 수 있는 두 가지 기본 레이아웃, 즉 "사이드바" 레이아웃과 "헤더" 레이아웃이 포함되어 있습니다. 사이드바 레이아웃이 기본값이지만 애플리케이션의 `resources/views/layouts/app.blade.php` 파일에서 사용되는 레이아웃을 수정하여 헤더 레이아웃으로 전환할 수 있습니다. 또한 기본 Flux 컴포넌트에 `container` 속성을 추가해야 합니다.

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

로그인 페이지 및 등록 페이지와 같이 Livewire 스타터 키트에 포함된 인증 페이지는 "단순", "카드" 및 "분할"의 세 가지 레이아웃 변형도 제공합니다.

인증 레이아웃을 변경하려면 애플리케이션의 `resources/views/layouts/auth.blade.php` 파일에서 사용되는 레이아웃을 수정하세요.

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a name="authentication"></a>
## 입증 (Authentication)

모든 스타터 키트는 [Laravel Fortify](/docs/12.x/fortify)를 사용하여 인증을 처리합니다. Fortify는 라우트, 컨트롤러 및 로그인, 등록, 비밀번호 재설정, 이메일 확인 등에 대한 논리를 제공합니다.

Fortify는 애플리케이션의 `config/fortify.php` 구성 파일에서 활성화된 기능을 기반으로 다음 인증 라우트를 자동으로 등록합니다.

| 라우트 | 방법 | 설명 |
| ---------------------------------- | ------ | ----------------------------------- |
| `/login` | `GET` | 로그인 양식 표시 |
| `/login` | `POST` | 사용자 인증 |
| `/logout` | `POST` | 사용자 로그아웃 |
| `/register` | `GET` | 등록 양식 표시 |
| `/register` | `POST` | 새 사용자 만들기 |
| `/forgot-password` | `GET` | 비밀번호 재설정 요청 양식 표시 |
| `/forgot-password` | `POST` | 비밀번호 재설정 링크 보내기 |
| `/reset-password/{token}` | `GET` | 비밀번호 재설정 양식 표시 |
| `/reset-password` | `POST` | 비밀번호 업데이트 |
| `/email/verify` | `GET` | 이메일 확인 공지 표시 |
| `/email/verify/{id}/{hash}` | `GET` | 이메일 주소 확인 |
| `/email/verification-notification` | `POST` | 확인 이메일 다시 보내기 |
| `/user/confirm-password` | `GET` | 비밀번호 확인 양식 표시 |
| `/user/confirm-password` | `POST` | 비밀번호 확인 |
| `/two-factor-challenge` | `GET` | 2FA 챌린지 양식 표시 |
| `/two-factor-challenge` | `POST` | 2FA 코드 확인 |

`php artisan route:list` Artisan 명령을 사용하면 애플리케이션에 모든 라우트를 표시할 수 있습니다.

<a name="enabling-and-disabling-features"></a>
### 기능 활성화 및 비활성화

애플리케이션의 `config/fortify.php` 구성 파일에서 활성화되는 Fortify 기능을 제어할 수 있습니다.

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

기능을 비활성화하려면 `features` 배열에서 해당 기능 항목을 주석 처리하거나 제거하십시오. 예를 들어 공개 등록을 비활성화하려면 `Features::registration()`를 제거하세요.

[React](#react), [Svelte](#svelte) 또는 [Vue](#vue) 스타터 키트를 사용하는 경우 프론트엔드 코드에서 비활성화된 기능의 라우트에 대한 참조도 제거해야 합니다. 예를 들어 이메일 확인을 비활성화하는 경우 React, Svelte 또는 Vue 컴포넌트에서 `verification` 라우트에 대한 가져오기 및 참조를 제거해야 합니다. 이는 이러한 스타터 키트가 빌드 시 라우트 정의를 생성하는 유형 안전 라우팅을 위해 Wayfinder를 사용하기 때문에 필요합니다. 더 이상 존재하지 않는 라우트를 참조하면 애플리케이션이 빌드되지 않습니다.

<a name="customizing-actions"></a>
### 사용자 생성 및 비밀번호 재설정 사용자 지정

사용자가 비밀번호를 등록하거나 재설정하면 Fortify는 애플리케이션의 `app/Actions/Fortify` 디렉토리에 있는 작업 클래스를 호출합니다.

| 파일 | 설명 |
| ----------------------------- | ------------------------------------- |
| `CreateNewUser.php` | 새 사용자 확인 및 생성 |
| `ResetUserPassword.php` | 사용자 비밀번호 확인 및 업데이트 |
| `PasswordValidationRules.php` | 비밀번호 유효성 검사 규칙 정의 |

예를 들어 애플리케이션의 등록 논리를 사용자 지정하려면 `CreateNewUser` 작업을 편집해야 합니다.

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

스타터 키트에는 2단계 인증(2FA)이 내장되어 있어 사용자가 TOTP 호환 인증 앱을 사용하여 계정을 보호할 수 있습니다. 2FA는 기본적으로 애플리케이션의 `config/fortify.php` 구성 파일에 있는 `Features::twoFactorAuthentication()`를 통해 활성화됩니다.

`confirm` 옵션은 2FA를 완전히 활성화하기 전에 사용자가 코드를 확인하도록 요구하는 반면, `confirmPassword`는 2FA를 활성화 또는 비활성화하기 전에 비밀번호 확인을 요구합니다. 자세한 내용은 [Fortify의 2단계 인증 문서](/docs/12.x/fortify#two-factor-authentication)를 참조하세요.

<a name="rate-limiting"></a>
### 속도 제한

속도 제한은 무차별 공격과 반복적인 로그인 시도가 인증 엔드포인트를 압도하는 것을 방지합니다. 애플리케이션의 `FortifyServiceProvider`에서 Fortify의 속도 제한 동작을 사용자 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="workos"></a>
## WorkOS AuthKit 인증 (WorkOS AuthKit Authentication)

기본적으로 React, Svelte, Vue 및 Livewire 스타터 키트는 모두 Laravel의 내장 인증 시스템을 활용하여 로그인, 등록, 비밀번호 재설정, 이메일 확인 등을 제공합니다. 또한 다음을 제공하는 각 스타터 키트의 [WorkOS AuthKit](https://authkit.com) 기반 변형도 제공합니다.

<div class="content-list" markdown="1">

- 소셜 인증(Google, Microsoft, GitHub, Apple)
- 패스키 인증
- 이메일 기반 "Magic Auth"
- SSO

</div>

WorkOS를 인증으로 사용 프로바이더 [WorkOS 계정 필요](https://workos.com) WorkOS는 최대 100만 명의 월간 활성 사용자가 있는 애플리케이션에 대해 무료 인증을 제공합니다.

WorkOS AuthKit를 애플리케이션 인증 프로바이더로 사용하려면 `laravel new`를 통해 새 스타터 키트 구동 애플리케이션을 생성할 때 WorkOS 옵션을 선택하세요.

### WorkOS 스타터 키트 구성

WorkOS 구동 스타터 키트를 사용하여 새 애플리케이션을 생성한 후 애플리케이션의 `.env` 파일에서 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY` 및 `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 이러한 변수는 애플리케이션의 WorkOS 대시보드에 제공된 값과 일치해야 합니다.

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한 WorkOS 대시보드에서 애플리케이션 홈페이지 URL를 구성해야 합니다. 이 URL는 사용자가 애플리케이션에서 로그아웃한 후 리디렉션되는 곳입니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방법 구성

WorkOS 구동 스타터 키트를 사용하는 경우 애플리케이션의 WorkOS AuthKit 구성 설정 내에서 "이메일 + 비밀번호" 인증을 비활성화하여 사용자가 소셜 인증 프로바이더, 패스키, "Magic Auth" 및 SSO를 통해서만 인증할 수 있도록 하는 것이 좋습니다. 이를 통해 애플리케이션은 사용자 비밀번호 처리를 완전히 피할 수 있습니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 시간 초과 구성

또한 Laravel 애플리케이션에 구성된 세션 시간 초과 임계값(일반적으로 2시간)과 일치하도록 WorkOS AuthKit 세션 비활성 시간 초과를 구성하는 것이 좋습니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React, Svelte 및 Vue 스타터 키트는 Inertia의 [서버 측 렌더링](https://inertiajs.com/server-side-rendering) 기능과 호환됩니다. 애플리케이션에 맞는 Inertia SSR 호환 번들을 빌드하려면 `build:ssr` 명령을 실행하세요.

```shell
npm run build:ssr
```

편의를 위해 `composer dev:ssr` 명령도 사용할 수 있습니다. 이 명령은 애플리케이션에 대한 SSR 호환 번들을 구축한 후 Laravel 개발 서버 및 Inertia SSR 서버를 시작하므로 Inertia의 서버 측 렌더링 엔진을 사용하여 로컬에서 애플리케이션을 테스트할 수 있습니다.

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티에서 관리하는 스타터 키트

Laravel 설치 프로그램을 사용하여 새로운 Laravel 애플리케이션을 생성할 때 Packagist에서 사용할 수 있는 커뮤니티 유지 관리 스타터 키트를 `--using` 플래그에 제공할 수 있습니다.

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 키트 만들기

귀하의 스타터 키트를 다른 사람이 사용할 수 있도록 하려면 이를 [Packagist](https://packagist.org)에 게시해야 합니다. 스타터 키트는 `.env.example` 파일에 필수 환경 변수를 정의해야 하며 필요한 설치 후 명령은 스타터 키트 `composer.json` 파일의 `post-create-project-cmd` 배열에 나열되어야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문

<a name="faq-upgrade"></a>
#### 어떻게 업그레이드하나요?

모든 스타터 키트는 다음 애플리케이션을 위한 확실한 출발점을 제공합니다. 코드에 대한 완전한 소유권을 통해 귀하가 구상한 대로 정확하게 애플리케이션을 조정하고, 사용자 지정하고, 구축할 수 있습니다. 그러나 스타터 키트 자체를 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 확인을 어떻게 활성화하나요?

`App/Models/User.php` 모델에서 가져오기 `MustVerifyEmail`의 주석 처리를 제거하고 모델이 `MustVerifyEmail` 인터페이스를 구현하는지 확인하여 이메일 확인을 추가할 수 있습니다.

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

등록 후 사용자는 확인 이메일을 받게 됩니다. 사용자의 이메일 주소가 확인될 때까지 특정 라우트에 대한 액세스를 제한하려면 `verified` 미들웨어를 라우트에 추가하세요.

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> 스타터 키트의 [WorkOS](#workos) 변형을 사용하는 경우 이메일 확인이 필요하지 않습니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 어떻게 수정합니까?

애플리케이션의 브랜딩에 더 잘 맞도록 기본 이메일 템플릿을 사용자 지정할 수 있습니다. 이 템플릿을 수정하려면 다음 명령을 사용하여 이메일 뷰를 애플리케이션에 게시해야 합니다.

```
php artisan vendor:publish --tag=laravel-mail
```

그러면 `resources/views/vendor/mail`에 여러 파일이 생성됩니다. 이러한 파일과 `resources/views/vendor/mail/themes/default.css` 파일을 수정하여 기본 이메일 템플릿의 모양과 모양을 변경할 수 있습니다.
