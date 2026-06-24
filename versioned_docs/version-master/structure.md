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
기본 Laravel 애플리케이션 구조는 대규모 및 소규모 애플리케이션 모두에 훌륭한 출발점을 제공합니다. 그러나 애플리케이션을 원하는 대로 자유롭게 구성할 수 있습니다. Laravel은 Composer로 클래스가 자동 로드되는 한, 특정 클래스가 어디에 위치해야 하는지에 대해 거의 제약을 두지 않습니다.

<a name="the-root-directory"></a>
<!-- ## The Root Directory -->
## The Root Directory

<a name="the-root-app-directory"></a>
<!-- ### The App Directory -->
### The App Directory

<!-- The `app` directory contains the core code of your application. We'll explore this directory in more detail soon; however, almost all of the classes in your application will be in this directory. -->
`app` 디렉토리는 애플리케이션의 핵심 코드를 포함합니다. 이후에 이 디렉토리를 더 자세히 살펴보겠지만, 애플리케이션 내 거의 모든 클래스는 이 디렉토리에 위치합니다.

<a name="the-bootstrap-directory"></a>
<!-- ### The Bootstrap Directory -->
### The Bootstrap Directory

<!-- The `bootstrap` directory contains the `app.php` file which bootstraps the framework. This directory also houses a `cache` directory which contains framework generated files for performance optimization such as the route and services cache files. -->
`bootstrap` 디렉토리는 프레임워크를 부트스트랩하는 `app.php` 파일을 포함합니다. 또한 이 디렉토리에는 라우트 및 서비스 캐시 파일과 같이 성능 최적화를 위해 프레임워크가 생성하는 파일들이 위치한 `cache` 디렉토리도 있습니다.

<a name="the-config-directory"></a>
<!-- ### The Config Directory -->
### The Config Directory

<!-- The `config` directory, as the name implies, contains all of your application's configuration files. It's a great idea to read through all of these files and familiarize yourself with all of the options available to you. -->
이름 그대로 `config` 디렉토리는 애플리케이션의 모든 설정 파일을 포함합니다. 이 파일들을 읽으면서 제공되는 설정 옵션들을 익히는 것이 좋습니다.

<a name="the-database-directory"></a>
<!-- ### The Database Directory -->
### The Database Directory

<!-- The `database` directory contains your database migrations, model factories, and seeds. If you wish, you may also use this directory to hold an SQLite database. -->
`database` 디렉토리에는 데이터베이스 마이그레이션, 모델 팩토리, 시드가 있습니다. 원한다면 SQLite 데이터베이스 파일도 이 디렉토리에 둘 수 있습니다.

<a name="the-public-directory"></a>
<!-- ### The Public Directory -->
### The Public Directory

<!-- The `public` directory contains the `index.php` file, which is the entry point for all requests entering your application and configures autoloading. This directory also houses your assets such as images, JavaScript, and CSS. -->
`public` 디렉토리에는 애플리케이션에 들어오는 모든 요청의 진입점인 `index.php` 파일이 있습니다. 이 파일은 자동 로딩을 구성합니다. 또한 이미지, JavaScript, CSS 등의 정적 자산도 이 디렉토리에 위치합니다.

<a name="the-resources-directory"></a>
<!-- ### The Resources Directory -->
### The Resources Directory

<!-- The `resources` directory contains your [views](/docs/master/views) as well as your raw, un-compiled assets such as CSS or JavaScript. -->
`resources` 디렉토리에는 [views](/docs/master/views)와 CSS, JavaScript 등 컴파일되지 않은 원본 자산이 포함됩니다.

<a name="the-routes-directory"></a>
<!-- ### The Routes Directory -->
### The Routes Directory

<!-- The `routes` directory contains all of the route definitions for your application. By default, two route files are included with Laravel: `web.php` and `console.php`. -->
`routes` 디렉토리는 애플리케이션의 모든 라우트 정의를 포함합니다. 기본적으로 Laravel은 `web.php`와 `console.php` 두 개의 라우트 파일을 제공합니다.

<!-- The `web.php` file contains routes that Laravel places in the `web` middleware group, which provides session state, CSRF protection, and cookie encryption. If your application does not offer a stateless, RESTful API then all your routes will most likely be defined in the `web.php` file. -->
`web.php` 파일은 Laravel이 `web` 미들웨어 그룹에 위치시키는 라우트를 포함하며, 이 그룹은 세션 상태, CSRF 보호, 쿠키 암호화를 지원합니다. 애플리케이션이 상태 비저장(stateless) RESTful API를 제공하지 않는다면, 대부분 라우트는 `web.php`에 정의되어 있을 것입니다.

