<!-- # Configuration -->
# Configuration

- [Introduction](#introduction)
- [Environment Configuration](#environment-configuration)
    - [Environment Variable Types](#environment-variable-types)
    - [Retrieving Environment Configuration](#retrieving-environment-configuration)
    - [Determining The Current Environment](#determining-the-current-environment)
- [Accessing Configuration Values](#accessing-configuration-values)
- [Configuration Caching](#configuration-caching)
- [Debug Mode](#debug-mode)
- [Maintenance Mode](#maintenance-mode)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you. -->
Laravel 프레임워크의 모든 설정 파일은 `config` 디렉토리에 저장되어 있습니다. 각 옵션에는 문서가 작성되어 있으니, 파일을 살펴보면서 어떤 옵션들이 있는지 익숙해지면 좋습니다.

<!-- These configuration files allow you to configure things like your database connection information, your mail server information, as well as various other core configuration values such as your application timezone and encryption key. -->
이 설정 파일들을 통해 데이터베이스 연결 정보, 메일 서버 정보뿐만 아니라 애플리케이션의 타임존, 암호화 키 등 핵심 설정 값도 구성할 수 있습니다.

<a name="environment-configuration"></a>
<!-- ## Environment Configuration -->
## Environment Configuration

<!-- It is often helpful to have different configuration values based on the environment where the application is running. For example, you may wish to use a different cache driver locally than you do on your production server. -->
애플리케이션이 실행되는 환경에 따라 서로 다른 설정 값이 필요할 때가 많습니다. 예를 들어, 로컬에서는 실제 운영 서버와는 다른 캐시 드라이버를 사용하고 싶을 수 있습니다.

<!-- To make this a cinch, Laravel utilizes the [DotEnv](https://github.com/vlucas/phpdotenv) PHP library. In a fresh Laravel installation, the root directory of your application will contain a `.env.example` file that defines many common environment variables. During the Laravel installation process, this file will automatically be copied to `.env`. -->
이런 작업을 간편하게 하기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 사용합니다. 새롭게 Laravel을 설치하면, 애플리케이션의 루트 디렉토리에 `.env.example` 파일이 생성되어 다양한 환경 변수가 정의되어 있습니다. Laravel 설치 과정에서는 이 파일이 자동으로 `.env` 파일로 복사됩니다.

<!-- Laravel's default `.env` file contains some common configuration values that may differ based on whether your application is running locally or on a production web server. These values are then retrieved from various Laravel configuration files within the `config` directory using Laravel's `env` function. -->
Laravel의 기본 `.env` 파일에는 로컬 환경과 운영 웹 서버 환경에 따라 달라질 수 있는 몇 가지 일반적인 설정 값들이 들어 있습니다. 이 값들은 Laravel의 `env` 함수를 통해 `config` 디렉토리 내의 다양한 설정 파일에서 사용됩니다.

<!-- If you are developing with a team, you may wish to continue including a `.env.example` file with your application. By putting placeholder values in the example configuration file, other developers on your team can clearly see which environment variables are needed to run your application. -->
여러 명이 함께 개발을 한다면, 애플리케이션에 `.env.example` 파일을 계속 포함하고 관리하는 것을 추천합니다. 예시 파일에 플레이스홀더 값을 적어두면, 팀의 다른 개발자들도 애플리케이션을 실행하는 데 필요한 환경 변수를 쉽게 확인할 수 있습니다.

> [!TIP]
> `.env` 파일의 어떤 변수든 서버 환경 변수나 시스템 환경 변수 등 외부 환경 변수로 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
<!-- #### Environment File Security -->
#### Environment File Security

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed. -->
`.env` 파일은 애플리케이션의 소스 코드 저장소에 커밋해서는 안 됩니다. 개발자, 서버별로 서로 다른 환경 설정이 필요할 수 있기 때문입니다. 또한, 누군가가 소스 저장소에 접근하게 될 경우, 중요한 인증 정보들이 노출될 위험이 있으니 주의해야 합니다.

<a name="additional-environment-files"></a>
<!-- #### Additional Environment Files -->
#### Additional Environment Files

<!-- Before loading your application's environment variables, Laravel determines if either the `APP_ENV` environment variable has been externally provided or if the `--env` CLI argument has been specified. If so, Laravel will attempt to load an `.env.[APP_ENV]` file if it exists. If it does not exist, the default `.env` file will be loaded. -->
애플리케이션의 환경 변수를 로드하기 전에, Laravel은 `APP_ENV` 환경 변수가 외부에서 지정되었는지 또는 `--env` CLI 인자가 전달되었는지를 확인합니다. 이 경우 해당되는 `.env.[APP_ENV]` 파일이 있으면 이를 읽어옵니다. 파일이 없다면 기본 `.env` 파일을 사용합니다.

<a name="environment-variable-types"></a>
<!-- ### Environment Variable Types -->
### Environment Variable Types

<!-- All variables in your `.env` files are typically parsed as strings, so some reserved values have been created to allow you to return a wider range of types from the `env()` function: -->
`.env` 파일에 있는 모든 변수는 일반적으로 문자열로 해석됩니다. 하지만 `env()` 함수가 더 다양한 타입을 반환할 수 있도록 아래와 같은 예약어가 만들어져 있습니다:

<!--
`.env` Value  | `env()` Value
------------- | -------------
true | (bool) true
(true) | (bool) true
false | (bool) false
(false) | (bool) false
empty | (string) ''
(empty) | (string) ''
null | (null) null
(null) | (null) null
-->
`.env` 값  | `env()` 반환값
------------- | -------------
true | (bool) true
(true) | (bool) true
false | (bool) false
(false) | (bool) false
empty | (string) ''
(empty) | (string) ''
null | (null) null
(null) | (null) null

<!-- If you need to define an environment variable with a value that contains spaces, you may do so by enclosing the value in double quotes: -->
값에 공백이 포함된 환경 변수를 정의하려면, 값을 큰따옴표로 감싸면 됩니다:

```
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
<!-- ### Retrieving Environment Configuration -->
### Retrieving Environment Configuration

<!-- All of the variables listed in this file will be loaded into the `$_ENV` PHP super-global when your application receives a request. However, you may use the `env` helper to retrieve values from these variables in your configuration files. In fact, if you review the Laravel configuration files, you will notice many of the options are already using this helper: -->
이 파일에 나열된 모든 변수는 애플리케이션에 요청이 들어오면 `$_ENV` PHP 슈퍼글로벌에 로드됩니다. 설정 파일에서는 `env` 헬퍼로 해당 변수의 값을 가져올 수 있습니다. 실제로 Laravel 설정 파일들을 보면 많은 옵션이 이미 이 헬퍼를 사용하고 있음을 알 수 있습니다:

```
'debug' => env('APP_DEBUG', false),
```

<!-- The second value passed to the `env` function is the "default value". This value will be returned if no environment variable exists for the given key. -->
`env` 함수의 두 번째 인자는 "기본값"으로, 지정한 키에 해당하는 환경 변수가 없을 때 반환됩니다.

<a name="determining-the-current-environment"></a>
<!-- ### Determining The Current Environment -->
### Determining The Current Environment

<!-- The current application environment is determined via the `APP_ENV` variable from your `.env` file. You may access this value via the `environment` method on the `App` [facade](/docs/8.x/facades): -->
현재 애플리케이션의 환경은 `.env` 파일의 `APP_ENV` 변수를 통해 결정됩니다. 이 값은 `App` [facade](/docs/8.x/facades)의 `environment` 메서드를 통해 가져올 수 있습니다:

```
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

<!-- You may also pass arguments to the `environment` method to determine if the environment matches a given value. The method will return `true` if the environment matches any of the given values: -->
또한, `environment` 메서드에 인자를 전달해 현재 환경이 주어진 값과 일치하는지 확인할 수 있습니다. 이 메서드는 환경이 인자로 전달한 값 중 하나와 일치하면 `true`를 반환합니다:

```
if (App::environment('local')) {
    // The environment is local
}

if (App::environment(['local', 'staging'])) {
    // The environment is either local OR staging...
}
```

> [!TIP]
> 현재 애플리케이션 환경은 서버 레벨의 `APP_ENV` 환경 변수를 설정해서 덮어쓸 수 있습니다.

<a name="accessing-configuration-values"></a>
<!-- ## Accessing Configuration Values -->
## Accessing Configuration Values

<!-- You may easily access your configuration values using the global `config` helper function from anywhere in your application. The configuration values may be accessed using "dot" syntax, which includes the name of the file and option you wish to access. A default value may also be specified and will be returned if the configuration option does not exist: -->
애플리케이션 어느 곳에서든 글로벌 `config` 헬퍼 함수를 통해 설정 값을 쉽게 가져올 수 있습니다. 파일 이름과 옵션 이름을 "dot" 구문(점 표기법)으로 지정하면 됩니다. 만약 해당 설정 옵션이 없다면 기본값도 지정해서 사용할 수 있습니다:

```
$value = config('app.timezone');

// Retrieve a default value if the configuration value does not exist...
$value = config('app.timezone', 'Asia/Seoul');
```

<!-- To set configuration values at runtime, pass an array to the `config` helper: -->
런타임에 설정 값을 변경하려면, 배열을 `config` 헬퍼에 전달하면 됩니다:

```
config(['app.timezone' => 'America/Chicago']);
```

<a name="configuration-caching"></a>
<!-- ## Configuration Caching -->
## Configuration Caching

<!-- To give your application a speed boost, you should cache all of your configuration files into a single file using the `config:cache` Artisan command. This will combine all of the configuration options for your application into a single file which can be quickly loaded by the framework. -->
애플리케이션의 성능을 높이기 위해, `config:cache` 아티즌 명령어를 사용해 모든 설정 파일을 하나의 파일로 캐싱할 수 있습니다. 이 명령은 애플리케이션의 모든 설정 값을 하나의 파일로 합쳐 프레임워크가 빠르게 로드할 수 있게 해줍니다.

<!-- You should typically run the `php artisan config:cache` command as part of your production deployment process. The command should not be run during local development as configuration options will frequently need to be changed during the course of your application's development. -->
보통 운영 서버에 배포할 때 `php artisan config:cache` 명령어를 실행해야 합니다. 개발 중에는 설정 값이 자주 변경될 수 있으므로, 이 명령어를 사용하지 않는 것이 좋습니다.

> [!NOTE]
> 배포 과정에서 `config:cache` 명령어를 실행했다면, 반드시 환경 변수 접근은 설정 파일 내부에서만 `env` 함수를 호출해야 합니다. 설정이 캐싱되면 `.env` 파일 자체는 더 이상 로드되지 않기 때문에, `env` 함수는 오직 외부 시스템 환경 변수만 반환합니다.

<a name="debug-mode"></a>
<!-- ## Debug Mode -->
## Debug Mode

<!-- The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file. -->
`config/app.php` 설정 파일의 `debug` 옵션은 사용자에게 오류 정보를 얼마나 보여줄지 결정합니다. 기본적으로, 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

<!-- For local development, you should set the `APP_DEBUG` environment variable to `true`. **In your production environment, this value should always be `false`. If the variable is set to `true` in production, you risk exposing sensitive configuration values to your application's end users.** -->
로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 반드시 `true`로 설정해야 합니다. **운영 환경에서는 이 값을 반드시 `false`로 두어야 하며, 만약 운영 환경에서 `true`로 되어 있다면 중요한 설정 값이 사용자에게 노출될 수 있으니 매우 주의해야 합니다.**

<a name="maintenance-mode"></a>
<!-- ## Maintenance Mode -->
## Maintenance Mode

<!-- When your application is in maintenance mode, a custom view will be displayed for all requests into your application. This makes it easy to "disable" your application while it is updating or when you are performing maintenance. A maintenance mode check is included in the default middleware stack for your application. If the application is in maintenance mode, a `Symfony\Component\HttpKernel\Exception\HttpException` instance will be thrown with a status code of 503. -->
애플리케이션이 유지보수 모드에 들어가면, 모든 요청에 대해 커스텀 뷰가 표시됩니다. 이를 통해 애플리케이션을 업데이트하거나 점검할 때 일시적으로 "비활성화"시킬 수 있습니다. 유지보수 모드 체크는 기본 미들웨어 스택에 포함되어 있으며, 유지보수 모드에서는 `Symfony\Component\HttpKernel\Exception\HttpException`이 503 상태 코드로 발생합니다.

<!-- To enable maintenance mode, execute the `down` Artisan command: -->
유지보수 모드를 활성화하려면 다음처럼 `down` 아티즌 명령어를 실행하세요:

```
php artisan down
```

<!-- If you would like the `Refresh` HTTP header to be sent with all maintenance mode responses, you may provide the `refresh` option when invoking the `down` command. The `Refresh` header will instruct the browser to automatically refresh the page after the specified number of seconds: -->
모든 유지보수 모드 응답에 `Refresh` HTTP 헤더를 추가하려면, `down` 명령 실행 시 `refresh` 옵션을 사용할 수 있습니다. `Refresh` 헤더는 브라우저가 지정된 초 이후 자동으로 페이지를 새로고침하도록 안내합니다:

```
php artisan down --refresh=15
```

<!-- You may also provide a `retry` option to the `down` command, which will be set as the `Retry-After` HTTP header's value, although browsers generally ignore this header: -->
또한 `down` 명령어에 `retry` 옵션을 지정하면, 해당 값이 `Retry-After` HTTP 헤더로 설정됩니다. 다만 대부분의 브라우저는 이 헤더를 무시합니다:

```
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
<!-- #### Bypassing Maintenance Mode -->
#### Bypassing Maintenance Mode

<!-- Even while in maintenance mode, you may use the `secret` option to specify a maintenance mode bypass token: -->
유지보수 모드에서도, `secret` 옵션을 사용하면 유지보수 모드를 우회할 토큰을 지정할 수 있습니다:

```
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

<!-- After placing the application in maintenance mode, you may navigate to the application URL matching this token and Laravel will issue a maintenance mode bypass cookie to your browser: -->
애플리케이션이 유지보수 모드인 상태에서 이 토큰에 해당하는 URL로 접속하면, Laravel이 브라우저에 유지보수 모드 우회 쿠키를 발급해줍니다:

<!--     https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515 -->
    https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515

<!-- When accessing this hidden route, you will then be redirected to the `/` route of the application. Once the cookie has been issued to your browser, you will be able to browse the application normally as if it was not in maintenance mode. -->
이 숨겨진 경로에 접근하면 애플리케이션의 `/` 경로로 리디렉션됩니다. 일단 쿠키가 발급되면 애플리케이션이 유지보수 모드여도 평소처럼 접근할 수 있습니다.

> [!TIP]
> 유지보수 모드 시크릿(우회 토큰)은 알파벳, 숫자, 대시(-)로 구성하는 것이 좋습니다. `?`, `&` 등 URL에서 특별한 의미가 있는 문자는 피해야 합니다.

<a name="pre-rendering-the-maintenance-mode-view"></a>
<!-- #### Pre-Rendering The Maintenance Mode View -->
#### Pre-Rendering The Maintenance Mode View

<!-- If you utilize the `php artisan down` command during deployment, your users may still occasionally encounter errors if they access the application while your Composer dependencies or other infrastructure components are updating. This occurs because a significant part of the Laravel framework must boot in order to determine your application is in maintenance mode and render the maintenance mode view using the templating engine. -->
배포 중에 `php artisan down` 명령을 사용하는 경우, 사용자가 Composer 의존성이나 기타 인프라가 업데이트될 때 애플리케이션에 접속하면 때로는 오류가 발생할 수 있습니다. 이는 Laravel 프레임워크의 주요 부분이 유지보수 모드 여부를 판단하고 뷰 엔진을 통해 화면을 렌더링해야 하기 때문입니다.

<!-- For this reason, Laravel allows you to pre-render a maintenance mode view that will be returned at the very beginning of the request cycle. This view is rendered before any of your application's dependencies have loaded. You may pre-render a template of your choice using the `down` command's `render` option: -->
이런 상황을 방지하기 위해, Laravel에서는 애플리케이션의 의존성이 로드되기 전에 가장 먼저 반환될 유지보수 모드 뷰를 미리 렌더링할 수 있습니다. 원하는 템플릿으로 미리 렌더하려면, `down` 명령의 `render` 옵션을 사용하세요:

```
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
<!-- #### Redirecting Maintenance Mode Requests -->
#### Redirecting Maintenance Mode Requests

<!-- While in maintenance mode, Laravel will display the maintenance mode view for all application URLs the user attempts to access. If you wish, you may instruct Laravel to redirect all requests to a specific URL. This may be accomplished using the `redirect` option. For example, you may wish to redirect all requests to the `/` URI: -->
유지보수 모드에서는 사용자가 어떤 URL로 접근하든 유지보수 화면이 표시됩니다. 만약 모든 요청을 특정 URL로 리디렉션하고 싶다면, `redirect` 옵션을 이용하면 됩니다. 예를 들어, 모든 요청을 `/` 경로로 리디렉션하려면 다음과 같이 실행하세요:

```
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
<!-- #### Disabling Maintenance Mode -->
#### Disabling Maintenance Mode

<!-- To disable maintenance mode, use the `up` command: -->
유지보수 모드를 해제하려면, `up` 명령을 사용하세요:

```
php artisan up
```

> [!TIP]
> 기본 유지보수 모드 템플릿은 `resources/views/errors/503.blade.php` 경로에 커스텀 템플릿을 만들어 변경할 수 있습니다.

<a name="maintenance-mode-queues"></a>
<!-- #### Maintenance Mode & Queues -->
#### Maintenance Mode & Queues

<!-- While your application is in maintenance mode, no [queued jobs](/docs/8.x/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode. -->
애플리케이션이 유지보수 모드일 때는 [queued jobs](/docs/8.x/queues)이 처리되지 않습니다. 유지보수 모드가 해제되면 대기 중이던 작업이 정상적으로 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
<!-- #### Alternatives To Maintenance Mode -->
#### Alternatives To Maintenance Mode

<!-- Since maintenance mode requires your application to have several seconds of downtime, consider alternatives like [Laravel Vapor](https://vapor.laravel.com) and [Envoyer](https://envoyer.io) to accomplish zero-downtime deployment with Laravel. -->
유지보수 모드는 몇 초 간 애플리케이션이 다운타임을 가지게 합니다. 완전한 무중단 배포가 필요하다면 [Laravel Vapor](https://vapor.laravel.com)나 [Envoyer](https://envoyer.io)와 같은 도구도 고려해볼 수 있습니다.