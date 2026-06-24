<!-- # Console Tests -->
# Console Tests

- [Introduction](#introduction)
- [Success / Failure Expectations](#success-failure-expectations)
- [Input / Output Expectations](#input-output-expectations)
- [Console Events](#console-events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In addition to simplifying HTTP testing, Laravel provides a simple API for testing your application's [custom console commands](/docs/10.x/artisan). -->
Laravel은 HTTP 테스트를 간단하게 만들어줄 뿐만 아니라, 애플리케이션의 [custom console commands](/docs/10.x/artisan)를 테스트할 수 있는 간단한 API도 제공합니다.

<a name="success-failure-expectations"></a>
<!-- ## Success / Failure Expectations -->
## Success / Failure Expectations

<!-- To get started, let's explore how to make assertions regarding an Artisan command's exit code. To accomplish this, we will use the `artisan` method to invoke an Artisan command from our test. Then, we will use the `assertExitCode` method to assert that the command completed with a given exit code: -->
먼저, Artisan 명령어의 종료 코드(exit code)를 어떻게 검증하는지 살펴보겠습니다. 이를 위해 테스트에서 `artisan` 메서드를 사용해 Artisan 명령어를 실행합니다. 그런 다음, `assertExitCode` 메서드를 이용해 명령어가 지정한 종료 코드로 정상적으로 완료되었는지 확인할 수 있습니다.

```
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('inspire')->assertExitCode(0);
}
```

<!-- You may use the `assertNotExitCode` method to assert that the command did not exit with a given exit code: -->
`assertNotExitCode` 메서드를 사용하면 명령어가 특정 종료 코드로 종료되지 않았는지도 검증할 수 있습니다.

```
$this->artisan('inspire')->assertNotExitCode(1);
```

<!-- Of course, all terminal commands typically exit with a status code of `0` when they are successful and a non-zero exit code when they are not successful. Therefore, for convenience, you may utilize the `assertSuccessful` and `assertFailed` assertions to assert that a given command exited with a successful exit code or not: -->
일반적으로 터미널 명령어는 성공하면 상태 코드 `0`으로, 실패했다면 0이 아닌 값으로 종료됩니다. 그래서 더 편리하게 사용하려면 `assertSuccessful`과 `assertFailed` 검증 메서드를 활용해 명령어가 성공했는지, 실패했는지를 간단히 확인할 수도 있습니다.

```
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
<!-- ## Input / Output Expectations -->
## Input / Output Expectations

<!-- Laravel allows you to easily "mock" user input for your console commands using the `expectsQuestion` method. In addition, you may specify the exit code and text that you expect to be output by the console command using the `assertExitCode` and `expectsOutput` methods. For example, consider the following console command: -->
Laravel은 콘솔 명령어 테스트 시 `expectsQuestion` 메서드를 활용해 사용자 입력을 손쉽게 "모킹(mock)"할 수 있습니다. 또한, `assertExitCode`와 `expectsOutput` 메서드를 이용해 명령어 실행 결과의 종료 코드와 출력되는 텍스트도 기대할 수 있습니다. 예를 들어, 아래와 같은 콘솔 명령어가 있다고 가정해봅시다.

```
Artisan::command('question', function () {
    $name = $this->ask('What is your name?');

    $language = $this->choice('Which language do you prefer?', [
        'PHP',
        'Ruby',
        'Python',
    ]);

    $this->line('Your name is '.$name.' and you prefer '.$language.'.');
});
```

<!-- You may test this command with the following test which utilizes the `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, `expectsOutputToContain`, `doesntExpectOutputToContain`, and `assertExitCode` methods: -->
아래와 같이 `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, `expectsOutputToContain`, `doesntExpectOutputToContain`, `assertExitCode` 등의 다양한 메서드를 활용해 이 명령어를 테스트할 수 있습니다.

```
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('question')
         ->expectsQuestion('What is your name?', 'Taylor Otwell')
         ->expectsQuestion('Which language do you prefer?', 'PHP')
         ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
         ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
         ->expectsOutputToContain('Taylor Otwell')
         ->doesntExpectOutputToContain('you prefer Ruby')
         ->assertExitCode(0);
}
```

<a name="confirmation-expectations"></a>
<!-- #### Confirmation Expectations -->
#### Confirmation Expectations

<!-- When writing a command which expects confirmation in the form of a "yes" or "no" answer, you may utilize the `expectsConfirmation` method: -->
명령어에서 "yes" 또는 "no"와 같이 사용자의 확인 답변을 기대하는 경우, `expectsConfirmation` 메서드를 사용할 수 있습니다.

```
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
<!-- #### Table Expectations -->
#### Table Expectations

<!-- If your command displays a table of information using Artisan's `table` method, it can be cumbersome to write output expectations for the entire table. Instead, you may use the `expectsTable` method. This method accepts the table's headers as its first argument and the table's data as its second argument: -->
만약 명령어가 Artisan의 `table` 메서드를 사용해 정보 테이블을 출력한다면, 테이블 전체에 대한 출력값을 모두 기대값으로 작성하는 게 번거로울 수 있습니다. 이럴 땐 `expectsTable` 메서드를 사용할 수 있습니다. 이 메서드는 테이블의 헤더를 첫 번째 인수로, 테이블의 데이터를 두 번째 인수로 받습니다.

```
$this->artisan('users:all')
    ->expectsTable([
        'ID',
        'Email',
    ], [
        [1, 'taylor@example.com'],
        [2, 'abigail@example.com'],
    ]);
```

<a name="console-events"></a>
<!-- ## Console Events -->
## Console Events

<!-- By default, the `Illuminate\Console\Events\CommandStarting` and `Illuminate\Console\Events\CommandFinished` events are not dispatched while running your application's tests. However, you can enable these events for a given test class by adding the `Illuminate\Foundation\Testing\WithConsoleEvents` trait to the class: -->
기본적으로는, 테스트를 실행하는 동안 `Illuminate\Console\Events\CommandStarting`과 `Illuminate\Console\Events\CommandFinished` 이벤트가 발생하지 않습니다. 하지만, 테스트 클래스에서 `Illuminate\Foundation\Testing\WithConsoleEvents` 트레이트를 추가하면 해당 이벤트가 활성화됩니다.

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\WithConsoleEvents;
use Tests\TestCase;

class ConsoleEventTest extends TestCase
{
    use WithConsoleEvents;

    // ...
}
```