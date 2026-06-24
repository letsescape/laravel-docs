<!-- # Console Tests -->
# Console Tests

- [Introduction](#introduction)
- [Success / Failure Expectations](#success-failure-expectations)
- [Input / Output Expectations](#input-output-expectations)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In addition to simplifying HTTP testing, Laravel provides a simple API for testing your application's [custom console commands](/docs/8.x/artisan). -->
HTTP テストの簡素化に加えて、Laravel はアプリケーションの [custom console commands](/docs/8.x/artisan) をテストするためのシンプルな API を提供します。

<a name="success-failure-expectations"></a>
<!-- ## Success / Failure Expectations -->
## Success / Failure Expectations

<!-- To get started, let's explore how to make assertions regarding an Artisan command's exit code. To accomplish this, we will use the `artisan` method to invoke an Artisan command from our test. Then, we will use the `assertExitCode` method to assert that the command completed with a given exit code: -->
まず、Artisan コマンドの終了コードに関するアサーションを行う方法を見てみましょう。これを達成するために、`artisan` メソッドを使用して、テストから Artisan コマンドを呼び出します。次に、`assertExitCode` メソッドを使用して、コマンドが指定された終了コードで完了したことをアサートします。

```
/**
 * Test a console command.
 *
 * @return void
 */
public function test_console_command()
{
    $this->artisan('inspire')->assertExitCode(0);
}
```

<!-- You may use the `assertNotExitCode` method to assert that the command did not exit with a given exit code: -->
`assertNotExitCode` メソッドを使用して、コマンドが特定の終了コードで終了しなかったことをアサートできます。

```
$this->artisan('inspire')->assertNotExitCode(1);
```

<!-- Of course, all terminal commands typically exit with a status code of `0` when they are successful and a non-zero exit code when they are not successful. Therefore, for convenience, you may utilize the `assertSuccessful` and `assertFailed` assertions to assert that a given command exited with a successful exit code or not: -->
もちろん、すべての端末コマンドは通常、成功した場合はステータス コード `0` で終了し、失敗した場合はゼロ以外の終了コードで終了します。したがって、便宜上、`assertSuccessful` および `assertFailed` アサーションを利用して、特定のコマンドが正常な終了コードで終了したかどうかをアサートできます。

```
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
<!-- ## Input / Output Expectations -->
## Input / Output Expectations

<!-- Laravel allows you to easily "mock" user input for your console commands using the `expectsQuestion` method. In addition, you may specify the exit code and text that you expect to be output by the console command using the `assertExitCode` and `expectsOutput` methods. For example, consider the following console command: -->
Laravel では、`expectsQuestion` メソッドを使用して、コンソール コマンドのユーザー入力を簡単に「モック」できます。さらに、`assertExitCode` および `expectsOutput` メソッドを使用して、コンソール コマンドによって出力されることが予想される終了コードとテキストを指定できます。たとえば、次のコンソール コマンドを考えてみましょう。

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

<!-- You may test this command with the following test which utilizes the `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, and `assertExitCode` methods: -->
このコマンドは、`expectsQuestion`、`expectsOutput`、`doesntExpectOutput`、および `assertExitCode` メソッドを使用する次のテストでテストできます。

```
/**
 * Test a console command.
 *
 * @return void
 */
public function test_console_command()
{
    $this->artisan('question')
         ->expectsQuestion('What is your name?', 'Taylor Otwell')
         ->expectsQuestion('Which language do you prefer?', 'PHP')
         ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
         ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
         ->assertExitCode(0);
}
```

<a name="confirmation-expectations"></a>
<!-- #### Confirmation Expectations -->
#### Confirmation Expectations

<!-- When writing a command which expects confirmation in the form of a "yes" or "no" answer, you may utilize the `expectsConfirmation` method: -->
「はい」または「いいえ」の回答形式での確認を要求するコマンドを作成する場合は、`expectsConfirmation` メソッドを使用できます。

```
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
<!-- #### Table Expectations -->
#### Table Expectations

<!-- If your command displays a table of information using Artisan's `table` method, it can be cumbersome to write output expectations for the entire table. Instead, you may use the `expectsTable` method. This method accepts the table's headers as its first argument and the table's data as its second argument: -->
コマンドが Artisan の `table` メソッドを使用して情報のテーブルを表示する場合、テーブル全体に対する出力の期待値を記述するのは面倒な場合があります。代わりに、`expectsTable` メソッドを使用できます。このメソッドは、テーブルのヘッダーを最初の引数として受け入れ、テーブルのデータを 2 番目の引数として受け入れます。

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

