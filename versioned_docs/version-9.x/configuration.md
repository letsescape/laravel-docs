<!-- # Configuration -->
# Configuration

- [Introduction](#introduction)
- [Environment Configuration](#environment-configuration)
    - [Environment Variable Types](#environment-variable-types)
    - [Retrieving Environment Configuration](#retrieving-environment-configuration)
    - [Determining The Current Environment](#determining-the-current-environment)
    - [Encrypting Environment Files](#encrypting-environment-files)
- [Accessing Configuration Values](#accessing-configuration-values)
- [Configuration Caching](#configuration-caching)
- [Debug Mode](#debug-mode)
- [Maintenance Mode](#maintenance-mode)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you. -->
Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에는 주석이 잘 달려 있으니, 파일을 살펴보며 제공되는 다양한 옵션에 익숙해지시길 권장합니다.

<!-- These configuration files allow you to configure things like your database connection information, your mail server information, as well as various other core configuration values such as your application timezone and encryption key. -->
이 설정 파일들은 데이터베이스 연결 정보, 메일 서버 정보, 그리고 애플리케이션의 타임존이나 암호화 키와 같은 주요 설정값들을 구성할 수 있도록 해줍니다.

<a name="application-overview"></a>
<!-- #### Application Overview -->
#### Application Overview

<!-- In a hurry? You can get a quick overview of your application's configuration, drivers, and environment via the `about` Artisan command: -->
빠르게 전체 설정 상태를 확인하고 싶은가요? `about` 아티즌 명령어를 사용하면 애플리케이션의 전체 설정, 드라이버, 환경 개요를 한눈에 확인할 수 있습니다.

```shell
php artisan about
```

<!-- If you're only interested in a particular section of the application overview output, you may filter for that section using the `--only` option: -->
특정 섹션만 보고 싶다면, `--only` 옵션으로 원하는 부분만 필터링할 수 있습니다.

```shell
php artisan about --only=environment
```

<a name="environment-configuration"></a>
<!-- ## Environment Configuration -->
## Environment Configuration

<!-- It is often helpful to have different configuration values based on the environment where the application is running. For example, you may wish to use a different cache driver locally than you do on your production server. -->
애플리케이션이 실행되는 환경에 따라 서로 다른 설정값을 사용하는 것이 도움이 될 때가 많습니다. 예를 들어, 개발 환경에서는 운영 서버와 다른 캐시 드라이버를 쓸 수 있습니다.

<!-- To make this a cinch, Laravel utilizes the [DotEnv](https://github.com/vlucas/phpdotenv) PHP library. In a fresh Laravel installation, the root directory of your application will contain a `.env.example` file that defines many common environment variables. During the Laravel installation process, this file will automatically be copied to `.env`. -->
이를 쉽게 관리할 수 있도록, Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 활용합니다. 새로 설치된 Laravel 프로젝트의 루트 디렉터리에는 일반적으로 자주 사용하는 환경 변수를 정의한 `.env.example` 파일이 포함되어 있습니다. Laravel 설치 과정에서 이 파일은 자동으로 `.env` 파일로 복사됩니다.

<!-- Laravel's default `.env` file contains some common configuration values that may differ based on whether your application is running locally or on a production web server. These values are then retrieved from various Laravel configuration files within the `config` directory using Laravel's `env` function. -->
Laravel의 기본 `.env` 파일에는 로컬 혹은 운영 웹 서버 등 실행 환경에 따라 달라질 수 있는 여러 설정값이 들어 있습니다. 이러한 값들은 Laravel `config` 디렉터리 안의 여러 설정 파일에서 `env` 함수를 통해 불러올 수 있습니다.

<!-- If you are developing with a team, you may wish to continue including a `.env.example` file with your application. By putting placeholder values in the example configuration file, other developers on your team can clearly see which environment variables are needed to run your application. -->
여러 사람이 함께 개발한다면, `.env.example` 파일을 계속 프로젝트에 포함하는 것이 좋습니다. 예시 파일에 플레이스홀더 값을 넣어두면, 팀원들이 애플리케이션을 실행하는 데 필요한 환경 변수를 명확히 파악할 수 있습니다.

> [!NOTE]
> `.env` 파일 내의 모든 변수는 서버 또는 시스템 환경 변수 등 외부 환경 변수로 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
<!-- #### Environment File Security -->
#### Environment File Security

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed. -->
`.env` 파일은 각 개발자 또는 서버마다 환경 구성이 다를 수 있기 때문에, 절대로 소스 컨트롤(버전 관리 저장소)에 커밋하면 안 됩니다. 만일 소스 저장소가 유출된다면, 중요한 인증 정보가 노출되어 보안 위험이 발생할 수 있습니다.

<!-- However, it is possible to encrypt your environment file using Laravel's built-in [environment encryption](#encrypting-environment-files). Encrypted environment files may be placed in source control safely. -->
하지만, Laravel 내장 [environment encryption](#encrypting-environment-files) 기능을 활용하면 환경 파일을 안전하게 암호화하여 소스 컨트롤에 포함시킬 수 있습니다.

<a name="additional-environment-files"></a>
<!-- #### Additional Environment Files -->
#### Additional Environment Files

<!-- Before loading your application's environment variables, Laravel determines if an `APP_ENV` environment variable has been externally provided or if the `--env` CLI argument has been specified. If so, Laravel will attempt to load an `.env.[APP_ENV]` file if it exists. If it does not exist, the default `.env` file will be loaded. -->
애플리케이션의 환경 변수를 로드하기 전에, Laravel은 외부에서 `APP_ENV` 환경 변수가 설정되어 있거나 CLI 인자로 `--env` 옵션이 지정되어 있는지 확인합니다. 만약 해당 환경 변수나 옵션이 지정되어 있다면, Laravel은 `.env.[APP_ENV]` 파일이 존재하는지 확인 후, 해당 파일이 있으면 로드합니다. 없다면 기본 `.env` 파일을 사용합니다.

<a name="environment-variable-types"></a>
<!-- ### Environment Variable Types -->
### Environment Variable Types

<!-- All variables in your `.env` files are typically parsed as strings, so some reserved values have been created to allow you to return a wider range of types from the `env()` function: -->
`.env` 파일에 있는 모든 변수는 기본적으로 문자열로 해석됩니다. 하지만, `env()` 함수에서 다양한 타입의 값도 반환할 수 있도록 일부 예약어(특정 값)가 마련되어 있습니다.

| `.env` 값    | `env()` 반환값  |
|--------------|----------------|
| true         | (bool) true    |
| (true)       | (bool) true    |
| false        | (bool) false   |
| (false)      | (bool) false   |
| empty        | (string) ''    |
| (empty)      | (string) ''    |
| null         | (null) null    |
| (null)       | (null) null    |

<!-- If you need to define an environment variable with a value that contains spaces, you may do so by enclosing the value in double quotes: -->
만약 값에 공백이 포함되어야 한다면, 큰따옴표로 값을 감싸서 정의할 수 있습니다.

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
<!-- ### Retrieving Environment Configuration -->
### Retrieving Environment Configuration

<!-- All of the variables listed in the `.env` file will be loaded into the `$_ENV` PHP super-global when your application receives a request. However, you may use the `env` function to retrieve values from these variables in your configuration files. In fact, if you review the Laravel configuration files, you will notice many of the options are already using this function: -->
`.env` 파일에 정의된 모든 변수는 애플리케이션이 요청을 받을 때 `$_ENV` PHP 슈퍼글로벌 변수로 로드됩니다. 하지만 실제 설정 파일에서는 `env` 함수를 사용해 값을 쉽게 불러올 수 있습니다. 실제로 Laravel의 여러 설정 파일을 살펴보면, 많은 옵션들이 이미 이 함수를 사용하고 있는 것을 볼 수 있습니다.

```
'debug' => env('APP_DEBUG', false),
```

<!-- The second value passed to the `env` function is the "default value". This value will be returned if no environment variable exists for the given key. -->
`env` 함수의 두 번째 인자는 "기본값"입니다. 만약 지정한 키에 맞는 환경 변수가 없다면 이 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
<!-- ### Determining The Current Environment -->
### Determining The Current Environment

<!-- The current application environment is determined via the `APP_ENV` variable from your `.env` file. You may access this value via the `environment` method on the `App` [facade](/docs/9.x/facades): -->
현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [facade](/docs/9.x/facades)의 `environment` 메서드를 통해 조회할 수 있습니다.

```
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

<!-- You may also pass arguments to the `environment` method to determine if the environment matches a given value. The method will return `true` if the environment matches any of the given values: -->
`environment` 메서드에 특정 값을 인수로 넘기면, 현재 환경이 해당 값과 일치하는지 확인할 수 있습니다. 여러 값을 배열로 전달하면, 그 중 하나라도 맞으면 `true`가 반환됩니다.

```
if (App::environment('local')) {
    // The environment is local
}

if (App::environment(['local', 'staging'])) {
    // The environment is either local OR staging...
}
```

> [!NOTE]
> 현재 애플리케이션 환경 감지는 서버 수준의 `APP_ENV` 환경 변수에 의해 덮어쓸 수 있습니다.

<a name="encrypting-environment-files"></a>
<!-- ### Encrypting Environment Files -->
### Encrypting Environment Files

<!-- Unencrypted environment files should never be stored in source control. However, Laravel allows you to encrypt your environment files so that they may safely be added to source control with the rest of your application. -->
암호화되지 않은 환경 파일은 소스 컨트롤에 절대 저장해선 안 됩니다. 하지만 Laravel은 환경 파일을 암호화하여 나머지 애플리케이션 소스와 함께 안전하게 소스 컨트롤에 포함시킬 수 있는 기능을 제공합니다.

<a name="encryption"></a>
<!-- #### Encryption -->
#### Encryption

<!-- To encrypt an environment file, you may use the `env:encrypt` command: -->
환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용합니다.

```shell
php artisan env:encrypt
```

<!-- Running the `env:encrypt` command will encrypt your `.env` file and place the encrypted contents in an `.env.encrypted` file. The decryption key is presented in the output of the command and should be stored in a secure password manager. If you would like to provide your own encryption key you may use the `--key` option when invoking the command: -->
`env:encrypt` 명령어를 실행하면 `.env` 파일이 암호화되어 `.env.encrypted` 파일에 저장됩니다. 복호화에 필요한 키는 명령어 실행 결과에 함께 출력되며, 반드시 안전한 비밀번호 관리 도구에 보관해야 합니다. 본인이 직접 사용할 암호화 키를 지정하고 싶다면, 아래와 같이 `--key` 옵션을 사용할 수 있습니다.

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 키의 길이는 사용하는 암호화 알고리즘의 요구 사항과 일치해야 합니다. 기본적으로 Laravel은 `AES-256-CBC` 알고리즘을 사용하며, 32자 키가 필요합니다. `--cipher` 옵션을 사용해 Laravel의 [encrypter](/docs/9.x/encryption)가 지원하는 다른 암호화 알고리즘을 선택할 수도 있습니다.

<!-- If your application has multiple environment files, such as `.env` and `.env.staging`, you may specify the environment file that should be encrypted by providing the environment name via the `--env` option: -->
여러 개의 환경 파일(예: `.env`, `.env.staging`)이 있다면, `--env` 옵션을 통해 암호화할 환경 파일을 지정할 수 있습니다.

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
<!-- #### Decryption -->
#### Decryption

<!-- To decrypt an environment file, you may use the `env:decrypt` command. This command requires a decryption key, which Laravel will retrieve from the `LARAVEL_ENV_ENCRYPTION_KEY` environment variable: -->
환경 파일을 복호화하려면 `env:decrypt` 명령어를 사용합니다. 이 명령어는 복호화 키가 필요하며, Laravel은 환경 변수 `LARAVEL_ENV_ENCRYPTION_KEY`에서 해당 키를 읽어옵니다.

```shell
php artisan env:decrypt
```

<!-- Or, the key may be provided directly to the command via the `--key` option: -->
혹은, 키를 직접 명령어의 `--key` 옵션에 지정할 수도 있습니다.

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

<!-- When the `env:decrypt` command is invoked, Laravel will decrypt the contents of the `.env.encrypted` file and place the decrypted contents in the `.env` file. -->
`env:decrypt` 명령어를 실행하면 Laravel이 `.env.encrypted` 파일을 복호화해서 `.env` 파일에 내용을 기록합니다.

<!-- The `--cipher` option may be provided to the `env:decrypt` command in order to use a custom encryption cipher: -->
커스텀 암호화 알고리즘을 사용하려면 `env:decrypt` 명령어에 `--cipher` 옵션을 지정할 수 있습니다.

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

<!-- If your application has multiple environment files, such as `.env` and `.env.staging`, you may specify the environment file that should be decrypted by providing the environment name via the `--env` option: -->
여러 개의 환경 파일(예: `.env`, `.env.staging`)이 있다면, `--env` 옵션으로 복호화할 환경 파일을 지정할 수 있습니다.

```shell
php artisan env:decrypt --env=staging
```

<!-- In order to overwrite an existing environment file, you may provide the `--force` option to the `env:decrypt` command: -->
기존 환경 파일을 덮어써야 할 경우, `env:decrypt` 명령어에 `--force` 옵션을 추가하면 됩니다.

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
<!-- ## Accessing Configuration Values -->
## Accessing Configuration Values

<!-- You may easily access your configuration values using the global `config` function from anywhere in your application. The configuration values may be accessed using "dot" syntax, which includes the name of the file and option you wish to access. A default value may also be specified and will be returned if the configuration option does not exist: -->
애플리케이션 어디에서든 전역 `config` 함수를 이용해 설정값에 쉽게 접근할 수 있습니다. 설정값은 "dot" 문법(점 표기법), 즉 파일명과 원하는 옵션명을 점으로 연결한 방식으로 접근합니다. 또한, 기본값을 지정할 수 있으며, 해당 설정이 없는 경우 기본값이 반환됩니다.

```
$value = config('app.timezone');

// Retrieve a default value if the configuration value does not exist...
$value = config('app.timezone', 'Asia/Seoul');
```

<!-- To set configuration values at runtime, pass an array to the `config` function: -->
런타임에 설정값을 변경하고 싶으면, `config` 함수에 배열을 넘기면 됩니다.

```
config(['app.timezone' => 'America/Chicago']);
```

<a name="configuration-caching"></a>
<!-- ## Configuration Caching -->
## Configuration Caching

<!-- To give your application a speed boost, you should cache all of your configuration files into a single file using the `config:cache` Artisan command. This will combine all of the configuration options for your application into a single file which can be quickly loaded by the framework. -->
애플리케이션의 성능을 높이기 위해, 모든 설정 파일을 하나의 파일로 캐싱할 수 있습니다. 이를 위해 `config:cache` 아티즌 명령어를 사용하세요. 이 명령어는 각종 설정 옵션들을 하나의 파일로 결합하며, 프레임워크가 이 파일을 빠르게 로드할 수 있게 합니다.

<!-- You should typically run the `php artisan config:cache` command as part of your production deployment process. The command should not be run during local development as configuration options will frequently need to be changed during the course of your application's development. -->
보통 운영 환경 배포 과정에서 `php artisan config:cache` 명령어를 실행해야 합니다. 로컬 개발 중에는 애플리케이션의 설정이 자주 바뀔 수 있으므로, 이 명령어를 실행하지 않아야 합니다.

<!-- The `config:clear` command may be used to purge the cached configuration: -->
설정 캐시를 제거하려면 `config:clear` 명령어를 사용하면 됩니다.

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행할 경우, 반드시 설정 파일 내부에서만 `env` 함수를 사용해야 합니다. 캐싱 이후에는 `.env` 파일이 더 이상 로드되지 않으며, 이때 `env` 함수는 외부(시스템 수준) 환경 변수만 반환할 수 있습니다.

<a name="debug-mode"></a>
<!-- ## Debug Mode -->
## Debug Mode

<!-- The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file. -->
`config/app.php` 설정 파일의 `debug` 옵션은 에러가 발생했을 때 사용자에게 얼마나 많은 정보를 보여줄지를 결정합니다. 이 옵션은 기본적으로 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

<!-- For local development, you should set the `APP_DEBUG` environment variable to `true`. **In your production environment, this value should always be `false`. If the variable is set to `true` in production, you risk exposing sensitive configuration values to your application's end users.** -->
로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **운영 환경에서는 이 값을 항상 `false`로 두어야 합니다. 운영 환경에서 이 변수가 `true`로 설정되면, 중요한 설정 정보가 애플리케이션 최종 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
<!-- ## Maintenance Mode -->
## Maintenance Mode

<!-- When your application is in maintenance mode, a custom view will be displayed for all requests into your application. This makes it easy to "disable" your application while it is updating or when you are performing maintenance. A maintenance mode check is included in the default middleware stack for your application. If the application is in maintenance mode, a `Symfony\Component\HttpKernel\Exception\HttpException` instance will be thrown with a status code of 503. -->
애플리케이션이 서비스 점검 모드(maintenance mode)일 때는, 모든 요청에 대해 커스텀 화면이 표시됩니다. 이 기능을 활용하면 유지보수 중이나 업데이트 중 쉽게 애플리케이션 접근을 제한할 수 있습니다. 서비스 점검 모드 체크는 애플리케이션의 기본 미들웨어 스택에 포함되어 있습니다. 점검 모드가 활성화된 경우, `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 503 상태 코드와 함께 발생합니다.

<!-- To enable maintenance mode, execute the `down` Artisan command: -->
서비스 점검 모드를 활성화하려면, `down` 아티즌 명령어를 사용하세요.

```shell
php artisan down
```

<!-- If you would like the `Refresh` HTTP header to be sent with all maintenance mode responses, you may provide the `refresh` option when invoking the `down` command. The `Refresh` header will instruct the browser to automatically refresh the page after the specified number of seconds: -->
점검 모드 시 모든 응답에 `Refresh` HTTP 헤더를 함께 보내고 싶다면, `down` 명령어를 실행할 때 `refresh` 옵션을 쓸 수 있습니다. `Refresh` 헤더는 브라우저에게 지정된 초 이후 자동으로 페이지를 새로 고치도록 안내합니다.

```shell
php artisan down --refresh=15
```

<!-- You may also provide a `retry` option to the `down` command, which will be set as the `Retry-After` HTTP header's value, although browsers generally ignore this header: -->
또한, `down` 명령어의 `retry` 옵션을 사용하면 `Retry-After` HTTP 헤더에 값을 지정할 수 있습니다. 하지만 대부분의 브라우저는 이 헤더를 무시합니다.

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
<!-- #### Bypassing Maintenance Mode -->
#### Bypassing Maintenance Mode

<!-- To allow maintenance mode to be bypassed using a secret token, you may use the `secret` option to specify a maintenance mode bypass token: -->
비밀 토큰을 사용해 서비스 점검 모드를 우회할 수 있습니다. `secret` 옵션을 사용하여 우회 토큰을 지정하면 됩니다.

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

<!-- After placing the application in maintenance mode, you may navigate to the application URL matching this token and Laravel will issue a maintenance mode bypass cookie to your browser: -->
애플리케이션을 점검 모드로 전환한 뒤, 위와 같이 토큰을 포함한 URL로 접속하면, Laravel이 브라우저에 점검 모드 우회 쿠키를 발급해 줍니다.

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

<!-- When accessing this hidden route, you will then be redirected to the `/` route of the application. Once the cookie has been issued to your browser, you will be able to browse the application normally as if it was not in maintenance mode. -->
이 숨겨진 주소에 접근하면 `/` 경로로 자동 리다이렉트되며 쿠키가 발급됩니다. 이후에는 점검 모드 상태임에도 불구하고 정상적으로 애플리케이션을 이용할 수 있습니다.

> [!NOTE]
> 점검 모드 비밀 토큰(secret)으로는 영문과 숫자, 그리고 선택적으로 대시(-) 문자를 사용하는 것이 일반적입니다. `?` 나 `&` 등 URL에서 특별한 의미를 가지는 문자는 피하는 것이 좋습니다.

<a name="pre-rendering-the-maintenance-mode-view"></a>
<!-- #### Pre-Rendering The Maintenance Mode View -->
#### Pre-Rendering The Maintenance Mode View

<!-- If you utilize the `php artisan down` command during deployment, your users may still occasionally encounter errors if they access the application while your Composer dependencies or other infrastructure components are updating. This occurs because a significant part of the Laravel framework must boot in order to determine your application is in maintenance mode and render the maintenance mode view using the templating engine. -->
배포 과정에서 `php artisan down` 명령어를 활용할 때, 사용자가 Composer 의존성이나 기타 인프라 구성 요소가 업데이트되는 도중 애플리케이션에 접근하면 에러가 발생할 수 있습니다. 이는 Laravel이 점검 모드 여부 판별과 화면 렌더링을 위해 일부 코어 기능을 부팅해야 하기 때문입니다.

<!-- For this reason, Laravel allows you to pre-render a maintenance mode view that will be returned at the very beginning of the request cycle. This view is rendered before any of your application's dependencies have loaded. You may pre-render a template of your choice using the `down` command's `render` option: -->
이 문제를 방지하기 위해, Laravel은 서버가 실제 부팅되기 전에 바로 반환되는 점검 모드 화면(뷰)을 미리 렌더링할 수 있습니다. `down` 명령어의 `render` 옵션을 사용해 원하는 템플릿을 미리 렌더링할 수 있습니다.

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
<!-- #### Redirecting Maintenance Mode Requests -->
#### Redirecting Maintenance Mode Requests

<!-- While in maintenance mode, Laravel will display the maintenance mode view for all application URLs the user attempts to access. If you wish, you may instruct Laravel to redirect all requests to a specific URL. This may be accomplished using the `redirect` option. For example, you may wish to redirect all requests to the `/` URI: -->
서비스 점검 모드가 활성화된 동안 Laravel은 모든 URL 요청에 대해 점검 모드 화면을 표시합니다. 만약, 별도의 특정 URL로 모든 요청을 리다이렉트하고 싶다면 `redirect` 옵션을 활용할 수 있습니다. 예를 들어, 모든 요청을 `/` 경로로 리다이렉트하고 싶을 때 다음과 같이 입력합니다.

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
<!-- #### Disabling Maintenance Mode -->
#### Disabling Maintenance Mode

<!-- To disable maintenance mode, use the `up` command: -->
점검 모드를 해제하려면, `up` 명령어를 사용하세요.

```shell
php artisan up
```

> [!NOTE]
> 기본 점검 모드 템플릿은 `resources/views/errors/503.blade.php` 파일을 직접 생성하여 원하는 내용으로 커스터마이즈할 수 있습니다.

<a name="maintenance-mode-queues"></a>
<!-- #### Maintenance Mode & Queues -->
#### Maintenance Mode & Queues

<!-- While your application is in maintenance mode, no [queued jobs](/docs/9.x/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode. -->
서비스 점검 모드가 활성화되어 있으면 [queued jobs](/docs/9.x/queues)는 처리되지 않습니다. 점검 모드가 해제되면 큐 작업이 다시 정상적으로 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
<!-- #### Alternatives To Maintenance Mode -->
#### Alternatives To Maintenance Mode

<!-- Since maintenance mode requires your application to have several seconds of downtime, consider alternatives like [Laravel Vapor](https://vapor.laravel.com) and [Envoyer](https://envoyer.io) to accomplish zero-downtime deployment with Laravel. -->
점검 모드는 몇 초간의 서비스 중단(downtime)이 필요합니다. Laravel로 무중단 배포(zero-downtime deployment)를 하고 싶다면 [Laravel Vapor](https://vapor.laravel.com)나 [Envoyer](https://envoyer.io) 같은 솔루션을 고려해 보세요.
