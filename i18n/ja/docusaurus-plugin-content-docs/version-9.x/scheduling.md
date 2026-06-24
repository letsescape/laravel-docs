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
以前は、サーバー上でスケジュールする必要があるタスクごとに cron 構成エントリを作成したかもしれません。ただし、タスクスケジュールがソース管理に含まれなくなり、既存の cron エントリを表示したり追加のエントリを追加するにはサーバーに SSH 接続する必要があるため、これはすぐに面倒になる可能性があります。

<!-- Laravel's command scheduler offers a fresh approach to managing scheduled tasks on your server. The scheduler allows you to fluently and expressively define your command schedule within your Laravel application itself. When using the scheduler, only a single cron entry is needed on your server. Your task schedule is defined in the `app/Console/Kernel.php` file's `schedule` method. To help you get started, a simple example is defined within the method. -->
Laravel のコマンド スケジューラは、サーバー上でスケジュールされたタスクを管理するための新しいアプローチを提供します。スケジューラを使用すると、Laravel アプリケーション自体内でコマンド スケジュールを流暢かつ表現力豊かに定義できます。スケジューラを使用する場合、サーバー上に必要な cron エントリは 1 つだけです。タスクスケジュールは、`app/Console/Kernel.php` ファイルの `schedule` メソッドで定義されます。開始しやすいように、メソッド内で簡単な例が定義されています。

<a name="defining-schedules"></a>
<!-- ## Defining Schedules -->
## Defining Schedules

<!-- You may define all of your scheduled tasks in the `schedule` method of your application's `App\Console\Kernel` class. To get started, let's take a look at an example. In this example, we will schedule a closure to be called every day at midnight. Within the closure we will execute a database query to clear a table: -->
スケジュールされたタスクはすべて、アプリケーションの `App\Console\Kernel` クラスの `schedule` メソッドで定義できます。まず、例を見てみましょう。この例では、毎日深夜に呼び出されるクロージャをスケジュールします。クロージャ内でデータベース クエリを実行してテーブルをクリアします。

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
クロージャを使用したスケジュールに加えて、[invokable objects](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke) をスケジュールすることもできます。呼び出し可能なオブジェクトは、`__invoke` メソッドを含む単純な PHP クラスです。

```
$schedule->call(new DeleteRecentUsers)->daily();
```

<!-- If you would like to view an overview of your scheduled tasks and the next time they are scheduled to run, you may use the `schedule:list` Artisan command: -->
スケジュールされたタスクの概要と次回の実行スケジュールを確認したい場合は、`schedule:list` Artisan コマンドを使用できます。

```bash
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
<!-- ### Scheduling Artisan Commands -->
### Scheduling Artisan Commands

<!-- In addition to scheduling closures, you may also schedule [Artisan commands](/docs/9.x/artisan) and system commands. For example, you may use the `command` method to schedule an Artisan command using either the command's name or class. -->
クロージャのスケジュールに加えて、[Artisan commands](/docs/9.x/artisan) およびシステム コマンドもスケジュールできます。たとえば、`command` メソッドを使用して、コマンドの名前またはクラスを使用してArtisan コマンドをスケジュールできます。

<!-- When scheduling Artisan commands using the command's class name, you may pass an array of additional command-line arguments that should be provided to the command when it is invoked: -->
コマンドのクラス名を使用してArtisan コマンドをスケジュールする場合、コマンドの呼び出し時にコマンドに指定する必要がある追加のコマンドライン引数の配列を渡すことができます。

```
use App\Console\Commands\SendEmailsCommand;

$schedule->command('emails:send Taylor --force')->daily();

$schedule->command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
<!-- ### Scheduling Queued Jobs -->
### Scheduling Queued Jobs

<!-- The `job` method may be used to schedule a [queued job](/docs/9.x/queues). This method provides a convenient way to schedule queued jobs without using the `call` method to define closures to queue the job: -->
`job` メソッドは、[queued job](/docs/9.x/queues) をスケジュールするために使用できます。このメソッドは、ジョブをキューに入れるクロージャを定義する `call` メソッドを使用せずに、キューに入れられたジョブをスケジュールする便利な方法を提供します。

```
use App\Jobs\Heartbeat;

$schedule->job(new Heartbeat)->everyFiveMinutes();
```