<!-- The `console.php` file is where you may define all of your closure-based console commands. Each closure is bound to a command instance allowing a simple approach to interacting with each command's IO methods. Even though this file does not define HTTP routes, it defines console based entry points (routes) into your application. You may also [schedule](/docs/master/scheduling) tasks in the `console.php` file. -->
`console.php` 파일은 클로저 기반 콘솔 명령어를 정의할 수 있는 곳입니다. 각 클로저는 명령 인스턴스에 바인딩되어 있어, 각 명령어의 IO 메서드와 쉽게 상호작용할 수 있습니다. 이 파일은 HTTP 라우트를 정의하지는 않지만, 콘솔 기반의 진입점(라우트)을 정의합니다. `console.php` 파일에서 [schedule](/docs/master/scheduling) 작업도 정의할 수 있습니다.

<!-- Optionally, you may install additional route files for API routes (`api.php`) and broadcasting channels (`channels.php`), via the `install:api` and `install:broadcasting` Artisan commands. -->
선택적으로, `install:api` 및 `install:broadcasting` Artisan 명령어를 통해 API 라우트(`api.php`) 및 브로드캐스팅 채널(`channels.php`)용 라우트 파일을 추가로 설치할 수 있습니다.

<!-- The `api.php` file contains routes that are intended to be stateless, so requests entering the application through these routes are intended to be authenticated [via tokens](/docs/master/sanctum) and will not have access to session state. -->
`api.php` 파일은 상태 비저장이며, 이 경로를 통해 들어오는 요청은 [via tokens](/docs/master/sanctum)을 통해 인증되어야 하고 세션 상태에 접근하지 않습니다.

<!-- The `channels.php` file is where you may register all of the [event broadcasting](/docs/master/broadcasting) channels that your application supports. -->
`channels.php` 파일은 애플리케이션이 지원하는 모든 [event broadcasting](/docs/master/broadcasting) 채널을 등록하는 곳입니다.

<a name="the-storage-directory"></a>
<!-- ### The Storage Directory -->
### The Storage Directory

<!-- The `storage` directory contains your logs, compiled Blade templates, file based sessions, file caches, and other files generated by the framework. This directory is segregated into `app`, `framework`, and `logs` directories. The `app` directory may be used to store any files generated by your application. The `framework` directory is used to store framework generated files and caches. Finally, the `logs` directory contains your application's log files. -->
`storage` 디렉토리에는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 파일 캐시 및 프레임워크가 생성하는 기타 파일들이 포함됩니다. 이 디렉토리는 `app`, `framework`, `logs` 하위 디렉토리로 구분됩니다. `app` 디렉토리는 애플리케이션이 생성하는 파일을 저장할 수 있습니다. `framework` 디렉토리는 프레임워크가 생성한 파일과 캐시를 저장합니다. 마지막으로 `logs` 디렉토리에는 애플리케이션 로그 파일이 있습니다.

<!-- The `storage/app/public` directory may be used to store user-generated files, such as profile avatars, that should be publicly accessible. You should create a symbolic link at `public/storage` which points to this directory. You may create the link using the `php artisan storage:link` Artisan command. -->
`storage/app/public` 디렉토리는 프로필 아바타 등 사용자 생성 파일을 공개적으로 접근 가능하도록 저장하는 데 사용될 수 있습니다. 이 디렉토리를 가리키는 `public/storage`에 심볼릭 링크를 생성하는 것이 좋습니다. `php artisan storage:link` Artisan 명령어로 이 링크를 생성할 수 있습니다.

<a name="the-tests-directory"></a>
<!-- ### The Tests Directory -->
### The Tests Directory

