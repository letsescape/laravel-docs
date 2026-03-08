# 라라벨 펄스 (Laravel Pulse)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
- [대시보드](#dashboard)
    - [인가](#dashboard-authorization)
    - [커스터마이징](#dashboard-customization)
    - [사용자 해석](#dashboard-resolving-users)
    - [카드](#dashboard-cards)
- [엔트리 수집](#capturing-entries)
    - [레코더](#recorders)
    - [필터링](#filtering)
- [성능](#performance)
    - [다른 데이터베이스 사용](#using-a-different-database)
    - [Redis 인제스트](#ingest)
    - [샘플링](#sampling)
    - [트리밍](#trimming)
    - [Pulse 예외 처리](#pulse-exceptions)
- [커스텀 카드](#custom-cards)
    - [카드 컴포넌트](#custom-card-components)
    - [스타일링](#custom-card-styling)
    - [데이터 수집 및 집계](#custom-card-data)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능과 사용 현황을 한눈에 파악할 수 있는 인사이트를 제공합니다. Pulse를 사용하면 느린 작업 및 엔드포인트와 같은 병목 현상을 추적하고, 가장 활발한 사용자를 찾아내는 등 다양한 정보를 확인할 수 있습니다.

개별 이벤트에 대한 심층적인 디버깅이 필요한 경우에는 [Laravel Telescope](/docs/12.x/telescope)를 참고하시기 바랍니다.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Pulse의 1차 저장소 구현에서는 현재 MySQL, MariaDB, PostgreSQL 데이터베이스가 필요합니다. 다른 데이터베이스 엔진을 사용하는 경우, Pulse 데이터를 위해 별도의 MySQL, MariaDB, 또는 PostgreSQL 데이터베이스를 준비해야 합니다.

Composer 패키지 관리자를 사용하여 Pulse를 설치할 수 있습니다:

```shell
composer require laravel/pulse
```

다음으로 `vendor:publish` Artisan 명령어를 실행하여 Pulse 설정 및 마이그레이션 파일을 배포해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

마지막으로, Pulse 데이터를 저장하기 위해 필요한 테이블을 생성하려면 `migrate` 명령어를 실행해야 합니다:

```shell
php artisan migrate
```

Pulse 데이터베이스 마이그레이션이 완료되면, `/pulse` 경로를 통해 Pulse 대시보드에 접근할 수 있습니다.

> [!NOTE]
> Pulse 데이터를 애플리케이션의 기본 데이터베이스에 저장하고 싶지 않은 경우, [별도의 데이터베이스 연결을 지정](#using-a-different-database)할 수 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

Pulse의 많은 설정 옵션들은 환경 변수로 제어할 수 있습니다. 사용 가능한 옵션을 확인하거나, 새로운 레코더를 등록하거나, 고급 설정을 구성하려면 `config/pulse.php` 설정 파일을 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## 대시보드 (Dashboard)

<a name="dashboard-authorization"></a>
### 인가 (Authorization)

Pulse 대시보드는 `/pulse` 경로를 통해 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접근이 가능하므로, 운영 환경에서는 `'viewPulse'` 인가 게이트를 커스터마이즈해야 합니다. 이는 애플리케이션의 `app/Providers/AppServiceProvider.php` 파일 내에서 설정할 수 있습니다:

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
### 커스터마이징 (Customization)

Pulse 대시보드의 카드 및 레이아웃은 대시보드 뷰를 게시하여 구성할 수 있습니다. 대시보드 뷰는 `resources/views/vendor/pulse/dashboard.blade.php` 경로에 게시됩니다:

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

대시보드는 [Livewire](https://livewire.laravel.com/)로 구동되며, 어떤 자바스크립트 에셋을 다시 빌드하지 않아도 카드와 레이아웃을 커스터마이즈할 수 있습니다.

이 파일 내에서 `<x-pulse>` 컴포넌트가 대시보드 렌더링을 담당하며, 카드들을 위한 그리드 레이아웃을 제공합니다. 대시보드를 화면 전체 너비로 확장하려면 `full-width` prop을 추가하면 됩니다:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

기본적으로 `<x-pulse>` 컴포넌트는 12 컬럼 그리드를 생성하지만, `cols` prop을 사용해 컬럼 수를 변경할 수 있습니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

각 카드는 공간 및 위치를 제어하기 위해 `cols`와 `rows` prop을 지원합니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

대부분의 카드에서는 스크롤 대신 전체 카드를 표시할 수 있도록 `expand` prop을 지원합니다:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### 사용자 해석 (Resolving Users)

사용자 관련 정보를 표시하는 카드(예: Application Usage 카드)에서는 Pulse가 사용자의 ID만을 기록합니다. 대시보드를 렌더링할 때, Pulse는 기본 `Authenticatable` 모델에서 `name`과 `email` 필드를 조회하고, 아바타는 Gravatar 웹 서비스를 사용해 표시합니다.

필드와 아바타를 변경하고 싶다면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에서 `Pulse::user` 메서드를 호출하여 커스터마이즈할 수 있습니다.

`user` 메서드는 `Authenticatable` 모델 인스턴스를 받아 `name`, `extra`, `avatar` 정보를 포함하는 배열을 반환하는 클로저를 받습니다:

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
> 인증된 사용자를 캡처하고 조회하는 방법을 완전히 커스터마이즈하려면 `Laravel\Pulse\Contracts\ResolvesUsers` 계약을 구현하고, Laravel의 [서비스 컨테이너](/docs/12.x/container#binding-a-singleton)에 바인딩할 수 있습니다.

<a name="dashboard-cards"></a>
### 카드 (Cards)

<a name="servers-card"></a>
#### 서버

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령어를 실행 중인 모든 서버의 시스템 리소스 사용량을 표시합니다. 시스템 리소스 리포팅에 대한 자세한 내용은 [servers recorder](#servers-recorder) 문서를 참고하세요.

인프라에서 서버를 교체한 경우, Pulse 대시보드에 일정 시간 이후 비활성화된 서버를 표시하지 않도록 할 수 있습니다. 이 경우, 비활성 서버가 대시보드에서 제거되는 시간을 초 단위로 지정하는 `ignore-after` prop을 사용할 수 있습니다. 또는 `1 hour`, `3 days and 1 hour`와 같은 상대적 시간 형식의 문자열도 지정할 수 있습니다:

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
#### 애플리케이션 사용량

`<livewire:pulse.usage />` 카드는 애플리케이션에 요청을 보내거나, 작업을 디스패치하거나, 느린 요청을 경험한 상위 10명의 사용자를 표시합니다.

화면에서 모든 사용량 지표를 동시에 보고 싶다면, 카드를 여러 번 포함하고 `type` 속성을 지정할 수 있습니다:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse가 사용자 정보를 어떻게 조회하고 표시하는지 커스터마이즈하는 방법은 [사용자 해석](#dashboard-resolving-users) 문서를 참고하세요.

> [!NOTE]
> 애플리케이션에 요청이 많이 들어오거나 작업이 자주 디스패치되는 경우, [샘플링](#sampling) 기능을 활성화하는 것이 좋습니다. 자세한 내용은 [user requests recorder](#user-requests-recorder), [user jobs recorder](#user-jobs-recorder), [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="exceptions-card"></a>
#### 예외

`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생한 예외의 빈도와 최신 발생 시점을 보여줍니다. 기본적으로 예외는 예외 클래스와 발생 위치를 기준으로 그룹화됩니다. 자세한 내용은 [exceptions recorder](#exceptions-recorder) 문서를 참고하세요.

<a name="queues-card"></a>
#### 큐

`<livewire:pulse.queues />` 카드는 애플리케이션의 큐 처리량을 표시합니다. 대기, 처리 중, 처리 완료, 다시 대기, 실패한 작업 수 등을 포함합니다. 자세한 내용은 [queues recorder](#queues-recorder) 문서를 참고하세요.

<a name="slow-requests-card"></a>
#### 느린 요청

`<livewire:pulse.slow-requests />` 카드는 기본값으로 1,000ms 임계값을 초과한 애플리케이션의 요청을 보여줍니다. 자세한 내용은 [slow requests recorder](#slow-requests-recorder) 문서를 참고하세요.

<a name="slow-jobs-card"></a>
#### 느린 작업

`<livewire:pulse.slow-jobs />` 카드는 기본값으로 1,000ms 임계값을 초과한 대기 작업을 표시합니다. 자세한 내용은 [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="slow-queries-card"></a>
#### 느린 쿼리

`<livewire:pulse.slow-queries />` 카드는 기본적으로 1,000ms 임계값을 초과한 데이터베이스 쿼리를 보여줍니다.

기본적으로 느린 쿼리는 SQL 쿼리(바인딩 제외)와 발생 위치 기준으로 그룹화됩니다. 쿼리 위치를 캡처하지 않고 SQL 쿼리 기준으로만 그룹화할 수도 있습니다.

아주 긴 SQL 쿼리에 구문 강조가 적용되어 렌더링 성능 문제가 발생한다면, `without-highlighting` prop을 추가해 강조를 비활성화할 수 있습니다:

```blade
<livewire:pulse.slow-queries without-highlighting />
```

자세한 내용은 [slow queries recorder](#slow-queries-recorder) 문서를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
#### 느린 외부 요청

`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel의 [HTTP 클라이언트](/docs/12.x/http-client)로 발생시킨 외부 요청 중 설정된 임계값(기본값 1,000ms)을 초과한 요청을 보여줍니다.

기본적으로 모든 엔트리를 전체 URL 기준으로 그룹화합니다. 그러나 정규 표현식을 사용해 유사한 요청을 그룹화하거나 정규화할 수도 있습니다. 자세한 내용은 [slow outgoing requests recorder](#slow-outgoing-requests-recorder) 문서를 참고하세요.

<a name="cache-card"></a>
#### 캐시

`<livewire:pulse.cache />` 카드는 애플리케이션의 캐시 적중 및 실패 통계를 전역 및 키별로 보여줍니다.

기본적으로 엔트리는 키별로 그룹화되나, 정규 표현식을 사용해 유사한 키를 그룹화할 수도 있습니다. 자세한 내용은 [cache interactions recorder](#cache-interactions-recorder) 문서를 참고하세요.

<a name="capturing-entries"></a>
## 엔트리 수집 (Capturing Entries)

대부분의 Pulse 레코더는 Laravel에서 발생하는 프레임워크 이벤트를 기반으로 자동으로 엔트리를 캡처합니다. 하지만 [servers recorder](#servers-recorder) 및 일부 서드파티 카드는 주기적으로 정보를 폴링해야 합니다. 이러한 카드들을 사용하려면 각 애플리케이션 서버에서 `pulse:check` 데몬을 실행해야 합니다:

```php
php artisan pulse:check
```

> [!NOTE]
> `pulse:check` 프로세스를 항상 백그라운드에서 실행하려면, Supervisor와 같은 프로세스 모니터를 사용하여 명령어가 멈추지 않도록 해야 합니다.

`pulse:check` 명령어는 장기 실행 프로세스이므로 코드베이스 변경을 감지하지 못합니다. 배포 과정에서 `pulse:restart` 명령어를 호출하여 프로세스를 정상적으로 재시작해야 합니다:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/12.x/cache)를 사용해 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 애플리케이션에 캐시 드라이버가 제대로 구성되어 있는지 확인하세요.

<a name="recorders"></a>
### 레코더 (Recorders)

레코더는 애플리케이션에서 수집된 엔트리를 Pulse 데이터베이스에 저장하는 역할을 합니다. 레코더는 [Pulse 설정 파일](#configuration)의 `recorders` 섹션에 등록 및 구성됩니다.

<a name="cache-interactions-recorder"></a>
#### 캐시 동작

`CacheInteractions` 레코더는 [캐시](/docs/12.x/cache)의 적중/실패 정보를 [캐시](#cache-card) 카드에 표시하기 위해 수집합니다.

[샘플링 비율](#sampling)과 무시할 키 패턴을 선택적으로 조정할 수 있습니다.

비슷한 키를 하나의 엔트리로 그룹화하는 키 그룹화도 설정할 수 있습니다. 예를 들어, 동일한 유형의 정보를 캐싱하는 고유 ID를 키에서 제거할 수 있습니다. 그룹은 정규 표현식으로 키 일부를 "찾아 바꾸기" 방식으로 구성합니다. 설정 파일에 예시가 포함되어 있습니다:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

일치하는 첫 번째 패턴이 사용됩니다. 일치하는 패턴이 없으면 키가 그대로 캡처됩니다.

<a name="exceptions-recorder"></a>
#### 예외

`Exceptions` 레코더는 애플리케이션에서 발생한 리포트 가능한 예외의 정보를 [예외](#exceptions-card) 카드에 표시하기 위해 수집합니다.

[샘플링 비율](#sampling)과 무시할 예외 패턴을 선택적으로 조정할 수 있습니다. 예외가 발생한 위치를 캡처할지 여부도 설정할 수 있습니다. 캡처한 위치 정보는 Pulse 대시보드에 표시되어 예외의 근원을 추적하는 데 도움이 됩니다. 동일한 예외가 여러 위치에서 발생하면, 각각의 고유 위치마다 여러 번 나타납니다.

<a name="queues-recorder"></a>
#### 큐

`Queues` 레코더는 애플리케이션의 큐 정보를 [큐](#queues-card) 카드에 표시하기 위해 수집합니다.

[샘플링 비율](#sampling)과 무시할 작업 패턴을 선택적으로 조정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
#### 느린 작업

`SlowJobs` 레코더는 애플리케이션에서 발생한 느린 작업 정보를 [느린 작업](#slow-jobs-recorder) 카드에 표시하기 위해 수집합니다.

느린 작업 임계값, [샘플링 비율](#sampling), 무시할 작업 패턴을 선택적으로 조정할 수 있습니다.

특정 작업이 다른 작업보다 오랜 시간이 걸릴 것으로 예상된다면, 작업별 임계값을 설정할 수 있습니다:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

정규 표현식 패턴이 작업 클래스명과 일치하지 않으면 `'default'` 값이 사용됩니다.

<a name="slow-outgoing-requests-recorder"></a>
#### 느린 외부 요청

`SlowOutgoingRequests` 레코더는 Laravel의 [HTTP 클라이언트](/docs/12.x/http-client)를 사용해 발생한 외부 요청 중 임계값을 초과한 요청 정보를 [느린 외부 요청](#slow-outgoing-requests-card) 카드에 표시합니다.

느린 외부 요청 임계값, [샘플링 비율](#sampling), 무시할 URL 패턴을 선택적으로 조정할 수 있습니다.

특정 요청이 다른 요청보다 오래 걸릴 것으로 예상된다면, 요청별 임계값을 설정할 수 있습니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

정규 표현식 패턴이 요청의 URL과 일치하지 않으면 `'default'` 값이 사용됩니다.

또한 유사한 URL을 하나의 엔트리로 그룹화할 수도 있습니다. 예를 들어, 고유 ID가 포함된 URL 경로나 도메인별로 그룹화할 수 있습니다. 그룹은 정규 표현식으로 URL 일부를 "찾아 바꾸기"하는 방식으로 구성합니다. 설정 파일에 몇 가지 예시가 포함되어 있습니다:

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

일치하는 첫 번째 패턴이 적용되며, 매칭되는 패턴이 없으면 URL이 그대로 캡처됩니다.

<a name="slow-queries-recorder"></a>
#### 느린 쿼리

`SlowQueries` 레코더는 지정된 임계값을 초과하는 모든 데이터베이스 쿼리를 [느린 쿼리](#slow-queries-card) 카드에 표시하기 위해 캡처합니다.

느린 쿼리 임계값, [샘플링 비율](#sampling), 무시할 쿼리 패턴을 선택적으로 조정할 수 있습니다. 쿼리 위치를 캡처할지 여부도 설정이 가능합니다. 캡처한 위치 정보는 Pulse 대시보드에 나타나 쿼리의 근원을 추적하는 데 도움이 됩니다. 동일 쿼리가 여러 위치에서 발생하면 각 위치마다 별도 항목으로 표시됩니다.

특정 쿼리가 다른 쿼리보다 오래 걸릴 것으로 예상되면 쿼리별 임계값을 설정할 수 있습니다:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

정규 표현식 패턴이 쿼리 SQL과 일치하지 않으면 `'default'` 값이 사용됩니다.

<a name="slow-requests-recorder"></a>
#### 느린 요청

`Requests` 레코더는 애플리케이션에 들어온 요청 정보를 [느린 요청](#slow-requests-card) 및 [애플리케이션 사용량](#application-usage-card) 카드에 표시하기 위해 캡처합니다.

느린 경로 임계값, [샘플링 비율](#sampling), 무시할 경로를 선택적으로 조정할 수 있습니다.

특정 요청에 대해 더 긴 시간을 허용하고 싶을 때, 요청별 임계값을 설정할 수 있습니다:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

정규 표현식 패턴이 요청 URL과 일치하지 않으면 `'default'` 값이 사용됩니다.

<a name="servers-recorder"></a>
#### 서버

`Servers` 레코더는 애플리케이션 서버의 CPU, 메모리, 저장소 사용량을 [서버](#servers-card) 카드에 표시하기 위해 캡처합니다. 이 레코더는 [pulse:check 명령어](#capturing-entries)를 각 모니터링 대상 서버에서 실행해야 합니다.

각 서버는 고유한 이름을 가져야 합니다. 기본적으로 Pulse는 PHP의 `gethostname` 함수로 반환되는 값을 사용합니다. 이를 커스터마이즈하려면 `PULSE_SERVER_NAME` 환경 변수를 설정할 수 있습니다:

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 설정 파일에서 모니터링할 디렉터리도 커스터마이즈할 수 있습니다.

<a name="user-jobs-recorder"></a>
#### 사용자 작업

`UserJobs` 레코더는 사용자가 디스패치한 작업의 정보를 [애플리케이션 사용량](#application-usage-card) 카드에 표시하기 위해 캡처합니다.

[샘플링 비율](#sampling), 무시할 작업 패턴을 선택적으로 조정할 수 있습니다.

<a name="user-requests-recorder"></a>
#### 사용자 요청

`UserRequests` 레코더는 사용자가 보낸 요청 정보를 [애플리케이션 사용량](#application-usage-card) 카드에 표시하기 위해 캡처합니다.

[샘플링 비율](#sampling), 무시할 URL 패턴을 선택적으로 조정할 수 있습니다.

<a name="filtering"></a>
### 필터링 (Filtering)

앞서 설명한 것처럼 많은 [레코더](#recorders)는 설정을 통해 요청의 URL 등 값에 기반해 엔트리를 "무시"하도록 할 수 있습니다. 그러나 때로는 현재 인증된 사용자 등 다른 조건을 기준으로 레코드를 필터링해야 할 수도 있습니다. 이 경우, Pulse의 `filter` 메서드에 클로저를 전달해 엔트리를 필터링할 수 있습니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드 내에서 `filter` 메서드를 호출합니다:

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

Pulse는 별도의 추가 인프라 없이 기존 애플리케이션에 바로 적용할 수 있도록 설계되었습니다. 하지만 트래픽이 많은 애플리케이션의 경우, Pulse가 애플리케이션 성능에 영향을 주지 않도록 여러 방법을 적용할 수 있습니다.

<a name="using-a-different-database"></a>
### 다른 데이터베이스 사용 (Using a Different Database)

트래픽이 많은 애플리케이션에서는 Pulse 전용 데이터베이스 연결을 사용하여 애플리케이션 DB에 영향을 주지 않도록 할 수 있습니다.

Pulse에서 사용하는 [데이터베이스 연결](/docs/12.x/database#configuration)은 `PULSE_DB_CONNECTION` 환경 변수를 통해 지정할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis 인제스트 (Redis Ingest)

> [!WARNING]
> Redis 인제스트 기능은 Redis 6.2 이상과 애플리케이션의 Redis 클라이언트 드라이버로 `phpredis` 또는 `predis`가 필요합니다.

기본적으로 Pulse는 클라이언트에 HTTP 응답을 보낸 후 또는 작업 처리 후 [설정된 데이터베이스 연결](#using-a-different-database)에 엔트리를 바로 저장합니다. 하지만 Pulse의 Redis 인제스트 드라이버를 이용하여 엔트리를 Redis 스트림으로 전송할 수도 있습니다. 이를 사용하려면 `PULSE_INGEST_DRIVER` 환경 변수를 설정합니다:

```ini
PULSE_INGEST_DRIVER=redis
```

Pulse는 기본적으로 기본 [Redis 연결](/docs/12.x/redis#configuration)을 사용하지만, `PULSE_REDIS_CONNECTION` 환경 변수로 따로 지정할 수 있습니다:

```ini
PULSE_REDIS_CONNECTION=pulse
```

> [!WARNING]
> Redis 인제스트 드라이버를 사용할 경우, Pulse 설치에는 반드시 Redis 기반 큐와 다른 Redis 연결을 사용해야 합니다(해당되는 경우).

Redis 인제스트를 사용할 때는 `pulse:work` 명령어를 실행해 스트림을 모니터링하고, Redis에서 Pulse의 데이터베이스 테이블로 엔트리를 옮겨야 합니다.

```php
php artisan pulse:work
```

> [!NOTE]
> `pulse:work` 프로세스를 항상 백그라운드에서 실행하려면 Supervisor와 같은 프로세스 모니터를 이용해 Pulse 워커가 중단되지 않도록 해야 합니다.

`pulse:work` 명령어는 장기 실행 프로세스이므로 코드베이스 변경을 바로 감지하지 않습니다. 애플리케이션 배포 과정에서 `pulse:restart` 명령어를 호출해 프로세스를 정상적으로 재시작해야 합니다:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [캐시](/docs/12.x/cache)를 이용해 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 캐시 드라이버가 애플리케이션에 제대로 구성되어 있는지 확인하세요.

<a name="sampling"></a>
### 샘플링 (Sampling)

기본적으로 Pulse는 애플리케이션에서 발생하는 모든 관련 이벤트를 수집합니다. 트래픽이 많은 애플리케이션에서는 긴 기간 동안 수백만 개의 데이터베이스 행이 대시보드에서 집계될 수 있습니다.

이 경우, 일부 Pulse 데이터 레코더에서 "샘플링"을 활성화할 수 있습니다. 예를 들어, [User Requests](#user-requests-recorder) 레코더의 샘플링 비율을 `0.1`로 설정하면 전체 요청 중 약 10%만 저장합니다. 대시보드에서는 값 앞에 `~`가 붙으며, 이는 값이 추정치임을 의미합니다.

집계 데이터가 많을수록 샘플링 비율을 더 낮춰도 정확도에 크게 영향을 주지 않습니다.

<a name="trimming"></a>
### 트리밍 (Trimming)

Pulse는 대시보드에서 설정한 기간을 벗어난 저장 엔트리를 자동으로 정리합니다. 트리밍은 데이터 인제스트 시 로터리 시스템을 통해 동작하며, Pulse [설정 파일](#configuration)에서 커스터마이즈할 수 있습니다.

<a name="pulse-exceptions"></a>
### Pulse 예외 처리 (Handling Pulse Exceptions)

Pulse 데이터 수집 중, 예를 들어 저장소 데이터베이스 연결 실패 등 예외가 발생하면, 애플리케이션에 영향을 주지 않도록 Pulse는 조용히 실패합니다.

이러한 예외 처리를 커스터마이즈하고 싶을 때는 `handleExceptionsUsing` 메서드에 클로저를 전달할 수 있습니다.

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
## 커스텀 카드 (Custom Cards)

Pulse는 애플리케이션 특성에 맞는 데이터를 표시할 수 있도록 커스텀 카드를 제작할 수 있게 지원합니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하므로, 커스텀 카드를 처음 작성하기 전 [Livewire 문서](https://livewire.laravel.com/docs)를 참고하는 것이 좋습니다.

<a name="custom-card-components"></a>
### 카드 컴포넌트 (Card Components)

라라벨 Pulse에서 커스텀 카드를 만들려면, 기본 `Card` Livewire 컴포넌트를 상속하고 대응되는 뷰를 작성하면 됩니다:

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

Livewire의 [lazy loading](https://livewire.laravel.com/docs/lazy) 기능을 사용할 때, `Card` 컴포넌트는 자동으로 `cols`, `rows` 속성이 전달된 플레이스홀더를 제공합니다.

Pulse 카드의 대응 뷰를 작성할 때는, 일관된 디자인을 위해 Pulse에서 제공하는 Blade 컴포넌트를 활용할 수 있습니다:

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

`$cols`, `$rows`, `$class`, `$expand` 변수는 각각 Blade 컴포넌트로 전달해야 대시보드 뷰에서 카드 레이아웃을 커스터마이즈할 수 있습니다. 또한 `wire:poll.5s=""` 속성을 추가하면 카드가 주기적으로 자동 업데이트됩니다.

Livewire 컴포넌트와 템플릿을 정의한 후, [대시보드 뷰](#dashboard-customization)에서 카드를 포함할 수 있습니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> 패키지 내에 카드를 포함하는 경우, `Livewire::component` 메서드로 컴포넌트를 등록해야 합니다.

<a name="custom-card-styling"></a>
### 스타일링 (Styling)

카드가 Pulse에 포함된 클래스와 컴포넌트 외에 추가 스타일을 필요로 한다면, 카드별 커스텀 CSS를 적용할 몇 가지 방법이 있습니다.

<a name="custom-card-styling-vite"></a>
#### 라라벨 Vite 통합

커스텀 카드가 애플리케이션 코드베이스 내에 있고, 라라벨 [Vite 통합](/docs/12.x/vite)을 사용한다면, `vite.config.js` 파일에서 카드용 CSS 엔트리포인트를 추가할 수 있습니다:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

그런 다음, [대시보드 뷰](#dashboard-customization)에서 `@vite` Blade 디렉티브를 사용해 카드용 CSS 엔트리포인트를 로드하면 됩니다:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS 파일

Pulse 카드가 패키지에 포함된 등 다양한 경우, Livewire 컴포넌트에 `css` 메서드를 정의해 추가 스타일시트를 Pulse에 포함할 수 있습니다:

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

이 카드가 대시보드에 포함되면, Pulse는 해당 파일 내용을 자동으로 `<style>` 태그로 인클루드하므로, 파일을 `public` 디렉터리에 별도로 게시할 필요가 없습니다.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS를 사용할 경우, 별도의 CSS 엔트리포인트를 만들어야 합니다. 아래 예시는 Tailwind의 [Preflight](https://tailwindcss.com/docs/preflight) 기본 스타일(이미 Pulse에 내장됨)을 제외하고, Pulse의 Tailwind 클래스와의 충돌을 막기 위해 CSS 선택자로 Tailwind를 범위지정하는 방식입니다:

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

또한 카드 뷰 내에 해당 CSS 선택자와 일치하는 `id` 또는 `class` 속성을 지정해야 합니다:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### 데이터 수집 및 집계 (Data Capture and Aggregation)

커스텀 카드는 어디서든 데이터를 조회 및 표시할 수 있습니다. 그러나 Pulse의 강력하고 효율적인 데이터 기록 및 집계 시스템을 그대로 활용하는 것이 좋습니다.

<a name="custom-card-data-capture"></a>
#### 엔트리 수집

Pulse는 `Pulse::record` 메서드를 통해 임의의 "엔트리"를 기록할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

`record` 메서드의 첫 번째 인자는 기록할 엔트리의 `type`, 두 번째 인자는 집계 데이터의 그룹화를 결정짓는 `key` 입니다. 대부분의 집계 메서드에서는 집계할 `value` 지정도 필요합니다. 위 예제에서는 `$sale->amount`가 집계 값입니다. 이후 `sum` 등 집계 메서드를 추가로 호출해, Pulse가 사전에 집계된 값을 "버킷"으로 저장하게 합니다.

사용 가능한 집계 메서드는 다음과 같습니다:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> 현재 인증된 사용자 ID를 기록하는 카드 패키지를 만들 때는, 애플리케이션에서 [사용자 해석 커스터마이징](#dashboard-resolving-users)을 고려하여 반드시 `Pulse::resolveAuthenticatedUserId()` 메서드를 사용해야 합니다.

<a name="custom-card-data-retrieval"></a>
#### 집계 데이터 조회

Pulse의 `Card` Livewire 컴포넌트를 상속받으면, 대시보드에 표시할 기간에 대한 집계 데이터를 `aggregate` 메서드로 조회할 수 있습니다:

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

`aggregate` 메서드는 PHP의 `stdClass` 객체 컬렉션을 반환합니다. 각 객체에는 앞서 기록한 `key`와 요청한 집계 값이 포함되어 있습니다:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse는 특히 미리 집계된 버킷에서 데이터를 가져옵니다. 따라서 지정한 집계 값이 사전 집계된 상태여야 합니다. 가장 오래된 버킷은 기간 경계에 걸칠 수 있으므로, Pulse는 이 구간을 직접 집계해 전체 기간에 대한 정확한 값을 제공합니다.

특정 유형에 대한 전체 합계를 조회하고 싶다면 `aggregateTotal` 메서드를 사용합니다. 예를 들어, 모든 사용자 판매 총합을 집계할 수 있습니다:

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### 사용자 표시

키로 사용자 ID가 집계된 데이터와 함께 작업할 때는, `Pulse::resolveUsers` 메서드로 키를 사용자 레코드로 해석할 수 있습니다:

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

`find` 메서드는 `name`, `extra`, `avatar` 키가 포함된 객체를 반환하며, `<x-pulse::user-card>` Blade 컴포넌트에 바로 전달할 수 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### 커스텀 레코더

패키지 제작자는 데이터 수집을 설정할 수 있는 레코더 클래스를 별도로 제공할 수도 있습니다.

레코더는 애플리케이션의 `config/pulse.php` 설정 파일의 `recorders` 섹션에서 등록됩니다:

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

레코더는 `$listen` 프로퍼티에 이벤트를 지정하여 이벤트 리스닝이 가능합니다. Pulse는 리스너를 자동 등록하고, 레코더의 `record` 메서드를 호출합니다:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * 리스닝할 이벤트.
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * 배포 기록.
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