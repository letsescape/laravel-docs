<!-- # Task Scheduling -->
# Task Scheduling

- [Introduction](#introduction)
- [Defining Schedules](#defining-schedules)
    - [Scheduling Artisan Commands](#scheduling-artisan-commands)
    - [Scheduling Queued Jobs](#scheduling-queued-jobs)
    - [Scheduling Shell Commands](#scheduling-shell-commands)
    - [Schedule Frequency Options](#schedule-frequency-options)
    - [Timezones](#timezones)
    - [Preventing Task Overlaps](#preventing-task-overlaps)
    - [Running Tasks on One Server](#running-tasks-on-one-server)
    - [Background Tasks](#background-tasks)
    - [Maintenance Mode](#maintenance-mode)
    - [Schedule Groups](#schedule-groups)
- [Running the Scheduler](#running-the-scheduler)
    - [Sub-Minute Scheduled Tasks](#sub-minute-scheduled-tasks)
    - [Running the Scheduler Locally](#running-the-scheduler-locally)
- [Task Output](#task-output)
- [Task Hooks](#task-hooks)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In the past, you may have written a cron configuration entry for each task you needed to schedule on your server. However, this can quickly become a pain because your task schedule is no longer in source control and you must SSH into your server to view your existing cron entries or add additional entries. -->
예전에는 서버에서 실행할 각 작업마다 크론(cron) 설정을 직접 작성했을 것입니다. 하지만 이 방식은 곧 번거로워집니다. 작업 스케줄이 더 이상 소스 관리 하에 있지 않게 되고, 기존 크론 항목을 확인하거나 새로운 작업을 추가하려면 서버에 SSH로 접속해야 하기 때문입니다.

<!-- Laravel's command scheduler offers a fresh approach to managing scheduled tasks on your server. The scheduler allows you to fluently and expressively define your command schedule within your Laravel application itself. When using the scheduler, only a single cron entry is needed on your server. Your task schedule is typically defined in your application's `routes/console.php` file. -->
Laravel의 명령어 스케줄러는 서버의 예약 작업을 더욱 손쉽게 관리할 수 있도록 새로운 방식을 제공합니다. 이 스케줄러를 사용하면, Laravel 애플리케이션 내에서 명령어 스케줄을 유연하게 정의할 수 있습니다. 스케줄러를 사용할 때는 서버에 단 하나의 크론 항목만 등록하면 되며, 실제 예약 작업들은 애플리케이션의 `routes/console.php` 파일에서 보통 정의합니다.

<a name="defining-schedules"></a>
<!-- ## Defining Schedules -->
## Defining Schedules

<!-- You may define all of your scheduled tasks in your application's `routes/console.php` file. To get started, let's take a look at an example. In this example, we will schedule a closure to be called every day at midnight. Within the closure we will execute a database query to clear a table: -->
모든 예약 작업은 애플리케이션의 `routes/console.php` 파일에서 정의할 수 있습니다. 우선 간단한 예제를 살펴보겠습니다. 아래 예제에서는 매일 자정마다 호출되는 클로저를 예약하고, 이 클로저에서 데이터베이스 쿼리를 실행하여 테이블을 비웁니다:

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

<!-- In addition to scheduling using closures, you may also schedule [invokable objects](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke). Invokable objects are simple PHP classes that contain an `__invoke` method: -->
클로저를 사용한 예약 외에도, [invokable objects](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)도 예약할 수 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 가진 간단한 PHP 클래스입니다:

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

<!-- If you prefer to reserve your `routes/console.php` file for command definitions only, you may use the `withSchedule` method in your application's `bootstrap/app.php` file to define your scheduled tasks. This method accepts a closure that receives an instance of the scheduler: -->
만약 `routes/console.php` 파일을 명령어 정의로만 사용하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 사용하여 예약 작업을 정의할 수 있습니다. 이 메서드는 스케줄러 인스턴스를 전달하는 클로저를 인자로 받습니다:

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

<!-- If you would like to view an overview of your scheduled tasks and the next time they are scheduled to run, you may use the `schedule:list` Artisan command: -->
예약된 작업과 다음 실행 예정 시간을 한눈에 확인하고 싶다면 `schedule:list` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
<!-- ### Scheduling Artisan Commands -->
### Scheduling Artisan Commands

<!-- In addition to scheduling closures, you may also schedule [Artisan commands](/docs/master/artisan) and system commands. For example, you may use the `command` method to schedule an Artisan command using either the command's name or class. -->
클로저뿐 아니라, [Artisan commands](/docs/master/artisan)와 시스템 명령어도 예약할 수 있습니다. 예를 들어, `command` 메서드를 사용해 명령어의 이름 또는 클래스명을 전달하여 Artisan 명령어를 스케줄링할 수 있습니다.

<!-- When scheduling Artisan commands using the command's class name, you may pass an array of additional command-line arguments that should be provided to the command when it is invoked: -->
명령어의 클래스명을 사용하여 Artisan 명령어를 예약할 때는, 명령어 실행 시에 제공할 추가 커맨드 라인 인수들을 배열 형태로 전달할 수 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
<!-- #### Scheduling Artisan Closure Commands -->
#### Scheduling Artisan Closure Commands

<!-- If you want to schedule an Artisan command defined by a closure, you may chain the scheduling related methods after the command's definition: -->
클로저로 정의된 Artisan 명령어를 예약하려면, 명령어 정의 후 바로 스케줄 관련 메서드를 체이닝하세요:

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

<!-- If you need to pass arguments to the closure command, you may provide them to the `schedule` method: -->
클로저 명령어에 인수를 전달해야 한다면, `schedule` 메서드에 인수 배열을 넘겨 사용할 수 있습니다:

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
<!-- ### Scheduling Queued Jobs -->
### Scheduling Queued Jobs

<!-- The `job` method may be used to schedule a [queued job](/docs/master/queues). This method provides a convenient way to schedule queued jobs without using the `call` method to define closures to queue the job: -->
`job` 메서드를 사용하면 [queued job](/docs/master/queues)을 쉽게 예약할 수 있습니다. 이 방법을 이용하면, 작업을 큐에 넣기 위해 `call` 메서드로 클로저를 정의하는 번거로움 없이 간편하게 예약할 수 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

<!-- Optional second and third arguments may be provided to the `job` method which specifies the queue name and queue connection that should be used to queue the job: -->
추가로 `job` 메서드의 두 번째와 세 번째 인수로 큐 이름과 큐 연결명을 지정할 수 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// Dispatch the job to the "heartbeats" queue on the "sqs" connection...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
<!-- ### Scheduling Shell Commands -->
### Scheduling Shell Commands

<!-- The `exec` method may be used to issue a command to the operating system: -->
`exec` 메서드는 운영체제에 명령어를 직접 실행시킬 수 있게 해줍니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
<!-- ### Schedule Frequency Options -->
### Schedule Frequency Options

<!-- We've already seen a few examples of how you may configure a task to run at specified intervals. However, there are many more task schedule frequencies that you may assign to a task: -->
앞에서 특정 주기로 작업을 실행하도록 설정하는 방법을 몇 가지 살펴보았습니다. 하지만 더욱 다양한 예약주기 메서드들이 존재합니다:

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 메서드                                  | 설명                                                      |
| -------------------------------------- | --------------------------------------------------------- |
| `->cron('* * * * *');`                 | 커스텀 크론 스케줄로 작업을 실행합니다.                       |
| `->everySecond();`                     | 매초마다 작업을 실행합니다.                                   |
| `->everyTwoSeconds();`                 | 2초마다 작업을 실행합니다.                                    |
| `->everyFiveSeconds();`                | 5초마다 작업을 실행합니다.                                    |
| `->everyTenSeconds();`                 | 10초마다 작업을 실행합니다.                                   |
| `->everyFifteenSeconds();`             | 15초마다 작업을 실행합니다.                                   |
| `->everyTwentySeconds();`              | 20초마다 작업을 실행합니다.                                   |
| `->everyThirtySeconds();`              | 30초마다 작업을 실행합니다.                                   |
| `->everyMinute();`                     | 매 분마다 작업을 실행합니다.                                   |
| `->everyTwoMinutes();`                 | 2분마다 작업을 실행합니다.                                    |
| `->everyThreeMinutes();`               | 3분마다 작업을 실행합니다.                                    |
| `->everyFourMinutes();`                | 4분마다 작업을 실행합니다.                                    |
| `->everyFiveMinutes();`                | 5분마다 작업을 실행합니다.                                    |
| `->everyTenMinutes();`                 | 10분마다 작업을 실행합니다.                                   |
| `->everyFifteenMinutes();`             | 15분마다 작업을 실행합니다.                                   |
| `->everyThirtyMinutes();`              | 30분마다 작업을 실행합니다.                                   |
| `->hourly();`                          | 1시간마다 작업을 실행합니다.                                   |
| `->hourlyAt(17);`                      | 매 시간 17분에 작업을 실행합니다.                              |
| `->everyOddHour($minutes = 0);`        | 홀수 시간마다 작업을 실행합니다.                               |
| `->everyTwoHours($minutes = 0);`       | 2시간마다 작업을 실행합니다.                                   |
| `->everyThreeHours($minutes = 0);`     | 3시간마다 작업을 실행합니다.                                   |
| `->everyFourHours($minutes = 0);`      | 4시간마다 작업을 실행합니다.                                   |
| `->everySixHours($minutes = 0);`       | 6시간마다 작업을 실행합니다.                                   |
| `->daily();`                           | 매일 자정에 작업을 실행합니다.                                 |
| `->dailyAt('13:00');`                  | 매일 13:00에 작업을 실행합니다.                               |
| `->twiceDaily(1, 13);`                 | 매일 1:00, 13:00에 작업을 실행합니다.                          |
| `->twiceDailyAt(1, 13, 15);`           | 매일 1:15, 13:15에 작업을 실행합니다.                          |
| `->daysOfMonth([1, 10, 20]);`          | 매월 지정된 날짜에 작업을 실행합니다.                           |
| `->weekly();`                          | 매주 일요일 00:00에 작업을 실행합니다.                          |
| `->weeklyOn(1, '8:00');`               | 매주 월요일 8:00에 작업을 실행합니다.                           |
| `->monthly();`                         | 매월 1일 00:00에 작업을 실행합니다.                             |
| `->monthlyOn(4, '15:00');`             | 매월 4일 15:00에 작업을 실행합니다.                             |
| `->twiceMonthly(1, 16, '13:00');`      | 매월 1일, 16일 13:00에 작업을 실행합니다.                        |
| `->lastDayOfMonth('15:00');`           | 매월 마지막 날 15:00에 작업을 실행합니다.                        |
| `->quarterly();`                       | 분기 첫날 00:00에 작업을 실행합니다.                             |
| `->quarterlyOn(4, '14:00');`           | 매 분기 4일 14:00에 작업을 실행합니다.                           |
| `->yearly();`                          | 매년 1월 1일 00:00에 작업을 실행합니다.                          |
| `->yearlyOn(6, 1, '17:00');`           | 매년 6월 1일 17:00에 작업을 실행합니다.                          |
| `->timezone('America/New_York');`      | 작업의 타임존을 설정합니다.                                      |

<!-- </div> -->
</div>

<!-- These methods may be combined with additional constraints to create even more finely tuned schedules that only run on certain days of the week. For example, you may schedule a command to run weekly on Monday: -->
이러한 메서드들은 추가 제약 조건과 조합하여, 특정 요일에만 실행되는 세밀한 스케줄을 만들 수 있습니다. 예를 들어, 매주 월요일에 명령어가 실행되도록 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

// Run once per week on Monday at 1 PM...
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// Run hourly from 8 AM to 5 PM on weekdays...
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```

<!-- A list of additional schedule constraints may be found below: -->
아래는 추가적인 스케줄 제약 조건의 목록입니다:

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 메서드                                       | 설명                                                 |
| -------------------------------------------- | --------------------------------------------------- |
| `->weekdays();`                              | 평일(월~금요일)에만 작업을 제한합니다.                 |
| `->weekends();`                              | 주말(토,일)에만 작업을 제한합니다.                    |
| `->sundays();`                               | 일요일에만 작업을 제한합니다.                         |
| `->mondays();`                               | 월요일에만 작업을 제한합니다.                         |
| `->tuesdays();`                              | 화요일에만 작업을 제한합니다.                         |
| `->wednesdays();`                            | 수요일에만 작업을 제한합니다.                         |
| `->thursdays();`                             | 목요일에만 작업을 제한합니다.                         |
| `->fridays();`                               | 금요일에만 작업을 제한합니다.                         |
| `->saturdays();`                             | 토요일에만 작업을 제한합니다.                         |
| `->days(array\|mixed);`                      | 지정한 요일에만 작업을 제한합니다.                     |
| `->between($startTime, $endTime);`           | 시작~종료 시간 사이에만 작업을 실행합니다.             |
| `->unlessBetween($startTime, $endTime);`     | 지정 시간대에는 작업을 실행하지 않습니다.              |
| `->when(Closure);`                           | 조건 클로저가 true인 경우에만 작업을 실행합니다.        |
| `->environments($env);`                      | 지정한 환경에서만 작업을 실행합니다.                   |

<!-- </div> -->
</div>

<a name="day-constraints"></a>
<!-- #### Day Constraints -->
#### Day Constraints

<!-- The `days` method may be used to limit the execution of a task to specific days of the week. For example, you may schedule a command to run hourly on Sundays and Wednesdays: -->
`days` 메서드는 특정 요일에만 작업이 실행되도록 설정할 때 사용합니다. 예를 들어, 매주 일요일과 수요일에 매시간 명령어를 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

<!-- Alternatively, you may use the constants available on the `Illuminate\Console\Scheduling\Schedule` class when defining the days on which a task should run: -->
또한, 작업이 실행될 요일을 정의할 때 `Illuminate\Console\Scheduling\Schedule` 클래스의 상수를 사용할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
<!-- #### Between Time Constraints -->
#### Between Time Constraints

<!-- The `between` method may be used to limit the execution of a task based on the time of day: -->
`between` 메서드는 작업 실행 시간을 특정 시간대로 제한할 때 사용합니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

<!-- Similarly, the `unlessBetween` method can be used to exclude the execution of a task for a period of time: -->
반대로, `unlessBetween` 메서드는 특정 시간대에는 작업을 제외시키는 방법입니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
<!-- #### Truth Test Constraints -->
#### Truth Test Constraints

<!-- The `when` method may be used to limit the execution of a task based on the result of a given truth test. In other words, if the given closure returns `true`, the task will execute as long as no other constraining conditions prevent the task from running: -->
`when` 메서드는 주어진 조건(클로저의 반환값이 true)일 때만 작업을 실행하도록 제어할 수 있습니다. 다른 제약 조건에 걸리지 않는다면, 조건이 `true`이면 실행됩니다:

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

<!-- The `skip` method may be seen as the inverse of `when`. If the `skip` method returns `true`, the scheduled task will not be executed: -->
`skip` 메서드는 `when`의 반대 개념으로, `skip` 메서드의 클로저가 `true`를 반환하면 예약된 작업을 실행하지 않습니다:

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

<!-- When using chained `when` methods, the scheduled command will only execute if all `when` conditions return `true`. -->
`when` 메서드를 연속적으로 체이닝하면, 모든 `when` 조건이 `true`를 반환할 때만 작업이 실행됩니다.

<a name="environment-constraints"></a>
<!-- #### Environment Constraints -->
#### Environment Constraints

<!-- The `environments` method may be used to execute tasks only on the given environments (as defined by the `APP_ENV` [environment variable](/docs/master/configuration#environment-configuration)): -->
`environments` 메서드는 지정된 환경에서만 작업을 실행하게 하는 방법입니다. 환경은 `APP_ENV` [environment variable](/docs/master/configuration#environment-configuration)로 정의됩니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
<!-- ### Timezones -->
### Timezones

<!-- Using the `timezone` method, you may specify that a scheduled task's time should be interpreted within a given timezone: -->
`timezone` 메서드를 사용하면, 예약 작업이 특정 타임존 기준으로 실행되도록 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

<!-- If you are repeatedly assigning the same timezone to all of your scheduled tasks, you can specify which timezone should be assigned to all schedules by defining a `schedule_timezone` option within your application's `app` configuration file: -->
만약 모든 예약 작업에 동일한 타임존을 반복적으로 부여한다면, 애플리케이션의 `app` 설정 파일에서 `schedule_timezone` 옵션을 지정할 수 있습니다:

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> 일부 타임존은 서머타임(일광 절약 시간제)을 사용합니다. 이로 인한 변화가 있을 때 예약된 작업이 한 번 더 실행되거나 아예 실행되지 않을 수 있습니다. 따라서 가능하면 타임존 스케줄링 사용을 피하는 것이 좋습니다.

<a name="preventing-task-overlaps"></a>
<!-- ### Preventing Task Overlaps -->
### Preventing Task Overlaps

<!-- By default, scheduled tasks will be run even if the previous instance of the task is still running. To prevent this, you may use the `withoutOverlapping` method: -->
기본적으로 예약한 작업은 이전 실행 인스턴스가 아직 완료되지 않은 경우에도 계속 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

<!-- In this example, the `emails:send` [Artisan command](/docs/master/artisan) will be run every minute if it is not already running. The `withoutOverlapping` method is especially useful if you have tasks that vary drastically in their execution time, preventing you from predicting exactly how long a given task will take. -->
위 예제는 `emails:send` [Artisan command](/docs/master/artisan)를 매분마다 실행하되, 이전 실행이 끝나지 않았다면 새로 실행하지 않습니다. `withoutOverlapping` 메서드는 실행 시간이 불규칙한 작업의 중첩 실행을 막아주어 유용합니다.

<!-- If needed, you may specify how many minutes must pass before the "without overlapping" lock expires. By default, the lock will expire after 24 hours: -->
필요하다면, 중첩 방지 락(lock)이 만료되는 시간(분 단위)을 지정할 수도 있습니다. 기본값은 24시간입니다:

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

<!-- Behind the scenes, the `withoutOverlapping` method utilizes your application's [cache](/docs/master/cache) to obtain locks. If necessary, you can clear these cache locks using the `schedule:clear-cache` Artisan command. This is typically only necessary if a task becomes stuck due to an unexpected server problem. -->
`withoutOverlapping` 메서드는 내부적으로 애플리케이션의 [cache](/docs/master/cache)를 활용해 락을 얻습니다. 예상치 못한 서버 문제로 작업이 중단되어 락이 남았다면, `schedule:clear-cache` Artisan 명령어로 이 락을 삭제할 수 있습니다. 보통 작업이 ‘멈춘’ 특이한 경우에 한해서만 필요합니다.

<a name="running-tasks-on-one-server"></a>
<!-- ### Running Tasks on One Server -->
### Running Tasks on One Server

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, 또는 `redis`여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<!-- If your application's scheduler is running on multiple servers, you may limit a scheduled job to only execute on a single server. For instance, assume you have a scheduled task that generates a new report every Friday night. If the task scheduler is running on three worker servers, the scheduled task will run on all three servers and generate the report three times. Not good! -->
스케줄러가 여러 대의 서버에서 실행 중일 때, 예약 작업을 한 서버에서만 실행하도록 제한할 수 있습니다. 예를 들어, 매주 금요일 밤마다 새 보고서를 생성하는 예약 작업이 있고, 세 대의 워커 서버에서 각각 스케줄러가 실행된다면, 세 서버 모두에서 동일 작업이 실행되어 중복 보고서가 생성될 수 있습니다.

<!-- To indicate that the task should run on only one server, use the `onOneServer` method when defining the scheduled task. The first server to obtain the task will secure an atomic lock on the job to prevent other servers from running the same task at the same time: -->
이럴 때 `onOneServer` 메서드를 사용하면, 먼저 락을 획득한 서버만 작업을 실행하게 됩니다(원자적 락):

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

<!-- You may use the `useCache` method to customize the cache store used by the scheduler to obtain the atomic locks necessary for single-server tasks: -->
스케줄러가 단일 서버 작업에 사용할 캐시 스토어를 지정하고 싶다면 `useCache` 메서드를 사용할 수 있습니다:

```php
Schedule::useCache('database');
```

<a name="naming-unique-jobs"></a>
<!-- #### Naming Single Server Jobs -->
#### Naming Single Server Jobs

<!-- Sometimes you may need to schedule the same job to be dispatched with different parameters, while still instructing Laravel to run each permutation of the job on a single server. To accomplish this, you may assign each schedule definition a unique name via the `name` method: -->
매개변수가 다른 동일한 작업을 여러 번 예약하면서도 각각을 단일 서버에서만 실행하고 싶을 때는, 각 스케줄 정의에 고유한 이름을 `name` 메서드로 부여하세요:

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

<!-- Similarly, scheduled closures must be assigned a name if they are intended to be run on one server: -->
마찬가지로, 클로저로 예약한 작업도 단일 서버 실행을 원한다면 이름을 반드시 지정해야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
<!-- ### Background Tasks -->
### Background Tasks

<!-- By default, multiple tasks scheduled at the same time will execute sequentially based on the order they are defined in your `schedule` method. If you have long-running tasks, this may cause subsequent tasks to start much later than anticipated. If you would like to run tasks in the background so that they may all run simultaneously, you may use the `runInBackground` method: -->
기본적으로 동시에 예약된 여러 작업은 `schedule` 메서드에 정의한 순서대로, 순차적으로 실행됩니다. 장시간 실행되는 작업이 있다면, 이후 작업이 예정보다 늦게 시작될 수 있습니다. 모든 작업을 동시에 실행하고 싶다면, `runInBackground` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> `runInBackground` 메서드는 `command`와 `exec` 메서드를 통해 예약된 작업에서만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
<!-- ### Maintenance Mode -->
### Maintenance Mode

<!-- Your application's scheduled tasks will not run when the application is in [maintenance mode](/docs/master/configuration#maintenance-mode), since we don't want your tasks to interfere with any unfinished maintenance you may be performing on your server. However, if you would like to force a task to run even in maintenance mode, you may call the `evenInMaintenanceMode` method when defining the task: -->
애플리케이션이 [maintenance mode](/docs/master/configuration#maintenance-mode)인 경우, 예약 작업은 실행되지 않습니다. 이는 메인터넌스 도중 예약 작업이 서버의 상태에 영향을 끼치는 것을 방지하기 위한 조치입니다. 그러나, 메인터넌스 모드 중에도 특정 작업을 강제로 실행하려면 `evenInMaintenanceMode` 메서드를 사용할 수 있습니다:

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="schedule-groups"></a>
<!-- ### Schedule Groups -->
### Schedule Groups

<!-- When defining multiple scheduled tasks with similar configurations, you can use Laravel's task grouping feature to avoid repeating the same settings for each task. Grouping tasks simplifies your code and ensures consistency across related tasks. -->
비슷한 설정을 가진 여러 예약 작업을 정의할 때는, Laravel의 작업 그룹 기능을 사용해 같은 설정을 반복 입력하지 않고 코드를 간결하게 작성할 수 있습니다. 그룹화로 연관된 작업들의 일관성을 유지할 수 있습니다.

<!-- To create a group of scheduled tasks, invoke the desired task configuration methods, followed by the `group` method. The `group` method accepts a closure that is responsible for defining the tasks that share the specified configuration: -->
예약 작업 그룹을 만들려면, 먼저 원하는 작업 설정 메서드들을 호출한 후, `group` 메서드 뒤에 그 설정을 공유할 작업들을 정의하는 클로저를 넘기세요. `group` 메서드는 지정된 설정을 공유하는 작업을 정의하는 클로저를 받습니다:

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
<!-- ## Running the Scheduler -->
## Running the Scheduler

<!-- Now that we have learned how to define scheduled tasks, let's discuss how to actually run them on our server. The `schedule:run` Artisan command will evaluate all of your scheduled tasks and determine if they need to run based on the server's current time. -->
이제 예약 작업을 정의하는 방법을 배웠으니, 실제 서버에서 어떻게 스케줄러를 실행하는지 알아보겠습니다. `schedule:run` Artisan 명령어는 모든 예약 작업을 평가하여 현재 실행되어야 하는지 판단합니다.

<!-- So, when using Laravel's scheduler, we only need to add a single cron configuration entry to our server that runs the `schedule:run` command every minute. If you do not know how to add cron entries to your server, consider using a managed platform such as [Laravel Cloud](https://cloud.laravel.com) which can manage the scheduled task execution for you: -->
따라서, Laravel 스케줄러를 사용할 때는 서버에 단 하나의 크론 항목만 등록하면 되고, 이 항목에서 매분마다 `schedule:run` 명령어를 실행하면 됩니다. 만약 크론 항목을 직접 설정하는 법이 어렵다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 관리형 플랫폼에서 예약 작업 실행을 쉽게 관리할 수 있습니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
<!-- ### Sub-Minute Scheduled Tasks -->
### Sub-Minute Scheduled Tasks

<!-- On most operating systems, cron jobs are limited to running a maximum of once per minute. However, Laravel's scheduler allows you to schedule tasks to run at more frequent intervals, even as often as once per second: -->
대부분의 운영체제에서 크론 작업은 1분에 한 번만 실행 가능합니다. 그러나 Laravel 스케줄러는 1초 단위 등, 그보다 더 짧은 간격으로 작업을 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

<!-- When sub-minute tasks are defined within your application, the `schedule:run` command will continue running until the end of the current minute instead of exiting immediately. This allows the command to invoke all required sub-minute tasks throughout the minute. -->
애플리케이션 내에 1분 미만 간격 작업이 정의되면, `schedule:run` 명령어는 실행 후 즉시 종료되지 않고 해당 분이 끝날 때까지 계속 동작합니다. 이를 통해 매분 내내 모든 짧은 주기의 예약 작업이 올바르게 수행됩니다.

<!-- Since sub-minute tasks that take longer than expected to run could delay the execution of later sub-minute tasks, it is recommended that all sub-minute tasks dispatch queued jobs or background commands to handle the actual task processing: -->
예상보다 시간이 오래 걸리는 1분 미만 작업으로 이후 작업 실행이 지연될 수 있으므로, 이러한 경우에는 실제 처리는 큐 작업 디스패치나 백그라운드 명령으로 분리하는 것이 좋습니다:

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
<!-- #### Interrupting Sub-Minute Tasks -->
#### Interrupting Sub-Minute Tasks

<!-- As the `schedule:run` command runs for the entire minute of invocation when sub-minute tasks are defined, you may sometimes need to interrupt the command when deploying your application. Otherwise, an instance of the `schedule:run` command that is already running would continue using your application's previously deployed code until the current minute ends. -->
1분 미만 작업이 정의되어 있으면, `schedule:run` 명령어는 전체 분마다 계속 실행됩니다. 배포(deploy) 중에는 이미 실행 중인 `schedule:run` 인스턴스를 중단해야 할 수도 있습니다. 그렇지 않으면 이미 실행 중이던 명령어가 이전 배포된 코드로 계속 실행될 수 있습니다.

<!-- To interrupt in-progress `schedule:run` invocations, you may add the `schedule:interrupt` command to your application's deployment script. This command should be invoked after your application is finished deploying: -->
이 경우, 배포가 끝난 뒤에 `schedule:interrupt` 명령어를 배포 스크립트에 추가해서 실행 중인 `schedule:run` 명령어를 중단할 수 있습니다:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
<!-- ### Running the Scheduler Locally -->
### Running the Scheduler Locally

<!-- Typically, you would not add a scheduler cron entry to your local development machine. Instead, you may use the `schedule:work` Artisan command. This command will run in the foreground and invoke the scheduler every minute until you terminate the command. When sub-minute tasks are defined, the scheduler will continue running within each minute to process those tasks: -->
보통 로컬 개발 환경에는 크론 항목을 추가하지 않습니다. 대신 `schedule:work` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 포그라운드에서 실행되며 사용자가 중단하기 전까지 매분마다 스케줄러를 실행합니다. 1분 미만 작업이 있을 때도 각각 해당 시간 내에서 반복 실행됩니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
<!-- ## Task Output -->
## Task Output

<!-- The Laravel scheduler provides several convenient methods for working with the output generated by scheduled tasks. First, using the `sendOutputTo` method, you may send the output to a file for later inspection: -->
Laravel 스케줄러는 예약 작업의 출력 결과를 다루기 위한 다양한 편의 메서드를 제공합니다. 먼저, `sendOutputTo` 메서드를 사용해 출력 결과를 파일로 남길 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

<!-- If you would like to append the output to a given file, you may use the `appendOutputTo` method: -->
파일에 내용을 이어붙이고 싶다면, `appendOutputTo` 메서드를 사용하세요:

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

<!-- Using the `emailOutputTo` method, you may email the output to an email address of your choice. Before emailing the output of a task, you should configure Laravel's [email services](/docs/master/mail): -->
`emailOutputTo` 메서드를 사용하면 출력 결과를 지정한 이메일 주소로 보낼 수도 있습니다. 이 기능을 사용하기 전에 반드시 Laravel의 [email services](/docs/master/mail)를 설정해야 합니다:

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

<!-- If you only want to email the output if the scheduled Artisan or system command terminates with a non-zero exit code, use the `emailOutputOnFailure` method: -->
예약 Artisan 명령어나 시스템 명령어가 종료 코드가 0이 아닌 경우에만 이메일을 받고 싶다면, `emailOutputOnFailure` 메서드를 사용하세요:

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo`는 `command` 및 `exec` 메서드로 예약된 작업에서만 사용할 수 있습니다.

<a name="task-hooks"></a>
<!-- ## Task Hooks -->
## Task Hooks

<!-- Using the `before` and `after` methods, you may specify code to be executed before and after the scheduled task is executed: -->
`before`와 `after` 메서드를 이용하면, 예약 작업 실행 전/후에 별도 코드를 실행시킬 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // The task is about to execute...
    })
    ->after(function () {
        // The task has executed...
    });
```

<!-- The `onSuccess` and `onFailure` methods allow you to specify code to be executed if the scheduled task succeeds or fails. A failure indicates that the scheduled Artisan or system command terminated with a non-zero exit code: -->
`onSuccess`와 `onFailure` 메서드는 작업이 성공적으로 완료되거나 실패했을 때(실패: 종료 코드가 0이 아님)에 실행할 코드를 등록할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // The task succeeded...
    })
    ->onFailure(function () {
        // The task failed...
    });
```

<!-- If output is available from your command, you may access it in your `after`, `onSuccess` or `onFailure` hooks by type-hinting an `Illuminate\Support\Stringable` instance as the `$output` argument of your hook's closure definition: -->
만약 명령어의 출력 결과를 활용하고 싶다면, `after`, `onSuccess`, `onFailure` 훅의 클로저에서 `Illuminate\Support\Stringable` 타입을 `$output` 인수로 받도록 선언할 수 있습니다:

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // The task succeeded...
    })
    ->onFailure(function (Stringable $output) {
        // The task failed...
    });
```

<a name="pinging-urls"></a>
<!-- #### Pinging URLs -->
#### Pinging URLs

<!-- Using the `pingBefore` and `thenPing` methods, the scheduler can automatically ping a given URL before or after a task is executed. This method is useful for notifying an external service, such as [Envoyer](https://envoyer.io), that your scheduled task is beginning or has finished execution: -->
`pingBefore`와 `thenPing` 메서드를 활용하면 작업 실행 전후에 특정 URL로 자동으로 핑(ping)을 보낼 수 있습니다. 이 기능은 [Envoyer](https://envoyer.io) 같은 외부 서비스에 예약 작업의 시작/종료를 알릴 때 유용합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

<!-- The `pingOnSuccess` and `pingOnFailure` methods may be used to ping a given URL only if the task succeeds or fails. A failure indicates that the scheduled Artisan or system command terminated with a non-zero exit code: -->
`pingOnSuccess`와 `pingOnFailure`는 작업 성공 시 또는 실패 시에만 지정된 URL로 핑을 보냅니다(실패는 종료 코드가 0이 아닐 때입니다):

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

<!-- The `pingBeforeIf`,`thenPingIf`,`pingOnSuccessIf`, and `pingOnFailureIf` methods may be used to ping a given URL only if a given condition is `true`: -->
`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 메서드는 특정 조건이 `true`일 때만 핑을 보냅니다:

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
<!-- ## Events -->
## Events

<!-- Laravel dispatches a variety of [events](/docs/master/events) during the scheduling process. You may [define listeners](/docs/master/events) for any of the following events: -->
Laravel은 스케줄링 과정에서 다양한 [events](/docs/master/events)를 발생시킵니다. 아래 이벤트들에 대해 [define listeners](/docs/master/events)할 수 있습니다:

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 이벤트 이름                                                  |
| ----------------------------------------------------------- |
| `Illuminate\Console\Events\ScheduledTaskStarting`           |
| `Illuminate\Console\Events\ScheduledTaskFinished`           |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped`            |
| `Illuminate\Console\Events\ScheduledTaskFailed`             |

<!-- </div> -->
</div>
