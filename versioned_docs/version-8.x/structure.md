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
기본 Laravel 애플리케이션 구조는 대규모든 소규모든 다양한 프로젝트에 적합한 출발점을 제공하도록 설계되어 있습니다. 하지만, 여러분은 필요에 따라 애플리케이션을 원하는 방식으로 자유롭게 구성할 수 있습니다. Laravel은 클래스가 어디에 위치해야 하는지에 대해 거의 제한을 두지 않으며, Composer가 해당 클래스를 오토로드할 수만 있다면 어디든 둘 수 있습니다.

<a name="the-root-directory"></a>
<!-- ## The Root Directory -->
## The Root Directory

<a name="the-root-app-directory"></a>
<!-- #### The App Directory -->
#### The App Directory

<!-- The `app` directory contains the core code of your application. We'll explore this directory in more detail soon; however, almost all of the classes in your application will be in this directory. -->
`app` 디렉터리에는 애플리케이션의 핵심 코드가 들어 있습니다. 이 디렉터리에 대해서는 아래에서 더 자세히 소개하겠지만, 여러분이 작성하는 대부분의 클래스는 이곳에 위치하게 됩니다.

<a name="the-bootstrap-directory"></a>
<!-- #### The Bootstrap Directory -->
#### The Bootstrap Directory

<!-- The `bootstrap` directory contains the `app.php` file which bootstraps the framework. This directory also houses a `cache` directory which contains framework generated files for performance optimization such as the route and services cache files. You should not typically need to modify any files within this directory. -->
`bootstrap` 디렉터리에는 프레임워크를 부트스트랩하는 `app.php` 파일이 들어 있습니다. 이 디렉터리에는 또한 프레임워크가 성능 최적화를 위해 생성하는 라우트 및 서비스 캐시 파일 등 다양한 캐시 파일이 저장되는 `cache` 디렉터리가 있습니다. 일반적으로 이 디렉터리 내의 파일을 직접 수정할 필요는 없습니다.

<a name="the-config-directory"></a>
<!-- #### The Config Directory -->
#### The Config Directory

<!-- The `config` directory, as the name implies, contains all of your application's configuration files. It's a great idea to read through all of these files and familiarize yourself with all of the options available to you. -->
`config` 디렉터리는 이름에서 알 수 있듯이 애플리케이션의 모든 설정 파일이 들어 있습니다. 이 디렉터리의 모든 파일을 한 번씩 읽어보고, 다양한 옵션들을 숙지하는 것이 좋습니다.

<a name="the-database-directory"></a>
<!-- #### The Database Directory -->
#### The Database Directory

<!-- The `database` directory contains your database migrations, model factories, and seeds. If you wish, you may also use this directory to hold an SQLite database. -->
`database` 디렉터리에는 데이터베이스 마이그레이션, 모델 팩토리, 시드 파일이 들어 있습니다. 원한다면 이 디렉터리에 SQLite 데이터베이스 파일을 저장할 수도 있습니다.

<a name="the-public-directory"></a>
<!-- #### The Public Directory -->
#### The Public Directory

<!-- The `public` directory contains the `index.php` file, which is the entry point for all requests entering your application and configures autoloading. This directory also houses your assets such as images, JavaScript, and CSS. -->
`public` 디렉터리에는 모든 요청이 애플리케이션으로 진입할 때 사용되는 엔트리 포인트인 `index.php` 파일이 있으며, 오토로딩을 설정합니다. 이 외에도 이미지, 자바스크립트, CSS와 같은 리소스 파일(에셋)이 함께 들어 있습니다.

<a name="the-resources-directory"></a>
<!-- #### The Resources Directory -->
#### The Resources Directory

<!-- The `resources` directory contains your [views](/docs/8.x/views) as well as your raw, un-compiled assets such as CSS or JavaScript. This directory also houses all of your language files. -->
`resources` 디렉터리에는 [views](/docs/8.x/views)를 비롯해 CSS, 자바스크립트 등 컴파일되지 않은 원본 자산 파일이 들어 있습니다. 또한, 모든 언어 파일도 이 디렉터리에 위치합니다.

