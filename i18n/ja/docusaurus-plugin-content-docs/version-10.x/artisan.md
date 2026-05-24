# Artisan コンソール (Artisan Console)

- [Introduction](#introduction)
    - [Tinker (REPL)](#tinker)
- [コマンドの書き込み](#writing-commands)
    - [コマンドの生成](#generating-commands)
    - [コマンド構造](#command-structure)
    - [終了コマンド](#closure-commands)
    - [分離可能なコマンド](#isolatable-commands)
- [入力の期待値の定義](#defining-input-expectations)
    - [Arguments](#arguments)
    - [Options](#options)
    - [入力配列](#input-arrays)
    - [入力の説明](#input-descriptions)
    - [不足している入力のプロンプト](#prompting-for-missing-input)
- [コマンド入出力](#command-io)
    - [入力の取得](#retrieving-input)
    - [入力を求めるプロンプト](#prompting-for-input)
    - [出力の書き込み](#writing-output)
- [コマンドの登録](#registering-commands)
- [プログラムによるコマンドの実行](#programmatically-executing-commands)
    - [他のコマンドからのコマンドの呼び出し](#calling-commands-from-other-commands)
- [信号処理](#signal-handling)
- [スタブのカスタマイズ](#stub-customization)
- [Events](#events)

<a name="introduction"></a>
## 導入 (Introduction)

Artisan は、Laravel に含まれるコマンドライン インターフェイスです。 Artisan は、アプリケーションのルートに `artisan` スクリプトとして存在し、アプリケーションの構築時に役立つ多数の便利なコマンドを提供します。使用可能なすべての Artisan コマンドのリストを表示するには、`list` コマンドを使用します。

```shell
php artisan list
```

すべてのコマンドには、コマンドで使用可能な引数とオプションを表示および説明する「ヘルプ」画面も含まれています。ヘルプ画面を表示するには、コマンド名の前に `help` を付けます。

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

ローカル開発環境として [Laravel Sail](/docs/{{version}}/sail) を使用している場合は、必ず `sail` コマンド ラインを使用して Artisan コマンドを呼び出してください。 Sail は、アプリケーションの Docker コンテナ内で Artisan コマンドを実行します。

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

Laravel Tinker は、[PsySH](https://github.com/bobthecow/psysh) パッケージを利用した、Laravel フレームワーク用の強力な REPL です。

<a name="installation"></a>
#### インストール

すべての Laravel アプリケーションにはデフォルトで Tinker が含まれています。ただし、以前にアプリケーションから Tinker を削除した場合は、Composer を使用して Tinker をインストールできます。

```shell
composer require laravel/tinker
```

> [!NOTE]  
> Laravel アプリケーションを操作する際に、ホットリロード、複数行のコード編集、オートコンプリートをお探しですか? [Tinkerwell](https://tinkerwell.app) をチェックしてください。

<a name="usage"></a>
#### 使用法

Tinker を使用すると、Eloquent モデル、ジョブ、イベントなどを含む Laravel アプリケーション全体をコマンドラインで操作できます。 Tinker 環境に入るには、`tinker` Artisan コマンドを実行します。

```shell
php artisan tinker
```

`vendor:publish` コマンドを使用して、Tinker の構成ファイルを公開できます。

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]  
> `Dispatchable` クラスの `dispatch` ヘルパ関数と `dispatch` メソッドは、ガベージ コレクションに依存してジョブをキューに配置します。したがって、tinker を使用する場合は、`Bus::dispatch` または `Queue::push` を使用してジョブをディスパッチする必要があります。

<a name="command-allow-list"></a>
#### コマンド許可リスト

Tinker は、「許可」リストを利用して、シェル内でどの Artisan コマンドの実行を許可するかを決定します。デフォルトでは、`clear-compiled`、`down`、`env`、`inspire`、`migrate`、`optimize`、および `up` コマンドを実行できます。さらに多くのコマンドを許可したい場合は、`tinker.php` 構成ファイルの `commands` 配列にコマンドを追加できます。

    'commands' => [
        // App\Console\Commands\ExampleCommand::class,
    ],

<a name="classes-that-should-not-be-aliased"></a>
#### エイリアスを付けるべきではないクラス

通常、Tinker でクラスを操作すると、Tinker は自動的にクラスのエイリアスを作成します。ただし、クラスによっては別名を付けたくない場合もあります。これを行うには、`tinker.php` 構成ファイルの `dont_alias` 配列内のクラスをリストします。

    'dont_alias' => [
        App\Models\User::class,
    ],

<a name="writing-commands"></a>
## コマンドの書き込み (Writing Commands)

Artisan で提供されるコマンドに加えて、独自のカスタム コマンドを作成できます。コマンドは通常、`app/Console/Commands` ディレクトリに保存されます。ただし、Composer によってコマンドをロードできる限り、独自の保存場所を自由に選択できます。

<a name="generating-commands"></a>
### コマンドの生成

新しいコマンドを作成するには、`make:command` Artisan コマンドを使用できます。このコマンドは、`app/Console/Commands` ディレクトリに新しいコマンド クラスを作成します。このディレクトリがアプリケーションに存在しなくても心配する必要はありません。このディレクトリは、`make:command` Artisan コマンドを初めて実行するときに作成されます。

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### コマンド構造

コマンドを生成した後、クラスの `signature` プロパティと `description` プロパティに適切な値を定義する必要があります。これらのプロパティは、`list` 画面にコマンドを表示するときに使用されます。 `signature` プロパティを使用すると、[コマンドの入力の期待値](#defining-input-expectations) を定義することもできます。コマンドが実行されると、`handle` メソッドが呼び出されます。コマンド ロジックをこのメソッドに配置できます。

コマンドの例を見てみましょう。コマンドの `handle` メソッドを介して、必要な依存関係をリクエストできることに注意してください。 Laravel [サービスコンテナ](/docs/{{version}}/container) は、このメソッドのシグネチャでタイプヒントされているすべての依存関係を自動的に挿入します。

    <?php

    namespace App\Console\Commands;

    use App\Models\User;
    use App\Support\DripEmailer;
    use Illuminate\Console\Command;

    class SendEmails extends Command
    {
        /**
         * The name and signature of the console command.
         *
         * @var string
         */
        protected $signature = 'mail:send {user}';

        /**
         * The console command description.
         *
         * @var string
         */
        protected $description = 'Send a marketing email to a user';

        /**
         * Execute the console command.
         */
        public function handle(DripEmailer $drip): void
        {
            $drip->send(User::find($this->argument('user')));
        }
    }

> [!NOTE]  
> コードをより再利用するには、コンソール コマンドを軽量にし、アプリケーション サービスに任せてタスクを実行することをお勧めします。上の例では、電子メールの送信という「重労働」を行うためにサービス クラスを挿入していることに注意してください。

<a name="closure-commands"></a>
### 終了コマンド

クロージャ ベースのコマンドは、コンソール コマンドをクラスとして定義する代替手段を提供します。ルート クロージャがコントローラの代替であるのと同じように、コマンド クロージャはコマンド クラスの代替であると考えてください。 `app/Console/Kernel.php` ファイルの `commands` メソッド内で、Laravel は `routes/console.php` ファイルをロードします。

    /**
     * Register the closure based commands for the application.
     */
    protected function commands(): void
    {
        require base_path('routes/console.php');
    }

このファイルは HTTP ルートを定義しませんが、アプリケーションへのコンソール ベースのエントリ ポイント (ルート) を定義します。このファイル内で、`Artisan::command` メソッドを使用して、クロージャ ベースのコンソール コマンドをすべて定義できます。 `command` メソッドは、[コマンド署名](#defining-input-expectations) と、コマンドの引数とオプションを受け取るクロージャの 2 つの引数を受け入れます。

    Artisan::command('mail:send {user}', function (string $user) {
        $this->info("Sending email to: {$user}!");
    });

クロージャは基礎となるコマンド インスタンスにバインドされているため、通常は完全なコマンド クラスでアクセスできるすべてのヘルパ メソッドに完全にアクセスできます。

<a name="type-hinting-dependencies"></a>
#### タイプヒンティングの依存関係

コマンドの引数とオプションを受け取ることに加えて、コマンド クロージャは、[サービスコンテナ](/docs/{{version}}/container) から解決したい追加の依存関係をタイプヒントで受け取ることもできます。

    use App\Models\User;
    use App\Support\DripEmailer;

    Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
        $drip->send(User::find($user));
    });

<a name="closure-command-descriptions"></a>
#### クロージャコマンドの説明

クロージャベースのコマンドを定義する場合、`purpose` メソッドを使用してコマンドに説明を追加できます。この説明は、`php artisan list` または `php artisan help` コマンドを実行すると表示されます。

    Artisan::command('mail:send {user}', function (string $user) {
        // ...
    })->purpose('Send a marketing email to a user');

<a name="isolatable-commands"></a>
### 分離可能なコマンド

> [!WARNING]  
> この機能を利用するには、アプリケーションが `memcached`、`redis`、`dynamodb`、`database`、`file`、または `array` キャッシュ ドライバをアプリケーションのデフォルト キャッシュ ドライバとして使用している必要があります。さらに、すべてのサーバーが同じ中央キャッシュ サーバーと通信している必要があります。

場合によっては、コマンドのインスタンスを一度に 1 つだけ実行できるようにしたい場合があります。これを実現するには、コマンド クラスに `Illuminate\Contracts\Console\Isolatable` インターフェイスを実装します。

    <?php

    namespace App\Console\Commands;

    use Illuminate\Console\Command;
    use Illuminate\Contracts\Console\Isolatable;

    class SendEmails extends Command implements Isolatable
    {
        // ...
    }

コマンドが `Isolatable` としてマークされている場合、Laravel は自動的に `--isolated` オプションをコマンドに追加します。そのオプションを指定してコマンドが呼び出されると、Laravel はそのコマンドの他のインスタンスがすでに実行されていないことを確認します。 Laravel は、アプリケーションのデフォルトのキャッシュドライバを使用してアトミックロックの取得を試みることによってこれを実現します。コマンドの他のインスタンスが実行中の場合、コマンドは実行されません。ただし、コマンドは引き続き正常終了ステータス コードで終了します。

```shell
php artisan mail:send 1 --isolated
```

コマンドが実行できない場合に返される終了ステータス コードを指定したい場合は、`isolated` オプションを使用して目的のステータス コードを指定できます。

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### ロックID

デフォルトでは、Laravel はコマンド名を使用して、アプリケーションのキャッシュ内のアトミック ロックを取得するために使用される文字列キーを生成します。ただし、Artisan コマンド クラスで `isolatableId` メソッドを定義することでこのキーをカスタマイズでき、コマンドの引数またはオプションをキーに統合できます。

```php
/**
 * Get the isolatable ID for the command.
 */
public function isolatableId(): string
{
    return $this->argument('user');
}
```

<a name="lock-expiration-time"></a>
#### ロックの有効期限

デフォルトでは、分離ロックはコマンドの終了後に期限切れになります。または、コマンドが中断されて完了できない場合、ロックは 1 時間後に期限切れになります。ただし、コマンドで `isolationLockExpiresAt` メソッドを定義することで、ロックの有効期限を調整できます。

```php
use DateTimeInterface;
use DateInterval;

/**
 * Determine when an isolation lock expires for the command.
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->addMinutes(5);
}
```

<a name="defining-input-expectations"></a>
## 入力の期待値の定義 (Defining Input Expectations)

コンソール コマンドを作成するときは、引数またはオプションを通じてユーザーからの入力を収集するのが一般的です。 Laravel では、コマンドの `signature` プロパティを使用して、ユーザーから期待する入力を定義するのが非常に便利です。 `signature` プロパティを使用すると、コマンドの名前、引数、オプションを単一の表現力豊かなルートのような構文で定義できます。

<a name="arguments"></a>
### 引数

ユーザーが指定したすべての引数とオプションは中括弧で囲まれます。次の例では、コマンドは 1 つの必須引数 `user` を定義します。

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

引数をオプションにしたり、引数のデフォルト値を定義したりすることもできます。

    // Optional argument...
    'mail:send {user?}'

    // Optional argument with default value...
    'mail:send {user=foo}'

<a name="options"></a>
### オプション

オプションは、引数と同様、ユーザー入力の別の形式です。コマンド ライン経由でオプションを指定する場合、オプションには 2 つのハイフン (`--`) が接頭辞として付けられます。オプションには、値を受け取るオプションと受け取らないオプションの 2 種類があります。値を受け取らないオプションは、ブール値の「スイッチ」として機能します。このタイプのオプションの例を見てみましょう。

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user} {--queue}';

この例では、Artisan コマンドを呼び出すときに `--queue` スイッチを指定できます。 `--queue` スイッチが渡された場合、オプションの値は `true` になります。それ以外の場合、値は `false` になります。

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 値を含むオプション

次に、値を期待するオプションを見てみましょう。ユーザーがオプションの値を指定する必要がある場合は、オプション名の末尾に `=` 記号を付ける必要があります。

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user} {--queue=}';

この例では、ユーザーは次のようにオプションの値を渡すことができます。コマンドの呼び出し時にオプションが指定されていない場合、その値は `null` になります。

```shell
php artisan mail:send 1 --queue=default
```

オプション名の後にデフォルト値を指定することで、オプションにデフォルト値を割り当てることができます。ユーザーによってオプション値が渡されない場合は、デフォルト値が使用されます。

    'mail:send {user} {--queue=default}'

<a name="option-shortcuts"></a>
#### オプションのショートカット

オプションを定義するときにショートカットを割り当てるには、オプション名の前にショートカットを指定し、ショートカットを完全なオプション名から区切るための区切り文字として `|` 文字を使用します。

    'mail:send {user} {--Q|queue}'

端末でコマンドを呼び出すときは、オプションのショートカットの前に 1 つのハイフンを付ける必要があり、オプションの値を指定するときに `=` 文字を含めないでください。

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 入力配列

複数の入力値を想定する引数またはオプションを定義したい場合は、`*` 文字を使用できます。まず、そのような引数を指定する例を見てみましょう。

    'mail:send {user*}'

このメソッドを呼び出すとき、`user` 引数がコマンド ラインに順番に渡される場合があります。たとえば、次のコマンドは、`user` の値を、値として `1` および `2` を持つ配列に設定します。

```shell
php artisan mail:send 1 2
```

この `*` 文字をオプションの引数定義と組み合わせて、引数の 0 個以上のインスタンスを許可できます。

    'mail:send {user?*}'

<a name="option-arrays"></a>
#### オプション配列

複数の入力値を予期するオプションを定義する場合、コマンドに渡される各オプション値の先頭にオプション名を付ける必要があります。

    'mail:send {--id=*}'

このようなコマンドは、複数の `--id` 引数を渡すことによって呼び出すことができます。

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 入力の説明

コロンを使用して引数名と説明を区切ることにより、入力引数とオプションに説明を割り当てることができます。コマンドを定義するのに少し余裕が必要な場合は、自由に定義を複数行に分けて記述してください。

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send
                            {user : The ID of the user}
                            {--queue : Whether the job should be queued}';

<a name="prompting-for-missing-input"></a>
### 不足している入力のプロンプト

コマンドに必須の引数が含まれている場合、それらが指定されていないと、ユーザーはエラー メッセージを受け取ります。あるいは、`PromptsForMissingInput` インターフェイスを実装することで、必要な引数が欠落している場合にユーザーに自動的にプロンプ​​トを表示するようにコマンドを構成することもできます。

    <?php

    namespace App\Console\Commands;

    use Illuminate\Console\Command;
    use Illuminate\Contracts\Console\PromptsForMissingInput;

    class SendEmails extends Command implements PromptsForMissingInput
    {
        /**
         * The name and signature of the console command.
         *
         * @var string
         */
        protected $signature = 'mail:send {user}';

        // ...
    }

Laravel がユーザーから必要な引数を収集する必要がある場合、引数の名前または説明を使用して質問をインテリジェントに表現することで、自動的にユーザーに引数を求めます。必要な引数を収集するために使用される質問をカスタマイズしたい場合は、引数名をキーとする質問の配列を返す `promptForMissingArgumentsUsing` メソッドを実装できます。

    /**
     * Prompt for missing input arguments using the returned questions.
     *
     * @return array
     */
    protected function promptForMissingArgumentsUsing()
    {
        return [
            'user' => 'Which user ID should receive the mail?',
        ];
    }

質問とプレースホルダーを含むタプルを使用して、プレースホルダー テキストを提供することもできます。

    return [
        'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
    ];

プロンプトを完全に制御したい場合は、ユーザーにプロンプ​​トを表示し、その回答を返すクロージャーを提供できます。

    use App\Models\User;
    use function Laravel\Prompts\search;

    // ...

    return [
        'user' => fn () => search(
            label: 'Search for a user:',
            placeholder: 'E.g. Taylor Otwell',
            options: fn ($value) => strlen($value) > 0
                ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
                : []
        ),
    ];

> [!NOTE]  
包括的な [Laravelプロンプト](/docs/{{version}}/prompts) ドキュメントには、使用可能なプロンプトとその使用法に関する追加情報が含まれています。

ユーザーに [options](#options) の選択または入力を求めるプロンプトを表示したい場合は、コマンドの `handle` メソッドにプロンプ​​トを含めることができます。ただし、不足している引数についても自動的にプロンプ​​トが表示された場合にのみユーザーにプロンプ​​トを表示したい場合は、`afterPromptingForMissingArguments` メソッドを実装できます。

    use Symfony\Component\Console\Input\InputInterface;
    use Symfony\Component\Console\Output\OutputInterface;
    use function Laravel\Prompts\confirm;

    // ...

    /**
     * Perform actions after the user was prompted for missing arguments.
     *
     * @param  \Symfony\Component\Console\Input\InputInterface  $input
     * @param  \Symfony\Component\Console\Output\OutputInterface  $output
     * @return void
     */
    protected function afterPromptingForMissingArguments(InputInterface $input, OutputInterface $output)
    {
        $input->setOption('queue', confirm(
            label: 'Would you like to queue the mail?',
            default: $this->option('queue')
        ));
    }

<a name="command-io"></a>
## コマンド入出力 (Command I/O)

<a name="retrieving-input"></a>
### 入力の取得

コマンドの実行中に、コマンドで受け入れられる引数とオプションの値にアクセスする必要がある場合があります。これを行うには、`argument` メソッドと `option` メソッドを使用できます。引数またはオプションが存在しない場合は、`null` が返されます。

    /**
     * Execute the console command.
     */
    public function handle(): void
    {
        $userId = $this->argument('user');
    }

すべての引数を `array` として取得する必要がある場合は、`arguments` メソッドを呼び出します。

    $arguments = $this->arguments();

オプションは、`option` メソッドを使用して引数と同じくらい簡単に取得できます。すべてのオプションを配列として取得するには、`options` メソッドを呼び出します。

    // Retrieve a specific option...
    $queueName = $this->option('queue');

    // Retrieve all options as an array...
    $options = $this->options();

<a name="prompting-for-input"></a>
### 入力を求めるプロンプト

> [!NOTE]  
> [Laravelプロンプト](/docs/{{version}}/prompts) は、プレースホルダー テキストや検証などのブラウザーのような機能を備えた、美しくユーザーフレンドリーなフォームをコマンドライン アプリケーションに追加するための PHP パッケージです。

出力を表示するだけでなく、コマンドの実行中にユーザーに入力を求めることもできます。 `ask` メソッドは、ユーザーに指定された質問を表示し、入力を受け入れて、ユーザーの入力をコマンドに返します。

    /**
     * Execute the console command.
     */
    public function handle(): void
    {
        $name = $this->ask('What is your name?');

        // ...
    }

`ask` メソッドは、ユーザー入力が提供されない場合に返されるデフォルト値を指定するオプションの 2 番目の引数も受け入れます。

    $name = $this->ask('What is your name?', 'Taylor');

`secret` メソッドは `ask` に似ていますが、ユーザーの入力はコンソールに入力するときに表示されません。この方法は、パスワードなどの機密情報を要求する場合に役立ちます。

    $password = $this->secret('What is the password?');

<a name="asking-for-confirmation"></a>
#### 確認を求める

ユーザーに簡単な「はいまたはいいえ」の確認を求める必要がある場合は、`confirm` メソッドを使用できます。デフォルトでは、このメソッドは `false` を返します。ただし、ユーザーがプロンプトに応じて `y` または `yes` を入力すると、メソッドは `true` を返します。

    if ($this->confirm('Do you wish to continue?')) {
        // ...
    }

必要に応じて、`true` を `confirm` メソッドの 2 番目の引数として渡すことで、確認プロンプトがデフォルトで `true` を返すように指定できます。

    if ($this->confirm('Do you wish to continue?', true)) {
        // ...
    }

<a name="auto-completion"></a>
#### オートコンプリート

`anticipate` メソッドを使用すると、可能な選択肢のオートコンプリートを提供できます。ユーザーは、オートコンプリートのヒントに関係なく、任意の回答を入力できます。

    $name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);

あるいは、`anticipate` メソッドの 2 番目の引数としてクロージャーを渡すこともできます。クロージャは、ユーザーが入力文字を入力するたびに呼び出されます。クロージャは、これまでのユーザーの入力を含む文字列パラメータを受け入れ、オートコンプリートのオプションの配列を返す必要があります。

    $name = $this->anticipate('What is your address?', function (string $input) {
        // Return auto-completion options...
    });

<a name="multiple-choice-questions"></a>
#### 多肢選択問題

質問するときにユーザーに事前定義された一連の選択肢を提供する必要がある場合は、`choice` メソッドを使用できます。オプションが選択されていない場合に、メソッドの 3 番目の引数としてインデックスを渡すことにより、デフォルト値の配列インデックスが返されるように設定できます。

    $name = $this->choice(
        'What is your name?',
        ['Taylor', 'Dayle'],
        $defaultIndex
    );

さらに、`choice` メソッドは、有効な応答を選択する最大試行回数と複数の選択が許可されるかどうかを決定するためのオプションの 4 番目と 5 番目の引数を受け入れます。

    $name = $this->choice(
        'What is your name?',
        ['Taylor', 'Dayle'],
        $defaultIndex,
        $maxAttempts = null,
        $allowMultipleSelections = false
    );

<a name="writing-output"></a>
### 出力の書き込み

出力をコンソールに送信するには、`line`、`info`、`comment`、`question`、`warn`、および `error` メソッドを使用できます。これらの各メソッドは、目的に応じて適切な ANSI カラーを使用します。たとえば、一般的な情報をユーザーに表示してみましょう。通常、`info` メソッドはコンソールに緑色のテキストとして表示されます。

    /**
     * Execute the console command.
     */
    public function handle(): void
    {
        // ...

        $this->info('The command was successful!');
    }

エラー メッセージを表示するには、`error` メソッドを使用します。通常、エラー メッセージ テキストは赤色で表示されます。

    $this->error('Something went wrong!');

`line` メソッドを使用して、色の付いていないプレーン テキストを表示できます。

    $this->line('Display this on the screen');

`newLine` メソッドを使用して空行を表示できます。

    // Write a single blank line...
    $this->newLine();

    // Write three blank lines...
    $this->newLine(3);

<a name="tables"></a>
#### テーブル

`table` メソッドを使用すると、複数の行/列のデータを簡単に正しくフォーマットできます。テーブルの列名とデータを指定するだけで、Laravel が自動的に実行します。
テーブルの適切な幅と高さを自動的に計算します。

    use App\Models\User;

    $this->table(
        ['Name', 'Email'],
        User::all(['name', 'email'])->toArray()
    );

<a name="progress-bars"></a>
#### プログレスバー

長時間実行されるタスクの場合は、タスクの完了度をユーザーに知らせる進行状況バーを表示すると便利です。 `withProgressBar` メソッドを使用すると、Laravel は進行状況バーを表示し、指定された反復可能な値を超えて反復ごとに進行状況を進めます。

    use App\Models\User;

    $users = $this->withProgressBar(User::all(), function (User $user) {
        $this->performTask($user);
    });

場合によっては、進行状況バーの進み方を手動で制御する必要がある場合があります。まず、プロセスが反復処理される合計ステップ数を定義します。次に、各項目を処理した後、進行状況バーを進めます。

    $users = App\Models\User::all();

    $bar = $this->output->createProgressBar(count($users));

    $bar->start();

    foreach ($users as $user) {
        $this->performTask($user);

        $bar->advance();
    }

    $bar->finish();

> [!NOTE]  
> より高度なオプションについては、[Symfony プログレスバーコンポーネントのドキュメント](https://symfony.com/doc/current/components/console/helpers/progressbar.html) を確認してください。

<a name="registering-commands"></a>
## コマンドの登録 (Registering Commands)

すべてのコンソール コマンドは、アプリケーションの「コンソール カーネル」である `App\Console\Kernel` クラス内に登録されます。このクラスの `commands` メソッド内に、カーネルの `load` メソッドへの呼び出しが表示されます。 `load` メソッドは、`app/Console/Commands` ディレクトリをスキャンし、そこに含まれる各コマンドを Artisan に自動的に登録します。 `load` メソッドへの追加呼び出しを自由に実行して、Artisan コマンドの他のディレクトリをスキャンすることもできます。

    /**
     * Register the commands for the application.
     */
    protected function commands(): void
    {
        $this->load(__DIR__.'/Commands');
        $this->load(__DIR__.'/../Domain/Orders/Commands');

        // ...
    }

必要に応じて、コマンドのクラス名を `App\Console\Kernel` クラス内の `$commands` プロパティに追加することで、コマンドを手動で登録できます。このプロパティがカーネルでまだ定義されていない場合は、手動で定義する必要があります。 Artisan が起動すると、このプロパティにリストされているすべてのコマンドが [サービスコンテナ](/docs/{{version}}/container) によって解決され、Artisan に登録されます。

    protected $commands = [
        Commands\SendEmails::class
    ];

<a name="programmatically-executing-commands"></a>
## プログラムによるコマンドの実行 (Programmatically Executing Commands)

場合によっては、CLI の外部で Artisan コマンドを実行したい場合があります。たとえば、ルートまたはコントローラからArtisan コマンドを実行したい場合があります。これを実現するには、`Artisan` ファサードで `call` メソッドを使用できます。 `call` メソッドは、コマンドのシグネチャ名またはクラス名のいずれかを最初の引数として受け入れ、コマンド パラメーターの配列を 2 番目の引数として受け入れます。終了コードが返されます。

    use Illuminate\Support\Facades\Artisan;

    Route::post('/user/{user}/mail', function (string $user) {
        $exitCode = Artisan::call('mail:send', [
            'user' => $user, '--queue' => 'default'
        ]);

        // ...
    });

あるいは、Artisan コマンド全体を文字列として `call` メソッドに渡すこともできます。

    Artisan::call('mail:send 1 --queue=default');

<a name="passing-array-values"></a>
#### 配列値の受け渡し

コマンドが配列を受け入れるオプションを定義している場合は、そのオプションに値の配列を渡すことができます。

    use Illuminate\Support\Facades\Artisan;

    Route::post('/mail', function () {
        $exitCode = Artisan::call('mail:send', [
            '--id' => [5, 13]
        ]);
    });

<a name="passing-boolean-values"></a>
#### ブール値を渡す

文字列値を受け入れないオプションの値 (`migrate:refresh` コマンドの `--force` フラグなど) を指定する必要がある場合は、オプションの値として `true` または `false` を渡す必要があります。

    $exitCode = Artisan::call('migrate:refresh', [
        '--force' => true,
    ]);

<a name="queueing-artisan-commands"></a>
#### Artisan コマンドのキューイング

`Artisan` ファサードで `queue` メソッドを使用すると、Artisan コマンドをキューに入れて、[キューワーカー](/docs/{{version}}/queues) によってバックグラウンドで処理されるようにすることもできます。この方法を使用する前に、キューを設定し、キュー リスナを実行していることを確認してください。

    use Illuminate\Support\Facades\Artisan;

    Route::post('/user/{user}/mail', function (string $user) {
        Artisan::queue('mail:send', [
            'user' => $user, '--queue' => 'default'
        ]);

        // ...
    });

`onConnection` メソッドと `onQueue` メソッドを使用すると、Artisan コマンドをディスパッチする接続またはキューを指定できます。

    Artisan::queue('mail:send', [
        'user' => 1, '--queue' => 'default'
    ])->onConnection('redis')->onQueue('commands');

<a name="calling-commands-from-other-commands"></a>
### 他のコマンドからのコマンドの呼び出し

場合によっては、既存の Artisan コマンドから他のコマンドを呼び出したい場合があります。これは、`call` メソッドを使用して行うことができます。この `call` メソッドは、コマンド名とコマンド引数/オプションの配列を受け入れます。

    /**
     * Execute the console command.
     */
    public function handle(): void
    {
        $this->call('mail:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        // ...
    }

別のコンソール コマンドを呼び出してその出力をすべて抑制したい場合は、`callSilently` メソッドを使用できます。 `callSilently` メソッドには、`call` メソッドと同じシグネチャがあります。

    $this->callSilently('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

<a name="signal-handling"></a>
## 信号処理 (Signal Handling)

ご存知かもしれませんが、オペレーティング システムでは、実行中のプロセスにシグナルを送信できます。たとえば、`SIGTERM` 信号は、オペレーティング システムがプログラムに終了を要求する方法です。 Artisan コンソール コマンドでシグナルをリッスンし、シグナルが発生したときにコードを実行したい場合は、`trap` メソッドを使用できます。

    /**
     * Execute the console command.
     */
    public function handle(): void
    {
        $this->trap(SIGTERM, fn () => $this->shouldKeepRunning = false);

        while ($this->shouldKeepRunning) {
            // ...
        }
    }

一度に複数の信号をリッスンするには、信号の配列を `trap` メソッドに提供します。

    $this->trap([SIGTERM, SIGQUIT], function (int $signal) {
        $this->shouldKeepRunning = false;

        dump($signal); // SIGTERM / SIGQUIT
    });

<a name="stub-customization"></a>
## スタブのカスタマイズ (Stub Customization)

Artisan コンソールの `make` コマンドは、コントローラ、ジョブ、移行、テストなどのさまざまなクラスを作成するために使用されます。これらのクラスは、入力に基づいて値が設定される「スタブ」ファイルを使用して生成されます。ただし、Artisan によって生成されたファイルに小さな変更を加えたい場合があります。これを実現するには、`stub:publish` コマンドを使用して最も一般的なスタブをアプリケーションに公開し、カスタマイズできるようにします。

```shell
php artisan stub:publish
```

公開されたスタブは、アプリケーションのルートの `stubs` ディレクトリ内に配置されます。これらのスタブに加えた変更は、Artisan の `make` コマンドを使用して対応するクラスを生成するときに反映されます。

<a name="events"></a>
## イベント (Events)

Artisan は、コマンドの実行時に `Illuminate\Console\Events\ArtisanStarting`、`Illuminate\Console\Events\CommandStarting`、および `Illuminate\Console\Events\CommandFinished` の 3 つのイベントを送出します。 `ArtisanStarting` イベントは、Artisan の実行が開始されるとすぐに送出されます。次に、コマンドが実行される直前に、`CommandStarting` イベントが送出されます。最後に、コマンドの実行が終了すると、`CommandFinished` イベントが送出されます。

