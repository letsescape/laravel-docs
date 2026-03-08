# Laravel Envoy

- [소개](#introduction)
- [설치](#installation)
- [작업 작성하기](#writing-tasks)
    - [작업 정의하기](#defining-tasks)
    - [서버 여러 대 사용하기](#multiple-servers)
    - [설정하기](#setup)
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

[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 실행하는 작업을 쉽게 수행하도록 도와주는 도구입니다. [Blade](/docs/12.x/blade) 스타일 문법을 사용하여 배포, Artisan 명령어 실행 등 다양한 작업을 간편하게 설정할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영체제만 지원하며, Windows 환경에서는 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 통해 사용 가능합니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 매니저를 사용하여 프로젝트에 Envoy를 설치하세요:

```shell
composer require laravel/envoy --dev
```

설치가 완료되면, Envoy 실행 파일이 애플리케이션의 `vendor/bin` 디렉터리에 생성됩니다:

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
## 작업 작성하기 (Writing Tasks)

<a name="defining-tasks"></a>
### 작업 정의하기 (Defining Tasks)

작업(Task)은 Envoy의 기본 단위로, 원격 서버에서 실행할 쉘 명령어를 정의합니다. 예를 들어, 모든 큐 작업자 서버에서 `php artisan queue:restart` 명령어를 실행하는 작업을 정의할 수 있습니다.

모든 Envoy 작업은 애플리케이션 루트에 `Envoy.blade.php` 파일에 정의해야 합니다. 다음은 기본 예제입니다:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

예제에서 볼 수 있듯 `@servers` 배열은 파일 상단에 정의되며, 작업 선언 시 `on` 옵션을 통해 참조합니다. `@servers` 선언은 반드시 한 줄로 작성해야 하며, `@task` 내에는 작업 실행 시 원격 서버에서 수행할 쉘 명령어를 작성합니다.

<a name="local-tasks"></a>
#### 로컬 작업 (Local Tasks)

로컬 컴퓨터에서 작업을 실행하려면 서버 IP를 `127.0.0.1`로 지정하면 됩니다:

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Envoy 작업 가져오기 (Importing Envoy Tasks)

`@import` 지시어를 사용하여 다른 Envoy 파일을 가져와, 해당 파일의 스토리와 작업들을 현재 파일에 추가할 수 있습니다. 가져온 후에는 해당 작업들을 마치 현재 파일에 정의된 것처럼 실행할 수 있습니다:

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### 서버 여러 대 사용하기 (Multiple Servers)

Envoy를 이용해 여러 서버에서 동시에 작업을 실행할 수 있습니다. 먼저 `@servers` 선언에 서버를 추가하고 각 서버에 고유 이름을 부여하세요. 그 다음 작업의 `on` 배열에 실행할 서버 이름들을 나열합니다:

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

기본적으로 작업은 서버 하나씩 순차적으로 실행됩니다. 첫 번째 서버에서 작업이 끝나야 두 번째 서버에서 실행을 시작합니다. 여러 서버에서 병렬로 작업을 실행하려면 작업 선언에 `parallel` 옵션을 추가하세요:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="setup"></a>
### 설정하기 (Setup)

Envoy 작업 실행 전에 임의 PHP 코드를 실행해야 할 때 `@setup` 지시어를 사용합니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

작업 실행 전에 다른 PHP 파일을 불러와야 한다면, `Envoy.blade.php` 파일 상단에 `@include` 지시어를 사용하세요:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### 변수 (Variables)

Envoy 작업 실행 시 명령줄에서 인수를 전달할 수 있습니다:

```shell
php vendor/bin/envoy run deploy --branch=master
```

작업 내에서는 Blade의 출력 구문을 이용해 옵션에 접근할 수 있으며, Blade `if` 문이나 반복문도 사용할 수 있습니다. 예를 들어 `$branch` 변수가 있을 때만 `git pull` 명령어를 실행하도록 할 수 있습니다:

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

스토리는 여러 작업을 하나의 이름 아래 그룹화한 것입니다. 예를 들어, `deploy` 스토리를 작성해 `update-code`와 `install-dependencies` 작업을 순서대로 실행할 수 있습니다:

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

스토리를 작성한 후에는 작업을 실행하는 것과 같은 방식으로 호출할 수 있습니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
### 후크 (Hooks)

작업과 스토리가 실행될 때 여러 후크가 실행됩니다. Envoy가 지원하는 후크 종류는 `@before`, `@after`, `@error`, `@success`, `@finished`가 있습니다. 모든 후크 내 코드는 PHP로 해석되며 로컬에서 실행되고, 원격 서버에서는 실행되지 않습니다.

필요한 만큼 여러 후크를 정의할 수 있으며, 작성된 순서대로 실행됩니다.

<a name="hook-before"></a>
#### `@before`

작업 실행 전에 등록된 모든 `@before` 후크가 실행됩니다. `@before` 후크는 실행될 작업 이름을 인수로 받습니다:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

작업 실행 후 등록된 모든 `@after` 후크가 실행됩니다. `@after` 후크는 실행된 작업 이름을 인수로 받습니다:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

작업이 실패했을 때(exit 상태 코드가 0보다 클 때) 등록된 모든 `@error` 후크가 실행됩니다. `@error` 후크는 실패한 작업 이름을 인수로 받습니다:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

모든 작업이 오류 없이 실행되었다면 등록된 모든 `@success` 후크가 실행됩니다:

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

모든 작업 실행 후 (종료 상태와 무관하게) 등록된 모든 `@finished` 후크가 실행됩니다. `@finished` 후크는 작업 종료 상태 코드(`null`이거나 0 이상 정수)를 인수로 받습니다:

```blade
@finished
    if ($exitCode > 0) {
        // 작업 중 오류가 있었습니다...
    }
@endfinished
```

<a name="running-tasks"></a>
## 작업 실행하기 (Running Tasks)

애플리케이션 `Envoy.blade.php` 파일에 정의된 작업 또는 스토리를 실행하려면 `run` 명령어에 실행할 이름을 전달하세요. Envoy는 작업을 실행하고 원격 서버에서 실행된 결과를 실시간으로 보여줍니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
### 작업 실행 확인 (Confirming Task Execution)

특정 작업 실행 전에 사용자에게 확인 메시지를 띄우고 싶다면, 작업 선언에 `confirm` 옵션을 추가하세요. 주로 파괴적인 작업에 유용합니다:

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

Envoy는 작업 실행 후 [Slack](https://slack.com)으로 알림을 보낼 수 있습니다. `@slack` 지시어는 Slack 웹훅 URL과 채널 또는 사용자 이름을 인수로 받습니다. Slack 제어판에서 "Incoming WebHooks" 통합을 만들어 웹훅 URL을 획득하세요.

`@slack` 지시어에 전체 웹훅 URL을 첫 번째 인수로 전달하고, 두 번째 인수로 채널명(`#channel`) 또는 사용자명(`@user`)을 작성하세요:

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

기본적으로 Envoy는 실행된 작업에 대한 메시지를 알림 채널로 전송합니다. 메시지를 커스텀하려면 세 번째 인수로 문자열을 넘기세요:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
### Discord

Envoy는 작업 완료 후 [Discord](https://discord.com)로도 알림을 보낼 수 있습니다. `@discord` 지시어는 Discord 웹훅 URL과 메시지를 받습니다. 서버 설정에서 "Webhook"을 생성하고, 어떤 채널에 게시할지 선택하여 웹훅 URL을 얻으세요. 전체 웹훅 URL을 `@discord` 지시어에 넘기면 됩니다:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
### Telegram

Envoy는 작업 완료 후 [Telegram](https://telegram.org)에도 알림을 보낼 수 있습니다. `@telegram` 지시어는 Telegram 봇 ID와 채팅 ID를 받습니다. [BotFather](https://t.me/botfather)를 통해 봇 ID를 생성하고, [@username_to_id_bot](https://t.me/username_to_id_bot)을 사용해 유효한 채팅 ID를 확인하세요. 두 값을 모두 `@telegram`에 전달해야 합니다:

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
### Microsoft Teams

Envoy는 작업 완료 후 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams)로 알림을 보낼 수 있습니다. `@microsoftTeams` 지시어는 필수로 Teams 웹훅 URL을 받고, 메시지, 테마 색상(success, info, warning, error) 및 옵션 배열을 인수로 받을 수 있습니다. Teams 제어판에서 [인바운드 웹훅](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)을 생성하여 웹훅 URL을 획득하세요. Teams API에는 제목, 요약, 섹션 등 메시지 박스를 세밀하게 커스터마이징할 수 있는 여러 속성이 있습니다. 자세한 내용은 [Microsoft Teams 문서](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)를 참고하세요.

전체 웹훅 URL을 다음과 같이 지시어에 넣어 사용하세요:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```