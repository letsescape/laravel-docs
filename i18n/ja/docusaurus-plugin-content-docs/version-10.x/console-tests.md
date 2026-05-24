# コンソールテスト (Console Tests)

- [Introduction](#introduction)
- [成功/失敗の期待](#success-failure-expectations)
- [入力/出力の期待](#input-output-expectations)
- [コンソールイベント](#console-events)

<a name="introduction"></a>
## 導入 (Introduction)

HTTP テストの簡素化に加えて、Laravel はアプリケーションの [カスタムコンソールコマンド](/docs/{{version}}/artisan) をテストするためのシンプルな API を提供します。

<a name="success-failure-expectations"></a>
## 成功/失敗の期待 (Success / Failure Expectations)

まず、Artisan コマンドの終了コードに関するアサーションを行う方法を見てみましょう。これを達成するために、`artisan` メソッドを使用して、テストから Artisan コマンドを呼び出します。次に、`assertExitCode` メソッドを使用して、コマンドが指定された終了コードで完了したことをアサートします。

    /**
     * Test a console command.
     */
    public function test_console_command(): void
    {
        $this->artisan('inspire')->assertExitCode(0);
    }

`assertNotExitCode` メソッドを使用して、コマンドが特定の終了コードで終了しなかったことをアサートできます。

    $this->artisan('inspire')->assertNotExitCode(1);

もちろん、すべての端末コマンドは通常、成功した場合はステータス コード `0` で終了し、失敗した場合はゼロ以外の終了コードで終了します。したがって、便宜上、`assertSuccessful` および `assertFailed` アサーションを利用して、特定のコマンドが正常な終了コードで終了したかどうかをアサートできます。

    $this->artisan('inspire')->assertSuccessful();

    $this->artisan('inspire')->assertFailed();

<a name="input-output-expectations"></a>
## 入力/出力の期待 (Input / Output Expectations)

Laravel では、`expectsQuestion` メソッドを使用して、コンソール コマンドのユーザー入力を簡単に「モック」できます。さらに、`assertExitCode` および `expectsOutput` メソッドを使用して、コンソール コマンドによって出力されることが予想される終了コードとテキストを指定できます。たとえば、次のコンソール コマンドを考えてみましょう。

    Artisan::command('question', function () {
        $name = $this->ask('What is your name?');

        $language = $this->choice('Which language do you prefer?', [
            'PHP',
            'Ruby',
            'Python',
        ]);

        $this->line('Your name is '.$name.' and you prefer '.$language.'.');
    });

このコマンドは、`expectsQuestion`、`expectsOutput`、`doesntExpectOutput`、`expectsOutputToContain`、`doesntExpectOutputToContain`、および `assertExitCode` メソッドを使用する次のテストでテストできます。

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

<a name="confirmation-expectations"></a>
#### 確認の期待

「はい」または「いいえ」の回答形式での確認を要求するコマンドを作成する場合は、`expectsConfirmation` メソッドを使用できます。

    $this->artisan('module:import')
        ->expectsConfirmation('Do you really wish to run this command?', 'no')
        ->assertExitCode(1);

<a name="table-expectations"></a>
#### テーブルの期待値

コマンドが Artisan の `table` メソッドを使用して情報のテーブルを表示する場合、テーブル全体に対する出力の期待値を記述するのは面倒な場合があります。代わりに、`expectsTable` メソッドを使用できます。このメソッドは、テーブルのヘッダーを最初の引数として受け入れ、テーブルのデータを 2 番目の引数として受け入れます。

    $this->artisan('users:all')
        ->expectsTable([
            'ID',
            'Email',
        ], [
            [1, 'taylor@example.com'],
            [2, 'abigail@example.com'],
        ]);

<a name="console-events"></a>
## コンソールイベント (Console Events)

デフォルトでは、アプリケーションのテストの実行中に、`Illuminate\Console\Events\CommandStarting` および `Illuminate\Console\Events\CommandFinished` イベントは送出されません。ただし、クラスに `Illuminate\Foundation\Testing\WithConsoleEvents` 特性を追加することで、特定のテスト クラスに対してこれらのイベントを有効にすることができます。

    <?php
    
    namespace Tests\Feature;

    use Illuminate\Foundation\Testing\WithConsoleEvents;
    use Tests\TestCase;
    
    class ConsoleEventTest extends TestCase
    {
        use WithConsoleEvents;
    
        // ...
    }