<!-- Optional second and third arguments may be provided to the `job` method which specifies the queue name and queue connection that should be used to queue the job: -->
オプションの 2 番目と 3 番目の引数を `job` メソッドに指定して、ジョブをキューに入れるために使用するキュー名とキュー接続を指定できます。

```
use App\Jobs\Heartbeat;

// Dispatch the job to the "heartbeats" queue on the "sqs" connection...
$schedule->job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
<!-- ### Scheduling Shell Commands -->
### Scheduling Shell Commands

<!-- The `exec` method may be used to issue a command to the operating system: -->
`exec` メソッドは、オペレーティング システムにコマンドを発行するために使用できます。

```
$schedule->exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
<!-- ### Schedule Frequency Options -->
### Schedule Frequency Options

<!-- We've already seen a few examples of how you may configure a task to run at specified intervals. However, there are many more task schedule frequencies that you may assign to a task: -->
指定した間隔でタスクを実行するように構成する方法の例をいくつか見てきました。ただし、タスクに割り当てることができるタスクスケジュールの頻度は他にもたくさんあります。

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
`->everyOddHour();`  |  Run the task every odd hour
`->everyTwoHours();`  |  Run the task every two hours
`->everyThreeHours();`  |  Run the task every three hours
`->everyFourHours();`  |  Run the task every four hours
`->everySixHours();`  |  Run the task every six hours
`->daily();`  |  Run the task every day at midnight
`->dailyAt('13:00');`  |  Run the task every day at 13:00
`->twiceDaily(1, 13);`  |  Run the task daily at 1:00 & 13:00
`->twiceDailyAt(1, 13, 15);`  |  Run the task daily at 1:15 & 13:15
`->weekly();`  |  Run the task every Sunday at 00:00
`->weeklyOn(1, '8:00');`  |  Run the task every week on Monday at 8:00
`->monthly();`  |  Run the task on the first day of every month at 00:00
`->monthlyOn(4, '15:00');`  |  Run the task every month on the 4th at 15:00
`->twiceMonthly(1, 16, '13:00');`  |  Run the task monthly on the 1st and 16th at 13:00
`->lastDayOfMonth('15:00');` | Run the task on the last day of the month at 15:00
`->quarterly();` |  Run the task on the first day of every quarter at 00:00
`->quarterlyOn(4, '14:00');` |  Run the task every quarter on the 4th at 14:00
`->yearly();`  |  Run the task on the first day of every year at 00:00
`->yearlyOn(6, 1, '17:00');`  |  Run the task every year on June 1st at 17:00
`->timezone('America/New_York');` | Set the timezone for the task
-->
方法 |説明
------------- | -------------
`->cron('* * * * *');` |  カスタム cron スケジュールでタスクを実行する
`->everyMinute();` |  タスクを毎分実行する
`->everyTwoMinutes();` |  タスクを 2 分ごとに実行する
`->everyThreeMinutes();` |  タスクを 3 分ごとに実行する
`->everyFourMinutes();` |  タスクを 4 分ごとに実行する
`->everyFiveMinutes();` |  タスクを 5 分ごとに実行する
`->everyTenMinutes();` |  タスクを 10 分ごとに実行する
`->everyFifteenMinutes();` |  タスクを 15 分ごとに実行する
`->everyThirtyMinutes();` |  タスクを 30 分ごとに実行する
`->hourly();` |  タスクを 1 時間ごとに実行する
`->hourlyAt(17);` |  タスクを毎時 17 分に実行します
`->everyOddHour();` |  奇数時間ごとにタスクを実行する
`->everyTwoHours();` |  タスクを 2 時間ごとに実行する
`->everyThreeHours();` |  タスクを 3 時間ごとに実行する
`->everyFourHours();` |  タスクを 4 時間ごとに実行する
`->everySixHours();` |  タスクを 6 時間ごとに実行する
`->daily();` |  毎日深夜にタスクを実行する
`->dailyAt('13:00');` |  毎日 13:00 にタスクを実行します
`->twiceDaily(1, 13);` |  タスクを毎日 1:00 と 13:00 に実行します
`->twiceDailyAt(1, 13, 15);` |  毎日 1:15 と 13:15 にタスクを実行します
`->weekly();` |  タスクを毎週日曜日の 00:00 に実行します
`->weeklyOn(1, '8:00');` |  タスクを毎週月曜日の 8:00 に実行します
`->monthly();` |  タスクを毎月 1 日の 00:00 に実行します。
`->monthlyOn(4, '15:00');` |  毎月 4 日の 15:00 にタスクを実行します
`->twiceMonthly(1, 16, '13:00');` |  毎月 1 日と 16 日の 13:00 にタスクを実行します。
`->lastDayOfMonth('15:00');` |毎月の最終日の 15:00 にタスクを実行します。
`->quarterly();` |  各四半期の初日の 00:00 にタスクを実行します。
`->quarterlyOn(4, '14:00');` |  タスクを四半期ごとに 4 日の 14:00 に実行します。
`->yearly();` |  毎年初日の 00:00 にタスクを実行します。
`->yearlyOn(6, 1, '17:00');` |  毎年 6 月 1 日の 17:00 にタスクを実行します。
`->timezone('America/New_York');` |タスクのタイムゾーンを設定する

