---
slug: /
---

<!-- # Installation -->
# Installation

- [Meet Laravel](#meet-laravel)
    - [Why Laravel?](#why-laravel)
- [Your First Laravel Project](#your-first-laravel-project)
- [Laravel & Docker](#laravel-and-docker)
    - [Getting Started On macOS](#getting-started-on-macos)
    - [Getting Started On Windows](#getting-started-on-windows)
    - [Getting Started On Linux](#getting-started-on-linux)
    - [Choosing Your Sail Services](#choosing-your-sail-services)
- [Initial Configuration](#initial-configuration)
    - [Environment Based Configuration](#environment-based-configuration)
    - [Databases & Migrations](#databases-and-migrations)
- [Next Steps](#next-steps)
    - [Laravel The Full Stack Framework](#laravel-the-fullstack-framework)
    - [Laravel The API Backend](#laravel-the-api-backend)

<a name="meet-laravel"></a>
<!-- ## Meet Laravel -->
## Meet Laravel

<!-- Laravel is a web application framework with expressive, elegant syntax. A web framework provides a structure and starting point for creating your application, allowing you to focus on creating something amazing while we sweat the details. -->
Laravel은 표현력 있고 우아한 문법을 제공하는 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 기본 구조와 시작점을 제공하므로, 여러분은 복잡한 부분은 우리가 처리하는 사이 멋진 것을 만드는 데 집중할 수 있습니다.

<!-- Laravel strives to provide an amazing developer experience while providing powerful features such as thorough dependency injection, an expressive database abstraction layer, queues and scheduled jobs, unit and integration testing, and more. -->
Laravel은 개발자가 뛰어난 경험을 얻을 수 있도록 노력하는 동시에, 강력한 기능도 제공합니다. 대표적으로 강력한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 테스트 및 통합 테스트 등의 기능이 있습니다.

<!-- Whether you are new to PHP web frameworks or have years of experience, Laravel is a framework that can grow with you. We'll help you take your first steps as a web developer or give you a boost as you take your expertise to the next level. We can't wait to see what you build. -->
PHP 웹 프레임워크가 처음인 분부터 다년간 경험이 있는 분까지, Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 처음 웹 개발을 시작하는 분이라면 저희가 첫걸음을 도와드릴 것이고, 전문가라면 기술을 한 단계 끌어올리는 데 도움이 되어드릴 것입니다. 여러분이 어떤 것을 만들어갈지 기대하고 있습니다.

> [!NOTE]
> Laravel이 처음이신가요? [Laravel Bootcamp](https://bootcamp.laravel.com)에서 실습을 통해 Laravel을 다루는 법을 배워보세요. 여러분의 첫 번째 Laravel 애플리케이션을 만드는 과정을 함께 안내해드립니다.

<a name="why-laravel"></a>
<!-- ### Why Laravel? -->
### Why Laravel?

<!-- There are a variety of tools and frameworks available to you when building a web application. However, we believe Laravel is the best choice for building modern, full-stack web applications. -->
웹 애플리케이션을 만들 때 다양한 도구와 프레임워크를 선택할 수 있습니다. 하지만 저희는 Laravel이 최신의 풀스택 웹 애플리케이션 개발에 가장 적합한 선택이라고 생각합니다.

<!-- #### A Progressive Framework -->
#### A Progressive Framework

<!-- We like to call Laravel a "progressive" framework. By that, we mean that Laravel grows with you. If you're just taking your first steps into web development, Laravel's vast library of documentation, guides, and [video tutorials](https://laracasts.com) will help you learn the ropes without becoming overwhelmed. -->
Laravel은 "진보적(progressive)" 프레임워크라고 부르기도 합니다. 즉, Laravel은 개발자와 함께 성장합니다. 웹 개발을 처음 시작하는 분이라면 Laravel의 방대한 문서, 가이드, [video tutorials](https://laracasts.com)을 활용해 부담 없이 기초부터 학습할 수 있습니다.

<!-- If you're a senior developer, Laravel gives you robust tools for [dependency injection](/docs/9.x/container), [unit testing](/docs/9.x/testing), [queues](/docs/9.x/queues), [real-time events](/docs/9.x/broadcasting), and more. Laravel is fine-tuned for building professional web applications and ready to handle enterprise work loads. -->
경험 많은 시니어 개발자라면, Laravel은 [dependency injection](/docs/9.x/container), [unit testing](/docs/9.x/testing), [queues](/docs/9.x/queues), [real-time events](/docs/9.x/broadcasting) 등 강력한 도구들을 제공합니다. Laravel은 전문적인 웹 애플리케이션 개발을 위해 최적화되어 있으며, 엔터프라이즈급 대규모 트래픽도 문제없이 대응할 수 있습니다.

<!-- #### A Scalable Framework -->
#### A Scalable Framework

<!-- Laravel is incredibly scalable. Thanks to the scaling-friendly nature of PHP and Laravel's built-in support for fast, distributed cache systems like Redis, horizontal scaling with Laravel is a breeze. In fact, Laravel applications have been easily scaled to handle hundreds of millions of requests per month. -->
Laravel은 매우 높은 확장성을 자랑합니다. PHP의 확장성 좋은 특성과, Laravel이 내장 지원하는 Redis와 같은 빠르고 분산된 캐시 시스템 덕분에, 수평 확장이 매우 쉽습니다. 실제로 Laravel로 개발한 애플리케이션이 매달 수억 건의 요청을 처리한 사례도 있습니다.

<!-- Need extreme scaling? Platforms like [Laravel Vapor](https://vapor.laravel.com) allow you to run your Laravel application at nearly limitless scale on AWS's latest serverless technology. -->
더 극한의 확장이 필요하다면? [Laravel Vapor](https://vapor.laravel.com)와 같은 플랫폼을 이용하면 AWS의 최신 서버리스(Serverless) 기술로 Laravel 애플리케이션을 사실상 무한대에 가깝게 확장할 수 있습니다.

<!-- #### A Community Framework -->
#### A Community Framework

<!-- Laravel combines the best packages in the PHP ecosystem to offer the most robust and developer friendly framework available. In addition, thousands of talented developers from around the world have [contributed to the framework](https://github.com/laravel/framework). Who knows, maybe you'll even become a Laravel contributor. -->
Laravel은 PHP 생태계에서 최고의 패키지를 결합하여 가장 강력하고 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수많은 능력 있는 개발자가 [contributed to the framework](https://github.com/laravel/framework)하고 있습니다. 여러분도 언젠가 Laravel의 기여자가 될 수도 있겠죠.

<a name="your-first-laravel-project"></a>
<!-- ## Your First Laravel Project -->
## Your First Laravel Project

<!-- Before creating your first Laravel project, you should ensure that your local machine has PHP and [Composer](https://getcomposer.org) installed. If you are developing on macOS, PHP and Composer can be installed via [Homebrew](https://brew.sh/). In addition, we recommend [installing Node and NPM](https://nodejs.org). -->
첫 Laravel 프로젝트를 생성하기 전, 로컬 머신에 PHP와 [Composer](https://getcomposer.org)가 설치되어 있는지 확인하세요. macOS 환경에서는 [Homebrew](https://brew.sh/)를 사용해 PHP와 Composer를 설치할 수 있습니다. 또한, [installing Node and NPM](https://nodejs.org)도 권장합니다.

<!-- After you have installed PHP and Composer, you may create a new Laravel project via the Composer `create-project` command: -->
PHP와 Composer 설치를 마친 후, Composer의 `create-project` 명령어로 새 Laravel 프로젝트를 생성할 수 있습니다:

```nothing
composer create-project laravel/laravel:^9.0 example-app
```

<!-- Or, you may create new Laravel projects by globally installing the Laravel installer via Composer: -->
또는 Composer를 통해 Laravel 인스톨러를 전역(global)으로 설치한 뒤, 다음과 같이 새 프로젝트를 생성할 수도 있습니다:

```nothing
composer global require laravel/installer

laravel new example-app
```

<!-- After the project has been created, start Laravel's local development server using the Laravel's Artisan CLI `serve` command: -->
프로젝트가 생성되면, Laravel의 Artisan CLI에서 제공하는 `serve` 명령어로 로컬 개발 서버를 시작하세요:

```nothing
cd example-app

php artisan serve
```

<!-- Once you have started the Artisan development server, your application will be accessible in your web browser at `http://localhost:8000`. Next, you're ready to [start taking your next steps into the Laravel ecosystem](#next-steps). Of course, you may also want to [configure a database](#databases-and-migrations). -->
Artisan 개발 서버를 시작하면, 브라우저에서 `http://localhost:8000` 주소로 애플리케이션에 접속할 수 있습니다. 이제 [start taking your next steps into the Laravel ecosystem](#next-steps) 나아갈 준비가 되었습니다. 물론, [configure a database](#databases-and-migrations)도 바로 진행하실 수 있습니다.

> [!NOTE]
> Laravel 애플리케이션을 빠르게 시작하고 싶다면, 공식 [starter kits](/docs/9.x/starter-kits)를 활용해보세요. Laravel의 스타터 키트는 신규 애플리케이션을 위한 백엔드와 프론트엔드 인증 기능을 손쉽게 제공합니다.

<a name="laravel-and-docker"></a>
<!-- ## Laravel & Docker -->
## Laravel & Docker

<!-- We want it to be as easy as possible to get started with Laravel regardless of your preferred operating system. So, there are a variety of options for developing and running a Laravel project on your local machine. While you may wish to explore these options at a later time, Laravel provides [Sail](/docs/9.x/sail), a built-in solution for running your Laravel project using [Docker](https://www.docker.com). -->
선호하는 운영 체제와 상관없이 Laravel을 최대한 쉽게 시작할 수 있도록 다양한 개발 환경 옵션을 제공합니다. 이 옵션들은 추후 다양하게 살펴볼 수 있지만, Laravel은 [Sail](/docs/9.x/sail)이라는 내장 솔루션을 통해 [Docker](https://www.docker.com)를 이용한 프로젝트 실행을 지원합니다.

<!-- Docker is a tool for running applications and services in small, light-weight "containers" which do not interfere with your local machine's installed software or configuration. This means you don't have to worry about configuring or setting up complicated development tools such as web servers and databases on your local machine. To get started, you only need to install [Docker Desktop](https://www.docker.com/products/docker-desktop). -->
Docker는 작은 크기의 "컨테이너" 환경에서 애플리케이션과 서비스를 실행할 수 있게 해주는 도구입니다. 이 컨테이너는 로컬 머신의 기존 소프트웨어나 설정에 영향을 주지 않으므로, 복잡한 웹 서버나 데이터베이스와 같은 개발 도구를 따로 설치하거나 설정할 필요가 없습니다. 시작을 위해선 [Docker Desktop](https://www.docker.com/products/docker-desktop)만 설치하면 됩니다.

<!-- Laravel Sail is a light-weight command-line interface for interacting with Laravel's default Docker configuration. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience. -->
Laravel Sail은 Laravel의 기본 Docker 설정을 손쉽게 다룰 수 있도록 해 주는 경량 명령줄 인터페이스입니다. Sail을 사용하면, Docker에 대한 사전 지식 없이도 PHP, MySQL, Redis를 활용한 Laravel 애플리케이션 개발을 바로 시작할 수 있습니다.

> [!NOTE]
> 이미 Docker에 익숙하다면 걱정하지 마세요! Sail의 모든 구성은 Laravel에 포함된 `docker-compose.yml` 파일을 통해 자유롭게 커스터마이즈할 수 있습니다.

<a name="getting-started-on-macos"></a>
<!-- ### Getting Started On macOS -->
### Getting Started On macOS

<!-- If you're developing on a Mac and [Docker Desktop](https://www.docker.com/products/docker-desktop) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
Mac에서 개발 중이고 [Docker Desktop](https://www.docker.com/products/docker-desktop)이 설치되어 있다면, 터미널에서 간단한 명령어로 새 Laravel 프로젝트를 만들 수 있습니다. 예를 들어, "example-app" 폴더에 Laravel 애플리케이션을 만들려면 다음 명령어를 실행하세요:

```shell
curl -s "https://laravel.build/example-app" | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like - just make sure the application name only contains alpha-numeric characters, dashes, and underscores. The Laravel application's directory will be created within the directory you execute the command from. -->
물론, 위 URL의 "example-app" 부분은 원하는 이름으로 변경할 수 있습니다. 애플리케이션 이름에는 영문자, 숫자, 하이픈(-), 밑줄(_)만 사용할 수 있습니다. Laravel 애플리케이션 디렉터리는 명령어를 실행한 현재 디렉터리 안에 만들어집니다.

<!-- Sail installation may take several minutes while Sail's application containers are built on your local machine. -->
Sail 설치 과정에서 컨테이너 빌드가 진행되므로, 약간의 시간이 걸릴 수 있습니다.

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
프로젝트 생성 후에는 앱 디렉터리로 이동해서 Laravel Sail을 실행할 수 있습니다. Sail은 Laravel 기본 Docker 설정을 다루는 간단한 명령줄 인터페이스를 제공합니다:

```shell
cd example-app

./vendor/bin/sail up
```

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
애플리케이션의 Docker 컨테이너가 모두 실행되면, 웹 브라우저에서 http://localhost 주소로 접속할 수 있습니다.

> [!NOTE]
> Laravel Sail에 대해 더 자세히 알고 싶다면 [complete documentation](/docs/9.x/sail)를 참고하세요.

<a name="getting-started-on-windows"></a>
<!-- ### Getting Started On Windows -->
### Getting Started On Windows

<!-- Before we create a new Laravel application on your Windows machine, make sure to install [Docker Desktop](https://www.docker.com/products/docker-desktop). Next, you should ensure that Windows Subsystem for Linux 2 (WSL2) is installed and enabled. WSL allows you to run Linux binary executables natively on Windows 10. Information on how to install and enable WSL2 can be found within Microsoft's [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10). -->
Windows에서 새 Laravel 애플리케이션을 만들기 전에 [Docker Desktop](https://www.docker.com/products/docker-desktop)을 먼저 설치해야 합니다. 그 다음, Windows Subsystem for Linux 2(WSL2)가 설치 및 활성화되어 있어야 합니다. WSL을 이용하면 Windows 10에서 리눅스 바이너리 실행 파일을 네이티브로 사용할 수 있습니다. WSL2 설치와 활성화에 관한 방법은 Microsoft의 [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10)에서 확인할 수 있습니다.

> [!NOTE]
> WSL2를 설치하고 활성화한 후에는 반드시 Docker Desktop이 [configured to use the WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/)되어 있어야 합니다.

<!-- Next, you are ready to create your first Laravel project. Launch [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) and begin a new terminal session for your WSL2 Linux operating system. Next, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
이제 새 Laravel 프로젝트를 만들 준비가 되었습니다. [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)을 실행하여, WSL2 Linux 터미널 세션을 시작하세요. 그 다음, 아래 명령어로 새 Laravel 프로젝트를 만들 수 있습니다. 예시로 "example-app" 디렉터리에 Laravel 애플리케이션을 생성하려면, 터미널에서 다음을 실행하세요:

```shell
curl -s https://laravel.build/example-app | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like - just make sure the application name only contains alpha-numeric characters, dashes, and underscores. The Laravel application's directory will be created within the directory you execute the command from. -->
물론, 위 URL의 "example-app" 부분은 원하는 이름으로 수정해도 됩니다. 이름은 영문자, 숫자, 하이픈(-), 밑줄(_)만 포함할 수 있습니다. Laravel 애플리케이션 디렉터리는 명령어를 실행한 현재 위치에 생성됩니다.

<!-- Sail installation may take several minutes while Sail's application containers are built on your local machine. -->
Sail 설치 작업에서 컨테이너 빌드가 이루어지므로 수 분 정도가 소요될 수 있습니다.

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
프로젝트가 생성된 후에는 애플리케이션 디렉터리로 이동하여 Laravel Sail을 실행하세요. Sail은 Laravel 기본 Docker 설정을 손쉽게 다루는 명령줄 인터페이스를 제공합니다:

```shell
cd example-app

./vendor/bin/sail up
```

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
애플리케이션 컨테이너가 실행되면, 브라우저에서 http://localhost 로 애플리케이션에 접속할 수 있습니다.

> [!NOTE]
> Laravel Sail 사용법을 더 자세히 알고 싶으시면 [complete documentation](/docs/9.x/sail)를 참고하세요.

<!-- #### Developing Within WSL2 -->
#### Developing Within WSL2

<!-- Of course, you will need to be able to modify the Laravel application files that were created within your WSL2 installation. To accomplish this, we recommend using Microsoft's [Visual Studio Code](https://code.visualstudio.com) editor and their first-party extension for [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack). -->
WSL2 환경에 생성된 Laravel 애플리케이션의 파일을 수정하려면, Microsoft의 [Visual Studio Code](https://code.visualstudio.com) 에디터와 공식 [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) 사용을 추천합니다.

<!-- Once these tools are installed, you may open any Laravel project by executing the `code .` command from your application's root directory using Windows Terminal. -->
이 도구들을 설치한 후, Windows Terminal에서 애플리케이션 루트 디렉터리에서 `code .` 명령어를 실행하면 언제든 Laravel 프로젝트를 Visual Studio Code로 열 수 있습니다.

<a name="getting-started-on-linux"></a>
<!-- ### Getting Started On Linux -->
### Getting Started On Linux

<!-- If you're developing on Linux and [Docker Compose](https://docs.docker.com/compose/install/) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
Linux 환경에서 개발 중이고 [Docker Compose](https://docs.docker.com/compose/install/)가 설치되어 있다면, 다음의 명령어로 곧바로 새 Laravel 프로젝트를 만들 수 있습니다. 예를 들어 "example-app" 디렉터리에 Laravel 애플리케이션을 생성하려면, 터미널에서 다음을 실행하세요:

```shell
curl -s https://laravel.build/example-app | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like - just make sure the application name only contains alpha-numeric characters, dashes, and underscores. The Laravel application's directory will be created within the directory you execute the command from. -->
마찬가지로 URL의 "example-app"은 원하는 이름으로 변경할 수 있으며, 이름에는 영문, 숫자, 하이픈(-), 밑줄(_)만 사용할 수 있습니다. 애플리케이션 디렉터리는 현재 경로에 생성됩니다.

<!-- Sail installation may take several minutes while Sail's application containers are built on your local machine. -->
Sail의 설치 및 애플리케이션 컨테이너 빌드에는 몇 분 정도 소요될 수 있습니다.

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
프로젝트가 만들어지면 앱 디렉터리로 이동해서 Laravel Sail을 실행하세요. Sail은 Laravel의 기본 Docker 설정을 관리할 수 있는 명령줄 도구를 제공합니다:

```shell
cd example-app

./vendor/bin/sail up
```

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
컨테이너가 모두 실행되면, 브라우저에서 http://localhost 주소로 접근할 수 있습니다.

> [!NOTE]
> Laravel Sail에 대해 더 알아보고 싶다면 [complete documentation](/docs/9.x/sail)를 참고하세요.

<a name="choosing-your-sail-services"></a>
<!-- ### Choosing Your Sail Services -->
### Choosing Your Sail Services

<!-- When creating a new Laravel application via Sail, you may use the `with` query string variable to choose which services should be configured in your new application's `docker-compose.yml` file. Available services include `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `minio`, `selenium`, and `mailpit`: -->
Sail을 이용해 새 Laravel 애플리케이션을 만들 때, `with` 쿼리 스트링 변수로 `docker-compose.yml`에 어떤 서비스를 추가할지 선택할 수 있습니다. 사용 가능한 서비스에는 `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `minio`, `selenium`, `mailpit` 등이 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

<!-- If you do not specify which services you would like configured, a default stack of `mysql`, `redis`, `meilisearch`, `mailpit`, and `selenium` will be configured. -->
특정 서비스를 지정하지 않으면, 기본적으로 `mysql`, `redis`, `meilisearch`, `mailpit`, `selenium`이 포함된 스택이 설정됩니다.

<!-- You may instruct Sail to install a default [Devcontainer](/docs/9.x/sail#using-devcontainers) by adding the `devcontainer` parameter to the URL: -->
또한 URL에 `devcontainer` 파라미터를 추가해, Sail이 기본 [Devcontainer](/docs/9.x/sail#using-devcontainers)를 설치하도록 할 수 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="initial-configuration"></a>
<!-- ## Initial Configuration -->
## Initial Configuration

<!-- All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you. -->
Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 모여 있습니다. 각 설정 옵션마다 자세한 설명이 작성되어 있으니, 시간을 내어 옵션들을 살펴보고 익숙해지세요.

<!-- Laravel needs almost no additional configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your application. -->
Laravel은 기본적으로 추가적인 설정 없이 바로 개발을 시작할 수 있게 설계되었습니다. 지금 바로 코딩을 시작해도 문제 없습니다! 하지만 필요하다면 `config/app.php` 파일과 관련 문서를 확인해보세요. 이 파일에는 `timezone`, `locale` 등 상황에 맞게 변경할 수 있는 다양한 옵션이 있습니다.

<a name="environment-based-configuration"></a>
<!-- ### Environment Based Configuration -->
### Environment Based Configuration

<!-- Since many of Laravel's configuration option values may vary depending on whether your application is running on your local machine or on a production web server, many important configuration values are defined using the `.env` file that exists at the root of your application. -->
Laravel의 설정 옵션 값들은, 애플리케이션이 로컬 머신에서 실행되는지 프로덕션 서버에서 동작하는지에 따라 달라질 수 있습니다. 이를 위해 많은 주요 설정 값이 애플리케이션 루트에 위치한 `.env` 파일에 정의되어 있습니다.

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed. -->
`.env` 파일은 각 개발자나 서버에서 서로 다른 환경 구성이 필요하기 때문에, 소스코드 저장소에는 포함하지 않아야 합니다. 게다가, 만약 소스코드 저장소에 접근 권한이 없는 사람이 접근하게 될 경우 중요한 자격 증명이 유출될 수 있으니 보안상 매우 위험합니다.

> [!NOTE]
> `.env` 파일과 환경 기반 설정에 대한 자세한 내용은 [configuration documentation](/docs/9.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
<!-- ### Databases & Migrations -->
### Databases & Migrations

<!-- Now that you have created your Laravel application, you probably want to store some data in a database. By default, your application's `.env` configuration file specifies that Laravel will be interacting with a MySQL database and will access the database at `127.0.0.1`. If you are developing on macOS and need to install MySQL, Postgres, or Redis locally, you may find it convenient to utilize [DBngin](https://dbngin.com/). -->
이제 Laravel 애플리케이션을 만들었으니, 데이터를 데이터베이스에 저장하고 싶을 것입니다. 기본적으로 `.env` 설정 파일에는 MySQL 데이터베이스와 `127.0.0.1` 주소로 접속하도록 지정되어 있습니다. macOS에서 MySQL, Postgres, Redis 등의 설치가 필요하다면 [DBngin](https://dbngin.com/)을 사용하면 간편하게 설치할 수 있습니다.

<!-- If you do not want to install MySQL or Postgres on your local machine, you can always use a [SQLite](https://www.sqlite.org/index.html) database. SQLite is a small, fast, self-contained database engine. To get started, update your `.env` configuration file to use Laravel's `sqlite` database driver. You may remove the other database configuration options: -->
로컬 머신에 MySQL이나 Postgres를 설치하고 싶지 않다면, [SQLite](https://www.sqlite.org/index.html) 데이터베이스도 사용할 수 있습니다. SQLite는 작고 빠르며 자체적으로 독립적인 데이터베이스 엔진입니다. 사용하려면 `.env` 파일에서 Laravel의 `sqlite` 데이터베이스 드라이버를 지정하면 됩니다. 그 외 다른 데이터베이스 설정은 삭제해도 됩니다:

```ini
DB_CONNECTION=sqlite # [tl! add]
DB_CONNECTION=mysql # [tl! remove]
DB_HOST=127.0.0.1 # [tl! remove]
DB_PORT=3306 # [tl! remove]
DB_DATABASE=laravel # [tl! remove]
DB_USERNAME=root # [tl! remove]
DB_PASSWORD= # [tl! remove]
```

<!-- Once you have configured your SQLite database, you may run your application's [database migrations](/docs/9.x/migrations), which will create your application's database tables: -->
SQLite 데이터베이스 설정을 마친 후에는 [database migrations](/docs/9.x/migrations) 명령어로 애플리케이션의 데이터베이스 테이블을 생성할 수 있습니다:

```shell
php artisan migrate
```

<!-- If an SQLite database does not exist for your application, Laravel will ask you if you would like the database to be created. Typically, the SQLite database file will be created at `database/database.sqlite`. -->
애플리케이션에 SQLite 데이터베이스 파일이 없다면, Laravel이 생성 여부를 묻고 직접 파일까지 만들어줍니다. 보통 `database/database.sqlite` 위치에 데이터베이스 파일이 생성됩니다.

<a name="next-steps"></a>
<!-- ## Next Steps -->
## Next Steps

<!-- Now that you have created your Laravel project, you may be wondering what to learn next. First, we strongly recommend becoming familiar with how Laravel works by reading the following documentation: -->
Laravel 프로젝트를 만들었다면, 이제 무엇을 배워야 할지 궁금하실 수 있습니다. 먼저 Laravel의 동작 방식을 잘 이해하기 위해 아래 문서를 읽어보는 것을 강력히 추천합니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- [Request Lifecycle](/docs/9.x/lifecycle)
- [Configuration](/docs/9.x/configuration)
- [Directory Structure](/docs/9.x/structure)
- [Frontend](/docs/9.x/frontend)
- [Service Container](/docs/9.x/container)
- [Facades](/docs/9.x/facades)
-->
- [Request Lifecycle](/docs/9.x/lifecycle)
- [Configuration](/docs/9.x/configuration)
- [Directory Structure](/docs/9.x/structure)
- [Frontend](/docs/9.x/frontend)
- [Service Container](/docs/9.x/container)
- [Facades](/docs/9.x/facades)

<!-- </div> -->
</div>

<!-- How you want to use Laravel will also dictate the next steps on your journey. There are a variety of ways to use Laravel, and we'll explore two primary use cases for the framework below. -->
Laravel을 사용하는 방식에 따라 앞으로의 학습 단계도 달라집니다. Laravel은 여러가지 방식으로 사용할 수 있는데, 아래에서는 대표적인 두 가지 주요 사용 사례를 살펴보겠습니다.

> [!NOTE]
> Laravel이 처음이라면, [Laravel Bootcamp](https://bootcamp.laravel.com)에서 직접 애플리케이션을 만들며 프레임워크를 체험해보세요.

<a name="laravel-the-fullstack-framework"></a>
<!-- ### Laravel The Full Stack Framework -->
### Laravel The Full Stack Framework

<!-- Laravel may serve as a full stack framework. By "full stack" framework we mean that you are going to use Laravel to route requests to your application and render your frontend via [Blade templates](/docs/9.x/blade) or a single-page application hybrid technology like [Inertia](https://inertiajs.com). This is the most common way to use the Laravel framework, and, in our opinion, the most productive way to use Laravel. -->
Laravel은 풀스택(Full Stack) 프레임워크로 사용할 수 있습니다. 여기서 "풀스택"이란, Laravel이 요청 라우팅을 담당하고 [Blade templates](/docs/9.x/blade)이나 [Inertia](https://inertiajs.com)와 같은 SPA(싱글 페이지 애플리케이션) 하이브리드 기술로 프론트엔드를 렌더링하는 방식을 말합니다. 이는 Laravel을 사용하는 가장 일반적이며, 저희가 생각하기에도 가장 생산적인 방법입니다.

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [frontend development](/docs/9.x/frontend), [routing](/docs/9.x/routing), [views](/docs/9.x/views), or the [Eloquent ORM](/docs/9.x/eloquent). In addition, you might be interested in learning about community packages like [Livewire](https://laravel-livewire.com) and [Inertia](https://inertiajs.com). These packages allow you to use Laravel as a full-stack framework while enjoying many of the UI benefits provided by single-page JavaScript applications. -->
이런 방식으로 Laravel을 사용할 계획이라면 [frontend development](/docs/9.x/frontend), [routing](/docs/9.x/routing), [views](/docs/9.x/views), [Eloquent ORM](/docs/9.x/eloquent) 관련 문서를 참고해보세요. 또한, [Livewire](https://laravel-livewire.com), [Inertia](https://inertiajs.com)와 같은 커뮤니티 패키지에도 관심을 가져볼만합니다. 이러한 패키지 덕분에 자바스크립트 SPA의 장점과 Laravel의 풀스택 프레임워크 기능을 함께 누릴 수 있습니다.

<!-- If you are using Laravel as a full stack framework, we also strongly encourage you to learn how to compile your application's CSS and JavaScript using [Vite](/docs/9.x/vite). -->
Laravel을 풀스택 프레임워크로 쓸 경우, [Vite](/docs/9.x/vite)를 활용해 애플리케이션의 CSS와 자바스크립트 빌드 방법도 꼭 공부해보시길 추천합니다.

> [!NOTE]
> 애플리케이션 개발에 빠르게 착수하고 싶으시면, 공식 [application starter kits](/docs/9.x/starter-kits)를 참고하세요.

<a name="laravel-the-api-backend"></a>
<!-- ### Laravel The API Backend -->
### Laravel The API Backend

<!-- Laravel may also serve as an API backend to a JavaScript single-page application or mobile application. For example, you might use Laravel as an API backend for your [Next.js](https://nextjs.org) application. In this context, you may use Laravel to provide [authentication](/docs/9.x/sanctum) and data storage / retrieval for your application, while also taking advantage of Laravel's powerful services such as queues, emails, notifications, and more. -->
Laravel은 자바스크립트 싱글 페이지 애플리케이션(SPA)이나 모바일 애플리케이션을 위한 백엔드 API로도 사용할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 사용할 수 있습니다. 이 경우, Laravel은 인증 기능([authentication](/docs/9.x/sanctum)), 데이터 저장 및 조회 등은 물론, 큐, 이메일, 알림 등 Laravel의 강력한 서비스를 모두 제공할 수 있습니다.

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/9.x/routing), [Laravel Sanctum](/docs/9.x/sanctum), and the [Eloquent ORM](/docs/9.x/eloquent). -->
이런 방식의 사용이 목표라면 [routing](/docs/9.x/routing), [Laravel Sanctum](/docs/9.x/sanctum), [Eloquent ORM](/docs/9.x/eloquent) 관련 문서를 참고해보세요.

> [!NOTE]
> Laravel 백엔드와 Next.js 프론트엔드의 시작 뼈대를 빠르게 만들고 싶다면, Laravel Breeze에서 [API stack](/docs/9.x/starter-kits#breeze-and-next)과 [Next.js frontend implementation](https://github.com/laravel/breeze-next)를 지원하니, 바로 사용해보실 수 있습니다.
