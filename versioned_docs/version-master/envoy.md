# Laravel Envoy

- [소개](#introduction)
- [설치](#installation)
- [작업 작성하기](#writing-tasks)
    - [작업 정의하기](#defining-tasks)
    - [다중 서버](#multiple-servers)
    - [설정](#setup)
    - [변수](#variables)
    - [스토리](#stories)
    - [후크](#completion-hooks)
- [작업 실행하기](#running-tasks)
    - [작업 실행 확인](#confirming-task-execution)
- [알림](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [Microsoft Teams](#microsoft-teams)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 실행하는 작업들을 자동으로 실행할 수 있게 도와주는 도구입니다. [Blade](/docs/master/blade) 스타일 문법을 사용하여 배포, Artisan 명령어 실행 등 다양한 작업을 손쉽게 구성할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영체제만 정식으로 지원하지만, [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 사용하면 Windows에서도 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 매니저를 사용해 프로젝트에 Envoy를 설치하세요:

```shell
composer require laravel/envoy --dev
```

Envoy 설치가 완료되면, Envoy 실행 파일은 애플리케이션의 `vendor/bin` 디렉토리 내에 위치하게 됩니다:

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
## 작업 작성하기 (Writing Tasks)

<a name="defining-tasks"></a>
### 작업 정의하기 (Defining Tasks)

작업(Task)은 Envoy의 기본 구성 단위로, 작업이 호출되었을 때 원격 서버에서 실행할 쉘 명령을 정의합니다. 예를 들어, 애플리케이션의 큐 작업 서버들에서 `php artisan queue:restart` 명령어를 실행하는 작업을 정의할 수 있습니다.

Envoy 작업들은 모두 애플리케이션 루트에 위치한 `Envoy.blade.php` 파일에 정의해야 합니다. 다음은 기본 예시입니다:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

위 예시를 보면, 파일 상단에 `@servers` 배열이 정의되어 있고, 이를 통해 `on` 옵션으로 작업이 실행될 서버를 지정할 수 있습니다. `@servers` 선언은 반드시 한 줄로 작성해야 하며, `@task` 블록 안에는 작업 실행 시 호출할 쉘 명령어들을 입력합니다.

<a name="local-tasks"></a>
#### 로컬 작업 (Local Tasks)

스크립트를 로컬 컴퓨터에서 실행하려면 서버 IP로 `127.0.0.1`을 지정하세요:

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Envoy 작업 불러오기 (Importing Envoy Tasks)

`@import` 지시어를 사용하면 다른 Envoy 파일을 가져와서, 그 파일 내의 스토리와 작업들을 현재 파일에 포함할 수 있습니다. 포함 후에는 마치 자신의 Envoy 파일에 작업이 정의된 것처럼 실행할 수 있습니다:

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### 다중 서버 (Multiple Servers)

Envoy는 한 작업을 여러 서버에서 쉽게 실행할 수 있도록 지원합니다. 먼저 `@servers` 선언에 추가 서버들을 이름과 함께 등록하세요. 그런 다음 작업의 `on` 옵션에 실행할 서버들 이름을 배열로 지정할 수 있습니다:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2']])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="parallel-execution"></a>
#### 병렬 실행 (Parallel Execution)

기본적으로 작업은 서버 별로 순차적으로 실행됩니다. 즉, 첫 번째 서버의 작업이 끝나야 두 번째 서버에서 작업이 실행됩니다. 여러 서버에서 병렬로 작업을 실행하고 싶다면, 작업 선언에 `parallel` 옵션을 `true`로 추가하세요:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="setup"></a>
### 설정 (Setup)

때로는 Envoy 작업을 실행하기 전에 임의의 PHP 코드를 실행해야 할 때가 있습니다. `@setup` 지시어를 사용하여 작업 실행 전에 실행할 PHP 코드를 정의할 수 있습니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

만약 작업 실행 전에 다른 PHP 파일들을 불러와야 한다면, `Envoy.blade.php` 파일 상단에 `@include` 지시어를 사용하세요:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### 변수 (Variables)

필요에 따라 Envoy 작업에 명령줄 인수를 넘겨줄 수 있습니다. 작업을 실행할 때 옵션을 지정해 전달하세요:

```shell
php vendor/bin/envoy run deploy --branch=master
```

작업 내에서는 Blade의 출력 구문을 사용해 인수에 접근할 수 있으며, 조건문이나 반복문도 자유롭게 작성할 수 있습니다. 예를 들어, `$branch` 변수 존재 여부를 확인 후 `git pull` 명령을 실행할 수 있습니다:

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
### 스토리 (Stories)

스토리는 여러 작업을 하나의 이름 아래 묶어 편리하게 실행할 수 있도록 하는 개념입니다. 예를 들어, `deploy` 스토리는 `update-code`와 `install-dependencies` 작업을 순서대로 실행할 수 있습니다:

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

스토리를 정의한 후에는 작업 실행과 동일하게 실행할 수 있습니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
### 후크 (Hooks)

작업과 스토리가 실행될 때 여러 후크가 작동할 수 있습니다. Envoy가 지원하는 후크는 `@before`, `@after`, `@error`, `@success`, 그리고 `@finished`입니다. 이 후크들에 작성한 코드는 모두 PHP로 해석되며, 작업이 실행되는 원격 서버가 아닌 로컬 환경에서 실행됩니다.

각 후크는 여러 번 정의할 수 있으며, Envoy 스크립트에 등장한 순서대로 실행됩니다.

<a name="hook-before"></a>
#### `@before`

작업 실행 전에 Envoy 스크립트 내에 등록된 모든 `@before` 후크가 실행됩니다. 후크는 실행될 작업 이름을 인수로 받습니다:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

작업 실행 후에 Envoy 스크립트 내에 등록된 모든 `@after` 후크가 실행됩니다. 후크는 실행이 완료된 작업 이름을 인수로 받습니다:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

작업이 실패하여 종료 코드가 `0`보다 클 때마다, 스크립트 내에 등록된 모든 `@error` 후크가 실행됩니다. 후크는 실패한 작업 이름을 인수로 받습니다:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

모든 작업이 오류 없이 성공적으로 실행되면, Envoy 스크립트 내에 등록된 모든 `@success` 후크가 실행됩니다:

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

모든 작업이 종료된 후(종료 상태 코드에 관계없이) 모든 `@finished` 후크가 실행됩니다. 후크는 작업의 종료 코드를 인수로 받는데, 이는 `null`이거나 `0` 이상의 정수일 수 있습니다:

```blade
@finished
    if ($exitCode > 0) {
        // 작업 중 오류가 있었습니다...
    }
@endfinished
```

<a name="running-tasks"></a>
## 작업 실행하기 (Running Tasks)

애플리케이션의 `Envoy.blade.php` 파일에 정의된 작업이나 스토리를 실행하려면, Envoy의 `run` 명령어 뒤에 실행할 작업이나 스토리 이름을 전달하세요. Envoy는 작업을 실행하며, 원격 서버에서 출력되는 결과를 실시간으로 보여줍니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
### 작업 실행 확인 (Confirming Task Execution)

서버에서 특정 작업을 실행하기 전에 실행 여부를 사용자에게 물어보도록 하려면, 작업 선언에 `confirm` 지시어를 추가하세요. 이는 특히 위험하거나 파괴적인 작업일 때 유용합니다:

```blade
@task('deploy', ['on' => 'web', 'confirm' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate
@endtask
```

<a name="notifications"></a>
## 알림 (Notifications)

<a name="slack"></a>
### Slack

Envoy는 작업 실행 후 [Slack](https://slack.com)으로 알림을 보낼 수 있습니다. `@slack` 지시어는 Slack 웹훅 URL과 채널 또는 사용자 이름을 인수로 받습니다. 웹훅 URL은 Slack 관리 콘솔에서 "Incoming WebHooks" 통합을 생성해 얻을 수 있습니다.

`@slack`에 첫 번째 인수로는 전체 웹훅 URL을, 두 번째 인수로는 채널명(`#channel`) 또는 사용자명(`@user`)을 전달하세요:

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

기본적으로 알림 메시지는 실행한 작업을 설명하지만, 세 번째 인수를 전달하여 사용자 정의 메시지로 덮어쓸 수 있습니다:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
### Discord

Envoy는 작업 후 [Discord](https://discord.com)로도 알림을 보낼 수 있습니다. `@discord` 지시어는 Discord 웹훅 URL과 메시지를 인수로 받습니다. 웹훅 URL은 Discord 서버 설정에서 "Webhook"을 생성하여 얻을 수 있습니다. `@discord`에 전체 웹훅 URL을 넘기면 됩니다:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
### Telegram

Envoy는 작업 후 [Telegram](https://telegram.org)으로도 알림을 전송합니다. `@telegram` 지시어는 Telegram 봇 ID와 채팅 ID를 인수로 받습니다. 봇 ID는 [BotFather](https://t.me/botfather)를 통해 새 봇을 생성하면 얻을 수 있고, 유효한 채팅 ID는 [@username_to_id_bot](https://t.me/username_to_id_bot)을 통해 알 수 있습니다. `@telegram` 에는 봇 ID와 채팅 ID를 모두 전체 문자열로 전달하세요:

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
### Microsoft Teams

Envoy는 작업 실행 후 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams)로도 알림을 보낼 수 있습니다. `@microsoftTeams` 지시어는 Teams 웹훅 URL(필수), 메시지, 테마 색상(success, info, warning, error), 그리고 옵션 배열을 인수로 받습니다. Teams 웹훅은 [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)을 생성해 얻을 수 있습니다. Teams API는 알림 박스의 제목, 요약, 섹션 등 다양한 커스터마이징 옵션을 제공합니다. 자세한 내용은 [Microsoft Teams 문서](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)를 참고하세요. `@microsoftTeams`에는 전체 웹훅 URL을 전달합니다:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```