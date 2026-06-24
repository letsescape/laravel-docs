---
slug: /
---

<!-- # Installation -->
# Installation

- [Meet Laravel](#meet-laravel)
    - [Why Laravel?](#why-laravel)
- [Your First Laravel Project](#your-first-laravel-project)
    - [Getting Started On macOS](#getting-started-on-macos)
    - [Getting Started On Windows](#getting-started-on-windows)
    - [Getting Started On Linux](#getting-started-on-linux)
    - [Choosing Your Sail Services](#choosing-your-sail-services)
    - [Installation Via Composer](#installation-via-composer)
- [Initial Configuration](#initial-configuration)
    - [Environment Based Configuration](#environment-based-configuration)
    - [Directory Configuration](#directory-configuration)
- [Next Steps](#next-steps)
    - [Laravel The Full Stack Framework](#laravel-the-fullstack-framework)
    - [Laravel The API Backend](#laravel-the-api-backend)

<a name="meet-laravel"></a>
<!-- ## Meet Laravel -->
## Meet Laravel

<!-- Laravel is a web application framework with expressive, elegant syntax. A web framework provides a structure and starting point for creating your application, allowing you to focus on creating something amazing while we sweat the details. -->
Laravel은 표현적이고 우아한 문법을 제공하는 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들 때 구조와 시작점을 제공하므로, 여러분은 세부적인 기술 설정에 얽매이지 않고 멋진 결과물에 집중할 수 있습니다.

<!-- Laravel strives to provide an amazing developer experience while providing powerful features such as thorough dependency injection, an expressive database abstraction layer, queues and scheduled jobs, unit and integration testing, and more. -->
Laravel은 강력한 기능(예: 완전한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 테스트와 통합 테스트 등)은 물론, 개발자가 멋진 경험을 누릴 수 있도록 끊임없이 노력하고 있습니다.

<!-- Whether you are new to PHP or web frameworks or have years of experience, Laravel is a framework that can grow with you. We'll help you take your first steps as a web developer or give you a boost as you take your expertise to the next level. We can't wait to see what you build. -->
PHP나 웹 프레임워크가 처음인 분도, 수년간 경험이 있으신 분도 Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 여러분이 웹 개발자에 첫 발을 내딛도록 도와드릴 수도 있고, 이미 숙련된 분이라면 새로운 수준에 도달하도록 한 단계 더 도약할 수 있도록 지원합니다. 여러분이 Laravel로 어떤 멋진 것을 만들지 저희도 무척 기대하고 있습니다.

<a name="why-laravel"></a>
<!-- ### Why Laravel? -->
### Why Laravel?

<!-- There are a variety of tools and frameworks available to you when building a web application. However, we believe Laravel is the best choice for building modern, full-stack web applications. -->
웹 애플리케이션을 만들 때 사용할 수 있는 다양한 도구와 프레임워크가 있습니다. 하지만 저희는 최신의 풀스택 웹 애플리케이션을 개발할 때 Laravel이 최고의 선택이라 믿습니다.

<!-- #### A Progressive Framework -->
#### A Progressive Framework

<!-- We like to call Laravel a "progressive" framework. By that, we mean that Laravel grows with you. If you're just taking your first steps into web development, Laravel's vast library of documentation, guides, and [video tutorials](https://laracasts.com) will help you learn the ropes without becoming overwhelmed. -->
저희는 Laravel을 "발전형(Progressive)" 프레임워크라 부릅니다. 즉, Laravel은 여러분의 성장 단계에 따라 함께 발전할 수 있습니다. 웹 개발 입문 시에도 방대한 문서, 안내서, [video tutorials](https://laracasts.com) 등 풍부한 리소스가 제공되어 부담 없이 기초부터 학습할 수 있습니다.

<!-- If you're a senior developer, Laravel gives you robust tools for [dependency injection](/docs/8.x/container), [unit testing](/docs/8.x/testing), [queues](/docs/8.x/queues), [real-time events](/docs/8.x/broadcasting), and more. Laravel is fine-tuned for building professional web applications and ready to handle enterprise work loads. -->
경험이 많은 시니어 개발자라면, Laravel에서 제공하는 [dependency injection](/docs/8.x/container), [unit testing](/docs/8.x/testing), [queues](/docs/8.x/queues), [real-time events](/docs/8.x/broadcasting) 등 다양한 강력한 도구들을 활용할 수 있습니다. Laravel은 전문가용 웹 애플리케이션 구축에도 특화되어 있으며, 대기업에서 필요로 하는 대규모 워크로드도 거뜬히 처리할 준비가 되어 있습니다.

<!-- #### A Scalable Framework -->
#### A Scalable Framework

<!-- Laravel is incredibly scalable. Thanks to the scaling-friendly nature of PHP and Laravel's built-in support for fast, distributed cache systems like Redis, horizontal scaling with Laravel is a breeze. In fact, Laravel applications have been easily scaled to handle hundreds of millions of requests per month. -->
Laravel은 매우 높은 확장성을 자랑합니다. PHP의 확장성에 더해 Laravel은 Redis와 같은 빠른 분산 캐시 시스템을 기본적으로 지원하므로, 수평 확장(서버를 여러 대로 늘리는 것)도 아주 쉽게 할 수 있습니다. 실제로 Laravel 애플리케이션은 월 수억 건 이상의 요청을 무리 없이 처리한 사례도 있습니다.

<!-- Need extreme scaling? Platforms like [Laravel Vapor](https://vapor.laravel.com) allow you to run your Laravel application at nearly limitless scale on AWS's latest serverless technology. -->
극한의 확장성이 필요하시다면, [Laravel Vapor](https://vapor.laravel.com)와 같은 플랫폼을 통해 AWS의 최신 서버리스 기술 환경에서 Laravel 애플리케이션을 거의 무제한 규모로 운영할 수도 있습니다.

<!-- #### A Community Framework -->
#### A Community Framework

<!-- Laravel combines the best packages in the PHP ecosystem to offer the most robust and developer friendly framework available. In addition, thousands of talented developers from around the world have [contributed to the framework](https://github.com/laravel/framework). Who knows, maybe you'll even become a Laravel contributor. -->
Laravel은 PHP 생태계의 최고의 패키지들을 한데 모아 가장 강력하고 개발자 친화적인 프레임워크를 만들었습니다. 또한, 전 세계 수천 명의 실력 있는 개발자들이 [contributed to the framework](https://github.com/laravel/framework)하고 있습니다. 어쩌면 여러분도 미래의 Laravel 기여자가 될지도 모릅니다.

<a name="your-first-laravel-project"></a>
<!-- ## Your First Laravel Project -->
## Your First Laravel Project

<!-- We want it to be as easy as possible to get started with Laravel. There are a variety of options for developing and running a Laravel project on your own computer. While you may wish to explore these options at a later time, Laravel provides [Sail](/docs/8.x/sail), a built-in solution for running your Laravel project using [Docker](https://www.docker.com). -->
여러분이 Laravel을 더 쉽게 시작할 수 있도록 다양한 방법을 준비했습니다. 개발에 사용하실 컴퓨터 환경에 따라 여러 가지 방식이 있지만, Laravel에는 자체적으로 [Sail](/docs/8.x/sail)이라는 솔루션이 내장되어 있어 [Docker](https://www.docker.com)를 사용해 간편하게 프로젝트를 실행할 수 있습니다.

<!-- Docker is a tool for running applications and services in small, light-weight "containers" which do not interfere with your local computer's installed software or configuration. This means you don't have to worry about configuring or setting up complicated development tools such as web servers and databases on your personal computer. To get started, you only need to install [Docker Desktop](https://www.docker.com/products/docker-desktop). -->
Docker는 각각의 독립된 "컨테이너" 안에서 여러 애플리케이션과 서비스를 실행할 수 있게 해주는 도구로, 로컬 컴퓨터의 기존 프로그램이나 설정을 건드리지 않습니다. 즉, 개인 컴퓨터에 웹 서버나 데이터베이스 같은 복잡한 개발 도구를 따로 설치하고 구성할 필요가 없습니다. 시작을 위해서는 [Docker Desktop](https://www.docker.com/products/docker-desktop)만 설치하면 됩니다.

<!-- Laravel Sail is a light-weight command-line interface for interacting with Laravel's default Docker configuration. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience. -->
Laravel Sail은 Laravel의 기본 Docker 구성과 상호작용할 수 있는 가벼운 명령줄 인터페이스입니다. Sail을 이용하면 Docker에 대한 사전 지식 없이도 PHP, MySQL, Redis를 활용한 Laravel 앱 개발을 바로 시작할 수 있습니다.

> [!TIP]
> 이미 Docker 사용에 익숙하신가요? 걱정하지 마세요! Sail의 모든 설정은 Laravel에 포함된 `docker-compose.yml` 파일을 수정해서 자유롭게 커스터마이징할 수 있습니다.

<a name="getting-started-on-macos"></a>
<!-- ### Getting Started On macOS -->
### Getting Started On macOS

<!-- If you're developing on a Mac and [Docker Desktop](https://www.docker.com/products/docker-desktop) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
Mac에서 개발 중이고 [Docker Desktop](https://www.docker.com/products/docker-desktop)이 이미 설치되어 있다면, 터미널 명령어 한 줄로 새로운 Laravel 프로젝트를 만들 수 있습니다. 예를 들어 "example-app"이라는 디렉토리에 Laravel 애플리케이션을 생성하려면 터미널에서 아래 명령을 실행하세요.

```nothing
curl -s "https://laravel.build/example-app" | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like. The Laravel application's directory will be created within the directory you execute the command from. -->
물론, 위 URL의 "example-app" 부분은 원하는 프로젝트 이름으로 자유롭게 변경해도 됩니다. Laravel 애플리케이션의 디렉토리는 명령을 실행한 현재 디렉토리 안에 생성됩니다.

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
프로젝트가 생성된 후에는 애플리케이션 디렉토리로 이동해서 Laravel Sail을 시작할 수 있습니다. Laravel Sail은 Laravel의 기본 Docker 구성을 쉽게 다룰 수 있는 명령줄 인터페이스를 제공합니다.

```nothing
cd example-app

./vendor/bin/sail up
```

<!-- The first time you run the Sail `up` command, Sail's application containers will be built on your machine. This could take several minutes. **Don't worry, subsequent attempts to start Sail will be much faster.** -->
Sail `up` 명령을 처음 실행하면, 애플리케이션 컨테이너가 여러분의 컴퓨터에서 빌드되므로 몇 분 정도 소요될 수 있습니다. **하지만 걱정하지 마세요, 다음부터는 훨씬 빠르게 시작됩니다.**

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
애플리케이션의 Docker 컨테이너가 모두 실행되면, 웹 브라우저에서 http://localhost 에 접속해 애플리케이션을 확인하실 수 있습니다.

> [!TIP]
> Laravel Sail에 대해 더 자세히 알아보고 싶다면 [complete documentation](/docs/8.x/sail)를 참고하세요.

<a name="getting-started-on-windows"></a>
<!-- ### Getting Started On Windows -->
### Getting Started On Windows

<!-- Before we create a new Laravel application on your Windows machine, make sure to install [Docker Desktop](https://www.docker.com/products/docker-desktop). Next, you should ensure that Windows Subsystem for Linux 2 (WSL2) is installed and enabled. WSL allows you to run Linux binary executables natively on Windows 10. Information on how to install and enable WSL2 can be found within Microsoft's [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10). -->
Windows 환경에서 새로운 Laravel 애플리케이션을 만들기 전, 먼저 [Docker Desktop](https://www.docker.com/products/docker-desktop)이 설치되어 있는지 확인하세요. 그리고 Windows Subsystem for Linux 2(WSL2)도 설치 및 활성화되어 있어야 합니다. WSL은 Windows 10에서 리눅스 바이너리 실행 파일을 직접 실행할 수 있게 해줍니다. WSL2 설치 및 활성화 방법은 마이크로소프트의 [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10)에서 확인하실 수 있습니다.

> [!TIP]
> WSL2 설치 및 활성화 후에는 Docker Desktop이 [configured to use the WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/)되어 있는지 확인하세요.

<!-- Next, you are ready to create your first Laravel project. Launch [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) and begin a new terminal session for your WSL2 Linux operating system. Next, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
이제 첫 Laravel 프로젝트를 만들 준비가 되었습니다. [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)를 실행하고, WSL2 리눅스 환경에서 새로운 터미널 세션을 시작하세요. 그리고 새로운 Laravel 프로젝트를 생성할 때는 아래와 같이 터미널에서 명령어 한 줄로 진행합니다. 예시는 "example-app" 디렉토리에 애플리케이션을 만드는 경우입니다.

```nothing
curl -s https://laravel.build/example-app | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like. The Laravel application's directory will be created within the directory you execute the command from. -->
"example-app" 부분은 자유롭게 원하는 이름으로 바꿔도 됩니다. 애플리케이션 디렉토리는 명령을 실행한 현재 디렉토리에 만들어집니다.

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
프로젝트가 생성된 후, 애플리케이션 디렉토리로 이동해서 Laravel Sail을 시작할 수 있습니다. Sail은 기본 Docker 구성을 명령줄에서 간단하게 조작할 수 있게 해줍니다.

```nothing
cd example-app

./vendor/bin/sail up
```

<!-- The first time you run the Sail `up` command, Sail's application containers will be built on your machine. This could take several minutes. **Don't worry, subsequent attempts to start Sail will be much faster.** -->
Sail `up` 명령을 처음 실행할 때는 애플리케이션 컨테이너가 초기 빌드되기 때문에 몇 분 정도 소요될 수 있습니다. **하지만 다음 번부터는 훨씬 빠르게 시작됩니다.**

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
컨테이너 실행이 완료되면, 웹 브라우저에서 http://localhost 로 접속해 애플리케이션을 확인하세요.

> [!TIP]
> Laravel Sail에 대해 더 자세히 알아보고 싶다면 [complete documentation](/docs/8.x/sail)를 참고하세요.

<!-- #### Developing Within WSL2 -->
#### Developing Within WSL2

<!-- Of course, you will need to be able to modify the Laravel application files that were created within your WSL2 installation. To accomplish this, we recommend using Microsoft's [Visual Studio Code](https://code.visualstudio.com) editor and their first-party extension for [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack). -->
WSL2 환경 내에 생성된 Laravel 애플리케이션 파일을 수정하려면, 마이크로소프트의 [Visual Studio Code](https://code.visualstudio.com) 에디터와 [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) 공식 확장팩 사용을 권장합니다.

<!-- Once these tools are installed, you may open any Laravel project by executing the `code .` command from your application's root directory using Windows Terminal. -->
이 도구들을 설치한 후, Windows Terminal에서 애플리케이션의 루트 디렉토리에서 `code .` 명령을 실행하면, 어느 Laravel 프로젝트든 바로 열 수 있습니다.

<a name="getting-started-on-linux"></a>
<!-- ### Getting Started On Linux -->
### Getting Started On Linux

<!-- If you're developing on Linux and [Docker Compose](https://docs.docker.com/compose/install/) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
Linux에서 개발 중이고 [Docker Compose](https://docs.docker.com/compose/install/)가 이미 설치되어 있다면, 명령어 한 줄로 쉽게 Laravel 프로젝트를 만들 수 있습니다. 예를 들어 "example-app" 폴더에 애플리케이션을 생성하려면 터미널에서 아래 명령을 실행하세요.

```nothing
curl -s https://laravel.build/example-app | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like. The Laravel application's directory will be created within the directory you execute the command from. -->
당연히 "example-app" 부분은 원하는 이름으로 바꿀 수 있습니다. 애플리케이션 디렉토리는 명령을 실행한 현재 폴더에 생성됩니다.

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
프로젝트가 만들어진 후엔 디렉토리로 이동해서 Laravel Sail을 시작합니다. Sail은 Laravel의 기본 Docker 구성을 명령줄에서 간편하게 관리할 수 있게 해줍니다.

```nothing
cd example-app

./vendor/bin/sail up
```

<!-- The first time you run the Sail `up` command, Sail's application containers will be built on your machine. This could take several minutes. **Don't worry, subsequent attempts to start Sail will be much faster.** -->
Sail `up` 명령을 처음 실행하면 컨테이너가 빌드되어 몇 분간 시간이 소요될 수 있습니다. **하지만 2회차부터는 더 빠르게 실행됩니다.**

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
컨테이너가 실행되면, 웹 브라우저에서 http://localhost 주소로 접속해 애플리케이션을 확인할 수 있습니다.

> [!TIP]
> Laravel Sail에 대해 더 자세히 알아보고 싶다면 [complete documentation](/docs/8.x/sail)를 참고하세요.

<a name="choosing-your-sail-services"></a>
<!-- ### Choosing Your Sail Services -->
### Choosing Your Sail Services

<!-- When creating a new Laravel application via Sail, you may use the `with` query string variable to choose which services should be configured in your new application's `docker-compose.yml` file. Available services include `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `minio`, `selenium`, and `mailhog`: -->
Sail을 통해 새 Laravel 애플리케이션을 만들 때, `with` 쿼리 스트링 변수로 새로운 애플리케이션의 `docker-compose.yml` 파일에 어떤 서비스가 포함될지 지정할 수 있습니다. 사용 가능한 서비스에는 `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `minio`, `selenium`, `mailhog` 등이 있습니다.

```nothing
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

<!-- If you do not specify which services you would like configured, a default stack of `mysql`, `redis`, `meilisearch`, `mailhog`, and `selenium` will be configured. -->
만약 별도로 서비스를 지정하지 않으면, `mysql`, `redis`, `meilisearch`, `mailhog`, `selenium`이 기본값으로 포함됩니다.

<a name="installation-via-composer"></a>
<!-- ### Installation Via Composer -->
### Installation Via Composer

<!-- If your computer already has PHP and Composer installed, you may create a new Laravel project by using Composer directly. After the application has been created, you may start Laravel's local development server using the Artisan CLI's `serve` command: -->
만약 컴퓨터에 PHP와 Composer가 이미 설치되어 있다면, Composer를 직접 활용해서 Laravel 프로젝트를 만들 수 있습니다. 애플리케이션 생성 후에는 Artisan CLI의 `serve` 명령어로 Laravel의 로컬 개발 서버를 실행할 수 있습니다.

```
composer create-project laravel/laravel:^8.0 example-app

cd example-app

php artisan serve
```

<a name="the-laravel-installer"></a>
<!-- #### The Laravel Installer -->
#### The Laravel Installer

<!-- Or, you may install the Laravel Installer as a global Composer dependency: -->
또는 Composer를 이용해 Laravel 인스톨러를 전역으로 설치할 수도 있습니다.

```nothing
composer global require laravel/installer

laravel new example-app

cd example-app

php artisan serve
```

<!-- Make sure to place Composer's system-wide vendor bin directory in your `$PATH` so the `laravel` executable can be located by your system. This directory exists in different locations based on your operating system; however, some common locations include: -->
시스템 전체에서 `laravel` 실행 파일을 찾을 수 있도록 Composer의 글로벌 vendor bin 디렉토리가 반드시 `$PATH`에 포함되어 있어야 합니다. 이 디렉토리는 운영체제마다 다르지만, 대표적으로 아래 위치에 존재합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- macOS: `$HOME/.composer/vendor/bin`
- Windows: `%USERPROFILE%\AppData\Roaming\Composer\vendor\bin`
- GNU / Linux Distributions: `$HOME/.config/composer/vendor/bin` or `$HOME/.composer/vendor/bin`
-->
- macOS: `$HOME/.composer/vendor/bin`
- Windows: `%USERPROFILE%\AppData\Roaming\Composer\vendor\bin`
- GNU / Linux 계열: `$HOME/.config/composer/vendor/bin` 또는 `$HOME/.composer/vendor/bin`

<!-- </div> -->
</div>

<!-- For convenience, the Laravel installer can also create a Git repository for your new project. To indicate that you want a Git repository to be created, pass the `--git` flag when creating a new project: -->
편의를 위해, Laravel 인스톨러는 새 프로젝트를 만들 때 Git 저장소도 함께 생성할 수 있습니다. 새로운 프로젝트를 만들 때 `--git` 플래그를 추가하면 프로젝트와 함께 Git 저장소가 생성됩니다.

```bash
laravel new example-app --git
```

<!-- This command will initialize a new Git repository for your project and automatically commit the base Laravel skeleton. The `git` flag assumes you have properly installed and configured Git. You can also use the `--branch` flag to set the initial branch name: -->
이 명령어는 프로젝트의 Git 저장소를 초기화하고, Laravel 기본 골격 코드를 자동으로 첫 커밋으로 만들어줍니다. `git` 플래그를 사용하려면 Git이 제대로 설치 및 설정되어 있어야 합니다. 또한, `--branch` 플래그를 사용해 초기 브랜치 이름을 지정할 수도 있습니다.

```bash
laravel new example-app --git --branch="main"
```

<!-- Instead of using the `--git` flag, you may also use the `--github` flag to create a Git repository and also create a corresponding private repository on GitHub: -->
`--git` 플래그 대신 `--github` 플래그를 사용하면, 로컬 Git 저장소는 물론 GitHub에 대응되는 비공개 저장소까지 자동으로 생성할 수 있습니다.

```bash
laravel new example-app --github
```

<!-- The created repository will then be available at `https://github.com/<your-account>/example-app`. The `github` flag assumes you have properly installed the [GitHub CLI](https://cli.github.com) and are authenticated with GitHub. Additionally, you should have `git` installed and properly configured. If needed, you can pass additional flags that are supported by the GitHub CLI: -->
이렇게 만들어진 저장소는 `https://github.com/<your-account>/example-app` 주소에서 확인할 수 있습니다. `github` 플래그를 사용하려면 [GitHub CLI](https://cli.github.com)가 설치되어 있고, GitHub에 인증되어 있어야 하며, `git`도 제대로 설치·설정되어 있어야 합니다. 필요하다면 GitHub CLI에서 지원하는 다양한 플래그도 함께 전달할 수 있습니다.

```bash
laravel new example-app --github="--public"
```

<!-- You may use the `--organization` flag to create the repository under a specific GitHub organization: -->
또한 `--organization` 플래그를 사용해 특정 GitHub 조직 하위에 저장소를 생성할 수도 있습니다.

```bash
laravel new example-app --github="--public" --organization="laravel"
```

<a name="initial-configuration"></a>
<!-- ## Initial Configuration -->
## Initial Configuration

<!-- All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you. -->
Laravel 프레임워크의 모든 설정 파일은 `config` 디렉토리에 저장되어 있습니다. 각 옵션마다 주석이 잘 달려 있으니, 직접 파일을 열어 다양한 옵션을 확인해보셔도 좋습니다.

<!-- Laravel needs almost no additional configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your application. -->
Laravel은 기본적으로 별다른 추가 설정 없이 바로 개발을 시작할 수 있습니다. 물론 필요에 따라 `config/app.php` 파일과 문서도 살펴보시길 권장합니다. 여기에는 `timezone`(타임존)이나 `locale`(로케일)처럼 애플리케이션 환경에 맞게 설정할 수 있는 여러 옵션이 있습니다.

<a name="environment-based-configuration"></a>
<!-- ### Environment Based Configuration -->
### Environment Based Configuration

<!-- Since many of Laravel's configuration option values may vary depending on whether your application is running on your local computer or on a production web server, many important configuration values are defined using the `.env` file that exists at the root of your application. -->
Laravel의 많은 설정 값들은 여러분의 애플리케이션이 로컬 컴퓨터에서 실행될 때와, 운영 서버(프로덕션 웹 서버)에서 실행될 때에 따라 달라질 수 있습니다. 그래서 중요한 설정 값 상당수는 애플리케이션 루트에 위치한 `.env` 파일을 통해 정의됩니다.

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed. -->
`.env` 파일은 각 개발자 또는 서버가 서로 다른 환경 설정을 가질 수 있기 때문에, 반드시 소스 관리 저장소에는 커밋하지 않아야 합니다. 그리고 만약 소스 저장소에 노출된 경우, 민감한 인증 정보가 유출될 수 있으므로 보안상으로도 매우 위험합니다.

> [!TIP]
> `.env` 파일 및 환경 기반 설정에 대해 더 자세한 내용은 [configuration documentation](/docs/8.x/configuration#environment-configuration)를 참고하세요.

<a name="directory-configuration"></a>
<!-- ### Directory Configuration -->
### Directory Configuration

<!-- Laravel should always be served out of the root of the "web directory" configured for your web server. You should not attempt to serve a Laravel application out of a subdirectory of the "web directory". Attempting to do so could expose sensitive files that exist within your application. -->
Laravel 애플리케이션은 항상 웹 서버의 "웹 디렉토리" 루트에서 서비스되어야 합니다. Laravel 애플리케이션을 "웹 디렉토리"의 하위 폴더에서 서비스하려는 시도는 하지 않아야 합니다. 그렇게 하면 애플리케이션 내의 민감한 파일들이 외부에 노출될 위험이 있습니다.

<a name="next-steps"></a>
<!-- ## Next Steps -->
## Next Steps

<!-- Now that you have created your Laravel project, you may be wondering what to learn next. First, we strongly recommend becoming familiar with how Laravel works by reading the following documentation: -->
이제 Laravel 프로젝트를 만들었으니, 앞으로 무엇을 학습하면 좋을지 고민하실 수 있습니다. 우선 Laravel의 작동 방식을 익히기 위해 아래 문서들을 반드시 읽어보시길 추천합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- [Request Lifecycle](/docs/8.x/lifecycle)
- [Configuration](/docs/8.x/configuration)
- [Directory Structure](/docs/8.x/structure)
- [Service Container](/docs/8.x/container)
- [Facades](/docs/8.x/facades)
-->
- [Request Lifecycle](/docs/8.x/lifecycle)
- [Configuration](/docs/8.x/configuration)
- [Directory Structure](/docs/8.x/structure)
- [Service Container](/docs/8.x/container)
- [Facades](/docs/8.x/facades)

<!-- </div> -->
</div>

<!-- How you want to use Laravel will also dictate the next steps on your journey. There are a variety of ways to use Laravel, and we'll explore two primary use cases for the framework below. -->
여러분이 Laravel을 어떤 용도로 쓰고 싶은지에 따라 앞으로의 학습 방향도 달라질 수 있습니다. Laravel을 활용하는 방법은 매우 다양하며, 아래에서는 대표적인 두 가지 활용 방식을 소개합니다.

<a name="laravel-the-fullstack-framework"></a>
<!-- ### Laravel The Full Stack Framework -->
### Laravel The Full Stack Framework

<!-- Laravel may serve as a full stack framework. By "full stack" framework we mean that you are going to use Laravel to route requests to your application and render your frontend via [Blade templates](/docs/8.x/blade) or using a single-page application hybrid technology like [Inertia.js](https://inertiajs.com). This is the most common way to use the Laravel framework. -->
Laravel은 풀스택 프레임워크로 사용될 수 있습니다. 여기서 "풀스택" 프레임워크란, Laravel이 모든 HTTP 요청의 라우팅을 담당하고, [Blade templates](/docs/8.x/blade)이나 [Inertia.js](https://inertiajs.com) 같은 단일 페이지 애플리케이션 하이브리드 기술로 프론트엔드 렌더링까지 포함한다는 의미입니다. 이것이 Laravel을 가장 일반적으로 활용하는 방식입니다.

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/8.x/routing), [views](/docs/8.x/views), or the [Eloquent ORM](/docs/8.x/eloquent). In addition, you might be interested in learning about community packages like [Livewire](https://laravel-livewire.com) and [Inertia.js](https://inertiajs.com). These packages allow you to use Laravel as a full-stack framework while enjoying many of the UI benefits provided by single-page JavaScript applications. -->
이런 방식으로 Laravel을 사용하고자 한다면 [routing](/docs/8.x/routing), [views](/docs/8.x/views), [Eloquent ORM](/docs/8.x/eloquent) 문서를 참고하길 권장합니다. 또한 [Livewire](https://laravel-livewire.com), [Inertia.js](https://inertiajs.com) 등 커뮤니티 패키지들도 살펴볼 만합니다. 이런 패키지들을 활용하면 단일 페이지 자바스크립트 앱의 UI 이점을 누리면서도 Laravel을 풀스택 프레임워크로 쓸 수 있습니다.

<!-- If you are using Laravel as a full stack framework, we also strongly encourage you to learn how to compile your application's CSS and JavaScript using [Laravel Mix](/docs/8.x/mix). -->
풀스택 프레임워크로 Laravel을 사용할 경우, [Laravel Mix](/docs/8.x/mix)를 활용해 CSS와 자바스크립트 번들링 방법도 꼭 배워 보길 권장합니다.

> [!TIP]
> 애플리케이션을 곧바로 개발하고 싶다면 공식 [application starter kits](/docs/8.x/starter-kits)부터 확인해보세요.

<a name="laravel-the-api-backend"></a>
<!-- ### Laravel The API Backend -->
### Laravel The API Backend

<!-- Laravel may also serve as an API backend to a JavaScript single-page application or mobile application. For example, you might use Laravel as an API backend for your [Next.js](https://nextjs.org) application. In this context, you may use Laravel to provide [authentication](/docs/8.x/sanctum) and data storage / retrieval for your application, while also taking advantage of Laravel's powerful services such as queues, emails, notifications, and more. -->
Laravel은 또한 자바스크립트 단일 페이지 애플리케이션이나 모바일 애플리케이션을 위한 API 백엔드로도 사용할 수 있습니다. 예를 들어 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 선택할 수도 있습니다. 이런 식으로 활용하면 Laravel은 [authentication](/docs/8.x/sanctum) 및 데이터 저장/조회는 물론, 큐, 이메일, 알림 등 강력한 다양한 서비스를 API로 제공할 수 있습니다.

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/8.x/routing), [Laravel Sanctum](/docs/8.x/sanctum), and the [Eloquent ORM](/docs/8.x/eloquent). -->
이런 방식으로 사용하고자 한다면 [routing](/docs/8.x/routing), [Laravel Sanctum](/docs/8.x/sanctum), [Eloquent ORM](/docs/8.x/eloquent) 관련 문서를 참고하면 좋습니다.

> [!TIP]
> Laravel 백엔드와 Next.js 프론트엔드를 빠르게 셋업하고 싶으신가요? Laravel Breeze에는 [API stack](/docs/8.x/starter-kits#breeze-and-next)과 [Next.js frontend implementation](https://github.com/laravel/breeze-next)가 준비되어 있어 몇 분 만에 시작할 수 있습니다.