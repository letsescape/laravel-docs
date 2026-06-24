<!-- # Starter Kits -->
# Starter Kits

- [Introduction](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [Installation](#laravel-breeze-installation)
    - [Breeze & Inertia](#breeze-and-inertia)
    - [Breeze & Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- To give you a head start building your new Laravel application, we are happy to offer authentication and application starter kits. These kits automatically scaffold your application with the routes, controllers, and views you need to register and authenticate your application's users. -->
새로운 Laravel 애플리케이션을 개발할 때 더 빠르게 시작할 수 있도록, 인증 및 애플리케이션 스타터 키트를 제공합니다. 이 키트는 회원 등록과 인증에 필요한 라우트, 컨트롤러, 뷰를 자동으로 생성해주어, 빠르게 기본 골격을 갖춘 애플리케이션을 만들 수 있습니다.

<!-- While you are welcome to use these starter kits, they are not required. You are free to build your own application from the ground up by simply installing a fresh copy of Laravel. Either way, we know you will build something great! -->
이러한 스타터 키트를 반드시 사용해야 하는 것은 아닙니다. 원한다면 Laravel을 새롭게 설치하여 처음부터 직접 애플리케이션을 구성할 수도 있습니다. 어떤 방식을 택하든 멋진 결과를 만들어낼 수 있을 것입니다!

<a name="laravel-breeze"></a>
<!-- ## Laravel Breeze -->
## Laravel Breeze

<!-- [Laravel Breeze](https://github.com/laravel/breeze) is a minimal, simple implementation of all of Laravel's [authentication features](/docs/8.x/authentication), including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's default view layer is made up of simple [Blade templates](/docs/8.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). -->
[Laravel Breeze](https://github.com/laravel/breeze)는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel의 모든 [authentication features](/docs/8.x/authentication)을 간결하고 단순하게 구현한 스타터 키트입니다. Breeze의 기본 뷰 레이어는 [Blade templates](https://tailwindcss.com)로 스타일링된 간단한 [Tailwind CSS](/docs/8.x/blade)으로 구성되어 있습니다.

<!-- Breeze provides a wonderful starting point for beginning a fresh Laravel application and is also great choice for projects that plan to take their Blade templates to the next level with [Laravel Livewire](https://laravel-livewire.com). -->
Breeze는 새로운 Laravel 애플리케이션을 시작할 때 훌륭한 출발점이 되어주며, [Laravel Livewire](https://laravel-livewire.com)와 함께 Blade 템플릿을 한 단계 더 발전시키려는 프로젝트에도 잘 어울리는 선택입니다.

<a name="laravel-breeze-installation"></a>
<!-- ### Installation -->
### Installation

<!-- First, you should [create a new Laravel application](/docs/8.x/installation), configure your database, and run your [database migrations](/docs/8.x/migrations): -->
먼저 [create a new Laravel application](/docs/8.x/installation)한 뒤, 데이터베이스를 설정하고 [database migrations](/docs/8.x/migrations)을 실행합니다.

```bash
curl -s https://laravel.build/example-app | bash

cd example-app

php artisan migrate
```

<!-- Once you have created a new Laravel application, you may install Laravel Breeze using Composer: -->
새 프로젝트가 준비되었다면, Composer를 사용해 Laravel Breeze를 설치합니다.

```bash
composer require laravel/breeze:1.9.2
```

<!-- After Composer has installed the Laravel Breeze package, you may run the `breeze:install` Artisan command. This command publishes the authentication views, routes, controllers, and other resources to your application. Laravel Breeze publishes all of its code to your application so that you have full control and visibility over its features and implementation. After Breeze is installed, you should also compile your assets so that your application's CSS file is available: -->
Composer로 Laravel Breeze 패키지 설치가 완료되면, `breeze:install` 아티즌 명령어를 실행할 수 있습니다. 이 명령어는 인증과 관련된 뷰, 라우트, 컨트롤러 등 여러 리소스를 프로젝트에 추가합니다. Breeze는 모든 코드를 프로젝트 내부에 직접 배포하기 때문에, 개발자가 기능 구현과 동작을 완전히 직접 제어하고 확인할 수 있습니다. 설치가 끝났다면, CSS 파일이 정상적으로 적용될 수 있도록 에셋도 빌드해야 합니다.

```nothing
php artisan breeze:install

npm install
npm run dev
php artisan migrate
```

<!-- Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file. -->
이제 웹 브라우저에서 애플리케이션의 `/login` 또는 `/register` 경로로 이동해볼 수 있습니다. Breeze에서 사용하는 모든 인증 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

> [!TIP]
> 애플리케이션의 CSS와 자바스크립트 번들링에 대해 더 자세히 알고 싶다면 [Laravel Mix documentation](/docs/8.x/mix#running-mix)를 참고하세요.

<a name="breeze-and-inertia"></a>
<!-- ### Breeze & Inertia -->
### Breeze & Inertia

<!-- Laravel Breeze also offers an [Inertia.js](https://inertiajs.com) frontend implementation powered by Vue or React. To use an Inertia stack, specify `vue` or `react` as your desired stack when executing the `breeze:install` Artisan command: -->
Laravel Breeze는 [Inertia.js](https://inertiajs.com)를 활용한 프론트엔드 스택도 제공합니다. 뷰(Vue) 또는 리액트(React)를 선택해 사용할 수 있습니다. 이너시아 스택을 적용하려면, `breeze:install` 아티즌 명령어를 실행할 때 원하는 스택 이름(`vue` 또는 `react`)을 함께 입력하면 됩니다.

```nothing
php artisan breeze:install vue

// Or...

php artisan breeze:install react

npm install
npm run dev
php artisan migrate
```

<a name="breeze-and-next"></a>
<!-- ### Breeze & Next.js / API -->
### Breeze & Next.js / API

<!-- Laravel Breeze can also scaffold an authentication API that is ready to authenticate modern JavaScript applications such as those powered by [Next](https://nextjs.org), [Nuxt](https://nuxt.com), and others. To get started, specify the `api` stack as your desired stack when executing the `breeze:install` Artisan command: -->
Laravel Breeze는 최신 자바스크립트 애플리케이션(예: [Next](https://nextjs.org), [Nuxt](https://nuxt.com) 등)에서 사용하기에 적합한 인증 API도 자동으로 구성할 수 있습니다. 시작하려면 `breeze:install` 아티즌 명령어 실행 시 `api` 스택을 지정해주면 됩니다.

```nothing
php artisan breeze:install api

php artisan migrate
```

<!-- During installation, Breeze will add a `FRONTEND_URL` environment variable to your application's `.env` file. This URL should be the URL of your JavaScript application. This will typically be `http://localhost:3000` during local development. -->
설치 과정에서 Breeze는 `.env` 파일에 `FRONTEND_URL` 환경 변수를 추가합니다. 이 값은 자바스크립트 프론트엔드 애플리케이션의 URL로 설정해야 합니다. 일반적으로 개발 환경에서는 `http://localhost:3000` 등으로 지정합니다.

<a name="next-reference-implementation"></a>
<!-- #### Next.js Reference Implementation -->
#### Next.js Reference Implementation

<!-- Finally, you are ready to pair this backend with the frontend of your choice. A Next reference implementation of the Breeze frontend is [available on GitHub](https://github.com/laravel/breeze-next). This frontend is maintained by Laravel and contains the same user interface as the traditional Blade and Inertia stacks provided by Breeze. -->
이제 백엔드를 다양한 프론트엔드와 연동할 준비가 끝났습니다. Breeze 프론트엔드의 Next.js 참고 구현체는 [available on GitHub](https://github.com/laravel/breeze-next). 이 프론트엔드는 Laravel에서 공식적으로 관리하며, Breeze의 기존 Blade 및 이너시아 스택과 동일한 사용자 인터페이스를 제공합니다.

<a name="laravel-jetstream"></a>
<!-- ## Laravel Jetstream -->
## Laravel Jetstream

<!-- While Laravel Breeze provides a simple and minimal starting point for building a Laravel application, Jetstream augments that functionality with more robust features and additional frontend technology stacks. **For those brand new to Laravel, we recommend learning the ropes with Laravel Breeze before graduating to Laravel Jetstream.** -->
Laravel Breeze가 단순하고 미니멀한 시작점을 제공하는 반면, Jetstream은 보다 강력한 기능과 추가 프론트엔드 기술 스택을 함께 제공합니다. **Laravel을 처음 접하는 분이라면, 먼저 Laravel Breeze로 기본 구조와 개념을 익히고, 그 다음에 Laravel Jetstream을 활용하는 것을 추천합니다.**

<!-- Jetstream provides a beautifully designed application scaffolding for Laravel and includes login, registration, email verification, two-factor authentication, session management, API support via Laravel Sanctum, and optional team management. Jetstream is designed using [Tailwind CSS](https://tailwindcss.com) and offers your choice of [Livewire](https://laravel-livewire.com) or [Inertia.js](https://inertiajs.com) driven frontend scaffolding. -->
Jetstream은 미려하게 디자인된 애플리케이션 스캐폴딩을 제공하며, 로그인, 회원가입, 이메일 인증, 2단계 인증, 세션 관리, Laravel Sanctum을 통한 API 지원, 팀 관리(선택 사항) 등의 기능을 지원합니다. [Tailwind CSS](https://tailwindcss.com)로 디자인되어 있으며, [Livewire](https://laravel-livewire.com) 또는 [Inertia.js](https://inertiajs.com) 중 원하는 프론트엔드 스캐폴딩 방식을 선택할 수 있습니다.

<!-- Complete documentation for installing Laravel Jetstream can be found within the [official Jetstream documentation](https://jetstream.laravel.com/introduction.html). -->
Laravel Jetstream의 설치 방법에 대한 전체 공식 문서는 [official Jetstream documentation](https://jetstream.laravel.com/introduction.html)에서 확인하실 수 있습니다.
