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
Artisan은 Laravel에 기본 포함된 command line interface(CLI)입니다. Artisan은 애플리케이션 루트에 있는 `artisan` 스크립트로 제공되며, 애플리케이션을 구축하는 동안 도움이 되는 다양한 명령어를 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 확인하려면 `list` 명령어를 사용하면 됩니다:

```shell
php artisan list
```

<!-- Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, precede the name of the command with `help`: -->
각 명령어에는 도움말 화면이 포함되어 있으며, 명령어에서 사용할 수 있는 인수 및 옵션을 표시하고 설명합니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙여 실행하세요.

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
<!-- #### Laravel Sail -->
#### Laravel Sail

<!-- If you are using [Laravel Sail](/docs/12.x/sail) as your local development environment, remember to use the `sail` command line to invoke Artisan commands. Sail will execute your Artisan commands within your application's Docker containers: -->
[Laravel Sail](/docs/12.x/sail)을 로컬 개발 환경으로 사용하는 경우 Artisan 명령어를 실행할 때 `sail` 명령을 사용해야 합니다. Sail은 애플리케이션의 Docker 컨테이너 안에서 Artisan 명령어를 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
<!-- ### Tinker (REPL) -->
### Tinker (REPL)

<!-- [Laravel Tinker](https://github.com/laravel/tinker) is a powerful REPL for the Laravel framework, powered by the [PsySH](https://github.com/bobthecow/psysh) package. -->
[Laravel Tinker](https://github.com/laravel/tinker)는 Laravel 프레임워크용 강력한 REPL(Read–Eval–Print Loop)로, [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 합니다.

<a name="installation"></a>
<!-- #### Installation -->
#### Installation

<!-- All Laravel applications include Tinker by default. However, you may install Tinker using Composer if you have previously removed it from your application: -->
모든 Laravel 애플리케이션에는 Tinker가 기본으로 포함되어 있습니다. 하지만 애플리케이션에서 Tinker를 삭제한 경우에는 Composer로 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션과 상호작용할 때 **핫 리로딩**, 멀티라인 코드 에디팅, 자동완성 등 편리한 기능이 필요하다면 [Tinkerwell](https://tinkerwell.app)을 참고해 보세요!

<a name="usage"></a>
<!-- #### Usage -->
#### Usage

<!-- Tinker allows you to interact with your entire Laravel application on the command line, including your Eloquent models, jobs, events, and more. To enter the Tinker environment, run the `tinker` Artisan command: -->
Tinker를 사용하면 Eloquent 모델, job, 이벤트 등 애플리케이션 전체와 명령줄에서 상호작용할 수 있습니다. Tinker 환경에 들어가려면 `tinker` Artisan 명령어를 실행하세요.

```shell
php artisan tinker
```

<!-- You can publish Tinker's configuration file using the `vendor:publish` command: -->
`vendor:publish` 명령어를 통해 Tinker의 설정 파일을 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 잡을 큐에 넣기 위해 가비지 컬렉션에 의존합니다. 따라서 Tinker에서 잡을 디스패치할 때는 `Bus::dispatch`나 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
<!-- #### Command Allow List -->
#### Command Allow List

<!-- Tinker utilizes an "allow" list to determine which Artisan commands are allowed to be run within its shell. By default, you may run the `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, and `optimize` commands. If you would like to allow more commands you may add them to the `commands` array in your `tinker.php` configuration file: -->
Tinker는 쉘 내에서 실행할 수 있는 Artisan 명령어를 "허용 목록"을 통해 제한합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어만 실행할 수 있습니다. 더 많은 명령어를 허용하려면 `tinker.php` 설정 파일의 `commands` 배열에 추가하세요.

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
<!-- #### Classes That Should Not Be Aliased -->
#### Classes That Should Not Be Aliased

<!-- Typically, Tinker automatically aliases classes as you interact with them in Tinker. However, you may wish to never alias some classes. You may accomplish this by listing the classes in the `dont_alias` array of your `tinker.php` configuration file: -->
일반적으로 Tinker는 상호작용하는 클래스를 자동으로 별칭 처리(alias)합니다. 하지만 특정 클래스는 절대로 별칭 처리하지 않도록 제한할 수도 있습니다. `tinker.php` 설정 파일의 `dont_alias` 배열에 클래스를 추가하면 됩니다:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
<!-- ## Writing Commands -->
## Writing Commands

<!-- In addition to the commands provided with Artisan, you may build your own custom commands. Commands are typically stored in the `app/Console/Commands` directory; however, you are free to choose your own storage location as long as you instruct Laravel to [scan other directories for Artisan commands](#registering-commands). -->
Artisan이 기본 제공하는 명령어 외에도 직접 사용자 지정 명령어를 만들 수 있습니다. 명령어 클래스는 보통 `app/Console/Commands` 디렉터리에 저장하지만, [scan other directories for Artisan commands](#registering-commands)하도록 지정하면 자유롭게 경로를 정할 수 있습니다.

<a name="generating-commands"></a>
<!-- ### Generating Commands -->
### Generating Commands

<!-- To create a new command, you may use the `make:command` Artisan command. This command will create a new command class in the `app/Console/Commands` directory. Don't worry if this directory does not exist in your application - it will be created the first time you run the `make:command` Artisan command: -->
새로운 명령어를 생성하려면 `make:command` Artisan 명령어를 사용하세요. 이 명령어는 `app/Console/Commands` 디렉터리 아래에 새로운 명령어 클래스를 만듭니다. 애플리케이션에 이 디렉터리가 없더라도 걱정하지 마세요. `make:command` Artisan 명령어를 처음 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
<!-- ### Command Structure -->
### Command Structure

<!-- After generating your command, you should define appropriate values for the `signature` and `description` properties of the class. These properties will be used when displaying your command on the `list` screen. The `signature` property also allows you to define [your command's input expectations](#defining-input-expectations). The `handle` method will be called when your command is executed. You may place your command logic in this method. -->
명령어를 생성한 후에는, 클래스의 `signature`와 `description` 속성에 알맞은 값을 지정해야 합니다. 이 속성들은 `list` 명령어로 명령어 목록을 표시할 때 사용됩니다. 또한 `signature` 속성을 통해 [your command's input expectations](#defining-input-expectations)도 정의할 수 있습니다. 명령어가 실행되면 `handle` 메서드가 호출되며, 명령어 로직은 이 메서드에 작성합니다.

<!-- Let's take a look at an example command. Note that we are able to request any dependencies we need via the command's `handle` method. The Laravel [service container](/docs/12.x/container) will automatically inject all dependencies that are type-hinted in this method's signature: -->
다음은 명령어 예시입니다. `handle` 메서드에서 필요한 의존성을 요청할 수 있다는 점에 주목하세요. Laravel의 [service container](/docs/12.x/container)는 명시적으로 타입힌트된 모든 의존성을 자동으로 주입합니다:

```php
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
```

> [!NOTE]
> 코드 재사용성을 높이기 위해, 콘솔 명령어는 최대한 간결하게 작성하고 애플리케이션 서비스에 실제 작업을 위임하는 것이 좋습니다. 위 예제에서 이메일 전송의 “실제 작업”을 서비스 클래스에 맡긴 모습을 볼 수 있습니다.

<a name="exit-codes"></a>
<!-- #### Exit Codes -->
#### Exit Codes

<!-- If nothing is returned from the `handle` method and the command executes successfully, the command will exit with a `0` exit code, indicating success. However, the `handle` method may optionally return an integer to manually specify the command's exit code: -->
`handle` 메서드에서 아무것도 반환하지 않고 정상적으로 명령어가 실행된 경우, 명령어는 `0` 종료 코드(성공)를 반환합니다. 하지만 필요하다면 `handle` 메서드에서 직접 정수형 반환값을 지정해 종료 코드를 컨트롤할 수 있습니다:

```php
$this->error('Something went wrong.');

return 1;
```

<!-- If you would like to "fail" the command from any method within the command, you may utilize the `fail` method. The `fail` method will immediately terminate execution of the command and return an exit code of `1`: -->
명령어 내 모든 메서드에서 명시적으로 실패 처리하려면 `fail` 메서드를 사용할 수 있습니다. `fail` 메서드는 즉시 명령어의 실행을 중단하고 종료 코드 `1`을 반환합니다:

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
<!-- ### Closure Commands -->
### Closure Commands

<!-- Closure-based commands provide an alternative to defining console commands as classes. In the same way that route closures are an alternative to controllers, think of command closures as an alternative to command classes. -->
클로저(익명 함수) 기반 명령어는 명령어 클래스를 정의하는 대신 사용할 수 있는 대체 방식입니다. 라우트 클로저가 컨트롤러의 대체 용도인 것과 유사하게, 클로저 명령어도 명령어 클래스의 대안입니다.

<!-- Even though the `routes/console.php` file does not define HTTP routes, it defines console-based entry points (routes) into your application. Within this file, you may define all of your closure-based console commands using the `Artisan::command` method. The `command` method accepts two arguments: the [command signature](#defining-input-expectations) and a closure which receives the command's arguments and options: -->
`routes/console.php` 파일은 HTTP 라우트가 아닌, 콘솔을 통한 애플리케이션 진입점(라우트)을 정의합니다. 이 파일에서 `Artisan::command` 메서드를 사용해 모든 클로저 기반 콘솔 명령어를 정의할 수 있습니다. `command` 메서드는 [command signature](#defining-input-expectations)와 명령어 인수 및 옵션을 받는 클로저를 인자로 받습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

<!-- The closure is bound to the underlying command instance, so you have full access to all of the helper methods you would typically be able to access on a full command class. -->
클로저는 내부적으로 명령어 인스턴스에 바인딩되기 때문에, 명령어 클래스에서 사용 가능한 모든 헬퍼 메서드를 그대로 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
<!-- #### Type-Hinting Dependencies -->
#### Type-Hinting Dependencies

<!-- In addition to receiving your command's arguments and options, command closures may also type-hint additional dependencies that you would like resolved out of the [service container](/docs/12.x/container): -->
클로저 명령어에서도 명령어 인수 및 옵션 외에 추가적인 의존성을 [service container](/docs/12.x/container)에서 타입힌트 방식으로 주입받을 수 있습니다:

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
클로저 기반 명령어 정의 시 `purpose` 메서드를 사용해 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help`로 확인할 수 있습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
<!-- ### Isolatable Commands -->
### Isolatable Commands

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 사용해야 하며, 모든 서버가 같은 중앙 캐시 서버와 통신해야 합니다.

<!-- Sometimes you may wish to ensure that only one instance of a command can run at a time. To accomplish this, you may implement the `Illuminate\Contracts\Console\Isolatable` interface on your command class: -->
하나의 명령어 인스턴스만 동시 실행되도록 보장하고 싶을 때가 있습니다. 이 경우 명령어 클래스에서 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하세요:

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
명령어를 `Isolatable`로 표시하면 해당 명령어의 옵션에 `--isolated`가 자동으로 추가되며, 이 옵션을 명시적으로 선언할 필요가 없습니다. 해당 옵션으로 명령어를 실행하면, Laravel은 해당 명령어가 이미 실행 중인지 확인하여, 실행 중이 아니라면 원자적(atomic) 락을 기본 캐시 드라이버를 통해 획득합니다. 이미 다른 인스턴스가 실행 중이면 명령어는 실행되지 않지만, 성공 상태 코드로 종료됩니다:

```shell
php artisan mail:send 1 --isolated
```

<!-- If you would like to specify the exit status code that the command should return if it is not able to execute, you may provide the desired status code via the `isolated` option: -->
명령어 실행 불가 시 반환할 상태 코드를 지정하고자 한다면 `isolated` 옵션에 원하는 코드를 전달하세요:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
<!-- #### Lock ID -->
#### Lock ID

<!-- By default, Laravel will use the command's name to generate the string key that is used to acquire the atomic lock in your application's cache. However, you may customize this key by defining an `isolatableId` method on your Artisan command class, allowing you to integrate the command's arguments or options into the key: -->
기본적으로 Laravel은 명령어 이름을 기반으로 락에 사용할 문자열 키를 생성합니다. 하지만 `isolatableId` 메서드를 명령어 클래스에 정의하면, 인수나 옵션 값을 포함하여 이 키를 사용자 지정할 수 있습니다:

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
기본적으로 isolation 락은 명령어가 종료될 때 만료되며, 만약 중단 등으로 정상 종료되지 않으면 1시간 후 만료됩니다. 락 만료 시간을 사용자 지정하려면 `isolationLockExpiresAt` 메서드를 정의하세요:

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
콘솔 명령어 작성 시에는, 사용자의 입력을 인수(argument)나 옵션(option)으로 받아야 할 때가 많습니다. Laravel은 명령어의 `signature` 속성을 통해 사용자에게 기대하는 입력을 매우 편리하게 정의할 수 있도록 지원합니다. `signature` 속성을 사용하면 명령어의 이름, 인수, 옵션을 라우트 시그니처와 유사한 하나의 표현식 문법으로 정의할 수 있습니다.

<a name="arguments"></a>
<!-- ### Arguments -->
### Arguments

<!-- All user supplied arguments and options are wrapped in curly braces. In the following example, the command defines one required argument: `user`: -->
모든 사용자 입력 인수와 옵션은 중괄호로 감싸서 정의합니다. 아래 예제에서 명령어는 필수 인수 `user`를 정의하고 있습니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

<!-- You may also make arguments optional or define default values for arguments: -->
인수를 선택적으로 만들거나 기본값을 설정할 수도 있습니다:

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
옵션도 인수와 마찬가지로 사용자 입력의 한 방식입니다. 옵션은 명령줄에서 두 개의 하이픈(`--`)으로 접두됩니다. 옵션에는 값을 받는 타입과, 값을 받지 않는 부울(boolean) “스위치” 타입 두 가지가 있습니다. 아래는 스위치 타입 옵션의 예시입니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

<!-- In this example, the `--queue` switch may be specified when calling the Artisan command. If the `--queue` switch is passed, the value of the option will be `true`. Otherwise, the value will be `false`: -->
위 예시에서는 명령어 실행 시 `--queue` 스위치를 지정할 수 있습니다. `--queue` 스위치가 전달되면 옵션 값은 `true`, 그렇지 않으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
<!-- #### Options With Values -->
#### Options With Values

<!-- Next, let's take a look at an option that expects a value. If the user must specify a value for an option, you should suffix the option name with a `=` sign: -->
다음은 값을 필요로 하는 옵션 예시입니다. 옵션 이름 뒤에 등호(`=`)를 붙여 정의하면 사용자가 값을 반드시 지정해야 합니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

<!-- In this example, the user may pass a value for the option like so. If the option is not specified when invoking the command, its value will be `null`: -->
이 경우 명령어 실행 시 다음과 같이 값을 전달해야 하며, 옵션이 생략되면 값은 `null`이 됩니다:

```shell
php artisan mail:send 1 --queue=default
```

<!-- You may assign default values to options by specifying the default value after the option name. If no option value is passed by the user, the default value will be used: -->
옵션에 기본값을 지정하려면 옵션 이름 뒤에 기본값을 추가하세요. 사용자가 값을 전달하지 않으면 이 값이 적용됩니다:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
<!-- #### Option Shortcuts -->
#### Option Shortcuts

<!-- To assign a shortcut when defining an option, you may specify it before the option name and use the `|` character as a delimiter to separate the shortcut from the full option name: -->
옵션 정의 시, `|` 구분자를 이용해 전체 옵션 이름 앞에 단축키(한 글자)를 지정할 수 있습니다:

```php
'mail:send {user} {--Q|queue=}'
```

<!-- When invoking the command on your terminal, option shortcuts should be prefixed with a single hyphen and no `=` character should be included when specifying a value for the option: -->
터미널에서 옵션 단축키를 사용할 때는 하이픈 하나만 붙이고, 값에는 `=` 없이 바로 이어서 씁니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
<!-- ### Input Arrays -->
### Input Arrays

<!-- If you would like to define arguments or options to expect multiple input values, you may use the `*` character. First, let's take a look at an example that specifies such an argument: -->
인수나 옵션이 복수의 입력값을 받기를 원한다면, `*` 문자를 이용하세요. 아래는 인수에 대해 배열 형태로 입력을 받을 때 예시입니다:

```php
'mail:send {user*}'
```

<!-- When running this command, the `user` arguments may be passed in order to the command line. For example, the following command will set the value of `user` to an array with `1` and `2` as its values: -->
이 경우, 명령어 실행 시 `user` 인수를 명령줄에 순서대로 전달할 수 있습니다. 예를 들어 다음 명령어는 `user` 값을 `1`과 `2`를 원소로 가지는 배열로 설정합니다:

```shell
php artisan mail:send 1 2
```

<!-- This `*` character can be combined with an optional argument definition to allow zero or more instances of an argument: -->
`*` 문자를 선택적 인수와 함께 사용하면, 인수의 개수를 0개 이상으로 허용할 수 있습니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
<!-- #### Option Arrays -->
#### Option Arrays

<!-- When defining an option that expects multiple input values, each option value passed to the command should be prefixed with the option name: -->
복수의 값을 받는 옵션 역시, 전달할 옵션 이름마다 개별적으로 값을 붙여서 여러 번 전달하면 됩니다:

```php
'mail:send {--id=*}'
```

<!-- Such a command may be invoked by passing multiple `--id` arguments: -->
이러한 명령어는 여러 개의 `--id` 인수를 전달하여 호출할 수 있습니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
<!-- ### Input Descriptions -->
### Input Descriptions

<!-- You may assign descriptions to input arguments and options by separating the argument name from the description using a colon. If you need a little extra room to define your command, feel free to spread the definition across multiple lines: -->
입력 인수나 옵션에 설명을 추가할 때는 인수/옵션 이름과 설명을 콜론으로 구분하면 됩니다. 명령어 정의가 길어질 경우, 여러 줄로 나누어 작성해도 무방합니다:

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
명령어에 필수 인수가 있을 때 사용자가 입력하지 않으면, 일반적으로 에러 메시지가 표시됩니다. 그러나 명령어에서 `PromptsForMissingInput` 인터페이스를 구현하면, 누락된 필수 인수에 대해 자동으로 프롬프트가 표시되어 사용자의 입력을 유도할 수 있습니다:

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
Laravel이 필수 인수를 직접 받아야 할 때, 인수 이름이나 설명에 기반하여 자동으로 질문을 생성해 사용자의 입력을 요청합니다. 질문을 사용자 지정하고 싶다면 `promptForMissingArgumentsUsing` 메서드를 구현하여, 인수 이름을 키로 가지는 질문 문자열의 배열을 반환하세요:

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
질문과 함께 플레이스홀더도 제공하려면, 질문 – 플레이스홀더를 튜플 형태(배열)로 지정할 수 있습니다:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

<!-- If you would like complete control over the prompt, you may provide a closure that should prompt the user and return their answer: -->
프롬프트 동작 전체를 완전히 제어하고 싶다면 사용자를 프롬프트하고 값을 반환하는 클로저를 사용할 수 있습니다:

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
> <!-- The comprehensive [Laravel Prompts](/docs/12.x/prompts) documentation includes additional information on the available prompts and their usage. -->
> [Laravel Prompts](/docs/12.x/prompts) 공식 문서에서 사용 가능한 프롬프트 유형들과 더 많은 옵션을 확인할 수 있습니다.

<!-- If you wish to prompt the user to select or enter [options](#options), you may include prompts in your command's `handle` method. However, if you only wish to prompt the user when they have also been automatically prompted for missing arguments, then you may implement the `afterPromptingForMissingArguments` method: -->
[options](#options)을 선택 또는 입력받는 프롬프트를 제공하려면 명령어의 `handle` 메서드 안에서 직접 프롬프트 코드를 작성하면 됩니다. 하지만, 누락된 인수 자동 프롬프트가 끝난 직후에만 별도 프롬프트를 띄우고 싶다면 `afterPromptingForMissingArguments` 메서드를 구현할 수 있습니다:

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
명령어 실행 중에는 정의한 인수와 옵션의 값을 얻어야 할 필요가 있습니다. 이때는 `argument`와 `option` 메서드를 사용하세요. 해당 인수 또는 옵션이 없으면 `null`을 반환합니다:

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
모든 인수를 `array`로 한 번에 얻으려면 `arguments` 메서드를 호출하세요:

```php
$arguments = $this->arguments();
```

<!-- Options may be retrieved just as easily as arguments using the `option` method. To retrieve all of the options as an array, call the `options` method: -->
옵션도 마찬가지로 단일 옵션 값을 `option`으로, 전체 옵션을 배열로는 `options` 메서드로 얻을 수 있습니다:

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
> [Laravel Prompts](/docs/12.x/prompts)는 커맨드라인 애플리케이션에서 플레이스홀더, 유효성검사 등 브라우저와 유사한 사용자 경험을 제공하는 아름답고 사용하기 쉬운 폼 생성을 도와주는 PHP 패키지입니다.

<!-- In addition to displaying output, you may also ask the user to provide input during the execution of your command. The `ask` method will prompt the user with the given question, accept their input, and then return the user's input back to your command: -->
콘솔에 메시지를 출력하는 것 외에도, 실행 중인 명령어에서 사용자의 입력을 직접 요청할 수도 있습니다. `ask` 메서드는 질문을 출력, 사용자의 입력을 받아, 반환합니다:

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
`ask` 메서드는 두 번째 인수로 기본값을 받을 수 있습니다. 사용자가 입력을 생략하면 이 값이 반환됩니다:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

<!-- The `secret` method is similar to `ask`, but the user's input will not be visible to them as they type in the console. This method is useful when asking for sensitive information such as passwords: -->
`secret` 메서드는 `ask`와 비슷하지만, 사용자가 입력하는 내용이 콘솔에 표시되지 않습니다. 비밀번호와 같은 민감한 정보를 입력받을 때 유용합니다:

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
<!-- #### Asking for Confirmation -->
#### Asking for Confirmation

<!-- If you need to ask the user for a simple "yes or no" confirmation, you may use the `confirm` method. By default, this method will return `false`. However, if the user enters `y` or `yes` in response to the prompt, the method will return `true`. -->
사용자에게 "예/아니요" 식의 간단한 확인을 요청해야 하는 경우 `confirm` 메서드를 사용하세요. 이 메서드는 기본적으로 `false`를 반환하지만, 사용자가 `y` 또는 `yes`를 입력하면 `true`를 반환합니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

<!-- If necessary, you may specify that the confirmation prompt should return `true` by default by passing `true` as the second argument to the `confirm` method: -->
필요하다면 `confirm` 메서드의 두 번째 인수로 `true`를 전달하여, 확인 프롬프트가 기본적으로 `true`를 반환하도록 지정할 수 있습니다:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
<!-- #### Auto-Completion -->
#### Auto-Completion

<!-- The `anticipate` method can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints: -->
`anticipate` 메서드는 사용자가 입력 중일 때 자동완성 힌트를 제공할 수 있습니다. 사용자는 힌트와 무관하게 아무 값이나 입력할 수 있습니다:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

<!-- Alternatively, you may pass a closure as the second argument to the `anticipate` method. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far, and return an array of options for auto-completion: -->
또는 `anticipate` 메서드의 두 번째 인자로 클로저를 전달할 수도 있습니다. 이 클로저는 사용자가 문자를 입력할 때마다 호출되며, 지금까지 입력한 문자열을 매개변수로 받아 자동완성 옵션 배열을 반환해야 합니다:

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
사용자에게 미리 정해진 선택지 중에서 선택을 요청하려면 `choice` 메서드를 사용하세요. 세 번째 인수로 선택지에서 기본값으로 표시할 인덱스를 전달할 수 있습니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

<!-- In addition, the `choice` method accepts optional fourth and fifth arguments for determining the maximum number of attempts to select a valid response and whether multiple selections are permitted: -->
또한, `choice` 메서드는 최대 시도 횟수(4번째 인수), 복수 선택 허용 여부(5번째 인수)를 추가적으로 지정할 수 있습니다:

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
콘솔에 메시지를 출력하려면 `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert`, `error`와 같은 다양한 메서드를 사용할 수 있습니다. 각 메서드는 용도에 맞는 ANSI 컬러가 적용됩니다. 예를 들면, `info`는 일반적으로 초록색으로 표시되어 정보를 알릴 때 사용합니다:

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
에러 메시지는 `error` 메서드를 사용하며, 일반적으로 빨간색으로 출력됩니다:

```php
$this->error('Something went wrong!');
```

<!-- You may use the `line` method to display plain, uncolored text: -->
단순 텍스트를 컬러 없이 출력하려면 `line` 메서드를 사용합니다:

```php
$this->line('Display this on the screen');
```

<!-- You may use the `newLine` method to display a blank line: -->
공백 줄을 생성하고 싶으면 `newLine` 메서드를 사용하세요:

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
`table` 메서드를 사용하면 여러 행/열로 이루어진 데이터를 보기 좋게 테이블 형태로 출력할 수 있습니다. 컬럼 명과 데이터만 넘겨주면 적절한 크기의 테이블로 자동 정렬됩니다:

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
실행 시간이 긴 작업에서는 진행 상황을 시각적으로 보여주면 좋습니다. `withProgressBar`를 사용하면, 지정한 이터러블 값을 순회할 때마다 진행률이 자동으로 표시됩니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

<!-- Sometimes, you may need more manual control over how a progress bar is advanced. First, define the total number of steps the process will iterate through. Then, advance the progress bar after processing each item: -->
직접 진행률 바의 제어가 필요할 경우, 먼저 전체 스텝 개수를 정의하고, 각 아이템 처리 후 바를 수동으로 advance 하세요:

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
> 더 고급 기능이 필요하다면 [Symfony Progress Bar component documentation](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
<!-- ## Registering Commands -->
## Registering Commands

<!-- By default, Laravel automatically registers all commands within the `app/Console/Commands` directory. However, you can instruct Laravel to scan other directories for Artisan commands using the `withCommands` method in your application's `bootstrap/app.php` file: -->
기본적으로 Laravel은 `app/Console/Commands` 디렉터리에 있는 모든 명령어를 자동으로 등록합니다. 하지만 필요에 따라 `bootstrap/app.php` 파일의 `withCommands` 메서드를 이용해 다른 디렉터리도 스캔하도록 지정할 수 있습니다:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

<!-- If necessary, you may also manually register commands by providing the command's class name to the `withCommands` method: -->
필요하다면 명령어의 클래스명을 `withCommands` 메서드에 직접 전달하여 수동으로 등록할 수도 있습니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

<!-- When Artisan boots, all the commands in your application will be resolved by the [service container](/docs/12.x/container) and registered with Artisan. -->
Artisan이 부팅되면, 애플리케이션의 모든 명령어가 [service container](/docs/12.x/container)에서 해결(resolve)되어 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
<!-- ## Programmatically Executing Commands -->
## Programmatically Executing Commands

<!-- Sometimes you may wish to execute an Artisan command outside of the CLI. For example, you may wish to execute an Artisan command from a route or controller. You may use the `call` method on the `Artisan` facade to accomplish this. The `call` method accepts either the command's signature name or class name as its first argument, and an array of command parameters as the second argument. The exit code will be returned: -->
CLI 환경이 아닌 곳에서 Artisan 명령어를 실행하고자 할 때도 있습니다. 예를 들어 라우트나 컨트롤러 내부에서 Artisan 명령어를 호출하고 싶을 때, `Artisan` 파사드의 `call` 메서드를 사용할 수 있습니다. `call` 메서드는 첫 번째 인수로 명령어 시그니처명 또는 클래스명, 두 번째 인수로 파라미터 배열을 받으며, 반환값은 종료 코드입니다:

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
또는, 전체 Artisan 명령어를 문자열로 `call` 메서드에 전달할 수도 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
<!-- #### Passing Array Values -->
#### Passing Array Values

<!-- If your command defines an option that accepts an array, you may pass an array of values to that option: -->
명령어에서 배열을 받는 옵션이 정의되어 있다면, 배열 값을 옵션에 전달할 수 있습니다:

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
문자열 값이 필요한 옵션이 아닌, 예를 들어 `migrate:refresh` 명령어의 `--force` 플래그와 동시에 사용하고 싶다면, 옵션 값을 `true` 혹은 `false`로 전달할 수 있습니다:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
<!-- #### Queueing Artisan Commands -->
#### Queueing Artisan Commands

<!-- Using the `queue` method on the `Artisan` facade, you may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/12.x/queues). Before using this method, make sure you have configured your queue and are running a queue listener: -->
`Artisan` 파사드의 `queue` 메서드를 사용하면 Artisan 명령어를 [queue workers](/docs/12.x/queues)에서 백그라운드로 처리하게 할 수 있습니다. 사용전에 큐 환경 설정과 큐 리스너 동작을 반드시 확인하세요:

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
`onConnection`, `onQueue` 메서드를 사용하면 명령어를 보낼 연결(connection)이나 큐(queue)를 지정할 수도 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
<!-- ### Calling Commands From Other Commands -->
### Calling Commands From Other Commands

<!-- Sometimes you may wish to call other commands from an existing Artisan command. You may do so using the `call` method. This `call` method accepts the command name and an array of command arguments / options: -->
기존 Artisan 명령어에서 다른 명령어를 실행하고 싶을 때가 있습니다. 이럴 때는 `call` 메서드를 사용하세요. 이 `call` 메서드는 명령어 이름과 명령어 인수/옵션 배열을 받습니다:

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
다른 콘솔 명령어를 호출할 때 출력까지 모두 숨기고 싶다면, `callSilently` 메서드를 사용하세요. `callSilently` 메서드는 `call` 메서드와 동일한 시그니처를 가집니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
<!-- ## Signal Handling -->
## Signal Handling

<!-- As you may know, operating systems allow signals to be sent to running processes. For example, the `SIGTERM` signal is how operating systems ask a program to terminate gracefully. If you wish to listen for signals in your Artisan console commands and execute code when they occur, you may use the `trap` method: -->
운영체제는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어 `SIGTERM`은 프로그램에 정상 종료를 요청할 때 사용됩니다. Artisan 콘솔 명령어에서 이런 시그널을 감지하고 특정 코드를 실행하려면 `trap` 메서드를 사용할 수 있습니다:

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
여러 개의 시그널을 동시에 감지하려면 `trap` 메서드에 시그널 배열을 전달하면 됩니다:

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
Artisan 콘솔의 `make` 명령어들은 컨트롤러, 잡(jobs), 마이그레이션, 테스트 등 다양한 클래스를 생성하는 데 사용됩니다. 이 클래스 생성은 미리 작성된 "stub" 파일을 기반으로, 입력에 따라 값이 채워져 만들어집니다. 보다 세밀하게 Artisan에서 생성하는 파일을 조정하고 싶다면, `stub:publish` 명령어로 가장 일반적인 스텁파일을 애플리케이션으로 복사해 수정할 수 있습니다:

```shell
php artisan stub:publish
```

<!-- The published stubs will be located within a `stubs` directory in the root of your application. Any changes you make to these stubs will be reflected when you generate their corresponding classes using Artisan's `make` commands. -->
퍼블리시된 스텁은 애플리케이션 루트에 `stubs` 디렉터리로 저장됩니다. 이 파일들을 수정하면, 해당 `make` 명령어로 생성하는 클래스에 곧바로 반영됩니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Artisan dispatches three events when running commands: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, and `Illuminate\Console\Events\CommandFinished`. The `ArtisanStarting` event is dispatched immediately when Artisan starts running. Next, the `CommandStarting` event is dispatched immediately before a command runs. Finally, the `CommandFinished` event is dispatched once a command finishes executing. -->
Artisan은 명령어 실행 시 세 가지 이벤트를 디스패치합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`.
`ArtisanStarting` 이벤트는 Artisan이 시작하는 즉시 디스패치됩니다. 이어서 명령어 실행 직전에는 `CommandStarting`, 명령어 실행이 끝나면 `CommandFinished` 이벤트가 각각 디스패치됩니다.
