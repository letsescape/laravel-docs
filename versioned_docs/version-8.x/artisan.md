<!-- # Artisan Console -->
# Artisan Console

- [Introduction](#introduction)
    - [Tinker (REPL)](#tinker)
- [Writing Commands](#writing-commands)
    - [Generating Commands](#generating-commands)
    - [Command Structure](#command-structure)
    - [Closure Commands](#closure-commands)
- [Defining Input Expectations](#defining-input-expectations)
    - [Arguments](#arguments)
    - [Options](#options)
    - [Input Arrays](#input-arrays)
    - [Input Descriptions](#input-descriptions)
- [Command I/O](#command-io)
    - [Retrieving Input](#retrieving-input)
    - [Prompting For Input](#prompting-for-input)
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
아티즌(Artisan)은 Laravel에 기본 포함된 명령줄 인터페이스입니다. 아티즌은 애플리케이션 루트에 `artisan` 스크립트로 존재하며, 애플리케이션을 개발할 때 도움이 되는 여러 유용한 명령어를 제공합니다. 사용 가능한 모든 아티즌 명령어 목록을 확인하려면 `list` 명령어를 실행하십시오.

```
php artisan list
```

<!-- Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, precede the name of the command with `help`: -->
각 명령어는 해당 명령어에서 사용할 수 있는 인수와 옵션을 표시하고 설명하는 "도움말(help)" 화면도 제공합니다. 도움말 화면을 확인하려면 명령어 이름 앞에 `help`를 붙여 실행하면 됩니다.

```
php artisan help migrate
```

<a name="laravel-sail"></a>
<!-- #### Laravel Sail -->
#### Laravel Sail

<!-- If you are using [Laravel Sail](/docs/8.x/sail) as your local development environment, remember to use the `sail` command line to invoke Artisan commands. Sail will execute your Artisan commands within your application's Docker containers: -->
[Laravel Sail](/docs/8.x/sail)을 로컬 개발 환경으로 사용 중이라면, 아티즌 명령어를 실행할 때 `sail` 커맨드라인을 사용해야 합니다. Sail은 아티즌 명령어를 애플리케이션의 Docker 컨테이너 내부에서 실행합니다.


<!--     ./sail artisan list -->
    ./sail artisan list


<a name="tinker"></a>
<!-- ### Tinker (REPL) -->
### Tinker (REPL)

<!-- Laravel Tinker is a powerful REPL for the Laravel framework, powered by the [PsySH](https://github.com/bobthecow/psysh) package. -->
Laravel Tinker는 Laravel 프레임워크를 위한 강력한 REPL(Read-Eval-Print Loop) 도구로, [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 동작합니다.

<a name="installation"></a>
<!-- #### Installation -->
#### Installation

<!-- All Laravel applications include Tinker by default. However, you may install Tinker using Composer if you have previously removed it from your application: -->
모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 만약 이전에 Tinker를 제거했다면, Composer를 통해 다시 설치할 수 있습니다.

```
composer require laravel/tinker
```

> [!TIP]
> Laravel 애플리케이션과 상호작용할 수 있는 그래픽 UI가 필요하다면 [Tinkerwell](https://tinkerwell.app)을 확인해 보세요!

<a name="usage"></a>
<!-- #### Usage -->
#### Usage

<!-- Tinker allows you to interact with your entire Laravel application on the command line, including your Eloquent models, jobs, events, and more. To enter the Tinker environment, run the `tinker` Artisan command: -->
Tinker를 사용하면 Eloquent 모델, 작업(Job), 이벤트 등 애플리케이션 전체를 명령줄에서 직접 다룰 수 있습니다. Tinker 환경에 진입하려면 `tinker` 아티즌 명령어를 실행하세요.

```
php artisan tinker
```

<!-- You can publish Tinker's configuration file using the `vendor:publish` command: -->
Tinker의 설정 파일을 배포하려면 `vendor:publish` 명령어를 사용할 수 있습니다.

```
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!NOTE]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 작업을 큐(Queue)에 넣기 위해 가비지 컬렉션에 의존합니다. 따라서 tinker에서는 작업을 디스패치(dispatch)할 때 `Bus::dispatch` 또는 `Queue::push`를 사용하는 것이 좋습니다.

<a name="command-allow-list"></a>
<!-- #### Command Allow List -->
#### Command Allow List

<!-- Tinker utilizes an "allow" list to determine which Artisan commands are allowed to be run within its shell. By default, you may run the `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, and `up` commands. If you would like to allow more commands you may add them to the `commands` array in your `tinker.php` configuration file: -->
Tinker는 내부적으로 "허용(allow) 목록"을 사용하여 어떤 아티즌 명령어를 Tinker 셸에서 실행할 수 있는지 결정합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, `up` 명령어만 실행할 수 있습니다. 추가로 허용하고 싶은 명령어가 있다면 `tinker.php` 설정 파일의 `commands` 배열에 추가하면 됩니다.

```
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
<!-- #### Classes That Should Not Be Aliased -->
#### Classes That Should Not Be Aliased

<!-- Typically, Tinker automatically aliases classes as you interact with them in Tinker. However, you may wish to never alias some classes. You may accomplish this by listing the classes in the `dont_alias` array of your `tinker.php` configuration file: -->
보통 Tinker에서는 셸에서 상호작용할 때 클래스가 자동으로 별칭(alias) 처리됩니다. 하지만 일부 클래스는 자동으로 별칭이 지정되지 않게 할 수 있습니다. 이를 위해 `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 추가하면 됩니다.

```
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
<!-- ## Writing Commands -->
## Writing Commands

<!-- In addition to the commands provided with Artisan, you may build your own custom commands. Commands are typically stored in the `app/Console/Commands` directory; however, you are free to choose your own storage location as long as your commands can be loaded by Composer. -->
기본 제공되는 아티즌 명령어 외에도, 직접 새로운 커스텀 명령어를 만들 수 있습니다. 명령어 클래스는 일반적으로 `app/Console/Commands` 디렉터리에 저장되지만, Composer가 불러올 수 있는 위치라면 원하는 디렉터리를 자유롭게 사용할 수 있습니다.

<a name="generating-commands"></a>
<!-- ### Generating Commands -->
### Generating Commands

<!-- To create a new command, you may use the `make:command` Artisan command. This command will create a new command class in the `app/Console/Commands` directory. Don't worry if this directory does not exist in your application - it will be created the first time you run the `make:command` Artisan command: -->
새 명령어를 만들려면 `make:command` 아티즌 명령어를 사용하면 됩니다. 이 명령어는 `app/Console/Commands` 디렉터리에 새로운 커맨드 클래스를 생성합니다. 해당 디렉터리가 아직 없더라도, `make:command` 아티즌 명령어를 처음 실행할 때 자동으로 생성됩니다.

```
php artisan make:command SendEmails
```

<a name="command-structure"></a>
<!-- ### Command Structure -->
### Command Structure

<!-- After generating your command, you should define appropriate values for the `signature` and `description` properties of the class. These properties will be used when displaying your command on the `list` screen. The `signature` property also allows you to define [your command's input expectations](#defining-input-expectations). The `handle` method will be called when your command is executed. You may place your command logic in this method. -->
명령어를 생성한 후에는 클래스의 `signature`와 `description` 속성에 적절한 값을 지정해야 합니다. 이 속성들은 `list` 화면에 명령어를 표시할 때 사용됩니다. 또한, `signature` 속성에서는 [your command's input expectations](#defining-input-expectations)도 정의할 수 있습니다. 명령어가 실제로 실행될 때는 `handle` 메서드가 호출되며, 여기에 명령어의 주요 로직을 작성하면 됩니다.

<!-- Let's take a look at an example command. Note that we are able to request any dependencies we need via the command's `handle` method. The Laravel [service container](/docs/8.x/container) will automatically inject all dependencies that are type-hinted in this method's signature: -->
예시 명령어를 살펴보겠습니다. 아래 예시에서는 필요한 의존성을 `handle` 메서드에서 타입힌트로 직접 주입받고 있습니다. Laravel [service container](/docs/8.x/container)는 메서드에 타입힌트된 모든 의존성을 자동으로 주입해줍니다.

```
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
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @param  \App\Support\DripEmailer  $drip
     * @return mixed
     */
    public function handle(DripEmailer $drip)
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```

> [!TIP]
> 코드 재사용성을 높이기 위해, 콘솔 명령어 내부에서는 가능한 한 로직을 최소화하고, 실제 처리 작업은 애플리케이션 서비스 클래스로 위임하는 것이 좋은 습관입니다. 위 예시처럼 서비스 클래스를 주입하여 이메일 전송과 같은 "핵심 작업"을 담당하도록 하는 방식을 추천합니다.

<a name="closure-commands"></a>
<!-- ### Closure Commands -->
### Closure Commands

<!-- Closure based commands provide an alternative to defining console commands as classes. In the same way that route closures are an alternative to controllers, think of command closures as an alternative to command classes. Within the `commands` method of your `app/Console/Kernel.php` file, Laravel loads the `routes/console.php` file: -->
클로저(Closure) 기반 명령어는 클래스 형태로 명령어를 작성하는 대신 클로저로 정의하는 또 다른 방법을 제공합니다. 라우트에서 클로저를 사용할 수 있듯, 명령어도 클로저로 정의할 수 있습니다. `app/Console/Kernel.php` 파일의 `commands` 메서드 안에서, Laravel은 `routes/console.php` 파일을 로드합니다.

```
/**
 * Register the closure based commands for the application.
 *
 * @return void
 */
protected function commands()
{
    require base_path('routes/console.php');
}
```

<!-- Even though this file does not define HTTP routes, it defines console based entry points (routes) into your application. Within this file, you may define all of your closure based console commands using the `Artisan::command` method. The `command` method accepts two arguments: the [command signature](#defining-input-expectations) and a closure which receives the command's arguments and options: -->
이 파일에서는 HTTP 라우트를 정의하지는 않지만, 애플리케이션의 콘솔 진입점(일종의 라우트)을 정의하게 됩니다. 이 파일 내에서 `Artisan::command` 메서드를 사용해 클로저 기반의 콘솔 명령어를 만들 수 있습니다. `command` 메서드는 [command signature](#defining-input-expectations)와, 명령어의 인수와 옵션을 전달받는 클로저를 인자로 받습니다.

```
Artisan::command('mail:send {user}', function ($user) {
    $this->info("Sending email to: {$user}!");
});
```

<!-- The closure is bound to the underlying command instance, so you have full access to all of the helper methods you would typically be able to access on a full command class. -->
클로저는 기반이 되는 명령어 인스턴스에 바인딩되기 때문에, 일반 커맨드 클래스에서 사용 가능한 헬퍼 메서드를 모두 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
<!-- #### Type-Hinting Dependencies -->
#### Type-Hinting Dependencies

<!-- In addition to receiving your command's arguments and options, command closures may also type-hint additional dependencies that you would like resolved out of the [service container](/docs/8.x/container): -->
명령어의 인수나 옵션뿐 아니라, 클로저에서 [service container](/docs/8.x/container)를 통해 추가 의존성을 타입힌트로 받아올 수도 있습니다.

```
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
<!-- #### Closure Command Descriptions -->
#### Closure Command Descriptions

<!-- When defining a closure based command, you may use the `purpose` method to add a description to the command. This description will be displayed when you run the `php artisan list` or `php artisan help` commands: -->
클로저 기반 명령어를 정의할 때, `purpose` 메서드를 사용해 명령어에 대한 설명을 추가할 수 있습니다. 이 설명은 `php artisan list`나 `php artisan help` 명령어 실행 시 출력됩니다.

```
Artisan::command('mail:send {user}', function ($user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="defining-input-expectations"></a>
<!-- ## Defining Input Expectations -->
## Defining Input Expectations

<!-- When writing console commands, it is common to gather input from the user through arguments or options. Laravel makes it very convenient to define the input you expect from the user using the `signature` property on your commands. The `signature` property allows you to define the name, arguments, and options for the command in a single, expressive, route-like syntax. -->
콘솔 명령어를 작성할 때, 사용자로부터 인수(argument)나 옵션(option) 형태로 입력값을 전달받는 일이 흔합니다. Laravel에서는 명령어의 `signature` 속성을 사용해 입력값의 종류를 간편하게 지정할 수 있습니다. `signature` 속성 하나만으로 명령어 이름, 인수, 옵션을 직관적이고 읽기 쉬운 형태로 정의할 수 있습니다.

<a name="arguments"></a>
<!-- ### Arguments -->
### Arguments

<!-- All user supplied arguments and options are wrapped in curly braces. In the following example, the command defines one required argument: `user`: -->
사용자가 입력하는 모든 인수와 옵션은 중괄호로 감쌉니다. 아래 예시에서 명령어는 필수 인수 `user`를 정의하고 있습니다.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

<!-- You may also make arguments optional or define default values for arguments: -->
인수를 선택적으로 만들거나 기본값을 지정할 수도 있습니다.

```
// Optional argument...
mail:send {user?}

// Optional argument with default value...
mail:send {user=foo}
```

<a name="options"></a>
<!-- ### Options -->
### Options

<!-- Options, like arguments, are another form of user input. Options are prefixed by two hyphens (`--`) when they are provided via the command line. There are two types of options: those that receive a value and those that don't. Options that don't receive a value serve as a boolean "switch". Let's take a look at an example of this type of option: -->
옵션도 인수와 마찬가지로 사용자 입력을 전달받는 방법 중 하나입니다. 옵션은 커맨드라인에서 두 개의 하이픈(`--`)을 붙여 전달합니다. 옵션에는 값을 필요로 하지 않는 스위치형 옵션과, 값을 전달받는 옵션 두 가지가 있습니다. 먼저 값이 없는(스위치) 옵션 예시를 확인해보세요.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

<!-- In this example, the `--queue` switch may be specified when calling the Artisan command. If the `--queue` switch is passed, the value of the option will be `true`. Otherwise, the value will be `false`: -->
위 예시에서 `--queue` 옵션은 아티즌 명령어 실행 시 함께 지정할 수 있습니다. 만약 `--queue`가 전달되면 옵션의 값은 `true`가 되고, 전달하지 않으면 `false`가 됩니다.

```
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
<!-- #### Options With Values -->
#### Options With Values

<!-- Next, let's take a look at an option that expects a value. If the user must specify a value for an option, you should suffix the option name with a `=` sign: -->
다음으로, 값을 받아야 하는 옵션 예시를 살펴보겠습니다. 옵션 값이 꼭 필요하다면 옵션 이름 뒤에 `=` 기호를 붙여서 정의합니다.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

<!-- In this example, the user may pass a value for the option like so. If the option is not specified when invoking the command, its value will be `null`: -->
이렇게 정의하면, 사용자는 아래와 같이 옵션에 값을 넘길 수 있습니다. 옵션을 생략하면 값은 `null`이 됩니다.

```
php artisan mail:send 1 --queue=default
```

<!-- You may assign default values to options by specifying the default value after the option name. If no option value is passed by the user, the default value will be used: -->
기본값이 있는 옵션을 정의하고 싶다면 옵션명 뒤에 기본값을 할당해줍니다. 사용자가 옵션 값을 주지 않으면 이 기본값이 사용됩니다.

```
mail:send {user} {--queue=default}
```

<a name="option-shortcuts"></a>
<!-- #### Option Shortcuts -->
#### Option Shortcuts

<!-- To assign a shortcut when defining an option, you may specify it before the option name and use the `|` character as a delimiter to separate the shortcut from the full option name: -->
옵션에 단축키(짧은 이름)를 지정하고 싶다면, 단축키를 먼저 쓰고 `|` 기호로 구분한 뒤 전체 이름을 작성합니다.

```
mail:send {user} {--Q|queue}
```

<!-- When invoking the command on your terminal, option shortcuts should be prefixed with a single hyphen: -->
터미널에서 명령어를 실행할 때는 단축 옵션은 한 개의 하이픈과 함께 사용합니다.

```
php artisan mail:send 1 -Q
```

<a name="input-arrays"></a>
<!-- ### Input Arrays -->
### Input Arrays

<!-- If you would like to define arguments or options to expect multiple input values, you may use the `*` character. First, let's take a look at an example that specifies such an argument: -->
인수나 옵션으로 여러 값을 입력받고 싶다면, 별표(`*`) 문자를 사용할 수 있습니다. 먼저, 다중 값을 받는 인수 예시를 살펴보세요.

```
mail:send {user*}
```

<!-- When calling this method, the `user` arguments may be passed in order to the command line. For example, the following command will set the value of `user` to an array with `foo` and `bar` as its values: -->
이 명령어를 실행할 때, `user` 인수에 여러 값을 전달할 수 있습니다. 아래와 같이 입력하면 `user`의 값은 `foo`, `bar`가 들어있는 배열이 됩니다.

```
php artisan mail:send foo bar
```

<!-- This `*` character can be combined with an optional argument definition to allow zero or more instances of an argument: -->
별표(`*`) 문자는 선택적 인수와도 조합할 수 있어, 0개 이상의 값을 허용할 수 있습니다.

```
mail:send {user?*}
```

<a name="option-arrays"></a>
<!-- #### Option Arrays -->
#### Option Arrays

<!-- When defining an option that expects multiple input values, each option value passed to the command should be prefixed with the option name: -->
여러 값을 받는 옵션을 정의할 때는 각 값 앞에 옵션명을 반복해 적으면 됩니다.

```
mail:send {user} {--id=*}

php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
<!-- ### Input Descriptions -->
### Input Descriptions

<!-- You may assign descriptions to input arguments and options by separating the argument name from the description using a colon. If you need a little extra room to define your command, feel free to spread the definition across multiple lines: -->
인수나 옵션에 설명을 추가하려면, 이름과 설명 사이에 콜론을 사용합니다. 명령어 정의가 길어진다면 여러 줄로 나누어 작성하셔도 됩니다.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : The ID of the user}
                        {--queue : Whether the job should be queued}';
```

<a name="command-io"></a>
<!-- ## Command I/O -->
## Command I/O

<a name="retrieving-input"></a>
<!-- ### Retrieving Input -->
### Retrieving Input

<!-- While your command is executing, you will likely need to access the values for the arguments and options accepted by your command. To do so, you may use the `argument` and `option` methods. If an argument or option does not exist, `null` will be returned: -->
명령어 실행 도중, 입력받은 인수나 옵션 값을 코드에서 활용할 일도 많습니다. 이때는 `argument`와 `option` 메서드를 사용하면 됩니다. 만약 해당 인수나 옵션이 없으면 `null`이 반환됩니다.

```
/**
 * Execute the console command.
 *
 * @return int
 */
public function handle()
{
    $userId = $this->argument('user');

    //
}
```

<!-- If you need to retrieve all of the arguments as an `array`, call the `arguments` method: -->
모든 인수 값을 `array`로 한 번에 가져오려면 `arguments` 메서드를 사용합니다.

```
$arguments = $this->arguments();
```

<!-- Options may be retrieved just as easily as arguments using the `option` method. To retrieve all of the options as an array, call the `options` method: -->
각 옵션 값 역시 `option` 메서드로 쉽게 얻을 수 있습니다. 모든 옵션 값을 배열로 받고 싶다면 `options` 메서드를 호출하면 됩니다.

```
// Retrieve a specific option...
$queueName = $this->option('queue');

// Retrieve all options as an array...
$options = $this->options();
```

<a name="prompting-for-input"></a>
<!-- ### Prompting For Input -->
### Prompting For Input

<!-- In addition to displaying output, you may also ask the user to provide input during the execution of your command. The `ask` method will prompt the user with the given question, accept their input, and then return the user's input back to your command: -->
출력 결과를 보여주는 것뿐 아니라, 명령어 실행 도중 사용자에게 추가 입력을 요청할 수도 있습니다. `ask` 메서드는 질문을 보여주고, 사용자의 입력값을 받아 반환합니다.

```
/**
 * Execute the console command.
 *
 * @return mixed
 */
public function handle()
{
    $name = $this->ask('What is your name?');
}
```

<!-- The `secret` method is similar to `ask`, but the user's input will not be visible to them as they type in the console. This method is useful when asking for sensitive information such as passwords: -->
`secret` 메서드는 `ask`와 비슷하지만, 입력한 내용이 콘솔에 표시되지 않습니다. 비밀번호 등 민감한 정보를 입력받을 때 적합합니다.

```
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
<!-- #### Asking For Confirmation -->
#### Asking For Confirmation

<!-- If you need to ask the user for a simple "yes or no" confirmation, you may use the `confirm` method. By default, this method will return `false`. However, if the user enters `y` or `yes` in response to the prompt, the method will return `true`. -->
사용자에게 간단히 "예/아니오"로 답할 수 있게 하고 싶을 때는 `confirm` 메서드를 사용하세요. 기본적으로 이 메서드는 `false`를 반환하지만, 사용자 입력이 `y` 또는 `yes`라면 `true`를 반환합니다.

```
if ($this->confirm('Do you wish to continue?')) {
    //
}
```

<!-- If necessary, you may specify that the confirmation prompt should return `true` by default by passing `true` as the second argument to the `confirm` method: -->
필요하다면, `confirm` 메서드의 두 번째 인자로 `true`를 전달하여 기본값이 `true`가 되도록 할 수 있습니다.

```
if ($this->confirm('Do you wish to continue?', true)) {
    //
}
```

<a name="auto-completion"></a>
<!-- #### Auto-Completion -->
#### Auto-Completion

<!-- The `anticipate` method can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints: -->
`anticipate` 메서드를 이용하면 입력 가능한 선택지를 자동 완성으로 보여줄 수 있습니다. 사용자는 자동완성 힌트를 참고하되, 힌트에 없는 값도 입력할 수 있습니다.

```
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

<!-- Alternatively, you may pass a closure as the second argument to the `anticipate` method. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far, and return an array of options for auto-completion: -->
또는 `anticipate` 메서드의 두 번째 인자로 클로저를 넘겨, 사용자가 입력할 때마다 동적으로 자동완성 옵션을 제공할 수도 있습니다. 이 클로저는 사용자가 입력한 문자열을 인자로 받아, 자동 완성용 배열을 반환해야 합니다.

```
$name = $this->anticipate('What is your address?', function ($input) {
    // Return auto-completion options...
});
```

<a name="multiple-choice-questions"></a>
<!-- #### Multiple Choice Questions -->
#### Multiple Choice Questions

<!-- If you need to give the user a predefined set of choices when asking a question, you may use the `choice` method. You may set the array index of the default value to be returned if no option is chosen by passing the index as the third argument to the method: -->
미리 정의된 선택지 중에서 사용자가 하나(또는 여러 개)를 고르도록 하려면 `choice` 메서드를 사용하면 됩니다. 세 번째 인수로 기본값의 배열 인덱스를 넘길 수 있으며, 네 번째와 다섯 번째 인수에서는 유효 응답 선택 시도 횟수와 복수 선택 허용 여부를 지정할 수 있습니다.

```
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

<!-- In addition, the `choice` method accepts optional fourth and fifth arguments for determining the maximum number of attempts to select a valid response and whether multiple selections are permitted: -->
또한 `choice` 메서드는 유효한 응답을 선택할 수 있는 최대 시도 횟수와 복수 선택 허용 여부를 결정하는 선택적 네 번째, 다섯 번째 인수를 받습니다.

```
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

<!-- To send output to the console, you may use the `line`, `info`, `comment`, `question`, `warn`, and `error` methods. Each of these methods will use appropriate ANSI colors for their purpose. For example, let's display some general information to the user. Typically, the `info` method will display in the console as green colored text: -->
콘솔에 결과를 출력하려면 `line`, `info`, `comment`, `question`, `warn`, `error` 등의 메서드를 사용할 수 있습니다. 각 메서드는 용도에 맞는 ANSI 색상을 사용해서 표시됩니다. 예를 들어, 일반적인 안내 메시지는 `info` 메서드를 사용하며, 보통 초록색으로 출력됩니다.

```
/**
 * Execute the console command.
 *
 * @return mixed
 */
public function handle()
{
    // ...

    $this->info('The command was successful!');
}
```

<!-- To display an error message, use the `error` method. Error message text is typically displayed in red: -->
오류 메시지를 출력하려면 `error` 메서드를 사용합니다. 오류 메시지는 레드 컬러로 표시됩니다.

```
$this->error('Something went wrong!');
```

<!-- You may use the `line` method to display plain, uncolored text: -->
컬러 없이 평범한 텍스트로 출력하고 싶으면 `line` 메서드를 사용하세요.

```
$this->line('Display this on the screen');
```

<!-- You may use the `newLine` method to display a blank line: -->
빈 줄을 삽입하려면 `newLine` 메서드를 사용할 수 있습니다.

```
// Write a single blank line...
$this->newLine();

// Write three blank lines...
$this->newLine(3);
```

<a name="tables"></a>
<!-- #### Tables -->
#### Tables

<!--
The `table` method makes it easy to correctly format multiple rows / columns of data. All you need to do is provide the column names and the data for the table and Laravel will
automatically calculate the appropriate width and height of the table for you:
-->
`table` 메서드를 사용하면 여러 줄/여러 컬럼의 데이터를 손쉽게 표 형태로 깔끔하게 출력할 수 있습니다. 컬럼 이름과 데이터 배열만 넘기면 Laravel이 적당한 너비와 높이도 자동으로 맞춰줍니다.

```
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
처리 시간이 오래 걸리는 작업일 때, 사용자에게 완료 진행 상태를 보여주고 싶으면 진행률 표시줄(progress bar)을 사용할 수 있습니다. `withProgressBar` 메서드를 사용하면, 주어진 이터러블 값을 순회하며 진행률이 표시됩니다.

```
use App\Models\User;

$users = $this->withProgressBar(User::all(), function ($user) {
    $this->performTask($user);
});
```

<!-- Sometimes, you may need more manual control over how a progress bar is advanced. First, define the total number of steps the process will iterate through. Then, advance the progress bar after processing each item: -->
진행률 표시줄을 좀 더 세밀하게 제어하고 싶다면, 전체 단계 수를 먼저 지정하고, 값마다 직접 진행도를 증가시키는 방법도 있습니다.

```
$users = App\Models\User::all();

$bar = $this->output->createProgressBar(count($users));

$bar->start();

foreach ($users as $user) {
    $this->performTask($user);

    $bar->advance();
}

$bar->finish();
```

> [!TIP]
> 더 고급 기능이 필요하면 [Symfony Progress Bar component documentation](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
<!-- ## Registering Commands -->
## Registering Commands

<!-- All of your console commands are registered within your application's `App\Console\Kernel` class, which is your application's "console kernel". Within the `commands` method of this class, you will see a call to the kernel's `load` method. The `load` method will scan the `app/Console/Commands` directory and automatically register each command it contains with Artisan. You are even free to make additional calls to the `load` method to scan other directories for Artisan commands: -->
모든 콘솔 명령어는 애플리케이션의 "콘솔 커널(Kernel)" 클래스인 `App\Console\Kernel`에서 등록됩니다. 이 클래스의 `commands` 메서드에서 커널의 `load` 메서드를 호출하는 것을 볼 수 있습니다. `load` 메서드는 `app/Console/Commands` 디렉터리를 스캔하여 그 안의 명령어를 자동으로 아티즌에 등록합니다. 필요하다면 다른 디렉터리도 스캔하도록 `load` 메서드를 추가로 호출할 수 있습니다.

```
/**
 * Register the commands for the application.
 *
 * @return void
 */
protected function commands()
{
    $this->load(__DIR__.'/Commands');
    $this->load(__DIR__.'/../Domain/Orders/Commands');

    // ...
}
```

<!-- If necessary, you may manually register commands by adding the command's class name to a `$commands` property within your `App\Console\Kernel` class. If this property is not already defined on your kernel, you should define it manually. When Artisan boots, all the commands listed in this property will be resolved by the [service container](/docs/8.x/container) and registered with Artisan: -->
특정 명령어를 수동으로 등록해야 할 경우, `App\Console\Kernel` 클래스 안에 `$commands` 속성(배열)을 만들어 등록하면 됩니다. 이 속성이 없으면 직접 정의하면 되며, 아티즌이 부팅할 때 이 배열에 있는 모든 명령어가 [service container](/docs/8.x/container)를 통해 불러와집니다.

```
protected $commands = [
    Commands\SendEmails::class
];
```

<a name="programmatically-executing-commands"></a>
<!-- ## Programmatically Executing Commands -->
## Programmatically Executing Commands

<!-- Sometimes you may wish to execute an Artisan command outside of the CLI. For example, you may wish to execute an Artisan command from a route or controller. You may use the `call` method on the `Artisan` facade to accomplish this. The `call` method accepts either the command's signature name or class name as its first argument, and an array of command parameters as the second argument. The exit code will be returned: -->
CLI(명령줄)가 아닌 코드에서 아티즌 명령어를 실행하고 싶을 때도 있습니다. 예를 들어, 라우트나 컨트롤러에서 아티즌 명령어를 실행할 수 있습니다. 이때는 `Artisan` 파사드의 `call` 메서드를 사용하면 됩니다. `call` 메서드의 첫 번째 인수로 명령어 시그니처(이름)나 클래스명을 넘기고, 두 번째 인수로 명령어의 파라미터 배열을 전달합니다. 이 때, 명령어 실행 결과는 종료 코드로 반환됩니다.

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function ($user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    //
});
```

<!-- Alternatively, you may pass the entire Artisan command to the `call` method as a string: -->
또는, 전체 아티즌 명령어를 문자열로 `call` 메서드에 전달할 수도 있습니다.

```
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
<!-- #### Passing Array Values -->
#### Passing Array Values

<!-- If your command defines an option that accepts an array, you may pass an array of values to that option: -->
옵션이 배열 입력을 허용하는 경우, 값을 배열로 전달하면 됩니다.

```
use Illuminate\Support\Facades\Artisan;

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
문자열이 아니라 불리언 값만 허용하는 옵션(예: `migrate:refresh` 명령어의 `--force` 플래그)을 지정하고 싶을 때는 값으로 `true`나 `false`를 넘기면 됩니다.

```
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
<!-- #### Queueing Artisan Commands -->
#### Queueing Artisan Commands

<!-- Using the `queue` method on the `Artisan` facade, you may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/8.x/queues). Before using this method, make sure you have configured your queue and are running a queue listener: -->
`Artisan` 파사드의 `queue` 메서드를 사용하면 아티즌 명령어를 큐(queue)에 넣을 수 있습니다. 이렇게 하면 명령어가 [queue workers](/docs/8.x/queues)에 의해 백그라운드에서 처리됩니다. 이 메서드를 사용하기 전에 큐 설정이 되어 있고 큐 리스너가 실행 중이어야 합니다.

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function ($user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    //
});
```

<!-- Using the `onConnection` and `onQueue` methods, you may specify the connection or queue the Artisan command should be dispatched to: -->
추가로, `onConnection` 및 `onQueue` 메서드를 사용하면 명령어가 어느 연결(connection)과 큐(queue)에서 실행될지 직접 지정할 수 있습니다.

```
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
<!-- ### Calling Commands From Other Commands -->
### Calling Commands From Other Commands

<!-- Sometimes you may wish to call other commands from an existing Artisan command. You may do so using the `call` method. This `call` method accepts the command name and an array of command arguments / options: -->
기존 아티즌 명령어 안에서 다른 명령어를 호출하고 싶을 수도 있습니다. 이때는 `call` 메서드를 사용하면 됩니다. 이 `call` 메서드는 명령어 이름과 인수/옵션 배열을 인수로 받습니다.

```
/**
 * Execute the console command.
 *
 * @return mixed
 */
public function handle()
{
    $this->call('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

    //
}
```

<!-- If you would like to call another console command and suppress all of its output, you may use the `callSilently` method. The `callSilently` method has the same signature as the `call` method: -->
다른 콘솔 명령어를 호출할 때 출력이 모두 숨겨지길 원하면 `callSilently` 메서드를 사용할 수 있습니다. `callSilently` 메서드는 `call` 메서드와 동일한 시그니처를 가집니다.

```
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
<!-- ## Signal Handling -->
## Signal Handling

<!-- The Symfony Console component, which powers the Artisan console, allows you to indicate which process signals (if any) your command handles. For example, you may indicate that your command handles the `SIGINT` and `SIGTERM` signals. -->
아티즌 콘솔의 기반이 되는 Symfony Console 컴포넌트를 사용하면, 명령어가 어떤 프로세스 시그널(Signal)을 처리할 수 있는지도 선언할 수 있습니다. 예를 들어, `SIGINT`나 `SIGTERM` 시그널을 명령어가 직접 처리하도록 지정할 수 있습니다.

<!-- To get started, you should implement the `Symfony\Component\Console\Command\SignalableCommandInterface` interface on your Artisan command class. This interface requires you to define two methods: `getSubscribedSignals` and `handleSignal`: -->
시작하려면, Artisan 명령어 클래스에서 `Symfony\Component\Console\Command\SignalableCommandInterface` 인터페이스를 구현해야 합니다. 이 인터페이스를 구현하면 `getSubscribedSignals`와 `handleSignal` 두 가지 메서드를 반드시 정의해야 합니다.

```php
<?php

use Symfony\Component\Console\Command\SignalableCommandInterface;

class StartServer extends Command implements SignalableCommandInterface
{
    // ...

    /**
     * Get the list of signals handled by the command.
     *
     * @return array
     */
    public function getSubscribedSignals(): array
    {
        return [SIGINT, SIGTERM];
    }

    /**
     * Handle an incoming signal.
     *
     * @param  int  $signal
     * @return void
     */
    public function handleSignal(int $signal): void
    {
        if ($signal === SIGINT) {
            $this->stopServer();

            return;
        }
    }
}
```

<!-- As you might expect, the `getSubscribedSignals` method should return an array of the signals that your command can handle, while the `handleSignal` method receives the signal and can respond accordingly. -->
예상할 수 있듯, `getSubscribedSignals` 메서드는 명령어에서 처리할 수 있는 시그널의 배열을 반환하며, `handleSignal` 메서드는 실제로 시그널이 발생했을 때 필요한 동작을 수행합니다.

<a name="stub-customization"></a>
<!-- ## Stub Customization -->
## Stub Customization

<!-- The Artisan console's `make` commands are used to create a variety of classes, such as controllers, jobs, migrations, and tests. These classes are generated using "stub" files that are populated with values based on your input. However, you may want to make small changes to files generated by Artisan. To accomplish this, you may use the `stub:publish` command to publish the most common stubs to your application so that you can customize them: -->
아티즌 콘솔의 `make` 관련 명령어는 컨트롤러, 작업(Job), 마이그레이션, 테스트 등 다양한 클래스를 생성할 때 사용됩니다. 이러한 클래스들은 "스텁(stub)" 파일을 템플릿 삼아 생성되며, 입력값에 따라 자동으로 일부 내용이 채워집니다. 하지만, 생성되는 파일의 일부를 자신만의 방식으로 수정하고 싶을 때도 있죠. 이럴 때는 `stub:publish` 명령어로 주요 스텁 파일을 애플리케이션에 복사해 원하는 대로 커스터마이즈할 수 있습니다.

```
php artisan stub:publish
```

<!-- The published stubs will be located within a `stubs` directory in the root of your application. Any changes you make to these stubs will be reflected when you generate their corresponding classes using Artisan's `make` commands. -->
배포된 스텁 파일들은 애플리케이션 루트의 `stubs` 디렉터리에 생깁니다. 이 파일을 직접 수정하면, 이후 아티즌의 `make` 관련 명령어로 생성되는 클래스에 반영됩니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Artisan dispatches three events when running commands: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, and `Illuminate\Console\Events\CommandFinished`. The `ArtisanStarting` event is dispatched immediately when Artisan starts running. Next, the `CommandStarting` event is dispatched immediately before a command runs. Finally, the `CommandFinished` event is dispatched once a command finishes executing. -->
아티즌이 명령어를 실행할 때, 세 가지 이벤트가 발생합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`. `ArtisanStarting` 이벤트는 아티즌 실행이 시작되자마자 발생합니다. 이어서, 각 명령어가 실행되기 직전에 `CommandStarting` 이벤트가, 명령어 실행이 끝나면 `CommandFinished` 이벤트가 트리거됩니다.
