---
slug: /
---

<!-- # Installation -->
# Installation

- [Meet Laravel](#meet-laravel)
    - [Why Laravel?](#why-laravel)
- [Creating a Laravel Project](#creating-a-laravel-project)
- [Initial Configuration](#initial-configuration)
    - [Environment Based Configuration](#environment-based-configuration)
    - [Databases and Migrations](#databases-and-migrations)
    - [Directory Configuration](#directory-configuration)
- [Docker Installation Using Sail](#docker-installation-using-sail)
    - [Sail on macOS](#sail-on-macos)
    - [Sail on Windows](#sail-on-windows)
    - [Sail on Linux](#sail-on-linux)
    - [Choosing Your Sail Services](#choosing-your-sail-services)
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
Laravel은 표현력이 뛰어나고 우아한 문법을 갖춘 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 출발점을 제공하므로, 세부적인 부분은 프레임워크에 맡기고 여러분은 멋진 것을 만드는 데 집중할 수 있습니다.

<!-- Laravel strives to provide an amazing developer experience while providing powerful features such as thorough dependency injection, an expressive database abstraction layer, queues and scheduled jobs, unit and integration testing, and more. -->
Laravel은 철저한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 및 통합 테스트 등 강력한 기능을 제공하면서도 뛰어난 개발자 경험을 제공하기 위해 노력합니다.

<!-- Whether you are new to PHP web frameworks or have years of experience, Laravel is a framework that can grow with you. We'll help you take your first steps as a web developer or give you a boost as you take your expertise to the next level. We can't wait to see what you build. -->
PHP 웹 프레임워크가 처음이든, 수년간의 경험이 있든, Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서 첫걸음을 내딛는 데 도움을 주거나, 전문성을 한 단계 더 끌어올릴 수 있도록 도와드리겠습니다. 여러분이 무엇을 만들어낼지 기대됩니다.

> [!NOTE]
> Laravel이 처음이신가요? 첫 Laravel 애플리케이션을 만드는 과정을 함께 따라가며 프레임워크를 직접 익힐 수 있는 [Laravel Bootcamp](https://bootcamp.laravel.com)를 확인해 보세요.

<a name="why-laravel"></a>
<!-- ### Why Laravel? -->
### Why Laravel?

<!-- There are a variety of tools and frameworks available to you when building a web application. However, we believe Laravel is the best choice for building modern, full-stack web applications. -->
웹 애플리케이션을 만들 때 사용할 수 있는 도구와 프레임워크는 다양합니다. 하지만 우리는 Laravel이 현대적인 풀스택 웹 애플리케이션을 만드는 데 가장 좋은 선택이라고 믿습니다.

<!-- #### A Progressive Framework -->
#### A Progressive Framework

<!-- We like to call Laravel a "progressive" framework. By that, we mean that Laravel grows with you. If you're just taking your first steps into web development, Laravel's vast library of documentation, guides, and [video tutorials](https://laracasts.com) will help you learn the ropes without becoming overwhelmed. -->
우리는 Laravel을 "점진적" 프레임워크라고 부릅니다. 이는 Laravel이 여러분과 함께 성장한다는 뜻입니다. 이제 막 웹 개발을 시작했다면, Laravel의 방대한 문서, 가이드, [video tutorials](https://laracasts.com)이 부담 없이 기본기를 익히는 데 도움을 줄 것입니다.

<!-- If you're a senior developer, Laravel gives you robust tools for [dependency injection](/docs/10.x/container), [unit testing](/docs/10.x/testing), [queues](/docs/10.x/queues), [real-time events](/docs/10.x/broadcasting), and more. Laravel is fine-tuned for building professional web applications and ready to handle enterprise work loads. -->
숙련된 개발자라면 Laravel은 [dependency injection](/docs/10.x/container), [unit testing](/docs/10.x/testing), [queues](/docs/10.x/queues), [real-time events](/docs/10.x/broadcasting) 등을 위한 견고한 도구를 제공합니다. Laravel은 전문적인 웹 애플리케이션 구축에 맞게 세심하게 조정되어 있으며, 엔터프라이즈 워크로드를 처리할 준비가 되어 있습니다.

<!-- #### A Scalable Framework -->
#### A Scalable Framework

<!-- Laravel is incredibly scalable. Thanks to the scaling-friendly nature of PHP and Laravel's built-in support for fast, distributed cache systems like Redis, horizontal scaling with Laravel is a breeze. In fact, Laravel applications have been easily scaled to handle hundreds of millions of requests per month. -->
Laravel은 매우 뛰어난 확장성을 제공합니다. PHP의 확장 친화적인 특성과 Redis 같은 빠른 분산 캐시 시스템에 대한 Laravel의 기본 지원 덕분에, Laravel로 수평 확장을 하는 일은 매우 쉽습니다. 실제로 Laravel 애플리케이션은 매월 수억 건의 요청을 처리하도록 손쉽게 확장된 사례가 있습니다.

<!-- Need extreme scaling? Platforms like [Laravel Vapor](https://vapor.laravel.com) allow you to run your Laravel application at nearly limitless scale on AWS's latest serverless technology. -->
극단적인 확장이 필요하신가요? [Laravel Vapor](https://vapor.laravel.com) 같은 플랫폼을 사용하면 AWS의 최신 서버리스 기술 위에서 Laravel 애플리케이션을 거의 무제한에 가까운 규모로 실행할 수 있습니다.

<!-- #### A Community Framework -->
#### A Community Framework

<!-- Laravel combines the best packages in the PHP ecosystem to offer the most robust and developer friendly framework available. In addition, thousands of talented developers from around the world have [contributed to the framework](https://github.com/laravel/framework). Who knows, maybe you'll even become a Laravel contributor. -->
Laravel은 PHP 생태계의 최고의 패키지들을 결합하여 가장 견고하고 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수천 명의 뛰어난 개발자들이 [contributed to the framework](https://github.com/laravel/framework)해 왔습니다. 어쩌면 여러분도 Laravel 기여자가 될 수 있습니다.

<a name="creating-a-laravel-project"></a>
<!-- ## Creating a Laravel Project -->
## Creating a Laravel Project

<!-- Before creating your first Laravel project, make sure that your local machine has PHP and [Composer](https://getcomposer.org) installed. If you are developing on macOS, PHP and Composer can be installed in minutes via [Laravel Herd](https://herd.laravel.com). In addition, we recommend [installing Node and NPM](https://nodejs.org). -->
첫 Laravel 프로젝트를 만들기 전에 로컬 머신에 PHP와 [Composer](https://getcomposer.org)가 설치되어 있는지 확인하세요. macOS에서 개발 중이라면 [Laravel Herd](https://herd.laravel.com)를 통해 몇 분 안에 PHP와 Composer를 설치할 수 있습니다. 또한 [installing Node and NPM](https://nodejs.org)를 권장합니다.

<!-- After you have installed PHP and Composer, you may create a new Laravel project via Composer's `create-project` command: -->
PHP와 Composer를 설치한 뒤에는 Composer의 `create-project` 명령어를 사용하여 새 Laravel 프로젝트를 만들 수 있습니다.

```nothing
composer create-project "laravel/laravel:^10.0" example-app
```

<!-- Or, you may create new Laravel projects by globally installing [the Laravel installer](https://github.com/laravel/installer) via Composer: -->
또는 Composer를 통해 [the Laravel installer](https://github.com/laravel/installer)를 전역으로 설치하여 새 Laravel 프로젝트를 만들 수도 있습니다.

```nothing
composer global require laravel/installer

laravel new example-app
```

<!-- Once the project has been created, start Laravel's local development server using Laravel Artisan's `serve` command: -->
프로젝트가 생성되면 Laravel Artisan의 `serve` 명령어를 사용하여 Laravel 로컬 개발 서버를 시작하세요.

```nothing
cd example-app

php artisan serve
```

<!-- Once you have started the Artisan development server, your application will be accessible in your web browser at [http://localhost:8000](http://localhost:8000). Next, you're ready to [start taking your next steps into the Laravel ecosystem](#next-steps). Of course, you may also want to [configure a database](#databases-and-migrations). -->
Artisan 개발 서버를 시작하면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접근할 수 있습니다. 이제 [start taking your next steps into the Laravel ecosystem](#next-steps)가 되었습니다. 물론 [configure a database](#databases-and-migrations)하고 싶을 수도 있습니다.

> [!NOTE]
> Laravel 애플리케이션 개발을 더 빠르게 시작하고 싶다면 [starter kits](/docs/10.x/starter-kits) 중 하나를 사용하는 것을 고려해 보세요. Laravel 스타터 키트는 새 Laravel 애플리케이션을 위한 백엔드와 프론트엔드 인증 스캐폴딩을 제공합니다.

<a name="initial-configuration"></a>
<!-- ## Initial Configuration -->
## Initial Configuration

<!-- All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you. -->
Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장됩니다. 각 옵션에는 문서가 작성되어 있으므로, 파일을 살펴보며 사용할 수 있는 옵션에 익숙해져도 좋습니다.

<!-- Laravel needs almost no additional configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your application. -->
Laravel은 기본 상태에서 추가 설정이 거의 필요하지 않습니다. 바로 개발을 시작해도 됩니다. 하지만 `config/app.php` 파일과 그 문서를 검토해 보는 것이 좋습니다. 이 파일에는 애플리케이션에 맞게 변경하고 싶을 수 있는 `timezone`, `locale` 같은 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
<!-- ### Environment Based Configuration -->
### Environment Based Configuration

<!-- Since many of Laravel's configuration option values may vary depending on whether your application is running on your local machine or on a production web server, many important configuration values are defined using the `.env` file that exists at the root of your application. -->
Laravel의 많은 설정 옵션 값은 애플리케이션이 로컬 머신에서 실행되는지, 프로덕션 웹 서버에서 실행되는지에 따라 달라질 수 있습니다. 그래서 중요한 설정 값 다수는 애플리케이션 루트에 있는 `.env` 파일을 사용하여 정의됩니다.

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed. -->
`.env` 파일은 애플리케이션의 소스 관리에 커밋해서는 안 됩니다. 애플리케이션을 사용하는 각 개발자/서버마다 서로 다른 환경 설정이 필요할 수 있기 때문입니다. 더 나아가 침입자가 소스 관리 저장소에 접근하게 되면 민감한 인증 정보가 노출될 수 있으므로 보안 위험이 됩니다.

> [!NOTE]
> `.env` 파일과 환경 기반 설정에 대한 자세한 내용은 전체 [configuration documentation](/docs/10.x/configuration#environment-configuration)를 확인하세요.

<a name="databases-and-migrations"></a>
<!-- ### Databases and Migrations -->
### Databases and Migrations

<!-- Now that you have created your Laravel application, you probably want to store some data in a database. By default, your application's `.env` configuration file specifies that Laravel will be interacting with a MySQL database and will access the database at `127.0.0.1`. -->
이제 Laravel 애플리케이션을 만들었으므로, 아마 데이터베이스에 데이터를 저장하고 싶을 것입니다. 기본적으로 애플리케이션의 `.env` 설정 파일은 Laravel이 MySQL 데이터베이스와 상호작용하며 `127.0.0.1`에서 데이터베이스에 접근하도록 지정합니다.

> [!NOTE]
> macOS에서 개발 중이고 MySQL, Postgres, Redis를 로컬에 설치해야 한다면 [DBngin](https://dbngin.com/) 사용을 고려해 보세요.

<!-- If you do not want to install MySQL or Postgres on your local machine, you can always use a [SQLite](https://www.sqlite.org/index.html) database. SQLite is a small, fast, self-contained database engine. To get started, update your `.env` configuration file to use Laravel's `sqlite` database driver. You may remove the other database configuration options: -->
로컬 머신에 MySQL이나 Postgres를 설치하고 싶지 않다면 언제든지 [SQLite](https://www.sqlite.org/index.html) 데이터베이스를 사용할 수 있습니다. SQLite는 작고 빠르며 자체 완결적인 데이터베이스 엔진입니다. 시작하려면 `.env` 설정 파일을 업데이트하여 Laravel의 `sqlite` 데이터베이스 드라이버를 사용하도록 변경하세요. 다른 데이터베이스 설정 옵션은 제거해도 됩니다.

```ini
DB_CONNECTION=sqlite # [tl! add]
DB_CONNECTION=mysql # [tl! remove]
DB_HOST=127.0.0.1 # [tl! remove]
DB_PORT=3306 # [tl! remove]
DB_DATABASE=laravel # [tl! remove]
DB_USERNAME=root # [tl! remove]
DB_PASSWORD= # [tl! remove]
```

<!-- Once you have configured your SQLite database, you may run your application's [database migrations](/docs/10.x/migrations), which will create your application's database tables: -->
SQLite 데이터베이스를 설정한 뒤에는 애플리케이션의 [database migrations](/docs/10.x/migrations)을 실행할 수 있습니다. 이 작업은 애플리케이션의 데이터베이스 테이블을 생성합니다.

```shell
php artisan migrate
```

<!-- If an SQLite database does not exist for your application, Laravel will ask you if you would like the database to be created. Typically, the SQLite database file will be created at `database/database.sqlite`. -->
애플리케이션을 위한 SQLite 데이터베이스가 존재하지 않는 경우, Laravel은 데이터베이스를 생성할지 물어봅니다. 일반적으로 SQLite 데이터베이스 파일은 `database/database.sqlite`에 생성됩니다.

<a name="directory-configuration"></a>
<!-- ### Directory Configuration -->
### Directory Configuration

<!-- Laravel should always be served out of the root of the "web directory" configured for your web server. You should not attempt to serve a Laravel application out of a subdirectory of the "web directory". Attempting to do so could expose sensitive files present within your application. -->
Laravel은 항상 웹 서버에 설정된 "웹 디렉터리"의 루트에서 제공되어야 합니다. "웹 디렉터리"의 하위 디렉터리에서 Laravel 애플리케이션을 제공하려고 시도해서는 안 됩니다. 그렇게 하면 애플리케이션 내부의 민감한 파일이 노출될 수 있습니다.

<a name="docker-installation-using-sail"></a>
<!-- ## Docker Installation Using Sail -->
## Docker Installation Using Sail

<!-- We want it to be as easy as possible to get started with Laravel regardless of your preferred operating system. So, there are a variety of options for developing and running a Laravel project on your local machine. While you may wish to explore these options at a later time, Laravel provides [Sail](/docs/10.x/sail), a built-in solution for running your Laravel project using [Docker](https://www.docker.com). -->
우리는 사용자가 선호하는 운영체제와 관계없이 Laravel을 가능한 한 쉽게 시작할 수 있기를 바랍니다. 그래서 로컬 머신에서 Laravel 프로젝트를 개발하고 실행하는 방법에는 여러 가지 선택지가 있습니다. 이러한 선택지는 나중에 살펴봐도 되지만, Laravel은 [Sail](https://www.docker.com)를 사용하여 Laravel 프로젝트를 실행할 수 있는 내장 솔루션인 [Docker](/docs/10.x/sail)을 제공합니다.

<!-- Docker is a tool for running applications and services in small, light-weight "containers" which do not interfere with your local machine's installed software or configuration. This means you don't have to worry about configuring or setting up complicated development tools such as web servers and databases on your local machine. To get started, you only need to install [Docker Desktop](https://www.docker.com/products/docker-desktop). -->
Docker는 애플리케이션과 서비스를 작고 가벼운 "컨테이너" 안에서 실행하는 도구입니다. 이 컨테이너는 로컬 머신에 설치된 소프트웨어나 설정에 영향을 주지 않습니다. 즉, 웹 서버나 데이터베이스 같은 복잡한 개발 도구를 로컬 머신에 설정하거나 구성하는 일을 걱정하지 않아도 됩니다. 시작하려면 [Docker Desktop](https://www.docker.com/products/docker-desktop)만 설치하면 됩니다.

<!-- Laravel Sail is a light-weight command-line interface for interacting with Laravel's default Docker configuration. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience. -->
Laravel Sail은 Laravel의 기본 Docker 설정과 상호작용하기 위한 가벼운 명령줄 인터페이스입니다. Sail은 Docker 경험이 없어도 PHP, MySQL, Redis를 사용하여 Laravel 애플리케이션을 구축할 수 있는 훌륭한 출발점을 제공합니다.

> [!NOTE]
> 이미 Docker 전문가이신가요? 걱정하지 마세요! Sail의 모든 것은 Laravel에 포함된 `docker-compose.yml` 파일을 사용하여 커스터마이즈할 수 있습니다.

<a name="sail-on-macos"></a>
<!-- ### Sail on macOS -->
### Sail on macOS

<!-- If you're developing on a Mac and [Docker Desktop](https://www.docker.com/products/docker-desktop) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
Mac에서 개발 중이고 [Docker Desktop](https://www.docker.com/products/docker-desktop)이 이미 설치되어 있다면, 간단한 터미널 명령어로 새 Laravel 프로젝트를 만들 수 있습니다. 예를 들어 "example-app"이라는 디렉터리에 새 Laravel 애플리케이션을 만들려면 터미널에서 다음 명령어를 실행하면 됩니다.

```shell
curl -s "https://laravel.build/example-app" | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like - just make sure the application name only contains alpha-numeric characters, dashes, and underscores. The Laravel application's directory will be created within the directory you execute the command from. -->
물론 이 URL의 "example-app"은 원하는 이름으로 변경할 수 있습니다. 단, 애플리케이션 이름에는 영숫자, 하이픈, 밑줄만 포함되어야 합니다. Laravel 애플리케이션의 디렉터리는 명령어를 실행한 디렉터리 안에 생성됩니다.

<!-- Sail installation may take several minutes while Sail's application containers are built on your local machine. -->
Sail 애플리케이션 컨테이너가 로컬 머신에서 빌드되는 동안 Sail 설치에는 몇 분이 걸릴 수 있습니다.

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
프로젝트가 생성되면 애플리케이션 디렉터리로 이동하여 Laravel Sail을 시작할 수 있습니다. Laravel Sail은 Laravel의 기본 Docker 설정과 상호작용하기 위한 간단한 명령줄 인터페이스를 제공합니다.

```shell
cd example-app

./vendor/bin/sail up
```

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
애플리케이션의 Docker 컨테이너가 시작되면 웹 브라우저에서 다음 주소로 애플리케이션에 접근할 수 있습니다: http://localhost.

> [!NOTE]
> Laravel Sail에 대해 더 알아보려면 [complete documentation](/docs/10.x/sail)를 확인하세요.

<a name="sail-on-windows"></a>
<!-- ### Sail on Windows -->
### Sail on Windows

<!-- Before we create a new Laravel application on your Windows machine, make sure to install [Docker Desktop](https://www.docker.com/products/docker-desktop). Next, you should ensure that Windows Subsystem for Linux 2 (WSL2) is installed and enabled. WSL allows you to run Linux binary executables natively on Windows 10. Information on how to install and enable WSL2 can be found within Microsoft's [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10). -->
Windows 머신에서 새 Laravel 애플리케이션을 만들기 전에 [Docker Desktop](https://www.docker.com/products/docker-desktop)을 설치했는지 확인하세요. 다음으로 Windows Subsystem for Linux 2(WSL2)가 설치되어 있고 활성화되어 있는지 확인해야 합니다. WSL을 사용하면 Windows 10에서 Linux 바이너리 실행 파일을 네이티브로 실행할 수 있습니다. WSL2 설치 및 활성화 방법에 대한 정보는 Microsoft의 [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10)에서 확인할 수 있습니다.

> [!NOTE]
> WSL2를 설치하고 활성화한 뒤에는 Docker Desktop이 [configured to use the WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/)되어 있는지 확인해야 합니다.

<!-- Next, you are ready to create your first Laravel project. Launch [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) and begin a new terminal session for your WSL2 Linux operating system. Next, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
이제 첫 Laravel 프로젝트를 만들 준비가 되었습니다. [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)을 실행하고 WSL2 Linux 운영체제용 새 터미널 세션을 시작하세요. 그런 다음 간단한 터미널 명령어를 사용하여 새 Laravel 프로젝트를 만들 수 있습니다. 예를 들어 "example-app"이라는 디렉터리에 새 Laravel 애플리케이션을 만들려면 터미널에서 다음 명령어를 실행하면 됩니다.

```shell
curl -s https://laravel.build/example-app | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like - just make sure the application name only contains alpha-numeric characters, dashes, and underscores. The Laravel application's directory will be created within the directory you execute the command from. -->
물론 이 URL의 "example-app"은 원하는 이름으로 변경할 수 있습니다. 단, 애플리케이션 이름에는 영숫자, 하이픈, 밑줄만 포함되어야 합니다. Laravel 애플리케이션의 디렉터리는 명령어를 실행한 디렉터리 안에 생성됩니다.

<!-- Sail installation may take several minutes while Sail's application containers are built on your local machine. -->
Sail 애플리케이션 컨테이너가 로컬 머신에서 빌드되는 동안 Sail 설치에는 몇 분이 걸릴 수 있습니다.

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
프로젝트가 생성되면 애플리케이션 디렉터리로 이동하여 Laravel Sail을 시작할 수 있습니다. Laravel Sail은 Laravel의 기본 Docker 설정과 상호작용하기 위한 간단한 명령줄 인터페이스를 제공합니다.

```shell
cd example-app

./vendor/bin/sail up
```

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
애플리케이션의 Docker 컨테이너가 시작되면 웹 브라우저에서 다음 주소로 애플리케이션에 접근할 수 있습니다: http://localhost.

> [!NOTE]
> Laravel Sail에 대해 더 알아보려면 [complete documentation](/docs/10.x/sail)를 확인하세요.

<!-- #### Developing Within WSL2 -->
#### Developing Within WSL2

<!-- Of course, you will need to be able to modify the Laravel application files that were created within your WSL2 installation. To accomplish this, we recommend using Microsoft's [Visual Studio Code](https://code.visualstudio.com) editor and their first-party extension for [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack). -->
물론 WSL2 설치 환경 안에 생성된 Laravel 애플리케이션 파일을 수정할 수 있어야 합니다. 이를 위해 Microsoft의 [Visual Studio Code](https://code.visualstudio.com) 편집기와 Microsoft에서 제공하는 [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) 확장 프로그램 사용을 권장합니다.

<!-- Once these tools are installed, you may open any Laravel project by executing the `code .` command from your application's root directory using Windows Terminal. -->
이 도구들이 설치되면 Windows Terminal에서 애플리케이션의 루트 디렉터리로 이동한 뒤 `code .` 명령어를 실행하여 어떤 Laravel 프로젝트든 열 수 있습니다.

<a name="sail-on-linux"></a>
<!-- ### Sail on Linux -->
### Sail on Linux

<!-- If you're developing on Linux and [Docker Compose](https://docs.docker.com/compose/install/) is already installed, you can use a simple terminal command to create a new Laravel project. -->
Linux에서 개발 중이고 [Docker Compose](https://docs.docker.com/compose/install/)가 이미 설치되어 있다면, 간단한 터미널 명령어로 새 Laravel 프로젝트를 만들 수 있습니다.

<!-- First, if you are using Docker Desktop for Linux, you should execute the following command. If you are not using Docker Desktop for Linux, you may skip this step: -->
먼저 Linux용 Docker Desktop을 사용 중이라면 다음 명령어를 실행해야 합니다. Linux용 Docker Desktop을 사용하지 않는다면 이 단계는 건너뛰어도 됩니다.

```shell
docker context use default
```

<!-- Then, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
그런 다음 "example-app"이라는 디렉터리에 새 Laravel 애플리케이션을 만들려면 터미널에서 다음 명령어를 실행하면 됩니다.

```shell
curl -s https://laravel.build/example-app | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like - just make sure the application name only contains alpha-numeric characters, dashes, and underscores. The Laravel application's directory will be created within the directory you execute the command from. -->
물론 이 URL의 "example-app"은 원하는 이름으로 변경할 수 있습니다. 단, 애플리케이션 이름에는 영숫자, 하이픈, 밑줄만 포함되어야 합니다. Laravel 애플리케이션의 디렉터리는 명령어를 실행한 디렉터리 안에 생성됩니다.

<!-- Sail installation may take several minutes while Sail's application containers are built on your local machine. -->
Sail 애플리케이션 컨테이너가 로컬 머신에서 빌드되는 동안 Sail 설치에는 몇 분이 걸릴 수 있습니다.

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
프로젝트가 생성되면 애플리케이션 디렉터리로 이동하여 Laravel Sail을 시작할 수 있습니다. Laravel Sail은 Laravel의 기본 Docker 설정과 상호작용하기 위한 간단한 명령줄 인터페이스를 제공합니다.

```shell
cd example-app

./vendor/bin/sail up
```

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
애플리케이션의 Docker 컨테이너가 시작되면 웹 브라우저에서 다음 주소로 애플리케이션에 접근할 수 있습니다: http://localhost.

> [!NOTE]
> Laravel Sail에 대해 더 알아보려면 [complete documentation](/docs/10.x/sail)를 확인하세요.

<a name="choosing-your-sail-services"></a>
<!-- ### Choosing Your Sail Services -->
### Choosing Your Sail Services

<!-- When creating a new Laravel application via Sail, you may use the `with` query string variable to choose which services should be configured in your new application's `docker-compose.yml` file. Available services include `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `typesense`, `minio`, `selenium`, and `mailpit`: -->
Sail을 통해 새 Laravel 애플리케이션을 만들 때 `with` 쿼리 문자열 변수를 사용하여 새 애플리케이션의 `docker-compose.yml` 파일에 어떤 서비스를 설정할지 선택할 수 있습니다. 사용 가능한 서비스에는 `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `typesense`, `minio`, `selenium`, `mailpit`이 포함됩니다.
```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

<!-- If you do not specify which services you would like configured, a default stack of `mysql`, `redis`, `meilisearch`, `mailpit`, and `selenium` will be configured. -->
구성하려는 서비스를 지정하지 않으면 `mysql`, `redis`, `meilisearch`, `mailpit`, `selenium`으로 구성된 기본 스택이 설정됩니다.

<!-- You may instruct Sail to install a default [Devcontainer](/docs/10.x/sail#using-devcontainers) by adding the `devcontainer` parameter to the URL: -->
URL에 `devcontainer` 매개변수를 추가하여 Sail이 기본 [Devcontainer](/docs/10.x/sail#using-devcontainers)를 설치하도록 지시할 수 있습니다.

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="ide-support"></a>
<!-- ## IDE Support -->
## IDE Support

<!-- You are free to use any code editor you wish when developing Laravel applications; however, [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/) offers extensive support for Laravel and its ecosystem, including [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html). -->
Laravel 애플리케이션을 개발할 때 원하는 코드 편집기를 자유롭게 사용할 수 있습니다. 하지만 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)은 [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html)를 포함하여 Laravel과 그 생태계를 폭넓게 지원합니다.

<!-- In addition, the community maintained [Laravel Idea](https://laravel-idea.com/) PhpStorm plugin offers a variety of helpful IDE augmentations, including code generation, Eloquent syntax completion, validation rule completion, and more. -->
또한 커뮤니티에서 유지 관리하는 [Laravel Idea](https://laravel-idea.com/) PhpStorm 플러그인은 코드 생성, Eloquent 문법 자동 완성, 유효성 검증 규칙 자동 완성 등 다양한 유용한 IDE 확장 기능을 제공합니다.

<a name="laravel-and-ai"></a>
<!-- ## Laravel and AI -->
## Laravel and AI

<!-- [Laravel Boost](https://github.com/laravel/boost) is a powerful tool that bridges the gap between AI coding agents and Laravel applications. Boost provides AI agents with Laravel-specific context, tools, and guidelines so they can generate more accurate, version-specific code that follows Laravel conventions. -->
[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 Laravel 애플리케이션 사이의 간극을 메워 주는 강력한 도구입니다. Boost는 AI 에이전트에 Laravel 전용 컨텍스트, 도구, 지침을 제공하여 Laravel 규칙을 따르는 더 정확하고 버전별로 알맞은 코드를 생성할 수 있게 합니다.

<!-- When you install Boost in your Laravel application, AI agents gain access to over 15 specialized tools including the ability to know which packages you are using, query your database, search the Laravel documentation, read browser logs, generate tests, and execute code via Tinker. -->
Laravel 애플리케이션에 Boost를 설치하면 AI 에이전트는 사용 중인 패키지를 파악하고, 데이터베이스를 쿼리하고, Laravel 문서를 검색하고, 브라우저 로그를 읽고, 테스트를 생성하고, Tinker를 통해 코드를 실행하는 기능을 포함한 15개 이상의 전문 도구에 접근할 수 있습니다.

<!-- In addition, Boost gives AI agents access to over 17,000 pieces of vectorized Laravel ecosystem documentation, specific to your installed package versions. This means agents can provide guidance targeted to the exact versions your project uses. -->
또한 Boost는 설치된 패키지 버전에 맞춘 17,000개 이상의 벡터화된 Laravel 생태계 문서를 AI 에이전트에 제공합니다. 즉, 에이전트는 프로젝트에서 사용하는 정확한 버전에 맞는 안내를 제공할 수 있습니다.

<!-- Boost also includes Laravel-maintained AI guidelines that nudge agents to follow framework conventions, write appropriate tests, and avoid common pitfalls when generating Laravel code. -->
Boost에는 Laravel에서 유지 관리하는 AI 지침도 포함되어 있어, 에이전트가 Laravel 코드를 생성할 때 프레임워크 규칙을 따르고, 적절한 테스트를 작성하며, 흔한 실수를 피하도록 도와줍니다.

<a name="installing-laravel-boost"></a>
<!-- ### Installing Laravel Boost -->
### Installing Laravel Boost

<!-- Boost can be installed in Laravel 10, 11, and 12 applications running PHP 8.1 or higher. To get started, install Boost as a development dependency: -->
Boost는 PHP 8.1 이상에서 실행되는 Laravel 10, 11, 12 애플리케이션에 설치할 수 있습니다. 시작하려면 Boost를 개발 의존성으로 설치합니다.

```shell
composer require laravel/boost --dev
```

<!-- Once installed, run the interactive installer: -->
설치가 끝나면 대화형 설치 프로그램을 실행합니다.

```shell
php artisan boost:install
```

<!-- The installer will auto-detect your IDE and AI agents, allowing you to opt into the features that make sense for your project. Boost respects existing project conventions and doesn't force opinionated style rules by default. -->
설치 프로그램은 IDE와 AI 에이전트를 자동으로 감지하여, 프로젝트에 적합한 기능을 선택할 수 있게 합니다. Boost는 기존 프로젝트 규칙을 존중하며, 기본적으로 특정 스타일 규칙을 강제로 적용하지 않습니다.

> [!NOTE]
> Boost에 대해 더 자세히 알아보려면 [Laravel Boost repository on GitHub](https://github.com/laravel/boost)를 확인하십시오.

<a name="next-steps"></a>
<!-- ## Next Steps -->
## Next Steps

<!-- Now that you have created your Laravel project, you may be wondering what to learn next. First, we strongly recommend becoming familiar with how Laravel works by reading the following documentation: -->
이제 Laravel 프로젝트를 만들었으므로 다음에 무엇을 배워야 할지 궁금할 수 있습니다. 먼저 다음 문서를 읽으며 Laravel이 어떻게 작동하는지 익히는 것을 강력히 권장합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- [Request Lifecycle](/docs/10.x/lifecycle)
- [Configuration](/docs/10.x/configuration)
- [Directory Structure](/docs/10.x/structure)
- [Frontend](/docs/10.x/frontend)
- [Service Container](/docs/10.x/container)
- [Facades](/docs/10.x/facades)
-->
- [Request Lifecycle](/docs/10.x/lifecycle)
- [Configuration](/docs/10.x/configuration)
- [Directory Structure](/docs/10.x/structure)
- [Frontend](/docs/10.x/frontend)
- [Service Container](/docs/10.x/container)
- [Facades](/docs/10.x/facades)

<!-- </div> -->
</div>

<!-- How you want to use Laravel will also dictate the next steps on your journey. There are a variety of ways to use Laravel, and we'll explore two primary use cases for the framework below. -->
Laravel을 어떤 방식으로 사용하려는지에 따라 다음 단계도 달라집니다. Laravel을 사용하는 방법은 다양하며, 아래에서는 이 프레임워크의 두 가지 주요 사용 사례를 살펴보겠습니다.

> [!NOTE]
> Laravel이 처음이신가요? 첫 Laravel 애플리케이션을 만드는 과정을 함께 따라가며 프레임워크를 직접 익힐 수 있는 [Laravel Bootcamp](https://bootcamp.laravel.com)를 확인하십시오.

<a name="laravel-the-fullstack-framework"></a>
<!-- ### Laravel the Full Stack Framework -->
### Laravel the Full Stack Framework

<!-- Laravel may serve as a full stack framework. By "full stack" framework we mean that you are going to use Laravel to route requests to your application and render your frontend via [Blade templates](/docs/10.x/blade) or a single-page application hybrid technology like [Inertia](https://inertiajs.com). This is the most common way to use the Laravel framework, and, in our opinion, the most productive way to use Laravel. -->
Laravel은 풀 스택 프레임워크로 사용할 수 있습니다. 여기서 "풀 스택" 프레임워크란 Laravel을 사용해 애플리케이션으로 들어오는 요청을 라우팅하고, [Blade templates](/docs/10.x/blade) 또는 [Inertia](https://inertiajs.com)와 같은 단일 페이지 애플리케이션 하이브리드 기술을 통해 프론트엔드를 렌더링한다는 의미입니다. 이는 Laravel 프레임워크를 사용하는 가장 일반적인 방식이며, 저희가 생각하기에 Laravel을 가장 생산적으로 사용하는 방식입니다.

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [frontend development](/docs/10.x/frontend), [routing](/docs/10.x/routing), [views](/docs/10.x/views), or the [Eloquent ORM](/docs/10.x/eloquent). In addition, you might be interested in learning about community packages like [Livewire](https://livewire.laravel.com) and [Inertia](https://inertiajs.com). These packages allow you to use Laravel as a full-stack framework while enjoying many of the UI benefits provided by single-page JavaScript applications. -->
Laravel을 이런 방식으로 사용할 계획이라면 [frontend development](/docs/10.x/frontend), [routing](/docs/10.x/routing), [views](/docs/10.x/views), [Eloquent ORM](/docs/10.x/eloquent)에 관한 문서를 확인해 보십시오. 또한 [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 같은 커뮤니티 패키지를 배우는 것도 도움이 될 수 있습니다. 이러한 패키지를 사용하면 단일 페이지 JavaScript 애플리케이션이 제공하는 다양한 UI 장점을 누리면서도 Laravel을 풀 스택 프레임워크로 사용할 수 있습니다.

<!-- If you are using Laravel as a full stack framework, we also strongly encourage you to learn how to compile your application's CSS and JavaScript using [Vite](/docs/10.x/vite). -->
Laravel을 풀 스택 프레임워크로 사용한다면 [Vite](/docs/10.x/vite)를 사용해 애플리케이션의 CSS와 JavaScript를 컴파일하는 방법도 반드시 익히는 것이 좋습니다.

> [!NOTE]
> 애플리케이션 개발을 빠르게 시작하고 싶다면 공식 [application starter kits](/docs/10.x/starter-kits) 중 하나를 확인하십시오.

<a name="laravel-the-api-backend"></a>
<!-- ### Laravel the API Backend -->
### Laravel the API Backend

<!-- Laravel may also serve as an API backend to a JavaScript single-page application or mobile application. For example, you might use Laravel as an API backend for your [Next.js](https://nextjs.org) application. In this context, you may use Laravel to provide [authentication](/docs/10.x/sanctum) and data storage / retrieval for your application, while also taking advantage of Laravel's powerful services such as queues, emails, notifications, and more. -->
Laravel은 JavaScript 단일 페이지 애플리케이션이나 모바일 애플리케이션을 위한 API 백엔드로도 사용할 수 있습니다. 예를 들어 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 사용할 수 있습니다. 이 경우 Laravel을 사용해 애플리케이션에 [authentication](/docs/10.x/sanctum)과 데이터 저장 및 조회 기능을 제공하면서, 큐, 이메일, 알림 등 Laravel의 강력한 서비스도 함께 활용할 수 있습니다.

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/10.x/routing), [Laravel Sanctum](/docs/10.x/sanctum), and the [Eloquent ORM](/docs/10.x/eloquent). -->
Laravel을 이런 방식으로 사용할 계획이라면 [routing](/docs/10.x/routing), [Laravel Sanctum](/docs/10.x/sanctum), [Eloquent ORM](/docs/10.x/eloquent)에 관한 문서를 확인해 보십시오.

> [!NOTE]
> Laravel 백엔드와 Next.js 프론트엔드의 스캐폴딩을 빠르게 시작해야 하나요? Laravel Breeze는 [API stack](/docs/10.x/starter-kits#breeze-and-next)과 [Next.js frontend implementation](https://github.com/laravel/breeze-next)을 제공하므로 몇 분 안에 시작할 수 있습니다.
