<!-- # Console Tests -->
# Console Tests

- [Introduction](#introduction)
- [Success / Failure Expectations](#success-failure-expectations)
- [Input / Output Expectations](#input-output-expectations)
- [Console Events](#console-events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In addition to simplifying HTTP testing, Laravel provides a simple API for testing your application's [custom console commands](/docs/11.x/artisan). -->
HTTP 테스트를 간편하게 해주는 것 외에도, Laravel은 애플리케이션의 [custom console commands](/docs/11.x/artisan)를 테스트할 수 있는 간단한 API도 제공합니다.

<a name="success-failure-expectations"></a>
<!-- ## Success / Failure Expectations -->
## Success / Failure Expectations

<!-- To get started, let's explore how to make assertions regarding an Artisan command's exit code. To accomplish this, we will use the `artisan` method to invoke an Artisan command from our test. Then, we will use the `assertExitCode` method to assert that the command completed with a given exit code: -->
먼저, Artisan 명령어의 종료 코드(exit code)를 어떻게 검증할 수 있는지 살펴보겠습니다. 테스트에서 `artisan` 메서드를 사용해서 Artisan 명령어를 실행한 뒤, `assertExitCode` 메서드로 해당 명령이 특정 종료 코드로 정상적으로 완료됐는지 확인할 수 있습니다.

```php tab=Pest
test('console command', function () {
    $this->artisan('inspire')->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('inspire')->assertExitCode(0);
}
```

<!-- You may use the `assertNotExitCode` method to assert that the command did not exit with a given exit code: -->
`assertNotExitCode` 메서드를 사용하면 명령이 특정 종료 코드로 종료되지 않았는지 확인할 수 있습니다.

```
$this->artisan('inspire')->assertNotExitCode(1);
```

<!-- Of course, all terminal commands typically exit with a status code of `0` when they are successful and a non-zero exit code when they are not successful. Therefore, for convenience, you may utilize the `assertSuccessful` and `assertFailed` assertions to assert that a given command exited with a successful exit code or not: -->
일반적으로 터미널 명령어는 성공하면 종료 코드가 `0`이고, 실패하면 0이 아닌 값이 반환됩니다. 그래서 더욱 편리하게, `assertSuccessful`과 `assertFailed`라는 assertion을 사용할 수 있습니다. 이 메서드를 활용하면 명령이 성공 또는 실패로 종료됐는지 쉽게 검증할 수 있습니다.

```
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
<!-- ## Input / Output Expectations -->
## Input / Output Expectations

<!-- Laravel allows you to easily "mock" user input for your console commands using the `expectsQuestion` method. In addition, you may specify the exit code and text that you expect to be output by the console command using the `assertExitCode` and `expectsOutput` methods. For example, consider the following console command: -->
Laravel에서는 `expectsQuestion` 메서드를 사용해 콘솔 명령어의 사용자 입력을 손쉽게 "모킹(mocking)"할 수 있습니다. 또한, `assertExitCode`와 `expectsOutput` 메서드로 콘솔 명령어가 반환하는 종료 코드와 출력되는 텍스트도 검증할 수 있습니다. 예를 들어, 아래와 같은 콘솔 명령어가 있다고 가정해보겠습니다.

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

<!-- You may test this command with the following test: -->
위 명령어는 아래의 테스트 코드로 검증할 수 있습니다.

```php tab=Pest
test('console command', function () {
    $this->artisan('question')
        ->expectsQuestion('What is your name?', 'Taylor Otwell')
        ->expectsQuestion('Which language do you prefer?', 'PHP')
        ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
        ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
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
        ->assertExitCode(0);
}
```

<!-- If you are utilizing the `search` or `multisearch` functions provided by [Laravel Prompts](/docs/11.x/prompts), you may use the `expectsSearch` assertion to mock the user's input, search results, and selection: -->
[Laravel Prompts](/docs/11.x/prompts)에서 제공하는 `search` 또는 `multisearch` 기능을 사용하는 경우, `expectsSearch` assertion을 활용해서 사용자의 입력, 검색 결과, 선택지를 모킹할 수 있습니다.

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->expectsSearch('What is your name?', search: 'Tay', answers: [
            'Taylor Otwell',
            'Taylor Swift',
            'Darian Taylor'
        ], answer: 'Taylor Otwell')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->expectsSearch('What is your name?', search: 'Tay', answers: [
            'Taylor Otwell',
            'Taylor Swift',
            'Darian Taylor'
        ], answer: 'Taylor Otwell')
        ->assertExitCode(0);
}
```

<!-- You may also assert that a console command does not generate any output using the `doesntExpectOutput` method: -->
콘솔 명령어가 어떤 출력도 생성하지 않았는지 확인하고 싶다면, `doesntExpectOutput` 메서드를 사용할 수 있습니다.

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->doesntExpectOutput()
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
            ->doesntExpectOutput()
            ->assertExitCode(0);
}
```

<!-- The `expectsOutputToContain` and `doesntExpectOutputToContain` methods may be used to make assertions against a portion of the output: -->
`expectsOutputToContain` 및 `doesntExpectOutputToContain` 메서드를 사용하면, 출력 결과의 일부 문자열만 포함됐는지 또는 포함되지 않았는지 검증할 수 있습니다.

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->expectsOutputToContain('Taylor')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
            ->expectsOutputToContain('Taylor')
            ->assertExitCode(0);
}
```

<a name="confirmation-expectations"></a>
<!-- #### Confirmation Expectations -->
#### Confirmation Expectations

<!-- When writing a command which expects confirmation in the form of a "yes" or "no" answer, you may utilize the `expectsConfirmation` method: -->
명령어에서 "yes" 또는 "no"와 같은 추가 확인을 요구할 때에는, `expectsConfirmation` 메서드를 사용할 수 있습니다.

```
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
<!-- #### Table Expectations -->
#### Table Expectations

<!-- If your command displays a table of information using Artisan's `table` method, it can be cumbersome to write output expectations for the entire table. Instead, you may use the `expectsTable` method. This method accepts the table's headers as its first argument and the table's data as its second argument: -->
명령어가 Artisan의 `table` 메서드를 사용해서 정보를 테이블 형태로 출력하는 경우, 전체 테이블의 출력값을 일일이 검증하는 것이 번거로울 수 있습니다. 이런 경우에는 `expectsTable` 메서드를 활용할 수 있습니다. 이 메서드는 첫 번째 인자로 테이블의 헤더를, 두 번째 인자로 테이블의 데이터를 받습니다.

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
기본적으로, 애플리케이션의 테스트를 실행할 때는 `Illuminate\Console\Events\CommandStarting`과 `Illuminate\Console\Events\CommandFinished` 이벤트가 발생하지 않습니다. 그러나, 테스트 클래스에 `Illuminate\Foundation\Testing\WithConsoleEvents` 트레이트(trait)를 추가하면 이러한 이벤트를 활성화할 수 있습니다.

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\WithConsoleEvents;

uses(WithConsoleEvents::class);

// ...
```

```php tab=PHPUnit
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
