# Laravel Pulse (Laravel Pulse)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
- [대시보드](#dashboard)
    - [인가](#dashboard-authorization)
    - [커스터마이즈](#dashboard-customization)
    - [사용자 정보 해석](#dashboard-resolving-users)
    - [카드](#dashboard-cards)
- [엔트리 캡처](#capturing-entries)
    - [레코더](#recorders)
    - [필터링](#filtering)
- [성능](#performance)
    - [다른 데이터베이스 사용](#using-a-different-database)
    - [Redis 인제스트](#ingest)
    - [샘플링](#sampling)
    - [트리밍](#trimming)
    - [Pulse 예외 처리](#pulse-exceptions)
- [사용자 정의 카드](#custom-cards)
    - [카드 컴포넌트](#custom-card-components)
    - [스타일링](#custom-card-styling)
    - [데이터 캡처 및 집계](#custom-card-data)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능과 사용 현황에 대한 인사이트를 한눈에 제공합니다. Pulse를 이용하면 느린 작업(job) 및 엔드포인트, 가장 활발한 사용자 등을 추적하여 병목 현상을 파악할 수 있습니다.

개별 이벤트의 심층 디버깅이 필요하다면 [Laravel Telescope](/docs/master/telescope) 문서를 참고하십시오.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Pulse의 기본 스토리지 구현체는 현재 MySQL, MariaDB, PostgreSQL 데이터베이스만을 지원합니다. 다른 데이터베이스 엔진을 사용 중인 경우, Pulse 데이터를 위해 별도의 MySQL, MariaDB, PostgreSQL 데이터베이스를 추가로 준비해야 합니다.

Composer 패키지 매니저를 사용하여 Pulse를 설치할 수 있습니다:

```shell
composer require laravel/pulse
```

다음으로, `vendor:publish` Artisan 명령어를 이용해 Pulse의 설정 및 마이그레이션 파일을 퍼블리시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

마지막으로, Pulse 데이터 저장에 필요한 테이블을 생성하려면 `migrate` 명령어를 실행하십시오:

```shell
php artisan migrate
```

Pulse의 데이터베이스 마이그레이션이 완료되면 `/pulse` 경로를 통해 Pulse 대시보드에 접근할 수 있습니다.

> [!NOTE]
> Pulse 데이터를 애플리케이션의 기본 데이터베이스가 아니라 별도의 데이터베이스에 저장하고 싶다면, [전용 데이터베이스 연결 지정 방법](#using-a-different-database)을 참고하십시오.

<a name="configuration"></a>
### 설정 (Configuration)

Pulse의 여러 설정 옵션은 환경 변수로 조정할 수 있습니다. 사용 가능한 옵션 확인, 새로운 레코더 등록, 고급 옵션 설정 등을 위해 `config/pulse.php` 구성 파일을 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## 대시보드 (Dashboard)

<a name="dashboard-authorization"></a>
### 인가 (Authorization)

Pulse 대시보드는 `/pulse` 경로를 통해 접근할 수 있습니다. 기본적으로 `local` 환경에서만 대시보드에 접근할 수 있으므로, 운영 환경에서는 `'viewPulse'` 인가 게이트를 커스터마이즈하여 권한을 설정해야 합니다. 아래와 같이 애플리케이션의 `app/Providers/AppServiceProvider.php` 파일에서 설정할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('viewPulse', function (User $user) {
        return $user->isAdmin();
    });

    // ...
}
```

<a name="dashboard-customization"></a>
### 커스터마이즈 (Customization)

Pulse 대시보드의 카드 및 레이아웃은 대시보드 뷰 파일을 퍼블리시하여 커스터마이즈할 수 있습니다. 해당 뷰는 `resources/views/vendor/pulse/dashboard.blade.php` 경로에 생성됩니다:

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

대시보드는 [Livewire](https://livewire.laravel.com/) 기반으로 동작하며, JavaScript 에셋을 다시 빌드하지 않아도 카드 및 레이아웃을 자유롭게 수정할 수 있습니다.

이 뷰 파일 내에서는 `<x-pulse>` 컴포넌트가 대시보드 렌더링을 담당하며, 카드들이 그리드 레이아웃으로 배치됩니다. 대시보드를 화면 전체 너비로 확장하려면 `full-width` 속성을 사용할 수 있습니다:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

기본적으로 `<x-pulse>` 컴포넌트는 12칸 그리드를 생성하지만, `cols` 속성으로 커스텀 칼럼 수를 지정할 수 있습니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

각 카드는 `cols` 및 `rows` 속성을 받아 공간과 위치를 조정할 수 있습니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

대부분의 카드에서는 `expand` 속성을 부여하여 스크롤 대신 카드 전체를 확장 표시할 수 있습니다:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### 사용자 정보 해석 (Resolving Users)

사용자 정보를 표시하는 카드(예: Application Usage 카드)의 경우, Pulse는 사용자 ID만을 기록합니다. 대시보드 렌더링 시 기본 `Authenticatable` 모델에서 `name`과 `email` 필드를 조회하고, 아바타는 Gravatar 웹 서비스를 사용해 표시합니다.

필드 및 아바타 표시 방식은 애플리케이션의 `App\Providers\AppServiceProvider`에서 `Pulse::user` 메서드를 호출해 커스터마이즈할 수 있습니다.

`user` 메서드는 표시할 `Authenticatable` 모델을 인수로 받아, `name`, `extra`, `avatar` 정보를 포함한 배열을 반환해야 합니다:

```php
use Laravel\Pulse\Facades\Pulse;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::user(fn ($user) => [
        'name' => $user->name,
        'extra' => $user->email,
        'avatar' => $user->avatar_url,
    ]);

    // ...
}
```

> [!NOTE]
> 인증된 사용자 캡처 및 조회 방식을 완전히 커스터마이즈하려면, `Laravel\Pulse\Contracts\ResolvesUsers` 인터페이스를 구현하고 Laravel [서비스 컨테이너](/docs/master/container#binding-a-singleton)에 바인딩할 수 있습니다.

<a name="dashboard-cards"></a>
### 카드 (Cards)

<a name="servers-card"></a>
#### Servers

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령어를 실행 중인 모든 서버의 시스템 리소스 사용량을 표시합니다. 시스템 리소스 리포팅에 대한 자세한 내용은 [servers recorder](#servers-recorder) 문서를 참고하세요.

인프라스트럭처에서 서버를 교체한 경우, 일정 기간 이후 Pulse 대시보드에서 비활성 서버를 숨기고 싶을 수 있습니다. 이럴 때는 `ignore-after` 속성에 비활성 서버를 몇 초 후 제거할지 지정하면 됩니다. 또한 `1 hour`, `3 days and 1 hour`와 같은 상대적 시간 문자열도 사용할 수 있습니다:

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
#### 애플리케이션 사용량 (Application Usage)

`<livewire:pulse.usage />` 카드는 애플리케이션에 요청을 보내거나 잡을 디스패치하며 느린 요청을 경험한 상위 10명의 사용자를 표시합니다.

모든 사용량 메트릭을 한 화면에 동시에 보고 싶다면 카드를 여러 번 포함시키고 `type` 속성을 구분하여 사용할 수 있습니다:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse가 사용자 정보를 조회하고 표시하는 방식을 커스터마이즈하려면 [사용자 정보 해석 문서](#dashboard-resolving-users)를 참고하세요.

> [!NOTE]
> 애플리케이션에 많은 요청이 들어오거나 잡이 많이 디스패치 된다면, [샘플링](#sampling)을 활성화하는 것이 좋습니다. 자세한 내용은 [user requests recorder](#user-requests-recorder), [user jobs recorder](#user-jobs-recorder), [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="exceptions-card"></a>
#### 예외 (Exceptions)

`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생한 예외의 빈도와 최근 발생 내역을 표시합니다. 기본적으로 예외는 예외 클래스와 발생 위치별로 그룹화됩니다. 자세한 내용은 [exceptions recorder](#exceptions-recorder) 문서를 참고하세요.

<a name="queues-card"></a>
#### 큐 (Queues)

`<livewire:pulse.queues />` 카드는 큐에 쌓인 작업(job)의 대기·처리·완료·재시도·실패 건수를 포함한 애플리케이션 큐 처리량을 보여줍니다. 더 자세한 내용은 [queues recorder](#queues-recorder) 문서를 참고하세요.

<a name="slow-requests-card"></a>
#### 느린 요청 (Slow Requests)

`<livewire:pulse.slow-requests />` 카드는 기본적으로 설정된 임계값(기본 1,000ms)을 초과하는 모든 요청을 보여줍니다. 더 자세한 내용은 [slow requests recorder](#slow-requests-recorder) 문서를 참고하세요.

<a name="slow-jobs-card"></a>
#### 느린 작업 (Slow Jobs)

`<livewire:pulse.slow-jobs />` 카드는 기본 임계값(1,000ms)을 초과하는 큐 작업을 보여줍니다. 더 자세한 내용은 [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="slow-queries-card"></a>
#### 느린 쿼리 (Slow Queries)

`<livewire:pulse.slow-queries />` 카드는 기본 임계값(1,000ms)을 초과하는 데이터베이스 쿼리를 보여줍니다.

기본적으로 느린 쿼리는 SQL 질의문(바인딩 제외)과 쿼리 발생 위치별로 그룹화됩니다. 단, 위치 캡처 기능을 비활성화할 경우 SQL 질의문만으로 그룹화할 수도 있습니다.

매우 긴 SQL 쿼리의 구문 강조로 인해 렌더링 성능 저하가 우려된다면, `without-highlighting` 속성을 추가해 구문 강조를 끌 수 있습니다:

```blade
<livewire:pulse.slow-queries without-highlighting />
```

자세한 내용은 [slow queries recorder](#slow-queries-recorder) 문서를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
#### 느린 외부 요청 (Slow Outgoing Requests)

`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel의 [HTTP 클라이언트](/docs/master/http-client)를 통해 이루어진 외부 요청 중, 임계값(기본 1,000ms)을 초과한 요청을 보여줍니다.

기본적으로 전체 URL별로 그룹화하지만, 유사한 외부 요청을 정규표현식으로 그룹화할 수도 있습니다. 자세한 내용은 [slow outgoing requests recorder](#slow-outgoing-requests-recorder) 문서를 참고하세요.

<a name="cache-card"></a>
#### 캐시 (Cache)

`<livewire:pulse.cache />` 카드는 애플리케이션 전체 및 개별 키별 캐시 적중(hit) 및 실패(miss) 통계를 보여줍니다.

기본적으로 키별로 그룹화하지만, 유사 키를 정규표현식으로 그룹화할 수도 있습니다. 더 자세한 내용은 [cache interactions recorder](#cache-interactions-recorder) 문서를 참고하세요.

<a name="capturing-entries"></a>
## 엔트리 캡처 (Capturing Entries)

대부분의 Pulse 레코더는 Laravel의 프레임워크 이벤트에 따라 자동으로 엔트리를 캡처합니다. 하지만 [servers recorder](#servers-recorder) 및 일부 서드파티 카드들은 정보를 주기적으로 폴링해야 하므로, 애플리케이션 각 서버에서 `pulse:check` 데몬을 실행해야 합니다:

```php
php artisan pulse:check
```

> [!NOTE]
> `pulse:check` 프로세스를 백그라운드에서 영구적으로 실행하려면 Supervisor와 같은 프로세스 모니터를 사용하여 명령어가 중단되지 않도록 관리해야 합니다.

`pulse:check` 명령어는 장시간 실행되는 프로세스이기 때문에 코드베이스 변경을 인식하지 못합니다. 따라서 애플리케이션 배포 과정에서 `pulse:restart` 명령어를 통해 명령어를 정상적으로 재시작해야 합니다:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/master/cache)를 재시작 신호 저장에 사용하므로, 이 기능 사용 전 애플리케이션에 적절한 캐시 드라이버가 설정되어 있는지 확인하십시오.

<a name="recorders"></a>
### 레코더 (Recorders)

레코더는 애플리케이션에서 발생한 엔트리를 캡처하여 Pulse 데이터베이스에 저장하는 역할을 합니다. 레코더는 [Pulse 설정 파일](#configuration) 내 `recorders` 섹션에서 등록·설정할 수 있습니다.

<a name="cache-interactions-recorder"></a>
#### 캐시 상호작용 (Cache Interactions)

`CacheInteractions` 레코더는 [캐시](/docs/master/cache)의 히트 및 미스 정보를 [Cache](#cache-card) 카드에 표시하도록 캡처합니다.

[샘플링 비율](#sampling)과 무시할 키 패턴 등을 옵션으로 조정할 수 있습니다.

또한, 유사한 키를 하나의 엔트리로 그룹화하도록 키 그룹핑을 설정할 수 있습니다. 예를 들어, 동일 유형의 정보를 캐싱하지만 각기 다른 고유 ID를 가지는 키에서 ID를 제거해 그룹화할 수 있습니다. 그룹은 정규표현식을 이용한 find & replace 방식으로 설정하며, 설정 예시는 아래와 같습니다:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

처음으로 일치하는 패턴이 적용되며, 일치하는 패턴이 없으면 키 자체가 그대로 캡처됩니다.

<a name="exceptions-recorder"></a>
#### 예외 (Exceptions)

`Exceptions` 레코더는 애플리케이션에서 발생한 리포팅 가능한 예외 정보를 [Exceptions](#exceptions-card) 카드에 표시하도록 캡처합니다.

[샘플링 비율](#sampling), 무시할 예외 패턴, 그리고 예외 발생 위치 저장 여부를 옵션으로 조정할 수 있습니다. 위치를 저장하는 경우 Pulse 대시보드에서 예외의 발생 위치를 파악하는 데 도움이 되지만, 동일 예외가 여러 위치에서 발생하면 각각의 위치별로 여러 개의 예외로 표시됩니다.

<a name="queues-recorder"></a>
#### 큐 (Queues)

`Queues` 레코더는 애플리케이션의 큐 정보를 [Queues](#queues-card) 카드에 표시하도록 캡처합니다.

[샘플링 비율](#sampling)과 무시할 작업 패턴을 옵션으로 조정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
#### 느린 작업 (Slow Jobs)

`SlowJobs` 레코더는 애플리케이션에서 발생한 느린 작업(job) 정보를 [Slow Jobs](#slow-jobs-recorder) 카드에 표시하도록 캡처합니다.

느린 작업 임계값, [샘플링 비율](#sampling), 무시할 작업 패턴 등을 옵션으로 조정할 수 있습니다.

특정 작업이 일반적으로 더 오래 걸린다면, 작업별 임계값도 아래와 같이 개별 설정할 수 있습니다:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

작업 클래스명이 어느 패턴과도 일치하지 않으면 `'default'` 값이 사용됩니다.

<a name="slow-outgoing-requests-recorder"></a>
#### 느린 외부 요청 (Slow Outgoing Requests)

`SlowOutgoingRequests` 레코더는 Laravel의 [HTTP 클라이언트](/docs/master/http-client)로 발생한 외부 HTTP 요청 중, 임계값을 초과한 요청 정보를 [Slow Outgoing Requests](#slow-outgoing-requests-card) 카드에 캡처합니다.

느린 외부 요청 임계값, [샘플링 비율](#sampling), 무시할 URL 패턴 등을 조정할 수 있습니다.

특정 외부 요청이 더 오래 걸릴 것으로 예상될 경우, 아래와 같이 요청별 임계값을 개별 설정할 수 있습니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

요청 URL이 어느 패턴과도 일치하지 않으면 `'default'` 값이 사용됩니다.

또한, 유사한 URL을 하나의 엔트리로 그룹화하도록 URL 그룹핑도 지원합니다. 예를 들어, URL 경로의 고유 ID를 제거하거나 도메인별 그룹화가 가능합니다. 설정 예시는 아래와 같습니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'groups' => [
        // '#^https://api\.github\.com/repos/.*$#' => 'api.github.com/repos/*',
        // '#^https?://([^/]*).*$#' => '\1',
        // '#/\d+#' => '/*',
    ],
],
```

처음으로 일치하는 패턴이 적용되며, 일치하는 패턴이 없으면 URL이 그대로 캡처됩니다.

<a name="slow-queries-recorder"></a>
#### 느린 쿼리 (Slow Queries)

`SlowQueries` 레코더는 설정된 임계값을 초과하는 애플리케이션의 데이터베이스 쿼리를 [Slow Queries](#slow-queries-card) 카드에 캡처합니다.

느린 쿼리 임계값, [샘플링 비율](#sampling), 무시할 쿼리 패턴, 쿼리 위치 캡처 여부 등을 설정할 수 있습니다. 쿼리 위치는 대시보드에 표시되어 쿼리의 발생 위치를 파악하는 데 유용하지만, 동일 쿼리가 여러 위치에서 실행될 경우 각각 별도로 표시될 수 있습니다.

특정 쿼리가 더 느릴 것으로 예상된다면 쿼리별 임계값도 설정할 수 있습니다:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

SQL이 어느 패턴과도 일치하지 않으면 `'default'` 값이 사용됩니다.

<a name="slow-requests-recorder"></a>
#### 느린 요청 (Slow Requests)

`Requests` 레코더는 애플리케이션에서 들어온 요청 정보를 [Slow Requests](#slow-requests-card) 및 [애플리케이션 사용량](#application-usage-card) 카드에 캡처합니다.

느린 요청 임계값, [샘플링 비율](#sampling), 무시할 경로 등을 조정할 수 있습니다.

특정 요청이 더 오래 걸릴 것으로 예상될 경우 아래와 같이 요청별 임계값을 개별 설정할 수 있습니다:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

요청 URL이 어느 패턴과도 일치하지 않으면 `'default'` 값이 사용됩니다.

<a name="servers-recorder"></a>
#### 서버 (Servers)

`Servers` 레코더는 애플리케이션 서버의 CPU, 메모리, 스토리지 사용량을 [Servers](#servers-card) 카드에 캡처합니다. 이 레코더는 [pulse:check 명령어](#capturing-entries)가 모니터링할 각 서버에서 실행 중이어야 합니다.

각 서버는 고유한 이름을 가져야 합니다. 기본적으로 PHP의 `gethostname`이 반환하는 값을 사용하지만, 커스터마이즈가 필요하다면 `PULSE_SERVER_NAME` 환경 변수를 설정할 수 있습니다:

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 구성 파일에서 모니터링할 디렉터리도 커스텀할 수 있습니다.

<a name="user-jobs-recorder"></a>
#### 사용자 작업 (User Jobs)

`UserJobs` 레코더는 애플리케이션에서 잡을 디스패치한 사용자 정보를 [애플리케이션 사용량](#application-usage-card) 카드에 캡처합니다.

[샘플링 비율](#sampling)과 무시할 작업 패턴을 옵션으로 조정할 수 있습니다.

<a name="user-requests-recorder"></a>
#### 사용자 요청 (User Requests)

`UserRequests` 레코더는 애플리케이션에 요청을 보낸 사용자 정보를 [애플리케이션 사용량](#application-usage-card) 카드에 캡처합니다.

[샘플링 비율](#sampling)과 무시할 URL 패턴을 옵션으로 조정할 수 있습니다.

<a name="filtering"></a>
### 필터링 (Filtering)

앞서 살펴보았듯, 많은 [레코더](#recorders)에서는 값(예: 요청의 URL)에 따라 특정 엔트리를 "무시"하도록 설정할 수 있습니다. 그러나, 때로는 현재 인증된 사용자 등 다른 조건을 기반으로 엔트리를 필터링하고 싶을 때가 있습니다. 이런 경우, Pulse의 `filter` 메서드에 클로저를 전달해 레코드를 필터링할 수 있습니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드 내에서 이 메서드를 호출합니다:

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Pulse\Entry;
use Laravel\Pulse\Facades\Pulse;
use Laravel\Pulse\Value;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::filter(function (Entry|Value $entry) {
        return Auth::user()->isNotAdmin();
    });

    // ...
}
```

<a name="performance"></a>
## 성능 (Performance)

Pulse는 별도의 인프라 없이도 기존 애플리케이션에 바로 적용할 수 있도록 설계되었습니다. 하지만 트래픽이 많은 애플리케이션에서는 Pulse가 성능에 미치는 영향을 최소화할 다양한 방법이 있습니다.

<a name="using-a-different-database"></a>
### 다른 데이터베이스 사용 (Using a Different Database)

트래픽이 많은 애플리케이션의 경우 Pulse를 위한 전용 데이터베이스 연결을 사용함으로써 본 애플리케이션 데이터베이스에 대한 부하를 줄일 수 있습니다.

Pulse가 사용할 [데이터베이스 연결](/docs/master/database#configuration)은 `PULSE_DB_CONNECTION` 환경 변수로 지정할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis 인제스트 (Redis Ingest)

> [!WARNING]
> Redis 인제스트 기능을 사용하려면 Redis 6.2 이상 및 애플리케이션에 `phpredis` 또는 `predis` 클라이언트 드라이버가 설정되어 있어야 합니다.

기본적으로 Pulse는 [설정된 데이터베이스 연결](#using-a-different-database)에 HTTP 응답 반환이나 작업 처리 직후 바로 엔트리를 저장합니다. 하지만 Pulse의 Redis 인제스트 드라이버를 사용하면 엔트리를 Redis 스트림에 보낼 수 있습니다. 이 기능은 환경 변수 `PULSE_INGEST_DRIVER`로 활성화할 수 있습니다:

```ini
PULSE_INGEST_DRIVER=redis
```

Pulse는 기본적으로 [Redis 연결](/docs/master/redis#configuration)을 사용하지만, `PULSE_REDIS_CONNECTION` 환경 변수로 커스터마이즈할 수도 있습니다:

```ini
PULSE_REDIS_CONNECTION=pulse
```

> [!WARNING]
> Redis 인제스트 드라이버 사용 시, Pulse 설치에 사용하는 Redis 연결과 Redis 기반 큐에 사용하는 연결은 반드시 분리해야 합니다.

Redis 인제스트를 사용할 경우, `pulse:work` 명령어를 실행하여 스트림을 모니터링하고 Redis에서 Pulse 데이터베이스 테이블로 엔트리를 이동시켜야 합니다.

```php
php artisan pulse:work
```

> [!NOTE]
> `pulse:work` 프로세스를 영구적으로 백그라운드에서 실행하려면 Supervisor 등의 프로세스 모니터를 사용해 Pulse 워커가 중단없이 실행되도록 해야 합니다.

`pulse:work` 역시 장시간 실행되는 프로세스이므로, 코드 변경을 감지하지 못합니다. 애플리케이션 배포 시에는 아래와 같이 명령어를 정상적으로 재시작해주어야 합니다:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/master/cache)를 재시작 신호 저장에 사용하므로, 이 기능 사용 전 애플리케이션에 적절한 캐시 드라이버가 설정되어 있는지 확인하십시오.

<a name="sampling"></a>
### 샘플링 (Sampling)

기본적으로 Pulse는 관련 이벤트가 발생할 때마다 모두 캡처합니다. 트래픽이 많은 경우, 대시보드에서 긴 기간 조회 시 수백만 개의 데이터 행 집계가 필요할 수 있습니다.

이런 환경에서는 특정 Pulse 데이터 레코더에 "샘플링"을 활성화할 수 있습니다. 예를 들어 [User Requests](#user-requests-recorder) 레코더의 샘플 비율을 `0.1`로 지정하면, 전체 요청 중 약 10%만 저장합니다. 대시보드에는 값이 스케일되어 표시되며, 근사치임을 나타내는 `~` 기호가 함께 표시됩니다.

특정 메트릭에 엔트리가 많을수록, 정확도 저하 없이 더 낮은 샘플 비율을 사용할 수 있습니다.

<a name="trimming"></a>
### 트리밍 (Trimming)

Pulse는 대시보드 조회 기간에서 벗어난 엔트리를 자동으로 트리밍(삭제)합니다. 트리밍은 데이터 인제스트 시 로터리(lottery) 방식으로 진행되며, Pulse [설정 파일](#configuration)에서 커스텀할 수 있습니다.

<a name="pulse-exceptions"></a>
### Pulse 예외 처리 (Handling Pulse Exceptions)

Pulse 데이터 캡처 중 데이터베이스 연결 실패 등 예외가 발생할 경우, 애플리케이션에 영향을 주지 않게 Pulse는 예외를 조용히 무시합니다.

예외 처리 방식을 커스터마이즈하려면 `handleExceptionsUsing` 메서드에 클로저를 전달할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;
use Illuminate\Support\Facades\Log;

Pulse::handleExceptionsUsing(function ($e) {
    Log::debug('An exception happened in Pulse', [
        'message' => $e->getMessage(),
        'stack' => $e->getTraceAsString(),
    ]);
});
```

<a name="custom-cards"></a>
## 사용자 정의 카드 (Custom Cards)

Pulse를 활용하면 애플리케이션에 특화된 데이터를 표시하는 사용자 정의 카드를 직접 만들 수 있습니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하므로, 첫 사용자 정의 카드를 만들기 전에 [Livewire 문서](https://livewire.laravel.com/docs)를 참고하면 좋습니다.

<a name="custom-card-components"></a>
### 카드 컴포넌트 (Card Components)

Laravel Pulse에서 사용자 정의 카드를 만들려면, 기본 `Card` Livewire 컴포넌트를 상속한 후 해당 뷰를 정의합니다:

```php
namespace App\Livewire\Pulse;

use Laravel\Pulse\Livewire\Card;
use Livewire\Attributes\Lazy;

#[Lazy]
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers');
    }
}
```

Livewire의 [lazy loading](https://livewire.laravel.com/docs/lazy) 기능을 사용할 경우, `Card` 컴포넌트가 자동으로 `cols`‧`rows` 속성에 따라 플레이스홀더를 제공합니다.

카드에 사용할 뷰에서는 Pulse의 Blade 컴포넌트를 활용해 일관성 있는 UI를 구현할 수 있습니다:

```blade
<x-pulse::card :cols="$cols" :rows="$rows" :class="$class" wire:poll.5s="">
    <x-pulse::card-header name="Top Sellers">
        <x-slot:icon>
            ...
        </x-slot:icon>
    </x-pulse::card-header>

    <x-pulse::scroll :expand="$expand">
        ...
    </x-pulse::scroll>
</x-pulse::card>
```

`$cols`, `$rows`, `$class`, `$expand` 변수는 해당 Blade 컴포넌트에 그대로 전달해 카드 레이아웃을 대시보드 뷰에서 자유롭게 조정할 수 있도록 합니다. 또한 `wire:poll.5s=""` 속성을 뷰에 추가하면 5초마다 카드가 자동 갱신되는 효과를 줍니다.

Livewire 컴포넌트 및 템플릿 정의가 끝나면, [대시보드 뷰](#dashboard-customization)에서 카드를 아래와 같이 추가할 수 있습니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> 카드가 패키지에 포함된 경우, `Livewire::component` 메서드를 통해 Livewire에 해당 컴포넌트를 반드시 등록해야 합니다.

<a name="custom-card-styling"></a>
### 스타일링 (Styling)

카드에서 Pulse 기본 클래스 및 컴포넌트 외의 추가적인 스타일링이 필요할 경우, 카드용 커스텀 CSS를 적용하는 몇 가지 방법이 있습니다.

<a name="custom-card-styling-vite"></a>
#### Laravel Vite 통합

커스텀 카드가 애플리케이션 코드베이스 내에 있고, Laravel의 [Vite 통합](/docs/master/vite)을 사용하는 경우, `vite.config.js`에 카드용 CSS 엔트리포인트를 추가할 수 있습니다:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

이후, [대시보드 뷰](#dashboard-customization)에서 `@vite` Blade 지시어로 해당 CSS 엔트리포인트를 지정하면 됩니다:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS 파일 직접 사용

Pulse 카드가 패키지 등에 포함되어 있는 경우 등에는, Livewire 컴포넌트에 `css` 메서드를 정의하여 해당 CSS 파일 경로를 반환하도록 할 수 있습니다:

```php
class TopSellers extends Card
{
    // ...

    protected function css()
    {
        return __DIR__.'/../../dist/top-sellers.css';
    }
}
```

이 카드가 대시보드에 포함되면, Pulse는 해당 CSS 파일 내용을 `<style>` 태그 내에 자동으로 포함시켜 별도로 public 디렉터리로 배포할 필요가 없습니다.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS를 사용할 경우, 별도의 CSS 엔트리포인트를 만드는 것이 좋습니다. 아래 예시는 Pulse가 이미 [Preflight](https://tailwindcss.com/docs/preflight) 기본 스타일을 포함하고 있으므로 이를 제외하고, CSS 셀렉터를 활용해 Pulse의 Tailwind 클래스와의 충돌을 방지하는 방법을 보여줍니다:

```css
@import "tailwindcss/theme.css";

@custom-variant dark (&:where(.dark, .dark *));
@source "./../../views/livewire/pulse/top-sellers.blade.php";

@theme {
  /* ... */
}

#top-sellers {
  @import "tailwindcss/utilities.css" source(none);
}
```

카드의 뷰에서는 해당 CSS 셀렉터에 매칭되는 `id` 또는 `class` 속성을 추가해야 합니다:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### 데이터 캡처 및 집계 (Data Capture and Aggregation)

사용자 정의 카드는 어느 곳에서든 데이터 조회 및 표시가 가능하지만, Pulse의 강력하고 효율적인 데이터 기록 및 집계 시스템을 활용할 수도 있습니다.

<a name="custom-card-data-capture"></a>
#### 엔트리 캡처 (Capturing Entries)

Pulse에서는 `Pulse::record` 메서드로 엔트리를 기록할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

첫 번째 인수는 기록할 엔트리의 `type`이며, 두 번째 인수는 집계 데이터의 그룹화를 결정하는 `key`입니다. 대부분의 집계 방법에서는 집계 대상이 되는 `value`(여기서는 `$sale->amount`)도 함께 지정해야 합니다. 이후 `sum` 등 하나 이상의 집계 메서드를 체이닝하여 선택할 수 있습니다.

지원하는 집계 메서드는 다음과 같습니다:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> 현재 인증된 사용자 ID를 집계에 활용하는 카드 패키지를 빌드할 때는, [사용자 정보 해석 커스터마이즈](#dashboard-resolving-users)가 적용된 경우를 고려하여 `Pulse::resolveAuthenticatedUserId()`를 사용해야 합니다.

<a name="custom-card-data-retrieval"></a>
#### 집계 데이터 조회 (Retrieving Aggregate Data)

Pulse의 `Card` Livewire 컴포넌트를 상속할 경우, 대시보드에서 조회 중인 기간에 맞춰 `aggregate` 메서드로 집계 데이터를 조회할 수 있습니다:

```php
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers', [
            'topSellers' => $this->aggregate('user_sale', ['sum', 'count'])
        ]);
    }
}
```

`aggregate` 메서드는 PHP의 `stdClass` 객체 컬렉션을 반환합니다. 각 객체는 미리 캡처했던 `key` 속성과, 요청한 집계별 속성을 포함합니다:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse는 주로 미리 집계된 버킷에서 데이터를 조회하므로, 데이터 기록 시 반드시 집계 메서드를 함께 명시해야 합니다. 가장 오래된 버킷은 조회 기간의 일부만 해당될 수 있기 때문에, Pulse는 해당 버킷 내 엔트리를 추가 집계해 갭을 메우고 각 요청마다 전체 기간에 대한 정확한 값을 계산합니다.

특정 타입 전체 합계를 구하려면 `aggregateTotal` 메서드를 사용할 수도 있습니다. 예를 들어, 전체 사용자 판매 합계를 구하는 방법은 다음과 같습니다:

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### 사용자 표시 (Displaying Users)

key 값으로 사용자 ID를 기록한 집계 데이터의 경우, `Pulse::resolveUsers` 메서드로 사용자 레코드를 손쉽게 조회할 수 있습니다:

```php
$aggregates = $this->aggregate('user_sale', ['sum', 'count']);

$users = Pulse::resolveUsers($aggregates->pluck('key'));

return view('livewire.pulse.top-sellers', [
    'sellers' => $aggregates->map(fn ($aggregate) => (object) [
        'user' => $users->find($aggregate->key),
        'sum' => $aggregate->sum,
        'count' => $aggregate->count,
    ])
]);
```

`find` 메서드는 `name`, `extra`, `avatar` 키를 가지는 객체를 반환하므로, 이를 그대로 `<x-pulse::user-card>` Blade 컴포넌트에 전달할 수도 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### 사용자 정의 레코더 (Custom Recorders)

패키지 제작자의 경우, 사용자가 데이터 캡처 방식을 쉽게 설정할 수 있도록 레코더 클래스를 제공할 수 있습니다.

레코더는 애플리케이션의 `config/pulse.php` 파일 내 `recorders` 섹션에 등록됩니다:

```php
[
    // ...
    'recorders' => [
        Acme\Recorders\Deployments::class => [
            // ...
        ],

        // ...
    ],
]
```

레코더 클래스에서는 `$listen` 속성을 지정해 이벤트 리스너로 사용할 수 있습니다. Pulse가 리스너를 자동 등록하고 `record` 메서드를 호출합니다:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * 리스닝할 이벤트 목록
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * 배포 기록
     */
    public function record(Deployment $event): void
    {
        $config = Config::get('pulse.recorders.'.static::class);

        Pulse::record(
            // ...
        );
    }
}
```
