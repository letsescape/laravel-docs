# 콘솔 테스트 (Console Tests)

- [소개](#introduction)
- [성공 / 실패 기대값](#success-failure-expectations)
- [입력 / 출력 기대값](#input-output-expectations)
- [콘솔 이벤트](#console-events)

<a name="introduction"></a>
## 소개

HTTP 테스트를 간소화하는 것과 더불어, Laravel은 애플리케이션의 [사용자 정의 콘솔 명령어](/docs/master/artisan)를 테스트하기 위한 간단한 API도 제공합니다.

<a name="success-failure-expectations"></a>
## 성공 / 실패 기대값

먼저, Artisan 명령어의 종료 코드(exit code)에 대한 단언(assertion) 방법을 알아보겠습니다. 이를 위해 테스트에서 `artisan` 메서드를 사용해 Artisan 명령어를 호출한 후, `assertExitCode` 메서드를 통해 명령어가 원하는 종료 코드로 정상적으로 종료되었는지 단언할 수 있습니다.

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

또한, `assertNotExitCode` 메서드를 사용하여 명령어가 특정 종료 코드로 종료되지 않았는지 확인할 수도 있습니다.

```php
$this->artisan('inspire')->assertNotExitCode(1);
```

일반적으로 모든 터미널 명령어는 성공 시 `0`, 실패 시 0이 아닌 값을 반환합니다. 따라서 편의상, 해당 명령어가 성공적으로 종료되었는지 혹은 실패했는지 확인하는 `assertSuccessful`, `assertFailed` 메서드도 사용할 수 있습니다.

```php
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
## 입력 / 출력 기대값

Laravel에서는 `expectsQuestion` 메서드를 통해 콘솔 명령어 실행 시 사용자의 입력을 손쉽게 "모킹"할 수 있습니다. 또한, `assertExitCode` 및 `expectsOutput` 메서드를 이용해 명령어의 종료 코드와 출력될 텍스트도 기대값으로 지정할 수 있습니다. 예를 들어, 아래와 같은 콘솔 명령어가 있다고 가정해 보겠습니다.

```php
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

이 명령어에 대해 다음과 같이 테스트를 작성할 수 있습니다.

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

만약 [Laravel Prompts](/docs/master/prompts)에서 제공하는 `search` 또는 `multisearch` 기능을 사용 중이라면, `expectsSearch` 단언을 이용해 사용자의 입력, 검색 결과, 선택 값을 모킹할 수 있습니다.

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

또한, 명령어가 아무런 출력을 생성하지 않았는지 확인하려면 `doesntExpectOutput` 메서드를 사용할 수 있습니다.

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

출력의 일부에 대해 단언하고 싶다면, `expectsOutputToContain`와 `doesntExpectOutputToContain` 메서드를 활용할 수 있습니다.

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
#### 확인(Confirmation) 기대값

명령어에서 "예(yes)/아니오(no)" 형태의 확인을 요구하는 경우, `expectsConfirmation` 메서드를 사용할 수 있습니다.

```php
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
#### 테이블 출력 기대값

Artisan의 `table` 메서드를 통해 정보를 표(table) 형식으로 출력하는 경우, 전체 테이블의 출력을 테스트로 작성하는 것이 번거로울 수 있습니다. 이럴 때는 `expectsTable` 메서드를 활용하는 것이 좋습니다. 첫 번째 인수로 헤더(header), 두 번째 인수로 데이터(data) 배열을 전달합니다.

```php
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
## 콘솔 이벤트 (Console Events)

기본적으로 `Illuminate\Console\Events\CommandStarting` 및 `Illuminate\Console\Events\CommandFinished` 이벤트는 애플리케이션의 테스트 실행 중에는 디스패치되지 않습니다. 그러나, 테스트 클래스에 `Illuminate\Foundation\Testing\WithConsoleEvents` 트레이트(trait)를 추가하면 해당 이벤트 디스패치가 활성화됩니다.

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\WithConsoleEvents;

pest()->use(WithConsoleEvents::class);

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