<!-- These methods may be combined with additional constraints to create even more finely tuned schedules that only run on certain days of the week. For example, you may schedule a command to run weekly on Monday: -->
これらの方法を追加の制約と組み合わせて、特定の曜日にのみ実行するさらに細かく調整されたスケジュールを作成できます。たとえば、コマンドを毎週月曜日に実行するようにスケジュールできます。

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
追加のスケジュール制約のリストは以下にあります。

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
方法 |説明
------------- | -------------
`->weekdays();` |  タスクを平日に限定する
`->weekends();` |  タスクを週末に限定する
`->sundays();` |  タスクを日曜日に限定する
`->mondays();` |  タスクを月曜日に限定する
`->tuesdays();` |  タスクを火曜日に限定する
`->wednesdays();` |  タスクを水曜日に限定する
`->thursdays();` |  タスクを木曜日に限定する
`->fridays();` |  タスクを金曜日に限定する
`->saturdays();` |  タスクを土曜日に限定する
`->days(array\|mixed);`  |  タスクを特定の日に限定する
`->between($startTime, $endTime);` |  開始時間と終了時間の間に実行するタスクを制限する
`->unlessBetween($startTime, $endTime);` |  開始時間と終了時間の間にタスクが実行されないように制限する
`->when(Closure);` |  真実のテストに基づいてタスクを制限する
`->environments($env);` |  タスクを特定の環境に限定する

<a name="day-constraints"></a>
<!-- #### Day Constraints -->
#### Day Constraints

<!-- The `days` method may be used to limit the execution of a task to specific days of the week. For example, you may schedule a command to run hourly on Sundays and Wednesdays: -->
`days` メソッドを使用すると、タスクの実行を特定の曜日に制限できます。たとえば、日曜日と水曜日に 1 時間ごとにコマンドを実行するようにスケジュールできます。

```
$schedule->command('emails:send')
                ->hourly()
                ->days([0, 3]);
```

<!-- Alternatively, you may use the constants available on the `Illuminate\Console\Scheduling\Schedule` class when defining the days on which a task should run: -->
あるいは、タスクを実行する日を定義するときに、`Illuminate\Console\Scheduling\Schedule` クラスで利用可能な定数を使用することもできます。

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
`between` メソッドは、時刻に基づいてタスクの実行を制限するために使用できます。

```
$schedule->command('emails:send')
                    ->hourly()
                    ->between('7:00', '22:00');
```

<!-- Similarly, the `unlessBetween` method can be used to exclude the execution of a task for a period of time: -->
同様に、`unlessBetween` メソッドを使用して、一定期間タスクの実行を除外できます。

