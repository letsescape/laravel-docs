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
    - [Running Tasks On One Server](#running-tasks-on-one-server)
    - [Background Tasks](#background-tasks)
    - [Maintenance Mode](#maintenance-mode)
- [Running The Scheduler](#running-the-scheduler)
    - [Running The Scheduler Locally](#running-the-scheduler-locally)
- [Task Output](#task-output)
- [Task Hooks](#task-hooks)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In the past, you may have written a cron configuration entry for each task you needed to schedule on your server. However, this can quickly become a pain because your task schedule is no longer in source control and you must SSH into your server to view your existing cron entries or add additional entries. -->
과거에는 서버에서 작업을 예약하기 위해 필요한 각 작업마다 cron 구성을 추가했을 수 있습니다. 하지만 이렇게 하면 작업 스케줄이 소스 관리에서 분리되고, 기존 cron 엔트리를 확인하거나 새로 추가하려면 서버에 SSH로 접속해야 해서 관리가 매우 번거롭게 됩니다.

<!-- Laravel's command scheduler offers a fresh approach to managing scheduled tasks on your server. The scheduler allows you to fluently and expressively define your command schedule within your Laravel application itself. When using the scheduler, only a single cron entry is needed on your server. Your task schedule is defined in the `app/Console/Kernel.php` file's `schedule` method. To help you get started, a simple example is defined within the method. -->
Laravel의 명령어 스케줄러(Command Scheduler)는 서버에서 예약 작업을 효율적으로 관리할 수 있는 새로운 접근 방식을 제공합니다. 스케줄러를 사용하면 Laravel 애플리케이션 내부에서 예약할 명령어 스케줄을 간결하고 직관적으로 정의할 수 있습니다. 스케줄러를 사용하면 서버에는 단 하나의 cron 엔트리만 필요합니다. 실제 예약 작업 스케줄은 `app/Console/Kernel.php` 파일의 `schedule` 메서드 안에서 정의합니다. 쉽게 시작할 수 있도록 이 메서드 내부에 간단한 예시가 포함되어 있습니다.

<a name="defining-schedules"></a>
<!-- ## Defining Schedules -->
## Defining Schedules

<!-- You may define all of your scheduled tasks in the `schedule` method of your application's `App\Console\Kernel` class. To get started, let's take a look at an example. In this example, we will schedule a closure to be called every day at midnight. Within the closure we will execute a database query to clear a table: -->
애플리케이션의 `App\Console\Kernel` 클래스의 `schedule` 메서드에서 모든 예약 작업을 정의할 수 있습니다. 시작 예시를 살펴보면, 이 예제에서는 매일 자정에 호출되는 클로저(익명 함수)를 예약합니다. 이 클로저 내부에서는 데이터베이스 쿼리를 실행해 테이블을 비웁니다.

```
<?php

namespace App\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;
use Illuminate\Support\Facades\DB;

class Kernel extends ConsoleKernel
{
    /**
     * Define the application's command schedule.
     *
     * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
     * @return void
     */
    protected function schedule(Schedule $schedule)
    {
        $schedule->call(function () {
            DB::table('recent_users')->delete();
        })->daily();
    }
}
```

<!-- In addition to scheduling using closures, you may also schedule [invokable objects](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke). Invokable objects are simple PHP classes that contain an `__invoke` method: -->
클로저를 사용한 예약뿐 아니라, [invokable objects](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)도 예약 작업에 사용할 수 있습니다. 호출 가능한 객체란 `__invoke` 메서드를 가진 간단한 PHP 클래스를 의미합니다.

```
$schedule->call(new DeleteRecentUsers)->daily();
```

<!-- If you would like to view an overview of your scheduled tasks and the next time they are scheduled to run, you may use the `schedule:list` Artisan command: -->
예약된 작업 목록과 각각의 다음 실행 시점을 한눈에 확인하려면, `schedule:list` 아티즌 명령어를 사용할 수 있습니다.

```nothing
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
<!-- ### Scheduling Artisan Commands -->
### Scheduling Artisan Commands

<!-- In addition to scheduling closures, you may also schedule [Artisan commands](/docs/8.x/artisan) and system commands. For example, you may use the `command` method to schedule an Artisan command using either the command's name or class. -->
클로저 외에도 [Artisan commands](/docs/8.x/artisan)와 시스템 명령어도 예약할 수 있습니다. 예를 들어, `command` 메서드를 사용해 명령어의 이름이나 클래스명을 전달하여 아티즌 명령어를 예약할 수 있습니다.

<!-- When scheduling Artisan commands using the command's class name, you may pass an array of additional command-line arguments that should be provided to the command when it is invoked: -->
명령어의 클래스명을 사용할 때는, 명령 실행 시 제공할 추가 명령행 인수를 배열로 전달할 수 있습니다.

```
use App\Console\Commands\SendEmailsCommand;

$schedule->command('emails:send Taylor --force')->daily();

$schedule->command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
<!-- ### Scheduling Queued Jobs -->
### Scheduling Queued Jobs

<!-- The `job` method may be used to schedule a [queued job](/docs/8.x/queues). This method provides a convenient way to schedule queued jobs without using the `call` method to define closures to queue the job: -->
`job` 메서드는 [queued job](/docs/8.x/queues)을 예약하는 데 쓸 수 있습니다. 이 메서드를 사용하면 잡을 큐에 쌓기 위한 클로저를 `call` 메서드로 직접 정의하지 않고도 손쉽게 예약할 수 있습니다.

```
use App\Jobs\Heartbeat;

$schedule->job(new Heartbeat)->everyFiveMinutes();
```

<!-- Optional second and third arguments may be provided to the `job` method which specifies the queue name and queue connection that should be used to queue the job: -->
`job` 메서드의 두 번째와 세 번째 인수로, 해당 잡을 등록할 큐 이름과 큐 커넥션을 지정할 수도 있습니다.

```
use App\Jobs\Heartbeat;

// Dispatch the job to the "heartbeats" queue on the "sqs" connection...
$schedule->job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
<!-- ### Scheduling Shell Commands -->
### Scheduling Shell Commands

<!-- The `exec` method may be used to issue a command to the operating system: -->
`exec` 메서드를 사용하면 운영체제의 명령어를 직접 실행하도록 예약할 수 있습니다.

```
$schedule->exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
<!-- ### Schedule Frequency Options -->
### Schedule Frequency Options

<!-- We've already seen a few examples of how you may configure a task to run at specified intervals. However, there are many more task schedule frequencies that you may assign to a task: -->
작업을 특정 주기마다 실행하도록 설정하는 기본 예시를 앞에서 살펴보았습니다. 하지만 실제로는 더 다양한 빈도로 작업을 예약할 수 있습니다.

<!--
Method  | Description
------------- | -------------
`->cron('* * * * *');`  |  Run the task on a custom cron schedule
`->everyMinute();`  |  Run the task every minute
`->everyTwoMinutes();`  |  Run the task every two minutes
`->everyThreeMinutes();`  |  Run the task every three minutes
`->everyFourMinutes();`  |  Run the task every four minutes
`->everyFiveMinutes();`  |  Run the task every five minutes
`->everyTenMinutes();`  |  Run the task every ten minutes
`->everyFifteenMinutes();`  |  Run the task every fifteen minutes
`->everyThirtyMinutes();`  |  Run the task every thirty minutes
`->hourly();`  |  Run the task every hour
`->hourlyAt(17);`  |  Run the task every hour at 17 minutes past the hour
`->everyTwoHours();`  |  Run the task every two hours
`->everyThreeHours();`  |  Run the task every three hours
`->everyFourHours();`  |  Run the task every four hours
`->everySixHours();`  |  Run the task every six hours
`->daily();`  |  Run the task every day at midnight
`->dailyAt('13:00');`  |  Run the task every day at 13:00
`->twiceDaily(1, 13);`  |  Run the task daily at 1:00 & 13:00
`->weekly();`  |  Run the task every Sunday at 00:00
`->weeklyOn(1, '8:00');`  |  Run the task every week on Monday at 8:00
`->monthly();`  |  Run the task on the first day of every month at 00:00
`->monthlyOn(4, '15:00');`  |  Run the task every month on the 4th at 15:00
`->twiceMonthly(1, 16, '13:00');`  |  Run the task monthly on the 1st and 16th at 13:00
`->lastDayOfMonth('15:00');` | Run the task on the last day of the month at 15:00
`->quarterly();` |  Run the task on the first day of every quarter at 00:00
`->yearly();`  |  Run the task on the first day of every year at 00:00
`->yearlyOn(6, 1, '17:00');`  |  Run the task every year on June 1st at 17:00
`->timezone('America/New_York');` | Set the timezone for the task
-->
메서드  | 설명
------------- | -------------
`->cron('* * * * *');`  |  사용자 정의 cron 스케줄로 작업을 실행합니다
`->everyMinute();`  |  1분마다 작업을 실행합니다
`->everyTwoMinutes();`  |  2분마다 작업을 실행합니다
`->everyThreeMinutes();`  |  3분마다 작업을 실행합니다
`->everyFourMinutes();`  |  4분마다 작업을 실행합니다
`->everyFiveMinutes();`  |  5분마다 작업을 실행합니다
`->everyTenMinutes();`  |  10분마다 작업을 실행합니다
`->everyFifteenMinutes();`  |  15분마다 작업을 실행합니다
`->everyThirtyMinutes();`  |  30분마다 작업을 실행합니다
`->hourly();`  |  1시간마다 작업을 실행합니다
`->hourlyAt(17);`  |  매 시 17분마다 작업을 실행합니다
`->everyTwoHours();`  |  2시간마다 작업을 실행합니다
`->everyThreeHours();`  |  3시간마다 작업을 실행합니다
`->everyFourHours();`  |  4시간마다 작업을 실행합니다
`->everySixHours();`  |  6시간마다 작업을 실행합니다
`->daily();`  |  매일 자정에 작업을 실행합니다
`->dailyAt('13:00');`  |  매일 13:00에 작업을 실행합니다
`->twiceDaily(1, 13);`  |  매일 1:00과 13:00에 작업을 실행합니다
`->weekly();`  |  매주 일요일 00:00에 작업을 실행합니다
`->weeklyOn(1, '8:00');`  |  매주 월요일 8:00에 작업을 실행합니다
`->monthly();`  |  매월 1일 00:00에 작업을 실행합니다
`->monthlyOn(4, '15:00');`  |  매월 4일 15:00에 작업을 실행합니다
`->twiceMonthly(1, 16, '13:00');`  |  매월 1일, 16일 13:00에 작업을 실행합니다
`->lastDayOfMonth('15:00');` | 매월 마지막 날 15:00에 작업을 실행합니다
`->quarterly();` |  매 분기 1일 00:00에 작업을 실행합니다
`->yearly();`  |  매년 1월 1일 00:00에 작업을 실행합니다
`->yearlyOn(6, 1, '17:00');`  |  매년 6월 1일 17:00에 작업을 실행합니다
`->timezone('America/New_York');` | 작업에 적용할 타임존을 설정합니다

<!-- These methods may be combined with additional constraints to create even more finely tuned schedules that only run on certain days of the week. For example, you may schedule a command to run weekly on Monday: -->
이 메서드들은 추가 제약 조건과 결합해, 더욱 세밀하게 특정 요일에만 동작하도록 스케줄을 조정할 수 있습니다. 예를 들어, 월요일마다 작업을 예약할 수도 있습니다.

```
// Run once per week on Monday at 1 PM...
$schedule->call(function () {
    //
})->weekly()->mondays()->at('13:00');

// Run hourly from 8 AM to 5 PM on weekdays...
$schedule->command('foo')
          ->weekdays()
          ->hourly()
          ->timezone('America/Chicago')
          ->between('8:00', '17:00');
```

<!-- A list of additional schedule constraints may be found below: -->
아래는 추가로 사용할 수 있는 스케줄 제약 조건입니다.

<!--
Method  | Description
------------- | -------------
`->weekdays();`  |  Limit the task to weekdays
`->weekends();`  |  Limit the task to weekends
`->sundays();`  |  Limit the task to Sunday
`->mondays();`  |  Limit the task to Monday
`->tuesdays();`  |  Limit the task to Tuesday
`->wednesdays();`  |  Limit the task to Wednesday
`->thursdays();`  |  Limit the task to Thursday
`->fridays();`  |  Limit the task to Friday
`->saturdays();`  |  Limit the task to Saturday
`->days(array\|mixed);`  |  Limit the task to specific days
`->between($startTime, $endTime);`  |  Limit the task to run between start and end times
`->unlessBetween($startTime, $endTime);`  |  Limit the task to not run between start and end times
`->when(Closure);`  |  Limit the task based on a truth test
`->environments($env);`  |  Limit the task to specific environments
-->
메서드  | 설명
------------- | -------------
`->weekdays();`  |  평일에만 작업 실행
`->weekends();`  |  주말에만 작업 실행
`->sundays();`  |  일요일에만 작업 실행
`->mondays();`  |  월요일에만 작업 실행
`->tuesdays();`  |  화요일에만 작업 실행
`->wednesdays();`  |  수요일에만 작업 실행
`->thursdays();`  |  목요일에만 작업 실행
`->fridays();`  |  금요일에만 작업 실행
`->saturdays();`  |  토요일에만 작업 실행
`->days(array\|mixed);`  |  특정 요일(들)만 작업 실행
`->between($startTime, $endTime);`  |  특정 시간대에만 작업 실행
`->unlessBetween($startTime, $endTime);`  |  지정한 시간대에는 작업 실행 금지
`->when(Closure);`  |  주어진 조건(클로저의 반환값)에 따라 작업 실행
`->environments($env);`  |  지정한 환경에서만 작업 실행

<a name="day-constraints"></a>
<!-- #### Day Constraints -->
#### Day Constraints

<!-- The `days` method may be used to limit the execution of a task to specific days of the week. For example, you may schedule a command to run hourly on Sundays and Wednesdays: -->
`days` 메서드를 사용해 작업을 특정 요일로 한정할 수 있습니다. 예를 들어, 일요일과 수요일마다 매시 명령어를 실행하도록 예약할 수 있습니다.

```
$schedule->command('emails:send')
                ->hourly()
                ->days([0, 3]);
```

<!-- Alternatively, you may use the constants available on the `Illuminate\Console\Scheduling\Schedule` class when defining the days on which a task should run: -->
또는, 작업을 실행할 요일 정의 시 `Illuminate\Console\Scheduling\Schedule` 클래스의 상수를 사용할 수도 있습니다.

```
use Illuminate\Console\Scheduling\Schedule;

$schedule->command('emails:send')
                ->hourly()
                ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
<!-- #### Between Time Constraints -->
#### Between Time Constraints

<!-- The `between` method may be used to limit the execution of a task based on the time of day: -->
`between` 메서드를 사용하면, 작업이 특정 시간대에만 실행되도록 제한할 수 있습니다.

```
$schedule->command('emails:send')
                    ->hourly()
                    ->between('7:00', '22:00');
```

<!-- Similarly, the `unlessBetween` method can be used to exclude the execution of a task for a period of time: -->
마찬가지로, `unlessBetween` 메서드를 사용하면, 정해진 시간대에는 작업이 실행되지 않도록 할 수 있습니다.

```
$schedule->command('emails:send')
                    ->hourly()
                    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
<!-- #### Truth Test Constraints -->
#### Truth Test Constraints

<!-- The `when` method may be used to limit the execution of a task based on the result of a given truth test. In other words, if the given closure returns `true`, the task will execute as long as no other constraining conditions prevent the task from running: -->
`when` 메서드를 이용하면, 주어진 조건(클로저의 반환값이 true인 경우)에 따라 작업 실행을 제한할 수 있습니다. 즉, 지정한 클로저가 `true`를 반환하면 다른 제약 조건에 막히지 않는 한 해당 작업이 실행됩니다.

```
$schedule->command('emails:send')->daily()->when(function () {
    return true;
});
```

<!-- The `skip` method may be seen as the inverse of `when`. If the `skip` method returns `true`, the scheduled task will not be executed: -->
`skip` 메서드는 `when`의 반대 역할을 합니다. `skip`이 `true`를 반환하면, 예약된 작업은 실행되지 않습니다.

```
$schedule->command('emails:send')->daily()->skip(function () {
    return true;
});
```

<!-- When using chained `when` methods, the scheduled command will only execute if all `when` conditions return `true`. -->
`when` 메서드를 여러 개 체이닝해서 사용할 경우, 모든 `when` 조건이 `true`를 반환해야만 예약된 명령어가 실행됩니다.

<a name="environment-constraints"></a>
<!-- #### Environment Constraints -->
#### Environment Constraints

<!-- The `environments` method may be used to execute tasks only on the given environments (as defined by the `APP_ENV` [environment variable](/docs/8.x/configuration#environment-configuration)): -->
`environments` 메서드를 사용하면, 지정한 [environment variable](/docs/8.x/configuration#environment-configuration)의 값(`APP_ENV`)에 해당하는 환경에서만 작업이 실행되게 할 수 있습니다.

```
$schedule->command('emails:send')
            ->daily()
            ->environments(['staging', 'production']);
```

<a name="timezones"></a>
<!-- ### Timezones -->
### Timezones

<!-- Using the `timezone` method, you may specify that a scheduled task's time should be interpreted within a given timezone: -->
`timezone` 메서드를 사용해, 예약 작업이 특정 타임존을 기준으로 동작하도록 지정할 수 있습니다.

```
$schedule->command('report:generate')
         ->timezone('America/New_York')
         ->at('2:00')
```

<!-- If you are repeatedly assigning the same timezone to all of your scheduled tasks, you may wish to define a `scheduleTimezone` method in your `App\Console\Kernel` class. This method should return the default timezone that should be assigned to all scheduled tasks: -->
모든 예약 작업에 동일한 타임존을 반복적으로 지정하고 있다면, `App\Console\Kernel` 클래스에 `scheduleTimezone` 메서드를 정의해 기본 타임존 값을 반환하도록 할 수 있습니다.

```
/**
 * Get the timezone that should be used by default for scheduled events.
 *
 * @return \DateTimeZone|string|null
 */
protected function scheduleTimezone()
{
    return 'America/Chicago';
}
```

> [!NOTE]
> 일부 타임존은 일광 절약 시간제(Daylight Saving Time, DST)를 사용합니다. 이로 인해 일광 절약 시간 변동 시 예약 작업이 두 번 실행되거나 아예 실행되지 않을 수 있습니다. 이러한 문제가 발생할 수 있으므로, 가능하다면 타임존 기반 스케줄링은 피하는 것이 좋습니다.

<a name="preventing-task-overlaps"></a>
<!-- ### Preventing Task Overlaps -->
### Preventing Task Overlaps

<!-- By default, scheduled tasks will be run even if the previous instance of the task is still running. To prevent this, you may use the `withoutOverlapping` method: -->
기본적으로 예약된 작업은 이전 작업 인스턴스가 아직 실행 중이더라도 또다시 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용할 수 있습니다.

```
$schedule->command('emails:send')->withoutOverlapping();
```

<!-- In this example, the `emails:send` [Artisan command](/docs/8.x/artisan) will be run every minute if it is not already running. The `withoutOverlapping` method is especially useful if you have tasks that vary drastically in their execution time, preventing you from predicting exactly how long a given task will take. -->
이 예시에서는 `emails:send` [Artisan command](/docs/8.x/artisan)가 현재 실행 중이지 않을 때에만 1분마다 실행됩니다. `withoutOverlapping` 메서드는 실행 시간 편차가 큰 작업에도 유용하게 사용할 수 있습니다.

<!-- If needed, you may specify how many minutes must pass before the "without overlapping" lock expires. By default, the lock will expire after 24 hours: -->
필요하다면, "중복 방지"를 위한 락(lock)이 만료되기까지 최대 대기 시간을 분 단위로 지정할 수 있습니다. 기본값은 24시간입니다.

```
$schedule->command('emails:send')->withoutOverlapping(10);
```

<a name="running-tasks-on-one-server"></a>
<!-- ### Running Tasks On One Server -->
### Running Tasks On One Server

> [!NOTE]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, `redis` 중 하나여야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<!-- If your application's scheduler is running on multiple servers, you may limit a scheduled job to only execute on a single server. For instance, assume you have a scheduled task that generates a new report every Friday night. If the task scheduler is running on three worker servers, the scheduled task will run on all three servers and generate the report three times. Not good! -->
애플리케이션의 스케줄러가 여러 서버에서 동작 중인 경우, 예약된 작업 중 일부를 한 서버에서만 실행하도록 제한할 수 있습니다. 예를 들어, 매주 금요일 밤에 새 리포트를 생성하는 작업이 있다고 가정해보겠습니다. 스케줄러가 세 대의 워커 서버에서 동작하고 있다면, 이 예약 작업은 세 서버에서 모두 실행되어 리포트가 세 번 생성됩니다. 이는 바람직하지 않겠죠!

<!-- To indicate that the task should run on only one server, use the `onOneServer` method when defining the scheduled task. The first server to obtain the task will secure an atomic lock on the job to prevent other servers from running the same task at the same time: -->
이럴 때는 예약 작업을 정의할 때 `onOneServer` 메서드를 사용하면 해당 작업이 오직 한 서버에서만 실행됩니다. 가장 먼저 락을 얻은 서버에서 원자적(atomic)으로 락이 걸려, 다른 서버에서는 같은 작업이 동시에 실행되지 않습니다.

```
$schedule->command('report:generate')
                ->fridays()
                ->at('17:00')
                ->onOneServer();
```

<a name="background-tasks"></a>
<!-- ### Background Tasks -->
### Background Tasks

<!-- By default, multiple tasks scheduled at the same time will execute sequentially based on the order they are defined in your `schedule` method. If you have long-running tasks, this may cause subsequent tasks to start much later than anticipated. If you would like to run tasks in the background so that they may all run simultaneously, you may use the `runInBackground` method: -->
기본적으로 여러 작업이 동시에 예약되어 있으면, `schedule` 메서드에 정의된 순서대로 순차적으로 실행됩니다. 실행 시간이 긴 작업이 있으면, 그 뒤에 있는 작업이 예정보다 늦게 시작될 수 있습니다. 여러 작업을 동시에 백그라운드에서 병렬로 실행하고 싶다면, `runInBackground` 메서드를 사용할 수 있습니다.

```
$schedule->command('analytics:report')
         ->daily()
         ->runInBackground();
```

> [!NOTE]
> `runInBackground` 메서드는 `command` 또는 `exec` 메서드로 예약한 작업에서만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
<!-- ### Maintenance Mode -->
### Maintenance Mode

<!-- Your application's scheduled tasks will not run when the application is in [maintenance mode](/docs/8.x/configuration#maintenance-mode), since we don't want your tasks to interfere with any unfinished maintenance you may be performing on your server. However, if you would like to force a task to run even in maintenance mode, you may call the `evenInMaintenanceMode` method when defining the task: -->
애플리케이션이 [maintenance mode](/docs/8.x/configuration#maintenance-mode)일 때는 예약된 작업이 실행되지 않습니다. 이는, 서버에서 완료되지 않은 유지 보수 작업이 있는 경우, 예약 작업이 그 과정에 영향을 주지 않도록 하기 위해서입니다. 하지만 유지 보수 모드에서도 특정 작업만은 꼭 실행해야 한다면, 작업 정의 시 `evenInMaintenanceMode` 메서드를 호출하면 강제로 실행할 수 있습니다.

```
$schedule->command('emails:send')->evenInMaintenanceMode();
```

<a name="running-the-scheduler"></a>
<!-- ## Running The Scheduler -->
## Running The Scheduler

<!-- Now that we have learned how to define scheduled tasks, let's discuss how to actually run them on our server. The `schedule:run` Artisan command will evaluate all of your scheduled tasks and determine if they need to run based on the server's current time. -->
이제 예약 작업을 정의하는 방법을 배웠으니, 실제로 서버에서 이 작업들을 실행하는 방법에 대해 알아보겠습니다. `schedule:run` 아티즌 명령어는 예약된 모든 작업을 서버의 현재 시각 기준으로 평가해, 실행해야 할 작업을 판단합니다.

<!-- So, when using Laravel's scheduler, we only need to add a single cron configuration entry to our server that runs the `schedule:run` command every minute. If you do not know how to add cron entries to your server, consider using a service such as [Laravel Forge](https://forge.laravel.com) which can manage the cron entries for you: -->
Laravel의 스케줄러를 사용할 때는 서버에 단 하나의 cron 엔트리만 추가하면 되며, 이 엔트리는 매분마다 `schedule:run` 명령어를 실행하도록 설정하면 됩니다. 서버에 cron 엔트리를 어떻게 추가하는지 모른다면, [Laravel Forge](https://forge.laravel.com)와 같은 서비스를 이용해 cron 관리를 자동화할 수 있습니다.

<!--     * * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1 -->
    * * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1

<a name="running-the-scheduler-locally"></a>
<!-- ## Running The Scheduler Locally -->
## Running The Scheduler Locally

<!-- Typically, you would not add a scheduler cron entry to your local development machine. Instead, you may use the `schedule:work` Artisan command. This command will run in the foreground and invoke the scheduler every minute until you terminate the command: -->
일반적으로 로컬 개발 환경에서는 scheduler cron 엔트리를 추가하지 않습니다. 대신 `schedule:work` 아티즌 명령어를 사용할 수 있습니다. 이 명령어는 포그라운드에서 실행되며, 수동으로 중단할 때까지 매분마다 스케줄러를 호출합니다.

```
php artisan schedule:work
```

<a name="task-output"></a>
<!-- ## Task Output -->
## Task Output

<!-- The Laravel scheduler provides several convenient methods for working with the output generated by scheduled tasks. First, using the `sendOutputTo` method, you may send the output to a file for later inspection: -->
Laravel 스케줄러는 예약 작업에서 만들어진 출력을 관리하기 위해 여러 편리한 메서드를 제공합니다. 우선, `sendOutputTo` 메서드로 작업의 실행 결과를 파일에 저장할 수 있습니다.

```
$schedule->command('emails:send')
         ->daily()
         ->sendOutputTo($filePath);
```

<!-- If you would like to append the output to a given file, you may use the `appendOutputTo` method: -->
출력을 파일에 덧붙이고 싶다면, `appendOutputTo` 메서드를 사용할 수 있습니다.

```
$schedule->command('emails:send')
         ->daily()
         ->appendOutputTo($filePath);
```

<!-- Using the `emailOutputTo` method, you may email the output to an email address of your choice. Before emailing the output of a task, you should configure Laravel's [email services](/docs/8.x/mail): -->
`emailOutputTo` 메서드를 사용하면, 작업의 실행 결과 출력을 원하는 이메일 주소로 전송할 수 있습니다. 이메일로 작업 출력을 전송하려면 먼저 Laravel의 [email services](/docs/8.x/mail)를 설정해 두어야 합니다.

```
$schedule->command('report:generate')
         ->daily()
         ->sendOutputTo($filePath)
         ->emailOutputTo('taylor@example.com');
```

<!-- If you only want to email the output if the scheduled Artisan or system command terminates with a non-zero exit code, use the `emailOutputOnFailure` method: -->
예약된 아티즌 명령어나 시스템 명령어가 0이 아닌 종료 코드를 반환할 때만 출력 결과를 이메일로 받고 싶다면, `emailOutputOnFailure` 메서드를 사용하면 됩니다.

```
$schedule->command('report:generate')
         ->daily()
         ->emailOutputOnFailure('taylor@example.com');
```

> [!NOTE]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command` 및 `exec` 메서드에 정의된 작업에서만 사용할 수 있습니다.

<a name="task-hooks"></a>
<!-- ## Task Hooks -->
## Task Hooks

<!-- Using the `before` and `after` methods, you may specify code to be executed before and after the scheduled task is executed: -->
`before`와 `after` 메서드를 사용하면, 예약 작업 실행 전후에 특정 코드를 실행하도록 지정할 수 있습니다.

```
$schedule->command('emails:send')
         ->daily()
         ->before(function () {
             // The task is about to execute...
         })
         ->after(function () {
             // The task has executed...
         });
```

<!-- The `onSuccess` and `onFailure` methods allow you to specify code to be executed if the scheduled task succeeds or fails. A failure indicates that the scheduled Artisan or system command terminated with a non-zero exit code: -->
`onSuccess`와 `onFailure` 메서드를 사용하면, 예약 작업이 성공하거나 실패했을 때 실행할 코드를 등록할 수 있습니다. 작업이 실패했다는 뜻은, 예약된 아티즌 명령어나 시스템 명령어가 0이 아닌 종료 코드를 반환한 경우입니다.

```
$schedule->command('emails:send')
         ->daily()
         ->onSuccess(function () {
             // The task succeeded...
         })
         ->onFailure(function () {
             // The task failed...
         });
```

<!-- If output is available from your command, you may access it in your `after`, `onSuccess` or `onFailure` hooks by type-hinting an `Illuminate\Support\Stringable` instance as the `$output` argument of your hook's closure definition: -->
명령어 실행 결과(output)를 사용할 수 있다면, `after`, `onSuccess`, `onFailure` 후크의 클로저 인자로 `Illuminate\Support\Stringable` 타입의 `$output` 인수를 명시하여 해당 출력을 받을 수 있습니다.

```
use Illuminate\Support\Stringable;

$schedule->command('emails:send')
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
`pingBefore` 와 `thenPing` 메서드를 사용하면, 예약 작업 실행 전후에 지정한 URL로 자동으로 핑(ping) 요청을 보낼 수 있습니다. 이 기능은 [Envoyer](https://envoyer.io)와 같은 외부 서비스에 예약 작업 시작 또는 완료를 실시간으로 알리는 용도로 유용하게 활용할 수 있습니다.

```
$schedule->command('emails:send')
         ->daily()
         ->pingBefore($url)
         ->thenPing($url);
```

<!-- The `pingBeforeIf` and `thenPingIf` methods may be used to ping a given URL only if a given condition is `true`: -->
`pingBeforeIf` 및 `thenPingIf` 메서드는, 주어진 조건이 `true`인 경우에만 지정한 URL로 핑을 보냅니다.

```
$schedule->command('emails:send')
         ->daily()
         ->pingBeforeIf($condition, $url)
         ->thenPingIf($condition, $url);
```

<!-- The `pingOnSuccess` and `pingOnFailure` methods may be used to ping a given URL only if the task succeeds or fails. A failure indicates that the scheduled Artisan or system command terminated with a non-zero exit code: -->
`pingOnSuccess` 및 `pingOnFailure` 메서드는, 작업이 성공하거나 실패했을 때만 각각 지정한 URL로 핑을 전송합니다. 실패란 예약된 아티즌 또는 시스템 명령어가 0이 아닌 종료 코드를 반환한 경우를 의미합니다.

```
$schedule->command('emails:send')
         ->daily()
         ->pingOnSuccess($successUrl)
         ->pingOnFailure($failureUrl);
```

<!-- All of the ping methods require the Guzzle HTTP library. Guzzle is typically installed in all new Laravel projects by default, but, you may manually install Guzzle into your project using the Composer package manager if it has been accidentally removed: -->
모든 핑(ping) 관련 메서드는 Guzzle HTTP 라이브러리가 필요합니다. Guzzle은 모든 신규 Laravel 프로젝트에 기본적으로 포함되어 있지만, 혹시 제거된 경우 Composer 패키지 매니저를 사용해 직접 설치할 수 있습니다.

```
composer require guzzlehttp/guzzle
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- If needed, you may listen to [events](/docs/8.x/events) dispatched by the scheduler. Typically, event listener mappings will be defined within your application's `App\Providers\EventServiceProvider` class: -->
필요하다면, 스케줄러에서 발생하는 [events](/docs/8.x/events)에 리스너를 등록해 동작을 확장할 수 있습니다. 보통 이벤트 리스너 매핑은 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에 정의합니다.

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Console\Events\ScheduledTaskStarting' => [
        'App\Listeners\LogScheduledTaskStarting',
    ],

    'Illuminate\Console\Events\ScheduledTaskFinished' => [
        'App\Listeners\LogScheduledTaskFinished',
    ],

    'Illuminate\Console\Events\ScheduledBackgroundTaskFinished' => [
        'App\Listeners\LogScheduledBackgroundTaskFinished',
    ],

    'Illuminate\Console\Events\ScheduledTaskSkipped' => [
        'App\Listeners\LogScheduledTaskSkipped',
    ],

    'Illuminate\Console\Events\ScheduledTaskFailed' => [
        'App\Listeners\LogScheduledTaskFailed',
    ],
];
```
