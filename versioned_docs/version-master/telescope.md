# Laravel Telescope (Laravel Telescope)

- [소개](#introduction)
- [설치](#installation)
    - [로컬 전용 설치](#local-only-installation)
    - [설정](#configuration)
    - [데이터 정리](#data-pruning)
    - [대시보드 접근 권한](#dashboard-authorization)
- [Telescope 업그레이드](#upgrading-telescope)
- [필터링](#filtering)
    - [엔트리 필터링](#filtering-entries)
    - [배치 필터링](#filtering-batches)
- [태깅](#tagging)
- [사용 가능한 워처](#available-watchers)
    - [배치 워처](#batch-watcher)
    - [캐시 워처](#cache-watcher)
    - [명령어 워처](#command-watcher)
    - [덤프 워처](#dump-watcher)
    - [이벤트 워처](#event-watcher)
    - [예외 워처](#exception-watcher)
    - [Gate 워처](#gate-watcher)
    - [HTTP 클라이언트 워처](#http-client-watcher)
    - [Job 워처](#job-watcher)
    - [로그 워처](#log-watcher)
    - [메일 워처](#mail-watcher)
    - [모델 워처](#model-watcher)
    - [알림 워처](#notification-watcher)
    - [쿼리 워처](#query-watcher)
    - [Redis 워처](#redis-watcher)
    - [요청 워처](#request-watcher)
    - [스케줄 워처](#schedule-watcher)
    - [뷰 워처](#view-watcher)
- [사용자 아바타 표시](#displaying-user-avatars)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 환경에서 Laravel 개발을 도울 수 있는 매우 유용한 도구입니다. Telescope는 애플리케이션에 들어오는 요청, 예외, 로그 엔트리, 데이터베이스 쿼리, 큐잉된 작업, 메일, 알림, 캐시 동작, 예약된 작업, 변수 덤프 등 다양한 정보를 깊이 있게 살펴볼 수 있도록 도와줍니다.

<img src="https://laravel.com/img/docs/telescope-example.png" />

<a name="installation"></a>
## 설치 (Installation)

Composer 패키지 관리자를 사용하여 Laravel 프로젝트에 Telescope를 설치할 수 있습니다.

```shell
composer require laravel/telescope
```

Telescope를 설치한 후, `telescope:install` Artisan 명령어를 실행하여 에셋과 마이그레이션을 게시합니다. 또한, Telescope에서 데이터를 저장하는 데 필요한 테이블을 생성하기 위해 `migrate` 명령어도 실행해야 합니다.

```shell
php artisan telescope:install

php artisan migrate
```

설치가 완료되면 `/telescope` 경로를 통해 Telescope 대시보드에 접근할 수 있습니다.

<a name="local-only-installation"></a>
### 로컬 전용 설치

Telescope를 오직 로컬 개발에만 사용할 계획이라면, 설치 시 `--dev` 플래그를 사용할 수 있습니다.

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

`telescope:install`을 실행한 후, 애플리케이션의 `bootstrap/providers.php` 설정 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거해야 합니다. 대신, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 안에서 Telescope의 서비스 프로바이더를 직접 등록해 주세요. 아래 예시는 현재 환경이 `local`일 때만 Telescope 관련 프로바이더를 등록하도록 합니다.

```php
/**
 * Register any application services.
 */
public function register(): void
{
    if ($this->app->environment('local') && class_exists(\Laravel\Telescope\TelescopeServiceProvider::class)) {
        $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
        $this->app->register(TelescopeServiceProvider::class);
    }
}
```

또한, Telescope 패키지가 [자동 발견](/docs/master/packages#package-discovery)되지 않도록 `composer.json` 파일에 아래 내용을 추가해야 합니다.

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "laravel/telescope"
        ]
    }
},
```

<a name="configuration"></a>
### 설정

Telescope의 에셋 게시 후, 기본 설정 파일은 `config/telescope.php`에 위치합니다. 이 설정 파일에서 [워처 옵션](#available-watchers) 등을 구성할 수 있습니다. 각 설정 항목에는 그 목적에 대한 설명이 포함되어 있으므로, 이 파일의 내용을 꼼꼼히 확인해 보시기 바랍니다.

원한다면, 다음과 같이 `enabled` 설정을 사용하여 Telescope의 데이터 수집을 완전히 비활성화할 수 있습니다.

```php
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
### 데이터 정리

정리 작업을 하지 않으면 `telescope_entries` 테이블에 레코드가 매우 빠르게 쌓일 수 있습니다. 이를 방지하려면, `telescope:prune` Artisan 명령어를 [스케줄러](/docs/master/scheduling)에 등록하여 매일 자동 실행되도록 해야 합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune')->daily();
```

기본적으로 24시간이 지난 모든 엔트리는 정리됩니다. 명령어 실행 시 `hours` 옵션을 사용하여 Telescope 데이터의 보관 기간을 지정할 수 있습니다. 예를 들어, 다음 명령어는 48시간 이전에 생성된 모든 레코드를 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
### 대시보드 접근 권한

Telescope 대시보드는 `/telescope` 경로를 통해 접근할 수 있습니다. 기본적으로 대시보드는 `local` 환경에서만 접근할 수 있습니다. `app/Providers/TelescopeServiceProvider.php` 파일 내부에 [인가 게이트](/docs/master/authorization#gates) 정의가 있으며, 이 게이트는 **비로컬** 환경에서 Telescope 접근을 제어합니다. 필요에 따라 이 게이트를 수정하여 Telescope 설치에 대한 접근을 제한할 수 있습니다.

```php
use App\Models\User;

/**
 * Register the Telescope gate.
 *
 * This gate determines who can access Telescope in non-local environments.
 */
protected function gate(): void
{
    Gate::define('viewTelescope', function (User $user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

> [!WARNING]
> 실제 운영 환경에서는 반드시 `APP_ENV` 환경 변수를 `production`으로 변경해야 합니다. 그렇지 않으면 Telescope 대시보드가 외부에 공개됩니다.

<a name="upgrading-telescope"></a>
## Telescope 업그레이드 (Upgrading Telescope)

Telescope의 새로운 주요 버전으로 업그레이드할 때는, [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 반드시 꼼꼼히 확인해야 합니다.

또한, Telescope의 새 버전으로 업그레이드할 때마다 Telescope의 에셋을 다시 게시해야 합니다.

```shell
php artisan telescope:publish
```

항상 최신 에셋을 유지하고 향후 업그레이드 시 문제를 예방하려면, 애플리케이션의 `composer.json` 파일의 `post-update-cmd` 스크립트에 `vendor:publish --tag=laravel-assets` 명령어를 추가할 수 있습니다.

```json
{
    "scripts": {
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=laravel-assets --ansi --force"
        ]
    }
}
```

<a name="filtering"></a>
## 필터링 (Filtering)

<a name="filtering-entries"></a>
### 엔트리 필터링

Telescope가 기록하는 데이터를 필터링하려면, `App\Providers\TelescopeServiceProvider` 클래스에 정의된 `filter` 클로저를 사용할 수 있습니다. 기본적으로 이 클로저는 `local` 환경에서는 모든 데이터를 기록하며, 그 외 환경에서는 예외, 실패한 작업, 예약된 작업, 모니터링된 태그가 있는 데이터만 기록합니다.

```php
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filter(function (IncomingEntry $entry) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entry->isReportableException() ||
            $entry->isFailedJob() ||
            $entry->isScheduledTask() ||
            $entry->isSlowQuery() ||
            $entry->hasMonitoredTag();
    });
}
```

<a name="filtering-batches"></a>
### 배치 필터링

`filter` 클로저가 개별 엔트리 데이터를 필터링하는 반면, `filterBatch` 메서드를 사용하면 하나의 요청 또는 콘솔 명령어에서 발생하는 모든 데이터를 대상으로 필터링할 수 있습니다. 클로저가 `true`를 반환하면, 해당 요청 또는 명령어의 모든 엔트리가 Telescope에 기록됩니다.

```php
use Illuminate\Support\Collection;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filterBatch(function (Collection $entries) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entries->contains(function (IncomingEntry $entry) {
            return $entry->isReportableException() ||
                $entry->isFailedJob() ||
                $entry->isScheduledTask() ||
                $entry->isSlowQuery() ||
                $entry->hasMonitoredTag();
            });
    });
}
```

<a name="tagging"></a>
## 태깅 (Tagging)

Telescope에서는 "태그"를 기준으로 엔트리를 검색할 수 있습니다. 일반적으로 태그는 Eloquent 모델 클래스명이나 인증된 사용자 ID와 같이 Telescope가 자동으로 엔트리마다 추가하는 정보를 의미합니다. 간혹, 직접 지정한 커스텀 태그를 추가하고 싶을 때가 있습니다. 이럴 때는 `Telescope::tag` 메서드를 사용할 수 있습니다. 이 메서드는 태그 배열을 반환하는 클로저를 인수로 받으며, 해당 태그들은 Telescope가 자동으로 추가하는 태그와 합쳐집니다. 보통 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 안에서 호출합니다.

```php
use Laravel\Telescope\EntryType;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::tag(function (IncomingEntry $entry) {
        return $entry->type === EntryType::REQUEST
            ? ['status:'.$entry->content['response_status']]
            : [];
    });
}
```

<a name="available-watchers"></a>
## 사용 가능한 워처 (Available Watchers)

Telescope의 "워처(watcher)"는 요청 또는 콘솔 명령 실행 시 애플리케이션의 다양한 데이터를 수집합니다. 사용하고 싶은 워처 목록은 `config/telescope.php` 설정 파일에서 원하는 대로 구성할 수 있습니다.

```php
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    // ...
],
```

특정 워처는 추가 커스터마이즈 옵션도 제공합니다.

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 100,
    ],
    // ...
],
```

<a name="batch-watcher"></a>
### 배치 워처

배치 워처는 큐에 등록된 [배치 작업](/docs/master/queues#job-batching)에 관한 정보(작업 및 연결 정보 등)를 기록합니다.

<a name="cache-watcher"></a>
### 캐시 워처

캐시 워처는 캐시 키를 조회(hit), 미스(miss), 갱신, 삭제(forget)했을 때의 데이터를 기록합니다.

<a name="command-watcher"></a>
### 명령어 워처

명령어 워처는 Artisan 명령어 실행 시 인수, 옵션, 종료 코드, 출력 내용을 기록합니다. 특정 명령어가 워처에 의해 기록되는 것을 제외하고 싶다면, `config/telescope.php` 파일의 `ignore` 옵션에 명령어를 지정할 수 있습니다.

```php
'watchers' => [
    Watchers\CommandWatcher::class => [
        'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
        'ignore' => ['key:generate'],
    ],
    // ...
],
```

<a name="dump-watcher"></a>
### 덤프 워처

덤프 워처는 Telescope 내에서 변수 덤프를 기록하고 표시합니다. Laravel을 사용할 때, 전역 `dump` 함수를 통해 변수를 덤프할 수 있습니다. 단, 웹 브라우저에서 덤프 워처 탭이 열려 있어야만 해당 덤프가 기록되며, 그렇지 않으면 워처가 이를 무시합니다.

<a name="event-watcher"></a>
### 이벤트 워처

이벤트 워처는 애플리케이션에서 디스패치된 [이벤트](/docs/master/events)의 페이로드(payload), 리스너, 브로드캐스트 데이터를 기록합니다. Laravel 프레임워크 내부의 이벤트는 이벤트 워처의 기록 대상에서 제외됩니다.

<a name="exception-watcher"></a>
### 예외 워처

예외 워처는 애플리케이션에서 발생한 보고 가능한 예외의 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
### Gate 워처

Gate 워처는 애플리케이션에서 수행된 [게이트 및 정책](/docs/master/authorization) 체크의 데이터와 결과를 기록합니다. 특정 ability가 워처에 기록되는 것을 제외하고 싶다면, `config/telescope.php` 파일의 `ignore_abilities` 옵션에 해당 ability를 지정할 수 있습니다.

```php
'watchers' => [
    Watchers\GateWatcher::class => [
        'enabled' => env('TELESCOPE_GATE_WATCHER', true),
        'ignore_abilities' => ['viewNova'],
    ],
    // ...
],
```

<a name="http-client-watcher"></a>
### HTTP 클라이언트 워처

HTTP 클라이언트 워처는 애플리케이션에서 발생한 [HTTP 클라이언트 요청](/docs/master/http-client)을 기록합니다.

<a name="job-watcher"></a>
### Job 워처

Job 워처는 애플리케이션에서 디스패치된 [작업](/docs/master/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 워처

로그 워처는 애플리케이션에서 기록된 [로그 데이터](/docs/master/logging)를 저장합니다.

기본적으로 Telescope는 `error` 이상의 로그 레벨만 기록합니다. 하지만, 애플리케이션의 `config/telescope.php` 설정 파일의 `level` 옵션을 수정하여 기록 범위를 변경할 수 있습니다.

```php
'watchers' => [
    Watchers\LogWatcher::class => [
        'enabled' => env('TELESCOPE_LOG_WATCHER', true),
        'level' => 'debug',
    ],

    // ...
],
```

<a name="mail-watcher"></a>
### 메일 워처

메일 워처를 사용하면, 애플리케이션에서 발송한 [이메일](/docs/master/mail)의 미리보기와 관련 데이터를 브라우저 내에서 확인할 수 있으며, `.eml` 파일로도 다운로드할 수 있습니다.

<a name="model-watcher"></a>
### 모델 워처

모델 워처는 Eloquent [모델 이벤트](/docs/master/eloquent#events)가 디스패치될 때 모델의 변경 사항을 기록합니다. 기록할 모델 이벤트 종류는 워처의 `events` 옵션으로 지정할 수 있습니다.

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    // ...
],
```

특정 요청 처리 과정에서 하이드레이트(hydrated)된 모델의 개수도 기록하고 싶다면, `hydrations` 옵션을 활성화하세요.

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
        'hydrations' => true,
    ],
    // ...
],
```

<a name="notification-watcher"></a>
### 알림 워처

알림 워처는 애플리케이션에서 발송된 모든 [알림](/docs/master/notifications)을 기록합니다. 알림이 이메일을 발생시키고 메일 워처가 활성화되어 있다면, 해당 이메일도 메일 워처 화면에서 미리보기로 확인할 수 있습니다.

<a name="query-watcher"></a>
### 쿼리 워처

쿼리 워처는 애플리케이션에서 실행된 모든 쿼리의 원본 SQL, 바인딩, 실행 시간을 기록합니다. 워처는 100ms보다 느린 쿼리에 `slow` 태그를 자동으로 부여합니다. 느린 쿼리 임계값은 워처의 `slow` 옵션으로 변경할 수 있습니다.

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 50,
    ],
    // ...
],
```

<a name="redis-watcher"></a>
### Redis 워처

Redis 워처는 애플리케이션에서 실행된 모든 [Redis](/docs/master/redis) 명령을 기록합니다. Redis를 캐시 목적으로 사용하는 경우, 캐시 명령도 Redis 워처를 통해 기록됩니다.

<a name="request-watcher"></a>
### 요청 워처

요청 워처는 요청, 헤더, 세션, 응답 데이터 등 애플리케이션이 처리한 각 요청에 대한 정보를 기록합니다. 기록할 응답 데이터의 크기는 `size_limit`(킬로바이트 단위) 옵션으로 제한할 수 있습니다.

```php
'watchers' => [
    Watchers\RequestWatcher::class => [
        'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
        'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
    ],
    // ...
],
```

<a name="schedule-watcher"></a>
### 스케줄 워처

스케줄 워처는 애플리케이션에서 실행된 [예약된 작업](/docs/master/scheduling)의 명령어 및 출력을 기록합니다.

<a name="view-watcher"></a>
### 뷰 워처

뷰 워처는 [뷰](/docs/master/views) 파일의 이름, 경로, 데이터, 렌더링에 사용된 "컴포저" 정보를 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시 (Displaying User Avatars)

Telescope 대시보드는 엔트리 저장 당시 인증된 사용자의 아바타를 표시합니다. 기본적으로 Telescope는 Gravatar 웹 서비스를 통해 아바타를 가져옵니다. 하지만, 아바타 URL을 직접 지정하고 싶다면 `App\Providers\TelescopeServiceProvider` 클래스에서 콜백을 등록할 수 있습니다. 이 콜백은 사용자 ID와 이메일을 받아서 해당 사용자의 아바타 이미지 URL을 반환해야 합니다.

```php
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    // ...

    Telescope::avatar(function (?string $id, ?string $email) {
        return ! is_null($id)
            ? '/avatars/'.User::find($id)->avatar_path
            : '/generic-avatar.jpg';
    });
}
```