```
$schedule->command('emails:send')
                    ->hourly()
                    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
<!-- #### Truth Test Constraints -->
#### Truth Test Constraints

<!-- The `when` method may be used to limit the execution of a task based on the result of a given truth test. In other words, if the given closure returns `true`, the task will execute as long as no other constraining conditions prevent the task from running: -->
`when` メソッドは、指定された真理値テストの結果に基づいてタスクの実行を制限するために使用できます。つまり、指定されたクロージャが `true` を返す場合、他の制約条件によってタスクの実行が妨げられない限り、タスクは実行されます。

```
$schedule->command('emails:send')->daily()->when(function () {
    return true;
});
```

<!-- The `skip` method may be seen as the inverse of `when`. If the `skip` method returns `true`, the scheduled task will not be executed: -->
`skip` メソッドは、`when` の逆と見なすことができます。 `skip` メソッドが `true` を返した場合、スケジュールされたタスクは実行されません。

```
$schedule->command('emails:send')->daily()->skip(function () {
    return true;
});
```

<!-- When using chained `when` methods, the scheduled command will only execute if all `when` conditions return `true`. -->
連鎖した `when` メソッドを使用する場合、スケジュールされたコマンドは、すべての `when` 条件が `true` を返した場合にのみ実行されます。

<a name="environment-constraints"></a>
<!-- #### Environment Constraints -->
#### Environment Constraints

<!-- The `environments` method may be used to execute tasks only on the given environments (as defined by the `APP_ENV` [environment variable](/docs/9.x/configuration#environment-configuration)): -->
`environments` メソッドは、指定された環境 (`APP_ENV` [environment variable](/docs/9.x/configuration#environment-configuration) で定義) でのみタスクを実行するために使用できます。

```
$schedule->command('emails:send')
            ->daily()
            ->environments(['staging', 'production']);
```

<a name="timezones"></a>
<!-- ### Timezones -->
### Timezones

<!-- Using the `timezone` method, you may specify that a scheduled task's time should be interpreted within a given timezone: -->
`timezone` メソッドを使用すると、スケジュールされたタスクの時間が特定のタイムゾーン内で解釈されるように指定できます。

```
$schedule->command('report:generate')
         ->timezone('America/New_York')
         ->at('2:00')
```

<!-- If you are repeatedly assigning the same timezone to all of your scheduled tasks, you may wish to define a `scheduleTimezone` method in your `App\Console\Kernel` class. This method should return the default timezone that should be assigned to all scheduled tasks: -->
スケジュールされたすべてのタスクに同じタイムゾーンを繰り返し割り当てる場合は、`App\Console\Kernel` クラスで `scheduleTimezone` メソッドを定義するとよいでしょう。このメソッドは、スケジュールされたすべてのタスクに割り当てる必要があるデフォルトのタイムゾーンを返す必要があります。

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

> [!WARNING]
> 一部のタイムゾーンでは夏時間が採用されていることに注意してください。夏時間の変更が発生すると、スケジュールされたタスクが 2 回実行されるか、まったく実行されない場合があります。このため、可能な限りタイムゾーンのスケジュールを回避することをお勧めします。

<a name="preventing-task-overlaps"></a>
<!-- ### Preventing Task Overlaps -->
### Preventing Task Overlaps

<!-- By default, scheduled tasks will be run even if the previous instance of the task is still running. To prevent this, you may use the `withoutOverlapping` method: -->
デフォルトでは、スケジュールされたタスクは、タスクの前のインスタンスがまだ実行中であっても実行されます。これを防ぐには、`withoutOverlapping` メソッドを使用します。

```
$schedule->command('emails:send')->withoutOverlapping();
```

<!-- In this example, the `emails:send` [Artisan command](/docs/9.x/artisan) will be run every minute if it is not already running. The `withoutOverlapping` method is especially useful if you have tasks that vary drastically in their execution time, preventing you from predicting exactly how long a given task will take. -->
この例では、`emails:send` [Artisan command](/docs/9.x/artisan) がまだ実行されていない場合、1 分ごとに実行されます。 `withoutOverlapping` メソッドは、実行時間が大幅に異なるタスクがあり、特定のタスクにかかる時間を正確に予測できない場合に特に便利です。

<!-- If needed, you may specify how many minutes must pass before the "without overlapping" lock expires. By default, the lock will expire after 24 hours: -->
必要に応じて、「重複なし」ロックの有効期限が切れるまでに何分経過するかを指定できます。デフォルトでは、ロックは 24 時間後に期限切れになります。

```
$schedule->command('emails:send')->withoutOverlapping(10);
```

<!-- Behind the scenes, the `withoutOverlapping` method utilizes your application's [cache](/docs/9.x/cache) to obtain locks. If necessary, you can clear these cache locks using the `schedule:clear-cache` Artisan command. This is typically only necessary if a task becomes stuck due to an unexpected server problem. -->
バックグラウンドで、`withoutOverlapping` メソッドはアプリケーションの [cache](/docs/9.x/cache) を利用してロックを取得します。必要に応じて、`schedule:clear-cache` Artisan コマンドを使用してこれらのキャッシュ ロックをクリアできます。これは通常、予期しないサーバーの問題によりタスクが停止した場合にのみ必要になります。

<a name="running-tasks-on-one-server"></a>
<!-- ### Running Tasks On One Server -->
### Running Tasks On One Server

> [!WARNING]
> この機能を利用するには、アプリケーションは、アプリケーションのデフォルトのキャッシュ ドライバとして `database`、`memcached`、`dynamodb`、または `redis` キャッシュ ドライバを使用している必要があります。さらに、すべてのサーバーが同じ中央キャッシュ サーバーと通信している必要があります。

<!-- If your application's scheduler is running on multiple servers, you may limit a scheduled job to only execute on a single server. For instance, assume you have a scheduled task that generates a new report every Friday night. If the task scheduler is running on three worker servers, the scheduled task will run on all three servers and generate the report three times. Not good! -->
アプリケーションのスケジューラが複数のサーバーで実行されている場合は、スケジュールされたジョブを単一のサーバーでのみ実行するように制限できます。たとえば、毎週金曜日の夜に新しいレポートを生成するスケジュールされたタスクがあるとします。タスク スケジューラが 3 台のワーカー サーバーで実行されている場合、スケジュールされたタスクは 3 台すべてのサーバーで実行され、レポートが 3 回生成されます。良くない！

<!-- To indicate that the task should run on only one server, use the `onOneServer` method when defining the scheduled task. The first server to obtain the task will secure an atomic lock on the job to prevent other servers from running the same task at the same time: -->
タスクを 1 つのサーバー上でのみ実行する必要があることを示すには、スケジュールされたタスクを定義するときに `onOneServer` メソッドを使用します。タスクを取得した最初のサーバーは、ジョブのアトミック ロックを確保し、他のサーバーが同じタスクを同時に実行できないようにします。

```
$schedule->command('report:generate')
                ->fridays()
                ->at('17:00')
                ->onOneServer();
