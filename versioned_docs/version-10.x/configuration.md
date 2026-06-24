<!-- # Configuration -->
# Configuration

- [Introduction](#introduction)
- [Environment Configuration](#environment-configuration)
    - [Environment Variable Types](#environment-variable-types)
    - [Retrieving Environment Configuration](#retrieving-environment-configuration)
    - [Determining the Current Environment](#determining-the-current-environment)
    - [Encrypting Environment Files](#encrypting-environment-files)
- [Accessing Configuration Values](#accessing-configuration-values)
- [Configuration Caching](#configuration-caching)
- [Debug Mode](#debug-mode)
- [Maintenance Mode](#maintenance-mode)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you. -->
Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에는 설명이 달려 있으니, 파일들을 살펴보면서 어떤 설정 값들이 있는지 익숙해지시길 권장합니다.

<!-- These configuration files allow you to configure things like your database connection information, your mail server information, as well as various other core configuration values such as your application timezone and encryption key. -->
이 설정 파일들은 데이터베이스 연결 정보, 메일 서버 정보와 같은 주요 환경 구성 값뿐만 아니라, 애플리케이션의 기본 타임존이나 암호화 키 등 다양한 핵심 설정 값들을 구성할 수 있도록 해줍니다.

<a name="application-overview"></a>
<!-- #### Application Overview -->
#### Application Overview

<!-- In a hurry? You can get a quick overview of your application's configuration, drivers, and environment via the `about` Artisan command: -->
빠르게 확인하실 필요가 있다면, `about` 아티즌 명령어를 통해 애플리케이션의 환경, 드라이버, 설정 등의 정보를 한눈에 확인할 수 있습니다.

```shell
php artisan about
```

<!-- If you're only interested in a particular section of the application overview output, you may filter for that section using the `--only` option: -->
애플리케이션 개요 출력 중 특정 섹션만 보고 싶다면, `--only` 옵션을 사용해 해당 부분만 필터링할 수 있습니다.

```shell
php artisan about --only=environment
```

<!-- Or, to explore a specific configuration file's values in detail, you may use the `config:show` Artisan command: -->
또한, 특정 설정 파일의 상세 내용을 확인하고 싶다면 `config:show` 아티즌 명령어를 사용하실 수 있습니다.

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
<!-- ## Environment Configuration -->
## Environment Configuration

<!-- It is often helpful to have different configuration values based on the environment where the application is running. For example, you may wish to use a different cache driver locally than you do on your production server. -->
애플리케이션이 실행되는 환경에 따라 서로 다른 설정 값을 사용하는 것이 유용할 때가 많습니다. 예를 들어, 로컬에서는 캐시 드라이버를 다르게 하거나, 운영 서버에서는 또 다른 값을 주고 싶을 수 있습니다.

<!-- To make this a cinch, Laravel utilizes the [DotEnv](https://github.com/vlucas/phpdotenv) PHP library. In a fresh Laravel installation, the root directory of your application will contain a `.env.example` file that defines many common environment variables. During the Laravel installation process, this file will automatically be copied to `.env`. -->
이러한 작업을 쉽게 해주기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 사용합니다. 새로운 Laravel 프로젝트를 설치하면, 애플리케이션의 루트 디렉터리에 `.env.example` 파일이 생성되며, 여기에는 자주 쓰는 환경 변수들이 정의되어 있습니다. Laravel 설치 과정에서 이 파일이 `.env`로 자동 복사됩니다.

<!-- Laravel's default `.env` file contains some common configuration values that may differ based on whether your application is running locally or on a production web server. These values are then retrieved from various Laravel configuration files within the `config` directory using Laravel's `env` function. -->
Laravel의 기본 `.env` 파일에는 로컬 개발 환경과 운영 서버 환경에서 서로 달라질 수 있는 일반적인 설정 값들이 담겨 있습니다. 이 값들은 `config` 디렉터리 안의 여러 Laravel 설정 파일에서 Laravel의 `env` 함수를 통해 불러오게 됩니다.

<!-- If you are developing with a team, you may wish to continue including a `.env.example` file with your application. By putting placeholder values in the example configuration file, other developers on your team can clearly see which environment variables are needed to run your application. -->
여러분이 팀 개발을 하고 있다면, `.env.example` 파일을 계속 소스 코드에 포함해두는 것이 좋습니다. 예시 파일에 플레이스홀더 값들을 미리 넣어두면, 동료 개발자들도 어떤 환경 변수가 필요한지 쉽게 파악할 수 있습니다.

> [!NOTE]
> `.env` 파일에 정의한 변수들은 서버 환경 변수나 시스템 환경 변수 등 외부 환경 변수로 언제든지 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
<!-- #### Environment File Security -->
#### Environment File Security

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed. -->
`.env` 파일은 각 개발자나 서버 별로 환경 설정이 다를 수 있으므로 소스 저장소에 커밋하면 안 됩니다. 또한, 만약 소스 저장소가 침해당하면 민감한 인증 정보가 유출될 위험도 있습니다.

<!-- However, it is possible to encrypt your environment file using Laravel's built-in [environment encryption](#encrypting-environment-files). Encrypted environment files may be placed in source control safely. -->
하지만, Laravel의 [environment encryption](#encrypting-environment-files) 기능을 사용하면 환경 파일을 암호화하여 안전하게 소스 저장소에 보관할 수도 있습니다.

<a name="additional-environment-files"></a>
<!-- #### Additional Environment Files -->
#### Additional Environment Files

<!-- Before loading your application's environment variables, Laravel determines if an `APP_ENV` environment variable has been externally provided or if the `--env` CLI argument has been specified. If so, Laravel will attempt to load an `.env.[APP_ENV]` file if it exists. If it does not exist, the default `.env` file will be loaded. -->
Laravel이 애플리케이션의 환경 변수를 로드하기 전에, `APP_ENV` 환경 변수가 외부에서 지정되어 있거나, 또는 명령줄의 `--env` 인자가 제공되어 있는지 확인합니다. 해당하는 경우, Laravel은 `.env.[APP_ENV]` 파일이 존재하면 그것을 먼저 로드합니다. 해당 파일이 없다면 기본 `.env` 파일을 사용합니다.

<a name="environment-variable-types"></a>
<!-- ### Environment Variable Types -->
### Environment Variable Types

<!-- All variables in your `.env` files are typically parsed as strings, so some reserved values have been created to allow you to return a wider range of types from the `env()` function: -->
`.env` 파일에 있는 모든 변수는 기본적으로 문자열로 처리됩니다. 하지만 `env()` 함수에서 더욱 다양한 타입의 값을 사용할 수 있도록 다음과 같이 예약된 값들이 있습니다.

| `.env` 값    | `env()` 반환값    |
|--------------|------------------|
| true         | (bool) true      |
| (true)       | (bool) true      |
| false        | (bool) false     |
| (false)      | (bool) false     |
| empty        | (string) ''      |
| (empty)      | (string) ''      |
| null         | (null) null      |
| (null)       | (null) null      |

<!-- If you need to define an environment variable with a value that contains spaces, you may do so by enclosing the value in double quotes: -->
값에 공백이 포함돼야 한다면 큰따옴표로 감싸서 정의할 수 있습니다.

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
<!-- ### Retrieving Environment Configuration -->
### Retrieving Environment Configuration

<!-- All of the variables listed in the `.env` file will be loaded into the `$_ENV` PHP super-global when your application receives a request. However, you may use the `env` function to retrieve values from these variables in your configuration files. In fact, if you review the Laravel configuration files, you will notice many of the options are already using this function: -->
`.env` 파일에 정의된 변수들은 애플리케이션이 요청을 받으면 `$_ENV` PHP 전역 변수로 모두 불러와집니다. 하지만, 설정 파일 안에서는 주로 `env` 함수를 사용해 해당 변수 값을 가져옵니다. 실제로 Laravel의 설정 파일을 살펴보면 이 함수가 널리 사용되고 있음을 알 수 있습니다.

```
'debug' => env('APP_DEBUG', false),
```

<!-- The second value passed to the `env` function is the "default value". This value will be returned if no environment variable exists for the given key. -->
`env` 함수에 두 번째 인수를 넘기면 "기본 값"이 됩니다. 즉, 해당 환경 변수 값이 존재하지 않을 때 이 기본 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
<!-- ### Determining the Current Environment -->
### Determining the Current Environment

<!-- The current application environment is determined via the `APP_ENV` variable from your `.env` file. You may access this value via the `environment` method on the `App` [facade](/docs/10.x/facades): -->
애플리케이션의 현재 환경은 `.env` 파일에 적힌 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [facade](/docs/10.x/facades)의 `environment` 메서드를 통해 확인할 수 있습니다.

```
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

<!-- You may also pass arguments to the `environment` method to determine if the environment matches a given value. The method will return `true` if the environment matches any of the given values: -->
또한, `environment` 메서드에 인수를 넘기면, 환경 값이 주어진 값과 일치하는지 확인할 수 있습니다. 하나라도 일치하면 `true`를 반환합니다.

```
if (App::environment('local')) {
    // The environment is local
}

if (App::environment(['local', 'staging'])) {
    // The environment is either local OR staging...
}
```

> [!NOTE]
> 서버 환경 변수로 `APP_ENV`를 지정하면, 현재 환경 감지는 그 값으로 덮어써집니다.

<a name="encrypting-environment-files"></a>
<!-- ### Encrypting Environment Files -->
### Encrypting Environment Files

<!-- Unencrypted environment files should never be stored in source control. However, Laravel allows you to encrypt your environment files so that they may safely be added to source control with the rest of your application. -->
암호화되지 않은 환경 파일은 소스 저장소에 절대 보관해서는 안 됩니다. 하지만, Laravel에서는 환경 파일을 암호화하여 애플리케이션 소스와 함께 안전하게 저장할 수 있습니다.

<a name="encryption"></a>
<!-- #### Encryption -->
#### Encryption

<!-- To encrypt an environment file, you may use the `env:encrypt` command: -->
환경 파일을 암호화하려면, `env:encrypt` 명령어를 사용합니다.

```shell
php artisan env:encrypt
```

<!-- Running the `env:encrypt` command will encrypt your `.env` file and place the encrypted contents in an `.env.encrypted` file. The decryption key is presented in the output of the command and should be stored in a secure password manager. If you would like to provide your own encryption key you may use the `--key` option when invoking the command: -->
`env:encrypt` 명령어를 실행하면 `.env` 파일이 암호화되어 `.env.encrypted` 파일에 저장됩니다. 암호화 키는 명령어 실행 결과에 출력되며, 반드시 안전한 비밀번호 관리자 등에 잘 보관해야 합니다. 만약 직접 키를 지정하고 싶다면 `--key` 옵션을 사용할 수 있습니다.

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 사용하려는 암호화 키의 길이는 사용하는 암호화 cipher가 요구하는 길이와 일치해야 합니다. Laravel은 기본적으로 `AES-256-CBC` cipher를 사용하며, 32자의 키를 필요로 합니다. `--cipher` 옵션을 통해 Laravel의 [encrypter](/docs/10.x/encryption)가 지원하는 다른 cipher도 사용할 수 있습니다.

<!-- If your application has multiple environment files, such as `.env` and `.env.staging`, you may specify the environment file that should be encrypted by providing the environment name via the `--env` option: -->
애플리케이션에 여러 환경 파일(예: `.env`, `.env.staging`)이 있다면, `--env` 옵션을 이용해 암호화할 환경 파일을 지정할 수 있습니다.

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
<!-- #### Decryption -->
#### Decryption

<!-- To decrypt an environment file, you may use the `env:decrypt` command. This command requires a decryption key, which Laravel will retrieve from the `LARAVEL_ENV_ENCRYPTION_KEY` environment variable: -->
암호화된 환경 파일을 복호화하려면, `env:decrypt` 명령어를 사용하세요. 이 명령어에는 복호화 키가 필요하며, Laravel은 이를 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 찾습니다.

```shell
php artisan env:decrypt
```

<!-- Or, the key may be provided directly to the command via the `--key` option: -->
또는, `--key` 옵션을 이용해 직접 키를 명령어에 전달할 수도 있습니다.

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

<!-- When the `env:decrypt` command is invoked, Laravel will decrypt the contents of the `.env.encrypted` file and place the decrypted contents in the `.env` file. -->
`env:decrypt` 명령어가 실행되면, `.env.encrypted` 파일이 복호화되어 그 결과가 `.env` 파일에 저장됩니다.

<!-- The `--cipher` option may be provided to the `env:decrypt` command in order to use a custom encryption cipher: -->
커스텀 암호화 cipher를 사용하려면 `env:decrypt` 명령어에 `--cipher` 옵션을 추가할 수 있습니다.

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

<!-- If your application has multiple environment files, such as `.env` and `.env.staging`, you may specify the environment file that should be decrypted by providing the environment name via the `--env` option: -->
애플리케이션에 여러 환경 파일(예: `.env`, `.env.staging`)이 있다면, `--env` 옵션을 이용해 복호화할 환경 파일을 지정할 수 있습니다.

```shell
php artisan env:decrypt --env=staging
```

<!-- In order to overwrite an existing environment file, you may provide the `--force` option to the `env:decrypt` command: -->
기존 환경 파일을 덮어쓰려면, `env:decrypt` 명령어에 `--force` 옵션을 추가하면 됩니다.

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
<!-- ## Accessing Configuration Values -->
## Accessing Configuration Values

<!-- You may easily access your configuration values using the `Config` facade or global `config` function from anywhere in your application. The configuration values may be accessed using "dot" syntax, which includes the name of the file and option you wish to access. A default value may also be specified and will be returned if the configuration option does not exist: -->
애플리케이션 어디에서나 `Config` 파사드나 전역 함수인 `config`를 이용해 손쉽게 설정 값을 가져올 수 있습니다. 설정 값은 "점 표기법(dot syntax)"을 사용하여, 파일 이름과 옵션 이름을 함께 지정합니다. 옵션이 존재하지 않을 때 사용할 기본 값도 설정할 수 있습니다.

```
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// Retrieve a default value if the configuration value does not exist...
$value = config('app.timezone', 'Asia/Seoul');
```

<!-- To set configuration values at runtime, you may invoke the `Config` facade's `set` method or pass an array to the `config` function: -->
실행 중에 설정 값을 변경하려면, `Config` 파사드의 `set` 메서드를 호출하거나, `config` 함수에 배열을 전달하면 됩니다.

```
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

<a name="configuration-caching"></a>
<!-- ## Configuration Caching -->
## Configuration Caching

<!-- To give your application a speed boost, you should cache all of your configuration files into a single file using the `config:cache` Artisan command. This will combine all of the configuration options for your application into a single file which can be quickly loaded by the framework. -->
애플리케이션의 성능을 높이기 위해, 모든 설정 파일을 하나의 파일로 캐싱할 수 있습니다. 이를 위해 `config:cache` 아티즌 명령어를 사용합니다. 이 명령어를 실행하면 모든 설정 옵션이 하나의 파일로 합쳐지며, 프레임워크가 빠르게 로드할 수 있습니다.

<!-- You should typically run the `php artisan config:cache` command as part of your production deployment process. The command should not be run during local development as configuration options will frequently need to be changed during the course of your application's development. -->
`php artisan config:cache` 명령어는 운영 환경(프로덕션) 배포 과정의 일부로 실행하는 것이 일반적입니다. 로컬 개발 중에는 애플리케이션을 개발하는 동안 설정 옵션이 자주 바뀌어야 하므로, 이 명령어를 실행해서는 안 됩니다.

<!-- Once the configuration has been cached, your application's `.env` file will not be loaded by the framework during requests or Artisan commands; therefore, the `env` function will only return external, system level environment variables. -->
설정이 캐싱되면, 애플리케이션 요청이나 아티즌 명령어 실행 시 `.env` 파일이 더 이상 불러와지지 않습니다. 따라서 `env` 함수는 외부(시스템 레벨)의 환경 변수만 반환합니다.

<!-- For this reason, you should ensure you are only calling the `env` function from within your application's configuration (`config`) files. You can see many examples of this by examining Laravel's default configuration files. Configuration values may be accessed from anywhere in your application using the `config` function [described above](#accessing-configuration-values). -->
이런 이유로, 반드시 **애플리케이션의 설정 파일(`config` 디렉터리 내부)에서만** `env` 함수를 호출해야 합니다. Laravel 기본 설정 파일들을 보면 이런 방식을 따르고 있음을 확인할 수 있습니다. 설정 값은 언제든 [described above](#accessing-configuration-values) `config` 함수를 통해 접근할 수 있습니다.

<!-- The `config:clear` command may be used to purge the cached configuration: -->
설정 캐시를 삭제하려면 `config:clear` 명령어를 사용해 캐시를 비울 수 있습니다.

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행했다면, 항상 **설정 파일 안에서만** `env` 함수를 사용하고 있다는 점을 꼭 확인하세요. 일단 설정이 캐싱되면 `.env` 파일은 더 이상 로드되지 않으니, `env` 함수는 시스템 레벨 환경 변수만 반환하게 됩니다.

<a name="debug-mode"></a>
<!-- ## Debug Mode -->
## Debug Mode

<!-- The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file. -->
`config/app.php` 설정 파일의 `debug` 옵션은 에러 발생 시 사용자에게 얼마나 많은 정보가 표시될지 결정합니다. 기본적으로 이 옵션은 `.env` 파일의 `APP_DEBUG` 환경 변수 값을 따라갑니다.

> [!WARNING]
> 로컬 개발 환경에서는 `APP_DEBUG` 값을 `true`로 두는 것이 좋습니다. **운영 환경(프로덕션)에서는 반드시 `false`로 설정해야 합니다. 운영 환경에서 이 값이 `true`로 되어 있으면, 민감한 설정 정보가 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
<!-- ## Maintenance Mode -->
## Maintenance Mode

<!-- When your application is in maintenance mode, a custom view will be displayed for all requests into your application. This makes it easy to "disable" your application while it is updating or when you are performing maintenance. A maintenance mode check is included in the default middleware stack for your application. If the application is in maintenance mode, a `Symfony\Component\HttpKernel\Exception\HttpException` instance will be thrown with a status code of 503. -->
애플리케이션이 점검 모드에 들어가면, 모든 요청에 대해 커스텀 뷰가 표시됩니다. 이를 통해 애플리케이션의 업데이트나 유지보수 중에 접근을 일시적으로 "막는" 것이 가능합니다. 점검 모드 체크는 애플리케이션의 기본 미들웨어 스택에 포함되어 있습니다. 점검 모드일 경우, `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 503 상태 코드로 던져집니다.

<!-- To enable maintenance mode, execute the `down` Artisan command: -->
점검 모드를 활성화하려면, `down` 아티즌 명령어를 실행하세요.

```shell
php artisan down
```

<!-- If you would like the `Refresh` HTTP header to be sent with all maintenance mode responses, you may provide the `refresh` option when invoking the `down` command. The `Refresh` header will instruct the browser to automatically refresh the page after the specified number of seconds: -->
모든 점검 모드 응답에 `Refresh` HTTP 헤더를 함께 보내고 싶다면, `down` 명령어를 실행할 때 `refresh` 옵션을 지정하면 됩니다. `Refresh` 헤더는 브라우저가 지정된 초(second) 만큼 대기한 뒤 자동으로 페이지를 새로고침 하도록 안내합니다.

```shell
php artisan down --refresh=15
```

<!-- You may also provide a `retry` option to the `down` command, which will be set as the `Retry-After` HTTP header's value, although browsers generally ignore this header: -->
`down` 명령어에 `retry` 옵션을 지정하면, `Retry-After` HTTP 헤더 값을 정할 수 있습니다. 다만, 브라우저들은 이 헤더를 거의 무시합니다.

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
<!-- #### Bypassing Maintenance Mode -->
#### Bypassing Maintenance Mode

<!-- To allow maintenance mode to be bypassed using a secret token, you may use the `secret` option to specify a maintenance mode bypass token: -->
점검 모드를 비밀 토큰으로 우회할 수 있도록 하려면, `secret` 옵션을 사용해 우회 토큰을 지정할 수 있습니다.

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

<!-- After placing the application in maintenance mode, you may navigate to the application URL matching this token and Laravel will issue a maintenance mode bypass cookie to your browser: -->
애플리케이션을 점검 모드로 전환한 후, 이 토큰과 일치하는 URL로 접속하면 Laravel이 브라우저에 점검 모드 우회 쿠키를 발급하게 됩니다.

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

<!-- If you would like Laravel to generate the secret token for you, you may use the `with-secret` option. The secret will be displayed to you once the application is in maintenance mode: -->
비밀 토큰을 Laravel이 자동으로 생성해주길 원하면, `with-secret` 옵션을 사용하세요. 애플리케이션이 점검 모드에 들어가면 비밀 토큰이 콘솔에 표시됩니다.

```shell
php artisan down --with-secret
```

<!-- When accessing this hidden route, you will then be redirected to the `/` route of the application. Once the cookie has been issued to your browser, you will be able to browse the application normally as if it was not in maintenance mode. -->
이 숨겨진 라우트에 접근하면 이후 `/` 경로로 자동 리다이렉트됩니다. 쿠키가 발급된 브라우저는 점검 모드임에도 평소처럼 애플리케이션 이용이 가능합니다.

> [!NOTE]
> 점검 모드 비밀 토큰은 영문자, 숫자, 그리고 선택적으로 대시(-) 등만 사용하는 것이 일반적입니다. URL 내 특수 의미를 가지는 `?`, `&` 등의 문자는 가급적 피해야 합니다.

<a name="pre-rendering-the-maintenance-mode-view"></a>
<!-- #### Pre-Rendering the Maintenance Mode View -->
#### Pre-Rendering the Maintenance Mode View

<!-- If you utilize the `php artisan down` command during deployment, your users may still occasionally encounter errors if they access the application while your Composer dependencies or other infrastructure components are updating. This occurs because a significant part of the Laravel framework must boot in order to determine your application is in maintenance mode and render the maintenance mode view using the templating engine. -->
배포 과정에서 `php artisan down` 명령어를 사용할 경우, 사용자들이 의도치 않게 에러 화면을 볼 수 있습니다. 이는 Laravel 프레임워크의 상당 부분이 부팅되어야 점검 모드 여부를 감지하고, 뷰 엔진을 통해 점검 모드 화면을 렌더링하기 때문입니다.

<!-- For this reason, Laravel allows you to pre-render a maintenance mode view that will be returned at the very beginning of the request cycle. This view is rendered before any of your application's dependencies have loaded. You may pre-render a template of your choice using the `down` command's `render` option: -->
이런 현상을 방지하기 위해, Laravel은 점검 모드 화면을 요청 루프의 가장 초기에 "미리 렌더"해서 반환하는 기능을 지원합니다. 원하는 템플릿을 `down` 명령어의 `render` 옵션으로 지정하여 미리 렌더할 수 있습니다.

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
<!-- #### Redirecting Maintenance Mode Requests -->
#### Redirecting Maintenance Mode Requests

<!-- While in maintenance mode, Laravel will display the maintenance mode view for all application URLs the user attempts to access. If you wish, you may instruct Laravel to redirect all requests to a specific URL. This may be accomplished using the `redirect` option. For example, you may wish to redirect all requests to the `/` URI: -->
점검 모드 동안에는, 사용자가 접속하는 모든 애플리케이션 URL에 점검 모드 화면이 표시됩니다. 하지만 모든 요청을 특정 URL로 리다이렉트할 수도 있습니다. 이를 위해 `redirect` 옵션을 사용할 수 있습니다. 예를 들어, 모든 요청을 `/` 경로로 보낼 수 있습니다.

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
<!-- #### Disabling Maintenance Mode -->
#### Disabling Maintenance Mode

<!-- To disable maintenance mode, use the `up` command: -->
점검 모드를 해제하려면, `up` 명령어를 실행하세요.

```shell
php artisan up
```

> [!NOTE]
> 기본 점검 모드 템플릿은 `resources/views/errors/503.blade.php`에 직접 정의하여 원하는 대로 커스터마이징할 수 있습니다.

<a name="maintenance-mode-queues"></a>
<!-- #### Maintenance Mode and Queues -->
#### Maintenance Mode and Queues

<!-- While your application is in maintenance mode, no [queued jobs](/docs/10.x/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode. -->
애플리케이션이 점검 모드인 동안에는 [queued jobs](/docs/10.x/queues)이 처리되지 않습니다. 점검 모드가 해제되면, 대기 중이던 작업들이 정상적으로 처리되기 시작합니다.

<a name="alternatives-to-maintenance-mode"></a>
<!-- #### Alternatives to Maintenance Mode -->
#### Alternatives to Maintenance Mode

<!-- Since maintenance mode requires your application to have several seconds of downtime, consider alternatives like [Laravel Vapor](https://vapor.laravel.com) and [Envoyer](https://envoyer.io) to accomplish zero-downtime deployment with Laravel. -->
점검 모드는 몇 초 동안이라도 애플리케이션의 다운타임(접속 불가 시간)을 반드시 수반합니다. 그렇기 때문에 Laravel로 무중단 배포(zero-downtime deployment)를 구현하고 싶다면 [Laravel Vapor](https://vapor.laravel.com)나 [Envoyer](https://envoyer.io) 같은 대안을 고려해 보시길 추천합니다.
