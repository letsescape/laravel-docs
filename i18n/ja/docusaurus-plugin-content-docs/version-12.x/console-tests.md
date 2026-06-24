<!-- # Console Tests -->
# Console Tests

- [Introduction](#introduction)
- [Success / Failure Expectations](#success-failure-expectations)
- [Input / Output Expectations](#input-output-expectations)
- [Console Events](#console-events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In addition to simplifying HTTP testing, Laravel provides a simple API for testing your application's [custom console commands](/docs/12.x/artisan). -->
HTTP テストの簡素化に加えて、Laravel はアプリケーションの [custom console commands](/docs/12.x/artisan) をテストするためのシンプルな API を提供します。

<a name="success-failure-expectations"></a>
<!-- ## Success / Failure Expectations -->
## Success / Failure Expectations

<!-- To get started, let's explore how to make assertions regarding an Artisan command's exit code. To accomplish this, we will use the `artisan` method to invoke an Artisan command from our test. Then, we will use the `assertExitCode` method to assert that the command completed with a given exit code: -->
まず、Artisan コマンドの終了コードに関するアサーションを行う方法を見てみましょう。これを達成するために、`artisan` メソッドを使用して、テストから Artisan コマンドを呼び出します。次に、`assertExitCode` メソッドを使用して、コマンドが指定された終了コードで完了したことをアサートします。

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
`assertNotExitCode` メソッドを使用して、コマンドが特定の終了コードで終了しなかったことをアサートできます。

```php
$this->artisan('inspire')->assertNotExitCode(1);
```

<!-- Of course, all terminal commands typically exit with a status code of `0` when they are successful and a non-zero exit code when they are not successful. Therefore, for convenience, you may utilize the `assertSuccessful` and `assertFailed` assertions to assert that a given command exited with a successful exit code or not: -->
もちろん、すべての端末コマンドは通常、成功した場合はステータス コード `0` で終了し、失敗した場合はゼロ以外の終了コードで終了します。したがって、便宜上、`assertSuccessful` および `assertFailed` アサーションを利用して、特定のコマンドが正常な終了コードで終了したかどうかをアサートできます。

```php
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
<!-- ## Input / Output Expectations -->
## Input / Output Expectations

<!-- Laravel allows you to easily "mock" user input for your console commands using the `expectsQuestion` method. In addition, you may specify the exit code and text that you expect to be output by the console command using the `assertExitCode` and `expectsOutput` methods. For example, consider the following console command: -->
Laravel では、`expectsQuestion` メソッドを使用して、コンソール コマンドのユーザー入力を簡単に「モック」できます。さらに、`assertExitCode` および `expectsOutput` メソッドを使用して、コンソール コマンドによって出力されることが予想される終了コードとテキストを指定できます。たとえば、次のコンソール コマンドを考えてみましょう。

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

<!-- You may test this command with the following test: -->
このコマンドは次のテストでテストできます。

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

<!-- If you are utilizing the `search` or `multisearch` functions provided by [Laravel Prompts](/docs/12.x/prompts), you may use the `expectsSearch` assertion to mock the user's input, search results, and selection: -->
[Laravel Prompts](/docs/12.x/prompts) によって提供される `search` 関数または `multisearch` 関数を利用している場合は、`expectsSearch` アサーションを使用してユーザーの入力、検索結果、および選択を模擬できます。

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
`doesntExpectOutput` メソッドを使用して、コンソール コマンドが出力を生成しないことをアサートすることもできます。

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
`expectsOutputToContain` メソッドと `doesntExpectOutputToContain` メソッドは、出力の一部に対してアサーションを行うために使用できます。

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
「はい」または「いいえ」の回答形式での確認を要求するコマンドを作成する場合は、`expectsConfirmation` メソッドを使用できます。

```php
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
<!-- #### Table Expectations -->
#### Table Expectations

<!-- If your command displays a table of information using Artisan's `table` method, it can be cumbersome to write output expectations for the entire table. Instead, you may use the `expectsTable` method. This method accepts the table's headers as its first argument and the table's data as its second argument: -->
コマンドが Artisan の `table` メソッドを使用して情報のテーブルを表示する場合、テーブル全体に対する出力の期待値を記述するのは面倒な場合があります。代わりに、`expectsTable` メソッドを使用できます。このメソッドは、テーブルのヘッダーを最初の引数として受け入れ、テーブルのデータを 2 番目の引数として受け入れます。

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
<!-- ## Console Events -->
## Console Events

<!-- By default, the `Illuminate\Console\Events\CommandStarting` and `Illuminate\Console\Events\CommandFinished` events are not dispatched while running your application's tests. However, you can enable these events for a given test class by adding the `Illuminate\Foundation\Testing\WithConsoleEvents` trait to the class: -->
デフォルトでは、アプリケーションのテストの実行中に、`Illuminate\Console\Events\CommandStarting` および `Illuminate\Console\Events\CommandFinished` イベントは送出されません。ただし、クラスに `Illuminate\Foundation\Testing\WithConsoleEvents` 特性を追加することで、特定のテスト クラスに対してこれらのイベントを有効にすることができます。

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