```

<a name="naming-unique-jobs"></a>
<!-- #### Naming Single Server Jobs -->
#### Naming Single Server Jobs

<!-- Sometimes you may need to schedule the same job to be dispatched with different parameters, while still instructing Laravel to run each permutation of the job on a single server. To accomplish this, you may assign each schedule definition a unique name via the `name` method: -->
場合によっては、単一サーバー上でジョブの各順列を実行するように Laravel に指示しながら、同じジョブを異なるパラメーターでディスパッチするようにスケジュールする必要がある場合があります。これを実現するには、`name` メソッドを使用して、各スケジュール定義に一意の名前を割り当てることができます。

```php
$schedule->job(new CheckUptime('https://laravel.com'))
            ->name('check_uptime:laravel.com')
            ->everyFiveMinutes()
            ->onOneServer();

$schedule->job(new CheckUptime('https://vapor.laravel.com'))
            ->name('check_uptime:vapor.laravel.com')
            ->everyFiveMinutes()
            ->onOneServer();
```

<!-- Similarly, scheduled closures must be assigned a name if they are intended to be run on one server: -->
同様に、スケジュールされたクロージャが 1 つのサーバー上で実行される場合は、名前を割り当てる必要があります。

```php
$schedule->call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```


<a name="background-tasks"></a>
<!-- ### Background Tasks -->
### Background Tasks

<!-- By default, multiple tasks scheduled at the same time will execute sequentially based on the order they are defined in your `schedule` method. If you have long-running tasks, this may cause subsequent tasks to start much later than anticipated. If you would like to run tasks in the background so that they may all run simultaneously, you may use the `runInBackground` method: -->
デフォルトでは、同時にスケジュールされた複数のタスクは、`schedule` メソッドで定義された順序に基づいて順次実行されます。長時間実行されるタスクがある場合、後続のタスクの開始が予想より大幅に遅くなる可能性があります。タスクをバックグラウンドで実行してすべてを同時に実行したい場合は、`runInBackground` メソッドを使用できます。

```
$schedule->command('analytics:report')
         ->daily()
         ->runInBackground();
