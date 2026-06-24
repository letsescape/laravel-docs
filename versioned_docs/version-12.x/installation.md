---
slug: /
---

<!-- # Installation -->
# Installation

- [Meet Laravel](#meet-laravel)
    - [Why Laravel?](#why-laravel)
- [Creating a Laravel Application](#creating-a-laravel-project)
    - [Installing PHP and the Laravel Installer](#installing-php)
    - [Creating an Application](#creating-an-application)
- [Initial Configuration](#initial-configuration)
    - [Environment Based Configuration](#environment-based-configuration)
    - [Databases and Migrations](#databases-and-migrations)
    - [Directory Configuration](#directory-configuration)
- [Installation Using Herd](#installation-using-herd)
    - [Herd on macOS](#herd-on-macos)
    - [Herd on Windows](#herd-on-windows)
- [IDE Support](#ide-support)
- [Laravel and AI](#laravel-and-ai)
    - [Installing Laravel Boost](#installing-laravel-boost)
- [Next Steps](#next-steps)
    - [Laravel the Full Stack Framework](#laravel-the-fullstack-framework)
    - [Laravel the API Backend](#laravel-the-api-backend)

<a name="meet-laravel"></a>
<!-- ## Meet Laravel -->
## Meet Laravel

<!-- Laravel is a web application framework with expressive, elegant syntax. A web framework provides a structure and starting point for creating your application, allowing you to focus on creating something amazing while we sweat the details. -->
Laravel은 표현력이 뛰어나고 우아한 문법을 제공하는 웹 애플리케이션 프레임워크입니다. 웹 프레임워크란, 애플리케이션을 만들 때 구조와 출발점을 제공하여, 여러분이 세세한 부분까지 신경 쓰지 않고도 멋진 것을 만드는 데 집중할 수 있게 도와주는 도구입니다.

<!-- Laravel strives to provide an amazing developer experience while providing powerful features such as thorough dependency injection, an expressive database abstraction layer, queues and scheduled jobs, unit and integration testing, and more. -->
Laravel은 강력한 기능과 함께 뛰어난 개발자 경험을 제공하기 위해 노력합니다. 예를 들어 철저한 의존성 주입, 표현력 높은 데이터베이스 추상화 레이어, 큐와 예약 작업, 단위 및 통합 테스트 등 다양한 기능을 제공합니다.

<!-- Whether you are new to PHP web frameworks or have years of experience, Laravel is a framework that can grow with you. We'll help you take your first steps as a web developer or give you a boost as you take your expertise to the next level. We can't wait to see what you build. -->
PHP 웹 프레임워크가 처음인 분이든, 다년간의 경험을 가진 개발자이든, Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서 첫 걸음을 내딛도록 돕거나, 여러분의 역량을 한 단계 더 성장시킬 수 있도록 지원합니다. 여러분이 Laravel로 어떤 것을 만들어낼지 기대됩니다.

<a name="why-laravel"></a>
<!-- ### Why Laravel? -->
### Why Laravel?

<!-- There are a variety of tools and frameworks available to you when building a web application. However, we believe Laravel is the best choice for building modern, full-stack web applications. -->
웹 애플리케이션을 개발할 때 선택할 수 있는 도구와 프레임워크는 다양합니다. 하지만 저희는 Laravel이 현대적이고, 풀스택 웹 애플리케이션을 구축하기에 가장 적합한 선택이라고 믿습니다.

<!-- #### A Progressive Framework -->
#### A Progressive Framework

<!-- We like to call Laravel a "progressive" framework. By that, we mean that Laravel grows with you. If you're just taking your first steps into web development, Laravel's vast library of documentation, guides, and [video tutorials](https://laracasts.com) will help you learn the ropes without becoming overwhelmed. -->
Laravel은 "점진적(progressive)" 프레임워크로 불리기도 합니다. 이는 Laravel이 여러분과 함께 성장할 수 있다는 뜻입니다. 웹 개발에 첫발을 들이는 단계라면, Laravel의 방대한 공식 문서, 가이드, [video tutorials](https://laracasts.com) 덕분에 부담 없이 기본기를 익힐 수 있습니다.

<!-- If you're a senior developer, Laravel gives you robust tools for [dependency injection](/docs/12.x/container), [unit testing](/docs/12.x/testing), [queues](/docs/12.x/queues), [real-time events](/docs/12.x/broadcasting), and more. Laravel is fine-tuned for building professional web applications and ready to handle enterprise workloads. -->
경험이 풍부한 시니어 개발자라면, Laravel은 [dependency injection](/docs/12.x/container), [unit testing](/docs/12.x/testing), [queues](/docs/12.x/queues), [real-time events](/docs/12.x/broadcasting) 등 전문가용 도구를 제공합니다. Laravel은 전문적인 웹 애플리케이션 구축에 최적화되어 있으며, 엔터프라이즈 규모의 트래픽도 거뜬히 처리할 준비가 되어 있습니다.

<!-- #### A Scalable Framework -->
#### A Scalable Framework

<!-- Laravel is incredibly scalable. Thanks to the scaling-friendly nature of PHP and Laravel's built-in support for fast, distributed cache systems like Redis, horizontal scaling with Laravel is a breeze. In fact, Laravel applications have been easily scaled to handle hundreds of millions of requests per month. -->
Laravel은 매우 뛰어난 확장성을 자랑합니다. PHP의 확장 친화적인 특성과, Redis와 같은 빠르고 분산된 캐시 시스템을 Laravel에서 기본적으로 지원하기 때문에, Laravel로 수평 확장이 매우 쉽게 가능합니다. 실제로, Laravel 애플리케이션은 월 수억 건의 요청을 처리하도록 쉽게 확장된 사례가 있습니다.

<!-- Need extreme scaling? Platforms like [Laravel Cloud](https://cloud.laravel.com) allow you to run your Laravel application at nearly limitless scale. -->
더 극단적인 확장이 필요하다면, [Laravel Cloud](https://cloud.laravel.com) 같은 플랫폼을 이용해 거의 무제한에 가까운 규모로 Laravel 애플리케이션을 운영할 수 있습니다.

<!-- #### An Agent Ready Framework -->
#### An Agent Ready Framework

<!-- Laravel's opinionated conventions and well-defined structure make it an ideal framework for [AI assisted development](/docs/12.x/ai) using tools like Cursor and Claude Code. When you ask an AI agent to add a controller, it knows exactly where to place it. When you need a new migration, the naming conventions and file locations are predictable. This consistency eliminates the guesswork that often trips up AI tools in more flexible frameworks. -->
Laravel은 명확한 규칙과 잘 정의된 구조를 갖추고 있어, Cursor나 Claude Code와 같은 도구를 활용한 [AI assisted development](/docs/12.x/ai)에 최적화되어 있습니다. 예를 들어, AI 에이전트에게 컨트롤러를 추가하라고 명령하면, 어디에 추가해야 하는지 정확히 알 수 있습니다. 마이그레이션 파일 역시 이름 규칙과 디렉터리 구조가 예측 가능해 AI 도구가 실수 없이 작업을 수행할 수 있습니다.

<!-- Beyond file organization, Laravel's expressive syntax and comprehensive documentation give AI agents the context they need to generate accurate, idiomatic code. Features like Eloquent relationships, form requests, and middleware follow patterns that agents can reliably understand and replicate. The result is AI-generated code that looks like it was written by a seasoned Laravel developer, not stitched together from generic PHP snippets. -->
파일 구조뿐만 아니라, 표현력 있는 문법과 포괄적인 문서 덕분에 AI 에이전트는 필요한 맥락 정보를 충분히 얻어 올바른 코드, 즉 Laravel 스타일의 코드를 만들어낼 수 있습니다. Eloquent 연관 관계, 폼 리퀘스트, 미들웨어와 같은 기능 역시 예측 가능한 패턴을 따르므로, AI가 쉽게 이해하고 활용할 수 있습니다. 그 결과, AI가 작성한 코드도 숙련된 Laravel 개발자가 작성한 것처럼 자연스럽게 만들어집니다.

<!-- To learn more about why Laravel is the perfect choice for AI assisted development, check out our documentation on [agentic development](/docs/12.x/ai). -->
AI 지원 개발에 이상적인 프레임워크로서의 Laravel에 대해 더 알고 싶다면 [agentic development](/docs/12.x/ai) 문서를 참고하세요.

<!-- #### A Community Framework -->
#### A Community Framework

<!-- Laravel combines the best packages in the PHP ecosystem to offer the most robust and developer friendly framework available. In addition, thousands of talented developers from around the world have [contributed to the framework](https://github.com/laravel/framework). Who knows, maybe you'll even become a Laravel contributor. -->
Laravel은 PHP 생태계의 우수한 패키지들을 결합하여, 가장 강력하고 개발자 친화적인 프레임워크를 제공합니다. 전 세계 수많은 뛰어난 개발자들이 Laravel에 [contributed to the framework](https://github.com/laravel/framework)하고 있습니다. 여러분도 언젠가 Laravel에 기여하게 될지도 모릅니다.

<a name="creating-a-laravel-project"></a>
<!-- ## Creating a Laravel Application -->
## Creating a Laravel Application

<a name="installing-php"></a>
<!-- ### Installing PHP and the Laravel Installer -->
### Installing PHP and the Laravel Installer

<!-- Before creating your first Laravel application, make sure that your local machine has [PHP](https://php.net), [Composer](https://getcomposer.org), and [the Laravel installer](https://github.com/laravel/installer) installed. In addition, you should install either [Node and NPM](https://nodejs.org) or [Bun](https://bun.sh/) so that you can compile your application's frontend assets. -->
처음 Laravel 애플리케이션을 만들기 전에, 로컬 머신에 [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [the Laravel installer](https://github.com/laravel/installer)가 설치되어 있는지 확인하세요. 또한, 애플리케이션의 프론트엔드 자산을 컴파일하기 위해 [Node and NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나를 설치해야 합니다.

<!-- If you don't have PHP and Composer installed on your local machine, the following commands will install PHP, Composer, and the Laravel installer on macOS, Windows, or Linux: -->
만약 로컬 머신에 PHP와 Composer가 설치되어 있지 않다면, 아래 명령어로 macOS, Windows, Linux에서 PHP, Composer, Laravel 설치 도구를 한 번에 설치할 수 있습니다:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# Run as administrator...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

<!-- After running one of the commands above, you should restart your terminal session. To update PHP, Composer, and the Laravel installer after installing them via `php.new`, you can re-run the command in your terminal. -->
위 명령어 중 하나를 실행한 후에는 터미널 세션을 다시 시작하세요. 추후 PHP, Composer, Laravel 설치 도구를 `php.new`로 설치한 이후에도, 위 명령어를 다시 실행하면 업데이트할 수 있습니다.

<!-- If you already have PHP and Composer installed, you may install the Laravel installer via Composer: -->
이미 PHP와 Composer가 설치되어 있다면 Composer로 Laravel 설치 도구만 따로 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> 보다 완벽한 기능과 그래픽 기반의 PHP 설치/관리를 원한다면 [Laravel Herd](#installation-using-herd)를 참고하세요.

<a name="creating-an-application"></a>
<!-- ### Creating an Application -->
### Creating an Application

<!-- After you have installed PHP, Composer, and the Laravel installer, you're ready to create a new Laravel application. The Laravel installer will prompt you to select your preferred testing framework, database, and starter kit: -->
PHP, Composer, Laravel 설치 도구 설치가 끝났다면 이제 새로운 Laravel 애플리케이션을 바로 만들 수 있습니다. Laravel 설치 도구는 원하는 테스트 프레임워크, 데이터베이스, 스타터 키트 등을 선택할 수 있도록 안내합니다:

```shell
laravel new example-app
```

<!-- Once the application has been created, you can start Laravel's local development server, queue worker, and Vite development server using the `dev` Composer script: -->
애플리케이션이 만들어지면, `dev` Composer 스크립트로 Laravel의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 실행할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

<!-- Once you have started the development server, your application will be accessible in your web browser at [http://localhost:8000](http://localhost:8000). Next, you're ready to [start taking your next steps into the Laravel ecosystem](#next-steps). Of course, you may also want to [configure a database](#databases-and-migrations). -->
개발 서버가 실행되면, 애플리케이션은 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 접속 가능합니다. 이제 [start taking your next steps into the Laravel ecosystem](#next-steps)할 준비가 되었습니다. 물론 [configure a database](#databases-and-migrations)도 원하실 수 있습니다.

> [!NOTE]
> Laravel 애플리케이션 개발을 빠르게 시작하고 싶다면 [starter kits](/docs/12.x/starter-kits)를 사용해 보세요. Laravel의 스타터 키트는 인증 시스템(백엔드/프론트엔드 포함)을 빠르게 적용할 수 있습니다.

<a name="initial-configuration"></a>
<!-- ## Initial Configuration -->
## Initial Configuration

<!-- All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you. -->
Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장됩니다. 각 옵션에는 설명이 잘 달려 있으니 언제든 파일을 살펴보며 설정 가능한 옵션을 익혀보세요.

<!-- Laravel needs almost no additional configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `url` and `locale` that you may wish to change according to your application. -->
Laravel은 기본값 그대로도 대부분의 경우 별도의 추가 설정이 필요하지 않습니다. 바로 개발을 시작하실 수 있습니다! 하지만, `config/app.php` 파일과 그 문서도 한번 확인해 보시기 바랍니다. 예를 들어 `url`, `locale` 등 애플리케이션 특성에 따라 변경할 수 있는 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
<!-- ### Environment Based Configuration -->
### Environment Based Configuration

<!-- Since many of Laravel's configuration option values may vary depending on whether your application is running on your local machine or on a production web server, many important configuration values are defined using the `.env` file that exists at the root of your application. -->
Laravel의 설정 값은 로컬 머신에서 실행하는지, 운영 서버에서 실행하는지에 따라 값이 달라질 수 있습니다. 그래서 중요한 설정 값들은 애플리케이션 루트의 `.env` 파일을 통해 지정하는 것이 일반적입니다.

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would be exposed. -->
`.env` 파일은 개발자나 서버별 환경이 다를 수 있으므로 애플리케이션의 소스 관리 시스템에는 커밋하지 않는 것이 좋습니다. 게다가 침입자가 소스 관리 저장소에 접근할 경우 중요한 인증 정보가 모두 노출되어 보안상 위험하기 때문입니다.

> [!NOTE]
> `.env` 파일과 환경 기반 설정에 대해 더 자세히 알고 싶다면 [configuration documentation](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
<!-- ### Databases and Migrations -->
### Databases and Migrations

<!-- Now that you have created your Laravel application, you probably want to store some data in a database. By default, your application's `.env` configuration file specifies that Laravel will be interacting with an SQLite database. -->
Laravel 애플리케이션을 만들었다면 데이터를 데이터베이스에 저장하고 싶을 것입니다. 기본적으로 여러분의 `.env` 설정 파일에는 Laravel이 SQLite 데이터베이스를 사용하도록 지정되어 있습니다.

<!-- During the creation of the application, Laravel created a `database/database.sqlite` file for you, and ran the necessary migrations to create the application's database tables. -->
애플리케이션을 생성하는 과정에서 Laravel이 자동으로 `database/database.sqlite` 파일을 만들고, 마이그레이션을 실행해 필요한 데이터베이스 테이블도 초기화합니다.

<!-- If you prefer to use another database driver such as MySQL or PostgreSQL, you can update your `.env` configuration file to use the appropriate database. For example, if you wish to use MySQL, update your `.env` configuration file's `DB_*` variables like so: -->
MySQL이나 PostgreSQL 등 다른 데이터베이스 드라이버를 사용하고 싶다면, `.env` 설정 파일에서 적절한 데이터베이스로 변경할 수 있습니다. 예를 들어 MySQL을 사용하려면, `.env` 설정 파일의 `DB_*` 변수를 아래와 같이 수정하면 됩니다:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

<!-- If you choose to use a database other than SQLite, you will need to create the database and run your application's [database migrations](/docs/12.x/migrations): -->
SQLite 이외 데이터베이스를 사용한다면, 직접 데이터베이스를 생성하고 [database migrations](/docs/12.x/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]
> macOS나 Windows에서 MySQL, PostgreSQL, Redis 등을 로컬에 설치하고 싶다면, [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)을 이용해 보세요.

<a name="directory-configuration"></a>
<!-- ### Directory Configuration -->
### Directory Configuration

<!-- Laravel should always be served out of the root of the "web directory" configured for your web server. You should not attempt to serve a Laravel application out of a subdirectory of the "web directory". Attempting to do so could expose sensitive files present within your application. -->
Laravel은 반드시 웹 서버의 "웹 디렉터리" 루트에서 서비스되어야 합니다. 웹 디렉터리의 하위 디렉터리에서 Laravel 애플리케이션을 실행하려고 해서는 안 됩니다. 그렇게 할 경우 애플리케이션에 포함된 민감한 파일들이 노출될 수 있습니다.

<a name="installation-using-herd"></a>
<!-- ## Installation Using Herd -->
## Installation Using Herd

<!-- [Laravel Herd](https://herd.laravel.com) is a blazing fast, native Laravel and PHP development environment for macOS and Windows. Herd includes everything you need to get started with Laravel development, including PHP and Nginx. -->
[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows에서 사용할 수 있는 매우 빠르고, 네이티브한 Laravel·PHP 개발 환경입니다. Herd에는 Laravel 개발에 필요한 PHP, Nginx 등이 모두 포함되어 있습니다.

<!-- Once you install Herd, you're ready to start developing with Laravel. Herd includes command line tools for `php`, `composer`, `laravel`, `expose`, `node`, `npm`, and `nvm`. -->
Herd를 설치하면 바로 Laravel 개발을 시작할 수 있습니다. Herd에는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등 개발에 필요한 명령줄 도구가 기본 제공됩니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 Herd에 강력한 추가 기능을 제공합니다. 예를 들어, 로컬 MySQL, Postgres, Redis 데이터베이스 생성/관리, 메일 뷰잉, 로그 모니터링 기능 등이 포함되어 있습니다.

<a name="herd-on-macos"></a>
<!-- ### Herd on macOS -->
### Herd on macOS

<!-- If you develop on macOS, you can download the Herd installer from the [Herd website](https://herd.laravel.com). The installer automatically downloads the latest version of PHP and configures your Mac to always run [Nginx](https://www.nginx.com/) in the background. -->
macOS에서 개발한다면 [Herd website](https://herd.laravel.com)에서 설치 프로그램을 다운로드할 수 있습니다. 설치 프로그램은 최신 버전의 PHP를 자동으로 다운로드하고, Mac에서 [Nginx](https://www.nginx.com/)가 항상 백그라운드에서 실행되도록 설정합니다.

<!-- Herd for macOS uses [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq) to support "parked" directories. Any Laravel application in a parked directory will automatically be served by Herd. By default, Herd creates a parked directory at `~/Herd` and you can access any Laravel application in this directory on the `.test` domain using its directory name. -->
macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 "파킹된" 디렉터리를 지원합니다. 파킹된 디렉터리 내의 Laravel 애플리케이션은 자동으로 Herd에서 서비스됩니다. 기본적으로 Herd는 `~/Herd` 경로에 파킹 디렉터리를 만드며, 이곳에 있는 Laravel 애플리케이션은 디렉터리 명을 그대로 사용해 `.test` 도메인에서 접근할 수 있습니다.

<!-- After installing Herd, the fastest way to create a new Laravel application is using the Laravel CLI, which is bundled with Herd: -->
Herd를 설치한 뒤, 새로운 Laravel 애플리케이션을 만들 때는 Herd와 함께 제공되는 Laravel CLI를 활용하는 것이 가장 빠릅니다:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

<!-- Of course, you can always manage your parked directories and other PHP settings via Herd's UI, which can be opened from the Herd menu in your system tray. -->
물론 시스템 트레이의 Herd 메뉴에서 Herd UI를 열어 파킹 디렉터리나 기타 PHP 설정을 직접 관리할 수도 있습니다.

<!-- You can learn more about Herd by checking out the [Herd documentation](https://herd.laravel.com/docs). -->
Herd에 대해 더 알고 싶다면 [Herd documentation](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
<!-- ### Herd on Windows -->
### Herd on Windows

<!-- You can download the Windows installer for Herd on the [Herd website](https://herd.laravel.com/windows). After the installation finishes, you can start Herd to complete the onboarding process and access the Herd UI for the first time. -->
[Herd website](https://herd.laravel.com/windows)에서 Windows용 설치 프로그램을 다운로드할 수 있습니다. 설치가 완료되면 Herd를 실행해 온보딩 절차를 마치고, Herd UI에 처음으로 접속할 수 있습니다.

<!-- The Herd UI is accessible by left-clicking on Herd's system tray icon. A right-click opens the quick menu with access to all tools that you need on a daily basis. -->
Herd UI는 시스템 트레이에 있는 Herd 아이콘을 왼쪽 클릭해서 열 수 있으며, 오른쪽 클릭하면 필요한 여러 도구에 빠르게 접근할 수 있는 메뉴가 나타납니다.

<!-- During installation, Herd creates a "parked" directory in your home directory at `%USERPROFILE%\Herd`. Any Laravel application in a parked directory will automatically be served by Herd, and you can access any Laravel application in this directory on the `.test` domain using its directory name. -->
설치 중 Herd는 홈 디렉터리의 `%USERPROFILE%\Herd`에 "파킹된" 디렉터리를 생성합니다. 이 디렉터리 안에 있는 모든 Laravel 애플리케이션은 Herd에 의해 자동으로 서비스되며, 디렉터리 이름을 사용해 `.test` 도메인으로 쉽게 접근할 수 있습니다.

<!-- After installing Herd, the fastest way to create a new Laravel application is using the Laravel CLI, which is bundled with Herd. To get started, open Powershell and run the following commands: -->
설치 후에는 Herd에 포함된 Laravel CLI로 새로운 Laravel 애플리케이션을 만들 수 있습니다. PowerShell을 열고 아래 명령어를 실행하세요:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

<!-- You can learn more about Herd by checking out the [Herd documentation for Windows](https://herd.laravel.com/docs/windows). -->
Herd에 대한 더 자세한 내용은 [Herd documentation for Windows](https://herd.laravel.com/docs/windows)를 참고하세요.

<a name="ide-support"></a>
<!-- ## IDE Support -->
## IDE Support

<!-- You are free to use any code editor you wish when developing Laravel applications. If you're looking for lightweight and extensible editors, [VS Code](https://code.visualstudio.com) or [Cursor](https://cursor.com) combined with the official [Laravel VS Code Extension](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel) offers excellent Laravel support with features like syntax highlighting, snippets, artisan command integration, and smart autocompletion for Eloquent models, routes, middleware, assets, config, and Inertia.js. -->
Laravel 애플리케이션 개발에는 원하는 어떤 코드 에디터도 자유롭게 사용할 수 있습니다. 가볍고 확장성 있는 에디터를 원한다면 [VS Code](https://code.visualstudio.com) 또는 [Cursor](https://cursor.com)에 공식 [Laravel VS Code Extension](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 추가해서 사용해 보세요. Laravel 전용 문법 하이라이팅, 코드 스니펫, 아티즌 명령어 통합, Eloquent 모델/라우트/미들웨어/에셋/설정/Inertia.js 자동완성 등 강력한 기능을 지원합니다.

<!-- For extensive and robust support of Laravel, take a look at [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025), a JetBrains IDE. PhpStorm's built-in Laravel framework support includes Blade templates, smart autocompletion for Eloquent models, routes, views, translations, and components, along with powerful code generation and navigation across Laravel projects. -->
좀 더 강력하고 깊이 있는 Laravel 지원을 원한다면 JetBrains의 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025)을 추천합니다. Blade 템플릿, Eloquent 모델/라우트/뷰/다국어/컴포넌트 자동완성, 강력한 코드 생성 및 프로젝트 전체 네비게이션 등 Laravel을 위한 내장 기능을 제공합니다.

<!-- For those seeking a cloud-based development experience, [Firebase Studio](https://firebase.studio/) provides instant access to building with Laravel directly in your browser. With zero setup required, Firebase Studio makes it easy to start building Laravel applications from any device. -->
클라우드 기반 개발 경험이 필요하다면 [Firebase Studio](https://firebase.studio/)를 활용해 브라우저에서 바로 Laravel 개발을 할 수 있습니다. 별도 셋업 없이, 언제 어디서든 즉시 Laravel 프로젝트를 시작할 수 있습니다.

<a name="laravel-and-ai"></a>
<!-- ## Laravel and AI -->
## Laravel and AI

<!-- [Laravel Boost](https://github.com/laravel/boost) is a powerful tool that bridges the gap between AI coding agents and Laravel applications. Boost provides AI agents with Laravel-specific context, tools, and guidelines so they can generate more accurate, version-specific code that follows Laravel conventions. -->
[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 Laravel 애플리케이션 사이의 장벽을 허물어주는 강력한 도구입니다. Boost는 AI 에이전트에게 Laravel만의 맥락, 도구, 지침을 제공하여, Laravel 규칙 및 버전에 맞는 더 정확한 코드를 만들어낼 수 있게 도와줍니다.

<!-- When you install Boost in your Laravel application, AI agents gain access to over 15 specialized tools including the ability to know which packages you are using, query your database, search the Laravel documentation, read browser logs, generate tests, and execute code via Tinker. -->
Boost를 애플리케이션에 설치하면, AI 에이전트가 사용할 수 있는 15개 이상의 전용 도구가 추가됩니다. 사용 중인 패키지 확인, 데이터베이스 쿼리, Laravel 문서 검색, 브라우저 로그 읽기, 테스트 생성, Tinker를 통한 코드 실행 등이 가능합니다.

<!-- In addition, Boost gives AI agents access to over 17,000 pieces of vectorized Laravel ecosystem documentation, specific to your installed package versions. This means agents can provide guidance targeted to the exact versions your project uses. -->
또한 Boost는 프로젝트별로 설치된 패키지 버전에 맞는 1만 7천개 이상의 벡터화된 Laravel 생태계 문서 데이터를 AI 에이전트에 제공합니다. 덕분에 AI가 프로젝트에 딱 맞는 버전의 정보를 기반으로 더 정확한 도움을 줄 수 있습니다.

<!-- Boost also includes Laravel-maintained AI guidelines that help agents to follow framework conventions, write appropriate tests, and avoid common pitfalls when generating Laravel code. -->
Boost에는 Laravel에서 직접 관리하는 AI 개발 지침이 함께 제공되어, 에이전트가 프레임워크 규칙을 잘 따르고, 적절한 테스트 코드를 작성하며, 코드 생성 시 흔히 저지르는 실수를 방지할 수 있습니다.

<a name="installing-laravel-boost"></a>
<!-- ### Installing Laravel Boost -->
### Installing Laravel Boost

<!-- Boost can be installed in Laravel 10, 11, and 12 applications running PHP 8.1 or higher. To get started, install Boost as a development dependency: -->
Boost는 PHP 8.1 이상을 사용하는 Laravel 10, 11, 12 버전에서 설치할 수 있습니다. 다음 명령어로 개발 의존성으로 Boost를 추가하세요:

```shell
composer require laravel/boost --dev
```

<!-- Once installed, run the interactive installer: -->
설치가 끝나면, 상호작용형 인스톨러를 실행합니다:

```shell
php artisan boost:install
```

<!-- The installer will auto-detect your IDE and AI agents, allowing you to opt into the features that make sense for your project. Boost respects existing project conventions and doesn't force opinionated style rules by default. -->
인스톨러는 여러분의 IDE와 AI 에이전트를 자동 감지하며, 프로젝트에 적합한 기능들을 선택적으로 활성화할 수 있습니다. Boost는 기존 프로젝트 규칙을 존중하며, 기본적으로 스타일 규칙을 강제하지 않습니다.

> [!NOTE]
> Boost에 대해 더 알아보려면 [Laravel Boost repository on GitHub](https://github.com/laravel/boost)를 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
<!-- #### Adding Custom AI Guidelines -->
#### Adding Custom AI Guidelines

<!-- To augment Laravel Boost with your own custom AI guidelines, add `.blade.php` or `.md` files to your application's `.ai/guidelines/*` directory. These files will automatically be included with Laravel Boost's guidelines when you run `boost:install`. -->
Laravel Boost에 직접 만든 AI 지침을 추가하고 싶다면, 애플리케이션의 `.ai/guidelines/*` 디렉터리에 `.blade.php` 또는 `.md` 파일을 넣으면 됩니다. 이 파일들은 `boost:install` 명령 실행 시 Boost의 기본 지침과 함께 자동으로 적용됩니다.

<a name="next-steps"></a>
<!-- ## Next Steps -->
## Next Steps

<!-- Now that you have created your Laravel application, you may be wondering what to learn next. First, we strongly recommend becoming familiar with how Laravel works by reading the following documentation: -->
이제 Laravel 애플리케이션을 만들었으니, 앞으로 무엇을 공부하고 개발할지 고민하실 수 있습니다. 먼저, Laravel이 어떻게 동작하는지 익히기 위해 다음 문서를 꼭 읽어보시길 추천합니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- [Request Lifecycle](/docs/12.x/lifecycle)
- [Configuration](/docs/12.x/configuration)
- [Directory Structure](/docs/12.x/structure)
- [Frontend](/docs/12.x/frontend)
- [Service Container](/docs/12.x/container)
- [Facades](/docs/12.x/facades)
-->
- [Request Lifecycle](/docs/12.x/lifecycle)
- [Configuration](/docs/12.x/configuration)
- [Directory Structure](/docs/12.x/structure)
- [Frontend](/docs/12.x/frontend)
- [Service Container](/docs/12.x/container)
- [Facades](/docs/12.x/facades)

<!-- </div> -->
</div>

<!-- How you want to use Laravel will also dictate the next steps on your journey. There are a variety of ways to use Laravel, and we'll explore two primary use cases for the framework below. -->
여러분이 Laravel을 어떻게 사용하고 싶은지에 따라서도 앞으로의 학습 방향이 달라집니다. Laravel 프레임워크를 활용하는 대표적인 두 가지 방식을 아래에서 소개합니다.

<a name="laravel-the-fullstack-framework"></a>
<!-- ### Laravel the Full Stack Framework -->
### Laravel the Full Stack Framework

<!-- Laravel may serve as a full stack framework. By "full stack" framework we mean that you are going to use Laravel to route requests to your application and render your frontend via [Blade templates](/docs/12.x/blade) or a single-page application hybrid technology like [Inertia](https://inertiajs.com). This is the most common way to use the Laravel framework, and, in our opinion, the most productive way to use Laravel. -->
Laravel을 풀스택 프레임워크로 사용할 수 있습니다. 여기서 "풀스택"이라는 것은, Laravel로 요청을 처리하고, [Blade templates](/docs/12.x/blade)이나 [Inertia](https://inertiajs.com) 같은 SPA 하이브리드 기술로 프론트엔드까지 직접 렌더링하는 방식을 의미합니다. 가장 일반적이고, 저희가 생각하기에도 가장 생산적인 Laravel 사용 방식입니다.

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [frontend development](/docs/12.x/frontend), [routing](/docs/12.x/routing), [views](/docs/12.x/views), or the [Eloquent ORM](/docs/12.x/eloquent). In addition, you might be interested in learning about community packages like [Livewire](https://livewire.laravel.com) and [Inertia](https://inertiajs.com). These packages allow you to use Laravel as a full-stack framework while enjoying many of the UI benefits provided by single-page JavaScript applications. -->
이 방식으로 Laravel을 사용할 계획이라면 [frontend development](/docs/12.x/frontend), [routing](/docs/12.x/routing), [views](/docs/12.x/views), [Eloquent ORM](/docs/12.x/eloquent) 문서를 확인해 보세요. 또한, 커뮤니티 패키지인 [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com)도 추천합니다. 이 패키지들은 Laravel 풀스택 프레임워크 환경에서, SPA가 주는 UI의 장점도 함께 누릴 수 있게 해 줍니다.

<!-- If you are using Laravel as a full stack framework, we also strongly encourage you to learn how to compile your application's CSS and JavaScript using [Vite](/docs/12.x/vite). -->
풀스택 프레임워크로 Laravel을 사용할 때는 [Vite](/docs/12.x/vite)로 CSS, 자바스크립트 자산을 빌드하는 방법도 꼭 익히시기 바랍니다.

> [!NOTE]
> 애플리케이션 개발을 더 빠르게 시작하고 싶다면 공식 [application starter kits](/docs/12.x/starter-kits)를 확인해보세요.

<a name="laravel-the-api-backend"></a>
<!-- ### Laravel the API Backend -->
### Laravel the API Backend

<!-- Laravel may also serve as an API backend to a JavaScript single-page application or mobile application. For example, you might use Laravel as an API backend for your [Next.js](https://nextjs.org) application. In this context, you may use Laravel to provide [authentication](/docs/12.x/sanctum) and data storage / retrieval for your application, while also taking advantage of Laravel's powerful services such as queues, emails, notifications, and more. -->
Laravel은 자바스크립트 싱글 페이지 애플리케이션(SPA)이나 모바일 애플리케이션을 위한 API 백엔드로도 사용할 수 있습니다. 예를 들어 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 사용할 수 있습니다. 이 경우, Laravel은 [authentication](/docs/12.x/sanctum)과 데이터 저장/조회 기능은 물론, 큐, 이메일, 알림 등 다양한 강력한 서비스를 제공합니다.

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/12.x/routing), [Laravel Sanctum](/docs/12.x/sanctum), and the [Eloquent ORM](/docs/12.x/eloquent). -->
이와 같이 Laravel을 API 백엔드로 활용한다면, [routing](/docs/12.x/routing), [Laravel Sanctum](/docs/12.x/sanctum), [Eloquent ORM](/docs/12.x/eloquent)에 관한 문서를 참고해 보세요.