<!-- The `tests` directory contains your automated tests. Example [Pest](https://pestphp.com) or [PHPUnit](https://phpunit.de/) unit tests and feature tests are provided out of the box. Each test class should be suffixed with the word `Test`. You may run your tests using the `/vendor/bin/pest` or `/vendor/bin/phpunit` commands. Or, if you would like a more detailed and beautiful representation of your test results, you may run your tests using the `php artisan test` Artisan command. -->
`tests` 디렉토리에는 자동화된 테스트가 포함됩니다. 예시로 [Pest](https://pestphp.com)나 [PHPUnit](https://phpunit.de/) 단위 테스트 및 기능 테스트가 기본 제공됩니다. 각 테스트 클래스는 `Test` 접미사를 붙여야 합니다. 테스트는 `/vendor/bin/pest` 또는 `/vendor/bin/phpunit` 명령어로 실행할 수 있으며, 더 자세하고 깔끔한 테스트 결과를 원하면 `php artisan test` Artisan 명령어로도 실행할 수 있습니다.

<a name="the-vendor-directory"></a>
<!-- ### The Vendor Directory -->
### The Vendor Directory

<!-- The `vendor` directory contains your [Composer](https://getcomposer.org) dependencies. -->
`vendor` 디렉토리에는 [Composer](https://getcomposer.org) 의존성이 저장됩니다.

<a name="the-app-directory"></a>
<!-- ## The App Directory -->
## The App Directory

<!-- The majority of your application is housed in the `app` directory. By default, this directory is namespaced under `App` and is autoloaded by Composer using the [PSR-4 autoloading standard](https://www.php-fig.org/psr/psr-4/). -->
애플리케이션 대부분은 `app` 디렉토리에 위치합니다. 기본적으로 이 디렉토리는 `App` 네임스페이스가 적용되며, Composer에 의해 [PSR-4 autoloading standard](https://www.php-fig.org/psr/psr-4/)을 사용해 자동 로드됩니다.

<!-- By default, the `app` directory contains the `Http`, `Models`, and `Providers` directories. However, over time, a variety of other directories will be generated inside the app directory as you use the make Artisan commands to generate classes. For example, the `app/Console` directory will not exist until you execute the `make:command` Artisan command to generate a command class. -->
기본적으로 `app` 디렉토리 내에는 `Http`, `Models`, `Providers` 디렉토리가 있습니다. 하지만 시간이 지나면서 Artisan의 make 명령어를 사용해 클래스를 생성할 때 다양한 다른 디렉토리들이 app 내부에 생성됩니다. 예를 들어, `app/Console` 디렉토리는 `make:command` Artisan 명령어를 실행해 명령 클래스가 생성되기 전까지는 존재하지 않습니다.

<!-- Both the `Console` and `Http` directories are further explained in their respective sections below, but think of the `Console` and `Http` directories as providing an API into the core of your application. The HTTP protocol and CLI are both mechanisms to interact with your application, but do not actually contain application logic. In other words, they are two ways of issuing commands to your application. The `Console` directory contains all of your Artisan commands, while the `Http` directory contains your controllers, middleware, and requests. -->
`Console` 및 `Http` 디렉토리는 아래에서 각각 더 자세히 설명하지만, `Console` 및 `Http` 디렉토리는 애플리케이션 핵심에 API 역할을 합니다. HTTP 프로토콜과 CLI는 모두 애플리케이션과 상호작용하는 방식이지만, 실제 애플리케이션 로직은 포함하지 않습니다. 즉, 애플리케이션에 명령을 전달하는 두 가지 방법입니다. `Console` 디렉토리에는 모든 Artisan 명령어가, `Http` 디렉토리에는 컨트롤러, 미들웨어, 요청 클래스가 있습니다.

> [!NOTE]
> `app` 디렉토리 내 많은 클래스들은 Artisan 명령어를 통해 생성할 수 있습니다. 사용 가능한 명령어를 확인하려면 터미널에서 `php artisan list make` 명령어를 실행하세요.

<a name="the-broadcasting-directory"></a>
<!-- ### The Broadcasting Directory -->
### The Broadcasting Directory

<!-- The `Broadcasting` directory contains all of the broadcast channel classes for your application. These classes are generated using the `make:channel` command. This directory does not exist by default, but will be created for you when you create your first channel. To learn more about channels, check out the documentation on [event broadcasting](/docs/master/broadcasting). -->
`Broadcasting` 디렉토리에는 애플리케이션의 브로드캐스트 채널 클래스가 모두 포함됩니다. 이 클래스들은 `make:channel` 명령어로 생성됩니다. 기본 상태에서는 이 디렉토리가 없지만, 첫 번째 채널 생성 시 자동으로 만들어집니다. 채널에 대한 자세한 내용은 [event broadcasting](/docs/master/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
<!-- ### The Console Directory -->
### The Console Directory

<!-- The `Console` directory contains all of the custom Artisan commands for your application. These commands may be generated using the `make:command` command. -->
`Console` 디렉토리에는 애플리케이션에 맞춤화한 모든 Artisan 명령어가 포함됩니다. 이 명령어들은 `make:command` 명령어로 생성할 수 있습니다.

<a name="the-events-directory"></a>
<!-- ### The Events Directory -->
### The Events Directory

<!-- This directory does not exist by default, but will be created for you by the `event:generate` and `make:event` Artisan commands. The `Events` directory houses [event classes](/docs/master/events). Events may be used to alert other parts of your application that a given action has occurred, providing a great deal of flexibility and decoupling. -->
기본적으로는 없지만, `event:generate` 또는 `make:event` Artisan 명령어를 실행하면 만들어집니다. `Events` 디렉토리에는 [event classes](/docs/master/events)가 담깁니다. 이벤트는 애플리케이션 내 다른 부분에 특정 동작이 발생했음을 알리기 위해 사용되며, 큰 유연성과 느슨한 결합을 제공합니다.

<a name="the-exceptions-directory"></a>
<!-- ### The Exceptions Directory -->
### The Exceptions Directory

<!-- The `Exceptions` directory contains all of the custom exceptions for your application. These exceptions may be generated using the `make:exception` command. -->
`Exceptions` 디렉토리에는 애플리케이션에서 사용하는 모든 커스텀 예외 클래스가 포함됩니다. 이 예외 클래스들은 `make:exception` 명령어로 생성할 수 있습니다.

<a name="the-http-directory"></a>
<!-- ### The Http Directory -->
### The Http Directory

<!-- The `Http` directory contains your controllers, middleware, and form requests. Almost all of the logic to handle requests entering your application will be placed in this directory. -->
`Http` 디렉토리에는 컨트롤러, 미들웨어, 폼 요청이 포함됩니다. 애플리케이션에 들어오는 요청을 처리하는 거의 모든 로직이 이곳에 배치됩니다.

<a name="the-jobs-directory"></a>
<!-- ### The Jobs Directory -->
### The Jobs Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:job` Artisan command. The `Jobs` directory houses the [queueable jobs](/docs/master/queues) for your application. Jobs may be queued by your application or run synchronously within the current request lifecycle. Jobs that run synchronously during the current request are sometimes referred to as "commands" since they are an implementation of the [command pattern](https://en.wikipedia.org/wiki/Command_pattern). -->
기본적으로는 없지만, `make:job` Artisan 명령어를 실행하면 생성됩니다. `Jobs` 디렉토리에는 애플리케이션의 [queueable jobs](/docs/master/queues)이 저장됩니다. 작업은 애플리케이션에서 큐에 넣거나 현재 요청 라이프사이클 내에서 동기적으로 실행할 수 있습니다. 현재 요청 중 동기 실행되는 작업은 때때로 [command pattern](https://en.wikipedia.org/wiki/Command_pattern)을 구현한 "commands"라 부르기도 합니다.

<a name="the-listeners-directory"></a>
<!-- ### The Listeners Directory -->
### The Listeners Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `event:generate` or `make:listener` Artisan commands. The `Listeners` directory contains the classes that handle your [events](/docs/master/events). Event listeners receive an event instance and perform logic in response to the event being fired. For example, a `UserRegistered` event might be handled by a `SendWelcomeEmail` listener. -->
기본적으로는 없지만, `event:generate` 또는 `make:listener` Artisan 명령어로 생성됩니다. `Listeners` 디렉토리에는 [events](/docs/master/events)를 처리하는 클래스가 포함됩니다. 이벤트 리스너는 이벤트 인스턴스를 받아 이벤트 발생에 대응하는 로직을 수행합니다. 예를 들어, `UserRegistered` 이벤트는 `SendWelcomeEmail` 리스너로 처리할 수 있습니다.

<a name="the-mail-directory"></a>
<!-- ### The Mail Directory -->
### The Mail Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:mail` Artisan command. The `Mail` directory contains all of your [classes that represent emails](/docs/master/mail) sent by your application. Mail objects allow you to encapsulate all of the logic of building an email in a single, simple class that may be sent using the `Mail::send` method. -->
기본적으로는 없지만, `make:mail` Artisan 명령어로 생성됩니다. `Mail` 디렉토리에는 애플리케이션에서 발송하는 [classes that represent emails](/docs/master/mail)가 포함됩니다. 메일 객체는 이메일을 만드는 모든 로직을 단일, 간단한 클래스로 캡슐화하며, `Mail::send` 메서드를 통해 메일을 보낼 수 있습니다.

<a name="the-models-directory"></a>
<!-- ### The Models Directory -->
### The Models Directory

<!-- The `Models` directory contains all of your [Eloquent model classes](/docs/master/eloquent). The Eloquent ORM included with Laravel provides a beautiful, simple ActiveRecord implementation for working with your database. Each database table has a corresponding "Model" which is used to interact with that table. Models allow you to query for data in your tables, as well as insert new records into the table. -->
`Models` 디렉토리에는 모든 [Eloquent model classes](/docs/master/eloquent)가 포함됩니다. Laravel에 포함된 Eloquent ORM은 데이터베이스와 작업하기 위한 아름답고 간단한 ActiveRecord 구현체를 제공합니다. 각 데이터베이스 테이블은 해당 테이블과 상호작용할 모델 클래스와 연결됩니다. 모델을 통해 테이블 내 데이터를 조회하거나 새 레코드를 삽입할 수 있습니다.

<a name="the-notifications-directory"></a>
<!-- ### The Notifications Directory -->
### The Notifications Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:notification` Artisan command. The `Notifications` directory contains all of the "transactional" [notifications](/docs/master/notifications) that are sent by your application, such as simple notifications about events that happen within your application. Laravel's notification feature abstracts sending notifications over a variety of drivers such as email, Slack, SMS, or stored in a database. -->
기본적으로는 없지만, `make:notification` Artisan 명령어로 생성됩니다. `Notifications` 디렉토리에는 애플리케이션에서 발송하는 "트랜잭션성" [notifications](/docs/master/notifications)이 포함됩니다. 예를 들어 애플리케이션 내에서 발생하는 이벤트에 대한 간단한 알림이 이에 해당합니다. Laravel의 알림 기능은 이메일, Slack, SMS, 데이터베이스 저장 등 다양한 드라이버에 걸쳐 알림 발송을 추상화합니다.

<a name="the-policies-directory"></a>
<!-- ### The Policies Directory -->
### The Policies Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:policy` Artisan command. The `Policies` directory contains the [authorization policy classes](/docs/master/authorization) for your application. Policies are used to determine if a user can perform a given action against a resource. -->
기본적으로는 없지만, `make:policy` Artisan 명령어로 생성됩니다. `Policies` 디렉토리에는 애플리케이션의 [authorization policy classes](/docs/master/authorization)가 포함됩니다. 정책은 사용자가 특정 리소스에 대해 주어진 작업을 수행할 수 있는지 결정할 때 사용됩니다.

<a name="the-providers-directory"></a>
<!-- ### The Providers Directory -->
### The Providers Directory

<!-- The `Providers` directory contains all of the [service providers](/docs/master/providers) for your application. Service providers bootstrap your application by binding services in the service container, registering events, or performing any other tasks to prepare your application for incoming requests. -->
`Providers` 디렉토리에는 애플리케이션의 모든 [service providers](/docs/master/providers)가 포함됩니다. 서비스 프로바이더는 서비스 컨테이너에 서비스를 바인딩하거나 이벤트 등록, 애플리케이션이 요청을 처리할 준비를 마치기 위한 작업을 수행함으로써 애플리케이션을 부트스트랩합니다.

<!-- In a fresh Laravel application, this directory will already contain the `AppServiceProvider`. You are free to add your own providers to this directory as needed. -->
새로운 Laravel 애플리케이션에서는 기본적으로 `AppServiceProvider`가 포함되어 있습니다. 필요에 따라 이 디렉토리에 자신의 프로바이더를 추가할 수 있습니다.

<a name="the-rules-directory"></a>
<!-- ### The Rules Directory -->
### The Rules Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:rule` Artisan command. The `Rules` directory contains the custom validation rule objects for your application. Rules are used to encapsulate complicated validation logic in a simple object. For more information, check out the [validation documentation](/docs/master/validation). -->
기본적으로는 없지만, `make:rule` Artisan 명령어로 생성됩니다. `Rules` 디렉토리에는 애플리케이션에서 사용하는 커스텀 유효성 검증 규칙 객체들이 포함됩니다. 규칙은 복잡한 검증 로직을 단순한 객체로 캡슐화하는 데 사용됩니다. 자세한 내용은 [validation documentation](/docs/master/validation)를 참고하세요.
