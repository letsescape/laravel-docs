<!-- # Processes -->
# Processes

- [Introduction](#introduction)
- [Invoking Processes](#invoking-processes)
    - [Process Options](#process-options)
    - [Process Output](#process-output)
    - [Pipelines](#process-pipelines)
- [Asynchronous Processes](#asynchronous-processes)
    - [Process IDs and Signals](#process-ids-and-signals)
    - [Asynchronous Process Output](#asynchronous-process-output)
- [Concurrent Processes](#concurrent-processes)
    - [Naming Pool Processes](#naming-pool-processes)
    - [Pool Process IDs and Signals](#pool-process-ids-and-signals)
- [Testing](#testing)
    - [Faking Processes](#faking-processes)
    - [Faking Specific Processes](#faking-specific-processes)
    - [Faking Process Sequences](#faking-process-sequences)
    - [Faking Asynchronous Process Lifecycles](#faking-asynchronous-process-lifecycles)
    - [Available Assertions](#available-assertions)
    - [Preventing Stray Processes](#preventing-stray-processes)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides an expressive, minimal API around the [Symfony Process component](https://symfony.com/doc/current/components/process.html), allowing you to conveniently invoke external processes from your Laravel application. Laravel's process features are focused on the most common use cases and a wonderful developer experience. -->
Laravel は、[Symfony Process component](https://symfony.com/doc/current/components/process.html) を中心とした表現力豊かな最小限の API を提供し、Laravel アプリケーションから外部プロセスを簡単に呼び出すことができます。 Laravel のプロセス機能は、最も一般的なユースケースと素晴らしい開発者エクスペリエンスに焦点を当てています。

<a name="invoking-processes"></a>
<!-- ## Invoking Processes -->
## Invoking Processes

<!-- To invoke a process, you may use the `run` and `start` methods offered by the `Process` facade. The `run` method will invoke a process and wait for the process to finish executing, while the `start` method is used for asynchronous process execution. We'll examine both approaches within this documentation. First, let's examine how to invoke a basic, synchronous process and inspect its result: -->
プロセスを呼び出すには、`Process` ファサードによって提供される `run` メソッドと `start` メソッドを使用できます。 `run` メソッドはプロセスを呼び出し、プロセスの実行が完了するまで待機しますが、`start` メソッドは非同期プロセスの実行に使用されます。このドキュメントでは両方のアプローチを検討します。まず、基本的な同期プロセスを呼び出してその結果を検査する方法を調べてみましょう。

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

<!-- Of course, the `Illuminate\Contracts\Process\ProcessResult` instance returned by the `run` method offers a variety of helpful methods that may be used to inspect the process result: -->
もちろん、`run` メソッドによって返される `Illuminate\Contracts\Process\ProcessResult` インスタンスには、プロセス結果の検査に使用できるさまざまな便利なメソッドが用意されています。

```php
$result = Process::run('ls -la');

$result->successful();
$result->failed();
$result->exitCode();
$result->output();
$result->errorOutput();
```

<a name="throwing-exceptions"></a>
<!-- #### Throwing Exceptions -->
#### Throwing Exceptions

<!-- If you have a process result and would like to throw an instance of `Illuminate\Process\Exceptions\ProcessFailedException` if the exit code is greater than zero (thus indicating failure), you may use the `throw` and `throwIf` methods. If the process did not fail, the process result instance will be returned: -->
処理結果があり、終了コードがゼロより大きい (つまり失敗を示す) 場合に `Illuminate\Process\Exceptions\ProcessFailedException` のインスタンスをスローしたい場合は、`throw` メソッドと `throwIf` メソッドを使用できます。プロセスが失敗しなかった場合は、プロセス結果のインスタンスが返されます。

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
<!-- ### Process Options -->
### Process Options

<!-- Of course, you may need to customize the behavior of a process before invoking it. Thankfully, Laravel allows you to tweak a variety of process features, such as the working directory, timeout, and environment variables. -->
もちろん、プロセスを呼び出す前にプロセスの動作をカスタマイズする必要がある場合があります。ありがたいことに、Laravel では作業ディレクトリ、タイムアウト、環境変数などのさまざまなプロセス機能を調整できます。

<a name="working-directory-path"></a>
<!-- #### Working Directory Path -->
#### Working Directory Path

<!-- You may use the `path` method to specify the working directory of the process. If this method is not invoked, the process will inherit the working directory of the currently executing PHP script: -->
`path` メソッドを使用して、プロセスの作業ディレクトリを指定できます。このメソッドが呼び出されない場合、プロセスは現在実行中の PHP スクリプトの作業ディレクトリを継承します。

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
<!-- #### Input -->
#### Input

<!-- You may provide input via the "standard input" of the process using the `input` method: -->
`input` メソッドを使用して、プロセスの「標準入力」経由で入力を提供できます。

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
<!-- #### Timeouts -->
#### Timeouts

<!-- By default, processes will throw an instance of `Illuminate\Process\Exceptions\ProcessTimedOutException` after executing for more than 60 seconds. However, you can customize this behavior via the `timeout` method: -->
デフォルトでは、プロセスは 60 秒以上実行された後に `Illuminate\Process\Exceptions\ProcessTimedOutException` のインスタンスをスローします。ただし、`timeout` メソッドを使用してこの動作をカスタマイズできます。

```php
$result = Process::timeout(120)->run('bash import.sh');
```

<!-- Or, if you would like to disable the process timeout entirely, you may invoke the `forever` method: -->
または、プロセス タイムアウトを完全に無効にしたい場合は、`forever` メソッドを呼び出します。

```php
$result = Process::forever()->run('bash import.sh');
```

<!-- The `idleTimeout` method may be used to specify the maximum number of seconds the process may run without returning any output: -->
`idleTimeout` メソッドは、出力を返さずにプロセスを実行できる最大秒数を指定するために使用できます。

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
<!-- #### Environment Variables -->
#### Environment Variables

<!-- Environment variables may be provided to the process via the `env` method. The invoked process will also inherit all of the environment variables defined by your system: -->
環境変数は、`env` メソッドを介してプロセスに提供できます。呼び出されたプロセスは、システムによって定義されたすべての環境変数も継承します。

```php
$result = Process::forever()
            ->env(['IMPORT_PATH' => __DIR__])
            ->run('bash import.sh');
```

<!-- If you wish to remove an inherited environment variable from the invoked process, you may provide that environment variable with a value of `false`: -->
呼び出されたプロセスから継承された環境変数を削除したい場合は、その環境変数に値 `false` を指定できます。

```php
$result = Process::forever()
            ->env(['LOAD_PATH' => false])
            ->run('bash import.sh');
```

<a name="tty-mode"></a>
<!-- #### TTY Mode -->
#### TTY Mode

<!-- The `tty` method may be used to enable TTY mode for your process. TTY mode connects the input and output of the process to the input and output of your program, allowing your process to open an editor like Vim or Nano as a process: -->
`tty` メソッドを使用して、プロセスの TTY モードを有効にすることができます。 TTY モードは、プロセスの入出力をプログラムの入出力に接続し、プロセスが Vim や Nano などのエディターをプロセスとして開くことができるようにします。

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
<!-- ### Process Output -->
### Process Output

<!-- As previously discussed, process output may be accessed using the `output` (stdout) and `errorOutput` (stderr) methods on a process result: -->
前述したように、プロセス出力には、プロセス結果の `output` (stdout) および `errorOutput` (stderr) メソッドを使用してアクセスできます。

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

<!-- However, output may also be gathered in real-time by passing a closure as the second argument to the `run` method. The closure will receive two arguments: the "type" of output (`stdout` or `stderr`) and the output string itself: -->
ただし、`run` メソッドの 2 番目の引数としてクロージャーを渡すことによって、出力をリアルタイムで収集することもできます。クロージャーは 2 つの引数を受け取ります: 出力の「タイプ」 (`stdout` または `stderr`) と出力文字列自体です。

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

<!-- Laravel also offers the `seeInOutput` and `seeInErrorOutput` methods, which provide a convenient way to determine if a given string was contained in the process' output: -->
Laravel では、`seeInOutput` メソッドと `seeInErrorOutput` メソッドも提供しています。これらは、特定の文字列がプロセスの出力に含まれているかどうかを判断する便利な方法を提供します。

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
<!-- #### Disabling Process Output -->
#### Disabling Process Output

<!-- If your process is writing a significant amount of output that you are not interested in, you can conserve memory by disabling output retrieval entirely. To accomplish this, invoke the `quietly` method while building the process: -->
プロセスが興味のない大量の出力を書き込んでいる場合は、出力の取得を完全に無効にすることでメモリを節約できます。これを実現するには、プロセスの構築中に `quietly` メソッドを呼び出します。

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
<!-- ### Pipelines -->
### Pipelines

<!-- Sometimes you may want to make the output of one process the input of another process. This is often referred to as "piping" the output of a process into another. The `pipe` method provided by the `Process` facades makes this easy to accomplish. The `pipe` method will execute the piped processes synchronously and return the process result for the last process in the pipeline: -->
場合によっては、あるプロセスの出力を別のプロセスの入力にしたい場合があります。これは、プロセスの出力を別のプロセスに「パイプする」と呼ばれることがよくあります。 `Process` ファサードによって提供される `pipe` メソッドを使用すると、これを簡単に実現できます。 `pipe` メソッドは、パイプされたプロセスを同期的に実行し、パイプラインの最後のプロセスの処理結果を返します。

```php
use Illuminate\Process\Pipe;
use Illuminate\Support\Facades\Process;

$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
});

if ($result->successful()) {
    // ...
}
```

<!-- If you do not need to customize the individual processes that make up the pipeline, you may simply pass an array of command strings to the `pipe` method: -->
パイプラインを構成する個々のプロセスをカスタマイズする必要がない場合は、コマンド文字列の配列を `pipe` メソッドに渡すだけで済みます。

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

<!-- The process output may be gathered in real-time by passing a closure as the second argument to the `pipe` method. The closure will receive two arguments: the "type" of output (`stdout` or `stderr`) and the output string itself: -->
プロセス出力は、`pipe` メソッドの 2 番目の引数としてクロージャを渡すことによってリアルタイムで収集できます。クロージャーは 2 つの引数を受け取ります: 出力の「タイプ」 (`stdout` または `stderr`) と出力文字列自体です。

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

<!-- Laravel also allows you to assign string keys to each process within a pipeline via the `as` method. This key will also be passed to the output closure provided to the `pipe` method, allowing you to determine which process the output belongs to: -->
Laravel では、`as` メソッドを使用して、パイプライン内の各プロセスに文字列キーを割り当てることもできます。このキーは、`pipe` メソッドに提供される出力クロージャにも渡され、出力がどのプロセスに属するかを判断できるようになります。

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->as('first')->command('cat example.txt');
    $pipe->as('second')->command('grep -i "laravel"');
})->start(function (string $type, string $output, string $key) {
    // ...
});
```

<a name="asynchronous-processes"></a>
<!-- ## Asynchronous Processes -->
## Asynchronous Processes

<!-- While the `run` method invokes processes synchronously, the `start` method may be used to invoke a process asynchronously. This allows your application to continue performing other tasks while the process runs in the background. Once the process has been invoked, you may utilize the `running` method to determine if the process is still running: -->
`run` メソッドはプロセスを同期的に呼び出しますが、`start` メソッドを使用してプロセスを非同期に呼び出すこともできます。これにより、プロセスがバックグラウンドで実行されている間、アプリケーションは他のタスクを実行し続けることができます。プロセスが呼び出されたら、`running` メソッドを使用して、プロセスがまだ実行中かどうかを確認できます。

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

<!-- As you may have noticed, you may invoke the `wait` method to wait until the process is finished executing and retrieve the process result instance: -->
お気づきかもしれませんが、`wait` メソッドを呼び出して、プロセスの実行が完了するまで待機し、プロセス結果のインスタンスを取得できます。

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
<!-- ### Process IDs and Signals -->
### Process IDs and Signals

<!-- The `id` method may be used to retrieve the operating system assigned process ID of the running process: -->
`id` メソッドは、オペレーティング システムに割り当てられた、実行中のプロセスのプロセス ID を取得するために使用できます。

```php
$process = Process::start('bash import.sh');

return $process->id();
```

<!-- You may use the `signal` method to send a "signal" to the running process. A list of predefined signal constants can be found within the [PHP documentation](https://www.php.net/manual/en/pcntl.constants.php): -->
`signal` メソッドを使用して、実行中のプロセスに「シグナル」を送信できます。事前定義された信号定数のリストは、[PHP documentation](https://www.php.net/manual/en/pcntl.constants.php) 内にあります。

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
<!-- ### Asynchronous Process Output -->
### Asynchronous Process Output

<!-- While an asynchronous process is running, you may access its entire current output using the `output` and `errorOutput` methods; however, you may utilize the `latestOutput` and `latestErrorOutput` to access the output from the process that has occurred since the output was last retrieved: -->
非同期プロセスの実行中は、`output` メソッドと `errorOutput` メソッドを使用して、その現在の出力全体にアクセスできます。ただし、`latestOutput` および `latestErrorOutput` を利用して、出力が最後に取得されてから発生したプロセスからの出力にアクセスすることもできます。

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

<!-- Like the `run` method, output may also be gathered in real-time from asynchronous processes by passing a closure as the second argument to the `start` method. The closure will receive two arguments: the "type" of output (`stdout` or `stderr`) and the output string itself: -->
`run` メソッドと同様に、`start` メソッドの 2 番目の引数としてクロージャを渡すことにより、非同期プロセスから出力をリアルタイムで収集することもできます。クロージャは、出力の「タイプ」(`stdout` または `stderr`) と出力文字列自体の 2 つの引数を受け取ります。

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

<a name="concurrent-processes"></a>
<!-- ## Concurrent Processes -->
## Concurrent Processes

<!-- Laravel also makes it a breeze to manage a pool of concurrent, asynchronous processes, allowing you to easily execute many tasks simultaneously. To get started, invoke the `pool` method, which accepts a closure that receives an instance of `Illuminate\Process\Pool`. -->
Laravel を使用すると、同時非同期プロセスのプールを簡単に管理できるため、多くのタスクを同時に簡単に実行できます。まず、`pool` メソッドを呼び出します。このメソッドは、`Illuminate\Process\Pool` のインスタンスを受け取るクロージャーを受け入れます。

<!-- Within this closure, you may define the processes that belong to the pool. Once a process pool is started via the `start` method, you may access the [collection](/docs/10.x/collections) of running processes via the `running` method: -->
このクロージャ内で、プールに属するプロセスを定義できます。 `start` メソッドを介してプロセス プールが開始されると、`running` メソッドを介して実行中のプロセスの [collection](/docs/10.x/collections) にアクセスできます。

```php
use Illuminate\Process\Pool;
use Illuminate\Support\Facades\Process;

$pool = Process::pool(function (Pool $pool) {
    $pool->path(__DIR__)->command('bash import-1.sh');
    $pool->path(__DIR__)->command('bash import-2.sh');
    $pool->path(__DIR__)->command('bash import-3.sh');
})->start(function (string $type, string $output, int $key) {
    // ...
});

while ($pool->running()->isNotEmpty()) {
    // ...
}

$results = $pool->wait();
```

<!-- As you can see, you may wait for all of the pool processes to finish executing and resolve their results via the `wait` method. The `wait` method returns an array accessible object that allows you to access the process result instance of each process in the pool by its key: -->
ご覧のとおり、すべてのプール プロセスの実行が完了するまで待機し、`wait` メソッドを介して結果を解決できます。 `wait` メソッドは、キーによってプール内の各プロセスのプロセス結果インスタンスにアクセスできるようにする、配列アクセス可能なオブジェクトを返します。

```php
$results = $pool->wait();

echo $results[0]->output();
```

<!-- Or, for convenience, the `concurrently` method may be used to start an asynchronous process pool and immediately wait on its results. This can provide particularly expressive syntax when combined with PHP's array destructuring capabilities: -->
または、便宜上、`concurrently` メソッドを使用して非同期プロセス プールを開始し、その結果をすぐに待機することもできます。これを PHP の配列分割機能と組み合わせると、特に表現力豊かな構文を提供できます。

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
<!-- ### Naming Pool Processes -->
### Naming Pool Processes

<!-- Accessing process pool results via a numeric key is not very expressive; therefore, Laravel allows you to assign string keys to each process within a pool via the `as` method. This key will also be passed to the closure provided to the `start` method, allowing you to determine which process the output belongs to: -->
数値キーを使用してプロセス プールの結果にアクセスすることは、あまり表現力がありません。したがって、Laravelでは、`as`メソッドを介してプール内の各プロセスに文字列キーを割り当てることができます。このキーは、`start` メソッドに提供されたクロージャにも渡され、出力がどのプロセスに属しているかを判断できるようになります。

```php
$pool = Process::pool(function (Pool $pool) {
    $pool->as('first')->command('bash import-1.sh');
    $pool->as('second')->command('bash import-2.sh');
    $pool->as('third')->command('bash import-3.sh');
})->start(function (string $type, string $output, string $key) {
    // ...
});

$results = $pool->wait();

return $results['first']->output();
```

<a name="pool-process-ids-and-signals"></a>
<!-- ### Pool Process IDs and Signals -->
### Pool Process IDs and Signals

<!-- Since the process pool's `running` method provides a collection of all invoked processes within the pool, you may easily access the underlying pool process IDs: -->
プロセス プールの `running` メソッドは、プール内で呼び出されたすべてのプロセスのコレクションを提供するため、基になるプールのプロセス ID に簡単にアクセスできます。

```php
$processIds = $pool->running()->each->id();
```

<!-- And, for convenience, you may invoke the `signal` method on a process pool to send a signal to every process within the pool: -->
また、便宜上、プロセス プールで `signal` メソッドを呼び出して、プール内のすべてのプロセスにシグナルを送信することもできます。

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Many Laravel services provide functionality to help you easily and expressively write tests, and Laravel's process service is no exception. The `Process` facade's `fake` method allows you to instruct Laravel to return stubbed / dummy results when processes are invoked. -->
多くの Laravel サービスは、テストを簡単かつ表現力豊かに作成できるようにする機能を提供しており、Laravel のプロセス サービスも例外ではありません。 `Process` ファサードの `fake` メソッドを使用すると、プロセスが呼び出されたときにスタブ/ダミーの結果を返すように Laravel に指示できます。

<a name="faking-processes"></a>
<!-- ### Faking Processes -->
### Faking Processes

<!-- To explore Laravel's ability to fake processes, let's imagine a route that invokes a process: -->
Laravel のプロセスを偽装する機能を調べるために、プロセスを呼び出すルートを想像してみましょう。

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

<!-- When testing this route, we can instruct Laravel to return a fake, successful process result for every invoked process by calling the `fake` method on the `Process` facade with no arguments. In addition, we can even [assert](#available-assertions) that a given process was "run": -->
このルートをテストするとき、引数なしで `Process` ファサードの `fake` メソッドを呼び出すことで、呼び出されたすべてのプロセスに対して偽の成功したプロセス結果を返すように Laravel に指示できます。さらに、特定のプロセスが「実行」されたことを [assert](#available-assertions) で確認することもできます。

```php
<?php

namespace Tests\Feature;

use Illuminate\Process\PendingProcess;
use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Support\Facades\Process;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_process_is_invoked(): void
    {
        Process::fake();

        $response = $this->get('/import');

        // Simple process assertion...
        Process::assertRan('bash import.sh');

        // Or, inspecting the process configuration...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

<!-- As discussed, invoking the `fake` method on the `Process` facade will instruct Laravel to always return a successful process result with no output. However, you may easily specify the output and exit code for faked processes using the `Process` facade's `result` method: -->
説明したように、`Process` ファサードで `fake` メソッドを呼び出すと、出力なしで常に成功したプロセス結果を返すように Laravel に指示されます。ただし、`Process` ファサードの `result` メソッドを使用すると、偽のプロセスの出力と終了コードを簡単に指定できます。

```php
Process::fake([
    '*' => Process::result(
        output: 'Test output',
        errorOutput: 'Test error output',
        exitCode: 1,
    ),
]);
```

<a name="faking-specific-processes"></a>
<!-- ### Faking Specific Processes -->
### Faking Specific Processes

<!-- As you may have noticed in a previous example, the `Process` facade allows you to specify different fake results per process by passing an array to the `fake` method. -->
前の例でお気づきかと思いますが、`Process` ファサードでは、配列を `fake` メソッドに渡すことで、プロセスごとに異なる偽の結果を指定できます。

<!-- The array's keys should represent command patterns that you wish to fake and their associated results. The `*` character may be used as a wildcard character. Any process commands that have not been faked will actually be invoked. You may use the `Process` facade's `result` method to construct stub / fake results for these commands: -->
配列のキーは、偽装したいコマンド パターンとそれに関連する結果を表す必要があります。 `*` 文字はワイルドカード文字として使用できます。偽装されていないプロセス コマンドは実際に呼び出されます。 `Process` ファサードの `result` メソッドを使用して、次のコマンドのスタブ/偽の結果を構築できます。

```php
Process::fake([
    'cat *' => Process::result(
        output: 'Test "cat" output',
    ),
    'ls *' => Process::result(
        output: 'Test "ls" output',
    ),
]);
```

<!-- If you do not need to customize the exit code or error output of a faked process, you may find it more convenient to specify the fake process results as simple strings: -->
偽のプロセスの終了コードやエラー出力をカスタマイズする必要がない場合は、偽のプロセスの結果を単純な文字列として指定する方が便利な場合があります。

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
<!-- ### Faking Process Sequences -->
### Faking Process Sequences

<!-- If the code you are testing invokes multiple processes with the same command, you may wish to assign a different fake process result to each process invocation. You may accomplish this via the `Process` facade's `sequence` method: -->
テストしているコードが同じコマンドで複数のプロセスを呼び出す場合、各プロセス呼び出しに異なる偽のプロセス結果を割り当てることができます。これは、`Process` ファサードの `sequence` メソッドを通じて実行できます。

```php
Process::fake([
    'ls *' => Process::sequence()
                ->push(Process::result('First invocation'))
                ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
<!-- ### Faking Asynchronous Process Lifecycles -->
### Faking Asynchronous Process Lifecycles

<!-- Thus far, we have primarily discussed faking processes which are invoked synchronously using the `run` method. However, if you are attempting to test code that interacts with asynchronous processes invoked via `start`, you may need a more sophisticated approach to describing your fake processes. -->
これまで、主に、`run` メソッドを使用して同期的に呼び出される偽装プロセスについて説明してきました。ただし、`start` 経由で呼び出される非同期プロセスと対話するコードをテストしようとしている場合は、偽のプロセスを記述するためのより洗練されたアプローチが必要になる場合があります。

<!-- For example, let's imagine the following route which interacts with an asynchronous process: -->
たとえば、非同期プロセスと対話する次のルートを想像してみましょう。

```php
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    $process = Process::start('bash import.sh');

    while ($process->running()) {
        Log::info($process->latestOutput());
        Log::info($process->latestErrorOutput());
    }

    return 'Done';
});
```

<!-- To properly fake this process, we need to be able to describe how many times the `running` method should return `true`. In addition, we may want to specify multiple lines of output that should be returned in sequence. To accomplish this, we can use the `Process` facade's `describe` method: -->
このプロセスを適切に偽装するには、`running` メソッドが `true` を返す回数を記述できる必要があります。さらに、順番に返される複数行の出力を指定したい場合があります。これを実現するには、`Process` ファサードの `describe` メソッドを使用します。

```php
Process::fake([
    'bash import.sh' => Process::describe()
            ->output('First line of standard output')
            ->errorOutput('First line of error output')
            ->output('Second line of standard output')
            ->exitCode(0)
            ->iterations(3),
]);
```

<!-- Let's dig into the example above. Using the `output` and `errorOutput` methods, we may specify multiple lines of output that will be returned in sequence. The `exitCode` method may be used to specify the final exit code of the fake process. Finally, the `iterations` method may be used to specify how many times the `running` method should return `true`. -->
上の例を詳しく見てみましょう。 `output` メソッドと `errorOutput` メソッドを使用すると、順番に返される複数行の出力を指定できます。 `exitCode` メソッドを使用して、偽のプロセスの最終終了コードを指定できます。最後に、`iterations` メソッドを使用して、`running` メソッドが `true` を返す回数を指定できます。

<a name="available-assertions"></a>
<!-- ### Available Assertions -->
### Available Assertions

<!-- As [previously discussed](#faking-processes), Laravel provides several process assertions for your feature tests. We'll discuss each of these assertions below. -->
[previously discussed](#faking-processes) として、Laravel は機能テスト用にいくつかのプロセス アサーションを提供します。これらの各主張については、以下で説明します。

<a name="assert-process-ran"></a>
<!-- #### assertRan -->
#### assertRan

<!-- Assert that a given process was invoked: -->
指定されたプロセスが呼び出されたことをアサートします。

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

<!-- The `assertRan` method also accepts a closure, which will receive an instance of a process and a process result, allowing you to inspect the process' configured options. If this closure returns `true`, the assertion will "pass": -->
`assertRan` メソッドは、プロセスのインスタンスとプロセス結果を受け取るクロージャーも受け入れます。これにより、プロセスの構成されたオプションを検査できるようになります。このクロージャが `true` を返す場合、アサーションは「合格」します。

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

<!-- The `$process` passed to the `assertRan` closure is an instance of `Illuminate\Process\PendingProcess`, while the `$result` is an instance of `Illuminate\Contracts\Process\ProcessResult`. -->
`assertRan` クロージャに渡される `$process` は `Illuminate\Process\PendingProcess` のインスタンスであり、`$result` は `Illuminate\Contracts\Process\ProcessResult` のインスタンスです。

<a name="assert-process-didnt-run"></a>
<!-- #### assertDidntRun -->
#### assertDidntRun

<!-- Assert that a given process was not invoked: -->
指定されたプロセスが呼び出されなかったことをアサートします。

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

<!-- Like the `assertRan` method, the `assertDidntRun` method also accepts a closure, which will receive an instance of a process and a process result, allowing you to inspect the process' configured options. If this closure returns `true`, the assertion will "fail": -->
`assertRan` メソッドと同様、`assertDidntRun` メソッドもクロージャを受け入れます。クロージャはプロセスのインスタンスとプロセス結果を受け取り、プロセスの構成されたオプションを検査できます。このクロージャが `true` を返す場合、アサーションは「失敗」します。

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
<!-- #### assertRanTimes -->
#### assertRanTimes

<!-- Assert that a given process was invoked a given number of times: -->
指定されたプロセスが指定された回数呼び出されたことをアサートします。

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

<!-- The `assertRanTimes` method also accepts a closure, which will receive an instance of a process and a process result, allowing you to inspect the process' configured options. If this closure returns `true` and the process was invoked the specified number of times, the assertion will "pass": -->
`assertRanTimes` メソッドは、プロセスのインスタンスとプロセス結果を受け取るクロージャーも受け入れます。これにより、プロセスの構成されたオプションを検査できるようになります。このクロージャが `true` を返し、プロセスが指定された回数呼び出された場合、アサーションは「合格」します。

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
<!-- ### Preventing Stray Processes -->
### Preventing Stray Processes

<!-- If you would like to ensure that all invoked processes have been faked throughout your individual test or complete test suite, you can call the `preventStrayProcesses` method. After calling this method, any processes that do not have a corresponding fake result will throw an exception rather than starting an actual process: -->
個々のテストまたはテスト スイート全体を通じて、呼び出されたすべてのプロセスが偽装されていることを確認したい場合は、`preventStrayProcesses` メソッドを呼び出すことができます。このメソッドを呼び出した後、対応する偽の結果を持たないプロセスは、実際のプロセスを開始するのではなく、例外をスローします。

```
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// Fake response is returned...
Process::run('ls -la');

// An exception is thrown...
Process::run('bash import.sh');
```