<a name="the-routes-directory"></a>
<!-- #### The Routes Directory -->
#### The Routes Directory

<!-- The `routes` directory contains all of the route definitions for your application. By default, several route files are included with Laravel: `web.php`, `api.php`, `console.php`, and `channels.php`. -->
`routes` 디렉터리에는 애플리케이션의 모든 라우트 정의가 들어 있습니다. 기본적으로 Laravel에는 여러 라우트 파일이 제공됩니다: `web.php`, `api.php`, `console.php`, `channels.php`가 있습니다.

<!-- The `web.php` file contains routes that the `RouteServiceProvider` places in the `web` middleware group, which provides session state, CSRF protection, and cookie encryption. If your application does not offer a stateless, RESTful API then it is likely that all of your routes will most likely be defined in the `web.php` file. -->
`web.php` 파일에는 `RouteServiceProvider`가 세션 상태 관리, CSRF 보호, 쿠키 암호화 등을 제공하는 `web` 미들웨어 그룹에 배치하는 라우트가 들어 있습니다. 만약 여러분의 애플리케이션이 상태 없는 RESTful API가 아니라면, 대부분의 라우트를 `web.php`에 정의하게 될 것입니다.

<!-- The `api.php` file contains routes that the `RouteServiceProvider` places in the `api` middleware group. These routes are intended to be stateless, so requests entering the application through these routes are intended to be authenticated [via tokens](/docs/8.x/sanctum) and will not have access to session state. -->
`api.php` 파일에는 `RouteServiceProvider`가 `api` 미들웨어 그룹으로 분류하는 라우트가 있습니다. 이 라우트들은 상태를 저장하지 않으며, 토큰 기반 인증을 통해 요청을 처리합니다([via tokens](/docs/8.x/sanctum)). 세션 상태에는 접근할 수 없습니다.

<!-- The `console.php` file is where you may define all of your closure based console commands. Each closure is bound to a command instance allowing a simple approach to interacting with each command's IO methods. Even though this file does not define HTTP routes, it defines console based entry points (routes) into your application. -->
`console.php` 파일에서는 클로저 방식의 콘솔 명령어를 정의할 수 있습니다. 각 클로저는 명령어 인스턴스에 바인딩되어, 각 명령어의 IO 메서드와 쉽게 상호작용할 수 있습니다. 이 파일은 HTTP 라우트를 정의하지 않지만, 콘솔 진입점(라우트)을 정의합니다.

<!-- The `channels.php` file is where you may register all of the [event broadcasting](/docs/8.x/broadcasting) channels that your application supports. -->
`channels.php` 파일에서는 애플리케이션에서 지원하는 [event broadcasting](/docs/8.x/broadcasting) 채널을 등록할 수 있습니다.

<a name="the-storage-directory"></a>
<!-- #### The Storage Directory -->
#### The Storage Directory

<!-- The `storage` directory contains your logs, compiled Blade templates, file based sessions, file caches, and other files generated by the framework. This directory is segregated into `app`, `framework`, and `logs` directories. The `app` directory may be used to store any files generated by your application. The `framework` directory is used to store framework generated files and caches. Finally, the `logs` directory contains your application's log files. -->
`storage` 디렉터리에는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 파일 캐시, 그 외 프레임워크에 의해 생성되는 여러 파일이 저장됩니다. 이 디렉터리는 `app`, `framework`, `logs` 하위 디렉터리로 나뉩니다. `app` 디렉터리는 애플리케이션에서 생성하는 파일을 저장할 때 사용할 수 있습니다. `framework` 디렉터리는 프레임워크가 생성하는 파일과 캐시가 저장됩니다. 마지막으로 `logs` 디렉터리에는 애플리케이션의 로그 파일이 위치합니다.

