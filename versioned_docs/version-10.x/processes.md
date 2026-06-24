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
Laravel은 [Symfony Process component](https://symfony.com/doc/current/components/process.html)를 감싸는 간결하고 명확한 API를 제공합니다. 이를 통해 Laravel 애플리케이션에서 외부 프로세스를 손쉽게 호출할 수 있습니다. Laravel의 프로세스 기능은 가장 일반적으로 사용되는 사례에 중점을 두며, 뛰어난 개발자 경험을 제공합니다.

<a name="invoking-processes"></a>
<!-- ## Invoking Processes -->
## Invoking Processes

<!-- To invoke a process, you may use the `run` and `start` methods offered by the `Process` facade. The `run` method will invoke a process and wait for the process to finish executing, while the `start` method is used for asynchronous process execution. We'll examine both approaches within this documentation. First, let's examine how to invoke a basic, synchronous process and inspect its result: -->
프로세스를 실행하려면 `Process` 파사드에서 제공하는 `run` 및 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 실행하고 해당 프로세스가 끝날 때까지 기다립니다. 반면, `start` 메서드는 비동기적으로 프로세스를 실행할 때 사용합니다. 이 문서에서는 두 가지 접근 방식을 모두 살펴봅니다. 먼저, 가장 기본적인 동기 프로세스를 호출하고 그 결과를 확인하는 방법을 예시로 보겠습니다.

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

<!-- Of course, the `Illuminate\Contracts\Process\ProcessResult` instance returned by the `run` method offers a variety of helpful methods that may be used to inspect the process result: -->
물론 `run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스는 프로세스 결과를 확인하는 데 사용할 수 있는 다양한 유용한 메서드를 제공합니다.

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
프로세스 실행 결과 인스턴스가 있을 때, 종료 코드가 0보다 클 경우(즉, 실패 시) `Illuminate\Process\Exceptions\ProcessFailedException` 예외를 던지고 싶다면 `throw` 및 `throwIf` 메서드를 사용할 수 있습니다. 프로세스가 실패하지 않은 경우에는 결과 인스턴스를 그대로 반환합니다.

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
<!-- ### Process Options -->
### Process Options

<!-- Of course, you may need to customize the behavior of a process before invoking it. Thankfully, Laravel allows you to tweak a variety of process features, such as the working directory, timeout, and environment variables. -->
프로세스를 실행하기 전에 동작을 세부적으로 조정하고 싶을 때가 있습니다. Laravel은 작업 디렉터리, 타임아웃, 환경 변수 등 다양한 프로세스 속성을 손쉽게 설정할 수 있도록 지원합니다.

<a name="working-directory-path"></a>
<!-- #### Working Directory Path -->
#### Working Directory Path

<!-- You may use the `path` method to specify the working directory of the process. If this method is not invoked, the process will inherit the working directory of the currently executing PHP script: -->
`path` 메서드를 사용해 프로세스의 작업 디렉터리를 지정할 수 있습니다. 이 메서드를 호출하지 않으면 현재 실행 중인 PHP 스크립트의 작업 디렉터리를 상속하게 됩니다.

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
<!-- #### Input -->
#### Input

<!-- You may provide input via the "standard input" of the process using the `input` method: -->
`input` 메서드를 사용해 프로세스의 표준 입력(standard input)으로 값을 전달할 수 있습니다.

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
<!-- #### Timeouts -->
#### Timeouts

<!-- By default, processes will throw an instance of `Illuminate\Process\Exceptions\ProcessTimedOutException` after executing for more than 60 seconds. However, you can customize this behavior via the `timeout` method: -->
기본적으로 프로세스는 60초 이상 실행될 경우 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외를 던집니다. 이 동작은 `timeout` 메서드로 변경할 수 있습니다.

```php
$result = Process::timeout(120)->run('bash import.sh');
```

<!-- Or, if you would like to disable the process timeout entirely, you may invoke the `forever` method: -->
또한, 프로세스 타임아웃을 완전히 비활성화하고 싶다면 `forever` 메서드를 사용할 수 있습니다.

```php
$result = Process::forever()->run('bash import.sh');
```

<!-- The `idleTimeout` method may be used to specify the maximum number of seconds the process may run without returning any output: -->
`idleTimeout` 메서드는 프로세스가 아무 출력도 하지 않은 채로 동작할 수 있는 최대 시간을(초 단위로) 지정합니다.

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
<!-- #### Environment Variables -->
#### Environment Variables

<!-- Environment variables may be provided to the process via the `env` method. The invoked process will also inherit all of the environment variables defined by your system: -->
`env` 메서드를 통해, 프로세스에 환경 변수를 설정할 수 있습니다. 호출된 프로세스는 시스템에 정의된 모든 환경 변수도 함께 상속받게 됩니다.

```php
$result = Process::forever()
            ->env(['IMPORT_PATH' => __DIR__])
            ->run('bash import.sh');
```

<!-- If you wish to remove an inherited environment variable from the invoked process, you may provide that environment variable with a value of `false`: -->
상속된 환경 변수 중 특정 값을 제거하고 싶다면 환경 변수의 값을 `false`로 지정하면 됩니다.

```php
$result = Process::forever()
            ->env(['LOAD_PATH' => false])
            ->run('bash import.sh');
```

<a name="tty-mode"></a>
<!-- #### TTY Mode -->
#### TTY Mode

<!-- The `tty` method may be used to enable TTY mode for your process. TTY mode connects the input and output of the process to the input and output of your program, allowing your process to open an editor like Vim or Nano as a process: -->
`tty` 메서드를 사용하면 프로세스에 TTY 모드를 활성화할 수 있습니다. TTY 모드는 프로세스의 입력과 출력을 현재 프로그램의 입력 및 출력과 직접 연결하기 때문에, Vim, Nano와 같은 에디터를 서브 프로세스로 열 수 있습니다.

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
<!-- ### Process Output -->
### Process Output

<!-- As previously discussed, process output may be accessed using the `output` (stdout) and `errorOutput` (stderr) methods on a process result: -->
이미 설명한 것처럼, 프로세스 실행 결과 인스턴스에서는 `output`(표준 출력, stdout), `errorOutput`(표준 에러 출력, stderr) 메서드로 출력을 확인할 수 있습니다.

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

<!-- However, output may also be gathered in real-time by passing a closure as the second argument to the `run` method. The closure will receive two arguments: the "type" of output (`stdout` or `stderr`) and the output string itself: -->
하지만, `run` 메서드의 두 번째 인자로 클로저를 전달해서 실시간으로 프로세스 출력을 수집할 수도 있습니다. 이 클로저는 "type"(`stdout` 또는 `stderr`)과 출력 문자열 두 개의 인자를 받습니다.

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

<!-- Laravel also offers the `seeInOutput` and `seeInErrorOutput` methods, which provide a convenient way to determine if a given string was contained in the process' output: -->
Laravel은 또한 `seeInOutput`, `seeInErrorOutput` 메서드를 제공하여, 특정 문자열이 프로세스 출력에 포함되어 있는지 쉽게 확인할 수 있습니다.

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
<!-- #### Disabling Process Output -->
#### Disabling Process Output

<!-- If your process is writing a significant amount of output that you are not interested in, you can conserve memory by disabling output retrieval entirely. To accomplish this, invoke the `quietly` method while building the process: -->
프로세스가 매우 많은 출력을 하며, 해당 출력이 필요 없는 경우, 출력을 완전히 비활성화하여 메모리를 아낄 수 있습니다. 이를 위해 프로세스를 구성할 때 `quietly` 메서드를 호출해 주세요.

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
<!-- ### Pipelines -->
### Pipelines

<!-- Sometimes you may want to make the output of one process the input of another process. This is often referred to as "piping" the output of a process into another. The `pipe` method provided by the `Process` facades makes this easy to accomplish. The `pipe` method will execute the piped processes synchronously and return the process result for the last process in the pipeline: -->
특정 상황에서는 한 프로세스의 출력을 다른 프로세스의 입력으로 전달하고 싶을 수 있습니다. 보통 이를 "파이핑"이라고 부릅니다. `Process` 파사드에서 제공하는 `pipe` 메서드를 사용하면 파이프라인을 쉽게 구현할 수 있습니다. `pipe` 메서드는 파이프에 연결된 모든 프로세스를 동기적으로 실행하며, 파이프라인에서 마지막 프로세스의 결과를 반환합니다.

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
파이프라인을 구성하는 각 프로세스를 별도로 설정할 필요가 없다면, 명령어 문자열 배열을 `pipe` 메서드에 바로 전달할 수 있습니다.

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

<!-- The process output may be gathered in real-time by passing a closure as the second argument to the `pipe` method. The closure will receive two arguments: the "type" of output (`stdout` or `stderr`) and the output string itself: -->
파이프라인 프로세스의 출력은 `pipe` 메서드의 두 번째 인자로 클로저를 전달하여 실시간으로 수집할 수도 있습니다. 이 클로저는 "type"(`stdout` 또는 `stderr`)과 출력 문자열을 인자로 받습니다.

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

<!-- Laravel also allows you to assign string keys to each process within a pipeline via the `as` method. This key will also be passed to the output closure provided to the `pipe` method, allowing you to determine which process the output belongs to: -->
또한, `as` 메서드를 사용해 파이프라인 내 각 프로세스에 문자열 키를 할당할 수 있습니다. 이 키는 `pipe` 메서드에 전달하는 클로저에도 전달되어 어떤 프로세스의 출력인지 구분하는 데 사용할 수 있습니다.

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
`run` 메서드는 프로세스를 동기적으로 호출하지만, `start` 메서드를 사용하면 비동기적으로 프로세스를 실행할 수 있습니다. 이를 통해 프로세스가 백그라운드에서 동작하는 동안 애플리케이션의 다른 작업을 계속 수행할 수 있습니다. 프로세스를 시작한 뒤에는 `running` 메서드를 활용하여 현재 프로세스가 수행 중인지 확인할 수 있습니다.

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

<!-- As you may have noticed, you may invoke the `wait` method to wait until the process is finished executing and retrieve the process result instance: -->
보시는 것처럼, 프로세스가 완료될 때까지 대기하려면 `wait` 메서드를 호출하여 결과 인스턴스를 받을 수 있습니다.

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
<!-- ### Process IDs and Signals -->
### Process IDs and Signals

<!-- The `id` method may be used to retrieve the operating system assigned process ID of the running process: -->
`id` 메서드를 사용하면 현재 실행 중인 프로세스에 할당된 운영체제의 프로세스 ID를 확인할 수 있습니다.

```php
$process = Process::start('bash import.sh');

return $process->id();
```

<!-- You may use the `signal` method to send a "signal" to the running process. A list of predefined signal constants can be found within the [PHP documentation](https://www.php.net/manual/en/pcntl.constants.php): -->
실행 중인 프로세스에 "시그널"을 보낼 때는 `signal` 메서드를 사용하면 됩니다. 사용할 수 있는 시그널 상수 목록은 [PHP documentation](https://www.php.net/manual/en/pcntl.constants.php)에서 확인할 수 있습니다.

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
<!-- ### Asynchronous Process Output -->
### Asynchronous Process Output

<!-- While an asynchronous process is running, you may access its entire current output using the `output` and `errorOutput` methods; however, you may utilize the `latestOutput` and `latestErrorOutput` to access the output from the process that has occurred since the output was last retrieved: -->
비동기 프로세스가 실행 중일 때는, `output`, `errorOutput` 메서드로 전체 출력을 확인할 수 있습니다. 또한, `latestOutput`, `latestErrorOutput` 메서드를 사용해 마지막 조회 이후 새롭게 발생한 출력만 볼 수도 있습니다.

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

<!-- Like the `run` method, output may also be gathered in real-time from asynchronous processes by passing a closure as the second argument to the `start` method. The closure will receive two arguments: the "type" of output (`stdout` or `stderr`) and the output string itself: -->
`run` 메서드와 마찬가지로, `start` 메서드의 두 번째 인자로 클로저를 넘기면 비동기 프로세스의 출력을 실시간으로 수집할 수 있습니다. 이 클로저는 "type"(`stdout` 또는 `stderr`)과 출력 문자열 두 개의 인자를 받습니다.

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
Laravel은 여러 개의 비동기 프로세스 풀(pool)을 손쉽게 관리할 수 있도록 지원합니다. 즉, 동시에 여러 작업을 병렬로 실행할 수 있습니다. 시작하려면, `Illuminate\Process\Pool` 인스턴스를 인자로 받는 클로저를 `pool` 메서드에 전달하세요.

<!-- Within this closure, you may define the processes that belong to the pool. Once a process pool is started via the `start` method, you may access the [collection](/docs/10.x/collections) of running processes via the `running` method: -->
이 클로저 내부에서 풀에 포함시킬 프로세스들을 정의합니다. 풀을 `start` 메서드로 실행하면, `running` 메서드를 통해 실행 중인 모든 프로세스 [collection](/docs/10.x/collections)에 접근할 수 있습니다.

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
위 예시처럼, 풀의 모든 프로세스가 완료될 때까지 대기하고, 각각의 결과를 `wait` 메서드로 받을 수 있습니다. `wait` 메서드는 배열처럼 접근 가능한 객체를 반환하며, 개별 프로세스의 결과 인스턴스도 키로 접근할 수 있습니다.

```php
$results = $pool->wait();

echo $results[0]->output();
```

<!-- Or, for convenience, the `concurrently` method may be used to start an asynchronous process pool and immediately wait on its results. This can provide particularly expressive syntax when combined with PHP's array destructuring capabilities: -->
더 간단하게, `concurrently` 메서드를 사용하면 비동기 프로세스 풀을 시작하고, 즉시 모든 결과를 기다릴 수 있습니다. 이 방법은 PHP의 배열 구조 분해(Destructuring)와 함께 사용하면 특히 문법이 간결해집니다.

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
숫자 키로 풀의 결과에 접근하는 것은 다소 직관적이지 않습니다. 그래서 Laravel은 `as` 메서드로 풀 내 각 프로세스에 문자열 키를 지정할 수 있게 지원합니다. 이 키는 `start` 메서드에 전달된 클로저에도 전달되어서, 어떤 프로세스에서 나온 출력인지 구분할 수 있습니다.

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
풀의 `running` 메서드는 풀 내에서 실행 중인 모든 프로세스의 컬렉션을 제공하므로, 각각의 프로세스 ID에도 쉽게 접근할 수 있습니다.

```php
$processIds = $pool->running()->each->id();
```

<!-- And, for convenience, you may invoke the `signal` method on a process pool to send a signal to every process within the pool: -->
또한 편의상, 프로세스 풀에 대해 `signal` 메서드를 호출하면 풀에 포함된 모든 프로세스에 동시에 시그널을 보낼 수 있습니다.

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Many Laravel services provide functionality to help you easily and expressively write tests, and Laravel's process service is no exception. The `Process` facade's `fake` method allows you to instruct Laravel to return stubbed / dummy results when processes are invoked. -->
Laravel은 다양한 서비스에서 테스트를 쉽게 작성할 수 있는 기능을 제공하며, 프로세스 서비스도 예외가 아닙니다. `Process` 파사드의 `fake` 메서드를 사용하면 프로세스 실행을 가짜로(stub/dummy) 대체할 수 있습니다.

<a name="faking-processes"></a>
<!-- ### Faking Processes -->
### Faking Processes

<!-- To explore Laravel's ability to fake processes, let's imagine a route that invokes a process: -->
Laravel의 프로세스 페이킹 기능을 알아보기 위해, 프로세스를 호출하는 라우트 예시로 시작해봅니다.

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

<!-- When testing this route, we can instruct Laravel to return a fake, successful process result for every invoked process by calling the `fake` method on the `Process` facade with no arguments. In addition, we can even [assert](#available-assertions) that a given process was "run": -->
이 라우트를 테스트할 때, `Process` 파사드의 `fake` 메서드를 인자 없이 호출하면 모든 프로세스 호출에 대해 성공한 가짜 결과가 반환됩니다. 또한, 특정 프로세스가 실제로 실행되었는지 [assert](#available-assertions)로 검증할 수도 있습니다.

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
설명했듯이, `Process` 파사드의 `fake` 메서드는 항상 출력이 없는, 성공한 결과만 반환합니다. 하지만, 꼭 필요하다면 `Process` 파사드의 `result` 메서드를 사용해, 가짜 프로세스들이 반환할 출력과 종료 코드를 손쉽게 지정할 수 있습니다.

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
앞선 예시에서처럼, `Process` 파사드의 `fake` 메서드에 배열을 전달하면 각 프로세스 패턴 별로 별도의 가짜 결과를 정의할 수 있습니다.

<!-- The array's keys should represent command patterns that you wish to fake and their associated results. The `*` character may be used as a wildcard character. Any process commands that have not been faked will actually be invoked. You may use the `Process` facade's `result` method to construct stub / fake results for these commands: -->
배열의 키는 페이크 결과를 지정하고 싶은 명령 패턴이 되고, 값은 해당 명령에 대한 결과입니다. `*` 문자는 와일드카드로 사용 가능하며, 페이킹(가짜)이 지정되지 않은 모든 명령은 실제로 실행됩니다. 이때 `Process` 파사드의 `result` 메서드를 사용해, stub/가짜 결과를 만들 수도 있습니다.

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
입출력, 종료 코드를 별도로 정의할 필요가 없다면, 결과값을 간단히 문자열로 지정할 수도 있습니다.

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
테스트에서 동일한 명령어가 여러 번 실행되는 경우, 프로세스 실행 시마다 서로 다른 페이크 결과를 반환하고 싶을 때가 있습니다. 이럴 때는 `Process` 파사드의 `sequence` 메서드를 사용합니다.

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
지금까지는 주로 `run` 메서드로 동기 호출한 프로세스의 페이킹을 다루었습니다. 그러나 테스트 코드에서 `start`로 호출한 비동기 프로세스와 상호작용해야 한다면, 보다 정교한 페이크 패턴이 필요할 수 있습니다.

<!-- For example, let's imagine the following route which interacts with an asynchronous process: -->
예를 들어, 다음과 같이 비동기 프로세스를 다루는 라우트가 있다고 가정해보겠습니다.

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
이런 프로세스를 제대로 페이킹하려면, `running` 메서드가 몇 번 `true`를 반환할지 정의할 수 있어야 합니다. 또한, 출력이 순차적으로 여러 줄 발생하는 것도 지정할 수 있어야 합니다. 이럴 땐 `Process` 파사드의 `describe` 메서드를 사용합니다.

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
위 코드에서 `output`, `errorOutput` 메서드로 여러 줄의 출력을 정의할 수 있고, `exitCode`로 종료 코드, `iterations`로 `running` 메서드가 `true`를 몇 번 반환할지 지정할 수 있습니다.

<a name="available-assertions"></a>
<!-- ### Available Assertions -->
### Available Assertions

<!-- As [previously discussed](#faking-processes), Laravel provides several process assertions for your feature tests. We'll discuss each of these assertions below. -->
[previously discussed](#faking-processes)에서 언급했던 것처럼, Laravel은 기능 테스트에서 프로세스 호출을 검증할 수 있는 다양한 assertion 메서드를 제공합니다. 각 메서드의 사용법은 아래와 같습니다.

<a name="assert-process-ran"></a>
<!-- #### assertRan -->
#### assertRan

<!-- Assert that a given process was invoked: -->
특정 프로세스가 호출되었는지 검증합니다.

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

<!-- The `assertRan` method also accepts a closure, which will receive an instance of a process and a process result, allowing you to inspect the process' configured options. If this closure returns `true`, the assertion will "pass": -->
`assertRan` 메서드는 클로저를 인자로 받을 수도 있습니다. 이 클로저에는 프로세스 인스턴스와 결과 인스턴스가 전달되어, 구체적인 설정 값을 점검할 수 있습니다. 클로저가 `true`를 반환하면 assertion이 통과합니다.

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

<!-- The `$process` passed to the `assertRan` closure is an instance of `Illuminate\Process\PendingProcess`, while the `$result` is an instance of `Illuminate\Contracts\Process\ProcessResult`. -->
`assertRan` 클로저에 전달되는 `$process`는 `Illuminate\Process\PendingProcess` 인스턴스이며, `$result`는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
<!-- #### assertDidntRun -->
#### assertDidntRun

<!-- Assert that a given process was not invoked: -->
특정 프로세스가 실행되지 않았는지 검증합니다.

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

<!-- Like the `assertRan` method, the `assertDidntRun` method also accepts a closure, which will receive an instance of a process and a process result, allowing you to inspect the process' configured options. If this closure returns `true`, the assertion will "fail": -->
`assertRan` 메서드와 마찬가지로, `assertDidntRun` 메서드도 클로저를 인자로 받을 수 있습니다. 이 클로저에는 프로세스 인스턴스와 결과 인스턴스가 전달되어 프로세스에 설정된 옵션을 점검할 수 있습니다. 클로저가 `true`를 반환할 경우 assertion이 실패합니다.

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
<!-- #### assertRanTimes -->
#### assertRanTimes

<!-- Assert that a given process was invoked a given number of times: -->
특정 프로세스가 주어진 횟수만큼 호출되었는지 검증합니다.

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

<!-- The `assertRanTimes` method also accepts a closure, which will receive an instance of a process and a process result, allowing you to inspect the process' configured options. If this closure returns `true` and the process was invoked the specified number of times, the assertion will "pass": -->
`assertRanTimes` 메서드 또한 클로저를 인자로 받아, 각 실행이 원하는 조건을 만족하는지 세부적으로 점검할 수 있습니다. 클로저가 `true`를 반환하고 지정한 횟수만큼 해당 프로세스가 실행되었다면 assertion이 통과합니다.

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
<!-- ### Preventing Stray Processes -->
### Preventing Stray Processes

<!-- If you would like to ensure that all invoked processes have been faked throughout your individual test or complete test suite, you can call the `preventStrayProcesses` method. After calling this method, any processes that do not have a corresponding fake result will throw an exception rather than starting an actual process: -->
개별 테스트 또는 전체 테스트 스위트에서 호출된 모든 프로세스가 반드시 페이킹(가짜 처리)되었는지 강제하고 싶다면 `preventStrayProcesses` 메서드를 호출하세요. 이 메서드 호출 후에는 페이크가 정의되지 않은 프로세스 실행 시 예외가 발생하며, 실제 프로세스가 동작하지 않습니다.

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
