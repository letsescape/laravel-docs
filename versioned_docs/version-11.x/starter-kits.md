<!-- # Starter Kits -->
# Starter Kits

- [Introduction](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [Installation](#laravel-breeze-installation)
    - [Breeze and Blade](#breeze-and-blade)
    - [Breeze and Livewire](#breeze-and-livewire)
    - [Breeze and React / Vue](#breeze-and-inertia)
    - [Breeze and Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- To give you a head start building your new Laravel application, we are happy to offer authentication and application starter kits. These kits automatically scaffold your application with the routes, controllers, and views you need to register and authenticate your application's users. -->
새로운 Laravel 애플리케이션을 빠르게 시작할 수 있도록, Laravel에서는 인증과 애플리케이션 스타터 키트를 제공합니다. 이 스타터 키트는 애플리케이션에서 사용자 등록 및 인증에 필요한 라우트, 컨트롤러, 뷰 등을 자동으로 만들어줍니다.

<!-- While you are welcome to use these starter kits, they are not required. You are free to build your own application from the ground up by simply installing a fresh copy of Laravel. Either way, we know you will build something great! -->
이러한 스타터 키트의 사용은 필수가 아니며, 원하신다면 Laravel을 처음부터 설치하여 직접 애플리케이션을 만들어갈 수도 있습니다. 어떤 방식을 선택하셔도 멋진 결과물을 만들 수 있을 것이라 믿습니다!

<a name="laravel-breeze"></a>
<!-- ## Laravel Breeze -->
## Laravel Breeze

<!-- [Laravel Breeze](https://github.com/laravel/breeze) is a minimal, simple implementation of all of Laravel's [authentication features](/docs/11.x/authentication), including login, registration, password reset, email verification, and password confirmation. In addition, Breeze includes a simple "profile" page where the user may update their name, email address, and password. -->
[Laravel Breeze](https://github.com/laravel/breeze)는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel의 [authentication features](/docs/11.x/authentication)을 최소한의 간단한 구현으로 제공합니다. 또한 Breeze에는 사용자가 이름, 이메일, 비밀번호를 업데이트할 수 있는 "프로필" 페이지도 포함되어 있습니다.

<!-- Laravel Breeze's default view layer is made up of simple [Blade templates](/docs/11.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). Additionally, Breeze provides scaffolding options based on [Livewire](https://livewire.laravel.com) or [Inertia](https://inertiajs.com), with the choice of using Vue or React for the Inertia-based scaffolding. -->
Laravel Breeze의 기본 뷰 레이어는 [Blade templates](/docs/11.x/blade)과 [Tailwind CSS](https://tailwindcss.com)로 구성되어 있습니다. 추가로, [Livewire](https://livewire.laravel.com) 또는 [Inertia](https://inertiajs.com)를 기반으로 한 스캐폴딩 방식도 제공하며, Inertia 기반의 경우 Vue 또는 React 중 원하는 것을 선택할 수 있습니다.

<!-- <img src="https://laravel.com/img/docs/breeze-register.png"/> -->
<img src="https://laravel.com/img/docs/breeze-register.png" />

<!-- #### Laravel Bootcamp -->
#### Laravel Bootcamp

<!-- If you're new to Laravel, feel free to jump into the [Laravel Bootcamp](https://bootcamp.laravel.com). The Laravel Bootcamp will walk you through building your first Laravel application using Breeze. It's a great way to get a tour of everything that Laravel and Breeze have to offer. -->
Laravel을 처음 접하시는 분이라면, [Laravel Bootcamp](https://bootcamp.laravel.com)에 참여해 보시길 권장합니다. Laravel Bootcamp에서는 Breeze를 활용하여 Laravel 애플리케이션을 처음부터 만들어 보는 과정을 친절히 안내해줍니다. 이를 통해 Laravel과 Breeze가 제공하는 다양한 기능을 짧은 시간 안에 경험할 수 있습니다.

<a name="laravel-breeze-installation"></a>
<!-- ### Installation -->
### Installation

<!-- First, you should [create a new Laravel application](/docs/11.x/installation). If you create your application using the [Laravel installer](/docs/11.x/installation#creating-a-laravel-project), you will be prompted to install Laravel Breeze during the installation process. Otherwise, you will need to follow the manual installation instructions below. -->
먼저, [create a new Laravel application](/docs/11.x/installation)해야 합니다. [Laravel installer](/docs/11.x/installation#creating-a-laravel-project)로 애플리케이션을 생성하면 설치 과정에서 Laravel Breeze 설치 여부를 묻는 안내가 표시됩니다. 만약 다른 방식으로 애플리케이션을 만들었다면, 아래의 수동 설치 방법을 따라야 합니다.

<!-- If you have already created a new Laravel application without a starter kit, you may manually install Laravel Breeze using Composer: -->
이미 스타터 키트 없이 Laravel 애플리케이션을 생성했다면, Composer를 이용해 Laravel Breeze를 직접 설치할 수 있습니다.

```shell
composer require laravel/breeze --dev
```

<!-- After Composer has installed the Laravel Breeze package, you should run the `breeze:install` Artisan command. This command publishes the authentication views, routes, controllers, and other resources to your application. Laravel Breeze publishes all of its code to your application so that you have full control and visibility over its features and implementation. -->
Composer로 Laravel Breeze 패키지 설치를 마친 후, `breeze:install` 아티즌 명령어를 실행해야 합니다. 이 명령어는 인증 관련 뷰, 라우트, 컨트롤러 등 필요한 자원들을 애플리케이션 내에 복사합니다. Breeze는 모든 코드를 애플리케이션 내로 직접 복사하므로, 각 기능의 구현과 동작 방식을 직접 확인하고 자유롭게 수정할 수 있습니다.

<!-- The `breeze:install` command will prompt you for your preferred frontend stack and testing framework: -->
`breeze:install` 명령어를 실행하면 프론트엔드 스택과 테스트 프레임워크에 대한 선호도를 선택할 수 있도록 안내가 나타납니다.

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<a name="breeze-and-blade"></a>
<!-- ### Breeze and Blade -->
### Breeze and Blade

<!-- The default Breeze "stack" is the Blade stack, which utilizes simple [Blade templates](/docs/11.x/blade) to render your application's frontend. The Blade stack may be installed by invoking the `breeze:install` command with no other additional arguments and selecting the Blade frontend stack. After Breeze's scaffolding is installed, you should also compile your application's frontend assets: -->
Breeze의 기본 "스택"은 Blade 스택입니다. 이 스택은 직관적이고 간단한 [Blade templates](/docs/11.x/blade)을 사용해 애플리케이션의 프론트엔드를 렌더링합니다. Blade 스택은 특별한 추가 인자 없이 `breeze:install` 명령어 실행 시 Blade 프론트엔드 스택을 선택하면 설치할 수 있습니다. 스캐폴딩이 완료된 후에는 프론트엔드 자산도 함께 빌드해야 합니다.

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<!-- Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file. -->
설치가 끝나면 웹 브라우저에서 애플리케이션의 `/login` 또는 `/register` 주소로 접속해 볼 수 있습니다. Breeze에서 사용되는 모든 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

> [!NOTE]
> 애플리케이션의 CSS와 JavaScript 컴파일에 대해 더 자세히 알고 싶다면, Laravel의 [Vite documentation](/docs/11.x/vite#running-vite)를 참고하시기 바랍니다.

<a name="breeze-and-livewire"></a>
<!-- ### Breeze and Livewire -->
### Breeze and Livewire

<!-- Laravel Breeze also offers [Livewire](https://livewire.laravel.com) scaffolding. Livewire is a powerful way of building dynamic, reactive, front-end UIs using just PHP. -->
Laravel Breeze는 [Livewire](https://livewire.laravel.com) 기반의 스캐폴딩도 제공하고 있습니다. Livewire는 PHP만으로 동적이고 반응성 높은 프론트엔드 UI를 만들 수 있게 해 주는 강력한 도구입니다.

<!-- Livewire is a great fit for teams that primarily use Blade templates and are looking for a simpler alternative to JavaScript-driven SPA frameworks like Vue and React. -->
Livewire 스택은 Blade 템플릿을 선호하고, Vue나 React 같은 자바스크립트 중심 SPA 프레임워크 대신 좀 더 단순한 솔루션을 찾는 분들에게 적합합니다.

<!-- To use the Livewire stack, you may select the Livewire frontend stack when executing the `breeze:install` Artisan command. After Breeze's scaffolding is installed, you should run your database migrations: -->
Livewire 스택을 사용하려면 `breeze:install` 아티즌 명령어 실행 시 Livewire 프론트엔드 스택을 선택하시면 됩니다. Breeze 스캐폴딩이 끝난 후에는 데이터베이스 마이그레이션을 실행해 마무리합니다.

```shell
php artisan breeze:install

php artisan migrate
```

<a name="breeze-and-inertia"></a>
<!-- ### Breeze and React / Vue -->
### Breeze and React / Vue

<!-- Laravel Breeze also offers React and Vue scaffolding via an [Inertia](https://inertiajs.com) frontend implementation. Inertia allows you to build modern, single-page React and Vue applications using classic server-side routing and controllers. -->
Laravel Breeze는 [Inertia](https://inertiajs.com) 기반으로 React와 Vue 스캐폴딩도 지원합니다. Inertia를 이용하면 전통적인 서버 사이드 라우팅과 컨트롤러 구조를 그대로 유지하면서도, 현대적인 싱글 페이지 React 또는 Vue 애플리케이션을 쉽게 만들 수 있습니다.

<!-- Inertia lets you enjoy the frontend power of React and Vue combined with the incredible backend productivity of Laravel and lightning-fast [Vite](https://vitejs.dev) compilation. To use an Inertia stack, you may select the Vue or React frontend stacks when executing the `breeze:install` Artisan command. -->
Inertia를 사용하면 Laravel의 뛰어난 백엔드 생산성과 [Vite](https://vitejs.dev)로 빌드되는 빠른 프론트엔드(React, Vue)의 장점을 모두 누릴 수 있습니다. Inertia 스택을 사용하려면 `breeze:install` 명령어 실행 시 Vue 또는 React 프론트엔드 스택을 선택하면 됩니다.

<!-- When selecting the Vue or React frontend stack, the Breeze installer will also prompt you to determine if you would like [Inertia SSR](https://inertiajs.com/server-side-rendering) or TypeScript support. After Breeze's scaffolding is installed, you should also compile your application's frontend assets: -->
만약 Vue 또는 React 프론트엔드 스택을 선택한다면, Breeze 인스톨러가 [Inertia SSR](https://inertiajs.com/server-side-rendering)과 TypeScript 지원 여부도 함께 물어보게 됩니다. Breeze 스캐폴딩이 완료된 이후에는 프론트엔드 자산도 빌드해야 합니다.

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<!-- Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file. -->
설치가 끝나면 웹 브라우저에서 애플리케이션의 `/login` 또는 `/register` 경로로 접속해 볼 수 있습니다. 모든 Breeze 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

<a name="breeze-and-next"></a>
<!-- ### Breeze and Next.js / API -->
### Breeze and Next.js / API

<!-- Laravel Breeze can also scaffold an authentication API that is ready to authenticate modern JavaScript applications such as those powered by [Next](https://nextjs.org), [Nuxt](https://nuxt.com), and others. To get started, select the API stack as your desired stack when executing the `breeze:install` Artisan command: -->
Laravel Breeze는 [Next](https://nextjs.org), [Nuxt](https://nuxt.com) 등 현대적인 JavaScript 프레임워크에서 사용할 수 있는 인증 API 스캐폴딩도 지원합니다. 시작하려면 `breeze:install` 아티즌 명령어 실행 시 API 스택을 선택하면 됩니다.

```shell
php artisan breeze:install

php artisan migrate
```

<!-- During installation, Breeze will add a `FRONTEND_URL` environment variable to your application's `.env` file. This URL should be the URL of your JavaScript application. This will typically be `http://localhost:3000` during local development. In addition, you should ensure that your `APP_URL` is set to `http://localhost:8000`, which is the default URL used by the `serve` Artisan command. -->
설치하는 과정에서 Breeze가 애플리케이션의 `.env` 파일에 `FRONTEND_URL` 환경 변수를 추가합니다. 이 URL에는 사용하려는 자바스크립트 애플리케이션의 주소를 입력해야 하며, 보통 로컬 개발 환경에서는 `http://localhost:3000`을 사용합니다. 또한 `APP_URL` 역시 `http://localhost:8000`로 설정되어 있는지 확인해야 하며, 이는 기본적으로 `serve` 아티즌 명령어가 사용하는 주소입니다.

<a name="next-reference-implementation"></a>
<!-- #### Next.js Reference Implementation -->
#### Next.js Reference Implementation

<!-- Finally, you are ready to pair this backend with the frontend of your choice. A Next reference implementation of the Breeze frontend is [available on GitHub](https://github.com/laravel/breeze-next). This frontend is maintained by Laravel and contains the same user interface as the traditional Blade and Inertia stacks provided by Breeze. -->
이제 백엔드를 원하는 프론트엔드와 연결할 준비가 완료되었습니다. Breeze 프론트엔드의 Next 참고 구현체는 [available on GitHub](https://github.com/laravel/breeze-next). 이 프론트엔드는 Laravel에서 공식적으로 관리되며, Breeze의 일반적인 Blade 및 Inertia 스택과 동일한 사용자 인터페이스를 제공합니다.

<a name="laravel-jetstream"></a>
<!-- ## Laravel Jetstream -->
## Laravel Jetstream

<!-- While Laravel Breeze provides a simple and minimal starting point for building a Laravel application, Jetstream augments that functionality with more robust features and additional frontend technology stacks. **For those brand new to Laravel, we recommend learning the ropes with Laravel Breeze before graduating to Laravel Jetstream.** -->
Laravel Breeze가 간단하고 미니멀한 시작점이라면, Jetstream은 보다 강력하고 다양한 기능, 그리고 추가적인 프론트엔드 기술 스택을 통해 Breeze의 역할을 확장합니다. **Laravel이 처음이신 분들은 Laravel Breeze를 먼저 경험한 뒤, Jetstream을 도입해 보시길 권장합니다.**

<!-- Jetstream provides a beautifully designed application scaffolding for Laravel and includes login, registration, email verification, two-factor authentication, session management, API support via Laravel Sanctum, and optional team management. Jetstream is designed using [Tailwind CSS](https://tailwindcss.com) and offers your choice of [Livewire](https://livewire.laravel.com) or [Inertia](https://inertiajs.com) driven frontend scaffolding. -->
Jetstream은 Laravel에 아름답게 디자인된 애플리케이션 스캐폴딩을 제공하며, 로그인, 회원가입, 이메일 인증, 2단계 인증, 세션 관리, Laravel Sanctum을 통한 API 지원, 선택적인 팀 관리까지 폭넓은 기능을 지원합니다. Jetstream 역시 [Tailwind CSS](https://tailwindcss.com)로 디자인되어 있으며, [Livewire](https://livewire.laravel.com) 또는 [Inertia](https://inertiajs.com) 기반 프론트엔드 스캐폴딩 중 원하는 방식을 선택할 수 있습니다.

<!-- Complete documentation for installing Laravel Jetstream can be found within the [official Jetstream documentation](https://jetstream.laravel.com). -->
Laravel Jetstream의 설치 방법과 자세한 기능은 [official Jetstream documentation](https://jetstream.laravel.com)에서 확인하실 수 있습니다.
