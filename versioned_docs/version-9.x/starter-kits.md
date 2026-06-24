<!-- # Starter Kits -->
# Starter Kits

- [Introduction](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [Installation](#laravel-breeze-installation)
    - [Breeze & Blade](#breeze-and-blade)
    - [Breeze & React / Vue](#breeze-and-inertia)
    - [Breeze & Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- To give you a head start building your new Laravel application, we are happy to offer authentication and application starter kits. These kits automatically scaffold your application with the routes, controllers, and views you need to register and authenticate your application's users. -->
새로운 Laravel 애플리케이션을 빠르게 시작할 수 있도록, 인증과 애플리케이션 초기 구성을 도와주는 스타터 키트를 제공합니다. 이 키트들은 회원가입, 인증에 필요한 라우트, 컨트롤러, 뷰를 자동으로 만들어 주기 때문에, 사용자 인증 기능이 필요한 애플리케이션의 뼈대를 손쉽게 구성할 수 있습니다.

<!-- While you are welcome to use these starter kits, they are not required. You are free to build your own application from the ground up by simply installing a fresh copy of Laravel. Either way, we know you will build something great! -->
이러한 스타터 키트를 꼭 사용해야 하는 것은 아닙니다. 원한다면 Laravel을 새로 설치한 뒤 직접 처음부터 필요한 기능을 구축해도 됩니다. 어떤 방식을 사용하더라도, 여러분이 멋진 서비스를 만들어낼 것이라 믿습니다!

<a name="laravel-breeze"></a>
<!-- ## Laravel Breeze -->
## Laravel Breeze

<!-- [Laravel Breeze](https://github.com/laravel/breeze) is a minimal, simple implementation of all of Laravel's [authentication features](/docs/9.x/authentication), including login, registration, password reset, email verification, and password confirmation. In addition, Breeze includes a simple "profile" page where the user may update their name, email address, and password. -->
[Laravel Breeze](https://github.com/laravel/breeze)는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel의 [authentication features](/docs/9.x/authentication)을 가장 단순하게 구현해둔 미니멀한 스타터 키트입니다. 또한, Breeze에는 사용자가 이름, 이메일 주소, 비밀번호를 수정할 수 있는 간단한 "프로필" 페이지도 포함되어 있습니다.

<!-- Laravel Breeze's default view layer is made up of simple [Blade templates](/docs/9.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). Or, Breeze can scaffold your application using Vue or React and [Inertia](https://inertiajs.com). -->
Laravel Breeze의 기본 뷰 레이어는 [Blade templates](https://tailwindcss.com)로 스타일링된 심플한 [Tailwind CSS](/docs/9.x/blade)으로 구성되어 있습니다. 상황에 따라 Vue, React, 그리고 [Inertia](https://inertiajs.com)를 활용한 옵션도 지원합니다.

<!-- Breeze provides a wonderful starting point for beginning a fresh Laravel application and is also a great choice for projects that plan to take their Blade templates to the next level with [Laravel Livewire](https://laravel-livewire.com). -->
Breeze는 새 프로젝트를 시작할 때 훌륭한 출발점이 되어주며, 특히 [Laravel Livewire](https://laravel-livewire.com)와 결합해 기존 Blade 템플릿을 더 진화시키고자 하는 프로젝트에도 잘 어울립니다.

<!-- <img src="https://laravel.com/img/docs/breeze-register.png"/> -->
<img src="https://laravel.com/img/docs/breeze-register.png" />

<!-- #### Laravel Bootcamp -->
#### Laravel Bootcamp

<!-- If you're new to Laravel, feel free to jump into the [Laravel Bootcamp](https://bootcamp.laravel.com). The Laravel Bootcamp will walk you through building your first Laravel application using Breeze. It's a great way to get a tour of everything that Laravel and Breeze have to offer. -->
Laravel이 처음이라면 [Laravel Bootcamp](https://bootcamp.laravel.com)를 시작해 보세요. 이 Bootcamp는 Breeze를 사용해 첫 번째 Laravel 애플리케이션을 만드는 전 과정을 친절하게 안내합니다. Laravel과 Breeze가 제공하는 다양한 기능을 둘러보기에도 아주 좋은 방법입니다.

<a name="laravel-breeze-installation"></a>
<!-- ### Installation -->
### Installation

<!-- First, you should [create a new Laravel application](/docs/9.x/installation), configure your database, and run your [database migrations](/docs/9.x/migrations). Once you have created a new Laravel application, you may install Laravel Breeze using Composer: -->
먼저 [create a new Laravel application](/docs/9.x/installation)을 생성하고, 데이터베이스를 설정한 뒤 [database migrations](/docs/9.x/migrations)을 실행해 주세요. 애플리케이션 준비가 완료되면, Composer로 Laravel Breeze를 설치할 수 있습니다.

```shell
composer require laravel/breeze --dev
```

<!-- Once Breeze is installed, you may scaffold your application using one of the Breeze "stacks" discussed in the documentation below. -->
Breeze가 설치되면, 아래 설명에서 소개하는 Breeze의 "스택(stack)" 중 하나를 선택해 애플리케이션 구조를 자동으로 만들어줄 수 있습니다.

<a name="breeze-and-blade"></a>
<!-- ### Breeze & Blade -->
### Breeze & Blade

<!-- After Composer has installed the Laravel Breeze package, you may run the `breeze:install` Artisan command. This command publishes the authentication views, routes, controllers, and other resources to your application. Laravel Breeze publishes all of its code to your application so that you have full control and visibility over its features and implementation. -->
Composer로 Laravel Breeze 패키지를 설치한 후에는 `breeze:install` 아티즌 명령어를 실행할 수 있습니다. 이 명령어는 인증에 필요한 뷰, 라우트, 컨트롤러 등 여러 리소스를 애플리케이션에 추가합니다. Laravel Breeze는 자신의 모든 코드를 여러분의 애플리케이션에 직접 복사해두기 때문에, 필요에 따라 언제든 기능을 자유롭게 수정하거나 확인할 수 있습니다.

<!-- The default Breeze "stack" is the Blade stack, which utilizes simple [Blade templates](/docs/9.x/blade) to render your application's frontend. The Blade stack may be installed by invoking the `breeze:install` command with no other additional arguments. After Breeze's scaffolding is installed, you should also compile your application's frontend assets: -->
Breeze의 기본 "스택"은 Blade 스택입니다. 이 스택은 심플한 [Blade templates](/docs/9.x/blade)으로 프론트엔드를 구성합니다. 별도의 인수 없이 `breeze:install` 명령어만 실행하면 Blade 스택이 설치됩니다. Breeze의 구조가 완성되면, 프론트엔드 자산도 컴파일해주어야 합니다.

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<!-- Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file. -->
이제 웹 브라우저에서 애플리케이션의 `/login` 또는 `/register` URL로 접속해 볼 수 있습니다. 모든 Breeze 인증 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

<a name="dark-mode"></a>
<!-- #### Dark Mode -->
#### Dark Mode

<!-- If you would like Breeze to include "dark mode" support when scaffolding your application's frontend, simply provide the `--dark` directive when executing the `breeze:install` command: -->
프론트엔드에 "다크 모드" 기능까지 함께 적용하고 싶다면, `breeze:install` 명령어에 `--dark` 옵션을 추가하면 됩니다.

```shell
php artisan breeze:install --dark
```

> [!NOTE]
> 애플리케이션의 CSS 및 JavaScript 자산 컴파일 방법이 궁금하다면 Laravel의 [Vite documentation](/docs/9.x/vite#running-vite)를 참고해 주세요.

<a name="breeze-and-inertia"></a>
<!-- ### Breeze & React / Vue -->
### Breeze & React / Vue

<!-- Laravel Breeze also offers React and Vue scaffolding via an [Inertia](https://inertiajs.com) frontend implementation. Inertia allows you to build modern, single-page React and Vue applications using classic server-side routing and controllers. -->
Laravel Breeze는 [Inertia](https://inertiajs.com)를 활용한 React, Vue 기반 프론트엔드 구성도 지원합니다. Inertia를 사용하면, 서버 사이드 라우팅과 컨트롤러의 장점은 그대로 누리면서 React나 Vue로 현대적인 싱글 페이지 애플리케이션을 만들 수 있습니다.

<!-- Inertia lets you enjoy the frontend power of React and Vue combined with the incredible backend productivity of Laravel and lightning-fast [Vite](https://vitejs.dev) compilation. To use an Inertia stack, specify `vue` or `react` as your desired stack when executing the `breeze:install` Artisan command. After Breeze's scaffolding is installed, you should also compile your application's frontend assets: -->
Inertia를 활용하면 React, Vue의 강력한 프론트엔드는 물론, Laravel의 뛰어난 생산성과 [Vite](https://vitejs.dev)로 번개처럼 빠른 빌드 환경을 모두 경험할 수 있습니다. Inertia 스택을 사용하려면, `breeze:install` 아티즌 명령어 실행 시 원하는 스택으로 `vue` 또는 `react`를 지정하면 됩니다. Breeze의 구조가 완성되면 프론트엔드 자산도 꼭 빌드해 주세요.

```shell
php artisan breeze:install vue

# Or...

php artisan breeze:install react

php artisan migrate
npm install
npm run dev
```

<!-- Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file. -->
이제 웹 브라우저에서 애플리케이션의 `/login` 또는 `/register` URL로 접속해 볼 수 있습니다. 모든 Breeze 인증 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

<a name="server-side-rendering"></a>
<!-- #### Server-Side Rendering -->
#### Server-Side Rendering

<!-- If you would like Breeze to scaffold support for [Inertia SSR](https://inertiajs.com/server-side-rendering), you may provide the `ssr` option when invoking the `breeze:install` command: -->
[Inertia SSR](https://inertiajs.com/server-side-rendering) 기능까지 포함해 구성하고 싶다면, `breeze:install` 명령어에 `ssr` 옵션을 추가해 실행하세요.

```shell
php artisan breeze:install vue --ssr
php artisan breeze:install react --ssr
```

<a name="breeze-and-next"></a>
<!-- ### Breeze & Next.js / API -->
### Breeze & Next.js / API

<!-- Laravel Breeze can also scaffold an authentication API that is ready to authenticate modern JavaScript applications such as those powered by [Next](https://nextjs.org), [Nuxt](https://nuxt.com), and others. To get started, specify the `api` stack as your desired stack when executing the `breeze:install` Artisan command: -->
Laravel Breeze는 [Next](https://nextjs.org), [Nuxt](https://nuxt.com) 등 최신 자바스크립트 프레임워크를 위한 인증 API도 쉽게 만들 수 있도록 지원합니다. 시작하려면, 원하는 스택으로 `api`를 지정해서 `breeze:install` 아티즌 명령어를 실행하세요.

```shell
php artisan breeze:install api

php artisan migrate
```

<!-- During installation, Breeze will add a `FRONTEND_URL` environment variable to your application's `.env` file. This URL should be the URL of your JavaScript application. This will typically be `http://localhost:3000` during local development. In addition, you should ensure that your `APP_URL` is set to `http://localhost:8000`, which is the default URL used by the `serve` Artisan command. -->
설치 과정에서 Breeze가 애플리케이션의 `.env` 파일에 `FRONTEND_URL` 환경 변수를 추가해줍니다. 이 값에는 자바스크립트 프론트엔드 앱의 주소를 입력하면 됩니다. 일반적으로 로컬 개발 환경에서는 `http://localhost:3000`이 사용됩니다. 또한 `APP_URL` 환경 변수는 `serve` Artisan 명령어가 사용하는 기본 값인 `http://localhost:8000`으로 잘 설정되어 있는지 확인해 주세요.

<a name="next-reference-implementation"></a>
<!-- #### Next.js Reference Implementation -->
#### Next.js Reference Implementation

<!-- Finally, you are ready to pair this backend with the frontend of your choice. A Next reference implementation of the Breeze frontend is [available on GitHub](https://github.com/laravel/breeze-next). This frontend is maintained by Laravel and contains the same user interface as the traditional Blade and Inertia stacks provided by Breeze. -->
모든 설정이 끝나면, 원하는 프론트엔드와 이 백엔드를 연결할 수 있습니다. Breeze 프론트엔드의 Next 참고 구현체는 [available on GitHub](https://github.com/laravel/breeze-next). 이 프론트엔드는 Laravel에서 공식적으로 관리하며, Breeze의 Blade, Inertia 스택과 동일한 사용자 인터페이스를 제공합니다.

<a name="laravel-jetstream"></a>
<!-- ## Laravel Jetstream -->
## Laravel Jetstream

<!-- While Laravel Breeze provides a simple and minimal starting point for building a Laravel application, Jetstream augments that functionality with more robust features and additional frontend technology stacks. **For those brand new to Laravel, we recommend learning the ropes with Laravel Breeze before graduating to Laravel Jetstream.** -->
Laravel Breeze가 가장 단순한 출발점을 제공한다면, Jetstream은 여기에 더 다양한 기능과 프론트엔드 선택지를 추가합니다. **Laravel을 이제 막 시작하는 분들께는 Breeze로 기본기를 먼저 익히신 후, Jetstream을 사용해보는 것을 추천합니다.**

<!-- Jetstream provides a beautifully designed application scaffolding for Laravel and includes login, registration, email verification, two-factor authentication, session management, API support via Laravel Sanctum, and optional team management. Jetstream is designed using [Tailwind CSS](https://tailwindcss.com) and offers your choice of [Livewire](https://laravel-livewire.com) or [Inertia](https://inertiajs.com) driven frontend scaffolding. -->
Jetstream은 아름답게 디자인된 애플리케이션 구조를 제공하며, 로그인, 회원가입, 이메일 인증, 2단계 인증, 세션 관리, Laravel Sanctum을 통한 API 지원, 필요하다면 팀 관리 기능까지 갖추고 있습니다. Jetstream은 [Tailwind CSS](https://tailwindcss.com)로 디자인되었고, 프론트엔드로는 [Livewire](https://laravel-livewire.com) 혹은 [Inertia](https://inertiajs.com) 중에서 선택할 수 있습니다.

<!-- Complete documentation for installing Laravel Jetstream can be found within the [official Jetstream documentation](https://jetstream.laravel.com/introduction.html). -->
Laravel Jetstream 설치에 관한 모든 공식 문서는 [official Jetstream documentation](https://jetstream.laravel.com/introduction.html)에서 확인하실 수 있습니다.
