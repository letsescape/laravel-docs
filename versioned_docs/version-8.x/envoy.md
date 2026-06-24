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

<!-- [Laravel Envoy](https://github.com/laravel/envoy) is a tool for executing common tasks you run on your remote servers. Using [Blade](/docs/8.x/blade) style syntax, you can easily setup tasks for deployment, Artisan commands, and more. Currently, Envoy only supports the Mac and Linux operating systems. However, Windows support is achievable using [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10). -->
[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 수행하는 작업을 손쉽게 실행할 수 있게 도와주는 도구입니다. [Blade](/docs/8.x/blade) 스타일의 문법을 활용하여 배포, Artisan 명령어 실행 등 다양한 작업을 간편하게 정의할 수 있습니다. 현재 엔보이는 Mac과 Linux 운영체제만 지원합니다. 하지만 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 사용하면 Windows에서도 사용할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install Envoy into your project using the Composer package manager: -->
우선, Composer 패키지 관리자를 이용해 프로젝트에 엔보이를 설치합니다:

```
composer require laravel/envoy --dev
```

<!-- Once Envoy has been installed, the Envoy binary will be available in your application's `vendor/bin` directory: -->
엔보이 설치가 완료되면, 애플리케이션의 `vendor/bin` 디렉터리에서 엔보이 실행 파일을 사용할 수 있습니다:


<!--     php vendor/bin/envoy -->
    php vendor/bin/envoy


<a name="writing-tasks"></a>
<!-- ## Writing Tasks -->
## Writing Tasks

<a name="defining-tasks"></a>
<!-- ### Defining Tasks -->
### Defining Tasks

<!-- Tasks are the basic building block of Envoy. Tasks define the shell commands that should execute on your remote servers when the task is invoked. For example, you might define a task that executes the `php artisan queue:restart` command on all of your application's queue worker servers. -->
작업(Task)은 엔보이의 기본 단위입니다. 작업은 해당 작업이 호출될 때 원격 서버에서 어떤 셸 명령어를 실행할지 정의합니다. 예를 들어, 모든 큐 워커 서버에서 `php artisan queue:restart` 명령어를 실행하는 작업을 만들 수도 있습니다.

<!-- All of your Envoy tasks should be defined in an `Envoy.blade.php` file at the root of your application. Here's an example to get you started: -->
모든 엔보이 작업은 애플리케이션 루트에 위치한 `Envoy.blade.php` 파일에 정의해야 합니다. 아래는 간단한 예시입니다:

```bash
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

<!-- As you can see, an array of `@servers` is defined at the top of the file, allowing you to reference these servers via the `on` option of your task declarations. The `@servers` declaration should always be placed on a single line. Within your `@task` declarations, you should place the shell commands that should execute on your servers when the task is invoked. -->
위 예시에서 볼 수 있듯, 파일 상단에 `@servers` 배열을 정의해서 작업 선언의 `on` 옵션에서 해당 서버를 참조할 수 있습니다. `@servers` 선언은 반드시 한 줄로 작성해야 합니다. 각 `@task` 선언 내부에는 해당 작업이 실행될 때 서버에서 실행할 셸 명령어를 작성합니다.

<a name="local-tasks"></a>
<!-- #### Local Tasks -->
#### Local Tasks

<!-- You can force a script to run on your local computer by specifying the server's IP address as `127.0.0.1`: -->
서버의 IP 주소를 `127.0.0.1`로 지정하면, 스크립트를 로컬 컴퓨터에서 강제로 실행할 수 있습니다:

```bash
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
<!-- #### Importing Envoy Tasks -->
#### Importing Envoy Tasks

<!-- Using the `@import` directive, you may import other Envoy files so their stories and tasks are added to yours. After the files have been imported, you may execute the tasks they contain as if they were defined in your own Envoy file: -->
`@import` 지시어를 이용하면 다른 엔보이 파일을 가져와서 그 안의 스토리와 작업을 현재 파일에서 사용할 수 있습니다. 가져온 후에는, 자신의 Envoy 파일에서 정의한 것처럼 해당 작업을 실행할 수 있습니다:

```bash
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
<!-- ### Multiple Servers -->
### Multiple Servers

<!-- Envoy allows you to easily run a task across multiple servers. First, add additional servers to your `@servers` declaration. Each server should be assigned a unique name. Once you have defined your additional servers you may list each of the servers in the task's `on` array: -->
엔보이를 이용하면 한 번에 여러 서버에서 작업을 손쉽게 실행할 수 있습니다. 우선 `@servers` 선언에 추가로 여러 서버를 등록하세요. 각 서버는 고유한 이름을 가져야 합니다. 이후, 작업의 `on` 배열에 여러 서버 이름을 나열하면 됩니다:

```bash
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
기본적으로, 작업은 각 서버에서 순차적으로(직렬로) 실행됩니다. 즉, 첫 번째 서버에서 작업이 끝난 후 두 번째 서버에서 작업이 시작됩니다. 여러 서버에서 작업을 병렬로 실행하고 싶다면, 작업 선언에 `parallel` 옵션을 추가하면 됩니다:

```bash
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
특정 작업을 실행하기 전에 임의의 PHP 코드를 실행해야 할 경우, `@setup` 지시어를 사용하여 그러한 코드를 작성할 수 있습니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

<!-- If you need to require other PHP files before your task is executed, you may use the `@include` directive at the top of your `Envoy.blade.php` file: -->
작업 실행 전 다른 PHP 파일을 불러와야 할 경우, `Envoy.blade.php` 파일 상단에 `@include` 지시어를 사용할 수 있습니다:

```bash
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
<!-- ### Variables -->
### Variables

<!-- If needed, you may pass arguments to Envoy tasks by specifying them on the command line when invoking Envoy: -->
필요하다면, Envoy 작업에 인수를 커맨드라인에서 전달할 수 있습니다:


<!--     php vendor/bin/envoy run deploy --branch=master -->
    php vendor/bin/envoy run deploy --branch=master


<!-- You may access the options within your tasks using Blade's "echo" syntax. You may also define Blade `if` statements and loops within your tasks. For example, let's verify the presence of the `$branch` variable before executing the `git pull` command: -->
작업 내부에서는 Blade의 "echo" 문법을 사용해 옵션에 접근할 수 있습니다. 또한 작업 내에서 Blade의 `if` 문이나 반복문 등도 자유롭게 사용할 수 있습니다. 예를 들어, `git pull` 명령 실행 전 `$branch` 변수가 존재하는지 확인할 수 있습니다:

```bash
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
스토리는 여러 작업을 하나의 이름 아래에 묶어 한 번에 실행할 수 있는 기능입니다. 예를 들어, `deploy`라는 스토리는 `update-code`와 `install-dependencies` 작업을 순서대로 실행할 수 있습니다:

```bash
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
스토리를 정의했다면, 작업 실행과 동일하게 아래와 같이 호출할 수 있습니다:


<!--     php vendor/bin/envoy run deploy -->
    php vendor/bin/envoy run deploy


<a name="completion-hooks"></a>
<!-- ### Hooks -->
### Hooks

<!-- When tasks and stories run, a number of hooks are executed. The hook types supported by Envoy are `@before`, `@after`, `@error`, `@success`, and `@finished`. All of the code in these hooks is interpreted as PHP and executed locally, not on the remote servers that your tasks interact with. -->
작업과 스토리가 실행될 때, 여러 종류의 후크(Hook)가 사용될 수 있습니다. 엔보이에서 지원하는 후크 유형에는 `@before`, `@after`, `@error`, `@success`, `@finished`가 있습니다. 이러한 후크에서 작성한 모든 코드는 PHP로 해석되며 원격 서버가 아니라 로컬에서 실행됩니다.

<!-- You may define as many of each of these hooks as you like. They will be executed in the order that they appear in your Envoy script. -->
각 후크 유형은 필요에 따라 원하는 만큼 정의할 수 있으며, Envoy 스크립트 내 작성된 순서대로 실행됩니다.

<a name="hook-before"></a>
<!-- #### `@before` -->
#### `@before`

<!-- Before each task execution, all of the `@before` hooks registered in your Envoy script will execute. The `@before` hooks receive the name of the task that will be executed: -->
각 작업 실행 전에, Envoy 스크립트에 등록된 모든 `@before` 후크가 실행됩니다. `@before` 내에서는 실행 예정인 작업의 이름을 받을 수 있습니다:

```php
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
각 작업 실행이 끝난 후, Envoy 스크립트에 등록된 모든 `@after` 후크가 실행됩니다. `@after` 후크는 실행 완료된 작업의 이름을 전달받습니다:

```php
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
작업이 실패(종료 코드가 `0`보다 큰 경우)할 때마다 Envoy 스크립트에 등록된 모든 `@error` 후크가 실행됩니다. `@error` 후크는 실행된 작업의 이름을 전달받습니다:

```php
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
모든 작업이 오류 없이 정상적으로 실행되었다면, Envoy 스크립트에 등록된 모든 `@success` 후크가 실행됩니다:

```bash
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
<!-- #### `@finished` -->
#### `@finished`

<!-- After all tasks have been executed (regardless of exit status), all of the `@finished` hooks will be executed. The `@finished` hooks receive the status code of the completed task, which may be `null` or an `integer` greater than or equal to `0`: -->
모든 작업의 실행이 끝나면(성공 여부와 관계없이) 모든 `@finished` 후크가 실행됩니다. `@finished` 후크는 완료된 작업의 상태 코드를 전달받으며, 이 값은 `null` 또는 `0` 이상의 `integer`일 수 있습니다:

```bash
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
애플리케이션의 `Envoy.blade.php` 파일에 정의된 작업 또는 스토리를 실행하려면, Envoy의 `run` 명령어에 실행할 작업이나 스토리 이름을 전달하세요. Envoy는 해당 작업을 실행한 후, 실행 과정에서 원격 서버에서 발생하는 출력을 실시간으로 표시해줍니다:


<!--     php vendor/bin/envoy run deploy -->
    php vendor/bin/envoy run deploy


<a name="confirming-task-execution"></a>
<!-- ### Confirming Task Execution -->
### Confirming Task Execution

<!-- If you would like to be prompted for confirmation before running a given task on your servers, you should add the `confirm` directive to your task declaration. This option is particularly useful for destructive operations: -->
특정 작업을 서버에서 실행하기 전에 확인(프롬프트)이 있도록 하려면, 작업 선언에 `confirm` 옵션을 추가하면 됩니다. 이 옵션은 파괴적인 작업에 특히 유용합니다:

```bash
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
엔보이는 모든 작업이 실행된 후 [Slack](https://slack.com)으로 알림을 보낼 수 있습니다. `@slack` 지시어는 Slack 훅(hook) URL과 채널 또는 사용자 이름을 인자로 받습니다. Slack 관리 패널에서 "Incoming WebHooks" 통합을 생성해 Webhook URL을 얻을 수 있습니다.

<!-- You should pass the entire webhook URL as the first argument given to the `@slack` directive. The second argument given to the `@slack` directive should be a channel name (`#channel`) or a user name (`@user`): -->
`@slack` 지시어의 첫 번째 인수로 전체 Webhook URL을 전달해야 합니다. `@slack` 지시어의 두 번째 인수로는 채널명(`#channel`) 또는 사용자명(`@user`)을 전달해야 합니다:

```
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

<!-- By default, Envoy notifications will send a message to the notification channel describing the task that was executed. However, you may overwrite this message with your own custom message by passing a third argument to the `@slack` directive: -->
기본적으로, 엔보이 알림은 실행된 작업을 설명하는 메시지를 알림 채널로 전송합니다. 하지만 `@slack` 지시어에 세 번째 인수로 직접 작성한 메시지를 전달하면 이 메시지를 덮어쓸 수 있습니다:

```
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
<!-- ### Discord -->
### Discord

<!-- Envoy also supports sending notifications to [Discord](https://discord.com) after each task is executed. The `@discord` directive accepts a Discord hook URL and a message. You may retrieve your webhook URL by creating a "Webhook" in your Server Settings and choosing which channel the webhook should post to. You should pass the entire Webhook URL into the `@discord` directive: -->
엔보이는 모든 작업이 실행된 후 [Discord](https://discord.com)로도 알림을 보낼 수 있습니다. `@discord` 지시어는 Discord Webhook URL과 메시지를 인자로 받습니다. Server Settings에서 "Webhook"을 생성하고, Webhook이 게시될 채널을 선택해 Webhook URL을 얻을 수 있습니다. 전체 Webhook URL을 `@discord` 지시어에 전달하면 됩니다:

```
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
<!-- ### Telegram -->
### Telegram

<!-- Envoy also supports sending notifications to [Telegram](https://telegram.org) after each task is executed. The `@telegram` directive accepts a Telegram Bot ID and a Chat ID. You may retrieve your Bot ID by creating a new bot using [BotFather](https://t.me/botfather). You can retrieve a valid Chat ID using [@username_to_id_bot](https://t.me/username_to_id_bot). You should pass the entire Bot ID and Chat ID into the `@telegram` directive: -->
엔보이는 모든 작업 실행 후 [Telegram](https://telegram.org)으로도 알림을 전송할 수 있습니다. `@telegram` 지시어는 Telegram 봇 ID와 채팅 ID를 인자로 받습니다. [BotFather](https://t.me/botfather)로 새 봇을 생성해 봇 ID를 얻을 수 있으며, [@username_to_id_bot](https://t.me/username_to_id_bot)을 사용하면 유효한 채팅 ID를 구할 수 있습니다. 두 인자를 모두 `@telegram` 지시어에 넣어 사용하세요:

```
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
<!-- ### Microsoft Teams -->
### Microsoft Teams

<!-- Envoy also supports sending notifications to [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams) after each task is executed. The `@microsoftTeams` directive accepts a Teams Webhook (required), a message, theme color (success, info, warning, error), and an array of options. You may retrieve your Teams Webook by creating a new [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook). The Teams API has many other attributes to customize your message box like title, summary, and sections. You can find more information on the [Microsoft Teams documentation](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message). You should pass the entire Webhook URL into the `@microsoftTeams` directive: -->
엔보이는 모든 작업 실행 후 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams)로도 알림을 보낼 수 있습니다. `@microsoftTeams` 지시어는 필수로 Teams Webhook과 메시지, 테마 색상(success, info, warning, error), 그리고 옵션 배열을 받을 수 있습니다. Teams Webhook은 [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)을 새로 만들어 얻을 수 있습니다. Teams API는 메시지 박스를 수정할 수 있는 title, summary, sections와 같은 여러 속성을 지원합니다. 더 자세한 내용은 [Microsoft Teams documentation](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)에서 확인할 수 있습니다. 전체 Webhook URL을 `@microsoftTeams` 지시어에 전달하도록 하세요:

```
@finished
    @microsoftTeams('webhook-url')
@endfinished
```