```

> [!WARNING]
> `runInBackground` メソッドは、`command` および `exec` メソッドを介してタスクをスケジュールする場合にのみ使用できます。

<a name="maintenance-mode"></a>
<!-- ### Maintenance Mode -->
### Maintenance Mode

<!-- Your application's scheduled tasks will not run when the application is in [maintenance mode](/docs/9.x/configuration#maintenance-mode), since we don't want your tasks to interfere with any unfinished maintenance you may be performing on your server. However, if you would like to force a task to run even in maintenance mode, you may call the `evenInMaintenanceMode` method when defining the task: -->
アプリケーションが [maintenance mode](/docs/9.x/configuration#maintenance-mode) にあるときは、アプリケーションのスケジュールされたタスクは実行されません。これは、サーバー上で実行している未完了のメンテナンスがタスクによって妨げられることが望ましくないためです。ただし、メンテナンス モードでもタスクを強制的に実行したい場合は、タスクを定義するときに `evenInMaintenanceMode` メソッドを呼び出すことができます。

```
$schedule->command('emails:send')->evenInMaintenanceMode();
```

<a name="running-the-scheduler"></a>
<!-- ## Running The Scheduler -->
## Running The Scheduler

<!-- Now that we have learned how to define scheduled tasks, let's discuss how to actually run them on our server. The `schedule:run` Artisan command will evaluate all of your scheduled tasks and determine if they need to run based on the server's current time. -->
スケジュールされたタスクを定義する方法を学習したので、実際にサーバー上でタスクを実行する方法について説明します。 `schedule:run` Artisan コマンドは、スケジュールされたタスクをすべて評価し、サーバーの現在時刻に基づいて実行する必要があるかどうかを判断します。

<!-- So, when using Laravel's scheduler, we only need to add a single cron configuration entry to our server that runs the `schedule:run` command every minute. If you do not know how to add cron entries to your server, consider using a service such as [Laravel Forge](https://forge.laravel.com) which can manage the cron entries for you: -->
したがって、Laravel のスケジューラーを使用する場合、`schedule:run` コマンドを毎分実行する単一の cron 構成エントリーをサーバーに追加するだけで済みます。サーバーに cron エントリを追加する方法がわからない場合は、cron エントリを管理できる [Laravel Forge](https://forge.laravel.com) などのサービスの使用を検討してください。

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="running-the-scheduler-locally"></a>
<!-- ## Running The Scheduler Locally -->
## Running The Scheduler Locally

<!-- Typically, you would not add a scheduler cron entry to your local development machine. Instead, you may use the `schedule:work` Artisan command. This command will run in the foreground and invoke the scheduler every minute until you terminate the command: -->
通常、ローカル開発マシンにスケジューラ cron エントリを追加しません。代わりに、`schedule:work` Artisan コマンドを使用できます。このコマンドはフォアグラウンドで実行され、コマンドを終了するまで毎分スケジューラを呼び出します。

```shell
php artisan schedule:work
```

<a name="task-output"></a>
<!-- ## Task Output -->
## Task Output

<!-- The Laravel scheduler provides several convenient methods for working with the output generated by scheduled tasks. First, using the `sendOutputTo` method, you may send the output to a file for later inspection: -->
Laravel スケジューラーは、スケジュールされたタスクによって生成された出力を操作するための便利なメソッドをいくつか提供します。まず、`sendOutputTo` メソッドを使用して、後で検査できるように出力をファイルに送信できます。

```
$schedule->command('emails:send')
         ->daily()
         ->sendOutputTo($filePath);
```

<!-- If you would like to append the output to a given file, you may use the `appendOutputTo` method: -->
出力を特定のファイルに追加したい場合は、`appendOutputTo` メソッドを使用できます。

```
$schedule->command('emails:send')
         ->daily()
         ->appendOutputTo($filePath);
