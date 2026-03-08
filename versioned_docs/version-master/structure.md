# 디렉터리 구조 (Directory Structure)

- [소개](#introduction)
- [루트 디렉터리](#the-root-directory)
    - [`app` 디렉터리](#the-root-app-directory)
    - [`bootstrap` 디렉터리](#the-bootstrap-directory)
    - [`config` 디렉터리](#the-config-directory)
    - [`database` 디렉터리](#the-database-directory)
    - [`public` 디렉터리](#the-public-directory)
    - [`resources` 디렉터리](#the-resources-directory)
    - [`routes` 디렉터리](#the-routes-directory)
    - [`storage` 디렉터리](#the-storage-directory)
    - [`tests` 디렉터리](#the-tests-directory)
    - [`vendor` 디렉터리](#the-vendor-directory)
- [App 디렉터리](#the-app-directory)
    - [`Broadcasting` 디렉터리](#the-broadcasting-directory)
    - [`Console` 디렉터리](#the-console-directory)
    - [`Events` 디렉터리](#the-events-directory)
    - [`Exceptions` 디렉터리](#the-exceptions-directory)
    - [`Http` 디렉터리](#the-http-directory)
    - [`Jobs` 디렉터리](#the-jobs-directory)
    - [`Listeners` 디렉터리](#the-listeners-directory)
    - [`Mail` 디렉터리](#the-mail-directory)
    - [`Models` 디렉터리](#the-models-directory)
    - [`Notifications` 디렉터리](#the-notifications-directory)
    - [`Policies` 디렉터리](#the-policies-directory)
    - [`Providers` 디렉터리](#the-providers-directory)
    - [`Rules` 디렉터리](#the-rules-directory)

<a name="introduction"></a>
## 소개 (Introduction)

기본적으로 제공되는 Laravel 애플리케이션 구조는 소규모와 대규모 애플리케이션 모두에 최적의 출발점을 제공하도록 설계되었습니다. 하지만 자신의 필요에 맞게 애플리케이션 구조를 자유롭게 구성할 수 있습니다. Laravel은 특정 클래스가 반드시 어디에 위치해야 한다는 제약을 거의 두지 않습니다. 오직 Composer가 해당 클래스를 오토로드(autoload)할 수 있기만 하면 됩니다.

<a name="the-root-directory"></a>
## 루트 디렉터리 (The Root Directory)

<a name="the-root-app-directory"></a>
### `app` 디렉터리

`app` 디렉터리에는 애플리케이션의 핵심 코드가 위치합니다. 이 디렉터리는 뒤에서 더 자세히 설명하겠지만, 애플리케이션의 거의 모든 클래스는 이 디렉터리 안에 들어 있습니다.

<a name="the-bootstrap-directory"></a>
### `bootstrap` 디렉터리

`bootstrap` 디렉터리에는 프레임워크를 초기화(부트스트랩)하는 `app.php` 파일이 포함되어 있습니다. 또한, 이곳에는 라우트와 서비스 캐시 파일 등 프레임워크가 성능 향상을 위해 생성한 파일들을 담고 있는 `cache` 디렉터리도 존재합니다.

<a name="the-config-directory"></a>
### `config` 디렉터리

`config` 디렉터리는 이름에서 알 수 있듯이 애플리케이션의 모든 설정 파일을 담고 있습니다. 이 디렉터리의 모든 파일을 한 번씩 읽어보고 다양한 설정 옵션에 익숙해지는 것이 좋습니다.

<a name="the-database-directory"></a>
### `database` 디렉터리

`database` 디렉터리는 데이터베이스 마이그레이션, 모델 팩토리, 시드(seed) 파일을 포함하고 있습니다. 필요하다면 이 디렉터리에 SQLite 데이터베이스 파일을 저장할 수도 있습니다.

<a name="the-public-directory"></a>
### `public` 디렉터리

`public` 디렉터리에는 모든 요청이 들어올 때 진입점이 되는 `index.php` 파일이 있으며, 오토로딩 설정도 이곳에서 처리됩니다. 또한, 이미지, JavaScript, CSS 등 애플리케이션의 에셋 파일들이 이 디렉터리에 위치합니다.

<a name="the-resources-directory"></a>
### `resources` 디렉터리

`resources` 디렉터리에는 [뷰(views)](/docs/master/views)와 함께 CSS, JavaScript 등 컴파일되지 않은 원본 에셋들이 들어 있습니다.

<a name="the-routes-directory"></a>
### `routes` 디렉터리

`routes` 디렉터리에는 애플리케이션의 모든 라우트 정의가 포함되어 있습니다. 기본적으로 Laravel에는 `web.php`와 `console.php` 두 개의 라우트 파일이 제공됩니다.

`web.php` 파일에는 Laravel이 `web` 미들웨어 그룹에 포함시키는 라우트들이 정의되어 있습니다. 이 그룹에는 세션 상태, CSRF 보호, 쿠키 암호화가 포함됩니다. 애플리케이션이 무상태(stateless) RESTful API를 제공하지 않는다면, 대부분의 라우트는 `web.php`에 정의하게 됩니다.

`console.php` 파일에서는 모든 클로저(Closure) 기반 콘솔 명령어를 정의할 수 있습니다. 각 클로저는 명령어 인스턴스에 바인딩되어, 명령어의 IO 메서드에 쉽게 접근할 수 있습니다. 이 파일은 HTTP 라우트를 정의하지는 않지만, 콘솔 진입점(라우트)을 애플리케이션에 제공합니다. 또한, `console.php` 파일에서 [스케줄링](https://laravel.com/docs/master/scheduling)도 할 수 있습니다.

선택적으로, `install:api`와 `install:broadcasting` Artisan 명령어를 사용해 API 라우트(`api.php`) 및 브로드캐스팅 채널(`channels.php`)용 추가 라우트 파일을 생성할 수 있습니다.

`api.php` 파일에는 무상태(stateless)로 동작하는 라우트들을 정의합니다. 이 라우트를 통한 요청은 주로 [토큰을 이용한 인증](/docs/master/sanctum)을 거치며, 세션 상태에 접근할 수 없습니다.

`channels.php` 파일은 애플리케이션이 지원하는 [이벤트 브로드캐스팅](/docs/master/broadcasting) 채널을 등록하는 곳입니다.

<a name="the-storage-directory"></a>
### `storage` 디렉터리

`storage` 디렉터리에는 로그(log), 컴파일된 Blade 템플릿, 파일 기반 세션, 파일 캐시, 프레임워크가 생성하는 기타 여러 파일이 담깁니다. 이 디렉터리는 각 역할에 따라 `app`, `framework`, `logs` 하위 디렉터리로 나뉩니다. `app` 디렉터리에는 애플리케이션이 생성하는 파일을 저장할 수 있습니다. `framework` 디렉터리에는 프레임워크가 생성한 파일과 캐시가 저장됩니다. 마지막으로 `logs` 디렉터리에는 애플리케이션 로그 파일이 있습니다.

`storage/app/public` 디렉터리는 사용자 아바타와 같이 공개적으로 접근 가능한 사용자 생성 파일을 저장하는 용도로 사용할 수 있습니다. 이 디렉터리를 가리키는 심볼릭 링크를 `public/storage`에 생성해야 하며, `php artisan storage:link` Artisan 명령어로 링크를 만들 수 있습니다.

<a name="the-tests-directory"></a>
### `tests` 디렉터리

`tests` 디렉터리에는 자동화된 테스트 코드들이 위치합니다. 기본적으로 [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de/) 기반의 단위 테스트 및 기능 테스트 예제가 제공됩니다. 각 테스트 클래스 이름은 반드시 `Test`로 끝나야 합니다. 테스트는 `/vendor/bin/pest` 또는 `/vendor/bin/phpunit` 명령어로 실행할 수 있습니다. 테스트 결과를 보다 보기 좋게 출력하고자 한다면 `php artisan test` Artisan 명령어를 사용할 수도 있습니다.

<a name="the-vendor-directory"></a>
### `vendor` 디렉터리

`vendor` 디렉터리에는 [Composer](https://getcomposer.org)로 설치한 모든 의존성 패키지가 위치합니다.

<a name="the-app-directory"></a>
## App 디렉터리 (The App Directory)

애플리케이션의 대부분은 `app` 디렉터리에 위치하게 됩니다. 기본적으로 이 디렉터리는 `App` 네임스페이스를 가지며, [PSR-4 오토로딩 표준](https://www.php-fig.org/psr/psr-4/)에 따라 Composer가 오토로드합니다.

기본적으로 `app` 디렉터리에는 `Http`, `Models`, `Providers` 하위 디렉터리가 존재합니다. 하지만 Artisan의 make 명령어로 클래스를 생성할 때마다 다양한 하위 디렉터리가 점진적으로 추가됩니다. 예를 들어, `app/Console` 디렉터리는 `make:command` Artisan 명령어로 명령어 클래스를 생성하기 전까지는 존재하지 않습니다.

`Console`과 `Http` 디렉터리에 대해서는 아래에서 각각 더 자세히 설명하지만, 이 두 디렉터리는 애플리케이션의 핵심에 접근할 수 있는 API 역할을 한다고 생각하면 됩니다. HTTP 프로토콜(웹 요청)과 CLI(명령줄 인터페이스)는 모두 애플리케이션과 소통하는 방법일 뿐, 실제 비즈니스 로직을 담고 있지는 않습니다. 즉, 두 방식 모두 애플리케이션에 명령을 내리는 통로입니다. `Console` 디렉터리는 모든 Artisan 명령어를, `Http` 디렉터리는 컨트롤러, 미들웨어, 요청 클래스를 담고 있습니다.

> [!NOTE]
> `app` 디렉터리의 많은 클래스들은 Artisan 명령어로 손쉽게 생성할 수 있습니다. 터미널에서 `php artisan list make` 명령어를 실행하면 생성 가능한 명령어 목록을 확인할 수 있습니다.

<a name="the-broadcasting-directory"></a>
### Broadcasting 디렉터리

`Broadcasting` 디렉터리에는 애플리케이션의 브로드캐스트 채널 클래스들이 위치합니다. 이 클래스들은 `make:channel` 명령어로 생성할 수 있습니다. 기본적으로 존재하지 않지만, 첫 채널을 만들 때 자동으로 생성됩니다. 추가적인 내용은 [이벤트 브로드캐스팅](/docs/master/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
### Console 디렉터리

`Console` 디렉터리에는 애플리케이션의 커스텀 Artisan 명령어들이 담겨 있습니다. 이 명령어들은 `make:command` 명령어로 생성할 수 있습니다.

<a name="the-events-directory"></a>
### Events 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 또는 `make:event` Artisan 명령어를 실행하면 자동으로 생성됩니다. `Events` 디렉터리에는 [이벤트 클래스](/docs/master/events)가 들어갑니다. 이벤트는 특정 동작이 발생했음을 애플리케이션의 다른 부분에 알리는 데 사용되며, 높은 유연성과 결합도 감소에 도움이 됩니다.

<a name="the-exceptions-directory"></a>
### Exceptions 디렉터리

`Exceptions` 디렉터리에는 애플리케이션의 커스텀 예외 클래스들이 포함됩니다. 이러한 예외 클래스들은 `make:exception` 명령어로 생성할 수 있습니다.

<a name="the-http-directory"></a>
### Http 디렉터리

`Http` 디렉터리에는 컨트롤러, 미들웨어, 폼 요청이 포함되어 있습니다. 즉, 애플리케이션으로 들어오는 요청을 처리(로직 수행)하기 위한 대부분의 코드가 이 디렉터리에 작성됩니다.

<a name="the-jobs-directory"></a>
### Jobs 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:job` Artisan 명령어를 실행하면 생성됩니다. `Jobs` 디렉터리에는 애플리케이션이 사용하는 [큐잉 가능한 작업 클래스](/docs/master/queues)가 들어갑니다. 작업(Job)은 애플리케이션에서 큐에 추가하거나 현재 요청 생명주기 내에서 동기적으로 실행할 수 있습니다. 동기적으로 실행되는 작업을 "커맨드(command)"라고 부르기도 하는데, [커맨드 패턴](https://en.wikipedia.org/wiki/Command_pattern)을 구현한 것이기 때문입니다.

<a name="the-listeners-directory"></a>
### Listeners 디렉터리

이 디렉터리 역시 기본적으로 존재하지 않지만, `event:generate` 또는 `make:listener` Artisan 명령어를 실행하면 자동 생성됩니다. `Listeners` 디렉터리에는 [이벤트](/docs/master/events)를 처리하는 리스너 클래스들이 위치합니다. 이벤트 리스너는 이벤트 인스턴스를 받아 이벤트 발생 시 실행할 로직을 처리합니다. 예를 들어, `UserRegistered` 이벤트를 `SendWelcomeEmail` 리스너가 처리할 수 있습니다.

<a name="the-mail-directory"></a>
### Mail 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:mail` Artisan 명령어로 생성할 수 있습니다. `Mail` 디렉터리에는 애플리케이션이 발송하는 [이메일 관련 클래스](/docs/master/mail)가 포함됩니다. 메일 객체는 이메일 생성 로직을 하나의 클래스에 담아 관리하며, `Mail::send` 메서드를 사용해 보낼 수 있습니다.

<a name="the-models-directory"></a>
### Models 디렉터리

`Models` 디렉터리에는 [Eloquent 모델 클래스](/docs/master/eloquent)가 들어 있습니다. Laravel에 포함된 Eloquent ORM은 데이터베이스 작업을 위한 간단하면서도 강력한 액티브 레코드(ActiveRecord) 구현을 제공합니다. 데이터베이스의 각각의 테이블에는 연관된 "모델" 클래스가 존재하며, 이 모델을 통해 데이터 조회, 레코드 추가 등 다양한 DB 작업을 할 수 있습니다.

<a name="the-notifications-directory"></a>
### Notifications 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:notification` Artisan 명령어로 생성할 수 있습니다. `Notifications` 디렉터리에는 애플리케이션이 전송하는 "트랜잭션성" [알림 클래스](/docs/master/notifications)가 저장됩니다. 이 알림 기능은 이메일, Slack, SMS, 데이터베이스 등에 다양한 드라이버를 통해 알림을 보낼 수 있도록 추상화되어 있습니다.

<a name="the-policies-directory"></a>
### Policies 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:policy` Artisan 명령어로 생성 가능합니다. `Policies` 디렉터리에는 애플리케이션의 [인가(authorization) 정책 클래스](/docs/master/authorization)가 위치합니다. Policy는 특정 리소스에 대해 사용자가 작업을 수행할 수 있는지를 판단하는 역할을 합니다.

<a name="the-providers-directory"></a>
### Providers 디렉터리

`Providers` 디렉터리에는 애플리케이션의 [서비스 프로바이더](/docs/master/providers)가 모두 저장됩니다. 서비스 프로바이더는 서비스 컨테이너에 서비스 바인딩, 이벤트 등록, 기타 애플리케이션 초기화 작업 등, 요청 처리 전 다양한 부트스트랩 동작을 수행합니다.

새로운 Laravel 애플리케이션에는 기본적으로 `AppServiceProvider`가 포함되어 있습니다. 필요에 따라 이 디렉터리에 원하는 서비스를 자유롭게 추가할 수 있습니다.

<a name="the-rules-directory"></a>
### Rules 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:rule` Artisan 명령어로 생성할 수 있습니다. `Rules` 디렉터리에는 애플리케이션의 커스텀 유효성 검증 규칙 객체가 포함됩니다. Rule 객체를 활용하면 복잡한 유효성 검증 로직을 간단한 객체로 캡슐화할 수 있습니다. 더 깊은 내용은 [유효성 검증 문서](/docs/master/validation)를 참고하세요.