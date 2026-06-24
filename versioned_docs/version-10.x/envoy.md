<!-- # Laravel Envoy -->
# Laravel Envoy

- [Introduction](#introduction)
- [Installation](#installation)
- [Writing Tasks](#writing-tasks)
    - [Defining Tasks](#defining-tasks)
    - [Multiple Servers](#multiple-servers)
    - [Setup](#setup)
    - [Variables](#variables)
    - [Stories](#stories)
    - [Hooks](#completion-hooks)
- [Running Tasks](#running-tasks)
    - [Confirming Task Execution](#confirming-task-execution)
- [Notifications](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [Microsoft Teams](#microsoft-teams)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Envoy](https://github.com/laravel/envoy) is a tool for executing common tasks you run on your remote servers. Using [Blade](/docs/10.x/blade) style syntax, you can easily setup tasks for deployment, Artisan commands, and more. Currently, Envoy only supports the Mac and Linux operating systems. However, Windows support is achievable using [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10). -->
[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 실행하는 작업들을 손쉽게 자동화할 수 있게 해주는 도구입니다. [Blade](/docs/10.x/blade) 스타일의 문법을 통해 배포, Artisan 명령 실행 등 다양한 작업을 손쉽게 작성할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영체제만 공식 지원합니다. 단, [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 이용하면 Windows 환경에서도 사용할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install Envoy into your project using the Composer package manager: -->
먼저 Composer 패키지 매니저를 사용하여 프로젝트에 Envoy를 설치합니다.

```shell
composer require laravel/envoy --dev
```

<!-- Once Envoy has been installed, the Envoy binary will be available in your application's `vendor/bin` directory: -->
설치가 완료되면, Envoy 실행 파일이 애플리케이션의 `vendor/bin` 디렉터리 안에 생성됩니다.

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
<!-- ## Writing Tasks -->
## Writing Tasks

<a name="defining-tasks"></a>
<!-- ### Defining Tasks -->
### Defining Tasks

<!-- Tasks are the basic building block of Envoy. Tasks define the shell commands that should execute on your remote servers when the task is invoked. For example, you might define a task that executes the `php artisan queue:restart` command on all of your application's queue worker servers. -->
태스크는 Envoy의 기본적인 구성 단위입니다. 태스크는 해당 태스크가 실행될 때 원격 서버에서 실행될 쉘 명령어들을 정의합니다. 예를 들어, 모든 큐 워커 서버에서 `php artisan queue:restart` 명령을 실행하는 태스크를 만들 수 있습니다.

<!-- All of your Envoy tasks should be defined in an `Envoy.blade.php` file at the root of your application. Here's an example to get you started: -->
모든 Envoy 태스크는 애플리케이션 루트에 있는 `Envoy.blade.php` 파일에 정의해야 합니다. 아래는 기본 예시입니다.

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

<!-- As you can see, an array of `@servers` is defined at the top of the file, allowing you to reference these servers via the `on` option of your task declarations. The `@servers` declaration should always be placed on a single line. Within your `@task` declarations, you should place the shell commands that should execute on your servers when the task is invoked. -->
보시다시피, 파일 맨 위에는 `@servers` 배열이 정의되어 있습니다. 이를 통해 태스크 선언의 `on` 옵션에서 서버를 참조할 수 있습니다. `@servers` 선언은 반드시 한 줄로 작성해야 합니다. 각 `@task` 선언 안에는 태스크 실행 시 서버에서 실행할 쉘 명령어를 작성합니다.

<a name="local-tasks"></a>
<!-- #### Local Tasks -->
#### Local Tasks

<!-- You can force a script to run on your local computer by specifying the server's IP address as `127.0.0.1`: -->
스크립트를 본인 컴퓨터에서 실행하려면, 서버의 IP 주소로 `127.0.0.1`을 지정하세요.

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
<!-- #### Importing Envoy Tasks -->
#### Importing Envoy Tasks

<!-- Using the `@import` directive, you may import other Envoy files so their stories and tasks are added to yours. After the files have been imported, you may execute the tasks they contain as if they were defined in your own Envoy file: -->
`@import` 디렉티브를 사용하면 다른 Envoy 파일을 임포트하여 해당 스토리와 태스크를 내 파일에 추가할 수 있습니다. 임포트된 파일에 정의된 태스크는 본인의 Envoy 파일에 작성된 것처럼 사용할 수 있습니다.

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
<!-- ### Multiple Servers -->
### Multiple Servers

<!-- Envoy allows you to easily run a task across multiple servers. First, add additional servers to your `@servers` declaration. Each server should be assigned a unique name. Once you have defined your additional servers you may list each of the servers in the task's `on` array: -->
Envoy를 사용하면 한 번에 여러 서버에 태스크를 쉽게 실행할 수 있습니다. 우선 `@servers` 선언에 추가 서버를 정의하고, 각 서버에 고유한 이름을 지정합니다. 추가한 서버들은 태스크의 `on` 배열에 나열하면 됩니다.

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2']])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="parallel-execution"></a>
<!-- #### Parallel Execution -->
#### Parallel Execution

<!-- By default, tasks will be executed on each server serially. In other words, a task will finish running on the first server before proceeding to execute on the second server. If you would like to run a task across multiple servers in parallel, add the `parallel` option to your task declaration: -->
기본적으로 태스크는 각 서버에서 순차적으로 실행됩니다. 즉, 첫 번째 서버에서 완료된 후 두 번째 서버에서 실행이 시작됩니다. 여러 서버에서 동시에 태스크를 실행하려면, 태스크 선언에 `parallel` 옵션을 추가하면 됩니다.

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="setup"></a>
<!-- ### Setup -->
### Setup

<!-- Sometimes, you may need to execute arbitrary PHP code before running your Envoy tasks. You may use the `@setup` directive to define a block of PHP code that should execute before your tasks: -->
가끔 Envoy 태스크를 실행하기 전에 임의의 PHP 코드를 실행해야 할 때가 있습니다. 이럴 때는 `@setup` 디렉티브를 사용해 태스크 실행 전에 동작할 PHP 코드를 정의할 수 있습니다.

```php
@setup
    $now = new DateTime;
@endsetup
```

<!-- If you need to require other PHP files before your task is executed, you may use the `@include` directive at the top of your `Envoy.blade.php` file: -->
태스크 실행 전 추가적으로 PHP 파일을 읽어와야 한다면, `Envoy.blade.php` 파일 상단에 `@include` 디렉티브를 사용할 수 있습니다.

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
<!-- ### Variables -->
### Variables

<!-- If needed, you may pass arguments to Envoy tasks by specifying them on the command line when invoking Envoy: -->
필요하다면 Envoy 태스크를 실행할 때 명령줄에서 인수를 전달할 수 있습니다.

```shell
php vendor/bin/envoy run deploy --branch=master
```

<!-- You may access the options within your tasks using Blade's "echo" syntax. You may also define Blade `if` statements and loops within your tasks. For example, let's verify the presence of the `$branch` variable before executing the `git pull` command: -->
태스크 내에서는 Blade의 "echo" 문법을 이용해 옵션 값을 가져올 수 있습니다. 또한, 태스크 안에서 Blade의 `if` 문이나 반복문도 사용할 수 있습니다. 예를 들어, `git pull` 명령을 실행하기 전에 `$branch` 변수가 존재하는지 확인할 수 있습니다.

```blade
@servers(['web' => ['user@192.168.1.1']])

@task('deploy', ['on' => 'web'])
    cd /home/user/example.com

    @if ($branch)
        git pull origin {{ $branch }}
    @endif

    php artisan migrate --force
@endtask
```

<a name="stories"></a>
<!-- ### Stories -->
### Stories

<!-- Stories group a set of tasks under a single, convenient name. For instance, a `deploy` story may run the `update-code` and `install-dependencies` tasks by listing the task names within its definition: -->
스토리는 여러 태스크를 하나의 이름으로 그룹화해서 한 번에 실행할 수 있게 해줍니다. 예를 들어, `deploy` 스토리는 `update-code`, `install-dependencies` 태스크를 묶어서 한 번에 실행할 수 있습니다.

```blade
@servers(['web' => ['user@192.168.1.1']])

@story('deploy')
    update-code
    install-dependencies
@endstory

@task('update-code')
    cd /home/user/example.com
    git pull origin master
@endtask

@task('install-dependencies')
    cd /home/user/example.com
    composer install
@endtask
```

<!-- Once the story has been written, you may invoke it in the same way you would invoke a task: -->
스토리가 작성되면 아래와 같이 태스크를 실행할 때와 마찬가지로 사용할 수 있습니다.

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
<!-- ### Hooks -->
### Hooks

<!-- When tasks and stories run, a number of hooks are executed. The hook types supported by Envoy are `@before`, `@after`, `@error`, `@success`, and `@finished`. All of the code in these hooks is interpreted as PHP and executed locally, not on the remote servers that your tasks interact with. -->
태스크와 스토리가 실행될 때, 다양한 훅이 함께 동작합니다. Envoy에서 지원하는 훅 타입은 `@before`, `@after`, `@error`, `@success`, `@finished`입니다. 이 훅 안의 코드는 모두 PHP로 해석되어 원격 서버가 아닌, 로컬 환경에서 실행됩니다.

<!-- You may define as many of each of these hooks as you like. They will be executed in the order that they appear in your Envoy script. -->
각 훅 타입은 동일한 타입의 훅을 여러 개 정의할 수 있으며, Envoy 스크립트 상에서 정의한 순서대로 실행됩니다.

<a name="hook-before"></a>
<!-- #### `@before` -->
#### `@before`

<!-- Before each task execution, all of the `@before` hooks registered in your Envoy script will execute. The `@before` hooks receive the name of the task that will be executed: -->
각 태스크 실행 전에, Envoy 스크립트에 등록된 모든 `@before` 훅이 실행됩니다. `@before` 훅은 실행될 태스크의 이름을 받습니다.

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
<!-- #### `@after` -->
#### `@after`

<!-- After each task execution, all of the `@after` hooks registered in your Envoy script will execute. The `@after` hooks receive the name of the task that was executed: -->
각 태스크 실행이 끝난 뒤 Envoy 스크립트 내 모든 `@after` 훅이 실행됩니다. `@after` 훅은 실행된 태스크의 이름을 받습니다.

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
<!-- #### `@error` -->
#### `@error`

<!-- After every task failure (exits with a status code greater than `0`), all of the `@error` hooks registered in your Envoy script will execute. The `@error` hooks receive the name of the task that was executed: -->
태스크가 실패(종료 코드가 `0`보다 클 때)하면, Envoy 스크립트 내 모든 `@error` 훅이 실행됩니다. `@error` 훅은 실행된 태스크의 이름을 받습니다.

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
<!-- #### `@success` -->
#### `@success`

<!-- If all tasks have executed without errors, all of the `@success` hooks registered in your Envoy script will execute: -->
모든 태스크가 에러 없이 완료된 경우, 등록된 모든 `@success` 훅이 실행됩니다.

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
<!-- #### `@finished` -->
#### `@finished`

<!-- After all tasks have been executed (regardless of exit status), all of the `@finished` hooks will be executed. The `@finished` hooks receive the status code of the completed task, which may be `null` or an `integer` greater than or equal to `0`: -->
모든 태스크가 실행된 뒤(성공/실패와 관계 없이) 모든 `@finished` 훅이 실행됩니다. `@finished` 훅은 완료된 태스크의 상태 코드를 받으며, 이 값은 `null`이거나 `0` 이상의 `integer`일 수 있습니다.

```blade
@finished
    if ($exitCode > 0) {
        // There were errors in one of the tasks...
    }
@endfinished
```

<a name="running-tasks"></a>
<!-- ## Running Tasks -->
## Running Tasks

<!-- To run a task or story that is defined in your application's `Envoy.blade.php` file, execute Envoy's `run` command, passing the name of the task or story you would like to execute. Envoy will execute the task and display the output from your remote servers as the task is running: -->
애플리케이션의 `Envoy.blade.php` 파일에 정의된 태스크나 스토리를 실행하려면, Envoy의 `run` 명령어에 실행하고자 하는 태스크 또는 스토리의 이름을 인자로 전달하면 됩니다. Envoy는 태스크를 실행하는 동안 원격 서버의 출력 결과를 실시간으로 보여줍니다.

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
<!-- ### Confirming Task Execution -->
### Confirming Task Execution

<!-- If you would like to be prompted for confirmation before running a given task on your servers, you should add the `confirm` directive to your task declaration. This option is particularly useful for destructive operations: -->
특정 태스크를 서버에서 실행하기 전에 확인을 요구하고 싶을 때는, 태스크 선언에 `confirm` 옵션을 추가하세요. 이 옵션은 파괴적 작업 등에서 실수로 실행하는 것을 예방하는 데 유용합니다.

```blade
@task('deploy', ['on' => 'web', 'confirm' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate
@endtask
```

<a name="notifications"></a>
<!-- ## Notifications -->
## Notifications

<a name="slack"></a>
<!-- ### Slack -->
### Slack

<!-- Envoy supports sending notifications to [Slack](https://slack.com) after each task is executed. The `@slack` directive accepts a Slack hook URL and a channel / user name. You may retrieve your webhook URL by creating an "Incoming WebHooks" integration in your Slack control panel. -->
Envoy는 각 태스크 실행 후 [Slack](https://slack.com)으로 알림 메시지를 보낼 수 있습니다. `@slack` 디렉티브에는 Slack 훅 URL과 채널 또는 사용자명을 지정합니다. 웹훅 URL은 Slack 관리 패널에서 "Incoming WebHooks" 통합을 생성하여 얻을 수 있습니다.

<!-- You should pass the entire webhook URL as the first argument given to the `@slack` directive. The second argument given to the `@slack` directive should be a channel name (`#channel`) or a user name (`@user`): -->
`@slack` 디렉티브의 첫 번째 인자로 전체 웹훅 URL을 전달해야 합니다. `@slack` 디렉티브의 두 번째 인자로는 채널명(`#channel`) 또는 사용자명(`@user`)을 전달해야 합니다.

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

<!-- By default, Envoy notifications will send a message to the notification channel describing the task that was executed. However, you may overwrite this message with your own custom message by passing a third argument to the `@slack` directive: -->
기본적으로 Envoy 알림은 해당 태스크의 실행 내역을 채널에 알려주지만, `@slack` 디렉티브에 세 번째 인자로 원하는 메시지를 전달하면 이 메시지를 덮어쓸 수 있습니다.

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
<!-- ### Discord -->
### Discord

<!-- Envoy also supports sending notifications to [Discord](https://discord.com) after each task is executed. The `@discord` directive accepts a Discord hook URL and a message. You may retrieve your webhook URL by creating a "Webhook" in your Server Settings and choosing which channel the webhook should post to. You should pass the entire Webhook URL into the `@discord` directive: -->
Envoy는 [Discord](https://discord.com)로도 태스크 마다 알림을 보낼 수 있습니다. `@discord` 디렉티브에는 Discord 웹훅 URL과 메시지를 입력해야 합니다. 웹훅 URL은 Discord 서버의 "서버 설정 > 웹훅"에서 새로 만들고, 원하는 채널을 선택하면 얻을 수 있습니다. 전체 웹훅 URL을 `@discord` 디렉티브에 전달하면 됩니다.

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
<!-- ### Telegram -->
### Telegram

<!-- Envoy also supports sending notifications to [Telegram](https://telegram.org) after each task is executed. The `@telegram` directive accepts a Telegram Bot ID and a Chat ID. You may retrieve your Bot ID by creating a new bot using [BotFather](https://t.me/botfather). You can retrieve a valid Chat ID using [@username_to_id_bot](https://t.me/username_to_id_bot). You should pass the entire Bot ID and Chat ID into the `@telegram` directive: -->
Envoy는 [Telegram](https://telegram.org)으로도 태스크 실행 후 알림을 보낼 수 있습니다. `@telegram` 디렉티브에는 Telegram Bot ID와 Chat ID가 필요합니다. Bot ID는 [BotFather](https://t.me/botfather)로 새 봇을 생성하여 얻을 수 있고, 유효한 Chat ID는 [@username_to_id_bot](https://t.me/username_to_id_bot)을 이용해 확인할 수 있습니다. 이 둘을 `@telegram`에 넘깁니다.

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
<!-- ### Microsoft Teams -->
### Microsoft Teams

<!-- Envoy also supports sending notifications to [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams) after each task is executed. The `@microsoftTeams` directive accepts a Teams Webhook (required), a message, theme color (success, info, warning, error), and an array of options. You may retrieve your Teams Webhook by creating a new [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook). The Teams API has many other attributes to customize your message box like title, summary, and sections. You can find more information on the [Microsoft Teams documentation](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message). You should pass the entire Webhook URL into the `@microsoftTeams` directive: -->
Envoy는 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams)로도 태스크 실행 후 알림을 보낼 수 있습니다. `@microsoftTeams` 디렉티브에는 Teams Webhook(필수), 메시지, 테마 색상(success, info, warning, error), 옵션 배열을 인자로 받습니다. Teams Webhook은 [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)을 통해 얻을 수 있습니다. Teams API에서는 제목, 설명, 섹션 등 메시지 박스를 커스터마이징할 수 있는 다양한 속성을 제공하므로, 자세한 내용은 [Microsoft Teams documentation](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)를 참고하세요. 전체 Webhook URL을 `@microsoftTeams` 디렉티브에 전달합니다.

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```