```

<!-- Using the `emailOutputTo` method, you may email the output to an email address of your choice. Before emailing the output of a task, you should configure Laravel's [email services](/docs/9.x/mail): -->
`emailOutputTo` メソッドを使用すると、出力を選択した電子メール アドレスに電子メールで送信できます。タスクの出力を電子メールで送信する前に、Laravel の [email services](/docs/9.x/mail) を構成する必要があります。

```
$schedule->command('report:generate')
         ->daily()
         ->sendOutputTo($filePath)
         ->emailOutputTo('taylor@example.com');
```

<!-- If you only want to email the output if the scheduled Artisan or system command terminates with a non-zero exit code, use the `emailOutputOnFailure` method: -->
スケジュールされた Artisan またはシステム コマンドがゼロ以外の終了コードで終了した場合にのみ出力を電子メールで送信する場合は、`emailOutputOnFailure` メソッドを使用します。

```
$schedule->command('report:generate')
         ->daily()
         ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`、`emailOutputOnFailure`、`sendOutputTo`、および `appendOutputTo` メソッドは、`command` および `exec` メソッド専用です。

<a name="task-hooks"></a>
<!-- ## Task Hooks -->
## Task Hooks

<!-- Using the `before` and `after` methods, you may specify code to be executed before and after the scheduled task is executed: -->
`before` メソッドと `after` メソッドを使用すると、スケジュールされたタスクの実行前後に実行されるコードを指定できます。

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
`onSuccess` メソッドと `onFailure` メソッドを使用すると、スケジュールされたタスクが成功または失敗した場合に実行されるコードを指定できます。失敗は、スケジュールされたArtisanまたはシステム コマンドがゼロ以外の終了コードで終了したことを示します。

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
コマンドから出力が利用可能な場合は、フックのクロージャ定義の `$output` 引数として `Illuminate\Support\Stringable` インスタンスをタイプヒントすることで、`after`、`onSuccess`、または `onFailure` フックで出力にアクセスできます。

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
`pingBefore` メソッドと `thenPing` メソッドを使用すると、スケジューラはタスクの実行前または実行後に、指定された URL に自動的に ping を送信できます。このメソッドは、スケジュールされたタスクの実行が開始または終了したことを [Envoyer](https://envoyer.io) などの外部サービスに通知するのに役立ちます。

```
$schedule->command('emails:send')
         ->daily()
         ->pingBefore($url)
         ->thenPing($url);
```

<!-- The `pingBeforeIf` and `thenPingIf` methods may be used to ping a given URL only if a given condition is `true`: -->
`pingBeforeIf` メソッドと `thenPingIf` メソッドは、特定の条件が `true` の場合にのみ、特定の URL に ping を実行するために使用できます。

```
$schedule->command('emails:send')
         ->daily()
         ->pingBeforeIf($condition, $url)
         ->thenPingIf($condition, $url);
```

<!-- The `pingOnSuccess` and `pingOnFailure` methods may be used to ping a given URL only if the task succeeds or fails. A failure indicates that the scheduled Artisan or system command terminated with a non-zero exit code: -->
`pingOnSuccess` メソッドと `pingOnFailure` メソッドは、タスクが成功または失敗した場合にのみ、特定の URL に ping を送信するために使用できます。失敗は、スケジュールされたArtisanまたはシステム コマンドがゼロ以外の終了コードで終了したことを示します。

```
$schedule->command('emails:send')
         ->daily()
         ->pingOnSuccess($successUrl)
         ->pingOnFailure($failureUrl);
```

<!-- All of the ping methods require the Guzzle HTTP library. Guzzle is typically installed in all new Laravel projects by default, but, you may manually install Guzzle into your project using the Composer package manager if it has been accidentally removed: -->
すべての ping メソッドには Guzzle HTTP ライブラリが必要です。 Guzzle は通常、デフォルトですべての新しい Laravel プロジェクトにインストールされますが、Guzzle が誤って削除された場合は、Composer パッケージ マネージャーを使用してプロジェクトに手動でインストールできます。

```shell
composer require guzzlehttp/guzzle
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- If needed, you may listen to [events](/docs/9.x/events) dispatched by the scheduler. Typically, event listener mappings will be defined within your application's `App\Providers\EventServiceProvider` class: -->
必要に応じて、スケジューラによってディスパッチされた [events](/docs/9.x/events) を聞くことができます。通常、イベント リスナ マッピングはアプリケーションの `App\Providers\EventServiceProvider` クラス内で定義されます。

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

