# 스타터 킷 (Starter Kits)

- [소개](#introduction)
- [스타터 킷으로 애플리케이션 생성하기](#creating-an-application)
- [사용 가능한 스타터 킷](#available-starter-kits)
    - [React](#react)
    - [Svelte](#svelte)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 킷 커스터마이즈](#starter-kit-customization)
    - [React](#react-customization)
    - [Svelte](#svelte-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [인증](#authentication)
    - [기능 활성화 및 비활성화](#enabling-and-disabling-features)
    - [사용자 생성 및 비밀번호 재설정 커스터마이즈](#customizing-actions)
    - [2단계 인증](#two-factor-authentication)
    - [속도 제한](#rate-limiting)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 유지 스타터 킷](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션 개발을 빠르게 시작할 수 있도록, 저희는 [애플리케이션 스타터 킷](https://laravel.com/starter-kits)을 제공합니다. 이 스타터 킷은 여러분이 Laravel 애플리케이션을 신속하게 구축할 수 있도록 도와주며, 사용자 등록 및 인증에 필요한 라우트, 컨트롤러, 뷰가 기본 제공됩니다. 스타터 킷은 인증을 위해 [Laravel Fortify](/docs/12.x/fortify)를 사용합니다.

이 스타터 킷을 반드시 사용할 필요는 없으며, 원한다면 Laravel을 처음부터 설치하여 직접 애플리케이션을 설계해도 됩니다. 어떤 방법을 택하든, 멋진 서비스를 만드시길 바랍니다!

<a name="creating-an-application"></a>
## 스타터 킷으로 애플리케이션 생성하기 (Creating an Application Using a Starter Kit)

Laravel 스타터 킷 중 하나로 새 애플리케이션을 생성하려면, 먼저 [PHP와 Laravel CLI 도구를 설치](/docs/12.x/installation#installing-php)해야 합니다. 이미 PHP와 Composer가 설치되어 있다면, 아래 명령어로 Laravel 설치기 CLI 도구를 Composer로 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

그 다음, Laravel 설치기 CLI를 사용하여 새 Laravel 애플리케이션을 생성합니다. 설치기를 실행하면 원하는 스타터 킷을 선택하라는 안내가 표시됩니다:

```shell
laravel new my-app
```

Laravel 애플리케이션이 생성된 후에는, NPM으로 프론트엔드 의존성을 설치하고 Laravel 개발 서버를 실행하면 됩니다:

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버가 실행되면, 애플리케이션은 브라우저에서 [http://localhost:8000](http://localhost:8000)에서 접근 가능합니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 킷 (Available Starter Kits)

<a name="react"></a>
### React

React 스타터 킷은 [Inertia](https://inertiajs.com)을 활용해 React 프론트엔드로 Laravel 애플리케이션을 구축하는 견고하고 현대적인 출발점을 제공합니다.

Inertia를 이용하면, 서버 사이드 라우팅과 컨트롤러를 그대로 활용하면서 모던한 싱글 페이지 React 애플리케이션을 만들 수 있습니다. 덕분에 React의 프론트엔드 기능과 Laravel의 강력한 백엔드 개발 생산성, Vite의 빠른 빌드 성능을 모두 누릴 수 있습니다.

React 스타터 킷은 React 19, TypeScript, Tailwind, 그리고 [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="svelte"></a>
### Svelte

Svelte 스타터 킷은 [Inertia](https://inertiajs.com)를 기반으로 Svelte 프론트엔드로 Laravel 애플리케이션을 구축하는 현대적이고 강력한 기초를 제공합니다.

Inertia를 통해 서버 사이드 라우팅과 컨트롤러를 그대로 활용하면서 싱글 페이지 Svelte 애플리케이션을 개발할 수 있습니다. Svelte의 프론트엔드 파워와 Laravel, Vite의 생산성을 함께 경험할 수 있습니다.

Svelte 스타터 킷은 Svelte 5, TypeScript, Tailwind, [shadcn-svelte](https://www.shadcn-svelte.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 킷은 [Inertia](https://inertiajs.com)를 활용해 Vue 프론트엔드로 Laravel 애플리케이션을 빠르게 시작할 수 있는 출발점을 제공합니다.

Inertia를 통해 서버 사이드 라우팅과 컨트롤러를 쓰면서 싱글 페이지 Vue 애플리케이션을 만들 수 있으며, Vue의 프론트엔드 기능과 Laravel, Vite의 생산성을 동시에 누릴 수 있습니다.

Vue 스타터 킷은 Vue Composition API, TypeScript, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 채택합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 킷은 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드를 활용한 Laravel 애플리케이션 개발의 최적 출발점입니다.

Livewire는 PHP만으로 다이나믹하고 반응형인 프론트엔드 UI를 빌드할 수 있는 강력한 방법입니다. Blade 템플릿 위주로 개발하는 팀이나, React, Svelte, Vue 등 JS 기반 SPA 프레임워크보다 더 단순한 대안을 찾는 분들에게 적합합니다.

Livewire 스타터 킷은 Livewire, Tailwind, [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
## 스타터 킷 커스터마이즈 (Starter Kit Customization)

<a name="react-customization"></a>
### React

React 스타터 킷은 Inertia 2, React 19, Tailwind 4, [shadcn/ui](https://ui.shadcn.com)로 구성됩니다. 모든 스타터 킷과 마찬가지로, 백엔드와 프론트엔드 코드는 모두 애플리케이션 내에 존재하므로 자유롭게 커스터마이즈할 수 있습니다.

프론트엔드 코드 대부분은 `resources/js` 디렉터리에 위치합니다. 스타일이나 동작을 자유롭게 변경하여 맞춤형 애플리케이션을 만들 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 타입 정의
```

추가적인 shadcn 컴포넌트를 도입하려면, [원하는 컴포넌트를 선택](https://ui.shadcn.com)한 다음 다음과 같이 `npx` 명령어로 추가할 수 있습니다:

```shell
npx shadcn@latest add switch
```

예시의 경우, Switch 컴포넌트가 `resources/js/components/ui/switch.tsx`에 추가됩니다. 추가된 컴포넌트는 어느 페이지에서든 사용할 수 있습니다:

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

#### 사용 가능한 레이아웃

React 스타터 킷에는 "sidebar" 레이아웃과 "header" 레이아웃, 두 가지 기본 레이아웃이 포함되어 있습니다. 기본값은 sidebar 레이아웃이며, `resources/js/layouts/app-layout.tsx` 파일에서 import 부분을 수정해 header 레이아웃으로 전환할 수 있습니다:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

#### 사이드바 변형

사이드바 레이아웃에는 기본 variant, "inset" variant, "floating" variant의 세 가지 변형이 있습니다. 원하는 variant로 사용하려면 `resources/js/components/app-sidebar.tsx` 컴포넌트에서 수정하면 됩니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

#### 인증 페이지 레이아웃 변형

React 스타터 킷의 로그인, 회원가입 등 인증 페이지에는 "simple", "card", "split" 세 가지 레이아웃 변형이 제공됩니다.

인증 레이아웃을 변경하려면 `resources/js/layouts/auth-layout.tsx`에서 import 부분을 수정합니다:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="svelte-customization"></a>
### Svelte

Svelte 스타터 킷은 Inertia 2, Svelte 5, Tailwind, [shadcn-svelte](https://www.shadcn-svelte.com/)로 구성되어 있습니다. 모든 스타터 킷과 마찬가지로, 백엔드와 프론트엔드 코드는 모두 애플리케이션 내에 존재하여 자유롭게 수정할 수 있습니다.

프론트엔드 코드 대부분은 `resources/js` 디렉터리에 있습니다. 여러분은 언제든 코드를 수정해 스타일이나 동작을 자유롭게 커스터마이즈할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 Svelte 컴포넌트
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수, 설정, Svelte rune 모듈
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 타입 정의
```

shadcn-svelte 컴포넌트를 추가하려면, [추가할 컴포넌트 선택](https://www.shadcn-svelte.com) 후 아래와 같이 실행하세요:

```shell
npx shadcn-svelte@latest add switch
```

이 명령어를 실행하면 Switch 컴포넌트가 `resources/js/components/ui/switch/switch.svelte`에 추가됩니다. 어느 페이지에서든 사용할 수 있습니다:

```svelte
<script lang="ts">
    import { Switch } from '@/components/ui/switch'
</script>

<div>
    <Switch />
</div>
```

#### 사용 가능한 레이아웃

Svelte 스타터 킷에는 "sidebar" 레이아웃과 "header" 레이아웃, 두 가지 기본 레이아웃이 있습니다. sidebar가 기본값이며, `resources/js/layouts/AppLayout.svelte`의 import 코드를 변경하여 header 레이아웃으로 전환할 수 있습니다:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.svelte'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.svelte'; // [tl! add]
```

#### 사이드바 변형

사이드바 레이아웃에는 기본 variant, "inset" variant, "floating" variant의 세 가지 변형이 있습니다. 원하는 variant로 변경하려면 `resources/js/components/AppSidebar.svelte`에서 수정합니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

#### 인증 페이지 레이아웃 변형

Svelte 스타터 킷에 포함된 인증 관련(로그인, 회원가입 등) 페이지의 레이아웃도 "simple", "card", "split" 중 선택할 수 있습니다.

변경하려면 `resources/js/layouts/AuthLayout.svelte`의 import 코드를 수정합니다:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.svelte'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.svelte'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 킷은 Inertia 2, Vue 3 Composition API, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/)로 구성되어 있습니다. 모든 스타터 킷이 그렇듯, 백엔드와 프론트엔드 코드는 전부 애플리케이션에 포함되어 자유로운 커스터마이즈가 가능합니다.

프론트엔드 코드는 대부분 `resources/js` 디렉터리에 있습니다. 스타일과 동작 모두 자유롭게 수정해 원하는 애플리케이션을 구축할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue composable, 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 타입 정의
```

shadcn-vue 컴포넌트 추가를 원한다면, [컴포넌트 선택](https://www.shadcn-vue.com) 후 아래 명령어를 실행하세요:

```shell
npx shadcn-vue@latest add switch
```

Switch 컴포넌트가 `resources/js/components/ui/Switch.vue`에 추가됩니다. 다음과 같이 임포트하여 사용할 수 있습니다:

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

#### 사용 가능한 레이아웃

Vue 스타터 킷에는 "sidebar" 레이아웃과 "header" 레이아웃, 두 가지 기본 레이아웃이 포함되어 있습니다. sidebar가 기본값이며, `resources/js/layouts/AppLayout.vue`의 import 부분을 변경하여 header 레이아웃으로 바꿀 수 있습니다:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

#### 사이드바 변형

사이드바 레이아웃에는 기본 variant, "inset" variant, "floating" variant의 세 가지 변형이 있습니다. 변경은 `resources/js/components/AppSidebar.vue`에서 직접 적용하면 됩니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

#### 인증 페이지 레이아웃 변형

Vue 스타터 킷의 로그인·회원가입 등 인증 페이지에도 "simple", "card", "split" 세 가지 레이아웃 변형이 있습니다.

변경하려면 `resources/js/layouts/AuthLayout.vue`의 import 코드를 수정하세요:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 킷은 Livewire 4, Tailwind, [Flux UI](https://fluxui.dev/)를 기반으로 합니다. 모든 스타터 킷과 마찬가지로 백엔드와 프론트엔드 코드는 애플리케이션 내에 존재하므로 자유롭게 커스터마이즈할 수 있습니다.

프론트엔드 코드는 대부분 `resources/views`에 위치하며, 다음과 같이 구성됩니다:

```text
resources/views
├── components            # 재사용 가능한 컴포넌트
├── flux                  # 커스터마이즈된 Flux 컴포넌트
├── layouts               # 애플리케이션 레이아웃
├── pages                 # Livewire 페이지
├── partials              # 재사용 가능한 Blade 부분(Partial)
├── dashboard.blade.php   # 인증 사용자 대시보드
├── welcome.blade.php     # 비회원 환영 페이지
```

#### 사용 가능한 레이아웃

Livewire 스타터 킷 역시 "sidebar"와 "header" 두 가지 레이아웃이 존재합니다. 기본값은 사이드바이며, `resources/views/layouts/app.blade.php`에서 사용하는 레이아웃을 변경할 수 있습니다. 아울러 주요 Flux 컴포넌트에 `container` 속성을 추가하세요:

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```

#### 인증 페이지 레이아웃 변형

Livewire 스타터 킷이 제공하는 인증 페이지(로그인, 회원가입 등) 역시 "simple", "card", "split" 중 하나로 설정할 수 있습니다.

`resources/views/layouts/auth.blade.php`에서 사용하는 레이아웃을 변경하면 됩니다:

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a name="authentication"></a>
## 인증 (Authentication)

모든 스타터 킷은 인증 처리를 위해 [Laravel Fortify](/docs/12.x/fortify)를 사용합니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 인증의 모든 라우트와 컨트롤러, 로직을 제공합니다.

Fortify는 애플리케이션의 `config/fortify.php` 설정 파일에 활성화된 기능을 기준으로 자동으로 다음 인증 라우트를 등록합니다:

| Route                              | Method | 설명                             |
| ---------------------------------- | ------ | --------------------------------- |
| `/login`                           | `GET`    | 로그인 폼 표시                    |
| `/login`                           | `POST`   | 사용자 인증                       |
| `/logout`                          | `POST`   | 사용자 로그아웃                   |
| `/register`                        | `GET`    | 회원가입 폼 표시                  |
| `/register`                        | `POST`   | 신규 사용자 생성                  |
| `/forgot-password`                 | `GET`    | 비밀번호 재설정 요청 폼 표시      |
| `/forgot-password`                 | `POST`   | 비밀번호 재설정 링크 전송         |
| `/reset-password/{token}`          | `GET`    | 비밀번호 재설정 폼 표시           |
| `/reset-password`                  | `POST`   | 비밀번호 업데이트                 |
| `/email/verify`                    | `GET`    | 이메일 인증 알림 표시             |
| `/email/verify/{id}/{hash}`        | `GET`    | 이메일 인증 처리                  |
| `/email/verification-notification` | `POST`   | 인증 이메일 재발송                |
| `/user/confirm-password`           | `GET`    | 비밀번호 재확인 폼                |
| `/user/confirm-password`           | `POST`   | 비밀번호 재확인 처리              |
| `/two-factor-challenge`            | `GET`    | 2단계 인증(2FA) 입력 폼           |
| `/two-factor-challenge`            | `POST`   | 2FA 코드 인증                     |

`php artisan route:list` Artisan 명령어를 통해 애플리케이션 내 등록된 모든 라우트를 확인할 수 있습니다.

<a name="enabling-and-disabling-features"></a>
### 기능 활성화 및 비활성화 (Enabling and Disabling Features)

애플리케이션의 `config/fortify.php` 설정 파일에서 Fortify 기능의 활성/비활성 여부를 설정할 수 있습니다:

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

특정 기능을 비활성화하려면 해당 엔트리를 `features` 배열에서 주석 처리하거나 삭제하면 됩니다. 예를 들어, `Features::registration()`을 제거하면 공개 회원가입이 비활성화됩니다.

[React](#react), [Svelte](#svelte), [Vue](#vue) 스타터 킷을 사용할 경우, 비활성화한 기능과 관련된 프론트엔드 코드 내 라우트 참조도 제거해야 합니다. 예를 들어, 이메일 인증을 비활성화했다면 관련 라우트 import 및 참조를 React, Svelte 또는 Vue 컴포넌트에서 제거해야 합니다. 이는 해당 스타터 킷이 타입-안전 라우팅을 위해 Wayfinder를 사용하며, 빌드 시점에 라우트 정의가 생성되기 때문입니다. 더 이상 존재하지 않는 라우트를 참조하면 빌드가 실패합니다.

<a name="customizing-actions"></a>
### 사용자 생성 및 비밀번호 재설정 커스터마이즈 (Customizing User Creation and Password Reset)

사용자가 회원가입 또는 비밀번호 재설정을 할 때, Fortify는 애플리케이션의 `app/Actions/Fortify` 디렉터리에 위치한 액션 클래스를 실행합니다:

| 파일                          | 설명                                     |
| ----------------------------- | ---------------------------------------- |
| `CreateNewUser.php`           | 신규 사용자 생성 및 유효성 검증          |
| `ResetUserPassword.php`       | 사용자 비밀번호 업데이트 및 유효성 검증  |
| `PasswordValidationRules.php` | 비밀번호 유효성 규칙 정의                |

예를 들어, 가입 로직을 커스터마이즈하려면 `CreateNewUser` 액션을 수정하세요:

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
### 2단계 인증 (Two-Factor Authentication)

스타터 킷은 2단계 인증(2FA)이 내장되어 있어 사용자들이 TOTP 호환 인증 앱으로 자신의 계정을 보다 안전하게 보호할 수 있습니다. 2FA는 기본적으로 `config/fortify.php` 파일의 `Features::twoFactorAuthentication()`로 활성화되어 있습니다.

`confirm` 옵션을 지정하면, 2FA 완전 활성화 전에 사용자가 코드를 입력해 검증해야 하며, `confirmPassword`가 true일 경우 2FA 활성화/비활성화 전에 비밀번호 재확인을 요구합니다. 자세한 내용은 [Fortify의 2단계 인증 문서](/docs/12.x/fortify#two-factor-authentication)를 참고하세요.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

속도 제한은 무차별 대입 공격이나 반복적인 로그인 시도로 인증 엔드포인트가 과도하게 사용되는 것을 방지합니다. Fortify의 속도 제한 동작은 애플리케이션의 `FortifyServiceProvider`에서 커스터마이즈할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="workos"></a>
## WorkOS AuthKit 인증 (WorkOS AuthKit Authentication)

기본적으로 React, Svelte, Vue, Livewire 스타터 킷은 모두 Laravel의 내장 인증 시스템을 사용해 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 기능을 제공합니다. 추가로, [WorkOS AuthKit](https://authkit.com)이 적용된 각 스타터 킷 버전도 제공되며, 아래 기능이 포함됩니다:

<div class="content-list" markdown="1">

- 소셜 인증(구글, 마이크로소프트, 깃허브, 애플)
- 패스키 인증
- 이메일 기반 매직 인증(Magic Auth)
- SSO(싱글 사인온)

</div>

WorkOS를 인증 공급자로 사용하려면 [WorkOS 계정이 필요](https://workos.com)합니다. WorkOS는 월 100만 명까지 무료로 인증을 제공합니다.

WorkOS AuthKit을 인증 공급자로 사용하고 싶다면, `laravel new` 명령어로 새 스타터 킷 기반 앱을 만들 때 WorkOS 옵션을 선택하세요.

### WorkOS 스타터 킷 설정하기

WorkOS 기반 스타터 킷으로 새 애플리케이션을 만든 후, 애플리케이션 `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 이 값들은 WorkOS 대시보드에서 제공된 정보와 일치해야 합니다:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한, WorkOS 대시보드에서 애플리케이션 홈페이지 URL도 설정해야 하며, 로그아웃 후 사용자가 리디렉션될 주소입니다.

#### AuthKit 인증 방식 설정

WorkOS 기반 스타터 킷을 사용할 때, 애플리케이션의 WorkOS AuthKit 설정에서 "이메일 + 비밀번호" 인증을 비활성화하는 것이 권장됩니다. 이렇게 하면 사용자는 소셜 인증, 패스키, 매직 인증, SSO 등으로만 인증할 수 있으며, 애플리케이션이 직접 비밀번호를 관리하지 않아도 됩니다.

#### AuthKit 세션 타임아웃 설정

또한, WorkOS AuthKit 세션 비활성 타임아웃을 Laravel 애플리케이션의 세션 타임아웃(일반적으로 2시간)과 맞춰 설정하는 것이 좋습니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React, Svelte, Vue 스타터 킷은 Inertia의 [서버 사이드 렌더링(SSR)](https://inertiajs.com/server-side-rendering) 기능과 호환됩니다. Inertia SSR 호환 번들을 빌드하려면 다음 명령어를 사용하세요:

```shell
npm run build:ssr
```

추가로, `composer dev:ssr` 명령도 준비되어 있습니다. 이 명령은 SSR 호환 번들 빌드 후 Laravel 개발 서버와 Inertia SSR 서버를 실행해 SSR 환경에서 애플리케이션을 로컬에서 테스트할 수 있게 해줍니다:

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지 스타터 킷 (Community Maintained Starter Kits)

Laravel 설치기를 사용할 때, Packagist에 등록된 어떤 커뮤니티 스타터 킷이든 `--using` 플래그로 지정할 수 있습니다:

```shell
laravel new my-app --using=example/starter-kit
```

#### 스타터 킷 만들기

자신이 만든 스타터 킷을 다른 사용자도 사용할 수 있도록 하려면, [Packagist](https://packagist.org)에 공개해야 합니다. 스타터 킷에 필요한 환경 변수는 `.env.example` 파일에 정의하고, 설치 후 실행할 명령어는 `composer.json`의 `post-create-project-cmd` 배열에 명시하세요.

<a name="faqs"></a>
### 자주 묻는 질문 (Frequently Asked Questions)

<a name="faq-upgrade"></a>
#### 업그레이드는 어떻게 하나요?

각 스타터 킷은 애플리케이션 시작에 충분한 기반을 제공합니다. 전체 코드를 직접 소유하므로 자유롭게 변경, 커스터마이즈, 확장이 가능합니다. 단, 스타터 킷 자체를 별도로 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증은 어떻게 활성화하나요?

이메일 인증을 활성화하려면, `App/Models/User.php` 모델에서 `MustVerifyEmail` import 주석을 해제하고, 모델이 `MustVerifyEmail` 인터페이스를 구현하는지 확인하세요:

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

회원가입 후, 사용자는 인증 이메일을 받게 됩니다. 특정 라우트에 대해 이메일 인증이 완료된 사용자만 접근하게 하려면, 해당 라우트에 `verified` 미들웨어를 추가합니다:

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 기반 스타터 킷을 사용하는 경우 이메일 인증이 필수가 아닙니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 어떻게 수정할 수 있나요?

애플리케이션 브랜드에 맞게 이메일 템플릿을 커스터마이즈할 수 있습니다. 아래 명령어로 이메일 뷰를 애플리케이션에 퍼블리시하면, 원하는 대로 수정할 수 있습니다:

```
php artisan vendor:publish --tag=laravel-mail
```

이 명령어를 실행하면 `resources/views/vendor/mail` 디렉터리에 여러 파일이 생성됩니다. 이들 파일과 `resources/views/vendor/mail/themes/default.css` 파일을 수정해서 이메일 템플릿의 스타일과 구조를 바꿀 수 있습니다.
