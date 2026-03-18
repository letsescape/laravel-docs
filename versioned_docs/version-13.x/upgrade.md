# 업그레이드 가이드 (Upgrade Guide)

- [12.x에서 13.0으로 업그레이드하기](#upgrade-13.0)
    - [AI를 사용한 업그레이드](#upgrading-using-ai)

<a name="high-impact-changes"></a>
## 주요 변경 사항 (High Impact Changes)

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [Laravel 인스톨러 업데이트](#updating-the-laravel-installer)
- [요청 위조 방지](#request-forgery-protection)

</div>

<a name="medium-impact-changes"></a>
## 중간 영향도 변경 사항 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [캐시 `serializable_classes` 구성](#cache-serializable_classes-configuration)

</div>

<a name="low-impact-changes"></a>
## 낮은 영향도 변경 사항 (Low Impact Changes)

<div class="content-list" markdown="1">

- [캐시 접두사와 세션 쿠키 이름](#cache-prefixes-and-session-cookie-names)
- [컬렉션 모델 직렬화 시 eager-loaded 연관관계 복원](#collection-model-serialization-restores-eager-loaded-relations)
- [`Container::call`과 nullable 클래스 기본값](#containercall-and-nullable-class-defaults)
- [도메인 라우트 등록 우선순위](#domain-route-registration-precedence)
- [`JobAttempted` 이벤트 예외 페이로드](#jobattempted-event-exception-payload)
- [Manager `extend` 콜백 바인딩](#manager-extend-callback-binding)
- [MySQL `DELETE` 쿼리에서 `JOIN`, `ORDER BY`, `LIMIT`](#mysql-delete-queries-with-join-order-by-and-limit)
- [페이지네이션 Bootstrap 뷰 이름](#pagination-bootstrap-view-names)
- [다형성 Pivot 테이블 이름 생성](#polymorphic-pivot-table-name-generation)
- [`QueueBusy` 이벤트 속성 이름 변경](#queuebusy-event-property-rename)
- [테스트 간 `Str` 팩토리 초기화](#str-factories-reset-between-tests)

</div>

<a name="upgrade-13.0"></a>
## 12.x에서 13.0으로 업그레이드하기 (Upgrading To 13.0 From 12.x)

#### 예상 업그레이드 소요 시간: 10분

> [!NOTE]
> 가능한 모든 브레이킹 체인지를 문서화하려고 노력했습니다. 다만 이 중 일부는 프레임워크의 비교적 드문 영역에만 해당하므로 실제로는 일부만 여러분의 애플리케이션에 영향을 줄 수 있습니다. 시간을 절약하고 싶다면 [Shift](https://laravelshift.com)를 사용할 수 있습니다. Shift는 Laravel 업그레이드를 자동화해 주는 커뮤니티 유지보수 서비스입니다.

<a name="upgrading-using-ai"></a>
### AI를 사용한 업그레이드

[Laravel Boost](https://github.com/laravel/boost)를 사용하면 업그레이드를 자동화할 수 있습니다. Boost는 AI 도우미에 업그레이드용 가이드 프롬프트를 제공하는 1차 제공 MCP 서버입니다. Laravel 12 애플리케이션에 설치한 뒤 Claude Code, Cursor, OpenCode, Gemini, VS Code에서 `/upgrade-laravel-13` 슬래시 명령어를 실행하면 Laravel 13 업그레이드를 시작할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트

**영향 가능성: 높음**

애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다:

<div class="content-list" markdown="1">

- `laravel/framework`를 `^13.0`으로
- `laravel/tinker`를 `^3.0`으로
- `phpunit/phpunit`을 `^12.0`으로
- `pestphp/pest`를 `^4.0`으로

</div>

<a name="updating-the-laravel-installer"></a>
### Laravel 인스톨러 업데이트

Laravel 인스톨러 CLI 도구를 사용해 새로운 Laravel 애플리케이션을 생성하고 있다면, Laravel 13.x와 호환되도록 인스톨러를 업데이트해야 합니다.

`composer global require`를 통해 Laravel 인스톨러를 설치했다면, `composer global update`로 업데이트할 수 있습니다:

```shell
composer global update laravel/installer
```

또는 [Laravel Herd](https://herd.laravel.com)에 포함된 Laravel 인스톨러를 사용 중이라면, Herd를 최신 릴리즈로 업데이트해야 합니다.

<a name="cache"></a>
### 캐시

<a name="cache-prefixes-and-session-cookie-names"></a>
#### 캐시 접두사와 세션 쿠키 이름

**영향 가능성: 낮음**

Laravel의 기본 캐시 및 Redis 키 접두사는 이제 하이픈(`-`)이 포함된 접미사를 사용합니다. 또한 기본 세션 쿠키 이름은 이제 애플리케이션 이름에 `Str::snake(...)`를 사용합니다.

대부분의 애플리케이션에서는 이미 애플리케이션 수준 설정 파일에서 해당 값을 정의하고 있으므로 이 변경의 영향을 받지 않습니다. 이 변경은 주로 애플리케이션 설정값이 없을 때 프레임워크 수준의 기본값에 의존하는 애플리케이션에만 영향을 줍니다.

애플리케이션이 이러한 생성된 기본값에 의존하고 있다면, 업그레이드 후 캐시 키와 세션 쿠키 이름이 바뀔 수 있습니다:

```php
// Laravel <= 12.x
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_cache_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_database_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_session';

// Laravel >= 13.x
Str::slug((string) env('APP_NAME', 'laravel')).'-cache-';
Str::slug((string) env('APP_NAME', 'laravel')).'-database-';
Str::snake((string) env('APP_NAME', 'laravel')).'_session';
```

이전 동작을 유지하고 싶다면 환경 변수에서 `CACHE_PREFIX`, `REDIS_PREFIX`, `SESSION_COOKIE`를 명시적으로 설정하세요.

<a name="store-and-repository-contracts-touch"></a>
#### `Store` 및 `Repository` 컨트랙트: `touch`

**영향 가능성: 매우 낮음**

캐시 컨트랙트에는 이제 항목 TTL을 연장하기 위한 `touch` 메서드가 포함됩니다. 커스텀 캐시 저장소 구현을 유지보수 중이라면 이 메서드를 추가해야 합니다:

```php
// Illuminate\Contracts\Cache\Store
public function touch($key, $seconds);
```

<a name="cache-serializable_classes-configuration"></a>
#### 캐시 `serializable_classes` 구성

**영향 가능성: 중간**

기본 애플리케이션 `cache` 구성에는 이제 `false`로 설정된 `serializable_classes` 옵션이 포함됩니다. 이는 애플리케이션의 `APP_KEY`가 유출되었을 때 PHP 역직렬화 gadget chain 공격을 완화하기 위해 캐시 역직렬화 동작을 더 엄격하게 만듭니다. 애플리케이션이 의도적으로 PHP 객체를 캐시에 저장하고 있다면, 역직렬화가 허용되어야 하는 클래스를 명시적으로 나열해야 합니다:

```php
'serializable_classes' => [
    App\Data\CachedDashboardStats::class,
    App\Support\CachedPricingSnapshot::class,
],
```

기존에 임의의 캐시 객체 역직렬화에 의존하고 있었다면, 해당 사용 방식을 명시적인 클래스 허용 목록 또는 배열 같은 비객체 캐시 페이로드로 옮겨야 합니다.

<a name="container"></a>
### 컨테이너

<a name="containercall-and-nullable-class-defaults"></a>
#### `Container::call`과 nullable 클래스 기본값

**영향 가능성: 낮음**

`Container::call`은 이제 바인딩이 존재하지 않을 때 nullable 클래스 파라미터의 기본값을 존중합니다. 이는 Laravel 12에서 도입된 생성자 주입 동작과 동일합니다:

```php
$container->call(function (?Carbon $date = null) {
    return $date;
});

// Laravel <= 12.x: Carbon instance
// Laravel >= 13.x: null
```

메서드 호출 주입 로직이 이전 동작에 의존하고 있었다면 해당 로직을 조정해야 할 수 있습니다.

<a name="contracts"></a>
### 컨트랙트

<a name="dispatcher-contract-dispatchafterresponse"></a>
#### `Dispatcher` 컨트랙트: `dispatchAfterResponse`

**영향 가능성: 매우 낮음**

`Illuminate\Contracts\Bus\Dispatcher` 컨트랙트에는 이제 `dispatchAfterResponse($command, $handler = null)` 메서드가 포함됩니다.

커스텀 dispatcher 구현을 유지보수 중이라면 이 메서드를 클래스에 추가해야 합니다.

<a name="responsefactory-contract-eventstream"></a>
#### `ResponseFactory` 컨트랙트: `eventStream`

**영향 가능성: 매우 낮음**

`Illuminate\Contracts\Routing\ResponseFactory` 컨트랙트에는 이제 `eventStream` 시그니처가 포함됩니다.

이 컨트랙트의 커스텀 구현을 유지보수 중이라면 해당 메서드를 추가해야 합니다.

<a name="mustverifyemail-contract-markemailasunverified"></a>
#### `MustVerifyEmail` 컨트랙트: `markEmailAsUnverified`

**영향 가능성: 매우 낮음**

`Illuminate\Contracts\Auth\MustVerifyEmail` 컨트랙트에는 이제 `markEmailAsUnverified()`가 포함됩니다.

이 컨트랙트의 커스텀 구현을 제공하고 있다면 호환성을 유지하기 위해 이 메서드를 추가해야 합니다.

<a name="database"></a>
### 데이터베이스

<a name="mysql-delete-queries-with-join-order-by-and-limit"></a>
#### MySQL `DELETE` 쿼리에서 `JOIN`, `ORDER BY`, `LIMIT`

**영향 가능성: 낮음**

Laravel은 이제 MySQL grammar에서 `ORDER BY`와 `LIMIT`를 포함한 전체 `DELETE ... JOIN` 쿼리를 컴파일합니다.

이전 버전에서는 조인된 삭제 쿼리에서 `ORDER BY` / `LIMIT` 절이 조용히 무시될 수 있었습니다. Laravel 13에서는 이 절들이 생성된 SQL에 포함됩니다. 그 결과, 이 문법을 지원하지 않는 데이터베이스 엔진(예: 일반적인 MySQL / MariaDB 변형)에서는 범위 제한 없는 삭제를 실행하는 대신 `QueryException`이 발생할 수 있습니다.

<a name="eloquent"></a>
### Eloquent

<a name="model-booting-and-nested-instantiation"></a>
#### 모델 부팅과 중첩 인스턴스 생성

**영향 가능성: 매우 낮음**

모델이 아직 부팅 중일 때 동일한 모델의 새 인스턴스를 만드는 것은 이제 허용되지 않으며 `LogicException`이 발생합니다.

이 변경은 모델의 `boot` 메서드 또는 트레이트의 `boot*` 메서드 내부에서 모델 인스턴스를 생성하는 코드에 영향을 줍니다:

```php
protected static function boot()
{
    parent::boot();

    // No longer allowed during booting...
    (new static())->getTable();
}
```

중첩 부팅을 피하려면 이 로직을 부팅 사이클 바깥으로 옮기세요.

<a name="polymorphic-pivot-table-name-generation"></a>
#### 다형성 Pivot 테이블 이름 생성

**영향 가능성: 낮음**

커스텀 pivot 모델 클래스를 사용하는 다형성 pivot 모델에 대해 테이블 이름을 추론할 때, Laravel은 이제 복수형 이름을 생성합니다.

애플리케이션이 기존의 단수형 추론 이름에 의존하고 있었고 커스텀 pivot 클래스를 사용하고 있다면, pivot 모델에 테이블 이름을 명시적으로 정의해야 합니다.

<a name="collection-model-serialization-restores-eager-loaded-relations"></a>
#### 컬렉션 모델 직렬화 시 eager-loaded 연관관계 복원

**영향 가능성: 낮음**

Eloquent 모델 컬렉션이 직렬화된 뒤 다시 복원될 때, 예를 들어 큐 작업에서, 이제 컬렉션 모델의 eager-loaded 연관관계도 함께 복원됩니다.

역직렬화 후 연관관계가 존재하지 않는다는 전제에 의존하던 코드가 있다면 해당 로직을 조정해야 할 수 있습니다.

<a name="http-client"></a>
### HTTP 클라이언트

<a name="http-client-response-throw-and-throwif-signatures"></a>
#### HTTP 클라이언트 `Response::throw` 및 `throwIf` 시그니처

**영향 가능성: 매우 낮음**

HTTP 클라이언트 응답 메서드는 이제 메서드 시그니처에서 콜백 파라미터를 선언합니다:

```php
public function throw($callback = null);
public function throwIf($condition, $callback = null);
```

커스텀 응답 클래스에서 이 메서드들을 오버라이드하고 있다면 시그니처가 호환되는지 확인해야 합니다.

<a name="notifications"></a>
### 알림

<a name="default-password-reset-subject"></a>
#### 기본 비밀번호 재설정 제목

**영향 가능성: 매우 낮음**

Laravel의 기본 비밀번호 재설정 메일 제목이 변경되었습니다:

```text
// Laravel <= 12.x
Reset Password Notification

// Laravel >= 13.x
Reset your password
```

테스트, 어설션, 번역 오버라이드가 이전 기본 문자열에 의존하고 있다면 해당 내용을 업데이트해야 합니다.

<a name="queued-notifications-and-missing-models"></a>
#### 큐 알림과 누락된 모델

**영향 가능성: 매우 낮음**

큐 알림은 이제 알림 클래스에 정의된 `#[DeleteWhenMissingModels]` 속성과 `$deleteWhenMissingModels` 속성을 존중합니다.

이전 버전에서는 모델이 누락된 경우 알림 작업이 삭제되기를 기대했더라도, 큐 알림 작업이 계속 실패할 수 있었습니다.

<a name="queue"></a>
### 큐

<a name="jobattempted-event-exception-payload"></a>
#### `JobAttempted` 이벤트 예외 페이로드

**영향 가능성: 낮음**

`Illuminate\Queue\Events\JobAttempted` 이벤트는 이제 이전의 boolean 속성 `$exceptionOccurred` 대신, 예외 객체 또는 `null`을 `$exception`을 통해 노출합니다:

```php
// Laravel <= 12.x
$event->exceptionOccurred;

// Laravel >= 13.x
$event->exception;
```

이 이벤트를 수신하고 있다면 리스너 코드를 이에 맞게 업데이트해야 합니다.

<a name="queuebusy-event-property-rename"></a>
#### `QueueBusy` 이벤트 속성 이름 변경

**영향 가능성: 낮음**

`Illuminate\Queue\Events\QueueBusy` 이벤트의 속성 `$connection`은 다른 큐 이벤트와의 일관성을 위해 `$connectionName`으로 이름이 변경되었습니다.

리스너에서 `$connection`을 참조하고 있다면 `$connectionName`으로 업데이트하세요.

<a name="queue-contract-method-additions"></a>
#### `Queue` 컨트랙트 메서드 추가

**영향 가능성: 매우 낮음**

`Illuminate\Contracts\Queue\Queue` 컨트랙트에는 이전에 docblock에만 선언되어 있던 큐 크기 검사 메서드가 이제 실제로 포함됩니다.

이 컨트랙트의 커스텀 큐 드라이버 구현을 유지보수 중이라면 다음 메서드를 구현해야 합니다:

<div class="content-list" markdown="1">

- `pendingSize`
- `delayedSize`
- `reservedSize`
- `creationTimeOfOldestPendingJob`

</div>

<a name="routing"></a>
### 라우팅

<a name="domain-route-registration-precedence"></a>
#### 도메인 라우트 등록 우선순위

**영향 가능성: 낮음**

명시적인 도메인을 가진 라우트는 이제 라우트 매칭 시 도메인이 없는 라우트보다 우선됩니다.

이로 인해 도메인이 없는 라우트가 먼저 등록되어 있더라도 catch-all 서브도메인 라우트가 더 일관되게 동작합니다. 애플리케이션이 도메인 라우트와 비도메인 라우트 간의 기존 등록 우선순위에 의존하고 있었다면 라우트 매칭 동작을 점검해야 합니다.

<a name="scheduling"></a>
### 스케줄링

<a name="withscheduling-registration-timing"></a>
#### `withScheduling` 등록 시점

**영향 가능성: 매우 낮음**

`ApplicationBuilder::withScheduling()`을 통해 등록된 스케줄은 이제 `Schedule`이 해석될 때까지 지연됩니다.

애플리케이션이 부트스트랩 중 즉시 스케줄이 등록되는 시점에 의존하고 있었다면 해당 로직을 조정해야 할 수 있습니다.

<a name="security"></a>
### 보안

<a name="request-forgery-protection"></a>
#### 요청 위조 방지

**영향 가능성: 높음**

Laravel의 CSRF 미들웨어 이름이 `VerifyCsrfToken`에서 `PreventRequestForgery`로 변경되었고, 이제 `Sec-Fetch-Site` 헤더를 사용한 요청 origin 검증을 포함합니다.

`VerifyCsrfToken`과 `ValidateCsrfToken`은 여전히 deprecated 별칭으로 남아 있지만, 테스트나 라우트 정의에서 미들웨어를 제외하는 경우처럼 직접 참조하고 있다면 `PreventRequestForgery`로 업데이트해야 합니다:

```php
use Illuminate\Foundation\Http\Middleware\PreventRequestForgery;
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;

// Laravel <= 12.x
->withoutMiddleware([VerifyCsrfToken::class]);

// Laravel >= 13.x
->withoutMiddleware([PreventRequestForgery::class]);
```

이제 미들웨어 구성 API도 `preventRequestForgery(...)`를 제공합니다.

<a name="support"></a>
### 지원

<a name="manager-extend-callback-binding"></a>
#### Manager `extend` 콜백 바인딩

**영향 가능성: 낮음**

Manager의 `extend` 메서드를 통해 등록된 커스텀 드라이버 클로저는 이제 manager 인스턴스에 바인딩됩니다.

이전까지는 이 콜백 내부에서 `$this`가 서비스 프로바이더 인스턴스 같은 다른 바인딩 객체라고 가정하고 있었다면, 해당 값은 `use (...)`를 사용한 클로저 캡처로 옮겨야 합니다.

<a name="str-factories-reset-between-tests"></a>
#### 테스트 간 `Str` 팩토리 초기화

**영향 가능성: 낮음**

Laravel은 이제 테스트 teardown 중 커스텀 `Str` 팩토리를 초기화합니다.

테스트 메서드 사이에서 커스텀 UUID / ULID / 랜덤 문자열 팩토리가 유지된다고 가정하고 있었다면, 관련 테스트 또는 setup 훅에서 매번 다시 설정해야 합니다.

<a name="jsfrom-uses-unescaped-unicode-by-default"></a>
#### `Js::from`의 기본 unescaped Unicode 사용

**영향 가능성: 매우 낮음**

`Illuminate\Support\Js::from`은 이제 기본적으로 `JSON_UNESCAPED_UNICODE`를 사용합니다.

테스트나 프론트엔드 출력 비교가 이스케이프된 Unicode 시퀀스, 예를 들어 `\u00e8`에 의존하고 있었다면 기대값을 업데이트해야 합니다.

<a name="views"></a>
### 뷰

<a name="pagination-bootstrap-view-names"></a>
#### 페이지네이션 Bootstrap 뷰 이름

**영향 가능성: 낮음**

Bootstrap 3 기본값에 대한 내부 페이지네이션 뷰 이름이 이제 더 명시적으로 바뀌었습니다:

```nothing
// Laravel <= 12.x
pagination::default
pagination::simple-default

// Laravel >= 13.x
pagination::bootstrap-3
pagination::simple-bootstrap-3
```

애플리케이션이 기존 페이지네이션 뷰 이름을 직접 참조하고 있다면 그 참조를 업데이트해야 합니다.

<a name="miscellaneous"></a>
### 기타 참고

또한 `laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경 사항도 함께 확인해 보시길 권장합니다. 이 중 상당수는 필수는 아니지만, 애플리케이션 파일과 동기화해 두는 편이 좋을 수 있습니다. 이 업그레이드 가이드에서 일부 변경은 다루지만, 설정 파일이나 주석 변경처럼 다루지 않는 내용도 있습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/12.x...13.x)를 사용하면 변경 사항을 쉽게 확인하고, 여러분에게 중요한 업데이트만 선택해 반영할 수 있습니다.
