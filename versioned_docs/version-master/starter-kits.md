# 스타터 키트 (Starter Kits)

- [소개](#introduction)
- [스타터 키트를 사용하여 애플리케이션 생성하기](#creating-an-application)
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
    - [Rate Limiting](#rate-limiting)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티에서 유지 관리하는 스타터 키트](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션을 더 빠르게 시작할 수 있도록 [애플리케이션 스타터 키트](https://laravel.com/starter-kits)를 제공합니다. 이러한 스타터 키트는 다음 Laravel 애플리케이션을 개발할 때 빠르게 시작할 수 있도록 도와주며, 사용자 등록과 인증에 필요한 라우트, 컨트롤러, 뷰를 기본적으로 포함하고 있습니다. 스타터 키트는 인증 기능을 제공하기 위해 [Laravel Fortify](/docs/master/fortify)를 사용합니다.

이 스타터 키트를 사용하는 것은 선택 사항이며 필수는 아닙니다. Laravel의 새 복사본을 설치하여 애플리케이션을 처음부터 직접 구축할 수도 있습니다. 어떤 방식을 선택하든 훌륭한 애플리케이션을 만들 수 있을 것입니다.

<a name="creating-an-application"></a>
## 스타터 키트를 사용하여 애플리케이션 생성하기 (Creating an Application Using a Starter Kit)

스타터 키트를 사용하여 새로운 Laravel 애플리케이션을 생성하려면 먼저 [PHP와 Laravel CLI 도구를 설치](/docs/master/installation#installing-php)해야 합니다. 이미 PHP와 Composer가 설치되어 있다면 Composer를 통해 Laravel installer CLI 도구를 설치할 수 있습니다.

```shell
composer global require laravel/installer
```

그 다음 Laravel installer CLI를 사용하여 새로운 Laravel 애플리케이션을 생성합니다. Laravel installer는 사용할 스타터 키트를 선택하도록 안내합니다.

```shell
laravel new my-app
```

Laravel 애플리케이션을 생성한 후에는 NPM을 통해 프론트엔드 의존성을 설치하고 Laravel 개발 서버를 실행하면 됩니다.

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버가 실행되면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접근할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 키트 (Available Starter Kits)

<a name="react"></a>
### React

React 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 React 프론트엔드를 가진 Laravel 애플리케이션을 구축할 때 사용할 수 있는 강력하고 현대적인 시작점을 제공합니다.

Inertia를 사용하면 전통적인 서버 사이드 라우팅과 컨트롤러를 활용하면서도 현대적인 단일 페이지 React 애플리케이션(SPA)을 만들 수 있습니다. 이를 통해 React의 강력한 프론트엔드 기능과 Laravel의 높은 백엔드 생산성, 그리고 빠른 Vite 컴파일을 함께 활용할 수 있습니다.

React 스타터 키트는 React 19, TypeScript, Tailwind, 그리고 [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="svelte"></a>
### Svelte

Svelte 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 Svelte 프론트엔드를 가진 Laravel 애플리케이션을 구축할 때 사용할 수 있는 강력하고 현대적인 시작점을 제공합니다.

Inertia를 사용하면 전통적인 서버 사이드 라우팅과 컨트롤러를 활용하면서도 현대적인 단일 페이지 Svelte 애플리케이션을 만들 수 있습니다. 이를 통해 Svelte의 프론트엔드 성능과 Laravel의 높은 백엔드 생산성, 그리고 빠른 Vite 컴파일을 함께 활용할 수 있습니다.

Svelte 스타터 키트는 Svelte 5, TypeScript, Tailwind, 그리고 [shadcn-svelte](https://www.shadcn-svelte.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 Vue 프론트엔드를 가진 Laravel 애플리케이션을 구축할 때 훌륭한 시작점을 제공합니다.

Inertia를 사용하면 전통적인 서버 사이드 라우팅과 컨트롤러를 활용하면서도 현대적인 단일 페이지 Vue 애플리케이션을 만들 수 있습니다. 이를 통해 Vue의 프론트엔드 기능과 Laravel의 백엔드 생산성, 그리고 빠른 Vite 컴파일을 함께 활용할 수 있습니다.

Vue 스타터 키트는 Vue Composition API, TypeScript, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드를 사용하는 Laravel 애플리케이션을 구축하기 위한 완벽한 시작점을 제공합니다.

Livewire는 PHP만으로 동적이고 반응형인 프론트엔드 UI를 만들 수 있는 강력한 방법입니다. Blade 템플릿을 주로 사용하는 팀이나 React, Svelte, Vue 같은 JavaScript 기반 SPA 프레임워크보다 더 단순한 대안을 찾는 팀에게 특히 적합합니다.

Livewire 스타터 키트는 Livewire, Tailwind, 그리고 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
## 스타터 키트 커스터마이징 (Starter Kit Customization)

<a name="react-customization"></a>
### React

React 스타터 키트는 Inertia 2, React 19, Tailwind 4, 그리고 [shadcn/ui](https://ui.shadcn.com)로 구성되어 있습니다. 다른 스타터 키트와 마찬가지로 모든 백엔드 및 프론트엔드 코드는 애플리케이션 내부에 포함되어 있으므로 완전히 자유롭게 커스터마이징할 수 있습니다.

프론트엔드 코드의 대부분은 `resources/js` 디렉토리에 위치합니다. 애플리케이션의 외형과 동작을 원하는 대로 변경하기 위해 이 코드들을 자유롭게 수정할 수 있습니다.

```text
resources/js/
├── components/    # Reusable React components
├── hooks/         # React hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

추가적인 shadcn 컴포넌트를 게시하려면 먼저 [게시할 컴포넌트를 찾습니다](https://ui.shadcn.com). 그 다음 `npx`를 사용하여 컴포넌트를 게시합니다.

```shell
npx shadcn@latest add switch
```

이 명령어는 Switch 컴포넌트를 `resources/js/components/ui/switch.tsx` 경로에 생성합니다. 컴포넌트가 생성된 후에는 원하는 페이지에서 사용할 수 있습니다.

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

React 스타터 키트에는 두 가지 기본 레이아웃이 포함되어 있습니다. 하나는 "sidebar" 레이아웃이고 다른 하나는 "header" 레이아웃입니다. 기본값은 sidebar 레이아웃이며, `resources/js/layouts/app-layout.tsx` 파일 상단에서 import하는 레이아웃을 변경하여 header 레이아웃으로 전환할 수 있습니다.

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### Sidebar 변형

sidebar 레이아웃에는 세 가지 변형이 있습니다: 기본 sidebar, "inset", 그리고 "floating". 원하는 변형을 사용하려면 `resources/js/components/app-sidebar.tsx` 컴포넌트를 수정합니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

React 스타터 키트에 포함된 로그인 페이지와 회원가입 페이지 같은 인증 페이지에도 세 가지 레이아웃 변형이 있습니다: "simple", "card", "split".

인증 레이아웃을 변경하려면 `resources/js/layouts/auth-layout.tsx` 파일 상단에서 import하는 레이아웃을 수정합니다.

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="svelte-customization"></a>
### Svelte

Svelte 스타터 키트는 Inertia 2, Svelte 5, Tailwind, 그리고 [shadcn-svelte](https://www.shadcn-svelte.com/)로 구성되어 있습니다. 다른 스타터 키트와 마찬가지로 모든 백엔드 및 프론트엔드 코드는 애플리케이션 내부에 포함되어 있으므로 완전히 커스터마이징할 수 있습니다.

프론트엔드 코드의 대부분은 `resources/js` 디렉토리에 위치합니다. 애플리케이션의 외형과 동작을 원하는 대로 수정할 수 있습니다.

```text
resources/js/
├── components/    # Reusable Svelte components
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration and Svelte rune modules
├── pages/         # Page components
└── types/         # TypeScript definitions
```

추가적인 shadcn-svelte 컴포넌트를 게시하려면 먼저 [게시할 컴포넌트를 찾습니다](https://www.shadcn-svelte.com). 그 다음 `npx`를 사용하여 게시합니다.

```shell
npx shadcn-svelte@latest add switch
```

이 명령어는 Switch 컴포넌트를 `resources/js/components/ui/switch/switch.svelte` 경로에 생성합니다.

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

Svelte 스타터 키트에도 "sidebar"와 "header" 두 가지 기본 레이아웃이 있습니다. 기본값은 sidebar이며 `resources/js/layouts/AppLayout.svelte` 파일에서 import하는 레이아웃을 변경하여 header 레이아웃으로 전환할 수 있습니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.svelte'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.svelte'; // [tl! add]
```

<a name="svelte-sidebar-variants"></a>
#### Sidebar 변형

sidebar 레이아웃에는 기본 sidebar, "inset", "floating" 세 가지 변형이 있습니다. `resources/js/components/AppSidebar.svelte` 컴포넌트를 수정하여 원하는 변형을 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="svelte-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Svelte 스타터 키트의 인증 페이지에도 "simple", "card", "split" 세 가지 레이아웃 변형이 있습니다.

인증 레이아웃을 변경하려면 `resources/js/layouts/AuthLayout.svelte` 파일에서 import하는 레이아웃을 수정합니다.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.svelte'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.svelte'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 키트는 Inertia 2, Vue 3 Composition API, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/)로 구성되어 있습니다. 다른 스타터 키트와 마찬가지로 모든 코드가 애플리케이션 내부에 존재하므로 자유롭게 커스터마이징할 수 있습니다.

프론트엔드 코드의 대부분은 `resources/js` 디렉토리에 있습니다.

```text
resources/js/
├── components/    # Reusable Vue components
├── composables/   # Vue composables / hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

추가적인 shadcn-vue 컴포넌트를 게시하려면 먼저 [컴포넌트를 찾은 뒤](https://www.shadcn-vue.com) `npx` 명령어로 게시합니다.

```shell
npx shadcn-vue@latest add switch
```

이 명령어는 Switch 컴포넌트를 `resources/js/components/ui/Switch.vue` 경로에 생성합니다.

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

Vue 스타터 키트에도 "sidebar"와 "header" 두 가지 기본 레이아웃이 있습니다. 기본값은 sidebar이며 `resources/js/layouts/AppLayout.vue` 파일에서 import를 변경하여 header 레이아웃으로 전환할 수 있습니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### Sidebar 변형

sidebar 레이아웃에는 기본 sidebar, "inset", "floating" 세 가지 변형이 있습니다. `resources/js/components/AppSidebar.vue`를 수정하여 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Vue 스타터 키트의 인증 페이지 역시 "simple", "card", "split" 세 가지 레이아웃 변형을 제공합니다.

`resources/js/layouts/AuthLayout.vue` 파일에서 import하는 레이아웃을 수정하여 변경할 수 있습니다.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 키트는 Livewire 4, Tailwind, 그리고 [Flux UI](https://fluxui.dev/)로 구성되어 있습니다. 다른 스타터 키트와 마찬가지로 모든 코드가 애플리케이션 내부에 있으므로 자유롭게 수정할 수 있습니다.

프론트엔드 코드는 대부분 `resources/views` 디렉토리에 있습니다.

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

Livewire 스타터 키트 역시 "sidebar"와 "header" 두 가지 기본 레이아웃을 제공합니다. 기본값은 sidebar입니다. header 레이아웃으로 변경하려면 `resources/views/layouts/app.blade.php` 파일에서 사용하는 레이아웃을 수정하고, main Flux 컴포넌트에 `container` 속성을 추가해야 합니다.

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Livewire 스타터 키트의 인증 페이지 역시 "simple", "card", "split" 세 가지 레이아웃을 제공합니다.

`resources/views/layouts/auth.blade.php` 파일에서 사용하는 레이아웃을 변경하면 됩니다.

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a name="authentication"></a>
## 인증 (Authentication)

모든 스타터 키트는 인증 처리를 위해 [Laravel Fortify](/docs/master/fortify)를 사용합니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 인증 기능에 필요한 라우트, 컨트롤러, 로직을 제공합니다.

Fortify는 애플리케이션의 `config/fortify.php` 설정 파일에서 활성화된 기능에 따라 다음과 같은 인증 라우트를 자동으로 등록합니다.

| Route                              | Method | Description                         |
| ---------------------------------- | ------ | ----------------------------------- |
| `/login`                           | `GET`    | 로그인 폼 표시                      |
| `/login`                           | `POST`   | 사용자 인증                         |
| `/logout`                          | `POST`   | 로그아웃                            |
| `/register`                        | `GET`    | 회원가입 폼 표시                    |
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
| `/two-factor-challenge`            | `GET`    | 2FA 인증 폼 표시                    |
| `/two-factor-challenge`            | `POST`   | 2FA 코드 검증                       |

애플리케이션에 등록된 모든 라우트는 `php artisan route:list` Artisan 명령어로 확인할 수 있습니다.

<a name="enabling-and-disabling-features"></a>
### 기능 활성화 및 비활성화

`config/fortify.php` 설정 파일에서 Fortify 기능을 제어할 수 있습니다.

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

기능을 비활성화하려면 `features` 배열에서 해당 항목을 주석 처리하거나 제거하면 됩니다. 예를 들어 `Features::registration()`을 제거하면 공개 회원가입 기능이 비활성화됩니다.

[React](#react), [Svelte](#svelte), [Vue](#vue) 스타터 키트를 사용하는 경우 프론트엔드 코드에서도 해당 기능과 관련된 라우트 참조를 제거해야 합니다. 예를 들어 이메일 인증을 비활성화했다면 React, Svelte, Vue 컴포넌트에서 `verification` 라우트에 대한 import와 참조를 제거해야 합니다.

이는 이 스타터 키트들이 빌드 시점에 타입 안전한 라우팅을 생성하는 Wayfinder를 사용하기 때문입니다. 존재하지 않는 라우트를 참조하면 애플리케이션 빌드가 실패합니다.

<a name="customizing-actions"></a>
### 사용자 생성 및 비밀번호 재설정 커스터마이징

사용자가 회원가입을 하거나 비밀번호를 재설정할 때 Fortify는 `app/Actions/Fortify` 디렉토리에 있는 액션 클래스를 호출합니다.

| File                          | Description                           |
| ----------------------------- | ------------------------------------- |
| `CreateNewUser.php`           | 새 사용자 유효성 검증 및 생성        |
| `ResetUserPassword.php`       | 사용자 비밀번호 유효성 검증 및 업데이트 |
| `PasswordValidationRules.php` | 비밀번호 유효성 검증 규칙 정의        |

예를 들어 회원가입 로직을 커스터마이징하려면 `CreateNewUser` 액션을 수정합니다.

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

스타터 키트에는 기본적으로 2단계 인증(2FA)이 포함되어 있습니다. 사용자는 TOTP를 지원하는 인증 앱을 사용하여 계정을 보호할 수 있습니다. 2FA는 `config/fortify.php` 설정 파일의 `Features::twoFactorAuthentication()` 옵션을 통해 기본적으로 활성화되어 있습니다.

`confirm` 옵션은 2FA를 완전히 활성화하기 전에 코드를 검증하도록 요구하며, `confirmPassword` 옵션은 2FA를 활성화하거나 비활성화하기 전에 비밀번호 확인을 요구합니다. 자세한 내용은 [Fortify의 2단계 인증 문서](/docs/master/fortify#two-factor-authentication)를 참고하십시오.

<a name="rate-limiting"></a>
### Rate Limiting

Rate limiting은 무차별 대입 공격(brute-force)이나 반복적인 로그인 시도가 인증 엔드포인트에 과부하를 주는 것을 방지합니다. Fortify의 rate limiting 동작은 `FortifyServiceProvider`에서 커스터마이징할 수 있습니다.

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="workos"></a>
## WorkOS AuthKit 인증 (WorkOS AuthKit Authentication)

기본적으로 React, Svelte, Vue, Livewire 스타터 키트는 Laravel의 내장 인증 시스템을 사용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등의 기능을 제공합니다.

또한 각 스타터 키트에는 [WorkOS AuthKit](https://authkit.com)을 기반으로 하는 변형 버전도 제공됩니다. 이 버전은 다음 기능을 제공합니다.

- 소셜 인증 (Google, Microsoft, GitHub, Apple)
- Passkey 인증
- 이메일 기반 "Magic Auth"
- SSO

WorkOS를 인증 제공자로 사용하려면 [WorkOS 계정](https://workos.com)이 필요합니다. WorkOS는 월간 활성 사용자 100만 명까지 무료 인증 서비스를 제공합니다.

WorkOS AuthKit을 애플리케이션의 인증 제공자로 사용하려면 `laravel new` 명령어로 애플리케이션을 생성할 때 WorkOS 옵션을 선택하면 됩니다.

### WorkOS 스타터 키트 설정

WorkOS 기반 스타터 키트를 사용하여 애플리케이션을 생성한 후 `.env` 파일에 다음 환경 변수를 설정해야 합니다.

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

이 값들은 WorkOS 대시보드에서 제공되는 애플리케이션 설정 값과 일치해야 합니다.

또한 WorkOS 대시보드에서 애플리케이션의 홈페이지 URL을 설정해야 합니다. 사용자가 애플리케이션에서 로그아웃한 후 이 URL로 리디렉션됩니다.

#### AuthKit 인증 방식 설정

WorkOS 기반 스타터 키트를 사용하는 경우 WorkOS AuthKit 설정에서 "Email + Password" 인증을 비활성화하는 것을 권장합니다. 이렇게 하면 사용자는 소셜 로그인, passkey, Magic Auth, SSO를 통해서만 인증할 수 있으며 애플리케이션이 사용자 비밀번호를 직접 처리할 필요가 없습니다.

#### AuthKit 세션 타임아웃 설정

WorkOS AuthKit 세션 비활성 시간 제한을 Laravel 애플리케이션의 세션 타임아웃과 동일하게 설정하는 것을 권장합니다. 일반적으로 Laravel의 기본 세션 타임아웃은 약 2시간입니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React, Svelte, Vue 스타터 키트는 Inertia의 [server-side rendering](https://inertiajs.com/server-side-rendering) 기능과 호환됩니다. Inertia SSR 번들을 빌드하려면 다음 명령어를 실행합니다.

```shell
npm run build:ssr
```

편의를 위해 `composer dev:ssr` 명령어도 제공됩니다. 이 명령어는 SSR 번들을 빌드한 후 Laravel 개발 서버와 Inertia SSR 서버를 함께 실행하여 로컬 환경에서 SSR을 테스트할 수 있도록 합니다.

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티에서 유지 관리하는 스타터 키트

Laravel installer로 새 애플리케이션을 생성할 때 Packagist에 등록된 커뮤니티 스타터 키트를 `--using` 옵션으로 지정할 수 있습니다.

```shell
laravel new my-app --using=example/starter-kit
```

#### 스타터 키트 만들기

자신의 스타터 키트를 다른 사람들이 사용할 수 있도록 하려면 [Packagist](https://packagist.org)에 게시해야 합니다. 또한 `.env.example` 파일에 필요한 환경 변수를 정의하고, 설치 후 실행해야 하는 명령어는 스타터 키트의 `composer.json` 파일의 `post-create-project-cmd` 배열에 추가해야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문

<a name="faq-upgrade"></a>
#### 어떻게 업그레이드하나요?

각 스타터 키트는 새로운 애플리케이션을 시작하기 위한 견고한 출발점을 제공합니다. 코드에 대한 완전한 소유권이 있으므로 원하는 대로 수정하고 확장하여 애플리케이션을 구축할 수 있습니다. 따라서 스타터 키트 자체를 별도로 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증을 어떻게 활성화하나요?

이메일 인증을 사용하려면 `App/Models/User.php` 모델에서 `MustVerifyEmail` import의 주석을 해제하고 모델이 `MustVerifyEmail` 인터페이스를 구현하도록 해야 합니다.

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

회원가입 후 사용자는 인증 이메일을 받게 됩니다. 사용자의 이메일이 인증될 때까지 특정 라우트 접근을 제한하려면 라우트에 `verified` middleware를 추가합니다.

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 변형 스타터 키트를 사용하는 경우 이메일 인증은 필요하지 않습니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 어떻게 수정하나요?

애플리케이션의 브랜딩에 맞게 기본 이메일 템플릿을 커스터마이징하고 싶을 수 있습니다. 이를 위해 다음 명령어를 실행하여 이메일 뷰를 애플리케이션으로 게시합니다.

```
php artisan vendor:publish --tag=laravel-mail
```

이 명령어를 실행하면 `resources/views/vendor/mail` 디렉토리에 여러 파일이 생성됩니다. 또한 `resources/views/vendor/mail/themes/default.css` 파일을 수정하여 기본 이메일 템플릿의 디자인과 스타일을 변경할 수 있습니다.