# 작업 스케줄링 (Task Scheduling)

- [소개](#introduction)
- [스케줄 정의](#defining-schedules)
    - [Artisan 명령어 스케줄링](#scheduling-artisan-commands)
    - [큐잉된 작업 스케줄링](#scheduling-queued-jobs)
    - [셸 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 빈도 옵션](#schedule-frequency-options)
    - [타임존](#timezones)
    - [작업 중첩 방지](#preventing-task-overlaps)
    - [한 서버에서만 작업 실행](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [메인터넌스 모드](#maintenance-mode)
    - [스케줄 그룹](#schedule-groups)
- [스케줄러 실행](#running-the-scheduler)
    - [1분 미만 간격 스케줄 작업](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 훅](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

과거에는 서버에서 예약 실행이 필요한 각 작업마다 직접 cron 설정 항목을 추가해야 했습니다. 하지만 이렇게 하면 작업 스케줄이 소스 제어에서 분리되어 관리가 어렵고, 기존 cron 항목을 확인하거나 추가하려면 매번 서버에 SSH로 접속해야 한다는 번거로움이 생깁니다.

Laravel의 명령어 스케줄러는 서버에서 예약 작업을 효율적으로 관리할 수 있는 새로운 방식을 제공합니다. 스케줄러를 사용하면 명령어 스케줄을 Laravel 애플리케이션 내부에서 직관적으로 정의할 수 있습니다. 스케줄러를 활용할 때는 서버에 단 하나의 cron 항목만 추가하면 충분합니다. 여러분의 작업 스케줄은 애플리케이션의 `routes/console.php` 파일 안에 보통 정의합니다.

<a name="defining-schedules"></a>
## 스케줄 정의 (Defining Schedules)

애플리케이션의 `routes/console.php` 파일에서 모든 예약 작업을 정의할 수 있습니다. 먼저 간단한 예시부터 살펴보겠습니다. 아래 예시에서는 매일 자정에 호출되는 클로저(익명함수)를 스케줄링하며, 이 클로저에서는 테이블을 비우는 데이터베이스 쿼리를 실행합니다:

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

클로저를 사용하는 것 외에도, [호출 가능한 오브젝트(invokable object)](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 이용해 예약 작업을 정의할 수도 있습니다. 호출 가능한 오브젝트는 `__invoke` 메서드를 포함하는 간단한 PHP 클래스입니다:

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

`routes/console.php` 파일을 명령어 정의 전용으로만 사용하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 이용해 예약 작업을 정의할 수 있습니다. 이 메서드는 스케줄러 인스턴스를 인자로 받는 클로저를 인자로 전달받습니다:

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

예약 작업의 전체 목록과 각 작업이 다음에 언제 실행되는지 한눈에 보고 싶다면, 다음 Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링

클로저뿐만 아니라, [Artisan 명령어](/docs/master/artisan)와 시스템 명령어도 예약 실행할 수 있습니다. 예를 들어, `command` 메서드를 사용하여 Artisan 명령어를 이름이나 클래스명으로 예약 스케줄링 할 수 있습니다.

클래스명을 통해 Artisan 명령어를 스케줄할 때에는, 명령어가 실행될 때 함께 전달할 추가 명령줄 인수 배열을 전달할 수 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
#### Artisan 클로저 명령어 스케줄링

클로저로 정의한 Artisan 명령어를 예약 실행하려면, 명령어 정의 뒤에 바로 스케줄 관련 메서드 체이닝이 가능합니다:

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

클로저 명령어에 인수를 전달해야 한다면, `schedule` 메서드로 인수를 지정해 줄 수 있습니다:

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐잉된 작업 스케줄링

`job` 메서드를 사용하면 [큐잉된 작업](/docs/master/queues)을 간편하게 예약할 수 있습니다. 이 방식은 클로저로 큐 작업을 정의하지 않아도 되므로 더 편리합니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

선택적으로 두 번째(큐 이름), 세 번째(큐 연결) 인자를 전달하여 작업이 등록될 큐와 연결을 직접 지정할 수도 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// "heartbeats" 큐, "sqs" 연결에 작업 디스패치...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 셸 명령어 스케줄링

`exec` 메서드를 이용해 운영체제에 명령어를 직접 실행할 수도 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 빈도 옵션 (Schedule Frequency Options)

실행 주기를 지정하는 예시를 앞에서 살펴보았지만, 실제로는 예약 작업의 실행 빈도를 훨씬 세밀하게 지정할 수 있습니다:

<div class="overflow-auto">

| 메서드                               | 설명                                                         |
| ------------------------------------ | ----------------------------------------------------------- |
| `->cron('* * * * *');`               | 커스텀 cron 표현식으로 작업 실행                              |
| `->everySecond();`                   | 매초 작업 실행                                               |
| `->everyTwoSeconds();`               | 2초마다 작업 실행                                            |
| `->everyFiveSeconds();`              | 5초마다 작업 실행                                            |
| `->everyTenSeconds();`               | 10초마다 작업 실행                                           |
| `->everyFifteenSeconds();`           | 15초마다 작업 실행                                           |
| `->everyTwentySeconds();`            | 20초마다 작업 실행                                           |
| `->everyThirtySeconds();`            | 30초마다 작업 실행                                           |
| `->everyMinute();`                   | 매분 작업 실행                                               |
| `->everyTwoMinutes();`                | 2분마다 작업 실행                                            |
| `->everyThreeMinutes();`              | 3분마다 작업 실행                                            |
| `->everyFourMinutes();`               | 4분마다 작업 실행                                            |
| `->everyFiveMinutes();`               | 5분마다 작업 실행                                            |
| `->everyTenMinutes();`                | 10분마다 작업 실행                                           |
| `->everyFifteenMinutes();`            | 15분마다 작업 실행                                           |
| `->everyThirtyMinutes();`             | 30분마다 작업 실행                                           |
| `->hourly();`                        | 매시각 작업 실행                                             |
| `->hourlyAt(17);`                    | 매시 17분에 작업 실행                                        |
| `->everyOddHour($minutes = 0);`      | 홀수 시각마다 작업 실행                                      |
| `->everyTwoHours($minutes = 0);`     | 2시간마다 작업 실행                                          |
| `->everyThreeHours($minutes = 0);`   | 3시간마다 작업 실행                                          |
| `->everyFourHours($minutes = 0);`    | 4시간마다 작업 실행                                          |
| `->everySixHours($minutes = 0);`     | 6시간마다 작업 실행                                          |
| `->daily();`                         | 매일 자정(00:00)에 작업 실행                                 |
| `->dailyAt('13:00');`                | 매일 13:00에 작업 실행                                       |
| `->twiceDaily(1, 13);`               | 매일 1:00, 13:00에 각각 작업 실행                            |
| `->twiceDailyAt(1, 13, 15);`         | 매일 1:15, 13:15에 각각 작업 실행                            |
| `->daysOfMonth([1, 10, 20]);`        | 지정한 월 일자에만 작업 실행                                 |
| `->weekly();`                        | 매주 일요일 00:00에 작업 실행                                |
| `->weeklyOn(1, '8:00');`             | 매주 월요일 8:00에 작업 실행                                 |
| `->monthly();`                       | 매월 1일 00:00에 작업 실행                                   |
| `->monthlyOn(4, '15:00');`           | 매월 4일 15:00에 작업 실행                                   |
| `->twiceMonthly(1, 16, '13:00');`    | 매월 1일, 16일 13:00에 작업 실행                             |
| `->lastDayOfMonth('15:00');`         | 매월 마지막 날 15:00에 작업 실행                             |
| `->quarterly();`                     | 분기별 첫날 00:00에 작업 실행                                |
| `->quarterlyOn(4, '14:00');`         | 분기별로 4일 14:00에 작업 실행                               |
| `->yearly();`                        | 매년 1월 1일 00:00에 작업 실행                               |
| `->yearlyOn(6, 1, '17:00');`         | 매년 6월 1일 17:00에 작업 실행                               |
| `->timezone('America/New_York');`    | 해당 작업의 타임존 지정                                      |

</div>

이러한 메서드는 추가 제약 조건과 조합하여, 특정 요일 등 더욱 세밀한 제어가 가능한 예약 스케줄을 생성할 수 있습니다. 예를 들어, 명령어를 매주 월요일에 실행하도록 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

// 매주 월요일 13시에 한 번 실행...
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// 평일 오전 8시부터 오후 5시까지 매시간 실행...
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```

추가적인 스케줄 제약 메서드는 아래 표를 참고하세요:

<div class="overflow-auto">

| 메서드                                   | 설명                                       |
| ---------------------------------------- | ---------------------------------------- |
| `->weekdays();`                          | 평일에만 작업 실행                        |
| `->weekends();`                          | 주말에만 작업 실행                        |
| `->sundays();`                           | 일요일에만 작업 실행                      |
| `->mondays();`                           | 월요일에만 작업 실행                      |
| `->tuesdays();`                          | 화요일에만 작업 실행                      |
| `->wednesdays();`                        | 수요일에만 작업 실행                      |
| `->thursdays();`                         | 목요일에만 작업 실행                      |
| `->fridays();`                           | 금요일에만 작업 실행                      |
| `->saturdays();`                         | 토요일에만 작업 실행                      |
| `->days(array|mixed);`                   | 지정된 요일에만 작업 실행                 |
| `->between($startTime, $endTime);`       | 특정 시작 ~ 종료 시간 사이에만 작업 실행   |
| `->unlessBetween($startTime, $endTime);` | 특정 시작 ~ 종료 시간 사이엔 작업 미실행   |
| `->when(Closure);`                       | 참/거짓 검사 결과에 따라 작업 실행        |
| `->environments($env);`                  | 지정한 환경에서만 작업 실행               |

</div>

<a name="day-constraints"></a>
#### 요일 제약 (Day Constraints)

`days` 메서드를 사용하면 특정 요일에만 작업을 실행할 수도 있습니다. 예를 들어, 매주 일요일과 수요일에 매시 작업을 실행하고 싶다면 다음과 같이 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

또는, `Illuminate\Console\Scheduling\Schedule` 클래스에서 제공하는 상수를 사용하여 좀 더 명확하게 지정할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 시간대 제약 (Between Time Constraints)

`between` 메서드는 작업 실행 시간을 하루 중 특정 시간대로 제한할 수 있습니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

반대로 `unlessBetween` 메서드를 사용하면, 지정한 시간대 사이에는 작업 실행을 제외할 수 있습니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 참/거짓 검사 제약 (Truth Test Constraints)

`when` 메서드는 특정 조건(클로저 반환 값이 true)일 때만 작업을 실행하도록 제한할 수 있습니다. 즉, 클로저가 `true`를 반환하고 다른 제약조건에도 저촉되지 않으면, 작업이 실행됩니다:

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메서드는 `when`과 반대로 동작합니다. 즉, `skip`에 전달한 클로저가 `true`를 반환하면 해당 예약 작업은 실행되지 않습니다:

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

여러 개의 `when` 메서드를 연속 체이닝하면, 모든 조건이 `true`여야 작업이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약 (Environment Constraints)

`environments` 메서드는 지정된 환경(`APP_ENV` [환경 변수](/docs/master/configuration#environment-configuration))에서만 작업이 실행되도록 할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 타임존 (Timezones)

`timezone` 메서드를 써서 예약 작업의 타임존을 직접 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

여러 예약 작업에 동일한 타임존을 반복해서 지정해야 한다면, 애플리케이션 설정 파일 `app`의 `schedule_timezone` 옵션에 기본 타임존을 설정해 둘 수도 있습니다:

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> 일부 타임존은 일광절약시간제(썸머타임)를 사용합니다. 썸머타임이 변경되는 시점에는 예약 작업이 두 번 실행되거나 아예 실행되지 않을 수도 있으니, 가능하다면 타임존 스케줄은 피하는 것을 권장합니다.

<a name="preventing-task-overlaps"></a>
### 작업 중첩 방지 (Preventing Task Overlaps)

기본적으로 예약된 작업은 이전 실행이 아직 끝나지 않았더라도 무조건 새로운 인스턴스로 실행됩니다. 이를 방지하고 싶다면 `withoutOverlapping` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

이 예제에서는, `emails:send` [Artisan 명령어](/docs/master/artisan)가 이미 실행 중인 경우 추가 실행을 막아줍니다. 작업별 실행 시간이 예측 불가할 때, 이 메서드가 특히 유용합니다.

필요하다면, 중첩 방지(락)가 만료되는 시간을 분 단위로 지정할 수도 있습니다. 기본 만료 시간은 24시간입니다:

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

내부적으로 `withoutOverlapping`은 애플리케이션의 [캐시](/docs/master/cache)를 사용해 락을 관리합니다. 만약 서버 장애 등으로 작업이 비정상적으로 중단되어 락이 계속 남아 있으면 `schedule:clear-cache` Artisan 명령어로 락을 수동 해제할 수 있습니다.

<a name="running-tasks-on-one-server"></a>
### 한 서버에서만 작업 실행 (Running Tasks on One Server)

> [!WARNING]
> 이 기능은 애플리케이션의 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, `redis` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버를 사용해야 제대로 동작합니다.

스케줄러가 여러 서버에서 동시에 실행되고 있을 때, 예약 작업이 단 한 서버에서만 실행되도록 제한할 수 있습니다. 예를 들어, 매주 금요일 밤마다 새로운 리포트를 생성하는 작업이 있을 때, 스케줄러가 3대의 워커 서버에서 실행되고 있다면 각 서버에서 작업이 중복 실행되어 리포트도 3개가 생성될 수 있습니다.

이런 상황을 방지하려면, 예약 작업을 정의할 때 `onOneServer` 메서드를 사용하세요. 이 메서드를 사용하면 해당 작업을 최초로 락(atomic lock)을 획득한 한 서버에서만 실행합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

`useCache` 메서드를 통해 스케줄러가 락 관리를 위해 사용할 캐시 스토어를 명시적으로 지정할 수도 있습니다:

```php
Schedule::useCache('database');
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업 명명하기 (Naming Single Server Jobs)

동일한 작업(잡)을 서로 다른 인수로 예약하며, 각각의 예약이 단일 서버에서만 실행되도록 하려면, 각 예약 정의마다 `name` 메서드로 고유한 이름을 지정해야 합니다:

```php
Schedule::job(new CheckUptime('https://laravel.com'))
    ->name('check_uptime:laravel.com')
    ->everyFiveMinutes()
    ->onOneServer();

Schedule::job(new CheckUptime('https://vapor.laravel.com'))
    ->name('check_uptime:vapor.laravel.com')
    ->everyFiveMinutes()
    ->onOneServer();
```

마찬가지로, 클로저로 예약한 작업도 단일 서버에서만 실행하려면 반드시 이름을 부여해야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업 (Background Tasks)

기본적으로 동시에 예약된 여러 작업은 `schedule` 메서드에 정의된 순서에 따라 하나씩 순차적으로 실행됩니다. 작업 중 일부가 오래 걸리면 나머지 작업이 예상보다 늦게 시작될 수 있습니다. 여러 작업을 백그라운드로 실행해 동시에 처리하고 싶을 때는 `runInBackground` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> `runInBackground`는 오직 `command`와 `exec` 메서드를 이용한 작업에만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 메인터넌스 모드 (Maintenance Mode)

애플리케이션이 [메인터넌스 모드](/docs/master/configuration#maintenance-mode)일 때는, 완료되지 않은 유지보수와 충돌이 생길 수 있으므로 예약 작업이 실행되지 않습니다. 그러나, 메인터넌스 모드에서도 특정 작업만 강제 실행해야 한다면, 예약 작업 정의 시 `evenInMaintenanceMode` 메서드를 추가하면 됩니다:

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="schedule-groups"></a>
### 스케줄 그룹 (Schedule Groups)

여러 작업을 비슷한 설정으로 예약할 때마다 동일한 설정을 반복적으로 작성하는 것은 번거롭고 오류를 유발할 수 있습니다. 이때는 Laravel의 작업 그룹(group) 기능을 사용하면, 여러 작업을 묶어서 한꺼번에 일관된 설정을 지정할 수 있습니다.

작업 그룹을 만들려면, 먼저 공통 설정 메서드들을 체이닝하고 `group` 메서드를 호출합니다. `group` 메서드의 인자로는 여러 작업을 정의하는 클로저를 전달합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::daily()
    ->onOneServer()
    ->timezone('America/New_York')
    ->group(function () {
        Schedule::command('emails:send --force');
        Schedule::command('emails:prune');
    });
```

<a name="running-the-scheduler"></a>
## 스케줄러 실행 (Running the Scheduler)

이제 예약 작업을 정의하는 방법을 배웠으니, 서버에서 실제로 이 작업들을 어떻게 실행하는지 알아보겠습니다. `schedule:run` Artisan 명령어는 모든 예약 작업을 평가하여, 서버의 현재 시간 기준으로 바로 실행이 필요한 작업만 수행합니다.

즉, Laravel의 스케줄러를 사용할 때는 오직 하나의 cron 설정 항목만 서버에 추가하면 충분합니다. 예를 들어 다음과 같이 `schedule:run` 명령어가 매분 실행되도록 합니다. 서버에 cron 항목을 추가하는 방법이 익숙하지 않다면, [Laravel Cloud](https://cloud.laravel.com) 같은 관리형 플랫폼을 활용하여 예약 작업 실행을 쉽게 할 수 있습니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만 간격 스케줄 작업 (Sub-Minute Scheduled Tasks)

대부분의 운영체제에서 cron 작업은 1분에 한 번씩만 실행할 수 있습니다. 하지만 Laravel의 스케줄러는 더 짧은 간격으로(심지어 매초 단위로도) 작업을 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

애플리케이션에 1분 미만 간격으로 실행되는 작업이 있을 경우, `schedule:run` 명령어는 한 번 호출된 뒤 즉시 종료되는 대신 현재 분이 끝날 때까지 계속 실행됩니다. 그 결과, 해당 1분 동안 모든 1분 미만 예약 작업이 정해진 빈도로 정확하게 호출될 수 있습니다.

1분 미만 작업이 이전 실행보다 오래 걸리면, 다음 작업의 실행이 지연될 수 있습니다. 그래서 이런 작업은 실제 처리를 직접 실행하지 않고, 큐잉된 잡이나 백그라운드 명령어로 처리하는 것을 권장합니다:

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### 1분 미만 작업 중단하기

1분 미만 간격 작업이 정의되어 있을 때는, `schedule:run` 명령어가 해당 분 동안 계속 실행되는 특성상, 애플리케이션을 배포할 때 이 명령이 계속 실행 중일 수 있습니다. 이미 실행 중인 `schedule:run` 프로세스가 있으면, 해당 프로세스가 끝날 때까지는 이전 코드로 작업을 실행하게 됩니다.

이럴 때는 배포 스크립트에서 `schedule:interrupt` 명령어를 써서 진행 중인 `schedule:run` 명령어를 강제 중단할 수 있습니다. 배포 종료 후 아래 명령어를 실행하세요:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행 (Running the Scheduler Locally)

일반적으로 로컬 개발 환경에서는 cron 항목을 추가하지 않습니다. 대신, `schedule:work` Artisan 명령어를 사용하여 스케줄러를 포그라운드에서 실행할 수 있습니다. 이 명령어는 사용자가 직접 중단할 때까지 1분마다 예약 작업을 평가합니다. 1분 미만 예약 작업이 있는 경우, 마찬가지로 매분마다 계속하여 반복 실행됩니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력 (Task Output)

Laravel 스케줄러는 예약 작업에서 생성된 출력을 쉽게 다룰 수 있는 여러 방법을 제공합니다. 우선, `sendOutputTo` 메서드를 사용하여 작업 출력을 파일로 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

출력을 파일에 덮어쓰기 방식이 아닌 추가(append)하고자 할 때는 `appendOutputTo` 메서드를 사용합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드를 사용하면, 작업 출력을 원하는 이메일 주소로 전송할 수 있습니다. 단, 작업 출력 이메일 전송 전에 [이메일 서비스](/docs/master/mail)를 반드시 설정해야 합니다:

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

만약, Artisan 혹은 시스템 명령어가 정상적으로 종료되지 않은(즉, 종료 코드가 0이 아님) 경우에만 출력 내용을 메일로 전송하고 싶다면, `emailOutputOnFailure` 메서드를 사용하세요:

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command` 및 `exec` 메서드에서 예약된 작업에만 사용할 수 있습니다.

<a name="task-hooks"></a>
## 작업 훅 (Task Hooks)

`before`와 `after` 메서드를 사용해 예약 작업 실행 전후에 특정 코드를 실행할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // 작업 실행 직전 수행될 코드...
    })
    ->after(function () {
        // 작업 실행 후 수행될 코드...
    });
```

`onSuccess`와 `onFailure` 메서드를 통해, 예약 작업이 성공(정상 종료)하거나 실패(비정상 종료)할 경우에만 특정 코드를 실행할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // 작업이 성공했을 때...
    })
    ->onFailure(function () {
        // 작업이 실패했을 때...
    });
```

명령어로부터 출력 결과를 받을 수 있다면, `after`, `onSuccess`, `onFailure` 훅에서 클로저 인자의 타입힌트로 `Illuminate\Support\Stringable`을 지정하여 `$output`을 직접 사용할 수 있습니다:

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // 작업이 성공했을 때 출력 결과 활용...
    })
    ->onFailure(function (Stringable $output) {
        // 작업이 실패했을 때 출력 결과 활용...
    });
```

<a name="pinging-urls"></a>
#### URL 핑 (Pinging URLs)

`pingBefore`와 `thenPing` 메서드를 사용하면 작업 실행 전후에 지정된 URL로 핑을 보내 외부 서비스(예: [Envoyer](https://envoyer.io))에 작업 시작/완료 상태를 알릴 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

작업 성공 시 또는 실패 시에만 특정 URL로 핑을 보내고 싶다면, `pingOnSuccess`, `pingOnFailure` 메서드를 사용할 수 있습니다. 실패란 Artisan 또는 시스템 명령어 종료 코드가 0이 아닐 때를 의미합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 메서드는 특정 조건이 `true`일 때만 지정한 URL로 핑을 보냅니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBeforeIf($condition, $url)
    ->thenPingIf($condition, $url);

Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccessIf($condition, $successUrl)
    ->pingOnFailureIf($condition, $failureUrl);
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 예약 작업 스케줄 프로세스 중 여러 [이벤트](/docs/master/events)를 디스패치(dispatch)합니다. 다음 이벤트에 대해 [리스너(listener)](/docs/master/events)를 정의할 수 있습니다:

<div class="overflow-auto">

| 이벤트명                                                    |
| ----------------------------------------------------------- |
| `Illuminate\Console\Events\ScheduledTaskStarting`           |
| `Illuminate\Console\Events\ScheduledTaskFinished`           |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped`            |
| `Illuminate\Console\Events\ScheduledTaskFailed`             |

</div>
