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
    - [Pausing Scheduled Tasks](#pausing-scheduled-tasks)
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
이전에는 서버에서 스케줄링해야 하는 각 작업마다 cron 설정 항목을 작성했을 수 있습니다. 하지만 이렇게 하면 작업 스케줄이 더 이상 소스 관리에 포함되지 않고, 기존 cron 항목을 확인하거나 새 항목을 추가하려면 서버에 SSH로 접속해야 하므로 금방 번거로워질 수 있습니다.

<!-- Laravel's command scheduler offers a fresh approach to managing scheduled tasks on your server. The scheduler allows you to fluently and expressively define your command schedule within your Laravel application itself. When using the scheduler, only a single cron entry is needed on your server. Your task schedule is typically defined in your application's `routes/console.php` file. -->
Laravel의 명령어 스케줄러는 서버의 스케줄된 작업을 관리하는 새로운 방식을 제공합니다. 스케줄러를 사용하면 Laravel 애플리케이션 안에서 명령어 스케줄을 유창하고 표현력 있게 정의할 수 있습니다. 스케줄러를 사용할 때 서버에는 하나의 cron 항목만 필요합니다. 작업 스케줄은 일반적으로 애플리케이션의 `routes/console.php` 파일에 정의합니다.

<a name="defining-schedules"></a>
<!-- ## Defining Schedules -->
## Defining Schedules

<!-- You may define all of your scheduled tasks in your application's `routes/console.php` file. To get started, let's take a look at an example. In this example, we will schedule a closure to be called every day at midnight. Within the closure we will execute a database query to clear a table: -->
스케줄된 모든 작업은 애플리케이션의 `routes/console.php` 파일에 정의할 수 있습니다. 먼저 예제를 살펴보겠습니다. 이 예제에서는 매일 자정에 호출될 클로저를 스케줄링합니다. 클로저 안에서는 테이블을 비우기 위해 데이터베이스 쿼리를 실행합니다.

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

<!-- In addition to scheduling using closures, you may also schedule [invokable objects](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke). Invokable objects are simple PHP classes that contain an `__invoke` method: -->
클로저를 사용한 스케줄링 외에도 [invokable objects](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 스케줄링할 수 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 포함하는 간단한 PHP 클래스입니다.

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

<!-- If you prefer to reserve your `routes/console.php` file for command definitions only, you may use the `withSchedule` method in your application's `bootstrap/app.php` file to define your scheduled tasks. This method accepts a closure that receives an instance of the scheduler: -->
`routes/console.php` 파일을 명령어 정의 전용으로만 사용하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 사용하여 스케줄된 작업을 정의할 수 있습니다. 이 메서드는 스케줄러 인스턴스를 전달받는 클로저를 인수로 받습니다.

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

<!-- If you would like to view an overview of your scheduled tasks and the next time they are scheduled to run, you may use the `schedule:list` Artisan command: -->
스케줄된 작업의 개요와 다음 실행 예정 시간을 확인하려면 `schedule:list` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
<!-- ### Scheduling Artisan Commands -->
### Scheduling Artisan Commands

<!-- In addition to scheduling closures, you may also schedule [Artisan commands](/docs/13.x/artisan) and system commands. For example, you may use the `command` method to schedule an Artisan command using either the command's name or class. -->
클로저를 스케줄링하는 것 외에도 [Artisan commands](/docs/13.x/artisan)와 시스템 명령어를 스케줄링할 수 있습니다. 예를 들어 `command` 메서드를 사용하면 명령어 이름 또는 클래스 중 하나로 Artisan 명령어를 스케줄링할 수 있습니다.

<!-- When scheduling Artisan commands using the command's class name, you may pass an array of additional command-line arguments that should be provided to the command when it is invoked: -->
명령어 클래스 이름을 사용하여 Artisan 명령어를 스케줄링할 때는, 명령어가 호출될 때 전달할 추가 명령줄 인수를 배열로 넘길 수 있습니다.

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
클로저로 정의된 Artisan 명령어를 스케줄링하려면, 명령어 정의 뒤에 스케줄링 관련 메서드를 체이닝할 수 있습니다.

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

<!-- If you need to pass arguments to the closure command, you may provide them to the `schedule` method: -->
클로저 명령어에 인수를 전달해야 한다면, `schedule` 메서드에 인수를 제공할 수 있습니다.

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
<!-- ### Scheduling Queued Jobs -->
### Scheduling Queued Jobs

<!-- The `job` method may be used to schedule a [queued job](/docs/13.x/queues). This method provides a convenient way to schedule queued jobs without using the `call` method to define closures to queue the job: -->
`job` 메서드는 [queued job](/docs/13.x/queues)을 스케줄링하는 데 사용할 수 있습니다. 이 메서드는 작업을 큐에 넣기 위해 `call` 메서드로 클로저를 정의하지 않고도 큐 작업을 스케줄링할 수 있는 편리한 방법을 제공합니다.

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

<!-- Optional second and third arguments may be provided to the `job` method which specifies the queue name and queue connection that should be used to queue the job: -->
`job` 메서드에는 선택적으로 두 번째와 세 번째 인수를 제공할 수 있으며, 각각 작업을 큐에 넣을 때 사용할 큐 이름과 큐 연결을 지정합니다.

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
`exec` 메서드는 운영체제에 명령어를 실행하도록 지시하는 데 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
<!-- ### Schedule Frequency Options -->
### Schedule Frequency Options

<!-- We've already seen a few examples of how you may configure a task to run at specified intervals. However, there are many more task schedule frequencies that you may assign to a task: -->
지정된 간격으로 작업을 실행하도록 설정하는 몇 가지 예제를 이미 살펴보았습니다. 하지만 작업에 지정할 수 있는 스케줄 주기는 훨씬 더 다양합니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| Method                             | Description                                              |
| ---------------------------------- | -------------------------------------------------------- |
| `->cron('* * * * *');`             | 사용자 정의 cron 스케줄로 작업을 실행합니다.                  |
| `->everySecond();`                 | 매초 작업을 실행합니다.                               |
| `->everyTwoSeconds();`             | 2초마다 작업을 실행합니다.                          |
| `->everyFiveSeconds();`            | 5초마다 작업을 실행합니다.                         |
| `->everyTenSeconds();`             | 10초마다 작업을 실행합니다.                          |
| `->everyFifteenSeconds();`         | 15초마다 작업을 실행합니다.                      |
| `->everyTwentySeconds();`          | 20초마다 작업을 실행합니다.                       |
| `->everyThirtySeconds();`          | 30초마다 작업을 실행합니다.                       |
| `->everyMinute();`                 | 매분 작업을 실행합니다.                               |
| `->everyTwoMinutes();`             | 2분마다 작업을 실행합니다.                          |
| `->everyThreeMinutes();`           | 3분마다 작업을 실행합니다.                        |
| `->everyFourMinutes();`            | 4분마다 작업을 실행합니다.                         |
| `->everyFiveMinutes();`            | 5분마다 작업을 실행합니다.                         |
| `->everyTenMinutes();`             | 10분마다 작업을 실행합니다.                          |
| `->everyFifteenMinutes();`         | 15분마다 작업을 실행합니다.                      |
| `->everyThirtyMinutes();`          | 30분마다 작업을 실행합니다.                       |
| `->hourly();`                      | 매시간 작업을 실행합니다.                                 |
| `->hourlyAt(17);`                  | 매시간 정각에서 17분이 지난 시점에 작업을 실행합니다.     |
| `->everyOddHour($minutes = 0);`    | 홀수 시간마다 작업을 실행합니다.                             |
| `->everyTwoHours($minutes = 0);`   | 2시간마다 작업을 실행합니다.                            |
| `->everyThreeHours($minutes = 0);` | 3시간마다 작업을 실행합니다.                          |
| `->everyFourHours($minutes = 0);`  | 4시간마다 작업을 실행합니다.                           |
| `->everySixHours($minutes = 0);`   | 6시간마다 작업을 실행합니다.                            |
| `->daily();`                       | 매일 자정에 작업을 실행합니다.                      |
| `->dailyAt('13:00');`              | 매일 13:00에 작업을 실행합니다.                         |
| `->twiceDaily(1, 13);`             | 매일 1:00와 13:00에 작업을 실행합니다.                      |
| `->twiceDailyAt(1, 13, 15);`       | 매일 1:15와 13:15에 작업을 실행합니다.                      |
| `->daysOfMonth([1, 10, 20]);`      | 매월 특정 날짜에 작업을 실행합니다.              |
| `->weekly();`                      | 매주 일요일 00:00에 작업을 실행합니다.                      |
| `->weeklyOn(1, '8:00');`           | 매주 월요일 8:00에 작업을 실행합니다.               |
| `->monthly();`                     | 매월 첫째 날 00:00에 작업을 실행합니다.   |
| `->monthlyOn(4, '15:00');`         | 매월 4일 15:00에 작업을 실행합니다.            |
| `->twiceMonthly(1, 16, '13:00');`  | 매월 1일과 16일 13:00에 작업을 실행합니다.       |
| `->lastDayOfMonth('15:00');`       | 매월 마지막 날 15:00에 작업을 실행합니다.      |
| `->quarterly();`                   | 매분기 첫째 날 00:00에 작업을 실행합니다. |
| `->quarterlyOn(4, '14:00');`       | 매분기 4일 14:00에 작업을 실행합니다.          |
| `->yearly();`                      | 매년 첫째 날 00:00에 작업을 실행합니다.    |
| `->yearlyOn(6, 1, '17:00');`       | 매년 6월 1일 17:00에 작업을 실행합니다.            |
| `->timezone('America/New_York');`  | 작업의 타임존을 설정합니다.                           |

<!-- </div> -->
</div>

<!-- These methods may be combined with additional constraints to create even more finely tuned schedules that only run on certain days of the week. For example, you may schedule a command to run weekly on Monday: -->
이러한 메서드는 추가 제약 조건과 조합하여, 특정 요일에만 실행되는 더욱 세밀한 스케줄을 만들 수 있습니다. 예를 들어 매주 월요일에 명령어가 실행되도록 스케줄링할 수 있습니다.

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
추가 스케줄 제약 조건 목록은 아래에서 확인할 수 있습니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| Method                                   | Description                                            |
| ---------------------------------------- | ------------------------------------------------------ |
| `->weekdays();`                          | 작업을 평일로 제한합니다.                            |
| `->weekends();`                          | 작업을 주말로 제한합니다.                            |
| `->sundays();`                           | 작업을 일요일로 제한합니다.                              |
| `->mondays();`                           | 작업을 월요일로 제한합니다.                              |
| `->tuesdays();`                          | 작업을 화요일로 제한합니다.                             |
| `->wednesdays();`                        | 작업을 수요일로 제한합니다.                           |
| `->thursdays();`                         | 작업을 목요일로 제한합니다.                            |
| `->fridays();`                           | 작업을 금요일로 제한합니다.                              |
| `->saturdays();`                         | 작업을 토요일로 제한합니다.                            |
| `->days(array\|mixed);`                  | 작업을 특정 요일로 제한합니다.                       |
| `->between($startTime, $endTime);`       | 작업을 시작 시간과 종료 시간 사이에만 실행되도록 제한합니다.     |
| `->unlessBetween($startTime, $endTime);` | 작업을 시작 시간과 종료 시간 사이에는 실행되지 않도록 제한합니다. |
| `->when(Closure);`                       | 진리 검사 결과에 따라 작업을 제한합니다.                  |
| `->environments($env);`                  | 작업을 특정 환경으로 제한합니다.               |

<!-- </div> -->
</div>

<a name="day-constraints"></a>
<!-- #### Day Constraints -->
#### Day Constraints

<!-- The `days` method may be used to limit the execution of a task to specific days of the week. For example, you may schedule a command to run hourly on Sundays and Wednesdays: -->
`days` 메서드는 작업 실행을 특정 요일로 제한하는 데 사용할 수 있습니다. 예를 들어 일요일과 수요일마다 매시간 명령어가 실행되도록 스케줄링할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

<!-- Alternatively, you may use the constants available on the `Illuminate\Console\Scheduling\Schedule` class when defining the days on which a task should run: -->
또는 작업이 실행될 요일을 정의할 때 `Illuminate\Console\Scheduling\Schedule` 클래스에서 제공하는 상수를 사용할 수 있습니다.

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
`between` 메서드는 하루 중 특정 시간대를 기준으로 작업 실행을 제한하는 데 사용할 수 있습니다.

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

<!-- Similarly, the `unlessBetween` method can be used to exclude the execution of a task for a period of time: -->
마찬가지로 `unlessBetween` 메서드는 특정 시간 동안 작업 실행을 제외하는 데 사용할 수 있습니다.

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
<!-- #### Truth Test Constraints -->
#### Truth Test Constraints

<!-- The `when` method may be used to limit the execution of a task based on the result of a given truth test. In other words, if the given closure returns `true`, the task will execute as long as no other constraining conditions prevent the task from running: -->
`when` 메서드는 주어진 진리 검사 결과를 기준으로 작업 실행을 제한하는 데 사용할 수 있습니다. 즉, 주어진 클로저가 `true`를 반환하면 작업 실행을 막는 다른 제약 조건이 없는 한 해당 작업이 실행됩니다.

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

<!-- The `skip` method may be seen as the inverse of `when`. If the `skip` method returns `true`, the scheduled task will not be executed: -->
`skip` 메서드는 `when`의 반대 개념으로 볼 수 있습니다. `skip` 메서드가 `true`를 반환하면 스케줄된 작업은 실행되지 않습니다.

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

<!-- When using chained `when` methods, the scheduled command will only execute if all `when` conditions return `true`. -->
`when` 메서드를 체이닝하여 사용할 때는 모든 `when` 조건이 `true`를 반환해야만 스케줄된 명령어가 실행됩니다.

<a name="environment-constraints"></a>
<!-- #### Environment Constraints -->
#### Environment Constraints

<!-- The `environments` method may be used to execute tasks only on the given environments (as defined by the `APP_ENV` [environment variable](/docs/13.x/configuration#environment-configuration)): -->
`environments` 메서드는 지정된 환경(`APP_ENV` [environment variable](/docs/13.x/configuration#environment-configuration)에 정의된 환경)에서만 작업을 실행하는 데 사용할 수 있습니다.

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
<!-- ### Timezones -->
### Timezones

<!-- Using the `timezone` method, you may specify that a scheduled task's time should be interpreted within a given timezone: -->
`timezone` 메서드를 사용하면 스케줄된 작업의 시간이 지정된 타임존을 기준으로 해석되도록 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

<!-- If you are repeatedly assigning the same timezone to all of your scheduled tasks, you can specify which timezone should be assigned to all schedules by defining a `schedule_timezone` option within your application's `app` configuration file: -->
모든 스케줄된 작업에 같은 타임존을 반복해서 지정하고 있다면, 애플리케이션의 `app` 설정 파일에 `schedule_timezone` 옵션을 정의하여 모든 스케줄에 적용할 타임존을 지정할 수 있습니다.

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> <!-- Remember that some timezones utilize daylight saving time. When daylight saving time changes occur, your scheduled task may run twice or even not run at all. For this reason, we recommend avoiding timezone scheduling when possible. -->
> 일부 타임존은 일광 절약 시간제를 사용한다는 점을 기억하세요. 일광 절약 시간이 변경될 때 스케줄된 작업이 두 번 실행되거나 전혀 실행되지 않을 수 있습니다. 이러한 이유로 가능하면 타임존 스케줄링은 피하는 것을 권장합니다.

<a name="preventing-task-overlaps"></a>
<!-- ### Preventing Task Overlaps -->
### Preventing Task Overlaps

<!-- By default, scheduled tasks will be run even if the previous instance of the task is still running. To prevent this, you may use the `withoutOverlapping` method: -->
기본적으로 스케줄된 작업은 이전 작업 인스턴스가 아직 실행 중이어도 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

<!-- In this example, the `emails:send` [Artisan command](/docs/13.x/artisan) will be run every minute if it is not already running. The `withoutOverlapping` method is especially useful if you have tasks that vary drastically in their execution time, preventing you from predicting exactly how long a given task will take. -->
이 예제에서 `emails:send` [Artisan command](/docs/13.x/artisan)는 이미 실행 중이 아니라면 매분 실행됩니다. `withoutOverlapping` 메서드는 실행 시간이 크게 달라져 특정 작업이 얼마나 오래 걸릴지 정확히 예측하기 어려운 작업이 있을 때 특히 유용합니다.

<!-- If needed, you may specify how many minutes must pass before the "without overlapping" lock expires. By default, the lock will expire after 24 hours: -->
필요하다면 "중복 실행 방지" 잠금이 만료되기까지 몇 분이 지나야 하는지 지정할 수 있습니다. 기본적으로 잠금은 24시간 후에 만료됩니다.

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

<!-- Behind the scenes, the `withoutOverlapping` method utilizes your application's [cache](/docs/13.x/cache) to obtain locks. If necessary, you can clear these cache locks using the `schedule:clear-cache` Artisan command. This is typically only necessary if a task becomes stuck due to an unexpected server problem. -->
내부적으로 `withoutOverlapping` 메서드는 잠금을 얻기 위해 애플리케이션의 [cache](/docs/13.x/cache)를 사용합니다. 필요한 경우 `schedule:clear-cache` Artisan 명령어를 사용하여 이러한 캐시 잠금을 지울 수 있습니다. 일반적으로 이는 예기치 못한 서버 문제로 작업이 멈춘 경우에만 필요합니다.

<a name="running-tasks-on-one-server"></a>
<!-- ### Running Tasks on One Server -->
### Running Tasks on One Server

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션이 기본 캐시 드라이버로 `database`, `memcached`, `dynamodb`, 또는 `redis` 캐시 드라이버를 사용해야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<!-- If your application's scheduler is running on multiple servers, you may limit a scheduled job to only execute on a single server. For instance, assume you have a scheduled task that generates a new report every Friday night. If the task scheduler is running on three worker servers, the scheduled task will run on all three servers and generate the report three times. Not good! -->
애플리케이션의 스케줄러가 여러 서버에서 실행 중이라면, 스케줄된 작업이 하나의 서버에서만 실행되도록 제한할 수 있습니다. 예를 들어 매주 금요일 밤에 새 보고서를 생성하는 스케줄된 작업이 있다고 가정해 보겠습니다. 작업 스케줄러가 세 대의 워커 서버에서 실행 중이라면, 스케줄된 작업은 세 서버 모두에서 실행되어 보고서가 세 번 생성됩니다. 좋지 않습니다!

<!-- To indicate that the task should run on only one server, use the `onOneServer` method when defining the scheduled task. The first server to obtain the task will secure an atomic lock on the job to prevent other servers from running the same task at the same time: -->
작업이 하나의 서버에서만 실행되어야 함을 나타내려면, 스케줄된 작업을 정의할 때 `onOneServer` 메서드를 사용하세요. 작업을 처음 획득한 서버가 해당 작업에 대한 원자적 잠금을 확보하여 다른 서버가 같은 작업을 동시에 실행하지 못하도록 합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

<!-- You may use the `useCache` method to customize the cache store used by the scheduler to obtain the atomic locks necessary for single-server tasks: -->
단일 서버 작업에 필요한 원자적 잠금을 얻을 때 스케줄러가 사용할 캐시 저장소를 사용자 정의하려면 `useCache` 메서드를 사용할 수 있습니다.

```php
Schedule::useCache('database');
```

<a name="naming-unique-jobs"></a>
<!-- #### Naming Single Server Jobs -->
#### Naming Single Server Jobs

<!-- Sometimes you may need to schedule the same job to be dispatched with different parameters, while still instructing Laravel to run each permutation of the job on a single server. To accomplish this, you may assign each schedule definition a unique name via the `name` method: -->
때로는 같은 작업을 서로 다른 매개변수로 디스패치하도록 스케줄링하면서도, 각 작업의 변형이 하나의 서버에서만 실행되도록 Laravel에 지시해야 할 수 있습니다. 이를 위해 `name` 메서드를 통해 각 스케줄 정의에 고유한 이름을 지정할 수 있습니다.

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
마찬가지로 스케줄된 클로저를 하나의 서버에서 실행하려면 이름을 지정해야 합니다.

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
기본적으로 같은 시간에 예약된 여러 작업은 `schedule` 메서드에 정의된 순서에 따라 순차적으로 실행됩니다. 오래 실행되는 작업이 있다면, 그 뒤의 작업들이 예상보다 훨씬 늦게 시작될 수 있습니다. 작업을 백그라운드에서 실행하여 모두 동시에 실행되도록 하려면 `runInBackground` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> `runInBackground` 메서드는 `command` 및 `exec` 메서드로 작업을 예약할 때만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
<!-- ### Maintenance Mode -->
### Maintenance Mode

<!-- Your application's scheduled tasks will not run when the application is in [maintenance mode](/docs/13.x/configuration#maintenance-mode), since we don't want your tasks to interfere with any unfinished maintenance you may be performing on your server. However, if you would like to force a task to run even in maintenance mode, you may call the `evenInMaintenanceMode` method when defining the task: -->
애플리케이션이 [maintenance mode](/docs/13.x/configuration#maintenance-mode)에 있으면 애플리케이션의 예약 작업은 실행되지 않습니다. 서버에서 아직 완료되지 않은 유지 관리 작업을 수행하는 동안 예약 작업이 방해되지 않도록 하기 위해서입니다. 하지만 유지 관리 모드에서도 작업을 강제로 실행하고 싶다면, 작업을 정의할 때 `evenInMaintenanceMode` 메서드를 호출할 수 있습니다.

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="pausing-scheduled-tasks"></a>
<!-- ### Pausing Scheduled Tasks -->
### Pausing Scheduled Tasks

<!-- You may temporarily pause scheduled task processing without changing your deployed code by using the `schedule:pause` Artisan command: -->
배포된 코드를 변경하지 않고도 `schedule:pause` Artisan 명령어를 사용하여 예약 작업 처리를 일시적으로 중지할 수 있습니다.

```shell
php artisan schedule:pause
```

<!-- While the scheduler is paused, no scheduled tasks will run. You may resume scheduled task processing using the `schedule:continue` command: -->
스케줄러가 일시 중지된 동안에는 어떤 예약 작업도 실행되지 않습니다. `schedule:continue` 명령어를 사용하여 예약 작업 처리를 다시 시작할 수 있습니다.

```shell
php artisan schedule:continue
```

<!-- If a task should still run while the scheduler is paused, you may mark it with the `evenWhenPaused` method: -->
스케줄러가 일시 중지된 상태에서도 특정 작업이 계속 실행되어야 한다면, `evenWhenPaused` 메서드로 해당 작업을 표시할 수 있습니다.

```php
Schedule::command('emails:send')->evenWhenPaused();
```

<a name="schedule-groups"></a>
<!-- ### Schedule Groups -->
### Schedule Groups

<!-- When defining multiple scheduled tasks with similar configurations, you can use Laravel's task grouping feature to avoid repeating the same settings for each task. Grouping tasks simplifies your code and ensures consistency across related tasks. -->
비슷한 설정을 가진 여러 예약 작업을 정의할 때, 각 작업마다 같은 설정을 반복하지 않도록 Laravel의 작업 그룹화 기능을 사용할 수 있습니다. 작업을 그룹화하면 코드가 단순해지고 관련 작업 간의 일관성을 유지할 수 있습니다.

<!-- To create a group of scheduled tasks, invoke the desired task configuration methods, followed by the `group` method. The `group` method accepts a closure that is responsible for defining the tasks that share the specified configuration: -->
예약 작업 그룹을 만들려면 원하는 작업 설정 메서드들을 호출한 뒤 `group` 메서드를 호출합니다. `group` 메서드는 지정된 설정을 공유하는 작업을 정의하는 클로저를 인수로 받습니다.

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
이제 예약 작업을 정의하는 방법을 배웠으므로, 서버에서 실제로 이를 실행하는 방법을 살펴보겠습니다. `schedule:run` Artisan 명령어는 모든 예약 작업을 평가하고, 서버의 현재 시간을 기준으로 해당 작업을 실행해야 하는지 판단합니다.

<!-- So, when using Laravel's scheduler, we only need to add a single cron configuration entry to our server that runs the `schedule:run` command every minute. If you do not know how to add cron entries to your server, consider using a managed platform such as [Laravel Cloud](https://cloud.laravel.com) which can manage the scheduled task execution for you: -->
따라서 Laravel 스케줄러를 사용할 때는 서버에 cron 설정 항목을 하나만 추가하면 됩니다. 이 항목은 매분 `schedule:run` 명령어를 실행합니다. 서버에 cron 항목을 추가하는 방법을 모른다면, 예약 작업 실행을 대신 관리해 줄 수 있는 [Laravel Cloud](https://cloud.laravel.com) 같은 관리형 플랫폼을 사용하는 것도 고려해 보십시오.

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
<!-- ### Sub-Minute Scheduled Tasks -->
### Sub-Minute Scheduled Tasks

<!-- On most operating systems, cron jobs are limited to running a maximum of once per minute. However, Laravel's scheduler allows you to schedule tasks to run at more frequent intervals, even as often as once per second: -->
대부분의 운영체제에서 cron 작업은 최대 1분에 한 번만 실행되도록 제한됩니다. 하지만 Laravel 스케줄러를 사용하면 작업을 더 짧은 간격으로, 심지어 1초에 한 번까지도 실행되도록 예약할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

<!-- When sub-minute tasks are defined within your application, the `schedule:run` command will continue running until the end of the current minute instead of exiting immediately. This allows the command to invoke all required sub-minute tasks throughout the minute. -->
애플리케이션 안에 1분 미만 작업이 정의되어 있으면, `schedule:run` 명령어는 즉시 종료되지 않고 현재 분이 끝날 때까지 계속 실행됩니다. 이를 통해 해당 분 동안 필요한 모든 1분 미만 작업을 호출할 수 있습니다.

<!-- Since sub-minute tasks that take longer than expected to run could delay the execution of later sub-minute tasks, it is recommended that all sub-minute tasks dispatch queued jobs or background commands to handle the actual task processing: -->
예상보다 오래 걸리는 1분 미만 작업은 이후의 1분 미만 작업 실행을 지연시킬 수 있습니다. 따라서 모든 1분 미만 작업은 실제 작업 처리를 큐 작업이나 백그라운드 명령어에 맡기는 것이 좋습니다.

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
<!-- #### Interrupting Sub-Minute Tasks -->
#### Interrupting Sub-Minute Tasks

<!-- As the `schedule:run` command runs for the entire minute of invocation when sub-minute tasks are defined, you may sometimes need to interrupt the command when deploying your application. Otherwise, an instance of the `schedule:run` command that is already running would continue using your application's previously deployed code until the current minute ends. -->
1분 미만 작업이 정의되어 있으면 `schedule:run` 명령어는 호출된 해당 1분 동안 계속 실행됩니다. 따라서 애플리케이션을 배포할 때 이 명령어를 중단해야 할 때가 있습니다. 그렇지 않으면 이미 실행 중인 `schedule:run` 명령어 인스턴스가 현재 분이 끝날 때까지 이전에 배포된 애플리케이션 코드를 계속 사용하게 됩니다.

<!-- To interrupt in-progress `schedule:run` invocations, you may add the `schedule:interrupt` command to your application's deployment script. This command should be invoked after your application is finished deploying: -->
진행 중인 `schedule:run` 호출을 중단하려면 애플리케이션 배포 스크립트에 `schedule:interrupt` 명령어를 추가할 수 있습니다. 이 명령어는 애플리케이션 배포가 완료된 뒤 호출해야 합니다.

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
<!-- ### Running the Scheduler Locally -->
### Running the Scheduler Locally

<!-- Typically, you would not add a scheduler cron entry to your local development machine. Instead, you may use the `schedule:work` Artisan command. This command will run in the foreground and invoke the scheduler every minute until you terminate the command. When sub-minute tasks are defined, the scheduler will continue running within each minute to process those tasks: -->
일반적으로 로컬 개발 머신에는 스케줄러 cron 항목을 추가하지 않습니다. 대신 `schedule:work` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 포그라운드에서 실행되며, 명령어를 종료할 때까지 매분 스케줄러를 호출합니다. 1분 미만 작업이 정의되어 있으면, 스케줄러는 각 분 안에서 계속 실행되며 해당 작업들을 처리합니다.

```shell
php artisan schedule:work
```

<a name="task-output"></a>
<!-- ## Task Output -->
## Task Output

<!-- The Laravel scheduler provides several convenient methods for working with the output generated by scheduled tasks. First, using the `sendOutputTo` method, you may send the output to a file for later inspection: -->
Laravel 스케줄러는 예약 작업에서 생성된 출력을 다루기 위한 편리한 메서드를 여러 가지 제공합니다. 먼저 `sendOutputTo` 메서드를 사용하면 나중에 확인할 수 있도록 출력을 파일로 보낼 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

<!-- If you would like to append the output to a given file, you may use the `appendOutputTo` method: -->
출력을 지정한 파일에 추가하고 싶다면 `appendOutputTo` 메서드를 사용할 수 있습니다.

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

<!-- Using the `emailOutputTo` method, you may email the output to an email address of your choice. Before emailing the output of a task, you should configure Laravel's [email services](/docs/13.x/mail): -->
`emailOutputTo` 메서드를 사용하면 원하는 이메일 주소로 출력을 이메일로 보낼 수 있습니다. 작업의 출력을 이메일로 보내기 전에 Laravel의 [email services](/docs/13.x/mail)를 설정해야 합니다.

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

<!-- If you only want to email the output if the scheduled Artisan or system command terminates with a non-zero exit code, use the `emailOutputOnFailure` method: -->
예약된 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료된 경우에만 출력을 이메일로 보내고 싶다면 `emailOutputOnFailure` 메서드를 사용하십시오.

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command` 및 `exec` 메서드에서만 사용할 수 있습니다.

<a name="task-hooks"></a>
<!-- ## Task Hooks -->
## Task Hooks

<!-- Using the `before` and `after` methods, you may specify code to be executed before and after the scheduled task is executed: -->
`before` 및 `after` 메서드를 사용하면 예약 작업이 실행되기 전과 실행된 후에 실행할 코드를 지정할 수 있습니다.

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
`onSuccess` 및 `onFailure` 메서드를 사용하면 예약 작업이 성공하거나 실패했을 때 실행할 코드를 지정할 수 있습니다. 실패는 예약된 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료되었음을 의미합니다.

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
명령어에서 출력이 제공되는 경우, 훅 클로저 정의의 `$output` 인수에 `Illuminate\Support\Stringable` 인스턴스를 타입 힌트로 지정하여 `after`, `onSuccess`, `onFailure` 훅에서 해당 출력에 접근할 수 있습니다.

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
`pingBefore` 및 `thenPing` 메서드를 사용하면 스케줄러가 작업 실행 전이나 실행 후에 지정한 URL로 자동으로 ping 요청을 보낼 수 있습니다. 이 메서드는 [Envoyer](https://envoyer.io) 같은 외부 서비스에 예약 작업이 시작되었거나 실행이 완료되었음을 알릴 때 유용합니다.

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

<!-- The `pingOnSuccess` and `pingOnFailure` methods may be used to ping a given URL only if the task succeeds or fails. A failure indicates that the scheduled Artisan or system command terminated with a non-zero exit code: -->
`pingOnSuccess` 및 `pingOnFailure` 메서드는 작업이 성공하거나 실패한 경우에만 지정한 URL로 ping 요청을 보내는 데 사용할 수 있습니다. 실패는 예약된 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료되었음을 의미합니다.

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

<!-- The `pingBeforeIf`,`thenPingIf`,`pingOnSuccessIf`, and `pingOnFailureIf` methods may be used to ping a given URL only if a given condition is `true`: -->
`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 메서드는 지정한 조건이 `true`인 경우에만 지정한 URL로 ping 요청을 보내는 데 사용할 수 있습니다.

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

<!-- Laravel dispatches a variety of [events](/docs/13.x/events) during the scheduling process. You may [define listeners](/docs/13.x/events) for any of the following events: -->
Laravel은 스케줄링 과정에서 다양한 [events](/docs/13.x/events)를 디스패치합니다. 다음 이벤트에 대해 [define listeners](/docs/13.x/events)할 수 있습니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 이벤트 이름                                                 |
| ----------------------------------------------------------- |
| `Illuminate\Console\Events\ScheduledTaskStarting`           |
| `Illuminate\Console\Events\ScheduledTaskFinished`           |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped`            |
| `Illuminate\Console\Events\ScheduledTaskFailed`             |

<!-- </div> -->
</div>
