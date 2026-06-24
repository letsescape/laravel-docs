<!-- # Artisan Console -->
# Artisan Console

- [Introduction](#introduction)
    - [Tinker (REPL)](#tinker)
- [Writing Commands](#writing-commands)
    - [Generating Commands](#generating-commands)
    - [Command Structure](#command-structure)
    - [Closure Commands](#closure-commands)
    - [Isolatable Commands](#isolatable-commands)
- [Defining Input Expectations](#defining-input-expectations)
    - [Arguments](#arguments)
    - [Options](#options)
    - [Input Arrays](#input-arrays)
    - [Input Descriptions](#input-descriptions)
    - [Prompting for Missing Input](#prompting-for-missing-input)
- [Command I/O](#command-io)
    - [Retrieving Input](#retrieving-input)
    - [Prompting for Input](#prompting-for-input)
    - [Writing Output](#writing-output)
- [Registering Commands](#registering-commands)
- [Programmatically Executing Commands](#programmatically-executing-commands)
    - [Calling Commands From Other Commands](#calling-commands-from-other-commands)
- [Signal Handling](#signal-handling)
- [Stub Customization](#stub-customization)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Artisan is the command line interface included with Laravel. Artisan exists at the root of your application as the `artisan` script and provides a number of helpful commands that can assist you while you build your application. To view a list of all available Artisan commands, you may use the `list` command: -->
Artisan は、Laravel に含まれるコマンドライン インターフェイスです。 Artisan は、アプリケーションのルートに `artisan` スクリプトとして存在し、アプリケーションの構築時に役立つ多数の便利なコマンドを提供します。使用可能なすべての Artisan コマンドのリストを表示するには、`list` コマンドを使用します。

```shell
php artisan list
```

<!-- Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, precede the name of the command with `help`: -->
すべてのコマンドには、コマンドで使用可能な引数とオプションを表示および説明する「ヘルプ」画面も含まれています。ヘルプ画面を表示するには、コマンド名の前に `help` を付けます。

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
<!-- #### Laravel Sail -->
#### Laravel Sail

<!-- If you are using [Laravel Sail](/docs/13.x/sail) as your local development environment, remember to use the `sail` command line to invoke Artisan commands. Sail will execute your Artisan commands within your application's Docker containers: -->
ローカル開発環境として [Laravel Sail](/docs/13.x/sail) を使用している場合は、必ず `sail` コマンド ラインを使用して Artisan コマンドを呼び出してください。 Sail は、アプリケーションの Docker コンテナ内で Artisan コマンドを実行します。

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
<!-- ### Tinker (REPL) -->
### Tinker (REPL)

<!-- [Laravel Tinker](https://github.com/laravel/tinker) is a powerful REPL for the Laravel framework, powered by the [PsySH](https://github.com/bobthecow/psysh) package. -->
[Laravel Tinker](https://github.com/laravel/tinker) は、[PsySH](https://github.com/bobthecow/psysh) パッケージを利用した、Laravel フレームワーク用の強力な REPL です。

<a name="installation"></a>
<!-- #### Installation -->
#### Installation

<!-- All Laravel applications include Tinker by default. However, you may install Tinker using Composer if you have previously removed it from your application: -->
すべての Laravel アプリケーションにはデフォルトで Tinker が含まれています。ただし、以前にアプリケーションから Tinker を削除した場合は、Composer を使用して Tinker をインストールできます。

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel アプリケーションを操作する際に、ホットリロード、複数行のコード編集、オートコンプリートをお探しですか? [Tinkerwell](https://tinkerwell.app) をチェックしてください。

<a name="usage"></a>
<!-- #### Usage -->
#### Usage

<!-- Tinker allows you to interact with your entire Laravel application on the command line, including your Eloquent models, jobs, events, and more. To enter the Tinker environment, run the `tinker` Artisan command: -->
Tinker を使用すると、Eloquent モデル、ジョブ、イベントなどを含む Laravel アプリケーション全体をコマンドラインで操作できます。 Tinker 環境に入るには、`tinker` Artisan コマンドを実行します。

```shell
php artisan tinker
```

<!-- You can publish Tinker's configuration file using the `vendor:publish` command: -->
`vendor:publish` コマンドを使用して、Tinker の構成ファイルを公開できます。

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `Dispatchable` クラスの `dispatch` ヘルパ関数と `dispatch` メソッドは、ガベージ コレクションに依存してジョブをキューに配置します。したがって、Tinker を使用する場合は、`Bus::dispatch` または `Queue::push` を使用してジョブをディスパッチする必要があります。

<a name="command-allow-list"></a>
<!-- #### Command Allow List -->
#### Command Allow List

<!-- Tinker utilizes an "allow" list to determine which Artisan commands are allowed to be run within its shell. By default, you may run the `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, and `optimize` commands. If you would like to allow more commands you may add them to the `commands` array in your `tinker.php` configuration file: -->
Tinker は、「許可」リストを利用して、シェル内でどの Artisan コマンドの実行を許可するかを決定します。デフォルトでは、`clear-compiled`、`down`、`env`、`inspire`、`migrate`、`migrate:install`、`up`、および `optimize` コマンドを実行できます。さらに多くのコマンドを許可したい場合は、`tinker.php` 構成ファイルの `commands` 配列にコマンドを追加できます。

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
<!-- #### Classes That Should Not Be Aliased -->
#### Classes That Should Not Be Aliased

<!-- Typically, Tinker automatically aliases classes as you interact with them in Tinker. However, you may wish to never alias some classes. You may accomplish this by listing the classes in the `dont_alias` array of your `tinker.php` configuration file: -->
通常、Tinker でクラスを操作すると、Tinker は自動的にクラスのエイリアスを作成します。ただし、クラスによっては別名を付けたくない場合もあります。これを行うには、`tinker.php` 構成ファイルの `dont_alias` 配列内のクラスをリストします。

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
<!-- ## Writing Commands -->
## Writing Commands

<!-- In addition to the commands provided with Artisan, you may build your own custom commands. Commands are typically stored in the `app/Console/Commands` directory; however, you are free to choose your own storage location as long as you instruct Laravel to [scan other directories for Artisan commands](#registering-commands). -->
Artisan で提供されるコマンドに加えて、独自のカスタム コマンドを作成できます。コマンドは通常、`app/Console/Commands` ディレクトリに保存されます。ただし、Laravel に [scan other directories for Artisan commands](#registering-commands) を指示する限り、独自の保存場所を自由に選択できます。

<a name="generating-commands"></a>
<!-- ### Generating Commands -->
### Generating Commands

<!-- To create a new command, you may use the `make:command` Artisan command. This command will create a new command class in the `app/Console/Commands` directory. Don't worry if this directory does not exist in your application - it will be created the first time you run the `make:command` Artisan command: -->
新しいコマンドを作成するには、`make:command` Artisan コマンドを使用できます。このコマンドは、`app/Console/Commands` ディレクトリに新しいコマンド クラスを作成します。このディレクトリがアプリケーションに存在しなくても心配する必要はありません。このディレクトリは、`make:command` Artisan コマンドを初めて実行するときに作成されます。

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
<!-- ### Command Structure -->
### Command Structure

<!-- After generating your command, you should define the command's signature and description using the `Signature` and `Description` attributes. The `Signature` attribute also allows you to define [your command's input expectations](#defining-input-expectations). The `handle` method will be called when your command is executed. You may place your command logic in this method. -->
コマンドを生成した後、`Signature` 属性と `Description` 属性を使用してコマンドの署名と説明を定義する必要があります。 `Signature` 属性を使用すると、[your command's input expectations](#defining-input-expectations) を定義することもできます。コマンドが実行されると、`handle` メソッドが呼び出されます。コマンド ロジックをこのメソッドに配置できます。

<!-- Let's take a look at an example command. Note that we are able to request any dependencies we need via the command's `handle` method. The Laravel [service container](/docs/13.x/container) will automatically inject all dependencies that are type-hinted in this method's signature: -->
コマンドの例を見てみましょう。コマンドの `handle` メソッドを介して、必要な依存関係をリクエストできることに注意してください。 Laravel [service container](/docs/13.x/container) は、このメソッドのシグネチャでタイプヒントされているすべての依存関係を自動的に挿入します。

```php
<?php

namespace App\Console\Commands;

use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;

#[Signature('mail:send {user}')]
#[Description('Send a marketing email to a user')]
class SendEmails extends Command
{
    /**
     * Execute the console command.
     */
    public function handle(DripEmailer $drip): void
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```

> [!NOTE]
> コードをより再利用するには、コンソール コマンドを軽量にし、アプリケーション サービスに任せてタスクを実行することをお勧めします。上の例では、電子メールの送信という「重労働」を行うためにサービス クラスを挿入していることに注意してください。

<a name="exit-codes"></a>
<!-- #### Exit Codes -->
#### Exit Codes

<!-- If nothing is returned from the `handle` method and the command executes successfully, the command will exit with a `0` exit code, indicating success. However, the `handle` method may optionally return an integer to manually specify the command's exit code: -->
`handle` メソッドから何も返されず、コマンドが正常に実行された場合、コマンドは成功を示す `0` 終了コードで終了します。ただし、`handle` メソッドは、コマンドの終了コードを手動で指定するために、オプションで整数を返すことができます。

```php
$this->error('Something went wrong.');

return 1;
```

<!-- If you would like to "fail" the command from any method within the command, you may utilize the `fail` method. The `fail` method will immediately terminate execution of the command and return an exit code of `1`: -->
コマンド内のいずれかのメソッドでコマンドを「失敗」させたい場合は、`fail` メソッドを利用できます。 `fail` メソッドはコマンドの実行を直ちに終了し、終了コード `1` を返します。

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
<!-- ### Closure Commands -->
### Closure Commands

<!-- Closure-based commands provide an alternative to defining console commands as classes. In the same way that route closures are an alternative to controllers, think of command closures as an alternative to command classes. -->
クロージャベースのコマンドは、コンソール コマンドをクラスとして定義する代替手段を提供します。ルート クロージャがコントローラの代替であるのと同じように、コマンド クロージャはコマンド クラスの代替であると考えてください。

<!-- Even though the `routes/console.php` file does not define HTTP routes, it defines console-based entry points (routes) into your application. Within this file, you may define all of your closure-based console commands using the `Artisan::command` method. The `command` method accepts two arguments: the [command signature](#defining-input-expectations) and a closure which receives the command's arguments and options: -->
`routes/console.php` ファイルは HTTP ルートを定義しませんが、アプリケーションへのコンソール ベースのエントリ ポイント (ルート) を定義します。このファイル内では、`Artisan::command` メソッドを使用して、クロージャベースのコンソール コマンドをすべて定義できます。 `command` メソッドは、[command signature](#defining-input-expectations) と、コマンドの引数とオプションを受け取るクロージャの 2 つの引数を受け入れます。

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

<!-- The closure is bound to the underlying command instance, so you have full access to all of the helper methods you would typically be able to access on a full command class. -->
クロージャは基礎となるコマンド インスタンスにバインドされているため、通常は完全なコマンド クラスでアクセスできるすべてのヘルパ メソッドに完全にアクセスできます。

<a name="type-hinting-dependencies"></a>
<!-- #### Type-Hinting Dependencies -->
#### Type-Hinting Dependencies

<!-- In addition to receiving your command's arguments and options, command closures may also type-hint additional dependencies that you would like resolved out of the [service container](/docs/13.x/container): -->
コマンドの引数とオプションを受け取ることに加えて、コマンド クロージャは、[service container](/docs/13.x/container) から解決したい追加の依存関係をタイプヒントで受け取ることもできます。

```php
use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Support\Facades\Artisan;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
<!-- #### Closure Command Descriptions -->
#### Closure Command Descriptions

<!-- When defining a closure-based command, you may use the `purpose` method to add a description to the command. This description will be displayed when you run the `php artisan list` or `php artisan help` commands: -->
クロージャベースのコマンドを定義する場合、`purpose` メソッドを使用してコマンドに説明を追加できます。この説明は、`php artisan list` または `php artisan help` コマンドを実行すると表示されます。

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
<!-- ### Isolatable Commands -->
### Isolatable Commands

> [!WARNING]
> この機能を利用するには、アプリケーションが `memcached`、`redis`、`dynamodb`、`database`、`file`、または `array` キャッシュ ドライバをアプリケーションのデフォルト キャッシュ ドライバとして使用している必要があります。さらに、すべてのサーバーが同じ中央キャッシュ サーバーと通信している必要があります。

<!-- Sometimes you may wish to ensure that only one instance of a command can run at a time. To accomplish this, you may implement the `Illuminate\Contracts\Console\Isolatable` interface on your command class: -->
場合によっては、コマンドのインスタンスを一度に 1 つだけ実行できるようにしたい場合があります。これを実現するには、コマンド クラスに `Illuminate\Contracts\Console\Isolatable` インターフェイスを実装します。

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\Isolatable;

class SendEmails extends Command implements Isolatable
{
    // ...
}
```

<!-- When you mark a command as `Isolatable`, Laravel automatically makes the `--isolated` option available for the command without needing to explicitly define it in the command's options. When the command is invoked with that option, Laravel will ensure that no other instances of that command are already running. Laravel accomplishes this by attempting to acquire an atomic lock using your application's default cache driver. If other instances of the command are running, the command will not execute; however, the command will still exit with a successful exit status code: -->
コマンドを`Isolatable`としてマークすると、Laravelはコマンドのオプションで明示的に定義しなくても、自動的に`--isolated`オプションをコマンドで使用できるようになります。そのオプションを指定してコマンドが呼び出されると、Laravel はそのコマンドの他のインスタンスがすでに実行されていないことを確認します。 Laravel は、アプリケーションのデフォルトのキャッシュドライバを使用してアトミックロックの取得を試みることによってこれを実現します。コマンドの他のインスタンスが実行中の場合、コマンドは実行されません。ただし、コマンドは引き続き正常終了ステータス コードで終了します。

```shell
php artisan mail:send 1 --isolated
```

<!-- If you would like to specify the exit status code that the command should return if it is not able to execute, you may provide the desired status code via the `isolated` option: -->
コマンドが実行できない場合に返される終了ステータス コードを指定したい場合は、`isolated` オプションを使用して目的のステータス コードを指定できます。

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
<!-- #### Lock ID -->
#### Lock ID

<!-- By default, Laravel will use the command's name to generate the string key that is used to acquire the atomic lock in your application's cache. However, you may customize this key by defining an `isolatableId` method on your Artisan command class, allowing you to integrate the command's arguments or options into the key: -->
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
<!-- #### Lock Expiration Time -->
#### Lock Expiration Time

<!-- By default, isolation locks expire after the command is finished. Or, if the command is interrupted and unable to finish, the lock will expire after one hour. However, you may adjust the lock expiration time by defining an `isolationLockExpiresAt` method on your command: -->
デフォルトでは、分離ロックはコマンドの終了後に期限切れになります。または、コマンドが中断されて完了できない場合、ロックは 1 時間後に期限切れになります。ただし、コマンドで `isolationLockExpiresAt` メソッドを定義することで、ロックの有効期限を調整できます。

```php
use DateTimeInterface;
use DateInterval;

/**
 * Determine when an isolation lock expires for the command.
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->plus(minutes: 5);
}
```

<a name="defining-input-expectations"></a>
<!-- ## Defining Input Expectations -->
## Defining Input Expectations

<!-- When writing console commands, it is common to gather input from the user through arguments or options. Laravel makes it very convenient to define the input you expect from the user using the `signature` property on your commands. The `signature` property allows you to define the name, arguments, and options for the command in a single, expressive, route-like syntax. -->
コンソール コマンドを作成するときは、引数またはオプションを通じてユーザーからの入力を収集するのが一般的です。 Laravel では、コマンドの `signature` プロパティを使用して、ユーザーから期待する入力を定義するのが非常に便利です。 `signature` プロパティを使用すると、コマンドの名前、引数、オプションを単一の表現力豊かなルートのような構文で定義できます。

<a name="arguments"></a>
<!-- ### Arguments -->
### Arguments

<!-- All user supplied arguments and options are wrapped in curly braces. In the following example, the command defines one required argument: `user`: -->
ユーザーが指定したすべての引数とオプションは中括弧で囲まれます。次の例では、コマンドは 1 つの必須引数 `user` を定義します。

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

<!-- You may also make arguments optional or define default values for arguments: -->
引数をオプションにしたり、引数のデフォルト値を定義したりすることもできます。

```php
// Optional argument...
'mail:send {user?}'

// Optional argument with default value...
'mail:send {user=foo}'
```

<a name="options"></a>
<!-- ### Options -->
### Options

<!-- Options, like arguments, are another form of user input. Options are prefixed by two hyphens (`--`) when they are provided via the command line. There are two types of options: those that receive a value and those that don't. Options that don't receive a value serve as a boolean "switch". Let's take a look at an example of this type of option: -->
オプションは、引数と同様、ユーザー入力の別の形式です。コマンド ライン経由でオプションを指定する場合、オプションには 2 つのハイフン (`--`) が接頭辞として付けられます。オプションには、値を受け取るオプションと受け取らないオプションの 2 種類があります。値を受け取らないオプションは、ブール値の「スイッチ」として機能します。このタイプのオプションの例を見てみましょう。

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

<!-- In this example, the `--queue` switch may be specified when calling the Artisan command. If the `--queue` switch is passed, the value of the option will be `true`. Otherwise, the value will be `false`: -->
この例では、Artisan コマンドを呼び出すときに `--queue` スイッチを指定できます。 `--queue` スイッチが渡された場合、オプションの値は `true` になります。それ以外の場合、値は `false` になります。

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
<!-- #### Options With Values -->
#### Options With Values

<!-- Next, let's take a look at an option that expects a value. If the user must specify a value for an option, you should suffix the option name with a `=` sign: -->
次に、値を期待するオプションを見てみましょう。ユーザーがオプションの値を指定する必要がある場合は、オプション名の末尾に `=` 記号を付ける必要があります。

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

<!-- In this example, the user may pass a value for the option like so. If the option is not specified when invoking the command, its value will be `null`: -->
この例では、ユーザーは次のようにオプションの値を渡すことができます。コマンドの呼び出し時にオプションが指定されていない場合、その値は `null` になります。

```shell
php artisan mail:send 1 --queue=default
```

<!-- You may assign default values to options by specifying the default value after the option name. If no option value is passed by the user, the default value will be used: -->
オプション名の後にデフォルト値を指定することで、オプションにデフォルト値を割り当てることができます。ユーザーによってオプション値が渡されない場合は、デフォルト値が使用されます。

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
<!-- #### Option Shortcuts -->
#### Option Shortcuts

<!-- To assign a shortcut when defining an option, you may specify it before the option name and use the `|` character as a delimiter to separate the shortcut from the full option name: -->
オプションを定義するときにショートカットを割り当てるには、オプション名の前にショートカットを指定し、ショートカットを完全なオプション名から区切るための区切り文字として `|` 文字を使用します。

```php
'mail:send {user} {--Q|queue=}'
```

<!-- When invoking the command on your terminal, option shortcuts should be prefixed with a single hyphen and no `=` character should be included when specifying a value for the option: -->
端末でコマンドを呼び出すときは、オプションのショートカットの前に 1 つのハイフンを付ける必要があり、オプションの値を指定するときに `=` 文字を含めないでください。

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
<!-- ### Input Arrays -->
### Input Arrays

<!-- If you would like to define arguments or options to expect multiple input values, you may use the `*` character. First, let's take a look at an example that specifies such an argument: -->
複数の入力値を想定する引数またはオプションを定義したい場合は、`*` 文字を使用できます。まず、そのような引数を指定する例を見てみましょう。

```php
'mail:send {user*}'
```

<!-- When running this command, the `user` arguments may be passed in order to the command line. For example, the following command will set the value of `user` to an array with `1` and `2` as its values: -->
このコマンドを実行するとき、`user` 引数がコマンド ラインに順番に渡される場合があります。たとえば、次のコマンドは、`user` の値を、値として `1` および `2` を持つ配列に設定します。

```shell
php artisan mail:send 1 2
```

<!-- This `*` character can be combined with an optional argument definition to allow zero or more instances of an argument: -->
この `*` 文字をオプションの引数定義と組み合わせて、引数の 0 個以上のインスタンスを許可できます。

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
<!-- #### Option Arrays -->
#### Option Arrays

<!-- When defining an option that expects multiple input values, each option value passed to the command should be prefixed with the option name: -->
複数の入力値を予期するオプションを定義する場合、コマンドに渡される各オプション値の先頭にオプション名を付ける必要があります。

```php
'mail:send {--id=*}'
```

<!-- Such a command may be invoked by passing multiple `--id` arguments: -->
このようなコマンドは、複数の `--id` 引数を渡すことによって呼び出すことができます。

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
<!-- ### Input Descriptions -->
### Input Descriptions

<!-- You may assign descriptions to input arguments and options by separating the argument name from the description using a colon. If you need a little extra room to define your command, feel free to spread the definition across multiple lines: -->
コロンを使用して引数名と説明を区切ることにより、入力引数とオプションに説明を割り当てることができます。コマンドを定義するのに少し余裕が必要な場合は、自由に定義を複数行に分けて記述してください。

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : The ID of the user}
                        {--queue : Whether the job should be queued}';
```

<a name="prompting-for-missing-input"></a>
<!-- ### Prompting for Missing Input -->
### Prompting for Missing Input

<!-- If your command contains required arguments, the user will receive an error message when they are not provided. Alternatively, you may configure your command to automatically prompt the user when required arguments are missing by implementing the `PromptsForMissingInput` interface: -->
コマンドに必須の引数が含まれている場合、それらが指定されていないと、ユーザーはエラー メッセージを受け取ります。あるいは、`PromptsForMissingInput` インターフェイスを実装することで、必要な引数が欠落している場合にユーザーに自動的にプロンプ​​トを表示するようにコマンドを構成することもできます。

```php
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
```

<!-- If Laravel needs to gather a required argument from the user, it will automatically ask the user for the argument by intelligently phrasing the question using either the argument name or description. If you wish to customize the question used to gather the required argument, you may implement the `promptForMissingArgumentsUsing` method, returning an array of questions keyed by the argument names: -->
Laravel がユーザーから必要な引数を収集する必要がある場合、引数の名前または説明を使用して質問をインテリジェントに表現することで、自動的にユーザーに引数を求めます。必要な引数を収集するために使用される質問をカスタマイズしたい場合は、引数名をキーとする質問の配列を返す `promptForMissingArgumentsUsing` メソッドを実装できます。

```php
/**
 * Prompt for missing input arguments using the returned questions.
 *
 * @return array<string, string>
 */
protected function promptForMissingArgumentsUsing(): array
{
    return [
        'user' => 'Which user ID should receive the mail?',
    ];
}
```

<!-- You may also provide placeholder text by using a tuple containing the question and placeholder: -->
質問とプレースホルダーを含むタプルを使用して、プレースホルダー テキストを提供することもできます。

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

<!-- If you would like complete control over the prompt, you may provide a closure that should prompt the user and return their answer: -->
プロンプトを完全に制御したい場合は、ユーザーにプロンプ​​トを表示し、その回答を返すクロージャーを提供できます。

```php
use App\Models\User;
use function Laravel\Prompts\search;

// ...

return [
    'user' => fn () => search(
        label: 'Search for a user:',
        placeholder: 'E.g. Taylor Otwell',
        options: fn ($value) => strlen($value) > 0
            ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
            : []
    ),
];
```

> [!NOTE]
<!-- The comprehensive [Laravel Prompts](/docs/13.x/prompts) documentation includes additional information on the available prompts and their usage. -->
包括的な [Laravel Prompts](/docs/13.x/prompts) ドキュメントには、使用可能なプロンプトとその使用法に関する追加情報が含まれています。

<!-- If you wish to prompt the user to select or enter [options](#options), you may include prompts in your command's `handle` method. However, if you only wish to prompt the user when they have also been automatically prompted for missing arguments, then you may implement the `afterPromptingForMissingArguments` method: -->
ユーザーに [options](#options) の選択または入力を求めるプロンプトを表示したい場合は、コマンドの `handle` メソッドにプロンプ​​トを含めることができます。ただし、不足している引数についても自動的にプロンプ​​トが表示された場合にのみユーザーにプロンプ​​トを表示したい場合は、`afterPromptingForMissingArguments` メソッドを実装できます。

```php
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use function Laravel\Prompts\confirm;

// ...

/**
 * Perform actions after the user was prompted for missing arguments.
 */
protected function afterPromptingForMissingArguments(InputInterface $input, OutputInterface $output): void
{
    $input->setOption('queue', confirm(
        label: 'Would you like to queue the mail?',
        default: $this->option('queue')
    ));
}
```

<a name="command-io"></a>
<!-- ## Command I/O -->
## Command I/O

<a name="retrieving-input"></a>
<!-- ### Retrieving Input -->
### Retrieving Input

<!-- While your command is executing, you will likely need to access the values for the arguments and options accepted by your command. To do so, you may use the `argument` and `option` methods. If an argument or option does not exist, `null` will be returned: -->
コマンドの実行中に、コマンドで受け入れられる引数とオプションの値にアクセスする必要がある場合があります。これを行うには、`argument` メソッドと `option` メソッドを使用できます。引数またはオプションが存在しない場合は、`null` が返されます。

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

<!-- If you need to retrieve all of the arguments as an `array`, call the `arguments` method: -->
すべての引数を `array` として取得する必要がある場合は、`arguments` メソッドを呼び出します。

```php
$arguments = $this->arguments();
```

<!-- Options may be retrieved just as easily as arguments using the `option` method. To retrieve all of the options as an array, call the `options` method: -->
オプションは、`option` メソッドを使用して引数と同じくらい簡単に取得できます。すべてのオプションを配列として取得するには、`options` メソッドを呼び出します。

```php
// Retrieve a specific option...
$queueName = $this->option('queue');

// Retrieve all options as an array...
$options = $this->options();
```

<a name="prompting-for-input"></a>
<!-- ### Prompting for Input -->
### Prompting for Input

> [!NOTE]
> [Laravel Prompts](/docs/13.x/prompts) は、プレースホルダー テキストや検証などのブラウザーのような機能を備えた、美しくユーザーフレンドリーなフォームをコマンドライン アプリケーションに追加するための PHP パッケージです。

<!-- In addition to displaying output, you may also ask the user to provide input during the execution of your command. The `ask` method will prompt the user with the given question, accept their input, and then return the user's input back to your command: -->
出力を表示するだけでなく、コマンドの実行中にユーザーに入力を求めることもできます。 `ask` メソッドは、ユーザーに指定された質問を表示し、入力を受け入れて、ユーザーの入力をコマンドに返します。

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $name = $this->ask('What is your name?');

    // ...
}
```

<!-- The `ask` method also accepts an optional second argument which specifies the default value that should be returned if no user input is provided: -->
`ask` メソッドは、ユーザー入力が提供されない場合に返されるデフォルト値を指定するオプションの 2 番目の引数も受け入れます。

```php
$name = $this->ask('What is your name?', 'Taylor');
```

<!-- The `secret` method is similar to `ask`, but the user's input will not be visible to them as they type in the console. This method is useful when asking for sensitive information such as passwords: -->
`secret` メソッドは `ask` に似ていますが、ユーザーの入力はコンソールに入力するときに表示されません。この方法は、パスワードなどの機密情報を要求する場合に役立ちます。

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
<!-- #### Asking for Confirmation -->
#### Asking for Confirmation

<!-- If you need to ask the user for a simple "yes or no" confirmation, you may use the `confirm` method. By default, this method will return `false`. However, if the user enters `y` or `yes` in response to the prompt, the method will return `true`. -->
ユーザーに簡単な「はいまたはいいえ」の確認を求める必要がある場合は、`confirm` メソッドを使用できます。デフォルトでは、このメソッドは `false` を返します。ただし、ユーザーがプロンプトに応じて `y` または `yes` を入力すると、メソッドは `true` を返します。

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

<!-- If necessary, you may specify that the confirmation prompt should return `true` by default by passing `true` as the second argument to the `confirm` method: -->
必要に応じて、`true` を `confirm` メソッドの 2 番目の引数として渡すことで、確認プロンプトがデフォルトで `true` を返すように指定できます。

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
<!-- #### Auto-Completion -->
#### Auto-Completion

<!-- The `anticipate` method can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints: -->
`anticipate` メソッドを使用すると、可能な選択肢のオートコンプリートを提供できます。ユーザーは、オートコンプリートのヒントに関係なく、任意の回答を入力できます。

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

<!-- Alternatively, you may pass a closure as the second argument to the `anticipate` method. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far, and return an array of options for auto-completion: -->
あるいは、`anticipate` メソッドの 2 番目の引数としてクロージャーを渡すこともできます。クロージャは、ユーザーが入力文字を入力するたびに呼び出されます。クロージャは、これまでのユーザーの入力を含む文字列パラメータを受け入れ、オートコンプリートのオプションの配列を返す必要があります。

```php
use App\Models\Address;

$name = $this->anticipate('What is your address?', function (string $input) {
    return Address::whereLike('name', "{$input}%")
        ->limit(5)
        ->pluck('name')
        ->all();
});
```

<a name="multiple-choice-questions"></a>
<!-- #### Multiple Choice Questions -->
#### Multiple Choice Questions

<!-- If you need to give the user a predefined set of choices when asking a question, you may use the `choice` method. You may set the array index of the default value to be returned if no option is chosen by passing the index as the third argument to the method: -->
質問するときにユーザーに事前定義された一連の選択肢を提供する必要がある場合は、`choice` メソッドを使用できます。オプションが選択されていない場合に、メソッドの 3 番目の引数としてインデックスを渡すことにより、デフォルト値の配列インデックスが返されるように設定できます。

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

<!-- In addition, the `choice` method accepts optional fourth and fifth arguments for determining the maximum number of attempts to select a valid response and whether multiple selections are permitted: -->
さらに、`choice` メソッドは、有効な応答を選択する最大試行回数と複数の選択が許可されるかどうかを決定するためのオプションの 4 番目と 5 番目の引数を受け入れます。

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex,
    $maxAttempts = null,
    $allowMultipleSelections = false
);
```

<a name="writing-output"></a>
<!-- ### Writing Output -->
### Writing Output

<!-- To send output to the console, you may use the `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert`, and `error` methods. Each of these methods will use appropriate ANSI colors for their purpose. For example, let's display some general information to the user. Typically, the `info` method will display in the console as green colored text: -->
出力をコンソールに送信するには、`line`、`newLine`、`info`、`comment`、`question`、`warn`、`alert`、および `error` メソッドを使用できます。これらの各メソッドは、目的に応じて適切な ANSI カラーを使用します。たとえば、一般的な情報をユーザーに表示してみましょう。通常、`info` メソッドはコンソールに緑色のテキストとして表示されます。

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    // ...

    $this->info('The command was successful!');
}
```

<!-- To display an error message, use the `error` method. Error message text is typically displayed in red: -->
エラー メッセージを表示するには、`error` メソッドを使用します。通常、エラー メッセージ テキストは赤色で表示されます。

```php
$this->error('Something went wrong!');
```

<!-- You may use the `line` method to display plain, uncolored text: -->
`line` メソッドを使用して、色の付いていないプレーン テキストを表示できます。

```php
$this->line('Display this on the screen');
```

<!-- You may use the `newLine` method to display a blank line: -->
`newLine` メソッドを使用して空行を表示できます。

```php
// Write a single blank line...
$this->newLine();

// Write three blank lines...
$this->newLine(3);
```

<a name="tables"></a>
<!-- #### Tables -->
#### Tables

<!-- The `table` method makes it easy to correctly format multiple rows / columns of data. All you need to do is provide the column names and the data for the table and Laravel will automatically calculate the appropriate width and height of the table for you: -->
`table` メソッドを使用すると、複数の行/列のデータを簡単に正しくフォーマットできます。テーブルの列名とデータを指定するだけで、Laravel がテーブルの適切な幅と高さを自動的に計算します。

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
<!-- #### Progress Bars -->
#### Progress Bars

<!-- For long running tasks, it can be helpful to show a progress bar that informs users how complete the task is. Using the `withProgressBar` method, Laravel will display a progress bar and advance its progress for each iteration over a given iterable value: -->
長時間実行されるタスクの場合は、タスクの完了度をユーザーに知らせる進行状況バーを表示すると便利です。 `withProgressBar` メソッドを使用すると、Laravel は進行状況バーを表示し、指定された反復可能な値を超えて反復ごとに進行状況を進めます。

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

<!-- Sometimes, you may need more manual control over how a progress bar is advanced. First, define the total number of steps the process will iterate through. Then, advance the progress bar after processing each item: -->
場合によっては、進行状況バーの進み方を手動で制御する必要がある場合があります。まず、プロセスが反復処理される合計ステップ数を定義します。次に、各項目を処理した後、進行状況バーを進めます。

```php
$users = App\Models\User::all();

$bar = $this->output->createProgressBar(count($users));

$bar->start();

foreach ($users as $user) {
    $this->performTask($user);

    $bar->advance();
}

$bar->finish();
```

> [!NOTE]
> より高度なオプションについては、[Symfony Progress Bar component documentation](https://symfony.com/doc/current/components/console/helpers/progressbar.html) を確認してください。

<a name="registering-commands"></a>
<!-- ## Registering Commands -->
## Registering Commands

<!-- By default, Laravel automatically registers all commands within the `app/Console/Commands` directory. However, you can instruct Laravel to scan other directories for Artisan commands using the `withCommands` method in your application's `bootstrap/app.php` file: -->
デフォルトでは、Laravel はすべてのコマンドを `app/Console/Commands` ディレクトリ内に自動的に登録します。ただし、アプリケーションの `bootstrap/app.php` ファイル内の `withCommands` メソッドを使用して、他のディレクトリで Artisan コマンドをスキャンするように Laravel に指示することができます。

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

<!-- If necessary, you may also manually register commands by providing the command's class name to the `withCommands` method: -->
必要に応じて、コマンドのクラス名を `withCommands` メソッドに指定して、コマンドを手動で登録することもできます。

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

<!-- When Artisan boots, all the commands in your application will be resolved by the [service container](/docs/13.x/container) and registered with Artisan. -->
Artisan が起動すると、アプリケーション内のすべてのコマンドが [service container](/docs/13.x/container) によって解決され、Artisan に登録されます。

<a name="programmatically-executing-commands"></a>
<!-- ## Programmatically Executing Commands -->
## Programmatically Executing Commands

<!-- Sometimes you may wish to execute an Artisan command outside of the CLI. For example, you may wish to execute an Artisan command from a route or controller. You may use the `call` method on the `Artisan` facade to accomplish this. The `call` method accepts either the command's signature name or class name as its first argument, and an array of command parameters as the second argument. The exit code will be returned: -->
場合によっては、CLI の外部で Artisan コマンドを実行したい場合があります。たとえば、ルートまたはコントローラからArtisan コマンドを実行したい場合があります。これを実現するには、`Artisan` ファサードで `call` メソッドを使用できます。 `call` メソッドは、コマンドのシグネチャ名またはクラス名のいずれかを最初の引数として受け入れ、コマンド パラメーターの配列を 2 番目の引数として受け入れます。終了コードが返されます。

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

<!-- Alternatively, you may pass the entire Artisan command to the `call` method as a string: -->
あるいは、Artisan コマンド全体を文字列として `call` メソッドに渡すこともできます。

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
<!-- #### Passing Array Values -->
#### Passing Array Values

<!-- If your command defines an option that accepts an array, you may pass an array of values to that option: -->
コマンドが配列を受け入れるオプションを定義している場合は、そのオプションに値の配列を渡すことができます。

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```

<a name="passing-boolean-values"></a>
<!-- #### Passing Boolean Values -->
#### Passing Boolean Values

<!-- If you need to specify the value of an option that does not accept string values, such as the `--force` flag on the `migrate:refresh` command, you should pass `true` or `false` as the value of the option: -->
文字列値を受け入れないオプションの値 (`migrate:refresh` コマンドの `--force` フラグなど) を指定する必要がある場合は、オプションの値として `true` または `false` を渡す必要があります。

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
<!-- #### Queueing Artisan Commands -->
#### Queueing Artisan Commands

<!-- Using the `queue` method on the `Artisan` facade, you may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/13.x/queues). Before using this method, make sure you have configured your queue and are running a queue listener: -->
`Artisan` ファサードで `queue` メソッドを使用すると、Artisan コマンドをキューに入れて、[queue workers](/docs/13.x/queues) によってバックグラウンドで処理されるようにすることもできます。この方法を使用する前に、キューを設定し、キュー リスナを実行していることを確認してください。

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

<!-- Using the `onConnection` and `onQueue` methods, you may specify the connection or queue the Artisan command should be dispatched to: -->
`onConnection` メソッドと `onQueue` メソッドを使用すると、Artisan コマンドをディスパッチする接続またはキューを指定できます。

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
<!-- ### Calling Commands From Other Commands -->
### Calling Commands From Other Commands

<!-- Sometimes you may wish to call other commands from an existing Artisan command. You may do so using the `call` method. This `call` method accepts the command name and an array of command arguments / options: -->
場合によっては、既存の Artisan コマンドから他のコマンドを呼び出したい場合があります。これは、`call` メソッドを使用して行うことができます。この `call` メソッドは、コマンド名とコマンド引数/オプションの配列を受け入れます。

```php
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
```

<!-- If you would like to call another console command and suppress all of its output, you may use the `callSilently` method. The `callSilently` method has the same signature as the `call` method: -->
別のコンソール コマンドを呼び出してその出力をすべて抑制したい場合は、`callSilently` メソッドを使用できます。 `callSilently` メソッドには、`call` メソッドと同じシグネチャがあります。

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
<!-- ## Signal Handling -->
## Signal Handling

<!-- As you may know, operating systems allow signals to be sent to running processes. For example, the `SIGTERM` signal is how operating systems ask a program to terminate gracefully. If you wish to listen for signals in your Artisan console commands and execute code when they occur, you may use the `trap` method: -->
ご存知かもしれませんが、オペレーティング システムでは、実行中のプロセスにシグナルを送信できます。たとえば、`SIGTERM` 信号は、オペレーティング システムがプログラムに正常に終了するように要求する方法です。 Artisan コンソール コマンドでシグナルをリッスンし、シグナルが発生したときにコードを実行したい場合は、`trap` メソッドを使用できます。

```php
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
```

<!-- To listen for multiple signals at once, you may provide an array of signals to the `trap` method: -->
一度に複数の信号をリッスンするには、信号の配列を `trap` メソッドに提供します。

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
<!-- ## Stub Customization -->
## Stub Customization

<!-- The Artisan console's `make` commands are used to create a variety of classes, such as controllers, jobs, migrations, and tests. These classes are generated using "stub" files that are populated with values based on your input. However, you may want to make small changes to files generated by Artisan. To accomplish this, you may use the `stub:publish` command to publish the most common stubs to your application so that you can customize them: -->
Artisan コンソールの `make` コマンドは、コントローラ、ジョブ、移行、テストなどのさまざまなクラスを作成するために使用されます。これらのクラスは、入力に基づいて値が設定される「スタブ」ファイルを使用して生成されます。ただし、Artisan によって生成されたファイルに小さな変更を加えたい場合があります。これを実現するには、`stub:publish` コマンドを使用して最も一般的なスタブをアプリケーションに公開し、カスタマイズできるようにします。

```shell
php artisan stub:publish
```

<!-- The published stubs will be located within a `stubs` directory in the root of your application. Any changes you make to these stubs will be reflected when you generate their corresponding classes using Artisan's `make` commands. -->
公開されたスタブは、アプリケーションのルートの `stubs` ディレクトリ内に配置されます。これらのスタブに加えた変更は、Artisan の `make` コマンドを使用して対応するクラスを生成するときに反映されます。

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Artisan dispatches three events when running commands: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, and `Illuminate\Console\Events\CommandFinished`. The `ArtisanStarting` event is dispatched immediately when Artisan starts running. Next, the `CommandStarting` event is dispatched immediately before a command runs. Finally, the `CommandFinished` event is dispatched once a command finishes executing. -->
Artisan は、コマンドの実行時に `Illuminate\Console\Events\ArtisanStarting`、`Illuminate\Console\Events\CommandStarting`、および `Illuminate\Console\Events\CommandFinished` の 3 つのイベントを送出します。 `ArtisanStarting` イベントは、Artisan の実行が開始されるとすぐに送出されます。次に、コマンドが実行される直前に、`CommandStarting` イベントが送出されます。最後に、コマンドの実行が終了すると、`CommandFinished` イベントが送出されます。

