<!-- # Directory Structure -->
# Directory Structure

- [Introduction](#introduction)
- [The Root Directory](#the-root-directory)
    - [The `app` Directory](#the-root-app-directory)
    - [The `bootstrap` Directory](#the-bootstrap-directory)
    - [The `config` Directory](#the-config-directory)
    - [The `database` Directory](#the-database-directory)
    - [The `public` Directory](#the-public-directory)
    - [The `resources` Directory](#the-resources-directory)
    - [The `routes` Directory](#the-routes-directory)
    - [The `storage` Directory](#the-storage-directory)
    - [The `tests` Directory](#the-tests-directory)
    - [The `vendor` Directory](#the-vendor-directory)
- [The App Directory](#the-app-directory)
    - [The `Broadcasting` Directory](#the-broadcasting-directory)
    - [The `Console` Directory](#the-console-directory)
    - [The `Events` Directory](#the-events-directory)
    - [The `Exceptions` Directory](#the-exceptions-directory)
    - [The `Http` Directory](#the-http-directory)
    - [The `Jobs` Directory](#the-jobs-directory)
    - [The `Listeners` Directory](#the-listeners-directory)
    - [The `Mail` Directory](#the-mail-directory)
    - [The `Models` Directory](#the-models-directory)
    - [The `Notifications` Directory](#the-notifications-directory)
    - [The `Policies` Directory](#the-policies-directory)
    - [The `Providers` Directory](#the-providers-directory)
    - [The `Rules` Directory](#the-rules-directory)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- The default Laravel application structure is intended to provide a great starting point for both large and small applications. But you are free to organize your application however you like. Laravel imposes almost no restrictions on where any given class is located - as long as Composer can autoload the class. -->
기본적으로 제공되는 Laravel 애플리케이션 구조는 소규모부터 대규모 애플리케이션까지 모두에 적합한 훌륭한 출발점을 제공합니다. 하지만, 여러분은 마음대로 애플리케이션의 구조를 변경해서 사용할 수 있습니다. Laravel은 클래스가 어떤 위치에 있든지 거의 제한을 두지 않습니다. Composer가 그 클래스를 자동 로딩할 수만 있다면 어디에 있어도 괜찮습니다.

> [!NOTE]
> Laravel이 처음이신가요? [Laravel Bootcamp](https://bootcamp.laravel.com)를 참고하여 실제로 애플리케이션을 만들어 보며 프레임워크의 핵심을 배워보시기 바랍니다.

<a name="the-root-directory"></a>
<!-- ## The Root Directory -->
## The Root Directory

<a name="the-root-app-directory"></a>
<!-- ### The App Directory -->
### The App Directory

<!-- The `app` directory contains the core code of your application. We'll explore this directory in more detail soon; however, almost all of the classes in your application will be in this directory. -->
`app` 디렉터리에는 애플리케이션의 핵심 코드가 포함되어 있습니다. 이 디렉터리에 대해 곧 더 자세히 살펴보겠습니다. 거의 모든 클래스가 이 디렉터리 안에 위치하게 됩니다.

<a name="the-bootstrap-directory"></a>
<!-- ### The Bootstrap Directory -->
### The Bootstrap Directory

<!-- The `bootstrap` directory contains the `app.php` file which bootstraps the framework. This directory also houses a `cache` directory which contains framework generated files for performance optimization such as the route and services cache files. -->
`bootstrap` 디렉터리에는 프레임워크를 부트스트랩하는 `app.php` 파일이 들어 있습니다. 또한 이 디렉터리에는 프레임워크가 생성한 파일(예: 라우트 캐시, 서비스 캐시 등)로 성능을 향상시키는 `cache` 디렉터리가 존재합니다.

<a name="the-config-directory"></a>
<!-- ### The Config Directory -->
### The Config Directory

<!-- The `config` directory, as the name implies, contains all of your application's configuration files. It's a great idea to read through all of these files and familiarize yourself with all of the options available to you. -->
이름에서 알 수 있듯이, `config` 디렉터리에는 애플리케이션의 모든 설정 파일이 들어 있습니다. 꼭 이 디렉터리 안의 파일들을 따라가며 읽어보고, 사용할 수 있는 다양한 옵션에 익숙해지길 권장합니다.

<a name="the-database-directory"></a>
<!-- ### The Database Directory -->
### The Database Directory

<!-- The `database` directory contains your database migrations, model factories, and seeds. If you wish, you may also use this directory to hold an SQLite database. -->
`database` 디렉터리에는 데이터베이스 마이그레이션, 모델 팩토리, 시드 파일이 들어 있습니다. 필요하다면 이 디렉터리에 SQLite 데이터베이스 파일을 함께 넣어 사용할 수도 있습니다.

<a name="the-public-directory"></a>
<!-- ### The Public Directory -->
### The Public Directory

<!-- The `public` directory contains the `index.php` file, which is the entry point for all requests entering your application and configures autoloading. This directory also houses your assets such as images, JavaScript, and CSS. -->
`public` 디렉터리에는 모든 요청이 들어오는 진입점 역할을 하는 `index.php` 파일이 있습니다. 이곳에서 오토로딩 설정도 이루어집니다. 또한 이미지, JavaScript, CSS와 같은 애플리케이션의 자산(assets) 파일도 여기에 둡니다.

<a name="the-resources-directory"></a>
<!-- ### The Resources Directory -->
### The Resources Directory

<!-- The `resources` directory contains your [views](/docs/11.x/views) as well as your raw, un-compiled assets such as CSS or JavaScript. -->
`resources` 디렉터리에는 [views](/docs/11.x/views)와 CSS/JavaScript 등 아직 컴파일되지 않은 원본 자산 파일이 들어 있습니다.

<a name="the-routes-directory"></a>
<!-- ### The Routes Directory -->
### The Routes Directory

<!-- The `routes` directory contains all of the route definitions for your application. By default, two route files are included with Laravel: `web.php` and `console.php`. -->
`routes` 디렉터리에는 애플리케이션의 모든 라우트 정의가 들어 있습니다. 기본적으로 Laravel에는 `web.php`와 `console.php` 두 개의 라우트 파일이 포함되어 있습니다.

<!-- The `web.php` file contains routes that Laravel places in the `web` middleware group, which provides session state, CSRF protection, and cookie encryption. If your application does not offer a stateless, RESTful API then all your routes will most likely be defined in the `web.php` file. -->
`web.php` 파일에는 세션 상태, CSRF 보호, 쿠키 암호화 등을 제공하는 `web` 미들웨어 그룹에 속하는 라우트가 정의됩니다. 애플리케이션이 별도의 RESTful API를 제공하지 않는다면, 대부분의 라우트는 `web.php` 파일에 작성하게 됩니다.

<!-- The `console.php` file is where you may define all of your closure based console commands. Each closure is bound to a command instance allowing a simple approach to interacting with each command's IO methods. Even though this file does not define HTTP routes, it defines console based entry points (routes) into your application. You may also [schedule](/docs/11.x/scheduling) tasks in the `console.php` file. -->
`console.php` 파일은 클로저(익명 함수) 기반의 콘솔 명령어를 정의하는 곳입니다. 각 클로저는 명령어 인스턴스에 바인딩되어, 각 명령어의 IO 메서드와 쉽게 상호작용할 수 있습니다. 이 파일은 HTTP 라우트를 정의하지는 않지만, 애플리케이션으로 진입하는 콘솔 엔트리포인트(라우트) 역할을 합니다. 또한, `console.php` 파일에 [schedule](/docs/11.x/scheduling)도 설정할 수 있습니다.

<!-- Optionally, you may install additional route files for API routes (`api.php`) and broadcasting channels (`channels.php`), via the `install:api` and `install:broadcasting` Artisan commands. -->
추가로, `install:api`, `install:broadcasting` 아티즌 명령어를 사용하면 API 라우트(`api.php`), 브로드캐스팅 채널(`channels.php`) 등 추가적인 라우트 파일을 설치할 수 있습니다.

<!-- The `api.php` file contains routes that are intended to be stateless, so requests entering the application through these routes are intended to be authenticated [via tokens](/docs/11.x/sanctum) and will not have access to session state. -->
`api.php` 파일에는 상태 비저장(stateless) 방식의 API 라우트가 정의되어 있으며, 이 라우트를 통하는 요청은 보통 [via tokens](/docs/11.x/sanctum) 인증을 거치고 세션 상태에 접근할 수 없습니다.

<!-- The `channels.php` file is where you may register all of the [event broadcasting](/docs/11.x/broadcasting) channels that your application supports. -->
`channels.php` 파일은 애플리케이션이 지원하는 모든 [event broadcasting](/docs/11.x/broadcasting) 채널을 등록하는 곳입니다.

<a name="the-storage-directory"></a>
<!-- ### The Storage Directory -->
### The Storage Directory

<!-- The `storage` directory contains your logs, compiled Blade templates, file based sessions, file caches, and other files generated by the framework. This directory is segregated into `app`, `framework`, and `logs` directories. The `app` directory may be used to store any files generated by your application. The `framework` directory is used to store framework generated files and caches. Finally, the `logs` directory contains your application's log files. -->
`storage` 디렉터리에는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 파일 캐시, 프레임워크가 생성하는 기타 파일들이 저장됩니다. 디렉터리는 `app`, `framework`, `logs`로 나뉩니다. `app` 디렉터리에는 애플리케이션에서 생성하는 임시 파일들을 저장할 수 있습니다. `framework` 디렉터리는 프레임워크가 생성한 파일이나 캐시 데이터를 저장합니다. 마지막으로 `logs` 디렉터리에는 애플리케이션의 로그 파일이 저장됩니다.

<!-- The `storage/app/public` directory may be used to store user-generated files, such as profile avatars, that should be publicly accessible. You should create a symbolic link at `public/storage` which points to this directory. You may create the link using the `php artisan storage:link` Artisan command. -->
`storage/app/public` 디렉터리는 프로필 아바타 등 사용자 생성 파일 중에서 공개적으로 접근이 가능한 파일을 저장할 수 있습니다. 이 디렉터리에 접근하려면 `public/storage`에 심볼릭 링크를 만들어주어야 하며, `php artisan storage:link` 아티즌 명령어로 쉽게 생성할 수 있습니다.

<a name="the-tests-directory"></a>
<!-- ### The Tests Directory -->
### The Tests Directory

<!-- The `tests` directory contains your automated tests. Example [Pest](https://pestphp.com) or [PHPUnit](https://phpunit.de/) unit tests and feature tests are provided out of the box. Each test class should be suffixed with the word `Test`. You may run your tests using the `/vendor/bin/pest` or `/vendor/bin/phpunit` commands. Or, if you would like a more detailed and beautiful representation of your test results, you may run your tests using the `php artisan test` Artisan command. -->
`tests` 디렉터리에는 자동화 테스트가 들어 있습니다. 예시로 [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de/)를 이용한 유닛 테스트와 기능 테스트가 기본 제공됩니다. 각 테스트 클래스의 이름은 반드시 `Test`로 끝나야 합니다. `/vendor/bin/pest` 또는 `/vendor/bin/phpunit` 명령어로 테스트를 실행할 수 있습니다. 또한, 더 보기 쉽고 상세한 테스트 결과를 원한다면 `php artisan test` 아티즌 명령어로 실행하는 것도 가능합니다.

<a name="the-vendor-directory"></a>
<!-- ### The Vendor Directory -->
### The Vendor Directory

<!-- The `vendor` directory contains your [Composer](https://getcomposer.org) dependencies. -->
`vendor` 디렉터리에는 [Composer](https://getcomposer.org)로 설치된 의존 패키지들이 들어 있습니다.

<a name="the-app-directory"></a>
<!-- ## The App Directory -->
## The App Directory

<!-- The majority of your application is housed in the `app` directory. By default, this directory is namespaced under `App` and is autoloaded by Composer using the [PSR-4 autoloading standard](https://www.php-fig.org/psr/psr-4/). -->
애플리케이션의 거의 모든 코드는 `app` 디렉터리 안에 들어 있습니다. 이 디렉터리는 기본적으로 `App` 네임스페이스 하위에 있으며, [PSR-4 autoloading standard](https://www.php-fig.org/psr/psr-4/)에 따라 Composer에 의해 자동 로드됩니다.

<!-- By default, the `app` directory contains the `Http`, `Models`, and `Providers` directories. However, over time, a variety of other directories will be generated inside the app directory as you use the make Artisan commands to generate classes. For example, the `app/Console` directory will not exist until you execute the `make:command` Artisan command to generate a command class. -->
기본적으로 `app` 디렉터리에는 `Http`, `Models`, `Providers` 디렉터리가 있습니다. 하지만, make 관련 아티즌 명령어를 통해 클래스를 생성해 나가면 다양한 추가 디렉터리가 생성됩니다. 예를 들어, `app/Console` 디렉터리는 `make:command` 아티즌 명령어로 명령어 클래스를 생성하기 전까지는 존재하지 않습니다.

<!-- Both the `Console` and `Http` directories are further explained in their respective sections below, but think of the `Console` and `Http` directories as providing an API into the core of your application. The HTTP protocol and CLI are both mechanisms to interact with your application, but do not actually contain application logic. In other words, they are two ways of issuing commands to your application. The `Console` directory contains all of your Artisan commands, while the `Http` directory contains your controllers, middleware, and requests. -->
`Console` 디렉터리와 `Http` 디렉터리에 관해서는 아래에서 좀 더 자세히 다루겠습니다. `Console` 및 `Http` 디렉터리는 애플리케이션의 핵심에 접근하는 API라고 생각하면 쉽습니다. HTTP 프로토콜과 CLI(명령줄)는 모두 애플리케이션과 상호작용하는 수단이며, 실제 비즈니스 로직을 담고 있지는 않습니다. 즉, 두 가지 모두 애플리케이션에 명령을 전달하는 방법입니다. `Console` 디렉터리에는 모든 아티즌 명령어가, `Http` 디렉터리에는 컨트롤러, 미들웨어, 폼 요청이 포함되어 있습니다.

> [!NOTE]
> `app` 디렉터리의 많은 클래스들은 아티즌 명령어로 자동 생성할 수 있습니다. 사용 가능한 명령어를 확인하려면 터미널에서 `php artisan list make` 명령어를 실행해 보세요.

<a name="the-broadcasting-directory"></a>
<!-- ### The Broadcasting Directory -->
### The Broadcasting Directory

<!-- The `Broadcasting` directory contains all of the broadcast channel classes for your application. These classes are generated using the `make:channel` command. This directory does not exist by default, but will be created for you when you create your first channel. To learn more about channels, check out the documentation on [event broadcasting](/docs/11.x/broadcasting). -->
`Broadcasting` 디렉터리에는 애플리케이션의 브로드캐스트 채널 클래스가 모두 담깁니다. 이 클래스들은 `make:channel` 명령어로 생성할 수 있습니다. 기본적으로 존재하지 않으며, 첫 브로드캐스트 채널을 만들 때 생성됩니다. 관련된 내용은 [event broadcasting](/docs/11.x/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
<!-- ### The Console Directory -->
### The Console Directory

<!-- The `Console` directory contains all of the custom Artisan commands for your application. These commands may be generated using the `make:command` command. -->
`Console` 디렉터리에는 애플리케이션에서 사용하는 모든 커스텀 아티즌 명령어가 저장됩니다. 이 명령어들은 `make:command` 명령어로 생성할 수 있습니다.

<a name="the-events-directory"></a>
<!-- ### The Events Directory -->
### The Events Directory

<!-- This directory does not exist by default, but will be created for you by the `event:generate` and `make:event` Artisan commands. The `Events` directory houses [event classes](/docs/11.x/events). Events may be used to alert other parts of your application that a given action has occurred, providing a great deal of flexibility and decoupling. -->
이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 또는 `make:event` 아티즌 명령어를 실행하면 생성됩니다. `Events` 디렉터리에는 [event classes](/docs/11.x/events)가 들어 있습니다. 이벤트는 애플리케이션의 여러 부분에 특정 동작이 발생했음을 알리는 용도로 사용하며, 높은 유연성과 결합도를 낮추는 설계에 도움이 됩니다.

<a name="the-exceptions-directory"></a>
<!-- ### The Exceptions Directory -->
### The Exceptions Directory

<!-- The `Exceptions` directory contains all of the custom exceptions for your application. These exceptions may be generated using the `make:exception` command. -->
`Exceptions` 디렉터리에는 애플리케이션의 커스텀 예외 클래스가 모두 들어 있습니다. 이 예외 클래스들은 `make:exception` 명령어로 생성할 수 있습니다.

<a name="the-http-directory"></a>
<!-- ### The Http Directory -->
### The Http Directory

<!-- The `Http` directory contains your controllers, middleware, and form requests. Almost all of the logic to handle requests entering your application will be placed in this directory. -->
`Http` 디렉터리에는 컨트롤러, 미들웨어, 그리고 폼 요청 클래스가 포함됩니다. 요청을 받아 처리하는 거의 모든 로직이 이곳에 작성됩니다.

<a name="the-jobs-directory"></a>
<!-- ### The Jobs Directory -->
### The Jobs Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:job` Artisan command. The `Jobs` directory houses the [queueable jobs](/docs/11.x/queues) for your application. Jobs may be queued by your application or run synchronously within the current request lifecycle. Jobs that run synchronously during the current request are sometimes referred to as "commands" since they are an implementation of the [command pattern](https://en.wikipedia.org/wiki/Command_pattern). -->
이 디렉터리는 기본적으로 존재하지 않지만, `make:job` 아티즌 명령어를 실행하면 생성됩니다. `Jobs` 디렉터리에는 애플리케이션의 [queueable jobs](/docs/11.x/queues)가 들어 있습니다. 작업은 큐를 통해 비동기로 또는 현재 요청의 라이프사이클 내에서 동기적으로 실행할 수 있습니다. 현재 요청에서 바로 수행되는 작업은 가끔 "커맨드"라고도 부르는데, 이는 [command pattern](https://en.wikipedia.org/wiki/Command_pattern)의 구현 방식이기 때문입니다.

<a name="the-listeners-directory"></a>
<!-- ### The Listeners Directory -->
### The Listeners Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `event:generate` or `make:listener` Artisan commands. The `Listeners` directory contains the classes that handle your [events](/docs/11.x/events). Event listeners receive an event instance and perform logic in response to the event being fired. For example, a `UserRegistered` event might be handled by a `SendWelcomeEmail` listener. -->
이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 또는 `make:listener` 아티즌 명령어를 실행하면 생성됩니다. `Listeners` 디렉터리에는 [events](/docs/11.x/events)를 처리하는 클래스가 담겨 있습니다. 이벤트 리스너는 이벤트 인스턴스를 전달받아, 해당 이벤트가 발생했을 때 필요한 로직을 수행합니다. 예를 들어, `UserRegistered` 이벤트가 발생하면 `SendWelcomeEmail` 리스너가 환영 이메일을 보내 처리할 수 있습니다.

<a name="the-mail-directory"></a>
<!-- ### The Mail Directory -->
### The Mail Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:mail` Artisan command. The `Mail` directory contains all of your [classes that represent emails](/docs/11.x/mail) sent by your application. Mail objects allow you to encapsulate all of the logic of building an email in a single, simple class that may be sent using the `Mail::send` method. -->
이 디렉터리는 기본적으로 존재하지 않지만, `make:mail` 아티즌 명령어를 실행하면 생성됩니다. `Mail` 디렉터리에는 애플리케이션에서 발송하는 [classes that represent emails](/docs/11.x/mail)가 들어 있습니다. 메일 오브젝트는 이메일을 구성하는 모든 로직을 단순한 하나의 클래스로 캡슐화하며, `Mail::send` 메서드로 발송할 수 있습니다.

<a name="the-models-directory"></a>
<!-- ### The Models Directory -->
### The Models Directory

<!-- The `Models` directory contains all of your [Eloquent model classes](/docs/11.x/eloquent). The Eloquent ORM included with Laravel provides a beautiful, simple ActiveRecord implementation for working with your database. Each database table has a corresponding "Model" which is used to interact with that table. Models allow you to query for data in your tables, as well as insert new records into the table. -->
`Models` 디렉터리에는 [Eloquent model classes](/docs/11.x/eloquent)가 모두 들어 있습니다. Laravel에 내장된 Eloquent ORM은 데이터베이스와 상호작용할 수 있도록 간단하고 직관적인 액티브 레코드(Active Record) 방식을 제공합니다. 각 데이터베이스 테이블에는 그에 대응하는 "모델"이 있어, 이 모델을 통해 데이터를 조회하거나 신규 레코드를 추가할 수 있습니다.

<a name="the-notifications-directory"></a>
<!-- ### The Notifications Directory -->
### The Notifications Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:notification` Artisan command. The `Notifications` directory contains all of the "transactional" [notifications](/docs/11.x/notifications) that are sent by your application, such as simple notifications about events that happen within your application. Laravel's notification feature abstracts sending notifications over a variety of drivers such as email, Slack, SMS, or stored in a database. -->
이 디렉터리는 기본적으로 존재하지 않지만, `make:notification` 아티즌 명령어를 실행하면 생성됩니다. `Notifications` 디렉터리에는 애플리케이션에서 발송하는 "트랜잭션성" [notifications](/docs/11.x/notifications)가 들어 있습니다. 예를 들어, 애플리케이션 내부의 특정 이벤트 발생시 전송되는 간단한 알림 등이 여기에 해당합니다. Laravel의 알림 기능은 이메일, Slack, SMS, 데이터베이스 저장 등 다양한 방법으로 알림을 추상화하여 전송할 수 있습니다.

<a name="the-policies-directory"></a>
<!-- ### The Policies Directory -->
### The Policies Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:policy` Artisan command. The `Policies` directory contains the [authorization policy classes](/docs/11.x/authorization) for your application. Policies are used to determine if a user can perform a given action against a resource. -->
이 디렉터리는 기본적으로 존재하지 않지만, `make:policy` 아티즌 명령어를 실행하면 생성됩니다. `Policies` 디렉터리에는 애플리케이션의 [authorization policy classes](/docs/11.x/authorization)가 포함됩니다. 정책(Policy)은 사용자가 특정 리소스에 대해 주어진 동작을 수행할 수 있는지 여부를 판별하는 데 사용됩니다.

<a name="the-providers-directory"></a>
<!-- ### The Providers Directory -->
### The Providers Directory

<!-- The `Providers` directory contains all of the [service providers](/docs/11.x/providers) for your application. Service providers bootstrap your application by binding services in the service container, registering events, or performing any other tasks to prepare your application for incoming requests. -->
`Providers` 디렉터리에는 애플리케이션의 모든 [service providers](/docs/11.x/providers)가 들어 있습니다. 서비스 프로바이더는 서비스 컨테이너에 서비스를 바인딩 하거나, 이벤트를 등록하거나, 애플리케이션이 요청을 처리할 수 있도록 준비하는 등 애플리케이션을 부트스트랩하는 역할을 합니다.

<!-- In a fresh Laravel application, this directory will already contain the `AppServiceProvider`. You are free to add your own providers to this directory as needed. -->
새로운 Laravel 애플리케이션을 설치하면 이 디렉터리에는 이미 `AppServiceProvider`가 포함되어 있습니다. 필요에 따라 직접 프로바이더를 추가해서 사용할 수 있습니다.

<a name="the-rules-directory"></a>
<!-- ### The Rules Directory -->
### The Rules Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:rule` Artisan command. The `Rules` directory contains the custom validation rule objects for your application. Rules are used to encapsulate complicated validation logic in a simple object. For more information, check out the [validation documentation](/docs/11.x/validation). -->
이 디렉터리는 기본적으로 존재하지 않지만, `make:rule` 아티즌 명령어를 실행하면 생성됩니다. `Rules` 디렉터리에는 애플리케이션에서 사용하는 커스텀 유효성 검증 Rule 객체가 포함됩니다. Rule을 사용하면 복잡한 검증 로직을 단순한 객체에 캡슐화할 수 있습니다. 더 자세한 내용은 [validation documentation](/docs/11.x/validation)를 참고하세요.
