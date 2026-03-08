# 디렉토리 구조 (Directory Structure)

- [소개](#introduction)
- [루트 디렉토리](#the-root-directory)
    - [`app` 디렉토리](#the-root-app-directory)
    - [`bootstrap` 디렉토리](#the-bootstrap-directory)
    - [`config` 디렉토리](#the-config-directory)
    - [`database` 디렉토리](#the-database-directory)
    - [`public` 디렉토리](#the-public-directory)
    - [`resources` 디렉토리](#the-resources-directory)
    - [`routes` 디렉토리](#the-routes-directory)
    - [`storage` 디렉토리](#the-storage-directory)
    - [`tests` 디렉토리](#the-tests-directory)
    - [`vendor` 디렉토리](#the-vendor-directory)
- [App 디렉토리](#the-app-directory)
    - [`Broadcasting` 디렉토리](#the-broadcasting-directory)
    - [`Console` 디렉토리](#the-console-directory)
    - [`Events` 디렉토리](#the-events-directory)
    - [`Exceptions` 디렉토리](#the-exceptions-directory)
    - [`Http` 디렉토리](#the-http-directory)
    - [`Jobs` 디렉토리](#the-jobs-directory)
    - [`Listeners` 디렉토리](#the-listeners-directory)
    - [`Mail` 디렉토리](#the-mail-directory)
    - [`Models` 디렉토리](#the-models-directory)
    - [`Notifications` 디렉토리](#the-notifications-directory)
    - [`Policies` 디렉토리](#the-policies-directory)
    - [`Providers` 디렉토리](#the-providers-directory)
    - [`Rules` 디렉토리](#the-rules-directory)

<a name="introduction"></a>
## 소개

기본 Laravel 애플리케이션 구조는 대규모 및 소규모 애플리케이션 모두에 훌륭한 출발점을 제공합니다. 그러나 애플리케이션을 원하는 대로 자유롭게 구성할 수 있습니다. Laravel은 Composer로 클래스가 자동 로드되는 한, 특정 클래스가 어디에 위치해야 하는지에 대해 거의 제약을 두지 않습니다.

<a name="the-root-directory"></a>
## 루트 디렉토리

<a name="the-root-app-directory"></a>
### `app` 디렉토리

`app` 디렉토리는 애플리케이션의 핵심 코드를 포함합니다. 이후에 이 디렉토리를 더 자세히 살펴보겠지만, 애플리케이션 내 거의 모든 클래스는 이 디렉토리에 위치합니다.

<a name="the-bootstrap-directory"></a>
### `bootstrap` 디렉토리

`bootstrap` 디렉토리는 프레임워크를 부트스트랩하는 `app.php` 파일을 포함합니다. 또한 이 디렉토리에는 라우트 및 서비스 캐시 파일과 같이 성능 최적화를 위해 프레임워크가 생성하는 파일들이 위치한 `cache` 디렉토리도 있습니다.

<a name="the-config-directory"></a>
### `config` 디렉토리

이름 그대로 `config` 디렉토리는 애플리케이션의 모든 설정 파일을 포함합니다. 이 파일들을 읽으면서 제공되는 설정 옵션들을 익히는 것이 좋습니다.

<a name="the-database-directory"></a>
### `database` 디렉토리

`database` 디렉토리에는 데이터베이스 마이그레이션, 모델 팩토리, 시드가 있습니다. 원한다면 SQLite 데이터베이스 파일도 이 디렉토리에 둘 수 있습니다.

<a name="the-public-directory"></a>
### `public` 디렉토리

`public` 디렉토리에는 애플리케이션에 들어오는 모든 요청의 진입점인 `index.php` 파일이 있습니다. 이 파일은 자동 로딩을 구성합니다. 또한 이미지, JavaScript, CSS 등의 정적 자산도 이 디렉토리에 위치합니다.

<a name="the-resources-directory"></a>
### `resources` 디렉토리

`resources` 디렉토리에는 [뷰](/docs/12.x/views)와 CSS, JavaScript 등 컴파일되지 않은 원본 자산이 포함됩니다.

<a name="the-routes-directory"></a>
### `routes` 디렉토리

`routes` 디렉토리는 애플리케이션의 모든 라우트 정의를 포함합니다. 기본적으로 Laravel은 `web.php`와 `console.php` 두 개의 라우트 파일을 제공합니다.

`web.php` 파일은 Laravel이 `web` 미들웨어 그룹에 위치시키는 라우트를 포함하며, 이 그룹은 세션 상태, CSRF 보호, 쿠키 암호화를 지원합니다. 애플리케이션이 상태 비저장(stateless) RESTful API를 제공하지 않는다면, 대부분 라우트는 `web.php`에 정의되어 있을 것입니다.

`console.php` 파일은 클로저 기반 콘솔 명령어를 정의할 수 있는 곳입니다. 각 클로저는 명령 인스턴스에 바인딩되어 있어, 각 명령어의 IO 메서드와 쉽게 상호작용할 수 있습니다. 이 파일은 HTTP 라우트를 정의하지는 않지만, 콘솔 기반의 진입점(라우트)을 정의합니다. 이 파일에서 [스케줄](/docs/12.x/scheduling) 작업도 정의할 수 있습니다.

선택적으로, `install:api` 및 `install:broadcasting` Artisan 명령어를 통해 API 라우트(`api.php`) 및 브로드캐스팅 채널(`channels.php`)용 라우트 파일을 추가로 설치할 수 있습니다.

`api.php` 파일은 상태 비저장이며, 이 경로를 통해 들어오는 요청은 [토큰 인증](/docs/12.x/sanctum)을 통해 인증되어야 하고 세션 상태에 접근하지 않습니다.

`channels.php` 파일은 애플리케이션이 지원하는 모든 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 채널을 등록하는 곳입니다.

<a name="the-storage-directory"></a>
### `storage` 디렉토리

`storage` 디렉토리에는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 파일 캐시 및 프레임워크가 생성하는 기타 파일들이 포함됩니다. 이 디렉토리는 `app`, `framework`, `logs` 하위 디렉토리로 구분됩니다. `app` 디렉토리는 애플리케이션이 생성하는 파일을 저장할 수 있습니다. `framework` 디렉토리는 프레임워크가 생성한 파일과 캐시를 저장합니다. 마지막으로 `logs` 디렉토리에는 애플리케이션 로그 파일이 있습니다.

`storage/app/public` 디렉토리는 프로필 아바타 등 사용자 생성 파일을 공개적으로 접근 가능하도록 저장하는 데 사용될 수 있습니다. 이 디렉토리를 가리키는 `public/storage`에 심볼릭 링크를 생성하는 것이 좋습니다. `php artisan storage:link` Artisan 명령어로 이 링크를 생성할 수 있습니다.

<a name="the-tests-directory"></a>
### `tests` 디렉토리

`tests` 디렉토리에는 자동화된 테스트가 포함됩니다. 예시로 [Pest](https://pestphp.com)나 [PHPUnit](https://phpunit.de/) 단위 테스트 및 기능 테스트가 기본 제공됩니다. 각 테스트 클래스는 `Test` 접미사를 붙여야 합니다. 테스트는 `/vendor/bin/pest` 또는 `/vendor/bin/phpunit` 명령어로 실행할 수 있으며, 더 자세하고 깔끔한 테스트 결과를 원하면 `php artisan test` Artisan 명령어로도 실행할 수 있습니다.

<a name="the-vendor-directory"></a>
### `vendor` 디렉토리

`vendor` 디렉토리에는 [Composer](https://getcomposer.org) 의존성이 저장됩니다.

<a name="the-app-directory"></a>
## App 디렉토리

애플리케이션 대부분은 `app` 디렉토리에 위치합니다. 기본적으로 이 디렉토리는 `App` 네임스페이스가 적용되며, Composer에 의해 [PSR-4 자동 로딩 표준](https://www.php-fig.org/psr/psr-4/)을 사용해 자동 로드됩니다.

기본적으로 `app` 디렉토리 내에는 `Http`, `Models`, `Providers` 디렉토리가 있습니다. 하지만 시간이 지나면서 Artisan의 make 명령어를 사용해 클래스를 생성할 때 다양한 다른 디렉토리들이 `app` 내부에 생성됩니다. 예를 들어, `app/Console` 디렉토리는 `make:command` Artisan 명령어를 실행해 명령 클래스가 생성되기 전까지는 존재하지 않습니다.

`Console` 및 `Http` 디렉토리는 아래에서 각각 더 자세히 설명하지만, 두 디렉토리는 애플리케이션 핵심에 API 역할을 합니다. HTTP 프로토콜과 CLI는 모두 애플리케이션과 상호작용하는 방식이지만, 실제 애플리케이션 로직은 포함하지 않습니다. 즉, 애플리케이션에 명령을 전달하는 두 가지 방법입니다. `Console` 디렉토리에는 모든 Artisan 명령어가, `Http` 디렉토리에는 컨트롤러, 미들웨어, 요청 클래스가 있습니다.

> [!NOTE]
> `app` 디렉토리 내 많은 클래스들은 Artisan 명령어를 통해 생성할 수 있습니다. 사용 가능한 명령어를 확인하려면 터미널에서 `php artisan list make` 명령어를 실행하세요.

<a name="the-broadcasting-directory"></a>
### Broadcasting 디렉토리

`Broadcasting` 디렉토리에는 애플리케이션의 브로드캐스트 채널 클래스가 모두 포함됩니다. 이 클래스들은 `make:channel` 명령어로 생성됩니다. 기본 상태에서는 이 디렉토리가 없지만, 첫 번째 채널 생성 시 자동으로 만들어집니다. 채널에 대한 자세한 내용은 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
### Console 디렉토리

`Console` 디렉토리에는 애플리케이션에 맞춤화한 모든 Artisan 명령어가 포함됩니다. 이 명령어들은 `make:command` 명령어로 생성할 수 있습니다.

<a name="the-events-directory"></a>
### Events 디렉토리

기본적으로는 없지만, `event:generate` 또는 `make:event` Artisan 명령어를 실행하면 만들어집니다. `Events` 디렉토리에는 [이벤트 클래스](/docs/12.x/events)가 담깁니다. 이벤트는 애플리케이션 내 다른 부분에 특정 동작이 발생했음을 알리기 위해 사용되며, 큰 유연성과 느슨한 결합을 제공합니다.

<a name="the-exceptions-directory"></a>
### Exceptions 디렉토리

`Exceptions` 디렉토리에는 애플리케이션에서 사용하는 모든 커스텀 예외 클래스가 포함됩니다. 이 예외 클래스들은 `make:exception` 명령어로 생성할 수 있습니다.

<a name="the-http-directory"></a>
### Http 디렉토리

`Http` 디렉토리에는 컨트롤러, 미들웨어, 폼 요청이 포함됩니다. 애플리케이션에 들어오는 요청을 처리하는 거의 모든 로직이 이곳에 배치됩니다.

<a name="the-jobs-directory"></a>
### Jobs 디렉토리

기본적으로는 없지만, `make:job` Artisan 명령어를 실행하면 생성됩니다. `Jobs` 디렉토리에는 애플리케이션의 [큐 가능 작업](/docs/12.x/queues)이 저장됩니다. 작업은 애플리케이션에서 큐에 넣거나 현재 요청 라이프사이클 내에서 동기적으로 실행할 수 있습니다. 현재 요청 중 동기 실행되는 작업은 때때로 [커맨드 패턴](https://en.wikipedia.org/wiki/Command_pattern)을 구현한 "commands"라 부르기도 합니다.

<a name="the-listeners-directory"></a>
### Listeners 디렉토리

기본적으로는 없지만, `event:generate` 또는 `make:listener` Artisan 명령어로 생성됩니다. `Listeners` 디렉토리에는 [이벤트](/docs/12.x/events)를 처리하는 클래스가 포함됩니다. 이벤트 리스너는 이벤트 인스턴스를 받아 이벤트 발생에 대응하는 로직을 수행합니다. 예를 들어, `UserRegistered` 이벤트는 `SendWelcomeEmail` 리스너로 처리할 수 있습니다.

<a name="the-mail-directory"></a>
### Mail 디렉토리

기본적으로는 없지만, `make:mail` Artisan 명령어로 생성됩니다. `Mail` 디렉토리에는 애플리케이션에서 발송하는 [이메일을 나타내는 클래스](/docs/12.x/mail)가 포함됩니다. 메일 객체는 이메일을 만드는 모든 로직을 단일, 간단한 클래스로 캡슐화하며, `Mail::send` 메서드를 통해 메일을 보낼 수 있습니다.

<a name="the-models-directory"></a>
### Models 디렉토리

`Models` 디렉토리에는 모든 [Eloquent 모델 클래스](/docs/12.x/eloquent)가 포함됩니다. Laravel에 포함된 Eloquent ORM은 데이터베이스와 작업하기 위한 아름답고 간단한 ActiveRecord 구현체를 제공합니다. 각 데이터베이스 테이블은 해당 테이블과 상호작용할 모델 클래스와 연결됩니다. 모델을 통해 테이블 내 데이터를 조회하거나 새 레코드를 삽입할 수 있습니다.

<a name="the-notifications-directory"></a>
### Notifications 디렉토리

기본적으로는 없지만, `make:notification` Artisan 명령어로 생성됩니다. `Notifications` 디렉토리에는 애플리케이션에서 발송하는 "트랜잭션성" [알림](/docs/12.x/notifications)이 포함됩니다. 예를 들어 애플리케이션 내에서 발생하는 이벤트에 대한 간단한 알림이 이에 해당합니다. Laravel의 알림 기능은 이메일, Slack, SMS, 데이터베이스 저장 등 다양한 드라이버에 걸쳐 알림 발송을 추상화합니다.

<a name="the-policies-directory"></a>
### Policies 디렉토리

기본적으로는 없지만, `make:policy` Artisan 명령어로 생성됩니다. `Policies` 디렉토리에는 애플리케이션의 [인가 정책 클래스](/docs/12.x/authorization)가 포함됩니다. 정책은 사용자가 특정 리소스에 대해 주어진 작업을 수행할 수 있는지 결정할 때 사용됩니다.

<a name="the-providers-directory"></a>
### Providers 디렉토리

`Providers` 디렉토리에는 애플리케이션의 모든 [서비스 프로바이더](/docs/12.x/providers)가 포함됩니다. 서비스 프로바이더는 서비스 컨테이너에 서비스를 바인딩하거나 이벤트 등록, 애플리케이션이 요청을 처리할 준비를 마치기 위한 작업을 수행함으로써 애플리케이션을 부트스트랩합니다.

새로운 Laravel 애플리케이션에서는 기본적으로 `AppServiceProvider`가 포함되어 있습니다. 필요에 따라 이 디렉토리에 자신의 프로바이더를 추가할 수 있습니다.

<a name="the-rules-directory"></a>
### Rules 디렉토리

기본적으로는 없지만, `make:rule` Artisan 명령어로 생성됩니다. `Rules` 디렉토리에는 애플리케이션에서 사용하는 커스텀 유효성 검증 규칙 객체들이 포함됩니다. 규칙은 복잡한 검증 로직을 단순한 객체로 캡슐화하는 데 사용됩니다. 자세한 내용은 [유효성 검증 문서](/docs/12.x/validation)를 참고하세요.