<!-- The `storage/app/public` directory may be used to store user-generated files, such as profile avatars, that should be publicly accessible. You should create a symbolic link at `public/storage` which points to this directory. You may create the link using the `php artisan storage:link` Artisan command. -->
`storage/app/public` 디렉터리는 프로필 아바타 등과 같은 사용자 생성 파일 등 공개적으로 접근 가능한 파일을 저장할 때 사용할 수 있습니다. 이 디렉터리에 연결된 심볼릭 링크를 `public/storage` 경로에 생성해야 하며, `php artisan storage:link` 아티즌 명령어를 사용해 쉽게 만들 수 있습니다.

<a name="the-tests-directory"></a>
<!-- #### The Tests Directory -->
#### The Tests Directory

<!-- The `tests` directory contains your automated tests. Example [PHPUnit](https://phpunit.de/) unit tests and feature tests are provided out of the box. Each test class should be suffixed with the word `Test`. You may run your tests using the `phpunit` or `php vendor/bin/phpunit` commands. Or, if you would like a more detailed and beautiful representation of your test results, you may run your tests using the `php artisan test` Artisan command. -->
`tests` 디렉터리에는 자동화 테스트가 들어 있습니다. 예시용 [PHPUnit](https://phpunit.de/) 단위 테스트와 기능 테스트가 기본적으로 제공됩니다. 각 테스트 클래스명은 반드시 `Test`로 끝나야 합니다. 테스트는 `phpunit` 또는 `php vendor/bin/phpunit` 명령어로 실행할 수 있으며, 테스트 결과를 좀 더 보기 좋고 상세하게 확인하고 싶다면 `php artisan test` 아티즌 명령어를 사용하면 됩니다.

<a name="the-vendor-directory"></a>
<!-- #### The Vendor Directory -->
#### The Vendor Directory

<!-- The `vendor` directory contains your [Composer](https://getcomposer.org) dependencies. -->
`vendor` 디렉터리에는 [Composer](https://getcomposer.org) 의존성이 저장됩니다.

<a name="the-app-directory"></a>
<!-- ## The App Directory -->
## The App Directory

<!-- The majority of your application is housed in the `app` directory. By default, this directory is namespaced under `App` and is autoloaded by Composer using the [PSR-4 autoloading standard](https://www.php-fig.org/psr/psr-4/). -->
애플리케이션의 대부분은 `app` 디렉터리에 들어 있습니다. 기본적으로 이 디렉터리는 `App` 네임스페이스 아래에 위치하며, [PSR-4 autoloading standard](https://www.php-fig.org/psr/psr-4/)을 통해 Composer에 의해 자동으로 로드됩니다.

<!-- The `app` directory contains a variety of additional directories such as `Console`, `Http`, and `Providers`. Think of the `Console` and `Http` directories as providing an API into the core of your application. The HTTP protocol and CLI are both mechanisms to interact with your application, but do not actually contain application logic. In other words, they are two ways of issuing commands to your application. The `Console` directory contains all of your Artisan commands, while the `Http` directory contains your controllers, middleware, and requests. -->
`app` 디렉터리에는 `Console`, `Http`, `Providers` 등 다양한 서브 디렉터리가 존재합니다. 이 중 `Console` 과 `Http` 디렉터리는 애플리케이션의 핵심에 접근하는 API 역할을 수행한다고 생각하면 이해하기 쉽습니다. HTTP 프로토콜과 CLI는 모두 애플리케이션과 상호작용하는 수단이지만, 실제 애플리케이션 로직이 포함되어 있지는 않습니다. 즉, 이들은 모두 애플리케이션에 명령을 전달하는 통로입니다. `Console` 디렉터리에는 모든 아티즌 명령어가 저장되며, `Http` 디렉터리에는 컨트롤러, 미들웨어, 폼 리퀘스트가 위치합니다.

<!-- A variety of other directories will be generated inside the `app` directory as you use the `make` Artisan commands to generate classes. So, for example, the `app/Jobs` directory will not exist until you execute the `make:job` Artisan command to generate a job class. -->
또한, 다양한 서브 디렉터리는 필요에 따라 `app` 디렉터리 안에서 `make` 아티즌 명령어로 클래스를 생성할 때 자동으로 생성됩니다. 예를 들어, `app/Jobs` 디렉터리는 `make:job` 아티즌 명령어를 실행하여 잡 클래스를 생성하기 전에는 존재하지 않습니다.

> [!TIP]
> `app` 디렉터리의 많은 클래스들은 아티즌 명령어를 통해 쉽게 생성할 수 있습니다. 사용 가능한 명령어 목록은 터미널에서 `php artisan list make` 명령어로 확인할 수 있습니다.

<a name="the-broadcasting-directory"></a>
<!-- #### The Broadcasting Directory -->
#### The Broadcasting Directory

<!-- The `Broadcasting` directory contains all of the broadcast channel classes for your application. These classes are generated using the `make:channel` command. This directory does not exist by default, but will be created for you when you create your first channel. To learn more about channels, check out the documentation on [event broadcasting](/docs/8.x/broadcasting). -->
`Broadcasting` 디렉터리에는 애플리케이션의 모든 브로드캐스트 채널 클래스가 저장됩니다. 이 클래스들은 `make:channel` 명령어로 생성합니다. 이 디렉터리는 기본적으로 존재하지 않으며, 첫 채널을 생성하면 자동으로 만들어집니다. 채널에 대한 더 자세한 정보는 [event broadcasting](/docs/8.x/broadcasting)를 참고해 보세요.

<a name="the-console-directory"></a>
<!-- #### The Console Directory -->
#### The Console Directory

<!-- The `Console` directory contains all of the custom Artisan commands for your application. These commands may be generated using the `make:command` command. This directory also houses your console kernel, which is where your custom Artisan commands are registered and your [scheduled tasks](/docs/8.x/scheduling) are defined. -->
`Console` 디렉터리에는 애플리케이션의 모든 커스텀 아티즌 명령어가 저장됩니다. 이 명령어들은 `make:command` 명령어로 생성할 수 있습니다. 또한 이 디렉터리에는 커스텀 아티즌 명령어를 등록하거나 [scheduled tasks](/docs/8.x/scheduling)을 정의할 때 사용하는 콘솔 커널도 함께 포함되어 있습니다.

<a name="the-events-directory"></a>
<!-- #### The Events Directory -->
#### The Events Directory

<!-- This directory does not exist by default, but will be created for you by the `event:generate` and `make:event` Artisan commands. The `Events` directory houses [event classes](/docs/8.x/events). Events may be used to alert other parts of your application that a given action has occurred, providing a great deal of flexibility and decoupling. -->
이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 또는 `make:event` 아티즌 명령어를 실행하면 자동으로 생성됩니다. `Events` 디렉터리에는 [event classes](/docs/8.x/events)가 저장됩니다. 이벤트는 특정 행동이 발생했음을 애플리케이션의 다른 부분에 알릴 때 사용되며, 유연성과 결합도를 낮추는 데 매우 유용합니다.

<a name="the-exceptions-directory"></a>
<!-- #### The Exceptions Directory -->
#### The Exceptions Directory

<!-- The `Exceptions` directory contains your application's exception handler and is also a good place to place any exceptions thrown by your application. If you would like to customize how your exceptions are logged or rendered, you should modify the `Handler` class in this directory. -->
`Exceptions` 디렉터리에는 애플리케이션의 예외 처리기가 들어 있으며, 애플리케이션에서 발생하는 예외를 정의하는 것도 좋은 위치입니다. 예외가 기록되거나 렌더링되는 방식을 커스터마이즈하려면 이 디렉터리 내의 `Handler` 클래스를 수정하면 됩니다.

<a name="the-http-directory"></a>
<!-- #### The Http Directory -->
#### The Http Directory

<!-- The `Http` directory contains your controllers, middleware, and form requests. Almost all of the logic to handle requests entering your application will be placed in this directory. -->
`Http` 디렉터리에는 컨트롤러, 미들웨어, 폼 리퀘스트가 저장됩니다. 애플리케이션으로 들어오는 요청을 처리하는 로직의 대부분은 이 디렉터리에 위치하게 됩니다.

<a name="the-jobs-directory"></a>
<!-- #### The Jobs Directory -->
#### The Jobs Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:job` Artisan command. The `Jobs` directory houses the [queueable jobs](/docs/8.x/queues) for your application. Jobs may be queued by your application or run synchronously within the current request lifecycle. Jobs that run synchronously during the current request are sometimes referred to as "commands" since they are an implementation of the [command pattern](https://en.wikipedia.org/wiki/Command_pattern). -->
이 디렉터리는 기본적으로 존재하지 않지만, `make:job` 아티즌 명령어를 실행하면 생성됩니다. `Jobs` 디렉터리에는 애플리케이션에서 사용하는 [queueable jobs](/docs/8.x/queues)가 담겨 있습니다. 잡은 애플리케이션에서 큐에 의해 처리되거나, 현재 요청의 실행 흐름 내에서 동기적으로 실행될 수도 있습니다. 요청 흐름 내에서 동기적으로 실행되는 잡은 종종 "커맨드 패턴"([command pattern](https://en.wikipedia.org/wiki/Command_pattern))의 구현체로서 "커맨드"라고 불리기도 합니다.

<a name="the-listeners-directory"></a>
<!-- #### The Listeners Directory -->
#### The Listeners Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `event:generate` or `make:listener` Artisan commands. The `Listeners` directory contains the classes that handle your [events](/docs/8.x/events). Event listeners receive an event instance and perform logic in response to the event being fired. For example, a `UserRegistered` event might be handled by a `SendWelcomeEmail` listener. -->
이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 또는 `make:listener` 아티즌 명령어를 실행하면 생성됩니다. `Listeners` 디렉터리에는 [events](/docs/8.x/events)를 처리하는 클래스가 포함됩니다. 이벤트 리스너는 이벤트 인스턴스를 받아 해당 이벤트가 발생했을 때 처리해야 할 로직을 실행합니다. 예를 들어, `UserRegistered` 이벤트가 발생하면 `SendWelcomeEmail` 리스너가 해당 이벤트를 처리할 수 있습니다.

<a name="the-mail-directory"></a>
<!-- #### The Mail Directory -->
#### The Mail Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:mail` Artisan command. The `Mail` directory contains all of your [classes that represent emails](/docs/8.x/mail) sent by your application. Mail objects allow you to encapsulate all of the logic of building an email in a single, simple class that may be sent using the `Mail::send` method. -->
이 디렉터리는 기본적으로 존재하지 않지만, `make:mail` 아티즌 명령어를 실행하면 생성됩니다. `Mail` 디렉터리에는 애플리케이션에서 전송하는 [classes that represent emails](/docs/8.x/mail)가 모두 저장됩니다. Mail 객체를 이용하면 이메일 작성에 필요한 모든 로직을 하나의 간단한 클래스로 캡슐화할 수 있으며, `Mail::send` 메서드를 사용해 전송할 수 있습니다.

<a name="the-models-directory"></a>
<!-- #### The Models Directory -->
#### The Models Directory

<!-- The `Models` directory contains all of your [Eloquent model classes](/docs/8.x/eloquent). The Eloquent ORM included with Laravel provides a beautiful, simple ActiveRecord implementation for working with your database. Each database table has a corresponding "Model" which is used to interact with that table. Models allow you to query for data in your tables, as well as insert new records into the table. -->
`Models` 디렉터리에는 모든 [Eloquent model classes](/docs/8.x/eloquent)가 들어 있습니다. Laravel에 포함된 Eloquent ORM은 데이터베이스 작업을 위한 간단하면서도 강력한 액티브 레코드 방식의 구현체를 제공합니다. 각 데이터베이스 테이블에는 해당 테이블과 상호작용하는 "모델"이 대응되며, 모델을 사용하면 테이블에서 데이터를 조회하거나 새로운 레코드를 삽입할 수 있습니다.

<a name="the-notifications-directory"></a>
<!-- #### The Notifications Directory -->
#### The Notifications Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:notification` Artisan command. The `Notifications` directory contains all of the "transactional" [notifications](/docs/8.x/notifications) that are sent by your application, such as simple notifications about events that happen within your application. Laravel's notification feature abstracts sending notifications over a variety of drivers such as email, Slack, SMS, or stored in a database. -->
이 디렉터리는 기본적으로 존재하지 않지만, `make:notification` 아티즌 명령어를 실행하면 생성됩니다. `Notifications` 디렉터리에는 애플리케이션에서 전송하는 "트랜잭셔널" [notifications](/docs/8.x/notifications) 클래스가 모두 들어 있습니다. 예를 들어, 애플리케이션 내에서 발생하는 이벤트에 대한 간단한 알림 등이 여기에 포함됩니다. Laravel의 알림 기능은 이메일, Slack, SMS, 데이터베이스 저장 등 다양한 드라이버를 통한 알림 발송을 추상화해줍니다.

<a name="the-policies-directory"></a>
<!-- #### The Policies Directory -->
#### The Policies Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:policy` Artisan command. The `Policies` directory contains the [authorization policy classes](/docs/8.x/authorization) for your application. Policies are used to determine if a user can perform a given action against a resource. -->
이 디렉터리는 기본적으로 존재하지 않지만, `make:policy` 아티즌 명령어를 실행하면 생성됩니다. `Policies` 디렉터리에는 애플리케이션의 [authorization policy classes](/docs/8.x/authorization)가 들어 있습니다. 정책은 사용자가 특정 리소스에 대해 특정 동작을 수행할 수 있는지 판단하는 데 사용됩니다.

<a name="the-providers-directory"></a>
<!-- #### The Providers Directory -->
#### The Providers Directory

<!-- The `Providers` directory contains all of the [service providers](/docs/8.x/providers) for your application. Service providers bootstrap your application by binding services in the service container, registering events, or performing any other tasks to prepare your application for incoming requests. -->
`Providers` 디렉터리에는 애플리케이션의 [service providers](/docs/8.x/providers)가 모두 저장됩니다. 서비스 프로바이더는 서비스 컨테이너에 서비스 바인딩, 이벤트 등록, 그 외 애플리케이션이 요청을 받을 준비를 하는 데 필요한 작업을 수행해 애플리케이션을 부트스트랩합니다.

<!-- In a fresh Laravel application, this directory will already contain several providers. You are free to add your own providers to this directory as needed. -->
새로운 Laravel 애플리케이션을 생성하면 이 디렉터리에는 여러 기본 프로바이더가 이미 들어 있습니다. 필요하다면 이곳에 직접 프로바이더를 추가해 사용할 수 있습니다.

<a name="the-rules-directory"></a>
<!-- #### The Rules Directory -->
#### The Rules Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:rule` Artisan command. The `Rules` directory contains the custom validation rule objects for your application. Rules are used to encapsulate complicated validation logic in a simple object. For more information, check out the [validation documentation](/docs/8.x/validation). -->
이 디렉터리는 기본적으로 존재하지 않지만, `make:rule` 아티즌 명령어를 실행하면 생성됩니다. `Rules` 디렉터리에는 애플리케이션의 커스텀 유효성 검증 룰 객체들이 들어 있습니다. 룰 객체는 복잡한 유효성 검증 로직을 단순한 객체로 캡슐화하는 데 사용됩니다. 더 자세한 내용은 [validation documentation](/docs/8.x/validation)를 참고해주세요.
